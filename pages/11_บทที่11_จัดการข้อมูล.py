"""บทที่ 11: จัดการข้อมูล"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 11: จัดการข้อมูล")

st.markdown("""
บทนี้ใช้ข้อมูลเดียวกับบทที่แล้ว (`data/students.csv`) ซึ่งมีค่าขาดหาย (missing value)
อยู่บ้าง — เป็นสถานการณ์ปกติของข้อมูลจริงที่ต้องจัดการก่อนนำไปวิเคราะห์ต่อ

### ตรวจสอบค่าขาดหาย (Missing Values)

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(df.isnull().sum())     # นับจำนวนค่าขาดหายในแต่ละคอลัมน์
```

`isnull()` คืนค่า `True`/`False` ของทุกตำแหน่งว่าขาดหายหรือไม่ ส่วน `.sum()` รวมจำนวน
`True` ในแต่ละคอลัมน์ (เพราะ `True` นับเป็น 1 ส่วน `False` นับเป็น 0)

### จัดการค่าขาดหายด้วย fillna และ dropna

**fillna** — เติมค่าแทนที่ค่าขาดหาย (เช่น เติมด้วยค่าเฉลี่ยของคอลัมน์นั้น)

```python
mean_score = df["math_score"].mean()
df["math_score"] = df["math_score"].fillna(mean_score)
print(df["math_score"].isnull().sum())   # 0 — ไม่มีค่าขาดหายแล้ว
```

**dropna** — ลบแถวที่มีค่าขาดหายออกไปทั้งแถว

```python
df_clean = df.dropna()    # ลบทุกแถวที่มีค่าขาดหายอย่างน้อย 1 คอลัมน์
print(len(df_clean))       # จำนวนแถวที่เหลือ (น้อยกว่าจำนวนแถวเดิม)
```

เลือกใช้วิธีไหนขึ้นอยู่กับสถานการณ์: `dropna` เหมาะกับกรณีข้อมูลขาดหายน้อยและไม่อยาก
เสี่ยงกับค่าที่เติมเอง ส่วน `fillna` เหมาะกับกรณีอยากเก็บข้อมูลทุกแถวไว้ใช้งาน

### จัดกลุ่มข้อมูลด้วย groupby

`groupby` ใช้แบ่งข้อมูลเป็นกลุ่มตามคอลัมน์ที่กำหนด แล้วคำนวณสรุปแต่ละกลุ่ม
(คล้ายกับ Pivot Table ใน Excel)

```python
result = df.groupby("major")["math_score"].mean()
print(result)
```

ผลลัพธ์จากการ groupby มักจะอยากเก็บไว้ใช้งานต่อในรูปแบบที่ตรวจสอบง่าย ใช้ `.round()`
ปัดทศนิยม และ `.to_dict()` แปลงเป็น dictionary ได้

```python
result = df.groupby("major")["math_score"].mean().round(2).to_dict()
print(result)    # {'Computer Science': 72.86, 'Data Science': 84.0, 'Statistics': 73.5}
```

นับจำนวนสมาชิกในแต่ละกลุ่มด้วย `.size()`

```python
counts = df.groupby("major").size().to_dict()
print(counts)
```

### เปลี่ยนชื่อคอลัมน์ด้วย rename

```python
df_renamed = df.rename(columns={"math_score": "mathematics_score"})
print(list(df_renamed.columns))
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")
st.info("💡 บทนี้ใช้ pandas ซึ่งโหลดช้ากว่าโค้ดทั่วไปเล็กน้อย ถ้ารันแล้วรอสักครู่ถือว่าปกติ")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (ตรวจสอบค่าขาดหาย)")
st.markdown("""
ตัวอย่าง:
```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(df["math_score"].isnull().sum())
print(df["python_score"].isnull().sum())
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
1
2
```
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex1_copy_isnull",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="1\n2",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด math_score ขาดหาย 1 ค่า python_score ขาดหาย 2 ค่า",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (dropna)")
st.markdown("""
ตัวอย่าง:
```python
import pandas as pd

df = pd.read_csv("data/students.csv")
df_clean = df.dropna()
print(len(df_clean))
```

ทำตามตัวอย่างนี้เป๊ะ ๆ
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex2_copy_dropna",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        'df_clean = df.dropna()\n'
        'print(len(df_clean))\n'
    ),
    check_type="exact",
    expected_output="17",
    hint="โค้ดนี้พร้อมใช้แล้ว ลองกดรันตามที่ให้มาดูผลลัพธ์ — จาก 20 แถว มี 3 แถวที่มีค่าขาดหายอย่างน้อย 1 คอลัมน์",
    timeout=15,
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — fillna ด้วยค่าเฉลี่ย")
st.markdown("""
เติมโค้ดให้เติมค่าขาดหายในคอลัมน์ `math_score` ด้วยค่าเฉลี่ยของคอลัมน์นั้น
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex3_fill_fillna",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        'mean_score = df["math_score"].mean()\n'
        '# TODO: เติมค่าขาดหายในคอลัมน์ math_score ด้วย mean_score\n'
        'df["math_score"] = \n'
        'print(df["math_score"].isnull().sum())\n'
    ),
    check_type="exact",
    expected_output="0",
    hint='ใช้ df["math_score"].fillna(mean_score) แล้วเก็บผลลัพธ์กลับไปที่ df["math_score"] เดิม',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — groupby คำนวณค่าเฉลี่ย")
st.markdown("""
เติมโค้ดให้คำนวณค่าเฉลี่ย `math_score` แยกตามสาขา (`major`) ปัดทศนิยม 2 ตำแหน่ง
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex4_fill_groupbymean",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: groupby ตาม major คำนวณค่าเฉลี่ย math_score ปัดทศนิยม 2 ตำแหน่ง แปลงเป็น dict\n'
        'result = \n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="{'Computer Science': 72.86, 'Data Science': 84.0, 'Statistics': 73.5}",
    hint='ใช้ df.groupby("major")["math_score"].mean().round(2).to_dict() ต่อกันตามลำดับที่เรียนไปในเนื้อหา',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — groupby นับจำนวนสมาชิก")
st.markdown("""
เติมโค้ดให้นับจำนวนนักศึกษาในแต่ละสาขาด้วย groupby (ไม่ใช้ `value_counts()` ที่เคยเรียน
ในบทก่อน ลองใช้ `.size()` ของ groupby แทน)
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex5_fill_groupbysize",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: groupby ตาม major นับจำนวนสมาชิกแต่ละกลุ่ม แปลงเป็น dict\n'
        'counts = \n'
        'print(counts)\n'
    ),
    check_type="exact",
    expected_output="{'Computer Science': 7, 'Data Science': 6, 'Statistics': 7}",
    hint='ใช้ df.groupby("major").size().to_dict()',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — เปลี่ยนชื่อคอลัมน์")
st.markdown("""
เติมโค้ดให้เปลี่ยนชื่อคอลัมน์ `attendance_rate` เป็น `attendance_percent`
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex6_fill_rename",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: เปลี่ยนชื่อคอลัมน์ attendance_rate เป็น attendance_percent\n'
        'df_renamed = \n'
        'print(list(df_renamed.columns))\n'
    ),
    check_type="exact",
    expected_output="['student_id', 'name', 'major', 'year', 'math_score', 'python_score', 'attendance_percent']",
    hint='ใช้ df.rename(columns={"attendance_rate": "attendance_percent"}) ตามรูปแบบที่เรียนไปในเนื้อหา',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — groupby หลายคอลัมน์ผสมกับ filter")
st.markdown("""
เติมโค้ดให้คำนวณค่าเฉลี่ย `attendance_rate` แยกตามชั้นปี (`year`) ปัดทศนิยม 2 ตำแหน่ง
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex7_fill_groupbyyear",
    title="", instructions="",
    starter_code=(
        'import pandas as pd\n'
        '\n'
        'df = pd.read_csv("data/students.csv")\n'
        '# TODO: groupby ตาม year คำนวณค่าเฉลี่ย attendance_rate ปัดทศนิยม 2 ตำแหน่ง แปลงเป็น dict\n'
        'result = \n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="{1: 73.4, 2: 89.0, 3: 93.2, 4: 75.25}",
    hint='ใช้ df.groupby("year")["attendance_rate"].mean().round(2).to_dict() ทำเหมือนข้อ 4 '
         'แต่เปลี่ยนคอลัมน์ที่ groupby และคอลัมน์ที่คำนวณ',
    timeout=15,
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — ทำความสะอาดข้อมูลครบวงจร")
st.markdown("""
เขียนฟังก์ชันชื่อ `clean_and_count(csv_path)` รับ path ของไฟล์ CSV แล้ว:
1. เติมค่าขาดหายในคอลัมน์ `math_score` และ `python_score` ด้วยค่าเฉลี่ยของคอลัมน์นั้น ๆ
2. return จำนวนค่าขาดหายทั้งหมดที่เหลืออยู่ในข้อมูล (ควรเป็น 0 ถ้าทำถูกต้อง)
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex8_write_cleancount",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef clean_and_count(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="clean_and_count",
    test_cases=[
        {"args": ("data/students.csv",), "expected": 0, "label": "หลังทำความสะอาดต้องไม่มีค่าขาดหาย"},
    ],
    hint='เติมค่าขาดหายทั้งสองคอลัมน์ด้วย .fillna() ของค่าเฉลี่ยตัวเอง (เหมือนข้อ 3 แต่ทำ 2 คอลัมน์) '
         'แล้ว return df.isnull().sum().sum() — ตัว .sum() ตัวแรกรวมตามคอลัมน์ ตัวที่สองรวมทุกคอลัมน์เข้าด้วยกัน',
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — หาสาขาที่มีคะแนนเฉลี่ยสูงสุด")
st.markdown("""
เขียนฟังก์ชันชื่อ `best_major(csv_path)` รับ path ของไฟล์ CSV แล้ว return ชื่อสาขา
ที่มีคะแนนเฉลี่ย `math_score` สูงสุด เป็น string
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex9_write_bestmajor",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef best_major(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="best_major",
    test_cases=[
        {"args": ("data/students.csv",), "expected": "Data Science", "label": "หาสาขาคะแนนเฉลี่ยสูงสุด"},
    ],
    hint="ใช้ groupby('major')['math_score'].mean() ก่อน ผลลัพธ์ที่ได้เป็น Series ที่มีชื่อสาขา "
         "เป็น index — ลองใช้ .idxmax() ดึงชื่อ index ที่มีค่าสูงสุดออกมาตรง ๆ (ฟังก์ชันนี้คืนชื่อ "
         "ของแถวที่ค่ามากที่สุด ต่างจาก .max() ที่คืนค่าตัวเลขเฉย ๆ)",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — เปรียบเทียบก่อน-หลัง dropna")
st.markdown("""
เขียนฟังก์ชันชื่อ `rows_removed_by_dropna(csv_path)` รับ path ของไฟล์ CSV แล้ว
return จำนวนแถวที่ถูกลบออกไปถ้าใช้ `dropna()` (ผลต่างระหว่างจำนวนแถวเดิมกับจำนวนแถว
หลัง dropna)
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex10_write_rowsremoved",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef rows_removed_by_dropna(csv_path):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="rows_removed_by_dropna",
    test_cases=[
        {"args": ("data/students.csv",), "expected": 3, "label": "จำนวนแถวที่ถูกลบ"},
    ],
    hint="หาจำนวนแถวทั้งหมดด้วย len(df) ก่อน dropna แล้วหาจำนวนแถวหลัง dropna ด้วย len(df.dropna()) "
         "สุดท้าย return ผลต่างระหว่างสองค่านี้",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — สรุปข้อมูลแบบกำหนดคอลัมน์ได้")
st.markdown("""
เขียนฟังก์ชันชื่อ `group_summary(csv_path, group_col, value_col)` รับ path ของไฟล์ CSV,
ชื่อคอลัมน์ที่จะใช้จัดกลุ่ม (`group_col`), และชื่อคอลัมน์ที่จะคำนวณค่าเฉลี่ย (`value_col`)
แล้ว return dictionary ของค่าเฉลี่ยแต่ละกลุ่ม ปัดทศนิยม 2 ตำแหน่ง

ฟังก์ชันนี้ทำงานคล้ายข้อ 4 และ 7 ที่ทำมา แต่ทำให้ใช้งานได้ทั่วไปกับคอลัมน์ไหนก็ได้
ไม่ต้องเขียนใหม่ทุกครั้ง — เป็นแนวคิดสำคัญของการเขียนฟังก์ชันให้ใช้ซ้ำได้
""")

render_exercise(
    lesson_id="lesson11", exercise_id="ex11_write_groupsummary",
    title="", instructions="",
    starter_code="import pandas as pd\n\ndef group_summary(csv_path, group_col, value_col):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="group_summary",
    test_cases=[
        {"args": ("data/students.csv", "major", "math_score"),
         "expected": {"Computer Science": 72.86, "Data Science": 84.0, "Statistics": 73.5},
         "label": "groupby major, ค่าเฉลี่ย math_score"},
        {"args": ("data/students.csv", "year", "attendance_rate"),
         "expected": {"1": 73.4, "2": 89.0, "3": 93.2, "4": 75.25},
         "label": "groupby year, ค่าเฉลี่ย attendance_rate"},
    ],
    hint="ใช้ group_col และ value_col แทนชื่อคอลัมน์ตรง ๆ ในโค้ด groupby ที่เคยเขียนในข้อ 4/7 "
         "(df.groupby(group_col)[value_col].mean().round(2).to_dict()) — ข้อนี้พิสูจน์ว่าฟังก์ชัน "
         "ที่ดีไม่ต้องเขียนค่าคงที่ตายตัว แต่รับ parameter มาแทนได้ "
         "(หมายเหตุ: เมื่อ key ของ dict เป็นตัวเลข เช่นกรณี groupby('year') ระบบตรวจจะแปลงเป็น "
         "string key ให้เสมอ เป็นพฤติกรรมปกติเมื่อส่งข้อมูลผ่าน JSON ไม่ต้องกังวลเรื่องนี้)",
    timeout=15,
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/10_บทที่10_อ่านข้อมูล.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/intro.py", label="🏠 กลับหน้าแรก")
