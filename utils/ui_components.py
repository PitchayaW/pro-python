"""
UI components — ฟังก์ชันกลางสำหรับแสดง exercise พร้อม code editor
ให้ทุกบทเรียนเรียกใช้ซ้ำได้ ลดโค้ดซ้ำซ้อน
"""

import re

import streamlit as st
from streamlit_ace import st_ace

from utils.checker import check_exact_output, check_function_with_tests
from utils.sandbox import run_code
from utils.progress import record_attempt, get_student_progress


def render_exercise(
    lesson_id: str,
    exercise_id: str,
    title: str,
    instructions: str,
    starter_code: str,
    check_type: str = "exact",          # "exact" หรือ "function"
    expected_output: str = None,         # ใช้ตอน check_type == "exact"
    function_name: str = None,           # ใช้ตอน check_type == "function"
    test_cases: list = None,             # ใช้ตอน check_type == "function"
    hint: str = None,
    height: int = 220,
    timeout: int = 5,                    # เพิ่มได้สำหรับ exercise ที่ใช้ library หนัก (pandas/numpy)
):
    """
    แสดง exercise 1 ข้อ พร้อม code editor, ปุ่มรัน, ปุ่มตรวจคำตอบ, และบันทึก progress

    เรียกใช้จากแต่ละไฟล์บทเรียนได้ตรง ๆ — ไม่ต้องเขียน UI ซ้ำทุกข้อ

    timeout: ค่า default 5 วินาทีพอสำหรับโค้ดทั่วไป แต่ exercise ที่ import pandas/numpy
    ควรตั้งสูงขึ้น (เช่น 10-15) เพราะการ import library หนักในแต่ละ subprocess ใหม่
    กินเวลามากกว่าโค้ดเปล่า ๆ โดยเฉพาะเมื่อมีคนใช้พร้อมกันหลายคนบน server ที่ resource จำกัด

    ถ้านักศึกษาเคยทำข้อนี้ผ่านมาก่อน (เช็คจาก Google Sheet ผ่าน get_student_progress)
    จะแสดง badge "ผ่านแล้ว" และดึงโค้ดที่ส่งตรวจครั้งล่าสุดมาเป็นค่าเริ่มต้นใน editor
    แทน starter_code เปล่า ๆ — ช่วยให้กลับมาทำต่อได้โดยไม่ต้องเริ่มใหม่จากศูนย์
    """
    student_id = st.session_state.get("student_id")
    previous_status = None
    previous_code = None
    if student_id:
        progress = get_student_progress(student_id)
        entry = progress.get(exercise_id)
        if entry:
            previous_status = entry.get("status")
            previous_code = entry.get("code")

    header_col1, header_col2 = st.columns([5, 1])
    with header_col1:
        st.subheader(title)
    with header_col2:
        if previous_status == "passed":
            st.success("✅ ผ่านแล้ว")

    st.markdown(instructions)

    if hint:
        with st.expander("💡 ขอคำใบ้"):
            st.markdown(hint)

    editor_key = f"editor_{lesson_id}_{exercise_id}"
    # ลำดับความสำคัญของค่าเริ่มต้นใน editor:
    # 1) ค่าที่อยู่ใน session_state อยู่แล้ว (กำลังพิมพ์อยู่ในเซสชันนี้ ไม่อยากให้ถูกเขียนทับ)
    # 2) โค้ดที่ส่งตรวจไว้ล่าสุดจาก Google Sheet (ถ้าเคยทำมาก่อนในเซสชันอื่น/อุปกรณ์อื่น)
    # 3) starter_code เปล่า (ยังไม่เคยทำข้อนี้มาก่อน)
    if editor_key in st.session_state:
        default_code = st.session_state[editor_key]
    elif previous_code:
        default_code = previous_code
    else:
        default_code = starter_code

    code = st_ace(
        value=default_code,
        language="python",
        theme="github",
        key=editor_key,
        height=height,
        font_size=14,
        show_gutter=True,
        wrap=False,
        auto_update=False,
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    run_clicked = col1.button("▶️ รันโค้ด", key=f"run_{lesson_id}_{exercise_id}")
    check_clicked = col2.button("✅ ตรวจคำตอบ", key=f"check_{lesson_id}_{exercise_id}",
                                  type="primary")

    result_area = st.container()

    if run_clicked:
        with st.spinner("กำลังรันโค้ด..."):
            result = run_code(code, timeout=timeout)
        with result_area:
            if result["success"]:
                st.code(result["output"] or "(โค้ดรันสำเร็จ แต่ไม่มีผลลัพธ์ที่ print ออกมา)",
                         language="text")
            else:
                st.error(result["error"])

    if check_clicked:
        student_name = st.session_state.get("student_name")

        if not student_id:
            st.warning("กรุณากรอกชื่อ-รหัสนักศึกษาที่หน้าแรกก่อนเริ่มทำแบบฝึกหัด")
        else:
            with st.spinner("กำลังตรวจคำตอบ..."):
                if check_type == "exact":
                    outcome = check_exact_output(code, expected_output, timeout=timeout)
                else:
                    outcome = check_function_with_tests(code, function_name, test_cases, timeout=timeout)

            with result_area:
                if outcome["passed"]:
                    st.success(outcome["message"])
                    st.balloons()
                else:
                    st.error(outcome["message"])

            record_attempt(student_id, student_name, lesson_id, exercise_id,
                            outcome["passed"], code=code)
            get_student_progress.clear()  # เคลียร์ cache ให้เห็น progress ล่าสุด


def render_student_login():
    """
    แสดงฟอร์มกรอกชื่อ/รหัสนักศึกษา (เรียกใช้ที่หน้าแรกของแอป)
    เก็บไว้ใน session_state เพื่อใช้ระบุตัวตนตอนบันทึกคะแนน

    รูปแบบรหัสนักศึกษาที่รับ: ตัวเลข 9 หลัก ขีด ตัวเลข 1 หลัก เช่น 663020579-1
    """
    st.markdown("### 👋 เริ่มต้นใช้งาน")
    with st.form("login_form"):
        student_id = st.text_input(
            "รหัสนักศึกษา",
            value=st.session_state.get("student_id", ""),
            placeholder="เช่น 663020579-1",
        )
        student_name = st.text_input("ชื่อ-นามสกุล", value=st.session_state.get("student_name", ""))
        submitted = st.form_submit_button("เข้าสู่บทเรียน", type="primary")

        if submitted:
            student_id = student_id.strip()
            if not student_id or not student_name:
                st.error("กรุณากรอกทั้งรหัสนักศึกษาและชื่อ-นามสกุล")
            elif not re.match(r"^\d{9}-\d$", student_id):
                st.error("รูปแบบรหัสนักศึกษาไม่ถูกต้อง ต้องเป็นตัวเลข 9 หลัก ขีด ตัวเลข 1 หลัก "
                          "เช่น 663020579-1")
            else:
                st.session_state["student_id"] = student_id
                st.session_state["student_name"] = student_name.strip()
                st.success(f"ยินดีต้อนรับ {student_name} 🎉")
                st.rerun()


def render_progress_sidebar(lesson_id: str = None, total_exercises: int = None):
    """
    แสดงความก้าวหน้าของนักศึกษาคนปัจจุบันที่ sidebar

    lesson_id, total_exercises: ถ้าระบุทั้งสองค่า จะแสดงสรุปเพิ่มเติมว่าทำผ่านไปแล้ว
    กี่ข้อจากทั้งหมดกี่ข้อ "ในบทที่เปิดอยู่ขณะนี้" (เช่น "บทนี้: 5/9 ข้อ")
    เรียกจากแต่ละไฟล์บทเรียนโดยส่ง lesson_id ของบทนั้นและจำนวนข้อทั้งหมดในบทมาด้วย
    """
    student_id = st.session_state.get("student_id")
    if not student_id:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**นักศึกษา:** {st.session_state.get('student_name', '')}")
    st.sidebar.markdown(f"**รหัส:** {student_id}")

    progress = get_student_progress(student_id)
    passed_count = sum(1 for entry in progress.values() if entry.get("status") == "passed")

    if progress:
        st.sidebar.markdown(f"**ผ่านแล้วทั้งคอร์ส:** {passed_count} แบบฝึกหัด")

    if lesson_id and total_exercises:
        passed_in_lesson = sum(
            1 for entry in progress.values()
            if entry.get("status") == "passed" and entry.get("lesson_id") == lesson_id
        )
        st.sidebar.markdown(f"**บทนี้:** {passed_in_lesson}/{total_exercises} ข้อ")
        st.sidebar.progress(passed_in_lesson / total_exercises if total_exercises else 0)

    if st.sidebar.button("ออกจากระบบ"):
        for key in ("student_id", "student_name"):
            st.session_state.pop(key, None)
        st.rerun()
