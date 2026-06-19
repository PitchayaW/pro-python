"""
Entry point ของแอป — ใช้ st.navigation เพื่อกำหนดชื่อหน้า (title) ที่แสดงใน
sidebar navigation menu เอง ไม่ให้พึ่งชื่อไฟล์ (ซึ่งจะโชว์เป็น "app" ถ้าใช้ระบบ
pages/ folder อัตโนมัติแบบเดิมของ Streamlit)
"""

import streamlit as st

st.set_page_config(
    page_title="เรียนไพธอนแบบอินเทอร์แอกทีฟ",
    page_icon="🐍",
    layout="wide",
)

pg = st.navigation([
    st.Page("pages/intro.py", title="บทนำ", icon="🏠", default=True),
    st.Page("pages/0_บทที่0_ความเป็นมา.py", title="บทที่ 0: ความเป็นมาของไพธอน"),
    st.Page("pages/1_บทที่1_การติดตั้ง.py", title="บทที่ 1: การติดตั้งและใช้งาน"),
    st.Page("pages/2_บทที่2_ตัวแปร.py", title="บทที่ 2: ตัวแปรและ Data Type"),
    st.Page("pages/3_บทที่3_data_structure.py", title="บทที่ 3: Data Structure"),
    st.Page("pages/4_บทที่4_conditions.py", title="บทที่ 4: Conditions"),
    st.Page("pages/5_บทที่5_loops.py", title="บทที่ 5: Loops"),
    st.Page("pages/6_บทที่6_functions.py", title="บทที่ 6: Functions"),
    st.Page("pages/7_บทที่7_error_handling.py", title="บทที่ 7: Error Handling"),
    st.Page("pages/8_บทที่8_built_in_functions.py", title="บทที่ 8: ฟังก์ชันสำเร็จรูปและ Library"),
    st.Page("pages/9_บทที่9_numpy.py", title="บทที่ 9: NumPy และ Linear Algebra"),
    st.Page("pages/10_บทที่10_อ่านข้อมูล.py", title="บทที่ 10: อ่านและสำรวจข้อมูล"),
    st.Page("pages/11_บทที่11_จัดการข้อมูล.py", title="บทที่ 11: จัดการและแสดงผลข้อมูล"),
])

pg.run()
