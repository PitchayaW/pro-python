"""บทที่ 3: Data Structure"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 3: Data Structure")

st.markdown("""
### List — เก็บข้อมูลหลายค่า แก้ไขได้

List ใช้เก็บข้อมูลหลายค่าเรียงตามลำดับ เข้าถึงสมาชิกได้ผ่าน index (เริ่มที่ 0)

```python
fruits = ["แอปเปิ้ล", "กล้วย", "ส้ม"]
print(fruits[0])        # แอปเปิ้ล
print(len(fruits))      # 3 (จำนวนสมาชิก)
fruits.append("มะม่วง")  # เพิ่มสมาชิกใหม่ต่อท้าย
print(fruits)            # ['แอปเปิ้ล', 'กล้วย', 'ส้ม', 'มะม่วง']
```

### Tuple — เหมือน list แต่แก้ไขไม่ได้

```python
coordinate = (13.7563, 100.5018)   # ละติจูด, ลองจิจูด
print(coordinate[0])
```

### Dictionary — เก็บข้อมูลแบบ key-value

```python
student = {"name": "สมชาย", "age": 20, "major": "Computer Science"}
print(student["name"])      # สมชาย
student["gpa"] = 3.5         # เพิ่ม key ใหม่
```

### Set — เก็บข้อมูลไม่ซ้ำ ไม่เรียงลำดับ

```python
unique_numbers = {1, 2, 2, 3, 3, 3}
print(unique_numbers)   # {1, 2, 3} — ตัวซ้ำถูกตัดออกอัตโนมัติ
```

### 2D List (Multidimensional List) — list ซ้อน list

บางครั้งข้อมูลมีลักษณะเป็น "ตาราง" (แถวและคอลัมน์) เช่น ตารางคะแนน, รูปภาพ, หรือ matrix
ในไพธอนเก็บข้อมูลแบบนี้ได้ด้วย **list ที่สมาชิกแต่ละตัวเป็น list อีกที** (list ซ้อน list)

```python
# ตารางคะแนนสอบของนักศึกษา 3 คน 2 วิชา (แถว = นักศึกษา, คอลัมน์ = วิชา)
scores = [
    [85, 90],   # นักศึกษาคนที่ 0
    [70, 75],   # นักศึกษาคนที่ 1
    [95, 88],   # นักศึกษาคนที่ 2
]

print(scores[0])       # [85, 90]  — แถวที่ 0 ทั้งแถว
print(scores[0][1])    # 90        — แถว 0 คอลัมน์ 1
print(len(scores))     # 3         — จำนวนแถว
print(len(scores[0]))  # 2         — จำนวนคอลัมน์ในแถวนั้น
```

การวนลูปดูข้อมูลทุกตัวใน 2D list ใช้ลูปซ้อนลูป (nested loop) — ลูปนอกไล่ทีละแถว
ลูปในไล่ทีละคอลัมน์ภายในแถวนั้น

