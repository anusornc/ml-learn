# Lab: Unsupervised Learning & K-Means Clustering

ลำดับขั้นตอนการปฏิบัติการ (Learning Sequence):

1. **ศึกษาทฤษฎี**: อ่านบทเรียน [18-ML-Unsupervised-KMeans.html](../18-ML-Unsupervised-KMeans.html) — ความแตกต่างของ Unsupervised Learning, ฟังก์ชันเป้าหมาย WCSS / Inertia, ขั้นตอนวิธี Lloyd's Algorithm และวิธีเลือกค่า K
2. **ทดลองจำลองเชิงโต้ตอบ (Interactive Sandbox)**: เปิด [index.html](index.html) เพื่อทดลองสร้างจุดข้อมูล, ปรับค่า K, สังเกตการเคลื่อนที่ของ Centroid และแบ่งพื้นที่ Voronoi แบบสด
3. **ฝึกคำนวณมือใน Excel (Hand-Calculation Worksheet)**:
   - ไฟล์โจทย์สำหรับผู้เรียน: [KMeans_Clustering_Step_by_Step_TH.xlsx](KMeans_Clustering_Step_by_Step_TH.xlsx)
   - ไฟล์เฉลยสำหรับตรวจคำตอบ: [KMeans_Clustering_Step_by_Step_TH_Solved.xlsx](KMeans_Clustering_Step_by_Step_TH_Solved.xlsx)
4. **รันโค้ด Python จากศูนย์ (From Scratch)**:
   - `python3 kmeans_from_scratch.py` — โมเดล K-Means แบบ Pure Python พิสูจน์โจทย์เดียวกับ Excel จุดต่อจุด (แสดงการสลับกลุ่มของ P4 และการลดลงของ WCSS)
5. **รันโค้ดประยุกต์จริงด้วย Scikit-Learn**:
   - `../lab-week2/.venv/bin/python kmeans_sklearn_clustering.py` (หรือ `python3 kmeans_sklearn_clustering.py`) — โครงงานแบ่งกลุ่มลูกค้าห้างสรรพสินค้า (Customer Segmentation) 200 รายการ พร้อม Elbow Method, Silhouette Score และบันทึกภาพกราฟิกวิเคราะห์

---

### สัญญาการสอนที่ต้องตรงกันทั้งบทเรียน โค้ด และใบงาน (Teaching Contracts)

1. **การวัดระยะทาง (Distance Metric)**: ใช้ Euclidean Distance $d(x, c) = \sqrt{\sum (x_j - c_j)^2}$
2. **การจัดกลุ่ม (Assignment)**: กำหนดแต่ละจุดไปยัง Centroid ที่ใกล้ที่สุด ($k^* = \arg\min_j d(x, c_j)$) หากระยะทางเท่ากันให้เลือกกลุ่มหมายเลขน้อยกว่า
3. **การอัปเดต Centroid (Update)**: ค่าเฉลี่ยพิกัดของสมาชิกในกลุ่มนั้น ๆ $\mu_k = \frac{1}{|S_k|} \sum_{x \in S_k} x$
4. **โจทย์ 8 จุดในใบงาน**:
   - จุดข้อมูล: $P_1(1,2), P_2(2,1), P_3(2,3), P_4(4,4), P_5(6,5), P_6(7,7), P_7(8,6), P_8(8,8)$
   - Centroid เริ่มต้น: $C_1=P_1(1,2), C_2=P_4(4,4)$
   - รอบที่ 1: กลุ่ม $[1, 1, 1, 2, 2, 2, 2, 2]$ → Centroid ใหม่ $C_1=(1.6667, 2.0), C_2=(6.6, 6.0)$ → $\text{WCSS}=23.87$
   - รอบที่ 2: $P_4$ สลับไปกลุ่ม 1 กลายเป็น $[1, 1, 1, 1, 2, 2, 2, 2]$ → Centroid ใหม่ $C_1=(2.25, 2.5), C_2=(7.25, 6.5)$ → $\text{WCSS}=17.50$
   - รอบที่ 3: ไม่มีการสลับกลุ่มอีกต่อไป → **ลู่เข้าสมบูรณ์ (Converged)** ที่ $\text{WCSS}=17.50$
5. **วิธีข้อศอก (Elbow Method)**:
   - $K=1 \to \text{WCSS}=99.50$
   - $K=2 \to \text{WCSS}=17.50$ (ลดลง $82.00$ หรือ $82.41\%$ — จุดข้อศอกที่เหมาะสมที่สุด)

---

### คำสั่งอัตโนมัติประจำแล็บ

- **สร้างใบงาน Excel ใหม่**: `python3 build_kmeans_workbook.py`
- **ตรวจสัญญาการสอนอัตโนมัติ**: `python3 test_lab.py`
