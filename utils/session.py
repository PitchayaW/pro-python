"""
จำการเข้าสู่ระบบไว้ใน URL (query parameters) เพื่อให้ refresh หน้า, ปิดแล้วเปิดแท็บเดิม,
หรือบุ๊กมาร์กลิงก์ไว้ กลับมาแล้วยังล็อกอินอยู่ ไม่ต้องกรอกใหม่

st.session_state ของ Streamlit จะหายทุกครั้งที่ refresh หรือเปิดหน้าใหม่ จึงต้องมีที่เก็บ
อีกชั้นหนึ่ง ส่วน URL เป็นวิธีที่ไม่ต้องเพิ่ม package และใช้ได้ทุกเบราว์เซอร์
"""

import json
import re
from urllib.parse import quote, unquote

import streamlit as st

STUDENT_ID_RE = re.compile(r"^\d{9}-\d$")
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@kkumail\.com$")

_QP_ID, _QP_EMAIL, _QP_NAME = "sid", "email", "name"
COOKIE_NAME = "pro_python_login"
COOKIE_DAYS = 180


def is_valid_login(student_id: str, student_email: str) -> bool:
    return bool(STUDENT_ID_RE.match(student_id or "")) and bool(EMAIL_RE.match((student_email or "").lower()))


def set_login(student_id: str, student_email: str, student_name: str = ""):
    st.session_state.pop("_logged_out", None)
    st.session_state["student_id"] = student_id
    st.session_state["student_email"] = student_email
    st.session_state["student_name"] = student_name
    sync_login_to_url()


def _login_from_cookie():
    try:
        raw = st.context.cookies.get(COOKIE_NAME)
    except Exception:  # noqa: BLE001
        return None
    if not raw:
        return None
    try:
        data = json.loads(unquote(raw))
        return str(data.get("sid", "")).strip(), str(data.get("email", "")).strip(), str(data.get("name", "")).strip()
    except Exception:  # noqa: BLE001
        return None


def restore_login_from_url():
    """
    ถ้า session ยังไม่ได้ล็อกอิน ให้ล็อกอินอัตโนมัติจาก
    1) URL (?sid=...&email=...) หรือ
    2) cookie ในเบราว์เซอร์ (เปิด pro-python.streamlit.app เปล่า ๆ ก็ยังจำได้)
    """
    ss = st.session_state
    if "student_id" in ss:
        return
    qp = st.query_params
    sid = qp.get(_QP_ID, "").strip()
    email = qp.get(_QP_EMAIL, "").strip()
    name = qp.get(_QP_NAME, "").strip()
    if not is_valid_login(sid, email):
        # หลังกดออกจากระบบ cookie ใน request เดิมยังอยู่ จึงห้ามใช้ cookie ในเซสชันนี้อีก
        cookie = None if ss.get("_logged_out") else _login_from_cookie()
        if not cookie:
            return
        sid, email, name = cookie
        if not is_valid_login(sid, email):
            return
    ss["student_id"] = sid
    ss["student_email"] = email
    ss["student_name"] = name


def render_cookie_script():
    """
    เขียน/ลบ cookie ในเบราว์เซอร์ด้วย JavaScript (st.context.cookies อ่านได้อย่างเดียว)
    เรียกทุกครั้งที่รัน: ถ้าล็อกอินอยู่ให้บันทึก cookie ไว้ ถ้าเพิ่งออกจากระบบให้ลบ cookie
    """
    ss = st.session_state
    if ss.get("student_id"):
        value = quote(json.dumps({
            "sid": ss["student_id"], "email": ss.get("student_email", ""),
            "name": ss.get("student_name", ""),
        }, ensure_ascii=False))
        js = (f'document.cookie = "{COOKIE_NAME}={value}; path=/; '
              f'max-age={COOKIE_DAYS * 86400}; SameSite=Lax; Secure";')
    elif ss.get("_logged_out"):
        js = f'document.cookie = "{COOKIE_NAME}=; path=/; max-age=0; SameSite=Lax; Secure";'
    else:
        # ยังไม่ได้ล็อกอิน: Streamlit Cloud ไม่ส่ง cookie ให้ server อ่าน จึงให้เบราว์เซอร์อ่าน cookie เอง
        # แล้วเปิดหน้าใหม่พร้อม ?sid=...&email=... ซึ่ง restore_login_from_url จะล็อกอินให้
        js = """
(function () {
  try {
    var m = document.cookie.match(/(?:^|; )%s=([^;]*)/);
    if (!m) return;
    var d = JSON.parse(decodeURIComponent(m[1]));
    if (!d.sid || !d.email) return;
    var w = window;
    try { if (window.top.location.href) w = window.top; } catch (e) {}
    var u = new URL(w.location.href);
    if (u.searchParams.get("sid")) return;
    u.searchParams.set("sid", d.sid);
    u.searchParams.set("email", d.email);
    if (d.name) u.searchParams.set("name", d.name);
    w.location.replace(u.toString());
  } catch (e) {}
})();""" % COOKIE_NAME
    if ss.get("_cookie_js") == js:
        return    # เขียนไปแล้วในเซสชันนี้
    ss["_cookie_js"] = js
    st.html(f"<script>{js}</script>", unsafe_allow_javascript=True)


def sync_login_to_url():
    """
    เขียนข้อมูลล็อกอินลง URL ทุกครั้งที่รัน (การเปลี่ยนหน้าใน st.navigation จะล้าง query params
    จึงต้องใส่กลับทุกรอบ)
    """
    sid = st.session_state.get("student_id")
    if not sid:
        return
    wanted = {_QP_ID: sid, _QP_EMAIL: st.session_state.get("student_email", "")}
    name = st.session_state.get("student_name", "")
    if name:
        wanted[_QP_NAME] = name
    for key, value in wanted.items():
        if st.query_params.get(key) != value:
            st.query_params[key] = value
    if not name and _QP_NAME in st.query_params:
        del st.query_params[_QP_NAME]


def clear_login():
    st.session_state["_logged_out"] = True
    for key in ("student_id", "student_email", "student_name"):
        st.session_state.pop(key, None)
    for key in (_QP_ID, _QP_EMAIL, _QP_NAME):
        if key in st.query_params:
            del st.query_params[key]
