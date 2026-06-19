"""บทที่ 8: ฟังก์ชันสำเร็จรูปและ Library"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson08", total_exercises=11)

st.title("บทที่ 8: ฟังก์ชันสำเร็จรูปและ Library")

st.markdown("""
### Built-in functions ที่ใช้บ่อย

ไพธอนมีฟังก์ชันสำเร็จรูปติดมาให้ใช้ได้เลยโดยไม่ต้อง import อะไรเพิ่ม ที่ใช้บ่อยมาก
ในงาน data science มีดังนี้

```python
numbers = [5, 2, 8, 1, 9]

print(len(numbers))      # 5   — จำนวนสมาชิก
print(sum(numbers))      # 25  — ผลรวม
print(max(numbers))      # 9   — ค่ามากสุด
print(min(numbers))      # 1   — ค่าน้อยสุด
print(sorted(numbers))   # [1, 2, 5, 8, 9] — เรียงลำดับ (list ใหม่ ไม่แก้ของเดิม)
print(sorted(numbers, reverse=True))  # [9, 8, 5, 2, 1] — เรียงจากมากไปน้อย
```

### map และ filter — ประมวลผล list แบบกระชับ

`map(function, list)` ใช้ฟังก์ชันกับสมาชิกทุกตัวใน list แล้วคืนค่าผลลัพธ์ทั้งหมด

```python
numbers = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)   # [2, 4, 6, 8]
```

`filter(function, list)` คัดเฉพาะสมาชิกที่ฟังก์ชันคืนค่า True

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)   # [2, 4, 6]
```

`lambda` คือการสร้างฟังก์ชันแบบสั้น ๆ ไม่ต้องตั้งชื่อ เหมาะกับงานง่าย ๆ บรรทัดเดียว
เทียบเท่ากับการเขียน `def` ปกติแต่กระชับกว่า

```python
square = lambda x: x ** 2     # เทียบเท่ากับ def square(x): return x ** 2
print(square(5))               # 25
```

### การ import module

โมดูลคือไฟล์ที่รวมฟังก์ชันสำเร็จรูปไว้ใช้งาน ไพธอนมีโมดูลมาตรฐานติดมาให้ใช้ได้เลย

```python
import math

print(math.sqrt(16))      # 4.0  — รากที่สอง
print(math.pi)              # 3.14159...
print(math.ceil(4.3))       # 5    — ปัดขึ้น
print(math.floor(4.7))      # 4    — ปัดลง

import random
print(random.randint(1, 10))   # สุ่มเลขจำนวนเต็มระหว่าง 1-10
```

import เฉพาะบางส่วนจากโมดูลได้ด้วย `from ... import ...`

```python
from math import sqrt, pi

print(sqrt(25))    # 5.0  — ไม่ต้องเขียน math.sqrt() แล้ว
print(pi)
```

### เตรียมพร้อมก่อนเข้าสู่ NumPy และการทำงานกับข้อมูลจริง

บทถัดไปจะเรียนรู้ NumPy ซึ่งเป็น library สำหรับคำนวณเชิงตัวเลขและ matrix ที่ทรงพลังกว่า
list ธรรมดามาก และเป็นพื้นฐานสำคัญของ pandas ที่จะใช้ทำงานกับข้อมูลจริงในบทหลัง ๆ
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (built-in functions)")
st.markdown("""
ตัวอย่าง:
```python
numbers = [3, 7, 1, 9, 4]
print(max(numbers))
print(min(numbers))
print(sum(numbers))
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
9
1
24
```
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex1_copy_builtins",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="9\n1\n24",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด ลองคำนวณผลรวมของ 3+7+1+9+4 ดูว่าตรงกับที่คาดไหม",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (math module)")
st.markdown("""
ตัวอย่าง:
```python
import math

