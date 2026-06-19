"""บทที่ 4: Conditions"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar()

st.title("บทที่ 4: Conditions (เงื่อนไข)")

st.markdown("""
### if / elif / else — ตัดสินใจตามเงื่อนไข

โปรแกรมส่วนใหญ่ต้อง "ตัดสินใจ" ว่าจะทำอะไรตามสถานการณ์ — เครื่องมือหลักคือ `if`

```python
age = 20
if age >= 18:
    print("เป็นผู้ใหญ่")
else:
    print("ยังเป็นผู้เยาว์")
```

ถ้ามีหลายเงื่อนไข ใช้ `elif` (ย่อจาก "else if") ต่อกันได้

```python
score = 75
if score >= 80:
    print("เกรด A")
elif score >= 70:
    print("เกรด B")
elif score >= 60:
    print("เกรด C")
else:
    print("เกรด D")
```

### Comparison operators

| Operator | ความหมาย | ตัวอย่าง |
|---|---|---|
| `==` | เท่ากับ | `5 == 5` → True |
| `!=` | ไม่เท่ากับ | `5 != 3` → True |
| `>` `<` | มากกว่า/น้อยกว่า | `5 > 3` → True |
| `>=` `<=` | มากกว่าเท่ากับ/น้อยกว่าเท่ากับ | `5 >= 5` → True |

### Logical operators

ใช้รวมหลายเงื่อนไขเข้าด้วยกัน

```python
age = 25
has_id = True

if age >= 18 and has_id:       # ต้องจริงทั้งคู่
    print("เข้าได้")

if age < 13 or age > 65:        # จริงอย่างใดอย่างหนึ่งก็พอ
    print("ราคาพิเศษ")

if not has_id:                   # กลับค่าความจริง
    print("กรุณาแสดงบัตร")
```

### in / not in — ตรวจสอบว่ามีอยู่ใน list, string, dict หรือไม่

`in` เป็น operator ที่ใช้บ่อยมากในงานจริง ตรวจสอบว่าค่าหนึ่งอยู่ใน "กลุ่ม" ของข้อมูลหรือไม่
ใช้ได้ทั้งกับ list, string, dict, set — เขียนสั้นและอ่านง่ายกว่าการเขียน `or` หลายตัว

```python
fruits = ["แอปเปิ้ล", "กล้วย", "ส้ม"]

if "กล้วย" in fruits:
    print("มีกล้วยอยู่ในรายการ")

if "มะม่วง" not in fruits:
    print("ไม่มีมะม่วงในรายการ")

# ใช้กับ string ตรวจสอบว่ามีตัวอักษร/คำนั้นอยู่หรือไม่
email = "somchai@kku.ac.th"
if "@" in email:
    print("รูปแบบอีเมลดูถูกต้อง")

# ใช้กับ dict จะตรวจสอบที่ key (ไม่ใช่ value)
student = {"name": "สมชาย", "age": 20}
if "name" in student:
    print("มีข้อมูลชื่ออยู่")
```

เทียบกับการเขียนแบบเดิมด้วย `or` หลายตัว จะเห็นว่า `in` กระชับกว่ามาก

```python
day = "เสาร์"

# แบบเดิม (or ซ้ำหลายตัว)
if day == "เสาร์" or day == "อาทิตย์":
    print("วันหยุด")

# แบบใช้ in (อ่านง่ายกว่าเมื่อมีหลายค่าให้เทียบ)
if day in ["เสาร์", "อาทิตย์"]:
    print("วันหยุด")
```

### Operator ที่นิยมใช้อื่น ๆ

**Chained comparison** — เขียนช่วงค่าได้กระชับกว่าใช้ `and`

```python
age = 30
if 18 <= age <= 60:        # เทียบเท่ากับ age >= 18 and age <= 60
    print("อยู่ในวัยทำงาน")
```

**is / is not** — ใช้เทียบกับ `None` โดยเฉพาะ (เป็นธรรมเนียมที่นิยมใช้ในวงการ Python)

```python
data = None
if data is None:
    print("ยังไม่มีข้อมูล")

result = 5
if result is not None:
    print("มีผลลัพธ์แล้ว")
```

**Conditional expression (ternary)** — เขียน if-else แบบสั้นในบรรทัดเดียว เหมาะกับเงื่อนไขง่าย ๆ

```python
age = 20
status = "ผู้ใหญ่" if age >= 18 else "ผู้เยาว์"
print(status)   # ผู้ใหญ่
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (if-else พื้นฐาน)")
st.markdown("""
ตัวอย่าง:
```python
number = 7
if number % 2 == 0:
    print("เลขคู่")
