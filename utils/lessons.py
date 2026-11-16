"""
รายการบทเรียนทั้งหมด (ใช้ร่วมกันระหว่าง navigation, หน้าแรก และ sidebar)
total = จำนวนแบบฝึกหัดในบทนั้น (0 = บทอ่านอย่างเดียว ไม่มีแบบฝึกหัด)
ถ้าเพิ่ม/ลบแบบฝึกหัดในบทไหน ให้แก้ตัวเลข total ที่นี่ด้วย
"""

LESSONS = [
    {"id": "lesson00", "no": 0, "title": "ความเป็นมาของไพธอน", "nav": "บทที่ 0: ความเป็นมาของไพธอน",
     "desc": "รู้จักไพธอนและเหตุผลที่ควรเรียน", "page": "pages/0_บทที่0_ความเป็นมา.py", "total": 0},
    {"id": "lesson01", "no": 1, "title": "การติดตั้งและใช้งาน", "nav": "บทที่ 1: การติดตั้งและใช้งาน",
     "desc": "Anaconda, Jupyter, Cloud, การติดตั้ง package", "page": "pages/1_บทที่1_การติดตั้ง.py", "total": 0},
    {"id": "lesson02", "no": 2, "title": "ตัวแปรและ Data Type", "nav": "บทที่ 2: ตัวแปรและ Data Type",
     "desc": "int, float, str, bool", "page": "pages/2_บทที่2_ตัวแปร.py", "total": 11},
    {"id": "lesson03", "no": 3, "title": "Data Structure", "nav": "บทที่ 3: Data Structure",
     "desc": "list, tuple, dict, set, 2D list", "page": "pages/3_บทที่3_data_structure.py", "total": 13},
    {"id": "lesson04", "no": 4, "title": "Conditions", "nav": "บทที่ 4: Conditions",
     "desc": "if, elif, else, in: ฝึกตรรกะ", "page": "pages/4_บทที่4_conditions.py", "total": 11},
    {"id": "lesson05", "no": 5, "title": "Loops", "nav": "บทที่ 5: Loops",
     "desc": "for, while: ฝึกตรรกะ", "page": "pages/5_บทที่5_loops.py", "total": 14},
    {"id": "lesson06", "no": 6, "title": "Functions", "nav": "บทที่ 6: Functions",
     "desc": "def, parameter, return, scope", "page": "pages/6_บทที่6_functions.py", "total": 13},
    {"id": "lesson07", "no": 7, "title": "Error Handling", "nav": "บทที่ 7: Error Handling",
     "desc": "try, except: จัดการข้อผิดพลาด", "page": "pages/7_บทที่7_error_handling.py", "total": 11},
    {"id": "lesson08", "no": 8, "title": "ฟังก์ชันสำเร็จรูปและ Library", "nav": "บทที่ 8: ฟังก์ชันสำเร็จรูปและ Library",
     "desc": "built-in functions, import", "page": "pages/8_บทที่8_built_in_functions.py", "total": 11},
    {"id": "lesson09", "no": 9, "title": "NumPy และ Linear Algebra เบื้องต้น", "nav": "บทที่ 9: NumPy และ Linear Algebra",
     "desc": "matrix, vector, การคำนวณเชิงเส้น", "page": "pages/9_บทที่9_numpy.py", "total": 11},
    {"id": "lesson10", "no": 10, "title": "อ่านและสำรวจข้อมูล", "nav": "บทที่ 10: อ่านและสำรวจข้อมูล",
     "desc": "pandas: อ่านไฟล์, head, info, filter", "page": "pages/10_บทที่10_อ่านข้อมูล.py", "total": 11},
    {"id": "lesson11", "no": 11, "title": "จัดการและแสดงผลข้อมูล", "nav": "บทที่ 11: จัดการและแสดงผลข้อมูล",
     "desc": "clean, groupby, visualization เบื้องต้น", "page": "pages/11_บทที่11_จัดการข้อมูล.py", "total": 11},
]

LESSONS_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}
TOTAL_EXERCISES = sum(lesson["total"] for lesson in LESSONS)


def passed_in_lesson(progress: dict, lesson_id: str) -> int:
    return sum(1 for e in progress.values() if e.get("passed") and e.get("lesson_id") == lesson_id)


def passed_total(progress: dict) -> int:
    return sum(1 for e in progress.values() if e.get("passed"))


def continue_lesson(progress: dict):
    """
    บทที่ควรทำต่อ: บทล่าสุดที่เคยทำ (ถ้ายังไม่ครบ) ไม่งั้นบทแรกที่ยังไม่ครบ
    คืน None ถ้ายังไม่เคยทำอะไรเลย
    """
    if not progress:
        return None
    latest = max(progress.values(), key=lambda e: e.get("ts") or "")
    lesson = LESSONS_BY_ID.get(latest.get("lesson_id"))
    if lesson and passed_in_lesson(progress, lesson["id"]) < lesson["total"]:
        return lesson
    for lesson in LESSONS:
        if lesson["total"] and passed_in_lesson(progress, lesson["id"]) < lesson["total"]:
            return lesson
    return None
