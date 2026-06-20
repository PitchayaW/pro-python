"""บทที่ 2: ตัวแปรและ Data Type"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise


if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson02", total_exercises=11)

st.title("บทที่ 2: ตัวแปรและ Data Type")

st.markdown("""
### ตัวแปร (Variable)

ตัวแปรคือ "ชื่อ" ที่ใช้เก็บค่าข้อมูลไว้ใช้งานต่อ ในไพธอนไม่ต้องประกาศประเภทข้อมูลล่วงหน้า
(ต่างจากภาษาอย่าง Java หรือ C++) แค่ตั้งชื่อแล้วกำหนดค่าได้เลย

```python
age = 25
name = "สมชาย"
height = 175.5
is_student = True
```

### ประเภทข้อมูลพื้นฐาน (Data Type)

| ประเภท | ตัวอย่าง | ใช้เก็บ |
|---|---|---|
| `int` | `25`, `-3`, `0` | จำนวนเต็ม |
| `float` | `175.5`, `3.14` | จำนวนทศนิยม |
| `str` | `"สมชาย"`, `'Hello'` | ข้อความ |
| `bool` | `True`, `False` | ค่าจริง/เท็จ |

ตรวจสอบประเภทของตัวแปรได้ด้วยฟังก์ชัน `type()`

```python
age = 25
print(type(age))  # <class 'int'>
```

### การคำนวณ (Arithmetic Operators)

ไพธอนมีเครื่องหมายคำนวณพื้นฐานให้ใช้ ดังนี้

| Operator | ความหมาย | ตัวอย่าง | ผลลัพธ์ |
|---|---|---|---|
| `+` | บวก | `5 + 3` | `8` |
| `-` | ลบ | `5 - 3` | `2` |
| `*` | คูณ | `5 * 3` | `15` |
| `/` | หาร (ได้ผลเป็นทศนิยมเสมอ) | `7 / 2` | `3.5` |
| `**` | ยกกำลัง | `2 ** 3` | `8` |
| `//` | หารปัดเศษทิ้ง (floor division) | `7 // 2` | `3` |
| `%` | หารเอาเศษ (modulo) | `7 % 2` | `1` |

`%` ใช้บ่อยมากในการตรวจสอบว่าหารลงตัวหรือไม่ (เศษเป็น 0 แปลว่าหารลงตัว) เช่นตรวจสอบ
เลขคู่/เลขคี่ ส่วน `//` ใช้เมื่อต้องการผลหารเป็นจำนวนเต็มโดยตัดทศนิยมทิ้ง

```python
print(10 % 3)    # 1   — 10 หาร 3 เหลือเศษ 1
print(10 // 3)    # 3   — 10 หาร 3 ได้ผลหารเต็ม 3 (ตัดเศษทิ้ง)
```

### ลำดับการคำนวณ (Operator Precedence)

เมื่อมีหลาย operator ผสมกันในนิพจน์เดียว ไพธอนคำนวณตามลำดับความสำคัญ
**วงเล็บ `()` → ยกกำลัง `**` → คูณ/หาร/หารเอาเศษ `* / // %` → บวก/ลบ `+ -`**
(เหมือนหลักการ "คูณหารก่อนบวกลบ" ที่เคยเรียนในวิชาคณิตศาสตร์)
ถ้า operator มีลำดับความสำคัญเท่ากัน จะคำนวณจากซ้ายไปขวา

```python
print(2 + 3 * 4)        # 14  — คูณก่อน (3*4=12) แล้วค่อยบวก (2+12=14)
print((2 + 3) * 4)       # 20  — วงเล็บก่อนเสมอ (2+3=5) แล้วค่อยคูณ (5*4=20)
print(2 ** 3 + 1)         # 9   — ยกกำลังก่อน (2**3=8) แล้วค่อยบวก (8+1=9)
print(10 - 4 / 2)          # 8.0 — หารก่อน (4/2=2.0) แล้วค่อยลบ (10-2.0=8.0)
```

**คำแนะนำ:** ถ้าไม่แน่ใจเรื่องลำดับ หรืออยากให้โค้ดอ่านง่ายชัดเจน ใส่วงเล็บครอบส่วนที่
ต้องการคำนวณก่อนได้เสมอ ไม่ผิดอะไรและช่วยลดข้อผิดพลาดจากการคำนวณผิดลำดับ

### Compound Assignment Operators — ย่อการอัปเดตตัวแปร

