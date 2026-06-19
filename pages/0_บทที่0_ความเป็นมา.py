"""บทที่ 0: ความเป็นมาของไพธอน"""

import streamlit as st
from utils.ui_components import render_progress_sidebar


if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 0: ความเป็นมาของไพธอน")

st.markdown("""
### ไพธอนคืออะไร

ไพธอน (Python) เป็นภาษาโปรแกรมที่สร้างโดย **Guido van Rossum** เริ่มพัฒนาในปี 1989
และเปิดตัวอย่างเป็นทางการในปี 1991 ชื่อ "Python" มาจากรายการตลกของอังกฤษ
*Monty Python's Flying Circus* ที่ Guido ชื่นชอบ — ไม่ได้มาจากชื่องูอย่างที่หลายคนเข้าใจ

แนวคิดหลักของไพธอนคือการเขียนโค้ดให้ **อ่านง่าย เข้าใจง่าย** เหมือนภาษาคนพูด
ต่างจากภาษาโปรแกรมยุคก่อนที่เน้นความเร็วของเครื่องมากกว่าความเข้าใจของมนุษย์

### ทำไมไพธอนถึงเหมาะกับ Data Science

| จุดเด่น | อธิบาย |
|---|---|
| Syntax อ่านง่าย | เหมาะกับคนที่ไม่ได้มาจากสาย Computer Science โดยตรง |
| Library ครบ | pandas, numpy, scikit-learn, TensorFlow ครอบคลุมงานข้อมูลทุกขั้นตอน |
| Community ใหญ่ | หาตัวอย่างโค้ด คำตอบ และความช่วยเหลือได้ง่ายมาก |
| ใช้ได้หลายงาน | Data Science, Web, Automation, AI ใช้ภาษาเดียวกันได้หมด |

### ไพธอนในโลกการทำงานจริง

องค์กรใหญ่อย่าง Google, Netflix, Instagram ใช้ไพธอนในระบบสำคัญ
ส่วนในงาน Data Science และ Machine Learning ไพธอนถือเป็นภาษาอันดับหนึ่งที่ใช้กันทั่วโลก
เพราะมี ecosystem ของ library ด้านข้อมูลที่สมบูรณ์ที่สุด
""")

st.markdown("---")
st.markdown("### 🤔 ตรวจความเข้าใจ")
st.markdown("ลองตอบคำถามต่อไปนี้ก่อนไปบทต่อไป (ไม่มีคะแนน แค่ทบทวนความเข้าใจ)")

q1 = st.radio(
    "1. ชื่อ 'Python' มาจากอะไร?",
    ["ชื่องูหลามที่ผู้สร้างชอบ", "รายการตลกของอังกฤษที่ผู้สร้างชอบ", "ชื่อบริษัทที่ผู้สร้างทำงานอยู่"],
    index=None,
)
if q1:
    if q1 == "รายการตลกของอังกฤษที่ผู้สร้างชอบ":
        st.success("ถูกต้อง! มาจาก Monty Python's Flying Circus ✅")
    else:
        st.error("ลองอ่านเนื้อหาข้างบนอีกครั้งนะครับ")

st.markdown("---")
col1, col2 = st.columns(2)
with col2:
    st.page_link("pages/1_บทที่1_การติดตั้ง.py", label="ไปบทต่อไป: การติดตั้งและใช้งาน ➡️")
