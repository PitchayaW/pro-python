"""บทที่ 6: Functions"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson06", total_exercises=11)

st.title("บทที่ 6: Functions (ฟังก์ชัน)")

st.markdown("""
### การสร้างฟังก์ชันด้วย def

ฟังก์ชันคือกลุ่มคำสั่งที่ตั้งชื่อไว้ใช้ซ้ำได้ ช่วยลดความซ้ำซ้อนของโค้ดและจัดระเบียบโปรแกรม

```python
def greet():
    print("สวัสดีครับ")

greet()   # เรียกใช้ฟังก์ชัน จะพิมพ์ "สวัสดีครับ"
greet()   # เรียกซ้ำได้เรื่อย ๆ
```

### Parameter และ Argument

ฟังก์ชันรับค่าเข้ามาประมวลผลได้ผ่าน parameter (ตัวแปรที่อยู่ในวงเล็บตอนนิยามฟังก์ชัน)

```python
def greet(name):           # name คือ parameter
    print(f"สวัสดี {name}")

greet("สมชาย")              # "สมชาย" คือ argument ที่ส่งเข้าไป
greet("สมหญิง")
```

ฟังก์ชันรับได้หลาย parameter และตั้งค่า default ได้

```python
def introduce(name, age=20):    # age มีค่า default เป็น 20
    print(f"ชื่อ {name} อายุ {age} ปี")

introduce("สมชาย")              # ใช้ age default = 20
introduce("สมหญิง", 25)         # ระบุ age เป็น 25
```

### การ return ค่า

ฟังก์ชันส่งค่ากลับออกมาใช้งานต่อได้ด้วย `return` — ถ้าไม่มี `return` ฟังก์ชันจะคืนค่า `None`

```python
def add(a, b):
    return a + b

result = add(3, 5)   # result เก็บค่า 8
print(result)
```

### Scope ของตัวแปร (local vs global)

ตัวแปรที่สร้างภายในฟังก์ชัน (local variable) จะมองไม่เห็นจากภายนอกฟังก์ชัน

```python
def my_function():
    x = 10        # x เป็น local variable อยู่ในฟังก์ชันนี้เท่านั้น
    print(x)

my_function()      # พิมพ์ 10
print(x)            # Error! x ไม่มีอยู่นอกฟังก์ชัน
```

