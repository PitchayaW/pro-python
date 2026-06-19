"""
Progress tracker — บันทึกคะแนน/ความก้าวหน้าของนักศึกษาลง Google Sheet
ใช้ gspread + Service Account credentials (เก็บใน st.secrets)
"""

import datetime
import streamlit as st


@st.cache_resource(show_spinner=False)
def _get_gsheet_client():
    """เชื่อมต่อ Google Sheets ผ่าน Service Account (cache ไว้ไม่ต้องเชื่อมใหม่ทุกครั้ง)"""
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    """เปิด worksheet ที่ใช้เก็บ progress (สร้าง header แถวแรกถ้ายังไม่มี)"""
    client = _get_gsheet_client()
    sheet_url = st.secrets["gcp_service_account"]["sheet_url"]
    sh = client.open_by_url(sheet_url)

    try:
        ws = sh.worksheet("progress")
    except Exception:
        ws = sh.add_worksheet(title="progress", rows=1000, cols=10)
        ws.append_row(["timestamp", "student_id", "student_name", "lesson_id",
                        "exercise_id", "status", "attempts", "code"])

    return ws


def record_attempt(student_id: str, student_name: str, lesson_id: str,
                    exercise_id: str, passed: bool, code: str = ""):
    """
    บันทึกการพยายามทำ exercise 1 ครั้งลง Google Sheet
    เก็บทุก attempt (ไม่ overwrite) เพื่อดูพัฒนาการได้ ส่วนหน้าสรุปจะกรองเอาแถวล่าสุดของแต่ละคน/exercise
    เก็บโค้ดที่ส่งตรวจไว้ด้วย เพื่อใช้แสดงกลับให้นักศึกษาเห็นโค้ดเดิมตอนกลับมาทำต่อ
    """
    try:
        ws = _get_worksheet()
        ws.append_row([
            datetime.datetime.now().isoformat(),
            student_id,
            student_name,
            lesson_id,
            exercise_id,
            "passed" if passed else "failed",
            1,
            code,
        ])
    except Exception as e:
        # ไม่ให้แอป crash ถ้า Google Sheet มีปัญหา (เช่น เน็ตหลุด) แค่แจ้งเตือนเบา ๆ
        st.warning(f"บันทึกคะแนนไม่สำเร็จ (ทำแบบฝึกหัดต่อได้ตามปกติ): {e}")


@st.cache_data(ttl=30, show_spinner=False)
def get_student_progress(student_id: str) -> dict:
    """
    ดึงความก้าวหน้าของนักศึกษาคนหนึ่ง คืนค่าเป็น
    {exercise_id: {"status": "passed"/"failed", "code": "...", "lesson_id": "..."}}
    โดยใช้ attempt ล่าสุดของแต่ละ exercise (แถวท้ายสุดที่เจอในชีตของ exercise นั้น)
    """
    try:
        ws = _get_worksheet()
        records = ws.get_all_records()
    except Exception:
        return {}

    progress = {}
    for row in records:
        if str(row.get("student_id")) == str(student_id):
            ex_id = row.get("exercise_id")
            progress[ex_id] = {
                "status": row.get("status"),
                "code": row.get("code", ""),
                "lesson_id": row.get("lesson_id", ""),
            }
    return progress


@st.cache_data(ttl=30, show_spinner=False)
def get_class_summary() -> list:
    """
    ดึงสรุปความก้าวหน้าของทั้งคลาส สำหรับอาจารย์ดูภาพรวม
    คืนค่าเป็น list of dict: [{"student_id", "student_name", "passed_count", "total_attempts"}]
    """
    try:
        ws = _get_worksheet()
        records = ws.get_all_records()
    except Exception:
        return []

    summary = {}
    for row in records:
        sid = str(row.get("student_id"))
        if sid not in summary:
            summary[sid] = {
                "student_id": sid,
                "student_name": row.get("student_name", ""),
                "passed_exercises": set(),
                "total_attempts": 0,
            }
        summary[sid]["total_attempts"] += 1
        if row.get("status") == "passed":
            summary[sid]["passed_exercises"].add(row.get("exercise_id"))

    result = []
    for sid, data in summary.items():
        result.append({
            "student_id": data["student_id"],
            "student_name": data["student_name"],
            "passed_count": len(data["passed_exercises"]),
            "total_attempts": data["total_attempts"],
        })
    return sorted(result, key=lambda x: x["passed_count"], reverse=True)
