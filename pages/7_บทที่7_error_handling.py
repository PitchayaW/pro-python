"""บทที่ 7: Error Handling"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson07", total_exercises=11)

st.title("บทที่ 7: Error Handling (การจัดการข้อผิดพลาด)")

st.markdown("""
### try / except — จับข้อผิดพลาดไม่ให้โปรแกรมล้ม

เวลาโค้ดเกิด error ขึ้นกลางทาง โปรแกรมจะหยุดทำงานทันที (crash) — `try/except`
ช่วยให้โปรแกรม "จับ" error นั้นไว้ แล้วทำงานอย่างอื่นต่อได้โดยไม่ล้ม

```python
try:
    result = 10 / 0     # บรรทัดนี้จะเกิด error
    print(result)
except ZeroDivisionError:
    print("ไม่สามารถหารด้วยศูนย์ได้")

print("โปรแกรมยังทำงานต่อได้")   # บรรทัดนี้จะถูกรันแม้เกิด error ด้านบน
```

ถ้าไม่มี `try/except` โปรแกรมจะหยุดทำงานทันทีที่เจอ error และบรรทัดหลังจากนั้นจะไม่ถูกรันเลย

### ประเภท Exception ที่พบบ่อย

| Exception | เกิดเมื่อ | ตัวอย่าง |
|---|---|---|
| `ZeroDivisionError` | หารด้วยศูนย์ | `10 / 0` |
| `ValueError` | แปลงค่าไม่ได้ | `int("abc")` |
| `KeyError` | ไม่มี key นั้นใน dict | `{}["x"]` |
| `IndexError` | index เกินขนาด list | `[1,2,3][10]` |
| `TypeError` | ชนิดข้อมูลไม่ตรงกับที่ใช้ได้ | `"5" + 5` |

จับ error แล้วเก็บข้อความ error ไว้ใช้งานได้ด้วย `as`

```python
try:
    number = int("abc")
except ValueError as e:
    print(f"เกิดข้อผิดพลาด: {e}")
```

จับหลายประเภท error พร้อมกันได้ โดยเขียน `except` หลายตัวต่อกัน

```python
try:
    value = int(input_text)
    result = 100 / value
except ValueError:
    print("กรุณากรอกตัวเลข")
except ZeroDivisionError:
    print("ห้ามกรอกเลข 0")
```

### finally — โค้ดที่รันเสมอไม่ว่าจะมี error หรือไม่

`finally` ใช้สำหรับโค้ดที่ต้องรันเสมอ ไม่ว่าจะเกิด error หรือไม่ (เช่น การปิดไฟล์ที่เปิดไว้)

```python
try:
    print("กำลังทำงาน...")
    result = 10 / 0
except ZeroDivisionError:
    print("เกิด error")
finally:
    print("ทำความสะอาดทรัพยากร (รันเสมอ)")
```

### การใช้งานจริงตอนอ่านไฟล์ข้อมูล

เวลาทำงานกับข้อมูลจริง (เช่นที่จะเรียนในบทถัดไปด้วย pandas) มักจะเจอข้อมูลที่ไม่สมบูรณ์
`try/except` ช่วยให้โปรแกรมจัดการกับข้อมูลแปลก ๆ ได้โดยไม่ล้มทั้งโปรแกรม

