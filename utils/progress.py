"""
Progress tracker: บันทึกคะแนน/ความก้าวหน้าของนักศึกษาลง Google Sheet
ใช้ gspread + Service Account credentials (เก็บใน st.secrets)

หลักการออกแบบ (แก้ปัญหานักศึกษากลับมาแล้วความคืบหน้าหาย):

1. อ่านชีตครั้งเดียวต่อเซสชัน แล้วเก็บ progress ไว้ใน st.session_state["progress"]
   หลังจากนั้นทุกการตรวจคำตอบจะอัปเดต progress ในเซสชันทันที ไม่ต้องอ่านชีตซ้ำ
2. การอ่านทั้งชีตใช้ cache กลาง (แชร์ทุกคน) อายุ 60 วินาที นักศึกษาทั้งห้องล็อกอินพร้อมกัน
   ก็ยังอ่านชีตแค่ครั้งเดียว ไม่ชนโควตา Google Sheets API (ราว 60 requests/นาที ต่อ service account)
3. ถ้าอ่าน/เขียนล้มเหลว จะไม่ cache ค่าว่างไว้ (แบบเดิมจะทำให้ดูเหมือนความคืบหน้าหาย)
   แต่จะแจ้งเตือนชัดเจนและลองใหม่อัตโนมัติ
4. การเขียนใช้คิว (pending rows): ถ้าเขียนไม่สำเร็จ แถวจะถูกเก็บไว้และส่งซ้ำรอบถัดไป ไม่หาย
5. สถานะ "ผ่านแล้ว" เป็นแบบถาวร: เคยผ่านครั้งเดียวก็นับว่าผ่าน แม้ส่งครั้งหลังจะผิด
   ส่วนโค้ดที่แสดงกลับใน editor ใช้โค้ดล่าสุดที่บันทึกไว้
"""

import datetime
import time

import streamlit as st

HEADER = ["timestamp", "student_id", "student_email", "student_name", "lesson_id",
          "exercise_id", "status", "attempts", "code"]

RETRY_COOLDOWN_SEC = 20     # เว้นระยะก่อนลองอ่าน/เขียนชีตใหม่หลังล้มเหลว (กันยิง API รัว ๆ)

_SS_PROGRESS = "progress"
_SS_LOADED_FOR = "_progress_loaded_for"
_SS_LOAD_ERROR = "_progress_load_error"
_SS_LOAD_FAILED_AT = "_progress_load_failed_at"
_SS_SESSION_ROWS = "_progress_session_rows"
_SS_PENDING = "_progress_pending_rows"
_SS_FLUSH_ERROR = "_progress_flush_error"
_SS_FLUSH_FAILED_AT = "_progress_flush_failed_at"


# --------------------------------------------------------------------------- #
# Google Sheets access
# --------------------------------------------------------------------------- #
def _is_retryable(exc: Exception) -> bool:
    """error ที่ควรลองใหม่: โดน rate limit (429) หรือ server/เน็ตมีปัญหาชั่วคราว"""
    try:
        from gspread.exceptions import APIError
        if isinstance(exc, APIError):
            code = getattr(exc, "code", None)
            if code is None:
                code = getattr(getattr(exc, "response", None), "status_code", None)
            return code in (429, 500, 502, 503, 504)
    except ImportError:
        pass
    try:
        import requests
        if isinstance(exc, requests.exceptions.RequestException):
            return True
    except ImportError:
        pass
    return isinstance(exc, (ConnectionError, TimeoutError))


def _with_retry(fn, tries: int = 3, first_delay: float = 1.0):
    """เรียก fn() ซ้ำแบบ exponential backoff เมื่อเจอ error ชั่วคราว"""
    delay = first_delay
    for attempt in range(tries):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1 or not _is_retryable(exc):
                raise
            time.sleep(delay)
            delay *= 2


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
    sh = _with_retry(lambda: client.open_by_url(sheet_url))

    try:
        ws = _with_retry(lambda: sh.worksheet("progress"))
    except Exception as exc:  # noqa: BLE001
        if _is_retryable(exc):
            raise
        ws = sh.add_worksheet(title="progress", rows=1000, cols=len(HEADER))
        ws.append_row(HEADER, value_input_option="RAW")
    return ws


@st.cache_data(ttl=60, show_spinner=False)
def _fetch_all_rows() -> list:
    """
    อ่านทุกแถวในชีต (cache กลางแชร์ทุกเซสชัน 60 วินาที)
    ถ้าล้มเหลวจะ raise ออกไป ซึ่ง st.cache_data จะไม่ cache ผลลัพธ์นั้น
    """
    ws = _get_worksheet()
    return _with_retry(ws.get_all_values)


