"""บทที่ 9: NumPy และ Linear Algebra เบื้องต้น"""

import streamlit as st
from utils.ui_components import render_progress_sidebar, render_exercise

if "student_id" not in st.session_state:
    st.warning("กรุณาเข้าสู่ระบบที่หน้าแรกก่อน")
    st.stop()

render_progress_sidebar(lesson_id="lesson09", total_exercises=11)

st.title("บทที่ 9: NumPy และ Linear Algebra เบื้องต้น")

st.markdown("""
### รู้จัก NumPy array

NumPy เป็น library สำหรับคำนวณเชิงตัวเลขที่เร็วกว่า list ธรรมดามาก เป็นพื้นฐานสำคัญ
ของ pandas และ library ML/Data Science ทั้งหมดที่จะเรียนต่อไป

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr)            # [1 2 3 4 5]
print(type(arr))       # <class 'numpy.ndarray'>
print(arr.shape)        # (5,)  — ขนาดของ array (5 แถว)
```

ข้อแตกต่างสำคัญจาก list ธรรมดา: การคำนวณกับ NumPy array ทำกับสมาชิกทุกตัวพร้อมกัน
(element-wise) โดยไม่ต้องวนลูป

```python
arr = np.array([1, 2, 3])
print(arr * 2)          # [2 4 6]   — คูณทุกตัวพร้อมกัน
print(arr + 10)          # [11 12 13]
print(arr + arr)         # [2 4 6]   — บวกแบบ element-wise

# เทียบกับ list ธรรมดา arr * 2 จะได้ [1,2,3,1,2,3] (ต่อ list ซ้ำ ไม่ใช่คูณ)
```

### สร้างและจัดการ Matrix (2D array)

Matrix คือ array 2 มิติ เหมือน 2D list ที่เรียนไปในบทก่อน แต่ NumPy คำนวณได้สะดวกกว่ามาก

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
print(matrix.shape)     # (2, 3)  — 2 แถว 3 คอลัมน์
print(matrix[0, 1])      # 2       — แถว 0 คอลัมน์ 1 (ใช้ comma แทนวงเล็บซ้อน)
print(matrix[0])          # [1 2 3] — แถวที่ 0 ทั้งแถว

# สร้าง matrix พิเศษที่ใช้บ่อย
zeros = np.zeros((2, 3))      # matrix ศูนย์ 2x3
ones = np.ones((3, 3))         # matrix หนึ่ง 3x3
identity = np.eye(3)            # identity matrix 3x3 (เส้นทแยงมุมเป็น 1)
```

### การคำนวณเชิงเส้นเบื้องต้น (Linear Algebra)

**Transpose** — สลับแถวกับคอลัมน์

```python
matrix = np.array([[1, 2], [3, 4]])
print(matrix.T)          # [[1, 3], [2, 4]]
```

**Matrix multiplication** — การคูณ matrix (ต่างจากการคูณ element-wise)

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(a * b)              # [[5, 12], [21, 32]]    — element-wise (คูณตำแหน่งต่อตำแหน่ง)
print(np.dot(a, b))       # [[19, 22], [43, 50]]    — matrix multiplication จริง
print(a @ b)               # [[19, 22], [43, 50]]    — เครื่องหมาย @ ทำแบบเดียวกับ np.dot
```

**ข้อควรระวัง:** เมื่อ print NumPy array/matrix ที่มีตัวเลขจำนวนหลักไม่เท่ากัน (เช่นมีทั้งเลข
หลักเดียวและสองหลักผสมกัน) NumPy จะเติมช่องว่างให้ตัวเลขชิดขวาเรียงสวยงามอัตโนมัติ
เช่น `[[ 4  4]\\n [10  8]]` (สังเกตช่องว่างก่อนเลข 4 ตัวแรก เพราะมีเลข 10 อยู่ในชุดเดียวกัน)
ถ้าทำ exercise ที่ตรวจคำตอบแบบ exact match แล้วได้ผลลัพธ์ถูกต้องเชิงตัวเลขแต่ระบบบอกว่าผิด
ลองตรวจสอบช่องว่างในผลลัพธ์ให้ตรงกับที่ระบบคาดไว้เป๊ะ ๆ ก่อน

**Determinant และ Inverse** — ใช้ตรวจสอบและแก้ระบบสมการเชิงเส้น

```python
matrix = np.array([[4, 7], [2, 6]])
print(np.linalg.det(matrix))      # 10.0  — ค่า determinant
print(np.linalg.inv(matrix))       # matrix ผกผัน (inverse)
```

### การประยุกต์ใช้ในงาน Data Science

NumPy ใช้เป็นพื้นฐานคำนวณทางสถิติเบื้องต้นได้สะดวก

```python
data = np.array([85, 90, 78, 92, 88])
print(np.mean(data))     # ค่าเฉลี่ย
print(np.std(data))       # ส่วนเบี่ยงเบนมาตรฐาน
print(np.max(data))       # ค่ามากสุด
print(np.sum(data))       # ผลรวม
```
""")