```python
def safe_convert_to_int(text):
    try:
        return int(text)
    except ValueError:
        return None    # คืนค่า None ถ้าแปลงไม่ได้ แทนที่จะทำให้โปรแกรม crash

print(safe_convert_to_int("42"))     # 42
print(safe_convert_to_int("abc"))    # None
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (try-except พื้นฐาน)")
st.markdown("""
ตัวอย่าง:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("หารด้วยศูนย์ไม่ได้")
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
หารด้วยศูนย์ไม่ได้
```
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex1_copy_basictry",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="หารด้วยศูนย์ไม่ได้",
    hint="ดูตัวอย่างด้านบนแล้วพิมพ์ตามทุกบรรทัด สังเกตการ indent ของโค้ดภายใน try และ except",
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (เก็บ error message ด้วย as)")
st.markdown("""
ตัวอย่าง:
```python
try:
    number = int("hello")
except ValueError as e:
    print("แปลงค่าไม่ได้")
```

ทำตามตัวอย่างนี้เป๊ะ ๆ
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex2_copy_asvar",
    title="", instructions="",
    starter_code=(
        'try:\n'
        '    number = int("hello")\n'
        'except ValueError as e:\n'
        '    print("แปลงค่าไม่ได้")\n'
    ),
    check_type="exact",
    expected_output="แปลงค่าไม่ได้",
    hint="โค้ดนี้พร้อมใช้แล้ว ลองกดรันตามที่ให้มาดูผลลัพธ์",
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — จับ IndexError")
st.markdown("""
เติมโค้ดให้จับ error ตอนเข้าถึง index ที่เกินขนาดของ list
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex3_fill_indexerror",
    title="", instructions="",
    starter_code=(
        'numbers = [1, 2, 3]\n'
        'try:\n'
        '    print(numbers[10])\n'
        '# TODO: เติม except สำหรับ IndexError\n'
        '\n'
        '    print("index เกินขนาด list")\n'
    ),
    check_type="exact",
    expected_output="index เกินขนาด list",
    hint="เติมบรรทัด except IndexError: ให้ตรง indent level เดียวกับ try ด้านบน",
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — จับหลาย exception")
st.markdown("""
เติมโค้ดให้จับทั้ง `ValueError` และ `ZeroDivisionError` แยกข้อความกัน
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex4_fill_multiexcept",
    title="", instructions="",
    starter_code=(
        'text = "0"\n'
        'try:\n'
        '    number = int(text)\n'
        '    result = 100 / number\n'
        '    print(result)\n'
        'except ValueError:\n'
        '    print("กรุณากรอกตัวเลข")\n'
        '# TODO: เติม except สำหรับ ZeroDivisionError พร้อมข้อความ "ห้ามหารด้วยศูนย์"\n'
        '\n'
    ),
    check_type="exact",
    expected_output="ห้ามหารด้วยศูนย์",
    hint='เติม except ZeroDivisionError: แล้วบรรทัดถัดไป print("ห้ามหารด้วยศูนย์") โดย indent ให้ตรงกับ except บรรทัดบน',
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — ใช้ finally")
st.markdown("""
เติมโค้ดให้มีส่วน `finally` ที่พิมพ์ข้อความเสมอ ไม่ว่าจะเกิด error หรือไม่
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex5_fill_finally",
    title="", instructions="",
    starter_code=(
        'try:\n'
        '    result = 10 / 0\n'
        'except ZeroDivisionError:\n'
        '    print("เกิด error")\n'
        '# TODO: เติม finally ที่พิมพ์ "จบการทำงาน"\n'
        '\n'
    ),
    check_type="exact",
    expected_output="เกิด error\nจบการทำงาน",
    hint='เติม finally: แล้วบรรทัดถัดไป print("จบการทำงาน") โดย indent ให้ตรงกับ except ด้านบน',
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — ฟังก์ชันแปลงค่าปลอดภัย")
st.markdown("""
เติมโค้ดในฟังก์ชันให้ดักจับ error ตอนแปลง string เป็น int แล้ว return `None` ถ้าแปลงไม่ได้
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex6_fill_safeconvert",
    title="", instructions="",
    starter_code=(
        'def safe_to_int(text):\n'
        '    try:\n'
        '        return int(text)\n'
        '    # TODO: เติม except ValueError ที่ return None\n'
        '    \n'
        '        \n'
        '\n'
        'print(safe_to_int("42"))\n'
        'print(safe_to_int("abc"))\n'
    ),
    check_type="exact",
    expected_output="42\nNone",
    hint="เติม except ValueError: แล้วบรรทัดถัดไป return None ให้ indent ตรงกับ except",
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — จับ KeyError จาก dictionary")
st.markdown("""
เติมโค้ดให้จับ error เวลาพยายามเข้าถึง key ที่ไม่มีอยู่ใน dictionary แล้วแสดงค่า default แทน
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex7_fill_keyerror",
    title="", instructions="",
    starter_code=(
        'student = {"name": "สมชาย", "age": 20}\n'
        'try:\n'
        '    print(student["gpa"])\n'
        '# TODO: เติม except KeyError ที่พิมพ์ "ไม่พบข้อมูล GPA"\n'
        '\n'
        '    \n'
    ),
    check_type="exact",
    expected_output="ไม่พบข้อมูล GPA",
    hint='เติม except KeyError: แล้วบรรทัดถัดไป print("ไม่พบข้อมูล GPA")',
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — ฟังก์ชันหารปลอดภัย")
st.markdown("""
เขียนฟังก์ชันชื่อ `safe_divide(a, b)` รับตัวเลข 2 ตัว แล้ว return ผลหาร `a / b`
ถ้าหารด้วยศูนย์ ให้ return ค่า `None` แทนที่จะทำให้โปรแกรม crash
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex8_write_safedivide",
    title="", instructions="",
    starter_code="def safe_divide(a, b):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="safe_divide",
    test_cases=[
        {"args": (10, 2), "expected": 5.0, "label": "หารปกติ"},
        {"args": (10, 0), "expected": None, "label": "หารด้วยศูนย์"},
        {"args": (0, 5), "expected": 0.0, "label": "เศษเป็น 0"},
        {"args": (-10, 2), "expected": -5.0, "label": "มีค่าลบ"},
    ],
    hint="ใช้ try ครอบการหาร a/b แล้ว return ผลลัพธ์ ถ้าเกิด ZeroDivisionError ให้ except จับแล้ว return None",
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — ฟังก์ชันแปลงค่าหลายตัวปลอดภัย")
st.markdown("""
เขียนฟังก์ชันชื่อ `safe_sum_strings(text_list)` รับ list ของ string ที่ควรจะแปลงเป็นตัวเลขได้
แล้ว return ผลรวมของค่าที่แปลงได้สำเร็จเท่านั้น (ตัวที่แปลงไม่ได้ให้ข้ามไปเฉย ๆ ไม่ทำให้โปรแกรมล้ม)

ตัวอย่าง: `safe_sum_strings(["10", "abc", "20", "xyz", "5"])` ควร return `35`
(บวกได้แค่ 10 + 20 + 5 ส่วน "abc" กับ "xyz" ข้ามไป)
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex9_write_safesum",
    title="", instructions="",
    starter_code="def safe_sum_strings(text_list):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="safe_sum_strings",
    test_cases=[
        {"args": (["10", "abc", "20", "xyz", "5"],), "expected": 35, "label": "มีค่าแปลงไม่ได้ผสม"},
        {"args": (["1", "2", "3"],), "expected": 6, "label": "แปลงได้ทุกตัว"},
        {"args": (["a", "b", "c"],), "expected": 0, "label": "แปลงไม่ได้เลย"},
        {"args": ([],), "expected": 0, "label": "list ว่าง"},
    ],
    hint="ตั้งตัวแปรสะสมผลรวมเริ่มที่ 0 วนลูปไล่ทีละ string ใน text_list ใช้ try แปลงเป็น int "
         "ถ้าแปลงสำเร็จให้บวกเข้าตัวแปรสะสม ถ้าเกิด ValueError (แปลงไม่ได้) ให้ except จับไว้แล้วข้ามไปต่อ "
         "(ไม่ต้องทำอะไร แค่ไม่บวกเข้าผลรวม) — try/except ต้องอยู่ภายในลูป ไม่ใช่ครอบลูปทั้งหมด",
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — ตรวจสอบช่วงอายุปลอดภัย")
st.markdown("""
เขียนฟังก์ชันชื่อ `validate_age(age_text)` รับค่าอายุที่เป็น string แล้ว return ข้อความ:
- ถ้าแปลงเป็นตัวเลขไม่ได้ → `"ข้อมูลไม่ถูกต้อง"`
- ถ้าแปลงได้แต่อายุติดลบหรือมากกว่า 120 → `"อายุไม่สมเหตุสมผล"`
- ถ้าแปลงได้และอยู่ในช่วงที่สมเหตุสมผล (0-120) → `"ข้อมูลถูกต้อง"`
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex10_write_validateage",
    title="", instructions="",
    starter_code="def validate_age(age_text):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="validate_age",
    test_cases=[
        {"args": ("25",), "expected": "ข้อมูลถูกต้อง", "label": "อายุปกติ"},
        {"args": ("abc",), "expected": "ข้อมูลไม่ถูกต้อง", "label": "แปลงไม่ได้"},
        {"args": ("-5",), "expected": "อายุไม่สมเหตุสมผล", "label": "อายุติดลบ"},
        {"args": ("200",), "expected": "อายุไม่สมเหตุสมผล", "label": "อายุเกิน 120"},
        {"args": ("0",), "expected": "ข้อมูลถูกต้อง", "label": "ขอบเขตพอดี 0"},
        {"args": ("120",), "expected": "ข้อมูลถูกต้อง", "label": "ขอบเขตพอดี 120"},
    ],
    hint="ใช้ try แปลง age_text เป็น int ก่อน ถ้าเกิด ValueError ให้ except จับแล้ว return ข้อความ "
         "'ข้อมูลไม่ถูกต้อง' ทันที ถ้าแปลงสำเร็จ ให้ตรวจสอบช่วงค่าด้วย if-else ตามเงื่อนไขที่กำหนด",
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — ดึงค่าจาก dictionary แบบปลอดภัยหลายชั้น")
st.markdown("""
เขียนฟังก์ชันชื่อ `get_nested_value(data, key1, key2)` รับ dictionary ที่อาจมี dictionary
ซ้อนอยู่ข้างใน (nested dict) พร้อม key 2 ชั้น แล้ว return ค่าที่ `data[key1][key2]`
ถ้าไม่พบ key ใดก็ตามในระหว่างทาง ให้ return `"ไม่พบข้อมูล"` แทนที่จะทำให้โปรแกรม crash

ตัวอย่าง: `get_nested_value({"student": {"name": "สมชาย"}}, "student", "name")`
ควร return `"สมชาย"`
""")

render_exercise(
    lesson_id="lesson07", exercise_id="ex11_write_nestedget",
    title="", instructions="",
    starter_code="def get_nested_value(data, key1, key2):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="get_nested_value",
    test_cases=[
        {"args": ({"student": {"name": "สมชาย"}}, "student", "name"), "expected": "สมชาย", "label": "พบทั้งสอง key"},
        {"args": ({"student": {"name": "สมชาย"}}, "teacher", "name"), "expected": "ไม่พบข้อมูล", "label": "ไม่พบ key1"},
        {"args": ({"student": {"name": "สมชาย"}}, "student", "age"), "expected": "ไม่พบข้อมูล", "label": "ไม่พบ key2"},
    ],
    hint="ใช้ try เข้าถึง data[key1] ก่อน แล้วเข้าถึง [key2] ของผลลัพธ์นั้นต่อ (เขียนต่อกันได้เป็น data[key1][key2]) "
         "ถ้าขั้นใดขั้นหนึ่งเกิด KeyError ให้ except จับแล้ว return ข้อความตามที่กำหนด",
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/6_บทที่6_functions.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/8_บทที่8_built_in_functions.py", label="ไปบทต่อไป: ฟังก์ชันสำเร็จรูปและ Library ➡️")
