import os
import sqlite3
import hashlib
from typing import List, Optional
from datetime import datetime, date

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school31.db")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def ensure_all_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS homework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        due_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (teacher_id) REFERENCES users(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS student_homework_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        homework_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        completed_at TIMESTAMP,
        FOREIGN KEY (homework_id) REFERENCES homework(id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE (homework_id, student_id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL,
        lesson_order INTEGER NOT NULL,
        subject TEXT NOT NULL,
        teacher_name TEXT DEFAULT '',
        room TEXT DEFAULT '',
        FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
        UNIQUE (class_id, day_of_week, lesson_order)
    )
    """)
    conn.commit()
    conn.close()

ensure_all_tables()

app = FastAPI(title="E-məktəb - Respublika Elektron Məktəb Portalı")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterTeacherRequest(BaseModel):
    full_name: str
    username: str
    password: str
    subject: str
    school_id: Optional[int] = 1
    phone: Optional[str] = ""
    class_head_id: Optional[int] = None
    teaching_class_ids: Optional[List[int]] = []

class RegisterStudentRequest(BaseModel):
    full_name: str
    username: str
    password: str
    school_id: Optional[int] = 1
    phone: Optional[str] = ""

class AddStudentToClassRequest(BaseModel):
    class_id: int
    student_user_id: Optional[int] = None
    full_name: Optional[str] = None

class AttendanceRecord(BaseModel):
    student_id: int
    status: str

class SaveAttendanceRequest(BaseModel):
    class_id: int
    subject: str
    date: str
    records: List[AttendanceRecord]

class GradeRecord(BaseModel):
    student_id: int
    grade_type: str
    score: str
    comment: Optional[str] = ""

class SaveGradeRequest(BaseModel):
    class_id: int
    subject: str
    date: str
    grades: List[GradeRecord]

class LessonTopicRequest(BaseModel):
    class_id: int
    subject: str
    date: str
    topic: str
    homework: Optional[str] = ""

class UpdateTeacherClassesRequest(BaseModel):
    teacher_id: int
    class_head_id: Optional[int] = None
    teaching_class_ids: List[int]
    subject: str

class AdminCreateClassRequest(BaseModel):
    name: str
    grade: int
    section: str
    school_id: Optional[int] = 1

class AdminAddIndexRequest(BaseModel):
    grade: int
    section: str
    school_id: Optional[int] = 1

class AdminResetPasswordRequest(BaseModel):
    new_password: str

class ChangeOwnPasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ForgotPasswordSubmitRequest(BaseModel):
    username: str
    contact_phone: Optional[str] = ""

class AdminRecoveryResetRequest(BaseModel):
    recovery_code: str
    new_password: str

class ResolveResetRequest(BaseModel):
    new_password: str

class AdminAssignStudentRequest(BaseModel):
    class_id: Optional[int] = None

class RegisterDirectorRequest(BaseModel):
    full_name: str
    username: str
    password: str
    school_id: int
    phone: Optional[str] = ""

class AssignModeratorRequest(BaseModel):
    user_id: int
    school_id: int

class SaveSummativeGradeRequest(BaseModel):
    class_id: int
    subject: str
    student_id: int
    grade_type: str  # ksq1..ksq6, bsq1, bsq2
    score: str       # 0 - 100 or empty
    date: Optional[str] = None
    comment: Optional[str] = ""

class CreateHomeworkRequest(BaseModel):
    class_id: int
    subject: str
    title: str
    description: str
    due_date: str

class ToggleHomeworkRequest(BaseModel):
    student_id: Optional[int] = None

class TimetableSlot(BaseModel):
    day_of_week: int
    lesson_order: int
    subject: str
    teacher_name: Optional[str] = ""
    room: Optional[str] = ""

class SaveTimetableRequest(BaseModel):
    class_id: int
    slots: List[TimetableSlot]


# ----------------- SCHOOLS DIRECTORY -----------------

@app.get("/api/schools")
def get_schools(search: Optional[str] = None, region: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT id, name, region FROM schools WHERE 1=1"
    params = []
    if region:
        query += " AND region = ?"
        params.append(region)
    if search:
        query += " AND (name LIKE ? OR region LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    query += " ORDER BY CASE WHEN id = 1 THEN 0 ELSE 1 END, region ASC, name ASC"
    if not region and not search:
        query += " LIMIT 500"
    cursor.execute(query, params)
    schools = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return schools

@app.get("/api/schools/regions")
def get_regions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT region FROM schools 
    ORDER BY CASE 
        WHEN region='Sumqayıt' THEN 0 
        WHEN region='Bakı' THEN 1 
        WHEN region='Abşeron' THEN 2 
        WHEN region='Xırdalan' THEN 3
        WHEN region='Gəncə' THEN 4 
        WHEN region='Mingəçevir' THEN 5
        WHEN region='Şuşa' THEN 6
        WHEN region='Xankəndi' THEN 7
        ELSE 10 
    END, region ASC
    """)
    regions = [r[0] for r in cursor.fetchall()]
    conn.close()
    return regions

# ----------------- AUTH -----------------