st.markdown("---")
st.markdown("## 📝 แบบฝึกหัด")
st.caption("ข้อ 1-2 ทำตามตัวอย่างให้ครบ | ข้อ 3-7 เติมโค้ดในจุดที่ขาด | ข้อ 8-11 เขียนเองทั้งหมด")
st.info("💡 บทนี้ใช้ NumPy ซึ่งโหลดช้ากว่าโค้ดทั่วไปเล็กน้อย ถ้ารันแล้วรอสักครู่ถือว่าปกติ")

# ============================================================
# ข้อ 1-2: ทำซ้ำเต็มจากตัวอย่าง
# ============================================================

st.markdown("### ข้อ 1: พิมพ์ตามตัวอย่าง (NumPy array พื้นฐาน)")
st.markdown("""
ตัวอย่าง:
```python
import numpy as np

arr = np.array([10, 20, 30])
print(arr)
print(arr * 2)
```

พิมพ์ตามตัวอย่างนี้เป๊ะ ๆ ให้ได้ผลลัพธ์:
```
[10 20 30]
[20 40 60]
```
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex1_copy_basicnumpy",
    title="", instructions="",
    starter_code="# พิมพ์โค้ดตามตัวอย่างด้านบนที่นี่\n",
    check_type="exact",
    expected_output="[10 20 30]\n[20 40 60]",
    hint="ดูตัวอย่างด้านบน สังเกตว่า NumPy array ไม่มี comma คั่นตอน print (ต่างจาก list ปกติ)",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 2: พิมพ์ตามตัวอย่าง (Matrix shape)")
st.markdown("""
ตัวอย่าง:
```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.shape)
print(matrix[1, 2])
```

ทำตามตัวอย่างนี้เป๊ะ ๆ
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex2_copy_matrixshape",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        'matrix = np.array([[1, 2, 3], [4, 5, 6]])\n'
        'print(matrix.shape)\n'
        'print(matrix[1, 2])\n'
    ),
    check_type="exact",
    expected_output="(2, 3)\n6",
    hint="โค้ดนี้พร้อมใช้แล้ว ลองกดรันตามที่ให้มาดูผลลัพธ์ matrix[1, 2] หมายถึงแถวที่ 1 คอลัมน์ที่ 2",
    timeout=15,
)

# ============================================================
# ข้อ 3-7: fill-in-the-blank
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 3: เติมโค้ดให้สมบูรณ์ — สร้าง array และคำนวณ")
st.markdown("""
เติมโค้ดให้สร้าง NumPy array จาก list แล้วบวกค่า 5 เข้าทุกสมาชิก
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex3_fill_createarray",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        'numbers = [1, 2, 3, 4]\n'
        '# TODO: แปลง numbers เป็น numpy array เก็บในตัวแปร arr\n'
        'arr = \n'
        'result = arr + 5\n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="[6 7 8 9]",
    hint="ใช้ np.array(numbers) แปลง list เป็น numpy array",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 4: เติมโค้ดให้สมบูรณ์ — Transpose matrix")
st.markdown("""
เติมโค้ดให้สลับแถวกับคอลัมน์ของ matrix (transpose)
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex4_fill_transpose",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        'matrix = np.array([[1, 2], [3, 4], [5, 6]])\n'
        '# TODO: สลับแถวกับคอลัมน์ เก็บในตัวแปร transposed\n'
        'transposed = \n'
        'print(transposed.shape)\n'
    ),
    check_type="exact",
    expected_output="(2, 3)",
    hint="ใช้ matrix.T เพื่อ transpose — สังเกตว่า shape เดิมคือ (3,2) ต้องกลายเป็น (2,3) หลัง transpose",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 5: เติมโค้ดให้สมบูรณ์ — Matrix multiplication")