เวลาต้องการอัปเดตค่าตัวแปรโดยใช้ค่าเดิมของมันเอง (เช่น `score = score + 10`) ไพธอนมี
เครื่องหมายย่อให้เขียนสั้นลงได้ ทำงานแบบเดียวกันแต่กระชับกว่า

| เขียนแบบย่อ | เทียบเท่ากับ |
|---|---|
| `x += 5` | `x = x + 5` |
| `x -= 5` | `x = x - 5` |
| `x *= 5` | `x = x * 5` |
| `x /= 5` | `x = x / 5` |
| `x **= 2` | `x = x ** 2` |
| `x //= 2` | `x = x // 2` |
| `x %= 2` | `x = x % 2` |

```python
score = 10
score += 5      # score กลายเป็น 15
score *= 2       # score กลายเป็น 30
print(score)      # 30
```

### การแปลงประเภทข้อมูล (Type Casting)

```python
age_text = "25"
age_number = int(age_text)   # แปลง string เป็น int
price = str(99.5)             # แปลง float เป็น string
```

### การต่อข้อความด้วย f-string

เวลาอยากนำตัวแปรมาแสดงรวมกับข้อความ ใช้ f-string ได้สะดวกมาก
(ใส่ `f` หน้าเครื่องหมายคำพูด แล้วใส่ตัวแปรในวงเล็บปีกกา `{ }`)

