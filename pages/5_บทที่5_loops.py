"""บทที่ 5: Loops"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson05", total_exercises=11)

st.title("บทที่ 5: Loops (การวนซ้ำ)")

st.markdown("""
### for loop — วนซ้ำตามจำนวนที่กำหนด

`for` ใช้วนซ้ำไปทีละสมาชิกใน list, string, หรือช่วงตัวเลข (`range`)

```python
fruits = ["แอปเปิ้ล", "กล้วย", "ส้ม"]
for fruit in fruits:
    print(fruit)
```

ใช้ `range(n)` เพื่อวนซ้ำตามจำนวนครั้งที่กำหนด (เริ่มที่ 0 ถึง n-1)

```python
for i in range(5):
    print(i)   # พิมพ์ 0, 1, 2, 3, 4
```

`range(start, stop)` กำหนดจุดเริ่มต้นได้ และ `range(start, stop, step)` กำหนดช่วงกระโดดได้

```python
for i in range(2, 10, 2):
    print(i)   # พิมพ์ 2, 4, 6, 8
```

### while loop — วนซ้ำตามเงื่อนไข

`while` วนซ้ำไปเรื่อย ๆ จนกว่าเงื่อนไขจะเป็นเท็จ — ต้องระวังอย่าให้วนไม่สิ้นสุด

```python
count = 0
while count < 5:
    print(count)
    count = count + 1   # ต้องอัปเดตตัวแปรไม่งั้นจะวนไม่หยุด
```

### break และ continue — ควบคุมการวนลูป

`break` หยุดลูปทันที ส่วน `continue` ข้ามไปรอบถัดไปโดยไม่ทำโค้ดที่เหลือในรอบนี้

```python
for i in range(10):
    if i == 5:
        break          # หยุดลูปทันทีที่ i เท่ากับ 5
    print(i)             # พิมพ์ 0, 1, 2, 3, 4

for i in range(10):
    if i % 2 == 0:
        continue        # ข้ามเลขคู่ ไม่พิมพ์
    print(i)             # พิมพ์ 1, 3, 5, 7, 9
```

### Nested loop — ลูปซ้อนลูป

ใช้เมื่อต้องวนซ้ำสองมิติ เช่น ตาราง หรือ 2D list ที่เรียนไปในบทก่อน

```python
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (for loop พื้นฐาน)")
st.markdown("""
ตัวอย่าง:
```python
for i in range(5):
    print(i)
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
0
1
2
3
4
```
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex1_copy_forloop",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="0\n1\n2\n3\n4",
    hint="ดูตัวอย่างด้านบน range(5) จะวนตั้งแต่ 0 ถึง 4 (ไม่รวม 5)",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (while loop)")
st.markdown("""
ตัวอย่าง:
```python
count = 0
while count < 3:
    print(f"รอบที่ {count}")
    count = count + 1
