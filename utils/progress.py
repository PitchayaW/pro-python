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
import threading
import time

import streamlit as st

HEADER = ["timestamp", "student_id", "student_email", "student_name", "lesson_id",
          "exercise_id", "status", "attempts", "code"]

RETRY_COOLDOWN_SEC = 20     # เว้นระยะก่อนลองอ่าน/เขียนชีตใหม่หลังล้มเหลว (กันยิง API รัว ๆ)
CACHE_TTL_SEC = 60          # อายุของสำเนาชีตที่แชร์ร่วมกันทุกเซสชัน

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

    # แก้หัวตารางแบบเก่า (8 คอลัมน์) ให้ตรงกับข้อมูลจริง 9 คอลัมน์ อาจารย์จะได้อ่านชีตถูก
    try:
        first = _with_retry(lambda: ws.row_values(1))
        if first and first[0].strip() == "timestamp" and first[:len(HEADER)] != HEADER:
            ws.update(range_name="A1:I1", values=[HEADER], value_input_option="RAW")
    except Exception:  # noqa: BLE001
        pass   # แก้หัวตารางไม่ได้ก็ไม่เป็นไร การอ่านไม่ได้อิงหัวตารางแล้ว
    return ws


@st.cache_resource(show_spinner=False)
def _shared_store() -> dict:
    """สำเนาข้อมูลชีตที่แชร์ร่วมกันทุกเซสชัน (อยู่ในหน่วยความจำของ server)"""
    return {"rows": None, "fetched_at": 0.0, "last_write": 0.0, "lock": threading.Lock()}


def _fetch_all_rows(force: bool = False) -> list:
    """
    อ่านทุกแถวในชีต โดยใช้สำเนากลางอายุ CACHE_TTL_SEC วินาที (ทั้งห้องอ่านชีตจริงแค่ครั้งเดียว)
    ทุกครั้งที่บันทึกสำเร็จ แถวใหม่จะถูกเพิ่มเข้าสำเนากลางด้วย (_append_to_shared)
    จึงไม่เกิดกรณีล็อกอินใหม่แล้วไม่เห็นข้อที่เพิ่งทำ
    ถ้าอ่านล้มเหลวจะ raise ออกไป และไม่เก็บผลลัพธ์ว่างไว้
    """
    store = _shared_store()
    with store["lock"]:
        if not force and store["rows"] is not None and time.time() - store["fetched_at"] < CACHE_TTL_SEC:
            return store["rows"]
    started = time.time()
    rows = _with_retry(_get_worksheet().get_all_values)
    rows = [[str(c) for c in r] for r in rows]
    with store["lock"]:
        # ถ้ามีการบันทึกเกิดขึ้นระหว่างที่กำลังอ่าน ข้อมูลที่อ่านมาอาจไม่มีแถวนั้น
        # ให้คงสำเนาเดิม (ที่ต่อแถวใหม่ไว้แล้ว) และให้อ่านใหม่รอบหน้า
        if store["last_write"] >= started and store["rows"] is not None:
            store["fetched_at"] = 0.0
            return store["rows"]
        store["rows"] = rows
        store["fetched_at"] = time.time()
    return rows


def _append_to_shared(rows: list):
    store = _shared_store()
    with store["lock"]:
        store["last_write"] = time.time()
        if store["rows"] is not None:
            store["rows"].extend([[str(c) for c in r] for r in rows])


def _parse_row(row: list) -> dict:
    """
    แปลง 1 แถวในชีตเป็น dict โดยอิง "ตำแหน่งคอลัมน์" ที่แอปเขียนจริง ไม่อิงหัวตาราง
    (หัวตารางในชีตเดิมเป็นแบบเก่า 8 คอลัมน์ ทำให้การอ่านตามชื่อหัวตารางเลื่อนไปหนึ่งช่อง
    และหาสถานะ passed ไม่เจอเลย)

    รองรับ 2 รูปแบบ:
    - ปัจจุบัน 9 คอลัมน์: timestamp, student_id, student_email, student_name, lesson_id,
      exercise_id, status, attempts, code
    - แบบเก่า 8 คอลัมน์ (ไม่มี email): timestamp, student_id, student_name, lesson_id,
      exercise_id, status, attempts, code
    """
    r = [str(c) for c in row] + [""] * (len(HEADER) - len(row))
    statuses = ("passed", "failed", "draft")
    if r[6].strip() not in statuses and r[5].strip() in statuses:
        return {"timestamp": r[0], "student_id": r[1].strip(), "student_email": "",
                "student_name": r[2], "lesson_id": r[3], "exercise_id": r[4],
                "status": r[5].strip(), "code": r[7]}
    return {"timestamp": r[0], "student_id": r[1].strip(), "student_email": r[2],
            "student_name": r[3], "lesson_id": r[4], "exercise_id": r[5],
            "status": r[6].strip(), "code": r[8]}


def _data_rows(rows: list) -> list:
    """ตัดแถวหัวตารางออก (ถ้ามี) แล้วแปลงทุกแถวเป็น dict"""
    if rows and str(rows[0][0] if rows[0] else "").strip() == "timestamp":
        rows = rows[1:]
    return [_parse_row(r) for r in rows if r]


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
    if code and code.strip() != "None":   # แถวเก่าบางแถวบันทึกโค้ดเป็นคำว่า None
        entry["code"] = code
    if ts:
        entry["ts"] = ts


def _build_progress(rows: list, student_id: str) -> dict:
    progress = {}
    sid = str(student_id).strip()
    for d in _data_rows(rows):
        if d["student_id"] == sid:
            _apply_row(progress, d["lesson_id"], d["exercise_id"], d["status"], d["code"], d["timestamp"])
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
        rows = _fetch_all_rows(force=force)
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
        _append_to_shared(batch)
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
    summary = {}
    for d in _data_rows(rows):
        sid = d["student_id"]
        if not sid:
            continue
        data = summary.setdefault(sid, {
            "student_id": sid, "student_email": "", "student_name": "",
            "passed_exercises": set(), "total_attempts": 0,
        })
        data["student_email"] = d["student_email"] or data["student_email"]
        data["student_name"] = d["student_name"] or data["student_name"]
        status = d["status"]
        if status in ("passed", "failed"):
            data["total_attempts"] += 1
        if status == "passed":
            data["passed_exercises"].add(d["exercise_id"])

    result = [{
        "student_id": d["student_id"],
        "student_email": d["student_email"],
        "student_name": d["student_name"],
        "passed_count": len(d["passed_exercises"]),
        "total_attempts": d["total_attempts"],
    } for d in summary.values()]
    return sorted(result, key=lambda x: x["passed_count"], reverse=True)
