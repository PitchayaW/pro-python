"""
Sandbox executor — รันโค้ด Python ที่ผู้ใช้พิมพ์เองอย่างปลอดภัย

วิธีการ: ตรวจสอบโค้ดด้วย AST (Abstract Syntax Tree) ก่อนรันเสมอ
ปฏิเสธโค้ดที่มีการ import โมดูลที่ไม่อนุญาต หรือเรียกใช้ฟังก์ชันอันตราย
(เช่น exec, eval, open, __import__) ตั้งแต่ขั้น parse — ไม่รอให้รันแล้วค่อยบล็อก
เพราะการ override __builtins__ หลังจากนั้นไม่ครอบคลุม exec/eval ที่ผูกกับ
interpreter โดยตรงเมื่อรันเป็นไฟล์สคริปต์ (ทดสอบแล้วว่า reassignment ไม่พอ)

จากนั้นรันด้วย subprocess จริง (ไม่ใช่ multiprocessing) เพื่อให้ kill ได้ตรงเวลา
ตอน timeout และไม่ติดปัญหา pickle function ที่ exec มา
"""

import ast
import json
import subprocess
import sys
import tempfile
import os


SAFE_MODULES = {"math", "random", "statistics", "datetime", "re", "json",
                 "pandas", "numpy", "matplotlib", "matplotlib.pyplot"}

# ชื่อฟังก์ชัน/built-in ที่ไม่อนุญาตให้เรียกใช้ในโค้ดนักศึกษาเด็ดขาด
BLOCKED_CALLS = {
    "exec", "eval", "compile", "__import__", "open", "input",
    "globals", "locals", "vars", "getattr", "setattr", "delattr",
    "exit", "quit", "help", "memoryview", "breakpoint",
}

# attribute ที่อันตรายถ้าถูกเข้าถึง (หลีกเลี่ยงการลอบใช้ผ่าน object introspection)
BLOCKED_ATTRIBUTES = {
    "__import__", "__subclasses__", "__bases__", "__globals__",
    "__builtins__", "__loader__", "__code__",
}


class _SecurityValidator(ast.NodeVisitor):
    """เดินผ่าน AST ของโค้ดผู้ใช้ เก็บรายการปัญหาด้านความปลอดภัยที่พบ"""

    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module not in {m.split(".")[0] for m in SAFE_MODULES}:
                self.violations.append(f"ไม่อนุญาตให้ import โมดูล '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        base_module = module.split(".")[0]
        if base_module not in {m.split(".")[0] for m in SAFE_MODULES}:
            self.violations.append(f"ไม่อนุญาตให้ import จากโมดูล '{module}'")
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Name) and func.id in BLOCKED_CALLS:
            self.violations.append(f"ไม่อนุญาตให้เรียกใช้ฟังก์ชัน '{func.id}'")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr in BLOCKED_ATTRIBUTES:
            self.violations.append(f"ไม่อนุญาตให้เข้าถึง attribute '{node.attr}'")
        self.generic_visit(node)

    def visit_Name(self, node):
        # กันการอ้างชื่อ dunder อันตรายตรง ๆ เช่น __builtins__
        if node.id in BLOCKED_ATTRIBUTES:
            self.violations.append(f"ไม่อนุญาตให้ใช้ชื่อ '{node.id}'")
        self.generic_visit(node)


