"""บทที่ 10: อ่านและสำรวจข้อมูล"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 10: อ่านและสำรวจข้อมูล")

st.markdown("""
### ข้อมูลตัวอย่างที่ใช้ในบทนี้

บทนี้และบทถัดไปจะใช้ข้อมูลคะแนนนักศึกษา 20 คน (ไฟล์ `data/students.csv`) ซึ่งมีคอลัมน์
`student_id`, `name`, `major`, `year`, `math_score`, `python_score`, `attendance_rate`
ข้อมูลนี้มีค่าขาดหาย (missing value) อยู่บ้างในบางคอลัมน์ ซึ่งเป็นเรื่องปกติของข้อมูลจริง
และจะได้ฝึกจัดการในบทที่ 11

### อ่านไฟล์ CSV ด้วย pandas

`pandas` เป็น library หลักสำหรับทำงานกับข้อมูลแบบตาราง อ่านไฟล์ CSV ได้ในคำสั่งเดียว

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(df)
```

ผลลัพธ์จะถูกเก็บใน **DataFrame** (ตัวแปร `df` ในตัวอย่าง) ซึ่งเป็นโครงสร้างข้อมูลหลัก
ของ pandas — คิดเป็นตารางที่มีแถวและคอลัมน์ เหมือน Excel

### ดูภาพรวมข้อมูล

```python
df.head()        # ดู 5 แถวแรก (ใส่ตัวเลขในวงเล็บเพื่อกำหนดจำนวนแถว เช่น df.head(10))
df.tail()         # ดู 5 แถวสุดท้าย
df.shape           # (จำนวนแถว, จำนวนคอลัมน์)
df.columns          # รายชื่อคอลัมน์ทั้งหมด
df.info()            # ประเภทข้อมูลของแต่ละคอลัมน์ + จำนวนค่าที่ไม่ขาดหาย
df.describe()         # สถิติเบื้องต้น (mean, std, min, max ฯลฯ) ของคอลัมน์ตัวเลข
```

### เลือกและกรองข้อมูล (Selecting & Filtering)

เลือกเฉพาะคอลัมน์ที่ต้องการ

```python
df["name"]                    # เลือกคอลัมน์เดียว (ได้ Series)
df[["name", "math_score"]]    # เลือกหลายคอลัมน์ (ได้ DataFrame ใส่ใน list ซ้อน)
```

กรองแถวตามเงื่อนไข (filtering) — ใช้หลักการเดียวกับ `if` แต่ใช้กับทั้งคอลัมน์พร้อมกัน

```python
high_scorers = df[df["math_score"] >= 80]      # กรองเฉพาะคนที่คะแนน math >= 80
cs_students = df[df["major"] == "Computer Science"]   # กรองเฉพาะสาขา CS

# รวมหลายเงื่อนไข ใช้ & (and) และ | (or) แทน and/or ปกติ พร้อมวงเล็บครอบแต่ละเงื่อนไข
result = df[(df["math_score"] >= 80) & (df["year"] == 2)]
```

### การจัดเรียงข้อมูล (Sorting)

```python
df.sort_values("math_score")                      # เรียงจากน้อยไปมาก
df.sort_values("math_score", ascending=False)       # เรียงจากมากไปน้อย
df.sort_values(["major", "math_score"])              # เรียงหลายคอลัมน์ตามลำดับที่ระบุ
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")
st.info("💡 บทนี้ใช้ pandas ซึ่งโหลดช้ากว่าโค้ดทั่วไปเล็กน้อย ถ้ารันแล้วรอสักครู่ถือว่าปกติ")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (อ่านไฟล์และดูขนาด)")
st.markdown("""
ตัวอย่าง:
```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(df.shape)
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
(20, 7)
```
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex1_copy_readcsv",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="(20, 7)",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด path ของไฟล์คือ data/students.csv ตรงตามที่ระบุไว้ในเนื้อหา",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (เลือกคอลัมน์)")
st.markdown("""
ตัวอย่าง:
```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(list(df["major"].unique()))
```

ทำตามตัวอย่างนี้เป๊ะ ๆ — `.unique()` แสดงค่าที่ไม่ซ้ำกันในคอลัมน์นั้น ครอบด้วย `list()`
เพื่อให้ผลลัพธ์ออกมาเป็น list ธรรมดาที่อ่านง่าย
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex2_copy_unique",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        'print(list(df["major"].unique()))\n'
    ),
    check_type="exact",
    expected_output="['Computer Science', 'Statistics', 'Data Science']",
    hint="โค้ดนี้พร้อมใช้แล้ว ลองกดรันตามที่ให้มาดูผลลัพธ์",
    timeout=15,
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — ดึงชื่อคอลัมน์ทั้งหมด")
st.markdown("""
เติมโค้ดให้นับจำนวนคอลัมน์ทั้งหมดในข้อมูล (ลองกดปุ่ม "รันโค้ด" หลังเติมเสร็จ จะเห็นว่า
ถ้าอยากดูตารางข้อมูลแบบเต็มก่อน สามารถเพิ่ม `print(df.head())` ชั่วคราวดูในช่อง editor ได้
แต่ตอนกด "ตรวจคำตอบ" ให้เอาออกก่อน เพราะระบบจะตรวจจากทุกบรรทัดที่ print ออกมา)
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex3_fill_columncount",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: นับจำนวนคอลัมน์ทั้งหมด เก็บในตัวแปร num_columns\n'
        'num_columns = \n'
        'print(num_columns)\n'
    ),
    check_type="exact",
    expected_output="7",
    hint="ใช้ len(df.columns) นับจำนวนคอลัมน์ — df.columns คือรายชื่อคอลัมน์ทั้งหมดที่เรียนไปในเนื้อหา",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — กรองข้อมูลตามเงื่อนไข")
st.markdown("""
เติมโค้ดให้กรองเฉพาะนักศึกษาที่มี `attendance_rate` มากกว่าเท่ากับ 90 แล้วแสดงจำนวนคน
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex4_fill_filter",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: กรองเฉพาะแถวที่ attendance_rate >= 90 เก็บในตัวแปร high_attendance\n'
        'high_attendance = \n'
        'print(len(high_attendance))\n'
    ),
    check_type="exact",
    expected_output="8",
    hint='ใช้ df[df["attendance_rate"] >= 90] กรองแถวตามเงื่อนไข แล้วใช้ len() นับจำนวนแถวที่ได้',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — เรียงลำดับข้อมูล")