def _column_index(header_row: list) -> dict:
    """map ชื่อคอลัมน์ -> ตำแหน่ง (อิงชื่อใน header จริง ถ้าไม่เจอใช้ตำแหน่งมาตรฐาน)"""
    header = [str(h).strip() for h in header_row]
    return {name: (header.index(name) if name in header else i) for i, name in enumerate(HEADER)}


def _cell(row: list, idx: dict, name: str) -> str:
    i = idx[name]
    return str(row[i]) if i < len(row) else ""


# --------------------------------------------------------------------------- #
# Progress model
# --------------------------------------------------------------------------- #
def _apply_row(progress: dict, lesson_id: str, exercise_id: str, status: str, code: str, ts: str):
    """รวม 1 attempt เข้าไปใน progress dict (เรียงจากเก่าไปใหม่)"""
    if not exercise_id:
        return
    entry = progress.setdefault(exercise_id, {
        "lesson_id": lesson_id, "passed": False, "status": None,
        "last_status": None, "code": "", "ts": "",
    })
    if lesson_id:
        entry["lesson_id"] = lesson_id
    if status == "passed":
        entry["passed"] = True
    entry["last_status"] = status
    # "status" คงไว้เพื่อความเข้ากันได้กับโค้ดเดิม: passed ถ้าเคยผ่าน ไม่งั้นใช้สถานะล่าสุด
    entry["status"] = "passed" if entry["passed"] else status
    if code:
        entry["code"] = code
    if ts:
        entry["ts"] = ts


def _build_progress(rows: list, student_id: str) -> dict:
    progress = {}
    if not rows:
        return progress
    idx = _column_index(rows[0])
    sid = str(student_id).strip()
    for row in rows[1:]:
        if _cell(row, idx, "student_id").strip() != sid:
            continue
        _apply_row(progress,
                   _cell(row, idx, "lesson_id"),
                   _cell(row, idx, "exercise_id"),
                   _cell(row, idx, "status"),
                   _cell(row, idx, "code"),
                   _cell(row, idx, "timestamp"))
    return progress


def load_progress(force: bool = False) -> bool:
    """
    โหลด progress ของนักศึกษาที่ล็อกอินอยู่จากชีตเข้า session_state (ครั้งเดียวต่อเซสชัน)
    คืนค่า True ถ้าโหลดสำเร็จ (หรือโหลดไว้แล้ว)
    """
    ss = st.session_state
    student_id = ss.get("student_id")
    if not student_id:
        return False
    if ss.get(_SS_LOADED_FOR) == student_id and not force:
        return True

    failed_at = ss.get(_SS_LOAD_FAILED_AT)
    if not force and failed_at and time.time() - failed_at < RETRY_COOLDOWN_SEC:
        return False

    try:
        if force:
            _fetch_all_rows.clear()
        rows = _fetch_all_rows()
    except Exception as exc:  # noqa: BLE001
        ss[_SS_LOAD_ERROR] = str(exc) or exc.__class__.__name__
        ss[_SS_LOAD_FAILED_AT] = time.time()
        ss.setdefault(_SS_PROGRESS, {})
        return False

    progress = _build_progress(rows, student_id)
    # ทับด้วยสิ่งที่ทำในเซสชันนี้ (อาจยังไม่อยู่ในชีต เพราะ cache หรือยังรอส่ง)
    for r in ss.get(_SS_SESSION_ROWS, []):
        if r[1] == student_id:
            _apply_row(progress, r[4], r[5], r[6], r[8], r[0])

    ss[_SS_PROGRESS] = progress
    ss[_SS_LOADED_FOR] = student_id
    ss.pop(_SS_LOAD_ERROR, None)
    ss.pop(_SS_LOAD_FAILED_AT, None)
    return True


def get_progress() -> dict:
    """
    คืน progress ของนักศึกษาที่ล็อกอินอยู่:
    {exercise_id: {"lesson_id", "passed", "status", "last_status", "code", "ts"}}
    """
    load_progress()
    return st.session_state.get(_SS_PROGRESS, {})


def get_student_progress(student_id: str) -> dict:
    """ใช้แทนฟังก์ชันเดิม (คืน progress ของคนที่ล็อกอินอยู่)"""
    if str(student_id) != str(st.session_state.get("student_id")):
        return {}
    return get_progress()


def progress_status() -> dict:
    """สถานะการเชื่อมต่อชีต สำหรับแสดงใน sidebar"""
    ss = st.session_state
    return {
        "loaded": ss.get(_SS_LOADED_FOR) == ss.get("student_id") and bool(ss.get("student_id")),
        "load_error": ss.get(_SS_LOAD_ERROR),
        "pending": len(ss.get(_SS_PENDING, [])),
        "flush_error": ss.get(_SS_FLUSH_ERROR),
    }


