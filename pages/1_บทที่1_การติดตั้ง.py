"""บทที่ 1: การติดตั้งและใช้งาน"""

import streamlit as st
from utils.ui_components import render_progress_sidebar


if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 1: การติดตั้งและใช้งานไพธอน")

st.markdown("""
ไพธอนใช้งานได้หลายรูปแบบ แต่ละแบบเหมาะกับสถานการณ์ต่างกัน
ในคอร์สนี้คุณกำลังใช้ไพธอนผ่านเว็บแอปนี้อยู่แล้ว (ไม่ต้องติดตั้งอะไร)
แต่ควรรู้จักวิธีอื่น ๆ ด้วย เผื่อต้องใช้งานนอกห้องเรียน
""")

tab1, tab2, tab3 = st.tabs(["💻 ติดตั้งในเครื่อง (Anaconda)", "📓 Jupyter Notebook", "☁️ ใช้งานผ่าน Cloud"])

with tab1:
    st.markdown("""
    ### Anaconda — ติดตั้งในคอมพิวเตอร์ตัวเอง

    Anaconda เป็นชุดติดตั้งไพธอนที่รวม library สำหรับ Data Science มาให้พร้อม
    (pandas, numpy, matplotlib ฯลฯ) ไม่ต้องติดตั้งทีละตัวเอง

    **ขั้นตอนคร่าว ๆ:**
    1. ดาวน์โหลดจาก [anaconda.com](https://www.anaconda.com/download)
    2. ติดตั้งตามค่าเริ่มต้น (Next ไปเรื่อย ๆ ได้)
    3. เปิดโปรแกรม **Anaconda Navigator** เพื่อเข้าถึงเครื่องมือต่าง ๆ
    4. หรือเปิด **Anaconda Prompt** (Windows) / Terminal (Mac) แล้วพิมพ์ `python` เพื่อเริ่มใช้งาน

    **ข้อดี:** ควบคุมเครื่องตัวเองได้เต็มที่ ทำงานได้แม้ไม่มีอินเทอร์เน็ต
    **ข้อเสีย:** ใช้พื้นที่เก็บข้อมูลมาก (หลาย GB) และตั้งค่าซับซ้อนกว่าวิธีอื่น
    """)

with tab2:
    st.markdown("""
    ### Jupyter Notebook — เขียนโค้ดทีละ "เซลล์"

    Jupyter Notebook คือเครื่องมือที่ให้เขียนโค้ดเป็นช่อง ๆ (cell) แล้วรันทีละช่องได้
    เหมาะกับการทดลอง วิเคราะห์ข้อมูล และดูผลลัพธ์ทันที (เช่น กราฟ ตาราง)

    **วิธีเปิดใช้งาน:**
    - ถ้าติดตั้ง Anaconda แล้ว เปิดผ่าน Anaconda Navigator ได้เลย
    - หรือพิมพ์คำสั่ง `jupyter notebook` ใน Terminal/Command Prompt

    **จุดเด่นของ Jupyter:**
    - รันโค้ดทีละส่วนได้ ไม่ต้องรันทั้งไฟล์
    - แสดงกราฟ ตาราง รูปภาพ ได้ในหน้าเดียวกัน
    - เหมาะกับงาน Data Science ที่ต้องสำรวจข้อมูลไปเรื่อย ๆ
    """)

with tab3:
    st.markdown("""
    ### ใช้งานผ่าน Cloud — ไม่ต้องติดตั้งอะไรเลย

    ถ้าไม่อยากติดตั้งโปรแกรมในเครื่อง สามารถเขียนไพธอนผ่านเว็บเบราว์เซอร์ได้ทันที

    **Google Colab** (แนะนำสำหรับเริ่มต้น)
    - เข้าผ่าน [colab.research.google.com](https://colab.research.google.com)
    - ใช้ Google Account ที่มีอยู่แล้วได้เลย ไม่ต้องติดตั้ง
    - มี library สำหรับ Data Science ติดมาให้พร้อม

    **เว็บแอปนี้**
    - ไม่ต้องติดตั้งอะไร เขียนโค้ดในช่อง editor แล้วกดรันได้ทันที
    - เหมาะสำหรับฝึกฝนตามบทเรียนนี้โดยเฉพาะ

    **ข้อดีของ Cloud:** เริ่มใช้งานได้ทันที ไม่ต้องตั้งค่าเครื่อง ใช้เครื่องไหนก็ได้
    **ข้อเสีย:** ต้องมีอินเทอร์เน็ตตลอดเวลาที่ใช้งาน
    """)

st.markdown("---")
st.markdown("""
### การติดตั้ง Package เพิ่มเติม

เมื่อต้องใช้ library ที่ไม่ได้ติดมาให้ตั้งแต่แรก ใช้คำสั่งติดตั้งผ่าน `pip`
(ถ้าใช้ Anaconda จะมีคำสั่ง `conda` ให้ใช้แทนได้เช่นกัน)

```bash
pip install pandas
pip install scikit-learn
```

ในเว็บแอปนี้ library ที่จำเป็น (pandas, numpy, matplotlib) ถูกติดตั้งไว้ให้เรียบร้อยแล้ว
""")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/0_บทที่0_ความเป็นมา.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/2_บทที่2_ตัวแปร.py", label="ไปบทต่อไป: ตัวแปรและ Data Type ➡️")