st.markdown("""
เติมโค้ดให้เรียงข้อมูลตาม `python_score` จากมากไปน้อย แล้วแสดงชื่อของคนที่คะแนนสูงสุด
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex5_fill_sort",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: เรียงข้อมูลตาม python_score จากมากไปน้อย เก็บในตัวแปร sorted_df\n'
        'sorted_df = \n'
        'print(sorted_df.iloc[0]["name"])\n'
    ),
    check_type="exact",
    expected_output="สุดา",
    hint='ใช้ df.sort_values("python_score", ascending=False) — สังเกตว่า .iloc[0] ดึงแถวแรกของ '
         'DataFrame ที่เรียงแล้ว แล้ว ["name"] ดึงค่าคอลัมน์ name ของแถวนั้น',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — กรองหลายเงื่อนไข")
st.markdown("""
เติมโค้ดให้กรองเฉพาะนักศึกษาสาขา Data Science ที่มี `math_score` มากกว่า 80
ขึ้นไป (ใช้ `&` รวมสองเงื่อนไข ตามที่เรียนไปในเนื้อหา)
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex6_fill_multifilter",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: กรองเฉพาะ major เป็น Data Science และ math_score > 80\n'
        'result = \n'
        'print(len(result))\n'
    ),
    check_type="exact",
    expected_output="4",
    hint='ใช้ df[(df["major"] == "Data Science") & (df["math_score"] > 80)] — ต้องมีวงเล็บครอบ '
         'แต่ละเงื่อนไขเสมอเวลาใช้ & กับ pandas',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — สถิติเบื้องต้นของคอลัมน์")