print(math.sqrt(36))
print(math.ceil(7.2))
```

ทำตามตัวอย่าง แต่เปลี่ยนเป็น `math.sqrt(64)` และ `math.floor(7.8)` แทน
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex2_copy_mathmodule",
    title="", instructions="",
    starter_code=(
        'import math\n'
        '\n'
        'print(math.sqrt(36))\n'
        'print(math.ceil(7.2))\n'
    ),
    check_type="exact",
    expected_output="8.0\n7",
    hint="แก้แค่ตัวเลขในวงเล็บ และเปลี่ยนชื่อฟังก์ชัน ceil เป็น floor (ปัดลงแทนปัดขึ้น)",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — sorted แบบ reverse")
st.markdown("""
เติมโค้ดให้เรียงลำดับ list จากมากไปน้อย
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex3_fill_sorted",
    title="", instructions="",
    starter_code=(
        'numbers = [5, 2, 8, 1, 9]\n'
        '# TODO: เรียงลำดับจากมากไปน้อย เก็บในตัวแปร result\n'
        'result = \n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="[9, 8, 5, 2, 1]",
    hint="ใช้ sorted() พร้อมกับ parameter ที่เรียนไปในเนื้อหาสำหรับเรียงจากมากไปน้อย",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — ใช้ map กับ lambda")
st.markdown("""
เติมโค้ดให้ใช้ `map` กับ `lambda` แปลงทุกตัวเลขใน list เป็นค่ายกกำลังสาม
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex4_fill_map",
    title="", instructions="",
    starter_code=(
        'numbers = [1, 2, 3, 4]\n'
        '# TODO: ใช้ map และ lambda แปลงทุกตัวเลขเป็นค่ายกกำลังสาม เก็บในตัวแปร cubed\n'
        'cubed = \n'
        'print(cubed)\n'
    ),
    check_type="exact",
    expected_output="[1, 8, 27, 64]",
    hint="ใช้ list(map(lambda x: ..., numbers)) โดยเขียนสูตรยกกำลังสาม (x ** 3) แทนจุดสามจุด "
         "อย่าลืมครอบด้วย list() เพื่อแปลงผลลัพธ์ของ map ให้เป็น list ที่ print ออกมาดูได้",
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — ใช้ filter กับ lambda")
st.markdown("""
เติมโค้ดให้ใช้ `filter` คัดเฉพาะตัวเลขที่มากกว่า 10 ออกมา
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex5_fill_filter",
    title="", instructions="",
    starter_code=(
        'numbers = [5, 15, 8, 20, 3, 12]\n'
        '# TODO: ใช้ filter และ lambda คัดเฉพาะตัวเลขที่มากกว่า 10 เก็บในตัวแปร big_numbers\n'
        'big_numbers = \n'
        'print(big_numbers)\n'
    ),
    check_type="exact",
    expected_output="[15, 20, 12]",
    hint="ใช้ list(filter(lambda x: ..., numbers)) โดยเขียนเงื่อนไข x > 10 แทนจุดสามจุด",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — import แบบเฉพาะส่วน")
st.markdown("""
เติมโค้ดให้ import เฉพาะ `randint` จาก `random` module (ไม่ต้อง import ทั้งโมดูล)
แล้วใช้แบบไม่ต้องมีคำว่า `random.` นำหน้า
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex6_fill_fromimport",
    title="", instructions="",
    starter_code=(
        '# TODO: import เฉพาะ randint จาก random module\n'
        '\n'
        '\n'
        'number = randint(5, 5)   # ใส่ค่าต่ำสุด=สูงสุด=5 เพื่อให้ผลลัพธ์ตรวจสอบได้แน่นอน\n'
        'print(number)\n'
    ),
    check_type="exact",
    expected_output="5",
    hint="ใช้รูปแบบ from random import randint แล้วเรียกใช้ randint(...) ตรง ๆ ไม่ต้องมี random. นำหน้า",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — รวม built-in หลายตัว")
st.markdown("""
เติมโค้ดให้หาผลต่างระหว่างค่ามากสุดกับค่าน้อยสุดใน list (range ของข้อมูล)
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex7_fill_rangecalc",
    title="", instructions="",
    starter_code=(
        'scores = [65, 88, 72, 95, 58, 80]\n'
        '# TODO: คำนวณผลต่างระหว่างคะแนนมากสุดกับน้อยสุด เก็บในตัวแปร score_range\n'
        'score_range = \n'
        'print(score_range)\n'
    ),
    check_type="exact",
    expected_output="37",
    hint="ใช้ max(scores) ลบด้วย min(scores)",
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — คำนวณค่าเฉลี่ยด้วย built-in functions")
st.markdown("""
เขียนฟังก์ชันชื่อ `calculate_mean(numbers)` รับ list ของตัวเลข แล้ว return ค่าเฉลี่ย
ปัดทศนิยม 2 ตำแหน่ง (ใช้ built-in functions อย่าง `sum()` และ `len()` ผสมกัน
ไม่ต้องเขียนวนลูปเอง)
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex8_write_mean",
    title="", instructions="",
    starter_code="def calculate_mean(numbers):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="calculate_mean",
    test_cases=[
        {"args": ([1, 2, 3, 4, 5],), "expected": 3.0, "label": "ค่าเฉลี่ยปกติ"},
        {"args": ([10, 20, 30],), "expected": 20.0, "label": "ค่าเฉลี่ยลงตัว"},
        {"args": ([5, 7, 9],), "expected": 7.0, "label": "ค่าเฉลี่ยอีกชุด"},
        {"args": ([1, 2],), "expected": 1.5, "label": "ค่าเฉลี่ยมีทศนิยม"},
    ],
    hint="ใช้ sum(numbers) หารด้วย len(numbers) แล้วครอบด้วย round(..., 2)",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — กรองและแปลงข้อมูลด้วย map/filter")
st.markdown("""
เขียนฟังก์ชันชื่อ `process_scores(scores)` รับ list ของคะแนน แล้ว return list ใหม่
ที่มีเฉพาะคะแนนที่ผ่าน (>= 50) และคูณด้วย 1.1 (โบนัส 10%) ปัดทศนิยม 1 ตำแหน่งทุกค่า

ตัวอย่าง: `process_scores([45, 60, 80, 30])` ควร return `[66.0, 88.0]`
(45 และ 30 ไม่ผ่านถูกตัดออก, 60×1.1=66.0, 80×1.1=88.0)

**แนวทาง:** ลองใช้ `filter` คัดคะแนนที่ผ่านก่อน แล้วใช้ `map` คูณโบนัสทีหลัง
(หรือจะเขียนด้วยวิธีอื่นที่ได้ผลลัพธ์ถูกต้องก็ได้)
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex9_write_processscores",
    title="", instructions="",
    starter_code="def process_scores(scores):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="process_scores",
    test_cases=[
        {"args": ([45, 60, 80, 30],), "expected": [66.0, 88.0], "label": "ผสมผ่าน-ไม่ผ่าน"},
        {"args": ([60, 70, 80],), "expected": [66.0, 77.0, 88.0], "label": "ผ่านทุกตัว"},
        {"args": ([10, 20, 30],), "expected": [], "label": "ไม่ผ่านเลย"},
    ],
    hint="ใช้ filter(lambda x: x >= 50, scores) คัดคะแนนที่ผ่านก่อน ครอบด้วย list() "
         "จากนั้นใช้ map(lambda x: round(x * 1.1, 1), ผลลัพธ์ที่กรองแล้ว) ครอบด้วย list() อีกที",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — หาค่ามัธยฐาน (median)")
st.markdown("""
เขียนฟังก์ชันชื่อ `find_median(numbers)` รับ list ของตัวเลข แล้ว return ค่ามัธยฐาน
(median — ค่ากึ่งกลางเมื่อเรียงลำดับแล้ว)
- ถ้าจำนวนสมาชิกเป็นเลขคี่ → ค่ากึ่งกลางตรงตัว
- ถ้าจำนวนสมาชิกเป็นเลขคู่ → ค่าเฉลี่ยของสองค่ากลาง

ตัวอย่าง: `find_median([3, 1, 2])` ควร return `2` (เรียงแล้วคือ 1,2,3 ค่ากลางคือ 2)
`find_median([4, 1, 3, 2])` ควร return `2.5` (เรียงแล้วคือ 1,2,3,4 เฉลี่ยของ 2,3 คือ 2.5)
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex10_write_median",
    title="", instructions="",
    starter_code="def find_median(numbers):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="find_median",
    test_cases=[
        {"args": ([3, 1, 2],), "expected": 2, "label": "จำนวนคี่"},
        {"args": ([4, 1, 3, 2],), "expected": 2.5, "label": "จำนวนคู่"},
        {"args": ([5],), "expected": 5, "label": "สมาชิกตัวเดียว"},
        {"args": ([10, 20],), "expected": 15.0, "label": "สองตัว"},
    ],
    hint="ใช้ sorted() เรียงลำดับก่อนเสมอ แล้วใช้ len() เช็คว่าจำนวนสมาชิกเป็นคู่หรือคี่ด้วย % 2 "
         "ถ้าคี่ ตำแหน่งกลางคือ len(numbers) // 2 (หารปัดเศษทิ้ง) ถ้าคู่ ต้องเฉลี่ยสองตำแหน่งกลาง "
         "ลองคิดดูว่าตำแหน่งกลางทั้งสองของกรณีคู่คือ index เท่าไรเทียบกับ len()",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — สุ่มเลขและตรวจสอบช่วง")
st.markdown("""
เขียนฟังก์ชันชื่อ `is_in_range(value, min_val, max_val)` รับตัวเลข `value` และช่วง
`min_val`, `max_val` แล้ว return `True` ถ้า `value` อยู่ในช่วงนั้น (รวมขอบทั้งสองด้าน)
และ return `False` ถ้าไม่อยู่ในช่วง — ใช้ความรู้เรื่อง comparison operator จากบทก่อน
ผสมกับการเขียนฟังก์ชันที่กระชับ
""")

render_exercise(
    lesson_id="lesson08", exercise_id="ex11_write_inrange",
    title="", instructions="",
    starter_code="def is_in_range(value, min_val, max_val):\n    # เขียนโค้ดของคุณที่นี่ (ลองใช้ chained comparison ที่เรียนไปในบทก่อน)\n    pass\n",
    check_type="function",
    function_name="is_in_range",
    test_cases=[
        {"args": (5, 1, 10), "expected": True, "label": "อยู่ในช่วง"},
        {"args": (15, 1, 10), "expected": False, "label": "เกินขอบบน"},
        {"args": (1, 1, 10), "expected": True, "label": "ขอบเขตพอดี (ล่าง)"},
        {"args": (10, 1, 10), "expected": True, "label": "ขอบเขตพอดี (บน)"},
        {"args": (-5, 1, 10), "expected": False, "label": "ต่ำกว่าขอบล่าง"},
    ],
    hint="ใช้ chained comparison แบบ min_val <= value <= max_val แล้ว return ผลลัพธ์ตรง ๆ ได้เลย "
         "เพราะการเปรียบเทียบให้ผลเป็น True/False อยู่แล้ว",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/7_บทที่7_error_handling.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/9_บทที่9_numpy.py", label="ไปบทต่อไป: NumPy และ Linear Algebra ➡️")
