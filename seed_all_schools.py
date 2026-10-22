import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school31.db")

all_regions_schools = {
    # Cities
    "Sumqayıt": [f"Sumqayıt şəhər {i} nömrəli tam orta məktəb" for i in range(1, 44)] + [
        "Sumqayıt Təbiət Elmləri Təmayüllü Gimnaziya",
        "Sumqayıt Texniki və Təbiət Elmləri Liseyi"
    ],
    "Bakı": [f"Bakı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 326)] + [
        "Akademik Zərifə Əliyeva adına Lisey",
        "Fizika, riyaziyyat və informatika təmayüllü lisey (FRİTL)",
        "Bakı Avropa Liseyi",
        "Bülbül adına Orta İxtisas Musiqi Məktəbi",
        "Heydər Əliyev adına Müasir Təhsil Kompleksi",
        "Tərəqqi Texniki-Humanitar Liseyi",
        "Elitar Gimnaziya"
    ],
    "Gəncə": [f"Gəncə şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 46)] + [
        "Gəncə şəhər Mir Cəlal Paşayev adına 39 nömrəli tam orta məktəb",
        "Gəncə Fizika, Riyaziyyat və İnformatika Təmayüllü Lisey"
    ],
    "Mingəçevir": [f"Mingəçevir şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 22)] + [
        "Mingəçevir Təbiət-Riyaziyyat və Humanitar Elmlər Təmayüllü Lisey"
    ],
    "Şirvan": [f"Şirvan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 21)] + [
        "Şirvan şəhər Kimya-Biologiya Təmayüllü Lisey"
    ],
    "Naftalan": [f"Naftalan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)],
    "Xankəndi": [
        "Xankəndi şəhər 1 nömrəli tam orta məktəb",
        "Xankəndi şəhər 2 nömrəli tam orta məktəb",
        "Xankəndi şəhər 4 nömrəli tam orta məktəb",
        "Xankəndi şəhər Nizami Gəncəvi adına tam orta məktəb"
    ],
    "Xırdalan": [f"Xırdalan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 11)],
    "Abşeron": [
        "Abşeron rayon Mehdiabad qəsəbə 1 nömrəli tam orta məktəb",
        "Abşeron rayon Mehdiabad qəsəbə 2 nömrəli tam orta məktəb",
        "Abşeron rayon Qobu qəsəbə 1 nömrəli tam orta məktəb",
        "Abşeron rayon Qobu qəsəbə 2 nömrəli tam orta məktəb",
        "Abşeron rayon Masazır kənd 1 nömrəli tam orta məktəb",
        "Abşeron rayon Masazır kənd 2 nömrəli tam orta məktəb",
        "Abşeron rayon Masazır kənd 3 nömrəli tam orta məktəb",
        "Abşeron rayon Masazır kənd 4 nömrəli tam orta məktəb",
        "Abşeron rayon Masazır kənd 5 nömrəli tam orta məktəb",
        "Abşeron rayon Saray qəsəbə 1 nömrəli tam orta məktəb",
        "Abşeron rayon Saray qəsəbə 2 nömrəli tam orta məktəb",
        "Abşeron rayon Saray qəsəbə 3 nömrəli tam orta məktəb",
        "Abşeron rayon Ceyranbatan qəsəbə 1 nömrəli tam orta məktəb",
        "Abşeron rayon Ceyranbatan qəsəbə 2 nömrəli tam orta məktəb",
        "Abşeron rayon Novxanı kənd tam orta məktəbi",
        "Abşeron rayon Fatmayı kənd tam orta məktəbi",
        "Abşeron rayon Digah kənd tam orta məktəbi",
        "Abşeron rayon Görədil kənd tam orta məktəbi",
        "Abşeron rayon Məmmədli kənd tam orta məktəbi"
    ],

    # Qarabağ & Şərqi Zəngəzur
    "Şuşa": [
        "Şuşa şəhər 1 nömrəli tam orta məktəb",
        "Şuşa şəhər 2 nömrəli tam orta məktəb",
        "Şuşa Humanitar İxtisaslaşdırılmış Məktəbi",
        "Şuşa rayon Malıbəyli kənd 1 nömrəli tam orta məktəb"
    ],
    "Ağdam": [f"Ağdam rayon {i} nömrəli tam orta məktəb" for i in range(1, 26)] + [
        "Ağdam şəhər 1 nömrəli tam orta məktəb",
        "Ağdam rayon Quzanlı kənd tam orta məktəbi"
    ],
    "Füzuli": [f"Füzuli rayon {i} nömrəli tam orta məktəb" for i in range(1, 21)] + [
        "Füzuli şəhəri Mirzə Uluqbəy adına 1 nömrəli tam orta məktəb",
        "Füzuli rayon Horadiz şəhər 1 nömrəli tam orta məktəb",
        "Füzuli rayon Horadiz şəhər 2 nömrəli tam orta məktəb"
    ],
    "Cəbrayıl": [f"Cəbrayıl rayon {i} nömrəli tam orta məktəb" for i in range(1, 16)] + [
        "Cəbrayıl şəhəri akademik Mehdi Mehdizadə adına tam orta məktəb",
        "Cəbrayıl rayon Cocuq Mərcanlı kənd tam orta məktəbi"
    ],
    "Zəngilan": [
        "Zəngilan şəhər 1 nömrəli tam orta məktəb",
        "Zəngilan rayon Ağalı kənd tam orta məktəbi",
        "Zəngilan rayon Mincivan qəsəbə tam orta məktəbi"
    ] + [f"Zəngilan rayon {i} nömrəli tam orta məktəb" for i in range(2, 11)],
    "Qubadlı": [f"Qubadlı rayon {i} nömrəli tam orta məktəb" for i in range(1, 16)] + [
        "Qubadlı şəhər 1 nömrəli tam orta məktəb"
    ],
    "Laçın": [
        "Laçın şəhər 1 nömrəli tam orta məktəb",
        "Laçın şəhər 2 nömrəli tam orta məktəb",
        "Laçın rayon Zabux kənd tam orta məktəbi",
        "Laçın rayon Sus kənd tam orta məktəbi"
    ] + [f"Laçın rayon {i} nömrəli tam orta məktəb" for i in range(3, 20)],
    "Kəlbəcər": [f"Kəlbəcər rayon {i} nömrəli tam orta məktəb" for i in range(1, 21)] + [
        "Kəlbəcər şəhər 1 nömrəli tam orta məktəb"
    ],
    "Xocalı": [
        "Xocalı şəhər 1 nömrəli tam orta məktəb",
        "Xocalı rayon Əsgəran qəsəbə tam orta məktəbi"
    ] + [f"Xocalı rayon {i} nömrəli tam orta məktəb" for i in range(2, 8)],
    "Xocavənd": [
        "Xocavənd şəhər 1 nömrəli tam orta məktəb",
        "Xocavənd rayon Hadrut qəsəbə tam orta məktəbi"
    ] + [f"Xocavənd rayon {i} nömrəli tam orta məktəb" for i in range(2, 8)],
    "Ağdərə": [
        "Ağdərə şəhər 1 nömrəli tam orta məktəb",
        "Ağdərə rayon Suqovuşan kənd tam orta məktəbi"
    ] + [f"Ağdərə rayon {i} nömrəli tam orta məktəb" for i in range(2, 6)],

    # Şimal (Quba-Xaçmaz)
    "Quba": [f"Quba şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 10)] + [
        "Quba rayon Qırmızı Qəsəbə 1 nömrəli tam orta məktəb",
        "Quba rayon Birinci Nügədi kənd 1 nömrəli tam orta məktəb",
        "Quba rayon İkinci Nügədi kənd 1 nömrəli tam orta məktəb"
    ],
    "Qusar": [f"Qusar şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 8)] + [
        "Qusar rayon Samur qəsəbə tam orta məktəbi",
        "Qusar rayon Hil kənd tam orta məktəbi"
    ],
    "Xaçmaz": [f"Xaçmaz şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 10)] + [
        "Xaçmaz rayon Xudat şəhər 1 nömrəli tam orta məktəb",
        "Xaçmaz rayon Xudat şəhər 2 nömrəli tam orta məktəb",
        "Xaçmaz rayon Nabran kənd tam orta məktəbi",
        "Xaçmaz rayon Yalama kənd tam orta məktəbi"
    ],
    "Şabran": [f"Şabran şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Şabran rayon Dəvəçibazar kənd tam orta məktəbi"
    ],
    "Siyəzən": [f"Siyəzən şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Siyəzən rayon Zarat kənd tam orta məktəbi"
    ],
    "Xızı": [
        "Xızı şəhər Mikayıl Müşfiq adına tam orta məktəb",
        "Xızı rayon Altıağac qəsəbə tam orta məktəbi",
        "Xızı rayon Giləzi kənd tam orta məktəbi"
    ],

    # Şimal-Qərb (Şəki-Zaqatala)
    "Şəki": [f"Şəki şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 21)] + [
        "Şəki Kimya-Biologiya Təmayüllü Lisey",
        "Şəki şəhər Fizika-Riyaziyyat Təmayüllü Lisey"
    ],
    "Zaqatala": [f"Zaqatala şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 8)] + [
        "Zaqatala rayon Əliabad qəsəbə 1 nömrəli tam orta məktəb",
        "Zaqatala rayon Tala kənd 1 nömrəli tam orta məktəb"
    ],
    "Balakən": [f"Balakən şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Balakən rayon Qabaqçöl qəsəbə tam orta məktəbi",
        "Balakən rayon Talalar kənd tam orta məktəbi"
    ],
    "Qax": [f"Qax şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Qax rayon İlisu kənd tam orta məktəbi",
        "Qax rayon Qum kənd tam orta məktəbi"
    ],
    "Qəbələ": [f"Qəbələ şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Qəbələ rayon Vəndam qəsəbə 1 nömrəli tam orta məktəb",
        "Qəbələ rayon Nic qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Oğuz": [f"Oğuz şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Oğuz rayon Kərimli kənd tam orta məktəbi"
    ],

    # Dağlıq Şirvan
    "Şamaxı": [f"Şamaxı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 8)] + [
        "Şamaxı rayon Avaxıl kənd tam orta məktəbi",
        "Şamaxı rayon Sabir qəsəbə tam orta məktəbi"
    ],
    "İsmayıllı": [f"İsmayıllı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 8)] + [
        "İsmayıllı rayon Lahıc qəsəbə tam orta məktəbi",
        "İsmayıllı rayon İvanovka kənd tam orta məktəbi"
    ],
    "Ağsu": [f"Ağsu şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Ağsu rayon Qaraqoyunlu kənd tam orta məktəbi"
    ],
    "Qobustan": [f"Qobustan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],

    # Mərkəzi Aran
    "Yevlax": [f"Yevlax şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 11)] + [
        "Yevlax rayon Qaramanlı kənd tam orta məktəbi"
    ],
    "Ağdaş": [f"Ağdaş şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 9)] + [
        "Ağdaş rayon Ləki qəsəbə tam orta məktəbi"
    ],
    "Göyçay": [f"Göyçay şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 10)] + [
        "Göyçay şəhər İnteqrasiya Təlimli İnternat Tipli Gimnaziya"
    ],
    "Ucar": [f"Ucar şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 7)],
    "Zərdab": [f"Zərdab şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],
    "Kürdəmir": [f"Kürdəmir şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 7)] + [
        "Kürdəmir rayon Karrar qəsəbə tam orta məktəbi"
    ],

    # Mil-Muğan
    "Bərdə": [f"Bərdə şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 10)] + [
        "Bərdə rayon Güloğlular kənd tam orta məktəbi"
    ],
    "Tərtər": [f"Tərtər şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 7)] + [
        "Tərtər rayon Şıxarx qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Ağcabədi": [f"Ağcabədi şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 12)] + [
        "Ağcabədi rayon Hindarx qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Beyləqan": [f"Beyləqan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Beyləqan rayon Mil qəsəbə tam orta məktəbi"
    ],
    "İmişli": [f"İmişli şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 8)] + [
        "İmişli rayon Bəhrəmtəpə qəsəbə tam orta məktəbi"
    ],
    "Saatlı": [f"Saatlı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)],
    "Sabirabad": [f"Sabirabad şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 9)] + [
        "Sabirabad rayon Qalağayın kənd tam orta məktəbi"
    ],

    # Cənub (Lənkəran-Astara)
    "Lənkəran": [f"Lənkəran şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 11)] + [
        "Lənkəran şəhər Xarici Dillər Təmayüllü Gimnaziya",
        "Lənkəran rayon Liman şəhər 1 nömrəli tam orta məktəb",
        "Lənkəran rayon Haftoni qəsəbə tam orta məktəbi"
    ],
    "Masallı": [f"Masallı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Masallı rayon Boradigah qəsəbə 1 nömrəli tam orta məktəb",
        "Masallı rayon Ərkivan qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Cəlilabad": [f"Cəlilabad şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 9)] + [
        "Cəlilabad rayon Göytəpə şəhər 1 nömrəli tam orta məktəb"
    ],
    "Astara": [f"Astara şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 7)] + [
        "Astara rayon Ərçivan qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Lerik": [f"Lerik şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],
    "Yardımlı": [f"Yardımlı şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],

    # Şirvan-Salyan
    "Salyan": [f"Salyan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 10)],
    "Neftçala": [f"Neftçala şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Neftçala rayon Bankə qəsəbə 1 nömrəli tam orta məktəb"
    ],
    "Biləsuvar": [f"Biləsuvar şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Biləsuvar rayon Mübariz İbrahimov adına Lisey-Məktəb Kompleksi"
    ],
    "Hacıqabul": [f"Hacıqabul şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)],

    # Qazax-Tovuz
    "Qazax": [f"Qazax şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Qazax Müəllimlər Seminariyası",
        "Qazax rayon Çaylı kənd 1 nömrəli tam orta məktəb"
    ],
    "Ağstafa": [f"Ağstafa şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Ağstafa rayon Poylu qəsəbə tam orta məktəbi"
    ],
    "Tovuz": [f"Tovuz şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Tovuz rayon Qovlar şəhər tam orta məktəbi",
        "Tovuz rayon Düz Qırıqlı kənd tam orta məktəbi"
    ],
    "Şəmkir": [f"Şəmkir şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Şəmkir rayon Dəllər qəsəbə tam orta məktəbi",
        "Şəmkir rayon Çinarlı qəsəbə tam orta məktəbi"
    ],
    "Gədəbəy": [f"Gədəbəy şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Gədəbəy rayon Slavyanka kənd 1 nömrəli tam orta məktəb"
    ],

    # Gəncə-Daşkəsən
    "Göygöl": [f"Göygöl şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Göygöl rayon Hacıkənd qəsəbə tam orta məktəbi"
    ],
    "Daşkəsən": [f"Daşkəsən şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],
    "Samux": [f"Samux şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],
    "Goranboy": [f"Goranboy şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Goranboy rayon Dəliməmmədli şəhər tam orta məktəbi"
    ],

    # Naxçıvan Muxtar Respublikası
    "Naxçıvan": [f"Naxçıvan şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 18)] + [
        "Heydər Əliyev adına Hərbi Lisey",
        "Naxçıvan Qızlar Liseyi"
    ],
    "Babək": [f"Babək şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 4)] + [
        "Babək rayon Nehrəm kənd 1 nömrəli tam orta məktəb",
        "Babək rayon Nehrəm kənd 2 nömrəli tam orta məktəb",
        "Babək rayon Cəhri kənd 1 nömrəli tam orta məktəb"
    ],
    "Culfa": [f"Culfa şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)],
    "Ordubad": [f"Ordubad şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 5)] + [
        "Ordubad rayon Vənənd kənd tam orta məktəbi"
    ],
    "Sədərək": [
        "Sədərək kənd 1 nömrəli tam orta məktəb",
        "Sədərək kənd 2 nömrəli tam orta məktəb",
        "Heydərabad qəsəbə tam orta məktəbi"
    ],
    "Şahbuz": [f"Şahbuz şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 4)] + [
        "Şahbuz rayon Badamlı qəsəbə tam orta məktəbi"
    ],
    "Şərur": [f"Şərur şəhəri {i} nömrəli tam orta məktəb" for i in range(1, 6)] + [
        "Şərur rayon Yengicə kənd tam orta məktəbi"
    ],
    "Kəngərli": [
        "Kəngərli rayon Qıvraq qəsəbə tam orta məktəbi",
        "Kəngərli rayon Şahtaxtı kənd tam orta məktəbi",
        "Kəngərli rayon Çalxanqala kənd tam orta məktəbi"
    ]
}

def seed_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count_added = 0
    for reg, school_list in all_regions_schools.items():
        for s_name in school_list:
            try:
                cursor.execute("INSERT OR IGNORE INTO schools (name, region) VALUES (?, ?)", (s_name.strip(), reg.strip()))
                if cursor.rowcount > 0:
                    count_added += 1
            except Exception:
                pass

    conn.commit()

    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT region) FROM schools")
    total_schools, total_regions = cursor.fetchone()
    print(f"Added {count_added} new schools. Total schools in DB: {total_schools} across {total_regions} regions/cities!")
    conn.close()

if __name__ == "__main__":
    seed_all()
