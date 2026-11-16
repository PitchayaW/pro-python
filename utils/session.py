"""
จำการเข้าสู่ระบบไว้ใน URL (query parameters) เพื่อให้ refresh หน้า, ปิดแล้วเปิดแท็บเดิม,
หรือบุ๊กมาร์กลิงก์ไว้ กลับมาแล้วยังล็อกอินอยู่ ไม่ต้องกรอกใหม่

st.session_state ของ Streamlit จะหายทุกครั้งที่ refresh หรือเปิดหน้าใหม่ จึงต้องมีที่เก็บ
อีกชั้นหนึ่ง ส่วน URL เป็นวิธีที่ไม่ต้องเพิ่ม package และใช้ได้ทุกเบราว์เซอร์
"""

import re

import streamlit as st

STUDENT_ID_RE = re.compile(r"^\d{9}-\d$")
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@kkumail\.com$")

_QP_ID, _QP_EMAIL, _QP_NAME = "sid", "email", "name"


def is_valid_login(student_id: str, student_email: str) -> bool:
    return bool(STUDENT_ID_RE.match(student_id or "")) and bool(EMAIL_RE.match((student_email or "").lower()))


def set_login(student_id: str, student_email: str, student_name: str = ""):
    st.session_state["student_id"] = student_id
    st.session_state["student_email"] = student_email
    st.session_state["student_name"] = student_name
    sync_login_to_url()


def restore_login_from_url():
    """ถ้า session ยังไม่ได้ล็อกอิน แต่ URL มีข้อมูลล็อกอินที่ถูกต้อง ให้ล็อกอินอัตโนมัติ"""
    if "student_id" in st.session_state:
        return
    qp = st.query_params
    sid = qp.get(_QP_ID, "").strip()
    email = qp.get(_QP_EMAIL, "").strip()
    if is_valid_login(sid, email):
        st.session_state["student_id"] = sid
        st.session_state["student_email"] = email
        st.session_state["student_name"] = qp.get(_QP_NAME, "").strip()


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
    for key in ("student_id", "student_email", "student_name"):
        st.session_state.pop(key, None)
    for key in (_QP_ID, _QP_EMAIL, _QP_NAME):
        if key in st.query_params:
            del st.query_params[key]