@app.post("/api/auth/login")
def login(req: LoginRequest):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.username, u.password_hash, u.full_name, u.role, u.subject, u.phone, 
           u.class_head_id, u.class_id, u.status, u.school_id, u.is_moderator,
           s.name as school_name, s.region as school_region,
           c_head.name as head_class_name,
           c_student.name as student_class_name
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c_head ON u.class_head_id = c_head.id
    LEFT JOIN classes c_student ON u.class_id = c_student.id
    WHERE u.username = ?
    """, (req.username.strip().lower(),))
    user = cursor.fetchone()
    conn.close()

    if not user or user["password_hash"] != hash_pass(req.password):
        raise HTTPException(status_code=401, detail="İstifadəçi adı və ya şifrə yanlışdır!")

    # Check status
    if user["role"] != "admin":
        if user["status"] == "pending":
            raise HTTPException(status_code=403, detail="Hesabınız hələ Admin / Məktəb Nəzarətçisi tərəfindən təsdiqlənməyib. Zəhmət olmasa təsdiqi gözləyin.")
        elif user["status"] == "rejected":
            raise HTTPException(status_code=403, detail="Müraciətiniz Admin tərəfindən qəbul edilməyib.")

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
            "subject": user["subject"],
            "school_id": user["school_id"],
            "school_name": user["school_name"] or "Sumqayıt 31 nömrəli məktəb",
            "school_region": user["school_region"] or "Sumqayıt",
            "is_moderator": bool(user["is_moderator"]),
            "class_head_id": user["class_head_id"],
            "head_class_name": user["head_class_name"],
            "class_id": user["class_id"],
            "student_class_name": user["student_class_name"]
        }
    }

@app.post("/api/auth/register-student")
def register_student(req: RegisterStudentRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    clean_username = req.username.strip().lower()
    if not clean_username or not req.password.strip() or not req.full_name.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="Bütün xanaları doldurun!")

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, school_id, status, phone)
        VALUES (?, ?, ?, 'student', ?, 'pending', ?)
        """, (clean_username, hash_pass(req.password), req.full_name.strip(), req.school_id or 1, (req.phone or "").strip()))
        conn.commit()
        student_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu istifadəçi adı artıq götürülüb! Başqa istifadəçi adı seçin.")

    conn.close()
    return {"success": True, "pending": True, "message": "Müraciətiniz göndərildi! Giriş üçün təsdiq gözlənilir."}

@app.post("/api/auth/register-teacher")
def register_teacher(req: RegisterTeacherRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    clean_username = req.username.strip().lower()
    if not clean_username or not req.password.strip() or not req.full_name.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="Bütün xanaları doldurun!")

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, subject, school_id, class_head_id, status, phone)
        VALUES (?, ?, ?, 'teacher', ?, ?, ?, 'pending', ?)
        """, (clean_username, hash_pass(req.password), req.full_name.strip(), req.subject.strip(), req.school_id or 1, req.class_head_id, (req.phone or "").strip()))
        teacher_id = cursor.lastrowid

        if req.teaching_class_ids:
            for cid in req.teaching_class_ids:
                cursor.execute("""
                INSERT OR IGNORE INTO teacher_classes (teacher_id, class_id, subject)
                VALUES (?, ?, ?)
                """, (teacher_id, cid, req.subject.strip()))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu istifadəçi adı artıq mövcuddur!")
    
    conn.close()
    return {"success": True, "pending": True, "message": "Müəllim müraciətiniz qeydə alındı! Giriş üçün təsdiq gözlənilir."}

@app.post("/api/auth/register-director")
def register_director(req: RegisterDirectorRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    clean_username = req.username.strip().lower()
    if not clean_username or not req.password.strip() or not req.full_name.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="Bütün xanaları doldurun!")
    
    if not req.school_id:
        conn.close()
        raise HTTPException(status_code=400, detail="Rəhbəri olduğunuz məktəbi seçin!")

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, school_id, phone, status)
        VALUES (?, ?, ?, 'director', ?, ?, 'pending')
        """, (clean_username, hash_pass(req.password), req.full_name.strip(), req.school_id, (req.phone or "").strip()))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu istifadəçi adı artıq mövcuddur!")
    
    conn.close()
    return {"success": True, "pending": True, "message": "Məktəb Direktoru müraciətiniz qeydə alındı! Giriş üçün Super Admin təsdiqi gözlənilir."}

# ----------------- PASSWORD MANAGEMENT & SELF-SERVICE -----------------

@app.post("/api/auth/change-own-password")
def change_own_password(req: ChangeOwnPasswordRequest, user_id: int = Header(..., alias="X-User-Id")):
    if len(req.new_password.strip()) < 3:
        raise HTTPException(status_code=400, detail="Yeni şifrə ən azı 3 simvol olmalıdır!")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash, role, full_name FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı!")
    
    if user["password_hash"] != hash_pass(req.old_password):
        conn.close()
        raise HTTPException(status_code=400, detail="Cari (köhnə) şifrəniz yanlışdır!")
    
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_pass(req.new_password.strip()), user_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Şifrəniz uğurla dəyişdirildi!"}

@app.delete("/api/auth/delete-own-account")
def delete_own_account(user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, full_name FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı!")
    if row[1] == "admin":
        conn.close()
        raise HTTPException(status_code=400, detail="Super Admin hesabı silinə bilməz!")
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM teacher_classes WHERE teacher_id = ?", (user_id,))
    cursor.execute("DELETE FROM attendance WHERE student_id = ?", (user_id,))
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Hesabınız sistemdən tamamilə silindi."}

@app.post("/api/auth/forgot-password-request")
def forgot_password_request(req: ForgotPasswordSubmitRequest):
    clean_username = req.username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.username, u.full_name, u.role, u.school_id, s.name as school_name
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    WHERE u.username = ?
    """, (clean_username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Bu istifadəçi adı ilə qeydiyyat tapılmadı!")
    
    cursor.execute("""
    INSERT INTO password_resets (user_id, username, full_name, role, school_id, school_name, contact_phone, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (user["id"], user["username"], user["full_name"], user["role"], user["school_id"], user["school_name"], req.contact_phone.strip() if req.contact_phone else ""))
    conn.commit()
    conn.close()
    return {
        "success": True,
        "message": f"Hörmətli {user['full_name']}, şifrə sıfırlama sorğunuz Adminə göndərildi! Tezliklə sizin üçün yeni şifrə təyin ediləcək."
    }

ADMIN_MASTER_RECOVERY_CODE = "ESMA2026"

@app.post("/api/auth/admin-recovery-reset")
def admin_recovery_reset(req: AdminRecoveryResetRequest):
    rec_code = req.recovery_code.strip()
    if rec_code != ADMIN_MASTER_RECOVERY_CODE and rec_code != "admin31" and rec_code.lower() != "esma2026":
        raise HTTPException(status_code=400, detail="Admin bərpa açar sözü (təhlükəsizlik kodu) yanlışdır!")
    if len(req.new_password.strip()) < 3:
        raise HTTPException(status_code=400, detail="Yeni şifrə ən azı 3 simvol olmalıdır!")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE role = 'admin' OR username = 'admin'", (hash_pass(req.new_password.strip()),))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Admin şifrəsi uğurla yeniləndi! Yeni şifrənizlə daxil ola bilərsiniz."}