st.markdown("""
เติมโค้ดให้คูณ matrix สองตัวด้วยวิธี matrix multiplication (ไม่ใช่ element-wise)
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex5_fill_matmul",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        'a = np.array([[1, 2], [3, 4]])\n'
        'b = np.array([[2, 0], [1, 2]])\n'
        '# TODO: คูณ matrix a กับ b แบบ matrix multiplication เก็บในตัวแปร result\n'
        'result = \n'
        'print(result)\n'
    ),
    check_type="exact",
    expected_output="[[ 4  4]\n [10  8]]",
    hint="ใช้ np.dot(a, b) หรือ a @ b (ไม่ใช่ a * b ซึ่งเป็น element-wise)",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 6: เติมโค้ดให้สมบูรณ์ — สถิติเบื้องต้นด้วย NumPy")
st.markdown("""
เติมโค้ดให้คำนวณค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐานของข้อมูล
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex6_fill_stats",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        'data = np.array([10, 20, 30, 40, 50])\n'
        '# TODO: คำนวณค่าเฉลี่ย เก็บในตัวแปร avg\n'
        'avg = \n'
        'print(avg)\n'
    ),
    check_type="exact",
    expected_output="30.0",
    hint="ใช้ np.mean(data) คำนวณค่าเฉลี่ย",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 7: เติมโค้ดให้สมบูรณ์ — สร้าง identity matrix")