```python
name = "สมชาย"
age = 25
print(f"ชื่อ {name} อายุ {age} ปี")   # ได้: ชื่อ สมชาย อายุ 25 ปี
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-8 เติมโค้ดในจุดที่ขาด | ข้อ 9-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (ทำซ้ำ)")
st.markdown("""
ดูตัวอย่างโค้ดนี้ก่อน:

```python
score = 85
print(score)
print(type(score))
```

**ลองพิมพ์โค้ดด้านบนนี้ในช่อง editor แล้วกดรัน** ให้ได้ผลลัพธ์ตรงตามนี้เป๊ะ:
```
85
<class 'int'>
```
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex1_copy_basic",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="85\n<class 'int'>",
    hint="ดูตัวอย่างโค้ดด้านบนแล้วพิมพ์ตามทุกบรรทัด ระวังตัวพิมพ์ใหญ่-เล็กและวงเล็บให้ตรงกับตัวอย่าง",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (เปลี่ยนค่านิดหน่อย)")
st.markdown("""
ตัวอย่าง:
```python
city = "ขอนแก่น"
print(f"ฉันอยู่ที่ {city}")
```

ทำตามตัวอย่าง แต่เปลี่ยนเป็นเมือง **"เชียงใหม่"** แทน ให้ได้ผลลัพธ์:
```
ฉันอยู่ที่ เชียงใหม่
```
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex2_copy_fstring",
    title="", instructions="",
    starter_code='city = ""\nprint(f"ฉันอยู่ที่ {city}")\n',
    check_type="exact",
    expected_output="ฉันอยู่ที่ เชียงใหม่",
    hint="แก้แค่ค่าในตัวแปร city เท่านั้น โครงสร้างโค้ดที่เหลือไม่ต้องเปลี่ยน",
)

# ============================================================
# ข้อ 3-8: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — ลำดับการคำนวณ")
st.markdown("""
เติมโค้ดให้คำนวณนิพจน์ตามลำดับการคำนวณที่เรียนไป โดยไม่ใส่วงเล็บเพิ่ม
(สังเกตว่าผลลัพธ์จะต่างจากการบวกแล้วคูณตามลำดับซ้ายไปขวาธรรมดา)
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex3_fill_precedence",
    title="", instructions="",
    starter_code=(
        '# TODO: คำนวณ 3 บวกกับ (4 คูณ 5) โดยใช้ลำดับการคำนวณปกติ ไม่ใส่วงเล็บเพิ่ม\n'
        'result = 3 \n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="23",
    hint="เติมเครื่องหมาย + 4 * 5 ต่อจาก 3 — เครื่องหมายคูณจะถูกคำนวณก่อนบวกเสมอตามลำดับที่เรียนไป",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — modulo ตรวจสอบเลขคู่/คี่")
st.markdown("""
เติมโค้ดให้ใช้ `%` ตรวจสอบว่าตัวเลขเป็นเลขคู่หรือไม่ (หารด้วย 2 ลงตัว)
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex4_fill_modulo",
    title="", instructions="",
    starter_code=(
        'number = 18\n'
        '# TODO: หาเศษจากการหาร number ด้วย 2 เก็บในตัวแปร remainder\n'
        'remainder = \n'
        'print(remainder)\n'
    ),
    check_type="exact",
    expected_output="0",
    hint="ใช้เครื่องหมาย % หาเศษจากการหาร number % 2 — ถ้าเป็นเลขคู่ เศษจะเป็น 0 เสมอ",
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — แปลงข้อความเป็นตัวเลข")
st.markdown("""
มีตัวแปร `price_text` เก็บราคาเป็น string อยู่ ต้องแปลงเป็น `int` ก่อนนำไปคำนวณ
เติมโค้ดในจุดที่มี `# TODO` ให้ครบ
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex5_fill_casting",
    title="", instructions="",
    starter_code=(
        'price_text = "150"\n'
        '# TODO: แปลง price_text เป็น int แล้วเก็บในตัวแปร price\n'
        'price = \n'
        'print(price)\n'
        'print(type(price))\n'
    ),
    check_type="exact",
    expected_output="150\n<class 'int'>",
    hint="มีฟังก์ชันสำหรับแปลง string เป็น int ที่เพิ่งเรียนไปในเนื้อหาด้านบน ลองมองหาในส่วน 'Type Casting'",
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — คำนวณราคารวม")
st.markdown("""
เติมโค้ดให้คำนวณราคารวม (`total`) จากราคาต่อหน่วยกับจำนวนที่ซื้อ แล้วแสดงผลด้วย f-string
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex6_fill_total",
    title="", instructions="",
    starter_code=(
        'price_per_item = 25.5\n'
        'quantity = 4\n'
        '# TODO: คำนวณราคารวม เก็บในตัวแปร total\n'
        'total = \n'
        'print(f"ราคารวม {total} บาท")\n'
    ),
    check_type="exact",
    expected_output="ราคารวม 102.0 บาท",
    hint="ราคารวม = ราคาต่อหน่วย คูณ จำนวนที่ซื้อ — ใช้เครื่องหมาย * ในการคูณ",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — ตรวจสอบ type ด้วย if")
st.markdown("""
เติมเงื่อนไขให้ตรวจสอบว่าตัวแปร `value` เป็น `str` หรือไม่ ถ้าเป็น string ให้พิมพ์ "เป็นข้อความ"
ถ้าไม่ใช่ให้พิมพ์ "ไม่ใช่ข้อความ"
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex7_fill_typecheck",
    title="", instructions="",
    starter_code=(
        'value = "สวัสดี"\n'
        '# TODO: เติมเงื่อนไขตรวจสอบว่า value เป็น str หรือไม่\n'
        'if :\n'
        '    print("เป็นข้อความ")\n'
        'else:\n'
        '    print("ไม่ใช่ข้อความ")\n'
    ),
    check_type="exact",
    expected_output="เป็นข้อความ",
    hint="ใช้ฟังก์ชัน type() เทียบกับ str ด้วยเครื่องหมาย == ในเงื่อนไข if",
)

