"""
Python for Data Science — Interactive Course
บทนำ: เข้าสู่ระบบ + ภาพรวมบทเรียน
"""

import streamlit as st
from utils.ui_components import render_student_login, render_progress_sidebar

LESSONS = [
    {"id": "lesson00", "no": 0, "title": "ความเป็นมาของไพธอน", "desc": "รู้จักไพธอนและเหตุผลที่ควรเรียน"},
    {"id": "lesson01", "no": 1, "title": "การติดตั้งและใช้งาน", "desc": "Anaconda, Jupyter, Cloud, การติดตั้ง package"},
    {"id": "lesson02", "no": 2, "title": "ตัวแปรและ Data Type", "desc": "int, float, str, bool"},
    {"id": "lesson03", "no": 3, "title": "Data Structure", "desc": "list, tuple, dict, set, 2D list"},
    {"id": "lesson04", "no": 4, "title": "Conditions", "desc": "if, elif, else, in — ฝึกตรรกะ"},
    {"id": "lesson05", "no": 5, "title": "Loops", "desc": "for, while — ฝึกตรรกะ"},
    {"id": "lesson06", "no": 6, "title": "Functions", "desc": "def, parameter, return, scope"},
    {"id": "lesson07", "no": 7, "title": "Error Handling", "desc": "try, except — จัดการข้อผิดพลาด"},
    {"id": "lesson08", "no": 8, "title": "ฟังก์ชันสำเร็จรูปและ Library", "desc": "built-in functions, import"},
    {"id": "lesson09", "no": 9, "title": "NumPy และ Linear Algebra เบื้องต้น", "desc": "matrix, vector, การคำนวณเชิงเส้น"},
    {"id": "lesson10", "no": 10, "title": "อ่านและสำรวจข้อมูล", "desc": "pandas: อ่านไฟล์, head, info, filter"},
    {"id": "lesson11", "no": 11, "title": "จัดการและแสดงผลข้อมูล", "desc": "clean, groupby, visualization เบื้องต้น"},
]

st.title("🐍 Learn Python Programming")
st.caption("เตรียมพื้นฐาน Python — เขียนโค้ดจริง รันจริง เห็นผลทันที")

if "student_id" not in st.session_state:
    render_student_login()
    st.stop()

render_progress_sidebar()

st.markdown("### 📚 บทเรียนทั้งหมด")
st.markdown("เลือกบทเรียนจากเมนูด้านซ้าย (sidebar) — แต่ละบทมีตัวอย่าง โจทย์ฝึก และ code editor ให้เขียนโค้ดเองได้เลย")

cols = st.columns(3)
for i, lesson in enumerate(LESSONS):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"**บทที่ {lesson['no']}: {lesson['title']}**")
            st.caption(lesson["desc"])

st.markdown("---")
st.info("👈 เริ่มจากบทที่ 0 ในเมนูด้านซ้าย แล้วไล่ตามลำดับได้เลยครับ")