```

ทำตามตัวอย่าง แต่เปลี่ยนเงื่อนไขเป็น **count < 5** แทน
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex2_copy_whileloop",
    title="", instructions="",
    starter_code=(
        'count = 0\n'
        'while count < 3:\n'
        '    print(f"รอบที่ {count}")\n'
        '    count = count + 1\n'
    ),
    check_type="exact",
    expected_output="รอบที่ 0\nรอบที่ 1\nรอบที่ 2\nรอบที่ 3\nรอบที่ 4",
    hint="แก้แค่ตัวเลขในเงื่อนไข while ไม่ต้องแก้ส่วนอื่น",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — วนลูปทาย list")
st.markdown("""
เติมโค้ดให้วนลูปพิมพ์สมาชิกทุกตัวใน list ของสี
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex3_fill_listloop",
    title="", instructions="",
    starter_code=(
        'colors = ["แดง", "เขียว", "น้ำเงิน"]\n'
        '# TODO: วนลูปพิมพ์สมาชิกทุกตัวใน colors\n'
        '\n'
        '\n'
    ),
    check_type="exact",
    expected_output="แดง\nเขียว\nน้ำเงิน",
    hint="ใช้ for ตัวแปร in colors: แล้ว print ตัวแปรนั้นในบรรทัดถัดไป (ต้อง indent ให้ตรงกัน)",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — ผลรวมด้วย for loop")
st.markdown("""
เติมโค้ดให้คำนวณผลรวมของเลข 1 ถึง 10 ด้วยการวนลูป
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex4_fill_sumloop",
    title="", instructions="",
    starter_code=(
        'total = 0\n'
        '# TODO: วนลูปด้วย range เพื่อบวกเลข 1 ถึง 10 เข้า total\n'
        'for i in range(1, 11):\n'
        '    \n'
        'print(total)\n'
    ),
    check_type="exact",
    expected_output="55",
    hint="ในลูปต้องอัปเดต total โดยเอาค่าเดิมบวกกับ i แล้วเก็บกลับที่ total เหมือนที่เคยทำกับการอัปเดตตัวแปรในบทก่อน",
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — break ออกจากลูป")
st.markdown("""
เติมโค้ดให้หยุดลูปทันทีที่เจอเลข 7 (ไม่พิมพ์เลข 7 และเลขถัดไป)
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex5_fill_break",
    title="", instructions="",
    starter_code=(
        'for i in range(10):\n'
        '    if i == 7:\n'
        '        # TODO: หยุดลูปทันที\n'
        '        \n'
        '    print(i)\n'
    ),
    check_type="exact",
    expected_output="0\n1\n2\n3\n4\n5\n6",
    hint="ใช้คำสั่งที่เรียนไปในเนื้อหาสำหรับหยุดลูปทันที (คำสั่งเดียว ไม่มี argument)",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — continue ข้ามรอบ")
st.markdown("""
เติมโค้ดให้ข้ามการพิมพ์เลขที่หารด้วย 3 ลงตัว (ข้ามไปรอบถัดไปโดยไม่พิมพ์)
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex6_fill_continue",
    title="", instructions="",
    starter_code=(
        'for i in range(1, 10):\n'
        '    if i % 3 == 0:\n'
        '        # TODO: ข้ามไปรอบถัดไป\n'
        '        \n'
        '    print(i)\n'
    ),
    check_type="exact",
    expected_output="1\n2\n4\n5\n7\n8",
    hint="ใช้คำสั่งที่เรียนไปในเนื้อหาสำหรับข้ามไปรอบถัดไปของลูปโดยไม่ทำโค้ดที่เหลือในรอบนั้น",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — nested loop กับ 2D list")
st.markdown("""
มี 2D list (ตารางตัวเลข) เติมโค้ดให้วนลูปซ้อนลูปพิมพ์ค่าทุกตัวในตาราง โดยพิมพ์ค่าในแถวเดียวกัน
คั่นด้วยช่องว่าง แล้วขึ้นบรรทัดใหม่เมื่อจบแต่ละแถว
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex7_fill_nestedloop",
    title="", instructions="",
    starter_code=(
        'matrix = [[1, 2, 3], [4, 5, 6]]\n'
        'for row in matrix:\n'
        '    # TODO: วนลูปในเพื่อพิมพ์ทุกค่าในแถวนี้ คั่นด้วยช่องว่าง (ใช้ end=" ")\n'
        '    \n'
        '    print()\n'
    ),
    check_type="exact",
    expected_output="1 2 3 \n4 5 6 ",
    hint='วนลูปในไล่ทีละค่าใน row แล้ว print(value, end=" ") เพื่อพิมพ์ติดกันโดยไม่ขึ้นบรรทัดใหม่ '
         'จากนั้น print() เปล่าด้านนอกลูปในจะขึ้นบรรทัดใหม่ให้',
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — ตรวจสอบจำนวนเฉพาะ")
st.markdown("""
เขียนฟังก์ชันชื่อ `is_prime(n)` รับจำนวนเต็มบวก แล้ว return `True` ถ้าเป็นจำนวนเฉพาะ
(prime number — หารด้วย 1 และตัวเองเท่านั้น) และ `False` ถ้าไม่ใช่

**หมายเหตุ:** เลข 1 ไม่ถือเป็นจำนวนเฉพาะ
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex8_write_isprime",
    title="", instructions="",
    starter_code="def is_prime(n):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="is_prime",
    test_cases=[
        {"args": (7,), "expected": True, "label": "7 เป็นจำนวนเฉพาะ"},
        {"args": (10,), "expected": False, "label": "10 ไม่เป็นจำนวนเฉพาะ"},
        {"args": (2,), "expected": True, "label": "2 เป็นจำนวนเฉพาะที่เล็กที่สุด"},
        {"args": (1,), "expected": False, "label": "1 ไม่ถือเป็นจำนวนเฉพาะ"},
        {"args": (17,), "expected": True, "label": "17 เป็นจำนวนเฉพาะ"},
    ],
    hint="ลองหารค่า n ด้วยเลขทุกตัวตั้งแต่ 2 ถึง n-1 ถ้ามีตัวใดหารลงตัว (เศษเป็น 0) แสดงว่าไม่ใช่จำนวนเฉพาะ "
         "อย่าลืมจัดการกรณี n=1 แยกเป็นพิเศษด้วย เพราะลูปแบบนี้อาจจะให้ผลผิดถ้า n น้อยมาก",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — กลับลำดับ List")
st.markdown("""
เขียนฟังก์ชันชื่อ `reverse_list(items)` รับ list แล้ว return list ใหม่ที่มีสมาชิก
เรียงลำดับกลับด้านจากเดิม (ห้ามใช้ `.reverse()` หรือ `list[::-1]` หรือ `reversed()` สำเร็จรูป
ให้ลองวนลูปสร้าง list ใหม่เอง)
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex9_write_reverselist",
    title="", instructions="",
    starter_code="def reverse_list(items):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="reverse_list",
    test_cases=[
        {"args": ([1, 2, 3],), "expected": [3, 2, 1], "label": "list 3 ตัว"},
        {"args": (["a", "b", "c", "d"],), "expected": ["d", "c", "b", "a"], "label": "list string 4 ตัว"},
        {"args": ([5],), "expected": [5], "label": "list ตัวเดียว"},
        {"args": ([],), "expected": [], "label": "list ว่าง"},
    ],
    hint="สร้าง list ว่างไว้เก็บผลลัพธ์ วนลูปไล่สมาชิกของ items จากตัวสุดท้ายมาตัวแรก "
         "(ลองใช้ range กับ index ที่ไล่ค่าลดลง หรือวิธีอื่นที่ทำให้ได้ลำดับย้อนกลับ) "
         "แล้ว append แต่ละตัวเข้า list ผลลัพธ์ตามลำดับที่ไล่",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — หาตัวหารร่วมมาก (GCD)")
st.markdown("""
เขียนฟังก์ชันชื่อ `find_gcd(a, b)` รับจำนวนเต็มบวก 2 ตัว แล้ว return ตัวหารร่วมมาก (GCD)
ของทั้งสองตัว

**แนวทาง:** ลองหาตัวเลขที่มากที่สุดที่หารทั้ง a และ b ลงตัวพร้อมกัน
(วิธีง่ายที่สุดคือไล่ตรวจตัวเลขตั้งแต่ค่าน้อยกว่าระหว่าง a, b ลงมาเรื่อย ๆ
จนเจอตัวแรกที่หารทั้งคู่ลงตัว)
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex10_write_gcd",
    title="", instructions="",
    starter_code="def find_gcd(a, b):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="find_gcd",
    test_cases=[
        {"args": (12, 18), "expected": 6, "label": "GCD(12, 18) = 6"},
        {"args": (7, 13), "expected": 1, "label": "GCD ของจำนวนเฉพาะที่ต่างกัน = 1"},
        {"args": (8, 8), "expected": 8, "label": "GCD ของเลขเท่ากัน"},
        {"args": (100, 75), "expected": 25, "label": "GCD(100, 75) = 25"},
    ],
    hint="หาค่าน้อยกว่าระหว่าง a กับ b ก่อน แล้วไล่ตรวจตัวเลขจากค่านั้นลงมาถึง 1 "
         "ตัวเลขแรกที่หารทั้ง a และ b ลงตัวพร้อมกัน (ใช้ % เช็คเศษเป็น 0 ทั้งสองตัว) คือ GCD ที่ต้องการ",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — สร้างตารางสูตรคูณ")
st.markdown("""
เขียนฟังก์ชันชื่อ `multiplication_table(n)` รับจำนวนเต็ม `n` แล้ว return list ของผลคูณ
`n × 1` ถึง `n × 10` ตามลำดับ (เป็น list ของตัวเลข 10 ตัว)

ตัวอย่าง: `multiplication_table(3)` ควร return `[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]`
""")

render_exercise(
    lesson_id="lesson05", exercise_id="ex11_write_multtable",
    title="", instructions="",
    starter_code="def multiplication_table(n):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="multiplication_table",
    test_cases=[
        {"args": (3,), "expected": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30], "label": "สูตรคูณแม่ 3"},
        {"args": (1,), "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "label": "สูตรคูณแม่ 1"},
        {"args": (5,), "expected": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50], "label": "สูตรคูณแม่ 5"},
    ],
    hint="สร้าง list ว่างไว้เก็บผลลัพธ์ วนลูปด้วย range ตั้งแต่ 1 ถึง 10 (รวม 10 ด้วย ระวัง range ไม่รวมค่า stop) "
         "ในแต่ละรอบคำนวณ n คูณกับเลขในรอบนั้น แล้ว append เข้า list ผลลัพธ์",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/4_บทที่4_conditions.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/6_บทที่6_functions.py", label="ไปบทต่อไป: Functions ➡️")
