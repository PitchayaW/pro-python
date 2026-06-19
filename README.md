# เรียนไพธอนแบบอินเทอร์แอกทีฟ

เว็บแอปสำหรับสอน Python เบื้องต้นแบบ interactive ใช้ Streamlit
นักศึกษาเขียนโค้ดในเบราว์เซอร์ได้จริง มีระบบตรวจคำตอบอัตโนมัติ
และบันทึกความก้าวหน้าลง Google Sheet ให้อาจารย์ดูได้

## โครงสร้างโปรเจกต์

```
python-course/
├── streamlit_app.py          # entry point หลัก — ตั้งชื่อหน้าทุกบทผ่าน st.navigation
├── pages/
│   ├── intro.py               # บทนำ (เข้าสู่ระบบ + ภาพรวมบทเรียน)
│   ├── 0_บทที่0_ความเป็นมา.py
│   ├── 1_บทที่1_การติดตั้ง.py
│   ├── 2_บทที่2_ตัวแปร.py
│   ├── 9_บทที่9_numpy.py      # NumPy และ Linear Algebra เบื้องต้น
│   └── ... (บทที่ 5-11 ปัจจุบันเป็น skeleton รอเติมเนื้อหา)
├── utils/
│   ├── sandbox.py           # รันโค้ดนักศึกษาอย่างปลอดภัย (AST validation + subprocess)
│   ├── checker.py           # ตรวจคำตอบ (exact match / test case)
│   ├── progress.py          # บันทึก/ดึง progress จาก Google Sheet
│   └── ui_components.py     # UI ที่ใช้ซ้ำได้ (code editor, ปุ่มรัน/ตรวจ)
├── requirements.txt
└── .streamlit/
    └── config.toml          # ตั้งค่าธีมสีของแอป
```

**หมายเหตุสำคัญ:** ไฟล์ entry point คือ `streamlit_app.py` (ไม่ใช่ `app.py`) เพราะใช้
`st.navigation` กำหนดชื่อหน้าที่แสดงใน sidebar เอง (เช่น "บทนำ", "บทที่ 1: ...")
แทนการให้ Streamlit เดาชื่อจากชื่อไฟล์อัตโนมัติ — ตอน deploy ต้องระบุไฟล์หลักเป็น
`streamlit_app.py`

## สถานะปัจจุบัน

- ✅ บทที่ 0-11: เนื้อหาและแบบฝึกหัดสมบูรณ์ครบทุกบท (9-11 ข้อ/บท) พร้อมใช้งานจริง
  (บทที่ 9 คือ NumPy และ Linear Algebra เบื้องต้น — แยกออกจาก built-in functions
  บทที่ 11 เน้น data cleaning และ groupby ไม่มี visualization เนื่องจากข้อจำกัดของ
  sandbox ที่รองรับเฉพาะ text output)
- ⚠️ Deploy บน Streamlit Cloud: หากเจอ error "you do not have access to this app",
  เป็นปัญหาสิทธิ์เชื่อมต่อ GitHub/Streamlit Cloud account ไม่ใช่ปัญหาโค้ด ให้ตรวจสอบ
  ที่ https://share.streamlit.io ว่า login บัญชีตรงกับที่สร้างแอปไว้ และตรวจสอบสิทธิ์
  OAuth ที่ https://github.com/settings/applications — ถ้าแก้ไม่ได้ ให้ลบแอปเดิมแล้ว
  สร้างใหม่จาก repo เดิม โดยตั้ง Main file path เป็น `streamlit_app.py`

## วิธีรันทดสอบในเครื่องตัวเอง (ก่อน deploy)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

หากยังไม่ได้ตั้งค่า Google Sheet (ขั้นตอนด้านล่าง) ระบบยังใช้งานได้ปกติ
แค่การบันทึกคะแนนจะไม่ทำงาน (จะมีข้อความเตือนแต่ไม่ทำให้แอปพัง)

---

## ขั้นตอนการ Deploy ขึ้น Streamlit Community Cloud (ฟรี)

### ส่วนที่ 1: เตรียม Google Sheet สำหรับเก็บคะแนน

