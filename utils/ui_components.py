"""
UI components — ฟังก์ชันกลางสำหรับแสดง exercise พร้อม code editor
ให้ทุกบทเรียนเรียกใช้ซ้ำได้ ลดโค้ดซ้ำซ้อน
"""

import streamlit as st
from streamlit_ace import st_ace

from utils.checker import check_exact_output, check_function_with_tests
from utils.lessons import LESSONS_BY_ID, TOTAL_EXERCISES, passed_in_lesson, passed_total
from utils.progress import (
    record_attempt, get_progress, load_progress, flush_pending, progress_status,
    reset_progress_state,
)
from utils.sandbox import run_code
from utils.session import STUDENT_ID_RE, EMAIL_RE, set_login, clear_login


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

    timeout: ค่า default 5 วินาทีพอสำหรับโค้ดทั่วไป แต่ exercise ที่ import pandas/numpy
    ควรตั้งสูงขึ้น (เช่น 10-15)

    การจำโค้ดของนักศึกษา (ลำดับความสำคัญของค่าเริ่มต้นใน editor):
    1) โค้ดที่กำลังพิมพ์อยู่ในเซสชันนี้ (_drafts) เก็บแยกจาก widget state เพราะ Streamlit
       จะลบ widget state ทิ้งเมื่อเปลี่ยนไปหน้าอื่น
    2) โค้ดล่าสุดที่บันทึกไว้ในชีต (ทั้งตอนกดรันและกดตรวจ) จากเซสชัน/อุปกรณ์อื่น
    3) starter_code
    """
    ss = st.session_state
    student_id = ss.get("student_id")
    progress = get_progress() if student_id else {}
    entry = progress.get(exercise_id) or {}
    saved_code = entry.get("code") or ""

    header_col1, header_col2 = st.columns([5, 1])
    with header_col1:
        st.subheader(title)
    with header_col2:
        if entry.get("passed"):
            st.success("✅ ผ่านแล้ว")
        elif entry.get("last_status") == "failed":
            st.warning("🔁 ยังไม่ผ่าน")
        elif saved_code:
            st.info("💾 มีโค้ดที่บันทึกไว้")

    st.markdown(instructions)

    if hint:
        with st.expander("💡 ขอคำใบ้"):
            st.markdown(hint)

    base_key = f"editor_{lesson_id}_{exercise_id}"
    drafts = ss.setdefault("_drafts", {})
    inits = ss.setdefault("_editor_init", {})
    versions = ss.setdefault("_editor_version", {})
    results = ss.setdefault("_results", {})
    editor_key = f"{base_key}_v{versions.get(base_key, 0)}"

    # กำหนดค่าเริ่มต้นเฉพาะตอน editor ถูกสร้างใหม่ (ครั้งแรก หรือกลับมาจากหน้าอื่น)
    # ระหว่างที่ editor ยังแสดงอยู่ ต้องส่งค่าเดิมเสมอ ไม่งั้น editor จะเด้งกลับไปเป็นค่าเก่าขณะพิมพ์
    if editor_key not in ss or editor_key not in inits:
        inits[editor_key] = drafts.get(base_key) or saved_code or starter_code

    code = st_ace(
        value=inits[editor_key],
        language="python",
        theme="github",
        key=editor_key,
        height=height,
        font_size=14,
        show_gutter=True,
        wrap=False,
        auto_update=True,    # ส่งโค้ดให้ server อัตโนมัติขณะพิมพ์ ไม่ต้องกด Ctrl+Enter/APPLY ก่อน
    )
    if code is None:
        code = inits[editor_key]
    drafts[base_key] = code

    col1, col2, col3 = st.columns([1, 1, 3])
    run_clicked = col1.button("▶️ รันโค้ด", key=f"run_{lesson_id}_{exercise_id}")
    check_clicked = col2.button("✅ ตรวจคำตอบ", key=f"check_{lesson_id}_{exercise_id}",
                                type="primary")
    if col3.button("↺ เริ่มใหม่จากโค้ดตั้งต้น", key=f"reset_{lesson_id}_{exercise_id}"):
        versions[base_key] = versions.get(base_key, 0) + 1
        drafts[base_key] = starter_code
        results.pop(base_key, None)
        st.rerun()

    student_email = ss.get("student_email", "")
    student_name = ss.get("student_name", "")

    if run_clicked:
        with st.spinner("กำลังรันโค้ด..."):
            result = run_code(code, timeout=timeout)
        saved = None
        # บันทึกโค้ดเป็น draft เมื่อกดรัน (เฉพาะเมื่อโค้ดเปลี่ยนจากที่บันทึกไว้) ให้กลับมาทำต่อได้
        if student_id and code.strip() and code != saved_code and code.strip() != starter_code.strip():
            saved = record_attempt(student_id, student_email, student_name, lesson_id,
                                   exercise_id, False, code=code, draft=True)
        results[base_key] = {"code": code, "kind": "run", "result": result, "saved": saved}

    if check_clicked:
        if not student_id:
            st.warning("กรุณากรอกรหัสนักศึกษาและอีเมลที่หน้าแรกก่อนเริ่มทำแบบฝึกหัด")
        else:
            with st.spinner("กำลังตรวจคำตอบ..."):
                if check_type == "exact":
                    outcome = check_exact_output(code, expected_output, timeout=timeout)
                else:
                    outcome = check_function_with_tests(code, function_name, test_cases, timeout=timeout)
            saved = record_attempt(student_id, student_email, student_name, lesson_id,
                                   exercise_id, outcome["passed"], code=code)
            results[base_key] = {"code": code, "kind": "check", "outcome": outcome,
                                 "saved": saved, "celebrate": outcome["passed"]}
            # rerun เพื่อให้ badge และแถบความคืบหน้าใน sidebar อัปเดตทันที
            st.rerun()

    # แสดงผลล่าสุดค้างไว้จนกว่าจะแก้โค้ด (auto_update ทำให้หน้ารันใหม่บ่อย ผลลัพธ์จะได้ไม่หาย)
    last = results.get(base_key)
    if last and last["code"] == code:
        if last["kind"] == "run":
            r = last["result"]
            if r["success"]:
                st.code(r["output"] or "(โค้ดรันสำเร็จ แต่ไม่มีผลลัพธ์ที่ print ออกมา)", language="text")
            else:
                st.error(r["error"])
        else:
            o = last["outcome"]
            if o["passed"]:
                st.success(o["message"])
                if last.pop("celebrate", False):
                    st.balloons()
            else:
                st.error(o["message"])
        if last.get("saved") is True:
            st.caption("💾 บันทึกโค้ดแล้ว")
        elif last.get("saved") is False:
            st.caption("⏳ ยังบันทึกลงระบบไม่สำเร็จ ระบบจะลองบันทึกให้ใหม่อัตโนมัติ (ทำต่อได้ตามปกติ)")


def render_student_login():
    """
    แสดงฟอร์มกรอกชื่อ/รหัสนักศึกษา (เรียกใช้ที่หน้าแรกของแอป)
    เก็บไว้ใน session_state และ URL เพื่อให้ refresh/กลับมาแล้วยังล็อกอินอยู่

    รูปแบบรหัสนักศึกษาที่รับ: ตัวเลข 9 หลัก ขีด ตัวเลข 1 หลัก เช่น 663020579-1
    อีเมลต้องเป็นโดเมน @kkumail.com เท่านั้น ส่วนชื่อ-นามสกุลเป็นช่องไม่บังคับ
    ใช้รหัสนักศึกษาเดิมทุกครั้ง ความคืบหน้าที่เคยทำไว้จะกลับมาเอง
    """
    st.markdown("### 👋 เริ่มต้นใช้งาน")
    st.caption("ใช้รหัสนักศึกษาเดิมทุกครั้ง ระบบจะดึงความคืบหน้าและโค้ดที่เคยทำไว้กลับมาให้อัตโนมัติ")
    with st.form("login_form"):
        student_id = st.text_input(
            "รหัสนักศึกษา",
            value=st.session_state.get("student_id", ""),
            placeholder="เช่น 663020579-1",
        )
        student_email = st.text_input(
            "อีเมล KKU",
            value=st.session_state.get("student_email", ""),
            placeholder="เช่น somchai.s@kkumail.com",
        )
        student_name = st.text_input(
            "ชื่อ-นามสกุล (ไม่บังคับ)",
            value=st.session_state.get("student_name", ""),
        )
        submitted = st.form_submit_button("เข้าสู่บทเรียน", type="primary")

        if submitted:
            student_id = student_id.strip()
            student_email = student_email.strip()
            student_name = student_name.strip()

            if not student_id or not student_email:
                st.error("กรุณากรอกทั้งรหัสนักศึกษาและอีเมล KKU (ชื่อ-นามสกุลไม่บังคับ)")
            elif not STUDENT_ID_RE.match(student_id):
                st.error("รูปแบบรหัสนักศึกษาไม่ถูกต้อง ต้องเป็นตัวเลข 9 หลัก ขีด ตัวเลข 1 หลัก "
                         "เช่น 663020579-1")
            elif not EMAIL_RE.match(student_email.lower()):
                st.error("กรุณากรอกอีเมลที่เป็นโดเมน @kkumail.com เท่านั้น เช่น somchai.s@kkumail.com")
            else:
                reset_progress_state()
                set_login(student_id, student_email, student_name)
                with st.spinner("กำลังโหลดความคืบหน้า..."):
                    load_progress(force=True)
                st.rerun()


def render_progress_sidebar(lesson_id: str = None, total_exercises: int = None):
    """
    แสดงความก้าวหน้าของนักศึกษาคนปัจจุบันที่ sidebar

    lesson_id, total_exercises: ถ้าระบุ จะแสดงสรุปว่าทำผ่านไปแล้วกี่ข้อ "ในบทที่เปิดอยู่"
    (ถ้าไม่ส่ง total_exercises จะใช้ค่าจาก utils/lessons.py)
    """
    ss = st.session_state
    student_id = ss.get("student_id")
    if not student_id:
        return

    progress = get_progress()
    status = progress_status()
    sb = st.sidebar

    sb.markdown("---")
    display_name = ss.get("student_name") or ss.get("student_email", "")
    sb.markdown(f"**นักศึกษา:** {display_name}")
    sb.markdown(f"**รหัส:** {student_id}")

    done = passed_total(progress)
    sb.markdown(f"**ทั้งคอร์ส:** ผ่าน {done}/{TOTAL_EXERCISES} ข้อ")
    sb.progress(min(done / TOTAL_EXERCISES, 1.0) if TOTAL_EXERCISES else 0.0)

    if lesson_id:
        total = total_exercises or LESSONS_BY_ID.get(lesson_id, {}).get("total", 0)
        if total:
            in_lesson = passed_in_lesson(progress, lesson_id)
            sb.markdown(f"**บทนี้:** ผ่าน {in_lesson}/{total} ข้อ")
            sb.progress(min(in_lesson / total, 1.0))

    if status["load_error"] and not status["loaded"]:
        sb.warning("⚠️ โหลดความคืบหน้าเดิมจากระบบไม่สำเร็จ (อาจมีผู้ใช้พร้อมกันมาก) "
                   "งานที่ทำตอนนี้ยังถูกบันทึกตามปกติ")
        if sb.button("🔄 โหลดความคืบหน้าอีกครั้ง"):
            load_progress(force=True)
            st.rerun()

    if status["pending"]:
        sb.info(f"⏳ มี {status['pending']} รายการรอบันทึกลงระบบ จะลองใหม่อัตโนมัติ")
        if sb.button("💾 บันทึกตอนนี้"):
            flush_pending(force=True)
            st.rerun()

    sb.caption("💡 เบราว์เซอร์นี้จะจำการเข้าสู่ระบบไว้ กลับมาเปิดแอปจะเข้าสู่ระบบให้อัตโนมัติ "
               "(ถ้าใช้เครื่องส่วนกลาง กดออกจากระบบทุกครั้ง)")

    if sb.button("ออกจากระบบ"):
        flush_pending(force=True)
        clear_login()
        reset_progress_state()
        for key in ("_drafts", "_editor_init", "_editor_version", "_results"):
            ss.pop(key, None)
        st.rerun()
