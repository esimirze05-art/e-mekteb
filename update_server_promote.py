import os

server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
with open(server_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace E.məktəb with E-məktəb
text = text.replace("E.məktəb", "E-məktəb")

# Add promote endpoints after admin_delete_class
target = '''@app.delete("/api/admin/classes/{class_id}")
def admin_delete_class(class_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
    cursor.execute("UPDATE users SET class_id = NULL WHERE class_id = ?", (class_id,))
    cursor.execute("UPDATE users SET class_head_id = NULL WHERE class_head_id = ?", (class_id,))
    conn.commit()
    conn.close()
    return {"success": True}'''

new_endpoints = '''@app.delete("/api/admin/classes/{class_id}")
def admin_delete_class(class_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
    cursor.execute("UPDATE users SET class_id = NULL WHERE class_id = ?", (class_id,))
    cursor.execute("UPDATE users SET class_head_id = NULL WHERE class_head_id = ?", (class_id,))
    conn.commit()
    conn.close()
    return {"success": True}

# Promote single class (grade increments by 1, section/index stays identical)
@app.post("/api/admin/classes/{class_id}/promote")
def promote_class(class_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, section, school_id FROM classes WHERE id = ?", (class_id,))
    cls = cursor.fetchone()
    if not cls:
        conn.close()
        raise HTTPException(status_code=404, detail="Sinif tapılmadı")
    
    current_grade = cls["grade"]
    section = cls["section"]
    school_id = cls["school_id"]

    if current_grade >= 11:
        cursor.execute("UPDATE users SET class_id = NULL WHERE class_id = ? AND role = 'student'", (class_id,))
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        conn.close()
        return {"success": True, "graduated": True, "message": f"{cls['name']} sinfi 11-ci sinfi bitirdi və məzun oldu! 🎓"}

    new_grade = current_grade + 1
    new_name = f"{new_grade}{section}"

    cursor.execute("SELECT id FROM classes WHERE name = ? AND school_id = ?", (new_name, school_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE users SET class_id = ? WHERE class_id = ?", (existing["id"], class_id))
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        conn.close()
        return {"success": True, "new_name": new_name, "message": f"Şagirdlər mövcud {new_name} sinfinə keçirildi!"}
    else:
        cursor.execute("UPDATE classes SET grade = ?, name = ? WHERE id = ?", (new_grade, new_name, class_id))
        conn.commit()
        conn.close()
        return {"success": True, "new_name": new_name, "message": f"Sinif {new_name} sinfinə yüksəldildi (indeks: {section})!"}

# Batch promote all classes in school by 1 year (11th graduates, index stays identical)
@app.post("/api/admin/schools/{school_id}/promote-all-classes")
def promote_all_classes_in_school(school_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, section FROM classes WHERE school_id = ? ORDER BY grade DESC", (school_id,))
    classes = [dict(c) for c in cursor.fetchall()]
    
    promoted_count = 0
    graduated_count = 0

    for cls in classes:
        c_grade = cls["grade"]
        c_sec = cls["section"]
        c_id = cls["id"]

        if c_grade >= 11:
            cursor.execute("UPDATE users SET class_id = NULL WHERE class_id = ? AND role = 'student'", (c_id,))
            cursor.execute("DELETE FROM classes WHERE id = ?", (c_id,))
            graduated_count += 1
        else:
            new_g = c_grade + 1
            new_n = f"{new_g}{c_sec}"
            cursor.execute("SELECT id FROM classes WHERE name = ? AND school_id = ?", (new_n, school_id))
            target = cursor.fetchone()
            if target:
                cursor.execute("UPDATE users SET class_id = ? WHERE class_id = ?", (target["id"], c_id))
                cursor.execute("DELETE FROM classes WHERE id = ?", (c_id,))
            else:
                cursor.execute("UPDATE classes SET grade = ?, name = ? WHERE id = ?", (new_g, new_n, c_id))
            promoted_count += 1
            
    conn.commit()
    conn.close()
    return {
        "success": True, 
        "promoted_count": promoted_count, 
        "graduated_count": graduated_count,
        "message": f"{promoted_count} sinif növbəti sinfə keçirildi (indekslər qorundu), {graduated_count} sinif məzun oldu!"
    }'''

assert target in text, "target not found in server.py"
text = text.replace(target, new_endpoints, 1)

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: server.py updated with class promotion & E-məktəb!")