def validate_code(code: str) -> dict:
    """
    ตรวจสอบโค้ดด้วย AST ก่อนรัน แยกกรณี syntax error ออกจาก security violation
    เพื่อให้แสดงข้อความที่ตรงประเด็นกับนักศึกษา (syntax ผิด ≠ โค้ดอันตราย)

    Returns:
        dict: {"ok": bool, "syntax_error": str|None, "security_violations": list}
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"ok": False, "syntax_error": str(e), "security_violations": []}

    validator = _SecurityValidator()
    validator.visit(tree)
    return {
        "ok": len(validator.violations) == 0,
        "syntax_error": None,
        "security_violations": validator.violations,
    }


def _validation_error_message(validation: dict) -> str:
    """แปลงผลตรวจสอบ (ที่ไม่ผ่าน) เป็นข้อความที่อ่านง่ายสำหรับนักศึกษา"""
    if validation["syntax_error"]:
        return f"โค้ดมี syntax ผิดพลาด: {validation['syntax_error']}\n(ตรวจสอบว่าเขียนโค้ดครบทุกจุด ไม่มีส่วนที่ขาดหายหรือพิมพ์ผิด)"
    return "พบโค้ดที่ไม่อนุญาตในบทเรียนนี้:\n- " + "\n- ".join(validation["security_violations"])


def _write_temp_script(content: str) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(content)
        return f.name


def _run_script(script_content: str, timeout: int):
    """รันสคริปต์ผ่าน subprocess จริง คืนค่า (success, stdout, stderr, timed_out)"""
    script_path = _write_temp_script(script_content)
    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode == 0, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired:
        return False, "", "", True
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


def run_code(code: str, timeout: int = 5) -> dict:
    """
    ตรวจสอบความปลอดภัยของโค้ดด้วย AST ก่อน แล้วรันผ่าน subprocess จริง

    Returns:
        dict: {"success": bool, "output": str, "error": str|None}
    """
    validation = validate_code(code)
    if not validation["ok"]:
        return {"success": False, "output": "", "error": _validation_error_message(validation)}

    ok, stdout, stderr, timed_out = _run_script(code, timeout)

    if timed_out:
        return {
            "success": False,
            "output": "",
            "error": f"โค้ดรันนานเกิน {timeout} วินาที (อาจมีลูปไม่สิ้นสุด) — ลองตรวจสอบเงื่อนไขการหยุดลูป",
        }

    if not ok:
        return {"success": False, "output": "", "error": stderr.strip()}

    return {"success": True, "output": stdout, "error": None}


def run_function_test(code: str, function_name: str, args: tuple, kwargs: dict = None,
                        timeout: int = 5) -> dict:
    """
    ตรวจสอบความปลอดภัยของโค้ดด้วย AST ก่อน แล้วรันโค้ดผู้ใช้ (ที่มี def function_name)
    พร้อมเรียกฟังก์ชันนั้นด้วย args/kwargs ที่กำหนด ภายใน subprocess เดียวกัน
    (จำเป็นต้องเรียกในกระบวนการเดียวกัน เพราะ function ที่ exec มาส่งข้าม process ไม่ได้)

    Returns:
        dict: {"success": bool, "return_value": Any, "error": str|None}
    """
    validation = validate_code(code)
    if not validation["ok"]:
        return {
            "success": False,
            "return_value": None,
            "error": _validation_error_message(validation),
        }

    kwargs = kwargs or {}
    call_block = f"""
import json as _harness_json

def _to_jsonable(_val):
    # ลองแปลง numpy scalar/array (และชนิดข้อมูลอื่นที่มี .item()/.tolist())
    # ให้เป็น native Python type ก่อนเสมอ เพื่อไม่ให้ผลลัพธ์ที่ถูกต้องถูกแปลงเป็น
    # string จนเทียบกับค่าที่คาดหวังไม่ตรง (เช่น numpy.int64 ไม่ JSON-serializable ตรงๆ)
    if hasattr(_val, "tolist"):
        try:
            return _val.tolist()
        except Exception:
            pass
    if hasattr(_val, "item"):
        try:
            return _val.item()
        except Exception:
            pass
    return _val

try:
    _result = {function_name}(*{args!r}, **{kwargs!r})
    _result = _to_jsonable(_result)
    print("___RESULT_START___")
    try:
        print(_harness_json.dumps({{"ok": True, "value": _result}}))
    except TypeError:
        print(_harness_json.dumps({{"ok": True, "value": str(_result)}}))
except NameError:
    print("___RESULT_START___")
    print(_harness_json.dumps({{"ok": False, "error": "ไม่พบฟังก์ชันชื่อ {function_name} — ตรวจสอบว่าตั้งชื่อถูกต้องหรือไม่"}}))
except Exception as _e:
    print("___RESULT_START___")
    print(_harness_json.dumps({{"ok": False, "error": str(_e)}}))
"""
    full_script = code + "\n" + call_block

    ok, stdout, stderr, timed_out = _run_script(full_script, timeout)

    if timed_out:
        return {
            "success": False,
            "return_value": None,
            "error": f"โค้ดรันนานเกิน {timeout} วินาที (อาจมีลูปไม่สิ้นสุด)",
        }

    if not ok:
        return {"success": False, "return_value": None, "error": stderr.strip()}

    marker = "___RESULT_START___"
    if marker not in stdout:
        return {
            "success": False,
            "return_value": None,
            "error": "ไม่พบผลลัพธ์จากการรันฟังก์ชัน (อาจมี syntax error)",
        }

    _, after = stdout.split(marker, 1)
    try:
        result = json.loads(after.strip())
    except json.JSONDecodeError:
        return {"success": False, "return_value": None, "error": "แปลงผลลัพธ์ไม่สำเร็จ"}

    if result.get("ok"):
        return {"success": True, "return_value": result.get("value"), "error": None}
    return {"success": False, "return_value": None, "error": result.get("error")}