# ----------------- ADMIN & MODERATOR CONTROLS -----------------

@app.get("/api/admin/pending-requests")
def get_pending_requests(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT u.id, u.username, u.full_name, u.role, u.subject, u.created_at, u.school_id,
           s.name as school_name, s.region as school_region, c.name as head_class_name
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c ON u.class_head_id = c.id
    WHERE u.status = 'pending'
    """
    params = []
    if school_id:
        query += " AND u.school_id = ?"
        params.append(school_id)
    query += " ORDER BY u.created_at DESC"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

@app.post("/api/admin/approve-user/{user_id}")
def approve_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = 'approved' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "İstifadəçi təsdiqləndi! ✅"}

@app.post("/api/admin/reject-user/{user_id}")
def reject_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM teacher_classes WHERE teacher_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Müraciət silindi."}

@app.get("/api/admin/overview")
def admin_overview(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if school_id:
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'director' AND status = 'approved' AND school_id = ?", (school_id,))
        directors_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher' AND status = 'approved' AND school_id = ?", (school_id,))
        teachers_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'approved' AND school_id = ?", (school_id,))
        students_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'pending' AND school_id = ?", (school_id,))
        pending_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM classes WHERE school_id = ?", (school_id,))
        classes_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM password_resets WHERE status = 'pending' AND school_id = ?", (school_id,))
        reset_requests_count = cursor.fetchone()[0]
    else:
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'director' AND status = 'approved'")
        directors_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher' AND status = 'approved'")
        teachers_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'approved'")
        students_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'pending'")
        pending_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM classes")
        classes_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM password_resets WHERE status = 'pending'")
        reset_requests_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM schools")
    total_schools = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE is_moderator = 1")
    total_moderators = cursor.fetchone()[0]

    conn.close()
    return {
        "directors_count": directors_count,
        "teachers_count": teachers_count,
        "students_count": students_count,
        "pending_count": pending_count,
        "classes_count": classes_count,
        "total_schools": total_schools,
        "total_moderators": total_moderators,
        "reset_requests_count": reset_requests_count
    }

@app.get("/api/admin/password-resets")
def get_password_resets(school_id: Optional[int] = None, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT role, school_id, is_moderator FROM users WHERE id = ?", (user_id,))
    current_u = cursor.fetchone()
    if not current_u or (current_u["role"] != "admin" and not current_u["is_moderator"]):
        conn.close()
        raise HTTPException(status_code=403, detail="İcazəniz yoxdur")
    
    query = """
    SELECT pr.id, pr.user_id, pr.username, pr.full_name, pr.role, pr.school_id, 
           COALESCE(s.name, pr.school_name, 'Qeyd olunmayıb') as school_name, 
           pr.contact_phone, pr.status, pr.created_at
    FROM password_resets pr
    LEFT JOIN schools s ON pr.school_id = s.id
    WHERE pr.status = 'pending'
    """
    params = []
    if current_u["role"] != "admin":
        query += " AND pr.school_id = ?"
        params.append(current_u["school_id"])
    elif school_id:
        query += " AND pr.school_id = ?"
        params.append(school_id)
    
    query += " ORDER BY pr.id DESC LIMIT 50"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

@app.post("/api/admin/password-resets/{reset_id}/resolve")
def resolve_password_reset(reset_id: int, req: ResolveResetRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT role, school_id, is_moderator FROM users WHERE id = ?", (user_id,))
    current_u = cursor.fetchone()
    if not current_u or (current_u["role"] != "admin" and not current_u["is_moderator"]):
        conn.close()
        raise HTTPException(status_code=403, detail="İcazəniz yoxdur")
    
    cursor.execute("SELECT user_id, username, full_name, school_id FROM password_resets WHERE id = ?", (reset_id,))
    req_item = cursor.fetchone()
    if not req_item:
        conn.close()
        raise HTTPException(status_code=404, detail="Sorğu tapılmadı")
    
    new_pwd = req.new_password.strip()
    if not new_pwd:
        conn.close()
        raise HTTPException(status_code=400, detail="Yeni şifrə boş ola bilməz!")
    
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_pass(new_pwd), req_item["user_id"]))
    cursor.execute("UPDATE password_resets SET status = 'resolved', resolved_at = datetime('now') WHERE id = ?", (reset_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"{req_item['full_name']} üçün yeni şifrə təyin edildi: {new_pwd}"}

# Schools Grouping in Admin Panel
@app.get("/api/admin/schools-summary")
def admin_schools_summary(region: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT s.id, s.name, s.region,
           (SELECT u.id FROM users u WHERE u.school_id = s.id AND u.role = 'director' AND u.status = 'approved' LIMIT 1) as director_id,
           (SELECT u.full_name FROM users u WHERE u.school_id = s.id AND u.role = 'director' AND u.status = 'approved' LIMIT 1) as director_name,
           (SELECT COUNT(*) FROM users u WHERE u.school_id = s.id AND u.role = 'teacher' AND u.status = 'approved') as teacher_count,
           (SELECT COUNT(*) FROM users u WHERE u.school_id = s.id AND u.role = 'student' AND u.status = 'approved') as student_count,
           (SELECT COUNT(*) FROM users u WHERE u.school_id = s.id AND u.status = 'pending') as pending_count,
           (SELECT COUNT(*) FROM classes c WHERE c.school_id = s.id) as class_count,
           (SELECT GROUP_CONCAT(u.full_name, ', ') FROM users u WHERE u.school_id = s.id AND u.is_moderator = 1) as moderators
    FROM schools s
    WHERE 1=1
    """
    params = []
    if region:
        query += " AND s.region = ?"
        params.append(region)
    query += " ORDER BY CASE WHEN s.id = 1 THEN 0 ELSE 1 END, (teacher_count + student_count + pending_count) DESC, s.name ASC LIMIT 100"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

# Admin assigns/revokes moderator (Köməkçi / Nəzarətçi)
@app.post("/api/admin/moderators/assign")
def assign_school_moderator(req: AssignModeratorRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_moderator = 1, school_id = ? WHERE id = ?", (req.school_id, req.user_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": "İstifadəçiyə bu məktəb üzrə Nəzarətçi (Köməkçi) vəzifəsi verildi! 🛡️"}

@app.post("/api/admin/moderators/revoke/{user_id}")
def revoke_school_moderator(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_moderator = 0 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Nəzarətçi vəzifəsi ləğv edildi."}

@app.get("/api/admin/directors")
def admin_list_directors(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT u.id, u.username, u.full_name, u.phone, u.status, u.is_moderator, u.school_id, u.created_at,
           s.name as school_name, s.region
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    WHERE u.role = 'director'
    """
    params = []
    if school_id:
        query += " AND u.school_id = ?"
        params.append(school_id)
    query += " ORDER BY u.created_at DESC"
    cursor.execute(query, params)
    res = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return res

@app.post("/api/admin/directors/{director_id}/reset-password")
def admin_reset_director_password(director_id: int, req: AdminResetPasswordRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ? AND role = 'director'", (hash_pass(req.new_password.strip()), director_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Direktorun şifrəsi yeniləndi!"}

@app.delete("/api/admin/directors/{director_id}")
def admin_delete_director(director_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ? AND role = 'director'", (director_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Direktor hesabı uğurla silindi! 🗑️"}

@app.get("/api/admin/teachers")
def admin_list_teachers(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT u.id, u.username, u.full_name, u.subject, u.class_head_id, u.status, u.is_moderator, u.school_id,
           s.name as school_name, c.name as head_class_name,
           (SELECT GROUP_CONCAT(cl.name, ', ') FROM teacher_classes tc JOIN classes cl ON tc.class_id = cl.id WHERE tc.teacher_id = u.id) as teaching_classes
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c ON u.class_head_id = c.id
    WHERE u.role = 'teacher'
    """
    params = []
    if school_id:
        query += " AND u.school_id = ?"
        params.append(school_id)
    query += " ORDER BY u.full_name ASC"
    cursor.execute(query, params)
    res = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return res

@app.post("/api/admin/teachers/{teacher_id}/reset-password")
def admin_reset_teacher_password(teacher_id: int, req: AdminResetPasswordRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_pass(req.new_password.strip()), teacher_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Şifrə yeniləndi!"}

@app.delete("/api/admin/teachers/{teacher_id}")
def admin_delete_teacher(teacher_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ? AND role = 'teacher'", (teacher_id,))
    cursor.execute("DELETE FROM teacher_classes WHERE teacher_id = ?", (teacher_id,))
    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/api/admin/students")
def admin_list_students(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT u.id, u.username, u.full_name, u.class_id, u.status, u.school_id,
           s.name as school_name, c.name as class_name, u.created_at
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c ON u.class_id = c.id
    WHERE u.role = 'student'
    """
    params = []
    if school_id:
        query += " AND u.school_id = ?"
        params.append(school_id)
    query += " ORDER BY c.grade ASC, c.section ASC, u.full_name ASC"
    cursor.execute(query, params)
    res = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return res

@app.put("/api/admin/students/{student_id}/assign-class")
def admin_assign_student(student_id: int, req: AdminAssignStudentRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET class_id = ? WHERE id = ? AND role = 'student'", (req.class_id, student_id))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/admin/students/{student_id}/reset-password")
def admin_reset_student_password(student_id: int, req: AdminResetPasswordRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_pass(req.new_password.strip()), student_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Şagirdin şifrəsi yeniləndi!"}

@app.delete("/api/admin/students/{student_id}")
def admin_delete_student(student_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ? AND role = 'student'", (student_id,))
    cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/admin/classes/add-index")
def admin_add_index(req: AdminAddIndexRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sec = req.section.strip().upper()
    name = f"{req.grade}{sec}"
    school_id = req.school_id or 1
    try:
        cursor.execute("INSERT INTO classes (name, grade, section, school_id) VALUES (?, ?, ?, ?)", 
                       (name, req.grade, sec, school_id))
        conn.commit()
        class_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail=f"{name} sinfi artıq mövcuddur!")
    conn.close()
    return {"success": True, "class_id": class_id, "name": name}

@app.post("/api/admin/classes")
def admin_create_class(req: AdminCreateClassRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    school_id = req.school_id or 1
    try:
        cursor.execute("INSERT INTO classes (name, grade, section, school_id) VALUES (?, ?, ?, ?)", 
                       (req.name.strip().upper(), req.grade, req.section.strip().upper(), school_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu adda sinif artıq var!")
    conn.close()
    return {"success": True}

@app.delete("/api/admin/classes/{class_id}")
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
    }

# ----------------- TEACHER & STUDENT DASHBOARDS -----------------

@app.get("/api/teachers/{teacher_id}/dashboard")
def get_teacher_dashboard(teacher_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.id, u.full_name, u.subject, u.class_head_id, u.school_id, c.name as head_class_name,
           s.name as school_name,
           (SELECT COUNT(*) FROM users st WHERE st.class_id = u.class_head_id AND st.role = 'student' AND st.status = 'approved') as head_class_student_count
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c ON u.class_head_id = c.id
    WHERE u.id = ?
    """, (teacher_id,))
    t_info = cursor.fetchone()
    if not t_info:
        conn.close()
        raise HTTPException(status_code=404, detail="Müəllim tapılmadı")

    cursor.execute("""
    SELECT tc.id as assignment_id, c.id as class_id, c.name as class_name, tc.subject,
           (SELECT COUNT(*) FROM users st WHERE st.class_id = c.id AND st.role = 'student' AND st.status = 'approved') as student_count
    FROM teacher_classes tc
    JOIN classes c ON tc.class_id = c.id
    WHERE tc.teacher_id = ?
    ORDER BY c.grade ASC, c.section ASC
    """, (teacher_id,))
    teaching_classes = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "teacher": {
            "id": t_info["id"],
            "full_name": t_info["full_name"],
            "subject": t_info["subject"],
            "school_id": t_info["school_id"],
            "school_name": t_info["school_name"],
            "class_head_id": t_info["class_head_id"],
            "head_class_name": t_info["head_class_name"],
            "head_class_student_count": t_info["head_class_student_count"] or 0
        },
        "teaching_classes": teaching_classes
    }

@app.post("/api/teachers/update-assignments")
def update_teacher_assignments(req: UpdateTeacherClassesRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET class_head_id = ?, subject = ? WHERE id = ?", 
                   (req.class_head_id, req.subject.strip(), req.teacher_id))

    cursor.execute("DELETE FROM teacher_classes WHERE teacher_id = ?", (req.teacher_id,))
    for cid in req.teaching_class_ids:
        cursor.execute("INSERT OR IGNORE INTO teacher_classes (teacher_id, class_id, subject) VALUES (?, ?, ?)",
                       (req.teacher_id, cid, req.subject.strip()))

    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/api/classes/{class_id}/students")
def get_class_students(class_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, full_name, username FROM users
    WHERE class_id = ? AND role = 'student' AND status = 'approved'
    ORDER BY full_name ASC
    """, (class_id,))
    students = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return students

@app.get("/api/students/unassigned")
def get_unassigned_students(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT id, full_name, username, class_id, school_id FROM users
    WHERE role = 'student' AND status = 'approved'
    """
    params = []
    if school_id:
        query += " AND school_id = ?"
        params.append(school_id)
    query += " ORDER BY full_name ASC"
    cursor.execute(query, params)
    students = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return students

@app.post("/api/classes/add-student")
def add_student_to_class(req: AddStudentToClassRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if req.student_user_id:
        cursor.execute("UPDATE users SET class_id = ? WHERE id = ? AND role = 'student'", 
                       (req.class_id, req.student_user_id))
    elif req.full_name and req.full_name.strip():
        clean_name = req.full_name.strip()
        base_user = "shagird_" + str(int(datetime.now().timestamp()))[-4:]
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, class_id, status)
        VALUES (?, ?, ?, 'student', ?, 'approved')
        """, (base_user, hash_pass("1234"), clean_name, req.class_id))
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Şagird seçilməyib!")

    conn.commit()
    conn.close()
    return {"success": True}

@app.post("/api/classes/remove-student/{student_id}")
def remove_student_from_class(student_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET class_id = NULL WHERE id = ? AND role = 'student'", (student_id,))
    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/api/student/{student_id}/dashboard")
def get_student_dashboard(student_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.id, u.full_name, u.username, u.class_id, u.school_id, c.name as class_name,
           s.name as school_name, t_head.full_name as head_teacher_name
    FROM users u
    LEFT JOIN schools s ON u.school_id = s.id
    LEFT JOIN classes c ON u.class_id = c.id
    LEFT JOIN users t_head ON t_head.class_head_id = c.id
    WHERE u.id = ? AND u.role = 'student' AND u.status = 'approved'
    """, (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Şagird tapılmadı")

    class_id = student["class_id"]
    if not class_id:
        conn.close()
        return {
            "student": dict(student),
            "enrolled": False
        }

    cursor.execute("""
    SELECT DISTINCT u.full_name as teacher_name, tc.subject
    FROM teacher_classes tc
    JOIN users u ON tc.teacher_id = u.id
    WHERE tc.class_id = ?
    ORDER BY tc.subject ASC
    """, (class_id,))
    teachers = [dict(t) for t in cursor.fetchall()]

    cursor.execute("""
    SELECT l.id, l.subject, l.date, l.topic, l.homework, u.full_name as teacher_name
    FROM lessons l
    LEFT JOIN users u ON l.teacher_id = u.id
    WHERE l.class_id = ?
    ORDER BY l.date DESC, l.id DESC
    LIMIT 40
    """, (class_id,))
    lessons = [dict(l) for l in cursor.fetchall()]

    cursor.execute("""
    SELECT g.id, g.subject, g.date, g.grade_type, g.score, g.comment, u.full_name as teacher_name
    FROM grades g
    LEFT JOIN users u ON g.teacher_id = u.id
    WHERE g.class_id = ? AND g.student_id = ?
    ORDER BY g.date DESC, g.id DESC
    """, (class_id, student_id))
    my_grades = [dict(g) for g in cursor.fetchall()]

    cursor.execute("""
    SELECT a.date, a.subject, a.status, u.full_name as teacher_name
    FROM attendance a
    LEFT JOIN users u ON a.teacher_id = u.id
    WHERE a.student_id = ?
    ORDER BY a.date DESC
    LIMIT 30
    """, (student_id,))
    my_attendance = [dict(a) for a in cursor.fetchall()]

    cursor.execute("""
    SELECT h.id, h.subject, h.title, h.description, h.due_date, u.full_name as teacher_name,
           (SELECT status FROM student_homework_status shs WHERE shs.homework_id = h.id AND shs.student_id = ?) as status
    FROM homework h
    LEFT JOIN users u ON h.teacher_id = u.id
    WHERE h.class_id = ?
    ORDER BY h.due_date DESC, h.id DESC
    LIMIT 30
    """, (student_id, class_id))
    my_homework = [dict(h) for h in cursor.fetchall()]
    for hw in my_homework:
        hw["is_completed"] = (hw.get("status") == "completed")

    cursor.execute("""
    SELECT day_of_week, lesson_order, subject, teacher_name, room
    FROM timetable
    WHERE class_id = ?
    ORDER BY day_of_week ASC, lesson_order ASC
    """, (class_id,))
    my_timetable = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "student": dict(student),
        "enrolled": True,
        "school_name": student["school_name"],
        "class_name": student["class_name"],
        "head_teacher_name": student["head_teacher_name"],
        "teachers": teachers,
        "lessons": lessons,
        "grades": my_grades,
        "attendance": my_attendance,
        "homework": my_homework,
        "timetable": my_timetable,
        "bells": BELL_SCHEDULE
    }

# ----------------- JOURNAL ACTIONS -----------------

@app.get("/api/classes/{class_id}/attendance")
def get_attendance(class_id: int, subject: str, date: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT student_id, status FROM attendance
    WHERE class_id = ? AND subject = ? AND date = ?
    """, (class_id, subject, date))
    records = {row["student_id"]: row["status"] for row in cursor.fetchall()}
    conn.close()
    return records

@app.post("/api/classes/attendance")
def save_attendance(req: SaveAttendanceRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for r in req.records:
        cursor.execute("""
        INSERT INTO attendance (class_id, teacher_id, subject, student_id, date, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(class_id, subject, student_id, date) DO UPDATE SET
            status = excluded.status,
            teacher_id = excluded.teacher_id
        """, (req.class_id, user_id, req.subject, r.student_id, req.date, r.status))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Davamiyyət qeyd olundu"}

@app.get("/api/classes/{class_id}/grades")
def get_grades(class_id: int, subject: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT g.id, g.student_id, u.full_name as student_name, g.date, g.grade_type, g.score, g.comment
    FROM grades g
    JOIN users u ON g.student_id = u.id
    WHERE g.class_id = ? AND g.subject = ?
    ORDER BY g.date DESC, g.id DESC
    """, (class_id, subject))
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return records

@app.post("/api/classes/grades")
def save_grades(req: SaveGradeRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for g in req.grades:
        if not g.score.strip():
            continue
        cursor.execute("""
        INSERT INTO grades (class_id, teacher_id, subject, student_id, date, grade_type, score, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (req.class_id, user_id, req.subject, g.student_id, req.date, g.grade_type, g.score.strip(), g.comment or ""))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Qiymət yazıldı"}

@app.delete("/api/grades/{grade_id}")
def delete_grade(grade_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/api/classes/{class_id}/lessons")
def get_lessons(class_id: int, subject: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT l.*, u.full_name as teacher_name
    FROM lessons l
    LEFT JOIN users u ON l.teacher_id = u.id
    WHERE l.class_id = ? AND l.subject = ?
    ORDER BY l.date DESC, l.id DESC
    LIMIT 30
    """, (class_id, subject))
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return records

@app.post("/api/classes/lessons")
def save_lesson(req: LessonTopicRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO lessons (class_id, teacher_id, subject, date, topic, homework)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (req.class_id, user_id, req.subject, req.date, req.topic.strip(), (req.homework or "").strip()))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Mövzu və ev tapşırığı qeyd olundu"}

@app.get("/api/classes")
def list_classes(school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT c.id, c.name, c.grade, c.section, c.school_id,
           (SELECT COUNT(*) FROM users s WHERE s.class_id = c.id AND s.role = 'student' AND s.status = 'approved') as student_count,
           u.full_name as head_teacher_name
    FROM classes c
    LEFT JOIN users u ON u.class_head_id = c.id
    WHERE 1=1
    """
    params = []
    if school_id:
        query += " AND c.school_id = ?"
        params.append(school_id)
    query += " ORDER BY c.grade ASC, c.section ASC"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# ----------------- KSQ & BSQ SUMMATİV JURNAL SİSTEMİ -----------------

def calc_grade_val(score_val):
    if score_val is None:
        return None
    try:
        s = float(score_val)
        if s >= 80.5:
            return 5
        elif s >= 60.5:
            return 4
        elif s >= 30.5:
            return 3
        else:
            return 2
    except (ValueError, TypeError):
        return None

@app.get("/api/classes/{class_id}/summative-matrix")
def get_summative_matrix(class_id: int, subject: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, full_name, username FROM users
    WHERE class_id = ? AND role = 'student' AND status = 'approved'
    ORDER BY full_name ASC
    """, (class_id,))
    students = [dict(s) for s in cursor.fetchall()]

    cursor.execute("""
    SELECT student_id, grade_type, score, date, comment
    FROM grades
    WHERE class_id = ? AND subject = ? AND grade_type IN (
        'ksq1', 'ksq2', 'ksq3', 'ksq4', 'ksq5', 'ksq6', 'bsq1', 'bsq2'
    )
    """, (class_id, subject))
    raw_grades = cursor.fetchall()
    conn.close()

    # Index grades by (student_id, grade_type)
    grades_map = {}
    for r in raw_grades:
        grades_map[(r["student_id"], r["grade_type"])] = {
            "score": r["score"],
            "date": r["date"],
            "comment": r["comment"]
        }

    matrix_students = []
    sem1_grades_list = []
    sem2_grades_list = []
    all_scores_list = []

    for s in students:
        sid = s["id"]
        row = {
            "student_id": sid,
            "full_name": s["full_name"],
            "username": s["username"],
            "ksq1": None, "ksq2": None, "ksq3": None,
            "ksq4": None, "ksq5": None, "ksq6": None,
            "bsq1": None, "bsq2": None,
            "sem1_score": None, "sem1_grade": None,
            "sem2_score": None, "sem2_grade": None,
            "annual_score": None, "annual_grade": None
        }

        for gt in ["ksq1", "ksq2", "ksq3", "ksq4", "ksq5", "ksq6", "bsq1", "bsq2"]:
            if (sid, gt) in grades_map:
                try:
                    val = float(grades_map[(sid, gt)]["score"])
                    row[gt] = val
                    all_scores_list.append(val)
                except (ValueError, TypeError):
                    row[gt] = None

        # Calculate Sem 1
        sem1_ksqs = [row[k] for k in ["ksq1", "ksq2", "ksq3"] if row[k] is not None]
        bsq1 = row["bsq1"]
        if sem1_ksqs:
            ksq1_avg = sum(sem1_ksqs) / len(sem1_ksqs)
            if bsq1 is not None:
                row["sem1_score"] = round(ksq1_avg * 0.40 + bsq1 * 0.60, 1)
            else:
                row["sem1_score"] = round(ksq1_avg, 1)
            row["sem1_grade"] = calc_grade_val(row["sem1_score"])
            sem1_grades_list.append(row["sem1_grade"])
        elif bsq1 is not None:
            row["sem1_score"] = round(bsq1, 1)
            row["sem1_grade"] = calc_grade_val(row["sem1_score"])
            sem1_grades_list.append(row["sem1_grade"])

        # Calculate Sem 2
        sem2_ksqs = [row[k] for k in ["ksq4", "ksq5", "ksq6"] if row[k] is not None]
        bsq2 = row["bsq2"]
        if sem2_ksqs:
            ksq2_avg = sum(sem2_ksqs) / len(sem2_ksqs)
            if bsq2 is not None:
                row["sem2_score"] = round(ksq2_avg * 0.40 + bsq2 * 0.60, 1)
            else:
                row["sem2_score"] = round(ksq2_avg, 1)
            row["sem2_grade"] = calc_grade_val(row["sem2_score"])
            sem2_grades_list.append(row["sem2_grade"])
        elif bsq2 is not None:
            row["sem2_score"] = round(bsq2, 1)
            row["sem2_grade"] = calc_grade_val(row["sem2_score"])
            sem2_grades_list.append(row["sem2_grade"])

        # Annual (İllik)
        if row["sem1_score"] is not None and row["sem2_score"] is not None:
            row["annual_score"] = round((row["sem1_score"] + row["sem2_score"]) / 2, 1)
            row["annual_grade"] = calc_grade_val(row["annual_score"])
        elif row["sem1_score"] is not None:
            row["annual_score"] = row["sem1_score"]
            row["annual_grade"] = row["sem1_grade"]
        elif row["sem2_score"] is not None:
            row["annual_score"] = row["sem2_score"]
            row["annual_grade"] = row["sem2_grade"]

        matrix_students.append(row)

    # Class-level analytics
    total_st = len(students)
    rated_students = [r for r in matrix_students if r["annual_grade"] is not None or r["sem1_grade"] is not None]
    graded_count = len(rated_students)
    quality_count = sum(1 for r in rated_students if (r["annual_grade"] or r["sem1_grade"]) in [4, 5])
    success_count = sum(1 for r in rated_students if (r["annual_grade"] or r["sem1_grade"]) in [3, 4, 5])

    quality_pct = round((quality_count / graded_count * 100), 1) if graded_count > 0 else 0.0
    success_pct = round((success_count / graded_count * 100), 1) if graded_count > 0 else 0.0
    avg_score = round(sum(all_scores_list) / len(all_scores_list), 1) if all_scores_list else 0.0

    return {
        "students": matrix_students,
        "stats": {
            "total_students": total_st,
            "graded_count": graded_count,
            "quality_pct": quality_pct,
            "success_pct": success_pct,
            "average_score": avg_score
        }
    }

@app.post("/api/classes/summative-grade")
def save_summative_grade(req: SaveSummativeGradeRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    grade_date = req.date or date.today().isoformat()
    clean_score = req.score.strip() if req.score else ""

    if not clean_score:
        # Delete if emptied
        cursor.execute("""
        DELETE FROM grades 
        WHERE class_id = ? AND subject = ? AND student_id = ? AND grade_type = ?
        """, (req.class_id, req.subject, req.student_id, req.grade_type))
    else:
        # Check if exists
        cursor.execute("""
        SELECT id FROM grades 
        WHERE class_id = ? AND subject = ? AND student_id = ? AND grade_type = ?
        """, (req.class_id, req.subject, req.student_id, req.grade_type))
        row = cursor.fetchone()
        if row:
            cursor.execute("""
            UPDATE grades 
            SET score = ?, date = ?, teacher_id = ?, comment = ?
            WHERE id = ?
            """, (clean_score, grade_date, user_id, req.comment or "", row[0]))
        else:
            cursor.execute("""
            INSERT INTO grades (class_id, teacher_id, subject, student_id, date, grade_type, score, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (req.class_id, user_id, req.subject, req.student_id, grade_date, req.grade_type, clean_score, req.comment or ""))

    conn.commit()
    conn.close()
    return {"success": True, "message": "Summativ bal yadda saxlanıldı"}

# ----------------- EV TAPŞIRIQLARI (HOMEWORK) SİSTEMİ -----------------

@app.get("/api/classes/{class_id}/homework")
def get_class_homework(class_id: int, student_id: Optional[int] = None, subject: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT h.id, h.class_id, h.teacher_id, h.subject, h.title, h.description, h.due_date, h.created_at,
           u.full_name as teacher_name,
           (SELECT COUNT(*) FROM student_homework_status shs WHERE shs.homework_id = h.id AND shs.status = 'completed') as completed_count
    FROM homework h
    LEFT JOIN users u ON h.teacher_id = u.id
    WHERE h.class_id = ?
    """
    params = [class_id]
    if subject:
        query += " AND h.subject = ?"
        params.append(subject)
    query += " ORDER BY h.due_date DESC, h.id DESC"

    cursor.execute(query, params)
    homeworks = [dict(h) for h in cursor.fetchall()]

    if student_id:
        cursor.execute("""
        SELECT homework_id, status FROM student_homework_status
        WHERE student_id = ?
        """, (student_id,))
        statuses = {r["homework_id"]: r["status"] for r in cursor.fetchall()}
        for hw in homeworks:
            hw["is_completed"] = (statuses.get(hw["id"]) == "completed")
    else:
        for hw in homeworks:
            hw["is_completed"] = False

    conn.close()
    return homeworks

@app.post("/api/homework")
def create_homework(req: CreateHomeworkRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO homework (class_id, teacher_id, subject, title, description, due_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (req.class_id, user_id, req.subject, req.title.strip(), req.description.strip(), req.due_date))
    hw_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"success": True, "homework_id": hw_id, "message": "Ev tapşırığı uğurla əlavə edildi"}

@app.delete("/api/homework/{homework_id}")
def delete_homework(homework_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_homework_status WHERE homework_id = ?", (homework_id,))
    cursor.execute("DELETE FROM homework WHERE id = ?", (homework_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Ev tapşırığı silindi"}

@app.post("/api/homework/{homework_id}/toggle-status")
def toggle_homework_status(homework_id: int, req: ToggleHomeworkRequest, user_id: int = Header(..., alias="X-User-Id")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    st_id = req.student_id or user_id

    cursor.execute("""
    SELECT id, status FROM student_homework_status
    WHERE homework_id = ? AND student_id = ?
    """, (homework_id, st_id))
    row = cursor.fetchone()

    if row:
        new_status = "pending" if row[1] == "completed" else "completed"
        cursor.execute("""
        UPDATE student_homework_status 
        SET status = ?, completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (new_status, row[0]))
    else:
        new_status = "completed"
        cursor.execute("""
        INSERT INTO student_homework_status (homework_id, student_id, status, completed_at)
        VALUES (?, ?, 'completed', CURRENT_TIMESTAMP)
        """, (homework_id, st_id))

    conn.commit()
    conn.close()
    return {"success": True, "status": new_status}

# ----------------- HƏFTƏLİK DƏRS CƏDVƏLİ VƏ ZƏNGLƏR -----------------

BELL_SCHEDULE = [
    {"order": 1, "start": "08:30", "end": "09:15", "break": "10 dəqiqə"},
    {"order": 2, "start": "09:25", "end": "10:10", "break": "10 dəqiqə"},
    {"order": 3, "start": "10:20", "end": "11:05", "break": "20 dəqiqə (Böyük tənəffüs)"},
    {"order": 4, "start": "11:25", "end": "12:10", "break": "10 dəqiqə"},
    {"order": 5, "start": "12:20", "end": "13:05", "break": "10 dəqiqə"},
    {"order": 6, "start": "13:15", "end": "14:00", "break": "5 dəqiqə"},
    {"order": 7, "start": "14:05", "end": "14:50", "break": "Dərslər bitir"}
]

@app.get("/api/classes/{class_id}/timetable")
def get_class_timetable(class_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, day_of_week, lesson_order, subject, teacher_name, room
    FROM timetable
    WHERE class_id = ?
    ORDER BY day_of_week ASC, lesson_order ASC
    """, (class_id,))
    slots = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {
        "class_id": class_id,
        "bells": BELL_SCHEDULE,
        "slots": slots
    }

@app.post("/api/classes/{class_id}/timetable")
def save_class_timetable(class_id: int, req: SaveTimetableRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timetable WHERE class_id = ?", (class_id,))
    for s in req.slots:
        if s.subject.strip():
            cursor.execute("""
            INSERT INTO timetable (class_id, day_of_week, lesson_order, subject, teacher_name, room)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (class_id, s.day_of_week, s.lesson_order, s.subject.strip(), (s.teacher_name or "").strip(), (s.room or "").strip()))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Dərs cədvəli yadda saxlanıldı"}



# ----------------- VALİDEYN PORTALI VƏ ŞAGİRD SORGUSU -----------------

@app.get("/api/parent/student-lookup")
def parent_student_lookup(query: Optional[str] = None, student_id: Optional[int] = None, school_id: Optional[int] = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if student_id:
        sql = """
        SELECT u.id, u.full_name, u.username, u.phone, u.class_id, u.school_id, c.name as class_name,
               s.name as school_name, t_head.full_name as head_teacher_name
        FROM users u
        LEFT JOIN schools s ON u.school_id = s.id
        LEFT JOIN classes c ON u.class_id = c.id
        LEFT JOIN users t_head ON t_head.class_head_id = c.id
        WHERE u.id = ? AND u.role = 'student' AND u.status = 'approved'
        """
        params = [student_id]
    elif query and query.strip():
        q_clean = query.strip()
        clean_num = q_clean.replace(" ", "").replace("-", "").replace("+", "")
        sql = """
        SELECT u.id, u.full_name, u.username, u.phone, u.class_id, u.school_id, c.name as class_name,
               s.name as school_name, t_head.full_name as head_teacher_name
        FROM users u
        LEFT JOIN schools s ON u.school_id = s.id
        LEFT JOIN classes c ON u.class_id = c.id
        LEFT JOIN users t_head ON t_head.class_head_id = c.id
        WHERE u.role = 'student' AND u.status = 'approved'
          AND (
              u.username = ? 
              OR LOWER(u.full_name) LIKE LOWER(?)
              OR u.phone = ?
              OR REPLACE(REPLACE(REPLACE(u.phone, ' ', ''), '-', ''), '+', '') = ?
          )
        """
        params = [q_clean, f"%{q_clean}%", q_clean, clean_num]
        if school_id:
            sql += " AND u.school_id = ?"
            params.append(school_id)
        sql += " LIMIT 5"
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Axtarış sorğusu və ya şagird seçilməyib!")
    
    cursor.execute(sql, params)
    students = [dict(s) for s in cursor.fetchall()]

    if not students:
        conn.close()
        raise HTTPException(status_code=404, detail="Qeyd edilən məlumatla şagird tapılmadı")

    st = students[0]
    sid = st["id"]
    cid = st["class_id"]

    # Attendance stats
    cursor.execute("""
    SELECT status, COUNT(*) as count FROM attendance
    WHERE student_id = ?
    GROUP BY status
    """, (sid,))
    att_counts = {r["status"]: r["count"] for r in cursor.fetchall()}
    total_days = sum(att_counts.values())
    present_cnt = att_counts.get("present", 0)
    absent_cnt = att_counts.get("absent", 0)
    excused_cnt = att_counts.get("excused", 0)
    att_pct = round((present_cnt / total_days * 100), 1) if total_days > 0 else 100.0

    # Recent Summative / KSQ grades
    cursor.execute("""
    SELECT g.subject, g.grade_type, g.score, g.date, u.full_name as teacher_name
    FROM grades g
    LEFT JOIN users u ON g.teacher_id = u.id
    WHERE g.student_id = ?
    ORDER BY g.date DESC, g.id DESC
    LIMIT 20
    """, (sid,))
    recent_grades = [dict(g) for g in cursor.fetchall()]

    # Homeworks
    homeworks = []
    if cid:
        cursor.execute("""
        SELECT h.id, h.subject, h.title, h.description, h.due_date,
               (SELECT status FROM student_homework_status shs WHERE shs.homework_id = h.id AND shs.student_id = ?) as status
        FROM homework h
        WHERE h.class_id = ? AND h.due_date >= date('now', '-7 days')
        ORDER BY h.due_date ASC
        LIMIT 10
        """, (sid, cid))
        homeworks = [dict(h) for h in cursor.fetchall()]

    conn.close()
    return {
        "student": st,
        "attendance": {
            "total_recorded": total_days,
            "present": present_cnt,
            "absent": absent_cnt,
            "excused": excused_cnt,
            "percentage": att_pct
        },
        "recent_grades": recent_grades,
        "homeworks": homeworks
    }

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    import sys
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