def reset_progress_state():
    """ล้างข้อมูล progress ในเซสชัน (ใช้ตอนออกจากระบบ)"""
    for key in (_SS_PROGRESS, _SS_LOADED_FOR, _SS_LOAD_ERROR, _SS_LOAD_FAILED_AT,
                _SS_SESSION_ROWS, _SS_FLUSH_ERROR, _SS_FLUSH_FAILED_AT):
        st.session_state.pop(key, None)
    # ไม่ลบ _SS_PENDING: ถ้ามีแถวค้างส่ง ให้ส่งต่อให้เสร็จแม้ออกจากระบบแล้ว


# --------------------------------------------------------------------------- #
# Writing
# --------------------------------------------------------------------------- #
def flush_pending(force: bool = False) -> bool:
    """ส่งแถวที่ค้างอยู่ทั้งหมดลงชีตในครั้งเดียว (append_rows) คืน True ถ้าไม่มีอะไรค้าง"""
    ss = st.session_state
    pending = ss.get(_SS_PENDING, [])
    if not pending:
        return True

    failed_at = ss.get(_SS_FLUSH_FAILED_AT)
    if not force and failed_at and time.time() - failed_at < RETRY_COOLDOWN_SEC:
        return False

    try:
        ws = _get_worksheet()
        batch = list(pending)
        _with_retry(lambda: ws.append_rows(batch, value_input_option="RAW"))
    except Exception as exc:  # noqa: BLE001
        ss[_SS_FLUSH_ERROR] = str(exc) or exc.__class__.__name__
        ss[_SS_FLUSH_FAILED_AT] = time.time()
        return False

    ss[_SS_PENDING] = pending[len(batch):]
    ss.pop(_SS_FLUSH_ERROR, None)
    ss.pop(_SS_FLUSH_FAILED_AT, None)
    return not ss[_SS_PENDING]


def record_attempt(student_id: str, student_email: str, student_name: str, lesson_id: str,
                   exercise_id: str, passed: bool, code: str = "", draft: bool = False) -> bool:
    """
    บันทึกการทำ exercise 1 ครั้ง
    - อัปเดต progress ในเซสชันทันที (หน้าจอเห็นผลทันทีแม้ชีตจะมีปัญหา)
    - ส่งลงชีต ถ้าไม่สำเร็จจะเก็บไว้ในคิวแล้วส่งใหม่อัตโนมัติ

    status ในชีต: "passed" / "failed" / "draft" (draft = กดรันโค้ด ยังไม่ได้ตรวจ)
    คืนค่า True ถ้าบันทึกลงชีตสำเร็จแล้ว
    """
    ss = st.session_state
    status = "draft" if draft else ("passed" if passed else "failed")
    row = [
        datetime.datetime.now().isoformat(timespec="seconds"),
        str(student_id), student_email or "", student_name or "",
        lesson_id, exercise_id, status, 1, code or "",
    ]
    ss.setdefault(_SS_SESSION_ROWS, []).append(row)
    ss.setdefault(_SS_PENDING, []).append(row)
    _apply_row(ss.setdefault(_SS_PROGRESS, {}), lesson_id, exercise_id, status, code, row[0])
    return flush_pending(force=True)


# --------------------------------------------------------------------------- #
# Teacher summary
# --------------------------------------------------------------------------- #
def get_class_summary() -> list:
    """
    สรุปความก้าวหน้าทั้งคลาส สำหรับอาจารย์ดูภาพรวม
    คืนค่าเป็น list of dict: [{"student_id", "student_email", "student_name",
                              "passed_count", "total_attempts"}]
    total_attempts นับเฉพาะการกดตรวจคำตอบ (ไม่นับ draft)
    """
    try:
        rows = _fetch_all_rows()
    except Exception:  # noqa: BLE001
        return []
    if not rows:
        return []

    idx = _column_index(rows[0])
    summary = {}
    for row in rows[1:]:
        sid = _cell(row, idx, "student_id").strip()
        if not sid:
            continue
        data = summary.setdefault(sid, {
            "student_id": sid, "student_email": "", "student_name": "",
            "passed_exercises": set(), "total_attempts": 0,
        })
        data["student_email"] = _cell(row, idx, "student_email") or data["student_email"]
        data["student_name"] = _cell(row, idx, "student_name") or data["student_name"]
        status = _cell(row, idx, "status")
        if status in ("passed", "failed"):
            data["total_attempts"] += 1
        if status == "passed":
            data["passed_exercises"].add(_cell(row, idx, "exercise_id"))

    result = [{
        "student_id": d["student_id"],
        "student_email": d["student_email"],
        "student_name": d["student_name"],
        "passed_count": len(d["passed_exercises"]),
        "total_attempts": d["total_attempts"],
    } for d in summary.values()]
    return sorted(result, key=lambda x: x["passed_count"], reverse=True)
