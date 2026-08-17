# Lab: Perceptron & MLP

ลำดับทำ (อย่ากระโดดไป Keras ก่อน)

1. อ่านบท [09-ML-NN.html](../09-ML-NN.html) — สูตร perceptron, สะพานจาก logistic, ภาพรวม backprop
2. เปิด [index.html](index.html) ทดลอง AND → OR → XOR ใน sandbox
3. รันโค้ดจากศูนย์
   - `python3 perceptron.py` — AND/OR ลู่เข้า, XOR ต้องพัง
   - `python3 mlp_xor.py` — โครง 2-2-1 แก้ XOR ได้เมื่อ `seed=0`
4. ทำใบงานคำนวณ 1 epoch
   - โจทย์: [Perceptron_MLP_1_Epoch_TH.xlsx](Perceptron_MLP_1_Epoch_TH.xlsx)
   - เฉลย: [Perceptron_MLP_1_Epoch_TH_Solved.xlsx](Perceptron_MLP_1_Epoch_TH_Solved.xlsx)
5. ค่อยเปิดแล็บ Keras จากหน้าสารบัญ

สัญญาที่ต้องจำให้ตรงกันทั้งบทเรียน โค้ด และใบงาน

- Step(z) = 1 เมื่อ **z ≥ 0**
- Loss ของ MLP = **½ (ŷ − y)²** แล้วอัปเดตด้วยเครื่องหมายลบ
- คำนวณ delta จากน้ำหนัก**เดิม** แล้วค่อยอัปเดต
- XOR + `seed=42` ใน `mlp_xor.py` มักค้างประมาณ 75% — ไม่ใช่บั๊ก เป็น plateau

สร้างใบงานใหม่: `python3 build_1_epoch_workbook.py`

ตรวจสัญญาการสอน: `python3 test_lab.py`