st.markdown("""
เติมโค้ดให้แสดงค่าเฉลี่ยของคอลัมน์ `math_score` (ปัดทศนิยม 2 ตำแหน่ง)
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex7_fill_meancol",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: คำนวณค่าเฉลี่ยของคอลัมน์ math_score ปัดทศนิยม 2 ตำแหน่ง\n'
        'avg_math = \n'
        'print(avg_math)\n'
    ),
    check_type="exact",
    expected_output="76.58",
    hint='ใช้ df["math_score"].mean() คำนวณค่าเฉลี่ย แล้วครอบด้วย round(..., 2) — pandas จะข้าม '
         'ค่า missing value (NaN) ในการคำนวณค่าเฉลี่ยให้อัตโนมัติ',
    timeout=15,
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — นับจำนวนนักศึกษาแต่ละสาขา")
st.markdown("""
เขียนฟังก์ชันชื่อ `count_by_major(csv_path)` รับ path ของไฟล์ CSV แล้ว return
dictionary ที่มี key เป็นชื่อสาขา และ value เป็นจำนวนนักศึกษาในสาขานั้น

**แนวทาง:** ใช้ `pd.read_csv()` อ่านไฟล์ก่อน แล้วใช้ method ของ pandas ที่นับจำนวน
ค่าที่ไม่ซ้ำในคอลัมน์ (ลองมองหาใน pandas documentation หรือค้นด้วยคำว่า "value_counts")
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex8_write_countmajor",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef count_by_major(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="count_by_major",
    test_cases=[
        {"args": ("data/students.csv",), "expected": {"Computer Science": 7, "Statistics": 7, "Data Science": 6},
         "label": "นับจำนวนนักศึกษาแต่ละสาขา"},
    ],
    hint='ใช้ df["major"].value_counts() ได้ผลลัพธ์เป็น Series ต้องแปลงเป็น dict ด้วย .to_dict() '
         'ก่อน return — ผลลัพธ์ของ value_counts() จะเรียงจากมากไปน้อยอัตโนมัติแต่ dict ไม่สนใจลำดับ',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — หาผู้ที่คะแนนรวมสูงสุด")
st.markdown("""
เขียนฟังก์ชันชื่อ `top_scorer(csv_path)` รับ path ของไฟล์ CSV แล้ว return ชื่อของ
นักศึกษาที่มีคะแนนรวม (`math_score` + `python_score`) สูงสุด เป็น string

**หมายเหตุ:** ข้อมูลมีค่า missing บางแถว ถ้าแถวไหนมีค่า missing ในคอลัมน์ที่เกี่ยวข้อง
ผลรวมของแถวนั้นจะกลายเป็น NaN และไม่ถูกเลือกเป็นคำตอบ (pandas จัดการเรื่องนี้ให้
อัตโนมัติเมื่อใช้ฟังก์ชันที่เหมาะสม)
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex9_write_topscorer",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef top_scorer(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="top_scorer",
    test_cases=[
        {"args": ("data/students.csv",), "expected": "สุดา", "label": "หาผู้คะแนนรวมสูงสุด"},
    ],
    hint='สร้างคอลัมน์ใหม่ชื่อ total_score = df["math_score"] + df["python_score"] ก่อน '
         'แล้วใช้ df.sort_values("total_score", ascending=False) เรียงจากมากไปน้อย '
         'จากนั้นดึงชื่อของแถวแรกด้วย .iloc[0]["name"]',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — กรองและนับตามเงื่อนไขซับซ้อน")
st.markdown("""
เขียนฟังก์ชันชื่อ `count_at_risk_students(csv_path)` รับ path ของไฟล์ CSV แล้ว return
จำนวนนักศึกษาที่ "มีความเสี่ยง" ตามเกณฑ์: `attendance_rate` ต่ำกว่า 80 **หรือ**
`math_score` ต่ำกว่า 60 (เข้าเกณฑ์ข้อใดข้อหนึ่งก็ถือว่ามีความเสี่ยง)
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex10_write_atrisk",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef count_at_risk_students(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="count_at_risk_students",
    test_cases=[
        {"args": ("data/students.csv",), "expected": 7, "label": "นับนักศึกษากลุ่มเสี่ยง"},
    ],
    hint='ใช้ df[(df["attendance_rate"] < 80) | (df["math_score"] < 60)] กรองตามเงื่อนไข '
         'สังเกตว่าใช้ | (หรือ) ไม่ใช่ & (และ) เพราะเข้าเกณฑ์ข้อใดข้อหนึ่งก็พอ แล้วใช้ len() นับจำนวนแถว',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — สรุปข้อมูลตามชั้นปี")
st.markdown("""
เขียนฟังก์ชันชื่อ `average_score_by_year(csv_path, year)` รับ path ของไฟล์ CSV และ
ชั้นปีที่ต้องการ (`year`) แล้ว return ค่าเฉลี่ยของ `python_score` เฉพาะนักศึกษาชั้นปีนั้น
ปัดทศนิยม 2 ตำแหน่ง ถ้าไม่มีนักศึกษาในชั้นปีนั้นเลย ให้ return `None`
""")

render_exercise(
    lesson_id="lesson10", exercise_id="ex11_write_avgbyyear",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef average_score_by_year(csv_path, year):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="average_score_by_year",
    test_cases=[
        {"args": ("data/students.csv", 1), "expected": 73.75, "label": "ชั้นปี 1"},
        {"args": ("data/students.csv", 4), "expected": 70.67, "label": "ชั้นปี 4"},
        {"args": ("data/students.csv", 99), "expected": None, "label": "ชั้นปีที่ไม่มีอยู่จริง"},
    ],
    hint='กรองข้อมูลด้วย df[df["year"] == year] ก่อน ถ้าผลลัพธ์ที่กรองได้มีความยาว (len) เป็น 0 '
         'ให้ return None ทันที ไม่งั้นคำนวณค่าเฉลี่ยของ python_score ในกลุ่มที่กรองได้ แล้วปัดทศนิยม',
    timeout=15,
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/9_บทที่9_numpy.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/11_บทที่11_จัดการข้อมูล.py", label="ไปบทต่อไป: จัดการและแสดงผลข้อมูล ➡️")