st.markdown("""
เติมโค้ดให้สร้าง identity matrix ขนาด 3x3 (เส้นทแยงมุมเป็น 1 ที่เหลือเป็น 0)
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex7_fill_identity",
    title="", instructions="",
    starter_code=(
        'import numpy as np\n'
        '\n'
        '# TODO: สร้าง identity matrix ขนาด 3x3 เก็บในตัวแปร identity_matrix\n'
        'identity_matrix = \n'
        'print(identity_matrix)\n'
    ),
    check_type="exact",
    expected_output="[[1. 0. 0.]\n [0. 1. 0.]\n [0. 0. 1.]]",
    hint="ใช้ np.eye(3) สร้าง identity matrix ขนาด 3x3",
    timeout=15,
)

# ============================================================
# ข้อ 8-11: เขียนเองทั้งหมด
# ============================================================

st.markdown("---")
st.markdown("### ข้อ 8: เขียนเอง — คำนวณ Dot Product ของ vector")
st.markdown("""
เขียนฟังก์ชันชื่อ `dot_product(v1, v2)` รับ list ของตัวเลข 2 ชุด (แทน vector)
ที่มีความยาวเท่ากัน แล้ว return ค่า dot product (ผลรวมของผลคูณแต่ละตำแหน่ง)

ตัวอย่าง: `dot_product([1, 2, 3], [4, 5, 6])` ควร return `32`
(1×4 + 2×5 + 3×6 = 4 + 10 + 18 = 32)

**แนวทาง:** ใช้ NumPy แปลง list เป็น array ก่อน แล้วใช้ฟังก์ชันคำนวณ dot product ที่เรียนไป
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex8_write_dotproduct",
    title="", instructions="",
    starter_code="import numpy as np\n\ndef dot_product(v1, v2):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="dot_product",
    test_cases=[
        {"args": ([1, 2, 3], [4, 5, 6]), "expected": 32, "label": "vector 3 มิติ"},
        {"args": ([1, 0], [0, 1]), "expected": 0, "label": "vector ตั้งฉาก"},
        {"args": ([2, 2], [2, 2]), "expected": 8, "label": "vector เหมือนกัน"},
    ],
    hint="แปลง v1, v2 เป็น np.array ก่อน แล้วใช้ np.dot(arr1, arr2) — ผลลัพธ์ที่ได้อาจเป็น numpy "
         "type ซึ่งระบบจะแปลงให้เป็น native type ให้อัตโนมัติ ไม่ต้องแปลงเองก็ได้",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 9: เขียนเอง — คำนวณ Determinant ของ matrix 2x2")
st.markdown("""
เขียนฟังก์ชันชื่อ `matrix_determinant(matrix)` รับ 2D list ขนาด 2x2 แล้ว return
ค่า determinant ปัดทศนิยม 2 ตำแหน่ง
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex9_write_determinant",
    title="", instructions="",
    starter_code="import numpy as np\n\ndef matrix_determinant(matrix):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="matrix_determinant",
    test_cases=[
        {"args": ([[4, 7], [2, 6]],), "expected": 10.0, "label": "det([[4,7],[2,6]]) = 10"},
        {"args": ([[1, 0], [0, 1]],), "expected": 1.0, "label": "det ของ identity matrix = 1"},
        {"args": ([[2, 0], [0, 2]],), "expected": 4.0, "label": "det([[2,0],[0,2]]) = 4"},
    ],
    hint="แปลง matrix เป็น np.array ก่อน แล้วใช้ np.linalg.det(arr) คำนวณ determinant "
         "อย่าลืมครอบด้วย round(..., 2) ก่อน return",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 10: เขียนเอง — ผลรวมแต่ละคอลัมน์ใน Matrix")
st.markdown("""
เขียนฟังก์ชันชื่อ `column_sums(matrix)` รับ 2D list (matrix) แล้ว return list ของ
ผลรวมแต่ละคอลัมน์ (ตรงข้ามกับ `row_sums` ที่เคยเขียนในบท Data Structure ซึ่งหาผลรวม
แต่ละแถว)

ตัวอย่าง: `column_sums([[1, 2, 3], [4, 5, 6]])` ควร return `[5, 7, 9]`
(คอลัมน์ 0: 1+4=5, คอลัมน์ 1: 2+5=7, คอลัมน์ 2: 3+6=9)
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex10_write_columnsums",
    title="", instructions="",
    starter_code="import numpy as np\n\ndef column_sums(matrix):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="column_sums",
    test_cases=[
        {"args": ([[1, 2, 3], [4, 5, 6]],), "expected": [5, 7, 9], "label": "matrix 2x3"},
        {"args": ([[1, 1], [2, 2], [3, 3]],), "expected": [6, 6], "label": "matrix 3x2"},
        {"args": ([[10], [20], [30]],), "expected": [60], "label": "matrix 3x1"},
    ],
    hint="แปลง matrix เป็น np.array ก่อน แล้วใช้ np.sum() พร้อมระบุ axis=0 เพื่อรวมตามแนวคอลัมน์ "
         "(axis=0 คือรวมข้ามแถว ได้ผลรวมต่อคอลัมน์ ส่วน axis=1 จะรวมต่อแถวแทน) "
         "ผลลัพธ์ที่ได้เป็น numpy array ต้องแปลงเป็น list ก่อน return ด้วย .tolist()",
    timeout=15,
)

st.markdown("---")
st.markdown("### ข้อ 11: เขียนเอง — แก้ระบบสมการเชิงเส้น")
st.markdown("""
เขียนฟังก์ชันชื่อ `solve_linear_system(a_matrix, b_vector)` รับ matrix สัมประสิทธิ์
`a_matrix` (2D list) และ vector ค่าคงที่ `b_vector` (list) ของระบบสมการเชิงเส้น
`Ax = b` แล้ว return ค่า `x` ที่แก้สมการได้ (เป็น list ปัดทศนิยม 2 ตำแหน่งทุกค่า)

ตัวอย่าง: ระบบสมการ `2x + y = 5` และ `x + 3y = 10` เขียนเป็น matrix ได้เป็น
`a_matrix = [[2, 1], [1, 3]]`, `b_vector = [5, 10]` ซึ่งคำตอบคือ `x=1, y=3`

**แนวทาง:** NumPy มีฟังก์ชันสำเร็จรูปสำหรับแก้ระบบสมการเชิงเส้นแบบนี้โดยตรง
ลองค้นดูในกลุ่มฟังก์ชัน `np.linalg`
""")

render_exercise(
    lesson_id="lesson09", exercise_id="ex11_write_linearsystem",
    title="", instructions="",
    starter_code="import numpy as np\n\ndef solve_linear_system(a_matrix, b_vector):\n    # เขียนโค้ดของคุณที่นี่\n    pass\n",
    check_type="function",
    function_name="solve_linear_system",
    test_cases=[
        {"args": ([[2, 1], [1, 3]], [5, 10]), "expected": [1.0, 3.0], "label": "ระบบสมการ 2 ตัวแปร"},
        {"args": ([[1, 0], [0, 1]], [7, 9]), "expected": [7.0, 9.0], "label": "identity matrix"},
        {"args": ([[3, 0], [0, 2]], [9, 8]), "expected": [3.0, 4.0], "label": "diagonal matrix"},
    ],
    hint="แปลง a_matrix และ b_vector เป็น np.array ก่อน แล้วใช้ np.linalg.solve(a, b) "
         "ฟังก์ชันนี้แก้ระบบสมการ Ax=b ให้โดยตรง ผลลัพธ์ที่ได้เป็น numpy array "
         "ต้องปัดทศนิยมและแปลงเป็น list ก่อน return (ลองใช้ np.round() ก่อน .tolist())",
    timeout=15,
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/8_บทที่8_built_in_functions.py", label="⬅️ บทก่อนหน้า")
with col2:
    st.page_link("pages/10_บทที่10_อ่านข้อมูล.py", label="ไปบทต่อไป: อ่านและสำรวจข้อมูล ➡️")
