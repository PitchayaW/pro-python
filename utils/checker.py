"""
Checker — ระบบตรวจคำตอบของนักศึกษา รองรับ 2 แบบ:
1. exact match: เทียบ output (stdout) กับค่าที่กำหนดเป๊ะ ๆ
2. test case: เรียกฟังก์ชันที่นักศึกษาเขียน ด้วย input หลายชุด เทียบ return value
"""

from utils.sandbox import run_code, run_function_test


def check_exact_output(code: str, expected_output: str, timeout: int = 5) -> dict:
    """
    ตรวจแบบ exact match — เทียบสิ่งที่ print ออกมา (ตัด whitespace ท้ายบรรทัด/ท้ายไฟล์)

    Returns:
        dict: {"passed": bool, "message": str}
    """
    result = run_code(code, timeout=timeout)

    if not result["success"]:
        return {"passed": False, "message": f"โค้ดมีข้อผิดพลาด:\n```\n{result['error']}\n```"}

    actual = result["output"].rstrip("\n")
    expected = expected_output.rstrip("\n")

    if actual == expected:
        return {"passed": True, "message": "ถูกต้อง! ✅"}

    return {
        "passed": False,
        "message": (
            f"ผลลัพธ์ยังไม่ตรง\n\n"
            f"**ที่ควรได้:**\n```\n{expected}\n```\n\n"
            f"**ที่ได้จริง:**\n```\n{actual}\n```"
        ),
    }


def check_function_with_tests(
    code: str,
    function_name: str,
    test_cases: list,
    timeout: int = 5,
) -> dict:
    """
    ตรวจแบบ test case — เรียกฟังก์ชันที่ผู้ใช้เขียน ด้วย input หลายชุด เทียบผลลัพธ์

    Args:
        code: โค้ดที่ผู้ใช้เขียน (ต้องมี def function_name(...) อยู่ในนั้น)
        function_name: ชื่อฟังก์ชันที่จะเรียกทดสอบ
        test_cases: list ของ dict เช่น
            [{"args": (1, 2), "expected": 3, "label": "บวกเลขบวก"}]

    Returns:
        dict: {"passed": bool, "message": str, "results": list}
    """
    # เช็ค syntax error ของโค้ดก่อน (รันเปล่า ๆ โดยไม่เรียกฟังก์ชัน) เพื่อให้ error message ชัดเจน
    pre_check = run_code(code, timeout=timeout)
    if not pre_check["success"]:
        return {
            "passed": False,
            "message": f"โค้ดมีข้อผิดพลาดก่อนถึงขั้นทดสอบ:\n```\n{pre_check['error']}\n```",
            "results": [],
        }

    test_results = []
    all_passed = True

    for i, case in enumerate(test_cases, start=1):
        args = case.get("args", ())
        kwargs = case.get("kwargs", {})
        expected = case["expected"]
        label = case.get("label", f"กรณีทดสอบที่ {i}")

        outcome = run_function_test(code, function_name, args, kwargs, timeout=timeout)

        if not outcome["success"]:
            test_results.append({
                "label": label, "passed": False, "args": args,
                "expected": expected, "actual": None, "error": outcome["error"],
            })
            all_passed = False
            continue

        actual = outcome["return_value"]
        passed = actual == expected
        test_results.append({
            "label": label, "passed": passed, "args": args,
            "expected": expected, "actual": actual, "error": None,
        })
        if not passed:
            all_passed = False

    passed_count = sum(1 for r in test_results if r["passed"])
    total_count = len(test_results)

    message_lines = [f"ผ่าน {passed_count}/{total_count} กรณีทดสอบ\n"]
    for r in test_results:
        icon = "✅" if r["passed"] else "❌"
        if r["error"]:
            message_lines.append(f"{icon} {r['label']}: เกิด error — {r['error']}")
        else:
            message_lines.append(
                f"{icon} {r['label']}: ใส่ {r['args']} → ได้ `{r['actual']}` "
                f"(ควรได้ `{r['expected']}`)"
            )

    return {"passed": all_passed, "message": "\n".join(message_lines), "results": test_results}