else:
    print("เลขคี่")
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ (number = 7) ให้ได้ผลลัพธ์:
```
เลขคี่
```
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex1_copy_evenodd",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="เลขคี่",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด เครื่องหมาย % คือหารเอาเศษ ลองคิดดูว่า 7 หาร 2 เหลือเศษเท่าไร",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (elif หลายเงื่อนไข)")
st.markdown("""
ตัวอย่าง:
```python
score = 75
if score >= 80:
    print("เกรด A")
elif score >= 70:
    print("เกรด B")
else:
    print("เกรด C")
```

ทำตามตัวอย่าง แต่เปลี่ยน score เป็น **95** แทน
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex2_copy_grade",
    title="", instructions="",
    starter_code=(
        'score = 0\n'
        'if score >= 80:\n'
        '    print("เกรด A")\n'
        'elif score >= 70:\n'
        '    print("เกรด B")\n'
        'else:\n'
        '    print("เกรด C")\n'
    ),
    check_type="exact",
    expected_output="เกรด A",
    hint="แก้แค่ค่าตัวแปร score บรรทัดแรก โครงสร้างเงื่อนไขที่เหลือไม่ต้องแก้",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — ตรวจสอบจำนวนเต็มบวก")
st.markdown("""
เติมเงื่อนไขให้ตรวจสอบว่าตัวเลขเป็นค่าบวกหรือไม่
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex3_fill_positive",
    title="", instructions="",
    starter_code=(
        'number = 15\n'
        '# TODO: เติมเงื่อนไขว่า number มากกว่า 0\n'
        'if :\n'
        '    print("เป็นจำนวนบวก")\n'
        'else:\n'
        '    print("ไม่ใช่จำนวนบวก")\n'
    ),
    check_type="exact",
    expected_output="เป็นจำนวนบวก",
    hint="ใช้เครื่องหมายเปรียบเทียบ 'มากกว่า' เทียบ number กับ 0 ตรงๆ",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — ใช้ and รวมเงื่อนไข")
st.markdown("""
เติมเงื่อนไขให้ตรวจสอบว่าอายุอยู่ในช่วง 18-60 ปี (รวมค่าทั้งสองขอบ) หรือไม่
ใช้ `and` รวม 2 เงื่อนไขเข้าด้วยกัน (หรือลองใช้ chained comparison ที่เรียนไปก็ได้)
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex4_fill_and",
    title="", instructions="",
    starter_code=(
        'age = 30\n'
        '# TODO: เติมเงื่อนไขว่า age อยู่ระหว่าง 18 ถึง 60 (รวมขอบ) โดยใช้ and\n'
        'if :\n'
        '    print("อยู่ในวัยทำงาน")\n'
        'else:\n'
        '    print("ไม่อยู่ในวัยทำงาน")\n'
    ),
    check_type="exact",
    expected_output="อยู่ในวัยทำงาน",
    hint="ต้องเช็คสองเงื่อนไขพร้อมกันคือ age มากกว่าเท่ากับ 18 และ age น้อยกว่าเท่ากับ 60 เชื่อมด้วย and",
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — ใช้ in ตรวจสอบสมาชิกใน list")
st.markdown("""
เติมเงื่อนไขให้ตรวจสอบว่าวันนี้เป็นวันเสาร์หรืออาทิตย์หรือไม่ (วันหยุดสุดสัปดาห์)
โดยใช้ `in` เทียบกับ list ของวันหยุด (ตามที่เรียนไปในเนื้อหาด้านบน)
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex5_fill_in",
    title="", instructions="",
    starter_code=(
        'day = "เสาร์"\n'
        'weekend_days = ["เสาร์", "อาทิตย์"]\n'
        '# TODO: เติมเงื่อนไขว่า day อยู่ใน weekend_days โดยใช้ in\n'
        'if :\n'
        '    print("วันหยุด")\n'
        'else:\n'
        '    print("วันทำงาน")\n'
    ),
    check_type="exact",
    expected_output="วันหยุด",
    hint="รูปแบบคือ ค่า in list_name — ตรวจสอบว่าตัวแปร day อยู่ใน weekend_days หรือไม่",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — ใช้ not in")
st.markdown("""
เติมเงื่อนไขให้ตรวจสอบว่าชื่อผู้ใช้ที่กรอกมา **ยังไม่มี** อยู่ในระบบหรือไม่ (เพื่ออนุญาตให้สมัครสมาชิกใหม่ได้)
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex6_fill_notin",
    title="", instructions="",
    starter_code=(
        'existing_users = ["somchai", "somying", "wichai"]\n'
        'new_username = "preecha"\n'
        '# TODO: เติมเงื่อนไขว่า new_username ไม่อยู่ใน existing_users\n'
        'if :\n'
        '    print("สมัครสมาชิกได้")\n'
        'else:\n'
        '    print("ชื่อผู้ใช้นี้มีคนใช้แล้ว")\n'
    ),
    check_type="exact",
    expected_output="สมัครสมาชิกได้",
    hint="ใช้ not in แทน in เพื่อตรวจสอบว่าค่านั้น 'ไม่อยู่' ใน list",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — เงื่อนไขซ้อนกัน (nested)")
st.markdown("""
เติมเงื่อนไขชั้นในให้ตรวจสอบว่ารหัสผ่านมีความยาวอย่างน้อย 8 ตัวอักษรหรือไม่
(ใช้ `len()` ตรวจความยาว) — เงื่อนไขชั้นนอกตรวจสอบว่ามี username ก่อนแล้ว
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex7_fill_nested",
    title="", instructions="",
    starter_code=(
        'username = "somchai"\n'
        'password = "12345678"\n'
        '\n'
        'if len(username) > 0:\n'
        '    # TODO: เติมเงื่อนไขว่าความยาวของ password อย่างน้อย 8 ตัวอักษร\n'
        '    if :\n'
        '        print("สมัครสมาชิกสำเร็จ")\n'
        '    else:\n'
        '        print("รหัสผ่านสั้นเกินไป")\n'
        'else:\n'
        '    print("กรุณากรอก username")\n'
    ),
    check_type="exact",
    expected_output="สมัครสมาชิกสำเร็จ",
    hint="ใช้ len(password) เทียบกับ 8 ด้วยเครื่องหมายมากกว่าเท่ากับ เหมือนที่เงื่อนไขชั้นนอกเช็ค len(username)",
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — ตัดเกรดจากคะแนน")
st.markdown("""
เขียนฟังก์ชันชื่อ `get_grade(score)` รับคะแนน (0-100) แล้ว return เกรดเป็น string ตามนี้:
- คะแนน 80 ขึ้นไป → `"A"`
- คะแนน 70-79 → `"B"`
- คะแนน 60-69 → `"C"`
- คะแนน 50-59 → `"D"`
- ต่ำกว่า 50 → `"F"`
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex8_write_grade",
    title="", instructions="",
    starter_code="def get_grade(score):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="get_grade",
    test_cases=[
        {"args": (95,), "expected": "A", "label": "คะแนน 95"},
        {"args": (75,), "expected": "B", "label": "คะแนน 75"},
        {"args": (65,), "expected": "C", "label": "คะแนน 65"},
        {"args": (55,), "expected": "D", "label": "คะแนน 55"},
        {"args": (30,), "expected": "F", "label": "คะแนน 30"},
        {"args": (80,), "expected": "A", "label": "ขอบเขตพอดี 80"},
        {"args": (60,), "expected": "C", "label": "ขอบเขตพอดี 60"},
    ],
    hint="ไล่เช็คเงื่อนไขจากคะแนนสูงสุดลงมาก่อนด้วย if-elif-else ระวังลำดับ: ถ้าเช็คจากคะแนนต่ำขึ้นไปก่อน "
         "ผลลัพธ์จะผิดเพราะเงื่อนไขแรกที่เป็นจริงจะถูกใช้ก่อนเสมอ",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — ตรวจสอบปีอธิกสุรทิน")
st.markdown("""
เขียนฟังก์ชันชื่อ `is_leap_year(year)` รับปี ค.ศ. แล้ว return `True`/`False`
ว่าเป็นปีอธิกสุรทิน (leap year) หรือไม่ ตามกฎ:
- ถ้าหารด้วย 4 ลงตัว **และ** หารด้วย 100 ไม่ลงตัว → เป็นปีอธิกสุรทิน
- หรือถ้าหารด้วย 400 ลงตัว → เป็นปีอธิกสุรทินเสมอ (ไม่ว่าจะหารด้วย 100 ลงตัวหรือไม่)
- กรณีอื่น → ไม่เป็นปีอธิกสุรทิน

ตัวอย่าง: ปี 2000 หารด้วย 400 ลงตัว → เป็นปีอธิกสุรทิน, ปี 1900 หารด้วย 100 ลงตัวแต่หารด้วย 400 ไม่ลงตัว → ไม่เป็น
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex9_write_leapyear",
    title="", instructions="",
    starter_code="def is_leap_year(year):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="is_leap_year",
    test_cases=[
        {"args": (2024,), "expected": True, "label": "2024 (หาร 4 ลงตัว ไม่หาร 100)"},
        {"args": (2023,), "expected": False, "label": "2023 (หาร 4 ไม่ลงตัว)"},
        {"args": (1900,), "expected": False, "label": "1900 (หาร 100 ลงตัว แต่หาร 400 ไม่ลงตัว)"},
        {"args": (2000,), "expected": True, "label": "2000 (หาร 400 ลงตัว)"},
        {"args": (2100,), "expected": False, "label": "2100 (หาร 100 ลงตัว แต่หาร 400 ไม่ลงตัว)"},
    ],
    hint="ใช้ % (หารเอาเศษ) ตรวจการหารลงตัว (เศษเป็น 0 แปลว่าหารลงตัว) แปลงกฎทั้ง 3 ข้อในโจทย์เป็นเงื่อนไข "
         "and/or ตรงตามที่อธิบายไว้ — กฎข้อแรกกับข้อสองเป็น 'หรือ' กัน (เป็นอธิกสุรทินได้จากเงื่อนไขใดเงื่อนไขหนึ่ง)",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — หมวดหมู่ BMI")
st.markdown("""
เขียนฟังก์ชันชื่อ `bmi_category(bmi)` รับค่า BMI แล้ว return หมวดหมู่เป็น string ตามเกณฑ์:
- BMI ต่ำกว่า 18.5 → `"น้ำหนักน้อย"`
- BMI 18.5 ถึง 22.9 → `"น้ำหนักปกติ"`
- BMI 23.0 ถึง 24.9 → `"น้ำหนักเกิน"`
- BMI 25.0 ขึ้นไป → `"อ้วน"`

(ค่าตามเกณฑ์มาตรฐานเอเชีย — ใช้ในการคำนวณเชิงสาธารณสุขจริง)
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex10_write_bmicategory",
    title="", instructions="",
    starter_code="def bmi_category(bmi):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="bmi_category",
    test_cases=[
        {"args": (17.0,), "expected": "น้ำหนักน้อย", "label": "BMI 17.0"},
        {"args": (20.0,), "expected": "น้ำหนักปกติ", "label": "BMI 20.0"},
        {"args": (24.0,), "expected": "น้ำหนักเกิน", "label": "BMI 24.0"},
        {"args": (28.0,), "expected": "อ้วน", "label": "BMI 28.0"},
        {"args": (18.5,), "expected": "น้ำหนักปกติ", "label": "ขอบเขตพอดี 18.5"},
        {"args": (25.0,), "expected": "อ้วน", "label": "ขอบเขตพอดี 25.0"},
    ],
    hint="ไล่เช็คจากค่าน้อยไปมากด้วย if-elif-else สังเกตว่าขอบเขตของแต่ละหมวดต่อเนื่องกัน "
         "(18.5 อยู่ในหมวด 'ปกติ' ไม่ใช่ 'น้อย') ลองเขียนเงื่อนไขแรกเป็น bmi < 18.5 ก่อน แล้วไล่ตามลำดับขอบเขต",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — ตรวจสอบคำที่ห้ามใช้")
st.markdown("""
เขียนฟังก์ชันชื่อ `contains_banned_word(text, banned_words)` รับข้อความ `text` (string)
และ list ของคำที่ห้ามใช้ `banned_words` แล้ว return `True` ถ้าพบว่ามีคำในกลุ่มคำห้ามใช้
ปรากฏอยู่ใน `text` (เป็นคำที่ตรงกันเป๊ะ ไม่ต้องดูเป็น substring) และ return `False` ถ้าไม่พบเลย

**แนวทาง:** ต้องแยกคำใน `text` ออกมาก่อน (ใช้ `.split()` แยกตามช่องว่าง) แล้วเช็คว่าคำใดคำหนึ่ง
ใน banned_words ปรากฏอยู่ใน list ของคำที่แยกออกมาหรือไม่
""")

render_exercise(
    lesson_id="lesson04", exercise_id="ex11_write_bannedword",
    title="", instructions="",
    starter_code=(
        "def contains_banned_word(text, banned_words):\n"
        "    # เขียนโค้ดของคุณที่นี่\n"
        "    # ลองใช้ text.split() แยกคำ แล้ววนลูปหรือใช้ in ตรวจสอบ\n"
        "    pass\n"
    ),
    check_type="function",
    function_name="contains_banned_word",
    test_cases=[
        {"args": ("this is a bad example", ["bad", "terrible"]), "expected": True, "label": "พบคำห้ามใช้"},
        {"args": ("this is a good example", ["bad", "terrible"]), "expected": False, "label": "ไม่พบคำห้ามใช้"},
        {"args": ("everything is terrible today", ["bad", "terrible"]), "expected": True, "label": "พบคำห้ามใช้คำที่สอง"},
        {"args": ("hello world", []), "expected": False, "label": "ไม่มีคำห้ามใช้เลย"},
    ],
    hint="แยกคำใน text ด้วย .split() จะได้ list ของคำทั้งหมด จากนั้นวนลูปไล่ทีละคำใน banned_words "
         "แล้วตรวจสอบด้วย in ว่าคำนั้นอยู่ใน list ที่แยกมาหรือไม่ — ถ้าพบแม้แค่คำเดียว ให้ return True ทันที",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/3_บทที่3_data_structure.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/5_บทที่5_loops.py", label="ไปบทต่อไป: Loops ➡️")