```python
for row in scores:
    for value in row:
        print(value, end=" ")
    print()   # ขึ้นบรรทัดใหม่หลังจบแต่ละแถว
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (List)")
st.markdown("""
ตัวอย่าง:
```python
colors = ["แดง", "เขียว", "น้ำเงิน"]
print(colors[0])
print(colors[2])
print(len(colors))
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
แดง
น้ำเงิน
3
```
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex1_copy_list",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="แดง\nน้ำเงิน\n3",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด สังเกตว่า index ตัวที่ 2 (colors[2]) หมายถึงสมาชิกตัวที่ 3 เพราะนับจาก 0",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (Dictionary)")
st.markdown("""
ตัวอย่าง:
```python
person = {"name": "สมหญิง", "age": 22}
print(person["name"])
print(person["age"])
```

ทำตามตัวอย่าง แต่เปลี่ยนเป็น `name` = **"วิชัย"** และ `age` = **30**
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex2_copy_dict",
    title="", instructions="",
    starter_code='person = {"name": "", "age": 0}\nprint(person["name"])\nprint(person["age"])\n',
    check_type="exact",
    expected_output="วิชัย\n30",
    hint="แก้แค่ค่าใน dictionary ตอนสร้าง (ฝั่งขวาของ : ) ไม่ต้องแก้ส่วน print",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — เพิ่มสมาชิกใน List")
st.markdown("""
มี list ของผลไม้อยู่แล้ว เติมโค้ดให้เพิ่ม "มะม่วง" เข้าไปต่อท้าย แล้วแสดง list ทั้งหมด
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex3_fill_append",
    title="", instructions="",
    starter_code=(
        'fruits = ["แอปเปิ้ล", "กล้วย", "ส้ม"]\n'
        '# TODO: เพิ่ม "มะม่วง" เข้าไปต่อท้าย list\n'
        '\n'
        'print(fruits)\n'
    ),
    check_type="exact",
    expected_output="['แอปเปิ้ล', 'กล้วย', 'ส้ม', 'มะม่วง']",
    hint="มี method ของ list ที่ใช้เพิ่มสมาชิกต่อท้าย ลองดูในเนื้อหาส่วน List ด้านบน (ใช้รูปแบบ list_name.xxx(ค่าที่จะเพิ่ม))",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — เข้าถึงค่าใน Dictionary")
st.markdown("""
เติมโค้ดให้ดึงค่า `"score"` จาก dictionary แล้วแสดงผลด้วย f-string
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex4_fill_dict_access",
    title="", instructions="",
    starter_code=(
        'student = {"name": "ดารณี", "score": 88}\n'
        '# TODO: ดึงค่า score จาก dict เก็บในตัวแปร score\n'
        'score = \n'
        'print(f"คะแนนของ {student[\\"name\\"]} คือ {score}")\n'
    ),
    check_type="exact",
    expected_output="คะแนนของ ดารณี คือ 88",
    hint='การดึงค่าจาก dictionary ใช้ชื่อ key ใส่ในวงเล็บเหลี่ยม เหมือนที่ print(student["name"]) ทำกับ key "name"',
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — slicing List")
st.markdown("""
เติมโค้ดให้ดึงสมาชิก 3 ตัวแรกของ list ด้วยวิธี slicing (`list[start:stop]`)
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex5_fill_slicing",
    title="", instructions="",
    starter_code=(
        'numbers = [10, 20, 30, 40, 50]\n'
        '# TODO: ดึง 3 ตัวแรกของ numbers ด้วย slicing เก็บในตัวแปร first_three\n'
        'first_three = \n'
        'print(first_three)\n'
    ),
    check_type="exact",
    expected_output="[10, 20, 30]",
    hint="slicing ใช้รูปแบบ list[start:stop] โดย stop คือตำแหน่งที่ "
         "ไม่รวม (exclusive) — ถ้าอยากได้ตั้งแต่ตัวแรก ไม่ต้องระบุ start ก็ได้",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — ตัดตัวซ้ำด้วย Set")
st.markdown("""
มี list ของเลขที่มีค่าซ้ำกันอยู่ เติมโค้ดให้แปลงเป็น set เพื่อตัดตัวซ้ำออก
แล้วแปลงกลับเป็น list ที่เรียงลำดับแล้ว (`sorted()`)
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex6_fill_set",
    title="", instructions="",
    starter_code=(
        'numbers = [3, 1, 2, 3, 1, 4, 2, 5]\n'
        '# TODO: แปลง numbers เป็น set เพื่อตัดตัวซ้ำ เก็บในตัวแปร unique_set\n'
        'unique_set = \n'
        'result = sorted(unique_set)\n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="[1, 2, 3, 4, 5]",
    hint="การแปลง list เป็น set ทำได้ด้วยฟังก์ชันที่ตรงกับชื่อชนิดข้อมูลนั้นเลย (เหมือนที่ int() แปลงเป็น int)",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — เข้าถึงค่าใน 2D List")
st.markdown("""
มีตารางคะแนน (2D list) เก็บคะแนนนักศึกษา 3 คน วิชาเดียว เติมโค้ดให้ดึงคะแนนของ
**นักศึกษาคนที่ 1** (index 1 ซึ่งคือคนที่สองในตาราง เพราะนับจาก 0) ออกมาแสดง
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex7_fill_2dlist",
    title="", instructions="",
    starter_code=(
        'scores = [\n'
        '    [85],\n'
        '    [70],\n'
        '    [95],\n'
        ']\n'
        '# TODO: ดึงคะแนนของนักศึกษาคนที่ index 1 เก็บในตัวแปร student1_score\n'
        '# หมายเหตุ: แต่ละแถวมีแค่ 1 ค่า ต้องดึงทั้งแถวมาก่อน แล้วดึงค่าแรกในแถวนั้น\n'
        'student1_score = \n'
        'print(student1_score)\n'
    ),
    check_type="exact",
    expected_output="70",
    hint="เข้าถึง 2D list ต้องระบุ index 2 ชั้น คือ [แถว][คอลัมน์] — แถวที่ 1 คอลัมน์ที่ 0 เขียนเป็น scores[1][0]",
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — หาผลรวมใน List")
st.markdown("""
เขียนฟังก์ชันชื่อ `sum_list(numbers)` รับ list ของตัวเลข แล้ว return ผลรวมของสมาชิกทั้งหมด
(ห้ามใช้ฟังก์ชัน `sum()` สำเร็จรูป ให้ลองเขียนด้วยการวนลูปหรือบวกค่าทีละตัวเอง)
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex8_write_sumlist",
    title="", instructions="",
    starter_code="def sum_list(numbers):\n    # เขียนโค้ดของคุณที่นี่ (ลองใช้ for loop บวกค่าสะสม)\n    pass\n",
    check_type="function",
    function_name="sum_list",
    test_cases=[
        {"args": ([1, 2, 3],), "expected": 6, "label": "list สั้น [1,2,3]"},
        {"args": ([10, 20, 30, 40],), "expected": 100, "label": "list 4 ตัว"},
        {"args": ([],), "expected": 0, "label": "list ว่าง"},
        {"args": ([5],), "expected": 5, "label": "list มีสมาชิกตัวเดียว"},
    ],
    hint="ตั้งตัวแปรสะสมผลรวมเริ่มที่ 0 ก่อนลูป แล้ววนลูปไล่ทีละสมาชิกใน list บวกเข้าตัวแปรสะสมไปทีละตัว "
         "สังเกตว่า list ว่างต้องได้ผลรวม 0 (ลูปไม่ทำงานเลยสักครั้ง ค่าเริ่มต้นจึงสำคัญ)",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — นับความถี่คำในรายการ")
st.markdown("""
เขียนฟังก์ชันชื่อ `count_items(items)` รับ list ของ string แล้ว return dictionary
ที่มี key เป็นชื่อสมาชิกแต่ละตัว และ value เป็นจำนวนครั้งที่ปรากฏใน list นั้น

ตัวอย่าง: `count_items(["a", "b", "a", "c", "b", "a"])`
ควร return `{"a": 3, "b": 2, "c": 1}`
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex9_write_countitems",
    title="", instructions="",
    starter_code="def count_items(items):\n    # เขียนโค้ดของคุณที่นี่ (ลองสร้าง dict ว่าง แล้ววนลูปนับ)\n    pass\n",
    check_type="function",
    function_name="count_items",
    test_cases=[
        {"args": (["a", "b", "a", "c", "b", "a"],), "expected": {"a": 3, "b": 2, "c": 1}, "label": "นับ a,b,c"},
        {"args": (["x", "x", "x"],), "expected": {"x": 3}, "label": "ซ้ำตัวเดียวทั้งหมด"},
        {"args": (["m", "n"],), "expected": {"m": 1, "n": 1}, "label": "ไม่ซ้ำเลย"},
    ],
    hint="สร้าง dictionary ว่างไว้เก็บผลลัพธ์ วนลูปไล่ทีละสมาชิกใน items แล้วตรวจสอบว่าค่านั้นมี key "
         "อยู่ใน dictionary แล้วหรือยัง (ใช้ in) — ถ้ามีแล้วให้เพิ่มค่าทีละ 1 ถ้ายังไม่มีให้สร้าง key ใหม่ค่าเริ่มต้นเป็น 1",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — หาค่าที่มากที่สุดและน้อยที่สุด")
st.markdown("""
เขียนฟังก์ชันชื่อ `min_max(numbers)` รับ list ของตัวเลข แล้ว return **tuple** ที่มี 2 ค่า
คือ (ค่าน้อยที่สุด, ค่ามากที่สุด) ตามลำดับ

(ห้ามใช้ฟังก์ชัน `min()`/`max()` สำเร็จรูป ให้ลองวนลูปเทียบค่าทีละตัวเอง)
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex10_write_minmax",
    title="", instructions="",
    starter_code="def min_max(numbers):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="min_max",
    test_cases=[
        {"args": ([3, 1, 4, 1, 5, 9, 2, 6],), "expected": [1, 9], "label": "list หลายค่า"},
        {"args": ([7],), "expected": [7, 7], "label": "list ตัวเดียว"},
        {"args": ([-5, 0, 5],), "expected": [-5, 5], "label": "มีค่าลบ"},
    ],
    hint="ตั้งตัวแปรเก็บค่าน้อยสุดและมากสุดเริ่มต้นด้วยสมาชิกตัวแรกของ list ก่อน "
         "แล้ววนลูปไล่ทุกตัว เทียบว่าค่านี้น้อยกว่าตัวที่เก็บไว้ไหม (ถ้าน้อยกว่าให้อัปเดต) "
         "และเทียบว่ามากกว่าตัวที่เก็บไว้ไหม (ถ้ามากกว่าให้อัปเดต) สุดท้าย return ทั้งสองค่าเป็น tuple",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — ผลรวมแต่ละแถวใน 2D List")
st.markdown("""
เขียนฟังก์ชันชื่อ `row_sums(matrix)` รับ 2D list (matrix) แล้ว return list ของผลรวม
แต่ละแถว

ตัวอย่าง: `row_sums([[1, 2, 3], [4, 5, 6]])` ควร return `[6, 15]`
(แถวแรก 1+2+3=6, แถวสอง 4+5+6=15)
""")

render_exercise(
    lesson_id="lesson03", exercise_id="ex11_write_rowsums",
    title="", instructions="",
    starter_code="def row_sums(matrix):\n    # เขียนโค้ดของคุณที่นี่ (ลองวนลูปนอกไล่ทีละแถว แล้ววนลูปในหรือใช้ sum() หาผลรวมของแถวนั้น)\n    pass\n",
    check_type="function",
    function_name="row_sums",
    test_cases=[
        {"args": ([[1, 2, 3], [4, 5, 6]],), "expected": [6, 15], "label": "matrix 2x3"},
        {"args": ([[10], [20], [30]],), "expected": [10, 20, 30], "label": "matrix 3x1"},
        {"args": ([[1, 1], [2, 2], [3, 3]],), "expected": [2, 4, 6], "label": "matrix 3x2"},
    ],
    hint="สร้าง list ว่างไว้เก็บผลลัพธ์ วนลูปนอกไล่ทีละแถวใน matrix สำหรับแต่ละแถวให้หาผลรวมของสมาชิกในแถวนั้น "
         "(จะใช้ sum() สำเร็จรูป หรือวนลูปในบวกเองก็ได้) แล้วเอาผลรวมที่ได้ไป append เข้า list ผลลัพธ์",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/2_บทที่2_ตัวแปร.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/4_บทที่4_conditions.py", label="ไปบทต่อไป: Conditions ➡️")
