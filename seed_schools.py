import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school31.db")

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        region TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Columns in users
    cursor.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cursor.fetchall()]
    if 'school_id' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN school_id INTEGER DEFAULT 1")
    if 'is_moderator' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN is_moderator INTEGER DEFAULT 0")

    # Columns in classes
    cursor.execute("PRAGMA table_info(classes)")
    c_cols = [c[1] for c in cursor.fetchall()]
    if 'school_id' not in c_cols:
        cursor.execute("ALTER TABLE classes ADD COLUMN school_id INTEGER DEFAULT 1")

    # Generate Republic-wide Schools
    schools = [
        ("Sumqayıt şəhər 31 nömrəli tam orta məktəb", "Sumqayıt"),
    ]

    # Sumqayıt (1-43)
    for i in range(1, 44):
        if i != 31:
            schools.append((f"Sumqayıt şəhər {i} nömrəli tam orta məktəb", "Sumqayıt"))

    # Bakı (1-325)
    for i in range(1, 326):
        schools.append((f"Bakı şəhəri {i} nömrəli tam orta məktəb", "Bakı"))
    
    # Bakı Famous Lyceums
    schools.extend([
        ("Akademik Zərifə Əliyeva adına Lisey", "Bakı"),
        ("Fizika, riyaziyyat və informatika təmayüllü lisey", "Bakı"),
        ("Bakı Avropa Liseyi", "Bakı"),
        ("Bülbül adına Orta İxtisas Musiqi Məktəbi", "Bakı"),
        ("Heydər Əliyev adına Müasir Təhsil Kompleksi", "Bakı"),
    ])

    # Gəncə (1-45)
    for i in range(1, 46):
        schools.append((f"Gəncə şəhəri {i} nömrəli tam orta məktəb", "Gəncə"))

    # Abşeron
    for i in range(1, 11):
        schools.append((f"Xırdalan şəhər {i} nömrəli tam orta məktəb", "Abşeron"))
    schools.extend([
        ("Saray qəsəbə 1 nömrəli tam orta məktəb", "Abşeron"),
        ("Saray qəsəbə 2 nömrəli tam orta məktəb", "Abşeron"),
        ("Mehdiabad qəsəbə 1 nömrəli tam orta məktəb", "Abşeron"),
        ("Mehdiabad qəsəbə 2 nömrəli tam orta məktəb", "Abşeron"),
        ("Masazır kənd 1 nömrəli tam orta məktəb", "Abşeron"),
        ("Masazır kənd 2 nömrəli tam orta məktəb", "Abşeron"),
        ("Qobu qəsəbə 1 nömrəli tam orta məktəb", "Abşeron"),
        ("Novxanı kənd tam orta məktəbi", "Abşeron"),
    ])

    # Azad olunmuş ərazilər
    schools.extend([
        ("Şuşa şəhər 1 nömrəli tam orta məktəb", "Şuşa"),
        ("Xankəndi şəhər 4 nömrəli tam orta məktəb", "Xankəndi"),
        ("Laçın şəhər 2 nömrəli tam orta məktəb", "Laçın"),
        ("Füzuli şəhər Mirzə Uluqbəy adına 1 nömrəli tam orta məktəb", "Füzuli"),
        ("Ağdam şəhər 1 nömrəli tam orta məktəb", "Ağdam"),
        ("Zəngilan rayon Ağalı kənd tam orta məktəbi", "Zəngilan"),
        ("Kəlbəcər şəhər 1 nömrəli tam orta məktəb", "Kəlbəcər"),
        ("Cəbrayıl şəhər Mehdi Mehdizadə adına tam orta məktəb", "Cəbrayıl"),
    ])

    # Mingəçevir (1-20)
    for i in range(1, 21):
        schools.append((f"Mingəçevir şəhər {i} nömrəli tam orta məktəb", "Mingəçevir"))

    # Şirvan (1-21)
    for i in range(1, 22):
        schools.append((f"Şirvan şəhər {i} nömrəli tam orta məktəb", "Şirvan"))

    # Naxçıvan (1-17)
    for i in range(1, 18):
        schools.append((f"Naxçıvan şəhər {i} nömrəli tam orta məktəb", "Naxçıvan"))

    # Digər Rayon Mərkəzləri
    regions = [
        "Lənkəran", "Şəki", "Quba", "Xaçmaz", "Şamaxı", "Qəbələ", "Zaqatala",
        "Bərdə", "Tovuz", "Şəmkir", "Cəlilabad", "Masallı", "İmişli", "Göyçay",
        "Salyan", "Goranboy", "Beyləqan", "Qazax", "Ağstafa", "Balakən", "İsmayıllı"
    ]
    for r in regions:
        for i in range(1, 11):
            schools.append((f"{r} şəhər {i} nömrəli tam orta məktəb", r))

    for name, reg in schools:
        cursor.execute("INSERT OR IGNORE INTO schools (name, region) VALUES (?, ?)", (name, reg))

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM schools")
    total = cursor.fetchone()[0]
    print(f"Total schools seeded: {total}")
    conn.close()

if __name__ == "__main__":
    seed()
