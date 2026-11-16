"""
Entry point ของแอป: ใช้ st.navigation เพื่อกำหนดชื่อหน้า (title) ที่แสดงใน
sidebar navigation menu เอง ไม่ให้พึ่งชื่อไฟล์

ไฟล์นี้รันทุกครั้งก่อนหน้าบทเรียน จึงใช้เป็นที่:
- กู้การเข้าสู่ระบบจาก URL (refresh/กลับมาแล้วไม่ต้องล็อกอินใหม่)
- โหลดความคืบหน้าจาก Google Sheet ครั้งเดียวต่อเซสชัน และส่งรายการที่ค้างบันทึก
- แสดงความคืบหน้าของแต่ละบทในเมนูด้านซ้าย
"""

import streamlit as st

from utils.lessons import LESSONS, passed_in_lesson
from utils.progress import get_progress, flush_pending
from utils.session import restore_login_from_url, sync_login_to_url

st.set_page_config(
    page_title="Learn Python Programming",
    page_icon="🐍",
    layout="wide",
)

restore_login_from_url()
sync_login_to_url()

progress = {}
if "student_id" in st.session_state:
    progress = get_progress()
flush_pending()   # ส่งแถวที่เคยบันทึกไม่สำเร็จ (ไม่ทำอะไรถ้าไม่มีค้าง)

pages = [st.Page("pages/intro.py", title="บทนำ", icon="🏠", default=True)]
for lesson in LESSONS:
    title, icon = lesson["nav"], None
    if progress and lesson["total"]:
        done = passed_in_lesson(progress, lesson["id"])
        if done >= lesson["total"]:
            icon = "✅"
        elif done:
            title = f"{title} ({done}/{lesson['total']})"
    pages.append(st.Page(lesson["page"], title=title, icon=icon))

pg = st.navigation(pages)
pg.run()