ตัวแปรที่สร้างนอกฟังก์ชัน (global variable) มองเห็นได้จากทุกที่ แต่การจะ "แก้ไข"
ค่าตัวแปร global จากภายในฟังก์ชันต้องใช้ `global` keyword (ไม่ค่อยแนะนำให้ใช้บ่อย
เพราะทำให้โค้ดติดตามยาก — ปกติแนะนำให้ใช้ parameter และ return แทน)
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (ฟังก์ชันพื้นฐาน)")
st.markdown("""
ตัวอย่าง:
```python
def say_hello():
    print("สวัสดีครับ")

say_hello()
say_hello()
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
สวัสดีครับ
สวัสดีครับ
```
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex1_copy_basicfunc",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="สวัสดีครับ\nสวัสดีครับ",
    hint="นิยามฟังก์ชันด้วย def ก่อน แล้วเรียกใช้ฟังก์ชันนั้น 2 ครั้งตามตัวอย่าง",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (ฟังก์ชันมี parameter)")
st.markdown("""
ตัวอย่าง:
```python
def greet(name):
    print(f"สวัสดี {name}")

greet("สมชาย")
```

ทำตามตัวอย่าง แต่เปลี่ยนเป็นเรียก `greet("วิภา")` แทน
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex2_copy_paramfunc",
    title="", instructions="",
    starter_code=(
        'def greet(name):\n'
        '    print(f"สวัสดี {name}")\n'
        '\n'
        'greet("สมชาย")\n'
    ),
    check_type="exact",
    expected_output="สวัสดี วิภา",
    hint="แก้แค่ argument ตอนเรียกใช้ฟังก์ชันบรรทัดสุดท้าย ไม่ต้องแก้ตัวฟังก์ชัน",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — ฟังก์ชัน return ค่า")
st.markdown("""
เติมโค้ดให้ฟังก์ชัน `square` คำนวณและ return ค่ายกกำลังสองของตัวเลขที่รับเข้ามา
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex3_fill_return",
    title="", instructions="",
    starter_code=(
        'def square(n):\n'
        '    # TODO: return ค่า n ยกกำลังสอง\n'
        '    \n'
        '\n'
        'result = square(5)\n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="25",
    hint="ใช้ return n ** 2 (เครื่องหมาย ** คือยกกำลัง) หรือ return n * n ก็ได้ผลเหมือนกัน",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — parameter ค่า default")
st.markdown("""
เติมโค้ดให้ parameter `greeting` มีค่า default เป็น `"สวัสดี"` แล้วทดสอบเรียกใช้ทั้งแบบ
ระบุค่าและไม่ระบุค่า
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex4_fill_default",
    title="", instructions="",
    starter_code=(
        '# TODO: เติมค่า default ให้ greeting เป็น "สวัสดี"\n'
        'def greet(name, greeting):\n'
        '    print(f"{greeting} {name}")\n'
        '\n'
        'greet("สมชาย")\n'
        'greet("สมหญิง", "หวัดดี")\n'
    ),
    check_type="exact",
    expected_output="สวัสดี สมชาย\nหวัดดี สมหญิง",
    hint='การตั้งค่า default ทำได้โดยเขียน parameter_name="ค่าเริ่มต้น" ในวงเล็บตอนนิยามฟังก์ชัน '
         'เช่น def greet(name, greeting="ค่าเริ่มต้น"):',
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — ฟังก์ชันเรียกฟังก์ชัน")
st.markdown("""
เติมโค้ดให้ฟังก์ชัน `calculate_total` เรียกใช้ฟังก์ชัน `apply_discount` ที่มีอยู่แล้ว
เพื่อคำนวณราคาหลังหักส่วนลด
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex5_fill_funccall",
    title="", instructions="",
    starter_code=(
        'def apply_discount(price, discount_percent):\n'
        '    return price * (1 - discount_percent / 100)\n'
        '\n'
        'def calculate_total(price, discount_percent):\n'
        '    # TODO: เรียกใช้ apply_discount แล้ว return ผลลัพธ์ (ปัดทศนิยม 2 ตำแหน่ง)\n'
        '    \n'
        '\n'
        'print(calculate_total(1000, 10))\n'
    ),
    check_type="exact",
    expected_output="900.0",
    hint="เรียก apply_discount(price, discount_percent) แล้วครอบด้วย round(..., 2) ก่อน return ผลลัพธ์",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — local vs global scope")
st.markdown("""
เติมโค้ดในฟังก์ชันให้สร้างตัวแปร local ชื่อ `result` แล้ว return ออกมา
(สังเกตว่าตัวแปร `result` ข้างนอกฟังก์ชันจะไม่ถูกฟังก์ชันนี้แก้ไข เพราะเป็นตัวแปรคนละตัวกัน)
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex6_fill_scope",
    title="", instructions="",
    starter_code=(
        'result = "ค่าเดิมข้างนอก"\n'
        '\n'
        'def compute():\n'
        '    # TODO: สร้างตัวแปร local ชื่อ result เก็บค่า "ค่าใหม่ในฟังก์ชัน" แล้ว return\n'
        '    \n'
        '    return result\n'
        '\n'
        'print(compute())\n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="ค่าใหม่ในฟังก์ชัน\nค่าเดิมข้างนอก",
    hint='เติมบรรทัด result = "ค่าใหม่ในฟังก์ชัน" ก่อนบรรทัด return — ตัวแปรนี้จะเป็น local '
         'แยกจากตัวแปร result ข้างนอกฟังก์ชันโดยสิ้นเชิง',
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — หลาย parameter พร้อม keyword argument")
st.markdown("""
เติมโค้ดเรียกใช้ฟังก์ชันโดยระบุชื่อ parameter ตรง ๆ (keyword argument) เพื่อสลับลำดับการส่งค่าได้
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex7_fill_kwargs",
    title="", instructions="",
    starter_code=(
        'def describe_person(name, age, city):\n'
        '    print(f"{name} อายุ {age} ปี อยู่ที่ {city}")\n'
        '\n'
        '# TODO: เรียกใช้ฟังก์ชันโดยระบุ city="ขอนแก่น", name="ปรีชา", age=28 (เรียงลำดับตามนี้)\n'
        '\n'
    ),
    check_type="exact",
    expected_output="ปรีชา อายุ 28 ปี อยู่ที่ ขอนแก่น",
    hint='เรียกฟังก์ชันโดยระบุชื่อ parameter=ค่า ตรง ๆ เช่น describe_person(city="...", name="...", age=...) '
         'วิธีนี้ลำดับการเขียนไม่ต้องตรงกับลำดับที่นิยามฟังก์ชันไว้',
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — ฟังก์ชันแฟกทอเรียล")
st.markdown("""
เขียนฟังก์ชันชื่อ `factorial(n)` รับจำนวนเต็มไม่ติดลบ แล้ว return ค่าแฟกทอเรียล (n!)
ตามนิยาม: `n! = n × (n-1) × (n-2) × ... × 1` และ `0! = 1`
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex8_write_factorial",
    title="", instructions="",
    starter_code="def factorial(n):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="factorial",
    test_cases=[
        {"args": (5,), "expected": 120, "label": "5! = 120"},
        {"args": (0,), "expected": 1, "label": "0! = 1 (กรณีพิเศษ)"},
        {"args": (1,), "expected": 1, "label": "1! = 1"},
        {"args": (4,), "expected": 24, "label": "4! = 24"},
    ],
    hint="ตั้งตัวแปรสะสมผลลัพธ์เริ่มที่ 1 (ไม่ใช่ 0 เพราะเป็นการคูณสะสม) วนลูปตั้งแต่ 1 ถึง n "
         "คูณตัวแปรสะสมด้วยเลขในแต่ละรอบ — ลองสังเกตว่า 0! ต้องได้ 1 โดยที่ลูปอาจจะไม่ทำงานเลยถ้า n=0",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — ตรวจสอบ palindrome")
st.markdown("""
เขียนฟังก์ชันชื่อ `is_palindrome(text)` รับ string แล้ว return `True` ถ้าข้อความนั้น
อ่านจากหน้าไปหลังกับหลังไปหน้าเหมือนกัน (palindrome) เช่น "level", "racecar"

(ไม่ต้องสนใจตัวพิมพ์ใหญ่-เล็กหรือช่องว่าง รับเฉพาะ input ที่เป็นตัวพิมพ์เล็กไม่มีช่องว่างพอ)
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex9_write_palindrome",
    title="", instructions="",
    starter_code="def is_palindrome(text):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="is_palindrome",
    test_cases=[
        {"args": ("level",), "expected": True, "label": "level เป็น palindrome"},
        {"args": ("hello",), "expected": False, "label": "hello ไม่เป็น palindrome"},
        {"args": ("racecar",), "expected": True, "label": "racecar เป็น palindrome"},
        {"args": ("a",), "expected": True, "label": "ตัวอักษรเดียวเป็น palindrome เสมอ"},
    ],
    hint="ลองสร้างข้อความที่กลับด้านแล้วเทียบกับข้อความเดิมว่าเหมือนกันไหม "
         "(การกลับด้าน string ทำได้คล้ายกับการกลับด้าน list ที่เคยฝึกในบทก่อน "
         "หรือใช้ slicing text[::-1] ก็ได้เช่นกัน)",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — ฟังก์ชันคำนวณค่าเฉลี่ยแบบมีเงื่อนไข")
st.markdown("""
เขียนฟังก์ชันชื่อ `average_passing(scores, passing_score)` รับ list ของคะแนน และ
คะแนนผ่าน (`passing_score`) แล้ว return ค่าเฉลี่ยของคะแนนที่ **ผ่าน** เท่านั้น
(คะแนน >= passing_score) ปัดทศนิยม 2 ตำแหน่ง

ถ้าไม่มีใครผ่านเลย ให้ return `0`
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex10_write_avgpassing",
    title="", instructions="",
    starter_code="def average_passing(scores, passing_score):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="average_passing",
    test_cases=[
        {"args": ([90, 45, 70, 30, 85], 50), "expected": 81.67, "label": "ผ่าน 3 จาก 5 คน"},
        {"args": ([30, 40, 20], 50), "expected": 0, "label": "ไม่มีใครผ่าน"},
        {"args": ([60, 70, 80], 50), "expected": 70.0, "label": "ผ่านทุกคน"},
    ],
    hint="กรองเอาเฉพาะคะแนนที่มากกว่าเท่ากับ passing_score ออกมาก่อน (ลองสร้าง list ใหม่เก็บเฉพาะคะแนนที่ผ่าน) "
         "ถ้า list ที่กรองได้มีความยาวเป็น 0 ให้ return 0 ทันที ไม่งั้นจะหารด้วย 0 ไม่ได้ "
         "ถ้ามีคนผ่าน ให้คำนวณผลรวมหารด้วยจำนวนคนที่ผ่าน แล้วปัดทศนิยม",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — ฟังก์ชันสร้างรหัสผ่านง่าย ๆ")
st.markdown("""
เขียนฟังก์ชันชื่อ `mask_email(email)` รับ email (string รูปแบบ `username@domain`)
แล้ว return string ที่ซ่อนตัวอักษรของ username ไว้ (แสดงตัวอักษรตัวแรกของ username
ตามด้วย `***` แล้วต่อด้วย `@domain` เหมือนเดิม)

ตัวอย่าง: `mask_email("somchai@kku.ac.th")` ควร return `"s***@kku.ac.th"`
""")

render_exercise(
    lesson_id="lesson06", exercise_id="ex11_write_maskemail",
    title="", instructions="",
    starter_code="def mask_email(email):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="mask_email",
    test_cases=[
        {"args": ("somchai@kku.ac.th",), "expected": "s***@kku.ac.th", "label": "email ปกติ"},
        {"args": ("a@example.com",), "expected": "a***@example.com", "label": "username ตัวเดียว"},
        {"args": ("preecha@gmail.com",), "expected": "p***@gmail.com", "label": "email gmail"},
    ],
    hint="แยก email ออกเป็น username กับ domain โดยใช้ .split('@') (จะได้ list 2 ส่วน) "
         "ดึงตัวอักษรตัวแรกของ username ด้วย index [0] แล้วต่อด้วย '***@' และ domain ที่แยกได้",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/5_บทที่5_loops.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/7_บทที่7_error_handling.py", label="ไปบทต่อไป: Error Handling ➡️")
