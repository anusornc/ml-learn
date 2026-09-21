# Jev Model Interactive Decision Sandbox (System 1 AI)

เครื่องมือจำลองการทำงานและห้องปฏิบัติการสำหรับ **Jev Model (`typesafe/jev-1.13`)** ซึ่งเป็นโมเดลประเภท **System 1 Structured Decision-Making** พัฒนาโดย TypeSafe AI ออกแบบมาเพื่อการตัดสินใจแบบ Type-Safe รวดเร็วพิเศษ (~100ms) โดยไม่มีข้อความบรรยายยืดยาว (Zero-prose)

---

## 🌟 จุดเด่นของโมเดล Jev

1. **System 1 Fast Inference:** ทำงานเร็วในระดับ 70–200 ms เหมาะกับการทำ Router, Classifier, และ Guardrail ในระบบ Agent
2. **Type-Safe Schema 100%:** ผลลัพธ์ถูกการันตีโครงสร้างตามคำถาม 3 รูปแบบ:
   - **`Choice`**: การเลือกตัวเลือกเดี่ยว พร้อมแจกแจงความน่าจะเป็น (Probability Distribution)
   - **`Score`**: คะแนนถ่วงน้ำหนักตามระดับความรุนแรง/ความสำคัญ (Weighted Score)
   - **`Noul`**: การประเมินความน่าจะเป็นของ "ใช่ / จริง" (Probability of True/Yes)
3. **Calibrated Probabilities:** มีการปรับเทียบความน่าจะเป็นเพื่อใช้ตัดสินใจกำหนดเกณฑ์ Auto-execute หรือส่งต่อให้มนุษย์ (Human-in-the-loop)

---

## 💻 วิธีเปิดใช้งาน Sandbox ผ่านเว็บ

1. เปิดไฟล์ [`lab-jev-decision/index.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-jev-decision/index.html) ในเบราว์เซอร์
2. มี Preset ตัวอย่างการใช้งานจริง 7 รูปแบบให้เลือกทดสอบ:
   - 💬 **Support Triage:** คัดกรองและแบ่งระดับตั๋วลูกค้า (Intent, Urgency Score, Human Needed)
   - 🛡️ **Agent Guardrail:** ตรวจสอบความปลอดภัย Tool-Calling ก่อนรันคำสั่ง Terminal
   - 🤖 **ML Model Router:** คัดกรองและเลือกรุ่นโมเดลที่เหมาะสมตามโจทย์โปรเจกต์
   - 🚨 **E-Commerce Moderation:** คัดกรองสินค้าและรีวิวต้องห้ามแบบฉับพลัน
   - ⚡ **SRE Incident Triaging:** ประเมินเหตุการณ์ระบบล่มและปลุก On-call Engineer
   - 💳 **Financial Anti-Fraud:** ตรวจสอบทุจริตธุรกรรมบัตรเครดิตและการขอ OTP ยืนยันตัวตน
   - ✂️ **Context Pruning:** บีบอัดประวัติคำสั่ง Tool Call ของ Coding Agent
3. หากมี API Key ของ Jev ให้คลิกปุ่ม **"ตั้งค่า API Key"** ด้านบนขวาเพื่อกรอกคีย์ (คีย์จะถูกเก็บใน `localStorage` ของเครื่องคุณเท่านั้น)
4. หรือหากยังไม่มีคีย์ สามารถกดปุ่ม **"🧪 ทดลองโหมด Mock"** เพื่อทดลองดูผลลัพธ์จำลอง 100% ได้ทันทีโดยไม่ติด CORS

---

## 🐍 วิธีรันและทดสอบผ่าน Python Terminal

คุณสามารถใช้สคริปต์ [`test_jev_api.py`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-jev-decision/test_jev_api.py) เพื่อทดสอบการส่งคำขอไปยัง REST API:

```bash
# กำหนด API Key ในสภาพแวดล้อม
export JEV_API_KEY="your_actual_api_key_here"

# รันสคริปต์
python3 lab-jev-decision/test_jev_api.py
```

---

## 🔗 อ้างอิงและเอกสารเพิ่มเติม

- เว็บไซต์ชุมชน Jev AI: [https://www.jevai.org/th](https://www.jevai.org/th)
- เอกสารสนามทดลอง Jev: [https://www.jevai.org/th/docs](https://www.jevai.org/th/docs)
- การเชื่อมต่อ Agent (MCP / Skills): [https://www.jevai.org/th/agent](https://www.jevai.org/th/agent)
