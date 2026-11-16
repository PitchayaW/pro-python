"""
Python for Data Science: Interactive Course
บทนำ: เข้าสู่ระบบ + ภาพรวมบทเรียนและความคืบหน้า
"""

import streamlit as st

from utils.lessons import LESSONS, TOTAL_EXERCISES, continue_lesson, passed_in_lesson, passed_total
from utils.progress import get_progress
from utils.ui_components import render_student_login, render_progress_sidebar

st.title("🐍 Learn Python Programming")
st.caption("เตรียมพื้นฐาน Python: เขียนโค้ดจริง รันจริง เห็นผลทันที")

if "student_id" not in st.session_state:
    render_student_login()
    st.stop()

render_progress_sidebar()
progress = get_progress()

# ---------- ความคืบหน้าของฉัน ----------
done = passed_total(progress)
st.markdown("### 📈 ความคืบหน้าของฉัน")
c1, c2 = st.columns([3, 2])
with c1:
    st.progress(min(done / TOTAL_EXERCISES, 1.0) if TOTAL_EXERCISES else 0.0,
                text=f"ผ่านแล้ว {done} จาก {TOTAL_EXERCISES} แบบฝึกหัด")
with c2:
    nxt = continue_lesson(progress)
    if nxt:
        st.page_link(nxt["page"], label=f"ทำต่อ: บทที่ {nxt['no']} {nxt['title']}", icon="▶️")
    elif done and done >= TOTAL_EXERCISES:
        st.success("🎉 ทำครบทุกแบบฝึกหัดแล้ว")
    else:
        st.page_link(LESSONS[0]["page"], label="เริ่มเรียนบทที่ 0", icon="▶️")

# ---------- บทเรียนทั้งหมด ----------
st.markdown("### 📚 บทเรียนทั้งหมด")
st.markdown("คลิกชื่อบทเพื่อเข้าเรียน แต่ละบทมีตัวอย่าง โจทย์ฝึก และ code editor ให้เขียนโค้ดเองได้เลย")

cols = st.columns(3)
for i, lesson in enumerate(LESSONS):
    with cols[i % 3]:
        with st.container(border=True):
            total = lesson["total"]
            passed = passed_in_lesson(progress, lesson["id"]) if total else 0
            icon = "✅" if total and passed >= total else ("📝" if passed else "📖")
            st.page_link(lesson["page"], label=f"บทที่ {lesson['no']}: {lesson['title']}", icon=icon)
            st.caption(lesson["desc"])
            if total:
                st.progress(min(passed / total, 1.0), text=f"ผ่าน {passed}/{total} ข้อ")
            else:
                st.caption("บทอ่าน (ไม่มีแบบฝึกหัด)")