st.markdown("---")
st.markdown("### ข้อ 8: เติมโค้ดให้สมบูรณ์ — อัปเดตค่าตัวแปรด้วย compound assignment")
st.markdown("""
ตัวแปรเก็บคะแนนเริ่มต้นที่ 0 ต้องการเพิ่มคะแนน 10 แต้ม 3 ครั้ง โดยใช้ `+=` ที่เรียนไป
(เขียนคำสั่งเพิ่มคะแนน 3 บรรทัด) แล้วแสดงคะแนนสุดท้าย
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex8_fill_update",
    title="", instructions="",
    starter_code=(
        'score = 0\n'
        '# TODO: เพิ่มคะแนนทีละ 10 แต้ม จำนวน 3 ครั้ง โดยใช้ += (เขียน score += 10 ซ้ำ 3 บรรทัด)\n'
        '\n'
        '\n'
        '\n'
        'print(f"คะแนนสุดท้าย: {score}")\n'
    ),
    check_type="exact",
    expected_output="คะแนนสุดท้าย: 30",
    hint="ใช้ compound assignment ที่เรียนไป score += 10 ซึ่งเทียบเท่ากับ score = score + 10 "
         "เขียนซ้ำกัน 3 บรรทัด",
)

# ============================================================
# ข้อ 9-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — ฟังก์ชันตรวจสอบประเภทข้อมูล")
st.markdown("""
เขียนฟังก์ชันชื่อ `describe_type(value)` ที่รับค่าเข้ามา 1 ค่า
แล้ว return ชื่อประเภทข้อมูลเป็น string ตามนี้:
- ถ้าเป็น int → return `"จำนวนเต็ม"`
- ถ้าเป็น float → return `"ทศนิยม"`
- ถ้าเป็น str → return `"ข้อความ"`
- ถ้าเป็น bool → return `"ค่าจริงเท็จ"`
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex9_write_describetype",
    title="", instructions="",
    starter_code="def describe_type(value):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="describe_type",
    test_cases=[
        {"args": (5,), "expected": "จำนวนเต็ม", "label": "ใส่ int"},
        {"args": (3.14,), "expected": "ทศนิยม", "label": "ใส่ float"},
        {"args": ("hello",), "expected": "ข้อความ", "label": "ใส่ string"},
        {"args": (True,), "expected": "ค่าจริงเท็จ", "label": "ใส่ bool (True)"},
        {"args": (False,), "expected": "ค่าจริงเท็จ", "label": "ใส่ bool (False)"},
    ],
    hint="ใช้ type(value) เทียบกับ int, float, str, bool ทีละชนิดด้วย if/elif แต่ละเงื่อนไข return ข้อความที่สอดคล้องกัน",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — คำนวณ BMI")
st.markdown("""
เขียนฟังก์ชันชื่อ `calculate_bmi(weight_kg, height_cm)` รับน้ำหนัก (กิโลกรัม) และส่วนสูง (เซนติเมตร)
แล้ว return ค่า BMI (ทศนิยม) ตามสูตร:

```
BMI = น้ำหนัก(kg) / (ส่วนสูง(m))^2
```

**ข้อสังเกต:** ส่วนสูงที่รับเข้ามาเป็นเซนติเมตร ต้องแปลงเป็นเมตรก่อนคำนวณ (หาร 100)
ปัดผลลัพธ์เป็นทศนิยม 2 ตำแหน่งด้วยฟังก์ชัน `round(ค่า, 2)`
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex10_write_bmi",
    title="", instructions="",
    starter_code="def calculate_bmi(weight_kg, height_cm):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="calculate_bmi",
    test_cases=[
        {"args": (70, 175), "expected": 22.86, "label": "น้ำหนัก 70kg ส่วนสูง 175cm"},
        {"args": (60, 160), "expected": 23.44, "label": "น้ำหนัก 60kg ส่วนสูง 160cm"},
        {"args": (50, 150), "expected": 22.22, "label": "น้ำหนัก 50kg ส่วนสูง 150cm"},
    ],
    hint="แปลงส่วนสูงจาก cm เป็น m ก่อน (หารด้วย 100) แล้วใช้สูตร BMI ที่ให้ไว้ในโจทย์ อย่าลืมปัดทศนิยมด้วย round()",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — ฟังก์ชันแปลงอุณหภูมิ")
st.markdown("""
เขียนฟังก์ชันชื่อ `celsius_to_fahrenheit(celsius)` รับอุณหภูมิเป็นองศาเซลเซียส
แล้ว return อุณหภูมิเป็นองศาฟาเรนไฮต์ ตามสูตร:

```
F = C × 9/5 + 32
```

ปัดผลลัพธ์เป็นทศนิยม 1 ตำแหน่งด้วย `round(ค่า, 1)`
""")

render_exercise(
    lesson_id="lesson02", exercise_id="ex11_write_temperature",
    title="", instructions="",
    starter_code="def celsius_to_fahrenheit(celsius):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="celsius_to_fahrenheit",
    test_cases=[
        {"args": (0,), "expected": 32.0, "label": "0 องศาเซลเซียส"},
        {"args": (100,), "expected": 212.0, "label": "100 องศาเซลเซียส"},
        {"args": (37,), "expected": 98.6, "label": "37 องศาเซลเซียส (อุณหภูมิร่างกาย)"},
        {"args": (-40,), "expected": -40.0, "label": "-40 องศาเซลเซียส"},
    ],
    hint="แทนค่า celsius ลงในสูตรที่ให้ไว้ในโจทย์ตรงๆ แล้วปัดทศนิยมด้วย round() ตามที่กำหนด",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_บทที่1_การติดตั้ง.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/3_บทที่3_data_structure.py", label="ไปบทต่อไป: Data Structure ➡️")