**1.1 สร้าง Google Sheet ใหม่**
- เข้า [sheets.google.com](https://sheets.google.com) สร้างไฟล์ใหม่ ตั้งชื่อ เช่น "Python Course Progress"
- คัดลอก URL ของ Sheet ไว้ (จะใช้ตอนตั้งค่า secrets)

**1.2 สร้าง Google Cloud Service Account**

ขั้นตอนนี้คือการสร้าง "บัญชีหุ่นยนต์" ที่แอปจะใช้เขียนข้อมูลลง Sheet แทนอาจารย์

1. ไปที่ [Google Cloud Console](https://console.cloud.google.com/)
2. สร้างโปรเจกต์ใหม่ (หรือใช้โปรเจกต์ที่มีอยู่) — คลิกเมนูด้านบนซ้าย "เลือกโปรเจกต์" → "โปรเจกต์ใหม่"
3. ไปที่ "APIs & Services" → "Enabled APIs & services" → คลิก "+ ENABLE APIS AND SERVICES"
4. ค้นหาและเปิดใช้งาน 2 อย่าง: **Google Sheets API** และ **Google Drive API**
5. ไปที่ "APIs & Services" → "Credentials" → คลิก "+ CREATE CREDENTIALS" → เลือก "Service account"
6. ตั้งชื่อ service account อะไรก็ได้ (เช่น `python-course-bot`) → คลิก "Create and Continue" → "Done" (ข้ามขั้นตอน role ได้)
7. คลิกที่ service account ที่สร้างไว้ → แท็บ "Keys" → "Add Key" → "Create new key" → เลือก **JSON** → Download
8. จะได้ไฟล์ `.json` ที่มีข้อมูล credentials — **เก็บไฟล์นี้เป็นความลับ ห้าม commit ขึ้น GitHub**

**1.3 แชร์ Google Sheet ให้ Service Account เข้าถึงได้**

1. เปิดไฟล์ JSON ที่ดาวน์โหลดมา หา field `client_email` (จะมีรูปแบบ `xxx@xxx.iam.gserviceaccount.com`)
2. กลับไปที่ Google Sheet ที่สร้างไว้ → คลิก "Share" (แชร์) → ใส่ email นั้น → ให้สิทธิ์ "Editor" → Send

ถ้าข้ามขั้นตอนนี้ แอปจะเชื่อมต่อ Sheet ไม่ได้เพราะ Service Account ไม่มีสิทธิ์เข้าถึงไฟล์

### ส่วนที่ 2: เตรียม GitHub Repository

1. สร้าง repository ใหม่บน GitHub (public หรือ private ก็ได้ — Streamlit Cloud เชื่อมต่อได้ทั้งสองแบบ)
2. push โค้ดทั้งโฟลเดอร์ `python-course/` ขึ้น repo

```bash
cd python-course
git init
git add .
git commit -m "Initial commit: Python interactive course"
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

**ข้อสำคัญ:** ไฟล์ `.streamlit/secrets.toml` ถูกใส่ใน `.gitignore` ไว้แล้ว — ห้าม commit ไฟล์นี้
เพราะมี credentials ลับอยู่ ค่า secrets จะตั้งบนหน้าเว็บของ Streamlit Cloud แทน (ขั้นตอนถัดไป)

### ส่วนที่ 3: Deploy บน Streamlit Community Cloud

1. เข้า [share.streamlit.io](https://share.streamlit.io) เข้าสู่ระบบด้วย GitHub account
2. คลิก "New app" → เลือก repository, branch (main), และไฟล์หลัก (`streamlit_app.py`)
3. ก่อนกด Deploy คลิก "Advanced settings" → ไปที่ช่อง **Secrets** → ใส่เนื้อหาตามรูปแบบนี้:

```toml
[gcp_service_account]
type = "service_account"
project_id = "ใส่ค่าจากไฟล์ JSON"
private_key_id = "ใส่ค่าจากไฟล์ JSON"
private_key = "ใส่ค่าจากไฟล์ JSON (รวม \n ด้วย ไม่ต้องแก้)"
client_email = "ใส่ค่าจากไฟล์ JSON"
client_id = "ใส่ค่าจากไฟล์ JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
sheet_url = "https://docs.google.com/spreadsheets/d/xxxxx/edit"
```

คัดลอกค่าจากไฟล์ JSON ที่ดาวน์โหลดมาตอนสร้าง Service Account ใส่ตรงตาม field
(เปิดไฟล์ JSON ด้วย text editor จะเห็น field ตรงกันเลย) ส่วน `sheet_url` ใส่ URL ของ
Google Sheet ที่สร้างไว้ในขั้นตอนที่ 1.1

4. คลิก "Save" แล้วกด "Deploy!"

รอประมาณ 2-5 นาที แอปจะพร้อมใช้งานที่ URL รูปแบบ `https://<app-name>.streamlit.app`

### ส่วนที่ 4: ทดสอบหลัง Deploy

1. เปิด URL ที่ได้ ลองกรอกชื่อ/รหัสนักศึกษาทดสอบ
2. เข้าไปทำแบบฝึกหัดสักข้อ กด "ตรวจคำตอบ"
3. เปิด Google Sheet ดูว่ามีแถวข้อมูลใหม่ขึ้นมาในชีท "progress" หรือไม่

ถ้าไม่มีข้อมูลขึ้น ให้ตรวจสอบ:
- Service Account email ถูกแชร์เข้า Google Sheet แล้วหรือยัง (ขั้นตอน 1.3)
- ค่า `sheet_url` ใน secrets ตรงกับ Sheet ที่แชร์ไว้หรือไม่
- เปิด Sheets API และ Drive API ครบทั้งสองหรือยัง (ขั้นตอน 1.2.4)

## การอัปเดตเนื้อหาในอนาคต

เมื่อแก้ไขไฟล์ในเครื่องแล้ว push ขึ้น GitHub ตามปกติ Streamlit Cloud จะ deploy
เวอร์ชันใหม่ให้อัตโนมัติภายในไม่กี่นาที ไม่ต้องตั้งค่าอะไรเพิ่ม

```bash
git add .
git commit -m "เพิ่มเนื้อหาบทที่ 3"
git push
```

## ข้อจำกัดที่ควรรู้

- Streamlit Community Cloud จำกัด RAM ที่ 1 GB ต่อแอป ถ้านักศึกษาเข้าพร้อมกันมากและรันโค้ดหนัก ๆ พร้อมกันอาจหน่วง
- แอปจะ "หลับ" ถ้าไม่มีคนใช้นานเกินไป และใช้เวลาราว 10-30 วินาทีในการ "ตื่น" ตอนมีคนเข้าใหม่
- การรันโค้ดนักศึกษาแต่ละครั้งใช้ subprocess แยก มี timeout 5 วินาทีต่อครั้ง กันลูปไม่สิ้นสุด
