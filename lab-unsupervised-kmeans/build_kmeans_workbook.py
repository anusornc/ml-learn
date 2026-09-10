#!/usr/bin/env python3
"""Generate the K-Means Clustering step-by-step hand-calculation workbooks.

Creates both the student workbook (formulas left blank for practice)
and the solved workbook (with formulas and calculations completed).
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

OUT_DIR = Path(__file__).resolve().parent

# Color Palette & Styles
BLUE = Font(name="Arial", color="0000FF")
BLACK = Font(name="Arial", color="000000")
BOLD = Font(name="Arial", bold=True, size=13)
SUBBOLD = Font(name="Arial", bold=True, size=11)
HEAD = Font(name="Arial", bold=True, color="FFFFFF", size=10)
NOTE = Font(name="Arial", italic=True, color="334155", size=9)
SUCCESS = Font(name="Arial", bold=True, color="047857", size=10)

YELLOW_FILL = PatternFill("solid", fgColor="FFF3BF")
NAVY_FILL = PatternFill("solid", fgColor="1E3A5F")
TEAL_FILL = PatternFill("solid", fgColor="0F766E")
INDIGO_FILL = PatternFill("solid", fgColor="4338CA")
LIGHT_GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
LIGHT_BLUE_FILL = PatternFill("solid", fgColor="E0F2FE")
LIGHT_PURPLE_FILL = PatternFill("solid", fgColor="F3E8FF")
GRAY_HEADER_FILL = PatternFill("solid", fgColor="475569")

THIN = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
)
DOUBLE_BOTTOM = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="double", color="1E293B"),
)
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(horizontal="center", vertical="center")


def _width(ws: Worksheet, widths: dict[str, float]) -> None:
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def _label(ws: Worksheet, cell: str, text: str, font: Font | None = None) -> None:
    ws[cell] = text
    ws[cell].font = font or Font(name="Arial", bold=True, size=10)


def _input(ws: Worksheet, cell: str, value: float | int | str, align: Alignment | None = None) -> None:
    ws[cell] = value
    ws[cell].font = BLUE
    ws[cell].fill = YELLOW_FILL
    ws[cell].border = THIN
    if align:
        ws[cell].alignment = align


def _blank(
    ws: Worksheet,
    cell: str,
    solved: bool,
    formula: str,
    num_format: str = "0.0000",
    fill: PatternFill = YELLOW_FILL,
    font: Font = BLACK,
    align: Alignment | None = None,
) -> None:
    ws[cell] = formula if solved else None
    ws[cell].font = font
    ws[cell].fill = fill
    ws[cell].border = THIN
    if num_format:
        ws[cell].number_format = num_format
    if align:
        ws[cell].alignment = align


def _headers(ws: Worksheet, row: int, values: list[str], fill: PatternFill) -> None:
    for idx, value in enumerate(values, start=1):
        cell = ws.cell(row=row, column=idx, value=value)
        cell.font = HEAD
        cell.fill = fill
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        cell.border = THIN
    ws.row_dimensions[row].height = 28


def build_guide(ws: Worksheet) -> None:
    ws.title = "00_Guide"
    ws["A1"] = "ใบงานคำนวณมือ K-Means Clustering ทีละขั้นตอน (Step-by-Step)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:G1")

    instructions = [
        "1. ลำดับการเรียนรู้: อ่านบทเรียน 18-ML-Unsupervised-KMeans.html → เปิด index.html (Sandbox) → ทำใบงาน Excel นี้ → รัน python3 kmeans_from_scratch.py",
        "2. รหัสสีในตาราง:",
        "    - เซลล์พื้นสีเหลือง + ตัวเลขสีน้ำเงิน = ค่าข้อมูลที่กำหนดให้ (ห้ามแก้ไขตอนทำแบบฝึกหัด)",
        "    - เซลล์พื้นสีเหลืองว่าง (ไฟล์โจทย์) = ให้ผู้เรียนพิมพ์สูตรคำนวณของ Excel ลงไปด้วยตนเอง (ห้ามพิมพ์เฉพาะคำตอบตัวเลข)",
        "    - เซลล์พื้นสีฟ้า/เขียว = ส่วนสรุปและวิเคราะห์ผลลัพธ์ของอัลกอริทึม",
        "3. สาระสำคัญและสูตรคณิตศาสตร์ของ K-Means (Lloyd's Algorithm):",
        "    (1) ระยะทางแบบยุคลิด (Euclidean Distance): d(x, c) = √[(x₁ - c₁)² + (x₂ - c₂)²]  → ใน Excel ใช้สูตร =SQRT((x1 - c1)^2 + (x2 - c2)^2)",
        "    (2) การกำหนดกลุ่ม (Assignment Step): กำหนดจุด x ไปยังคลัสเตอร์ k ที่มีระยะห่างน้อยที่สุด  → ใน Excel ใช้สูตร =IF(d_C1 <= d_C2, 1, 2)",
        "    (3) การคำนวณ Centroid ใหม่ (Update Step): หาค่าเฉลี่ยของจุดข้อมูลในกลุ่ม  → ใน Excel ใช้สูตร =AVERAGEIF(Cluster_Range, k, Feature_Range)",
        "    (4) ฟังก์ชันเป้าหมาย WCSS (Within-Cluster Sum of Squares / Inertia): WCSS = ∑ min ||x - c_k||²  → ใน Excel ใช้สูตร =SUM(d_min_sq)",
        "    (5) เงื่อนไขการลู่เข้า (Convergence): อัลกอริทึมสิ้นสุดเมื่อไม่มีจุดข้อมูลใดเปลี่ยนกลุ่มอีกต่อไป (Cluster Assignments คงที่)",
        "4. ไฟล์เฉลย (KMeans_Clustering_Step_by_Step_TH_Solved.xlsx) มีสูตรครบถ้วน ให้ใช้เพื่อตรวจสอบความเข้าใจหลังคำนวณด้วยตนเอง",
    ]

    for idx, text in enumerate(instructions, start=3):
        cell_ref = f"A{idx}"
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=10)
        ws.merge_cells(f"A{idx}:G{idx}")
        ws[cell_ref].alignment = WRAP
        ws.row_dimensions[idx].height = 24 if idx not in (4, 9) else 30

    _width(ws, {"A": 105, "B": 15, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15})


def build_kmeans_step_by_step(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "01_KMeans_2D_Step_by_Step"
    ws.views.sheetView[0].showGridLines = True

    # Title
    ws["A1"] = "การคำนวณ K-Means Clustering 2 มิติ (N=8 จุด, K=2 กลุ่ม, ฟีเจอร์: รายได้ X1 และ คะแนนใช้จ่าย X2)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    # Parameters & Initial Centroids
    ws["A3"] = "พารามิเตอร์เริ่มต้น:"
    ws["A3"].font = SUBBOLD
    ws["A4"] = "จำนวนกลุ่ม (K)"
    ws["B4"] = 2
    ws["B4"].font = BLUE
    ws["B4"].fill = YELLOW_FILL
    ws["B4"].border = THIN
    ws["B4"].alignment = CENTER

    ws["A5"] = "จำนวนจุด (N)"
    ws["B5"] = 8
    ws["B5"].font = BLUE
    ws["B5"].fill = YELLOW_FILL
    ws["B5"].border = THIN
    ws["B5"].alignment = CENTER

    _label(ws, "D3", "จุดศูนย์กลางเริ่มต้น (Initial Centroids t=0):", SUBBOLD)
    _headers(ws, 4, ["Centroid", "เลือกจากจุด", "X1 (รายได้)", "X2 (คะแนน)", "คำอธิบาย"], NAVY_FILL)

    centroid_rows = [
        (5, "C1 (กลุ่ม 1)", "P1", 1.0, 2.0, "จุดข้อมูลเริ่มต้นกลุ่มที่ 1"),
        (6, "C2 (กลุ่ม 2)", "P4", 4.0, 4.0, "จุดข้อมูลเริ่มต้นกลุ่มที่ 2"),
    ]
    for r, name, pt, x1, x2, desc in centroid_rows:
        ws.cell(row=r, column=4, value=name).font = Font(name="Arial", bold=True)
        ws.cell(row=r, column=4).border = THIN
        ws.cell(row=r, column=5, value=pt).alignment = CENTER
        ws.cell(row=r, column=5).font = BLUE
        ws.cell(row=r, column=5).fill = YELLOW_FILL
        ws.cell(row=r, column=5).border = THIN

        _input(ws, f"F{r}", x1, CENTER)
        _input(ws, f"G{r}", x2, CENTER)
        ws.cell(row=r, column=8, value=desc).font = NOTE
        ws.cell(row=r, column=8).border = THIN

    # ------------------ ITERATION 1 ------------------
    ws["A8"] = "【รอบที่ 1: Iteration 1】 — คำนวณระยะทาง Euclidean สู่ Centroid เริ่มต้น (C1: F5,G5 และ C2: F6,G6)"
    ws["A8"].font = SUBBOLD

    headers_iter1 = [
        "จุด",
        "X1",
        "X2",
        "d(P, C1)",
        "d(P, C2)",
        "กลุ่มที่ได้ (Cluster)",
        "d_min² (สำหรับ WCSS)",
        "Centroid ที่สังกัด",
    ]
    _headers(ws, 9, headers_iter1, TEAL_FILL)

    data_points = [
        ("P1", 1.0, 2.0),
        ("P2", 2.0, 1.0),
        ("P3", 2.0, 3.0),
        ("P4", 4.0, 4.0),
        ("P5", 6.0, 5.0),
        ("P6", 7.0, 7.0),
        ("P7", 8.0, 6.0),
        ("P8", 8.0, 8.0),
    ]

    for idx, (pname, x1, x2) in enumerate(data_points, start=10):
        ws[f"A{idx}"] = pname
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _input(ws, f"B{idx}", x1, CENTER)
        _input(ws, f"C{idx}", x2, CENTER)

        # Formulas for Iteration 1
        f_d1 = f"=SQRT((B{idx}-$F$5)^2 + (C{idx}-$G$5)^2)"
        f_d2 = f"=SQRT((B{idx}-$F$6)^2 + (C{idx}-$G$6)^2)"
        f_cluster = f"=IF(D{idx}<=E{idx}, 1, 2)"
        f_dmin_sq = f"=IF(F{idx}=1, D{idx}^2, E{idx}^2)"
        f_cname = f'=IF(F{idx}=1, "C1", "C2")'

        _blank(ws, f"D{idx}", solved, f_d1, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"E{idx}", solved, f_d2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{idx}", solved, f_cluster, "0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
        _blank(ws, f"G{idx}", solved, f_dmin_sq, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_cname, "@", LIGHT_GREEN_FILL, BLACK, CENTER)

    # Iteration 1 WCSS
    ws["A18"] = "รวม WCSS รอบที่ 1 (Inertia):"
    ws["A18"].font = Font(name="Arial", bold=True, size=10)
    ws.merge_cells("A18:F18")
    ws["A18"].alignment = Alignment(horizontal="right", vertical="center")
    _blank(
        ws,
        "G18",
        solved,
        "=SUM(G10:G17)",
        "0.0000",
        LIGHT_PURPLE_FILL,
        Font(name="Arial", bold=True, color="4338CA", size=11),
        CENTER,
    )
    ws["G18"].border = DOUBLE_BOTTOM

    # Updated Centroids Table after Iteration 1
    ws["A20"] = "【คำนวณ Centroid ใหม่หลังรอบที่ 1】: ใช้สูตร =AVERAGEIF(...) หาค่าเฉลี่ยของจุดที่สังกัดแต่ละกลุ่ม"
    ws["A20"].font = SUBBOLD

    headers_centroids = ["กลุ่ม (Cluster)", "จำนวนจุดสมาชิก", "Centroid X1 ใหม่", "Centroid X2 ใหม่", "สูตรที่ใช้"]
    _headers(ws, 21, headers_centroids, INDIGO_FILL)

    # C1 after iter 1 (mean of P1, P2, P3: x1=1.6667, x2=2.0000)
    ws["A22"] = "กลุ่ม 1 (Cluster 1)"
    ws["A22"].font = Font(name="Arial", bold=True)
    ws["A22"].border = THIN
    _blank(ws, "B22", solved, "=COUNTIF($F$10:$F$17, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C22", solved, "=AVERAGEIF($F$10:$F$17, 1, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D22", solved, "=AVERAGEIF($F$10:$F$17, 1, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E22"] = "=AVERAGEIF($F$10:$F$17, 1, feature_range)"
    ws["E22"].font = NOTE
    ws["E22"].border = THIN

    # C2 after iter 1 (mean of P4, P5, P6, P7, P8: x1=6.6000, x2=6.0000)
    ws["A23"] = "กลุ่ม 2 (Cluster 2)"
    ws["A23"].font = Font(name="Arial", bold=True)
    ws["A23"].border = THIN
    _blank(ws, "B23", solved, "=COUNTIF($F$10:$F$17, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C23", solved, "=AVERAGEIF($F$10:$F$17, 2, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D23", solved, "=AVERAGEIF($F$10:$F$17, 2, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E23"] = "=AVERAGEIF($F$10:$F$17, 2, feature_range)"
    ws["E23"].font = NOTE
    ws["E23"].border = THIN

    # ------------------ ITERATION 2 ------------------
    ws["A25"] = "【รอบที่ 2: Iteration 2】 — คำนวณระยะทาง Euclidean สู่ Centroid ใหม่ (C1: C22,D22 และ C2: C23,D23)"
    ws["A25"].font = SUBBOLD

    headers_iter2 = [
        "จุด",
        "X1",
        "X2",
        "d(P, C1_new)",
        "d(P, C2_new)",
        "กลุ่มใหม่ (Cluster 2)",
        "d_min²",
        "การเปลี่ยนแปลงกลุ่ม",
    ]
    _headers(ws, 26, headers_iter2, TEAL_FILL)

    for idx, (pname, x1, x2) in enumerate(data_points, start=27):
        prev_idx = idx - 17  # points to row 10..17 in iter 1
        ws[f"A{idx}"] = pname
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _input(ws, f"B{idx}", x1, CENTER)
        _input(ws, f"C{idx}", x2, CENTER)

        f_d1_2 = f"=SQRT((B{idx}-$C$22)^2 + (C{idx}-$D$22)^2)"
        f_d2_2 = f"=SQRT((B{idx}-$C$23)^2 + (C{idx}-$D$23)^2)"
        f_cluster_2 = f"=IF(D{idx}<=E{idx}, 1, 2)"
        f_dmin_sq_2 = f"=IF(F{idx}=1, D{idx}^2, E{idx}^2)"
        f_change = f'=IF(F{idx}=F{prev_idx}, "คงเดิม", "ย้ายกลุ่ม (สลับ!)")'

        _blank(ws, f"D{idx}", solved, f_d1_2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"E{idx}", solved, f_d2_2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{idx}", solved, f_cluster_2, "0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
        _blank(ws, f"G{idx}", solved, f_dmin_sq_2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_change, "@", LIGHT_GREEN_FILL, Font(name="Arial", bold=True), CENTER)

    # Iteration 2 WCSS
    ws["A35"] = "รวม WCSS รอบที่ 2 (Inertia):"
    ws["A35"].font = Font(name="Arial", bold=True, size=10)
    ws.merge_cells("A35:F35")
    ws["A35"].alignment = Alignment(horizontal="right", vertical="center")
    _blank(
        ws,
        "G35",
        solved,
        "=SUM(G27:G34)",
        "0.0000",
        LIGHT_PURPLE_FILL,
        Font(name="Arial", bold=True, color="4338CA", size=11),
        CENTER,
    )
    ws["G35"].border = DOUBLE_BOTTOM

    # Updated Centroids Table after Iteration 2
    ws["A37"] = "【Centroid หลังรอบที่ 2】: P4 ได้สลับจากกลุ่ม 2 ไปอยู่กลุ่ม 1 ทำให้จุดศูนย์กลางเคลื่อนตัวอีกครั้ง"
    ws["A37"].font = SUBBOLD

    _headers(ws, 38, ["กลุ่ม (Cluster)", "จำนวนจุดสมาชิก", "Centroid X1 ใหม่", "Centroid X2 ใหม่", "จุดสมาชิกในกลุ่ม"], INDIGO_FILL)

    # C1 after iter 2 (mean of P1, P2, P3, P4: x1=2.2500, x2=2.5000)
    ws["A39"] = "กลุ่ม 1 (Cluster 1)"
    ws["A39"].font = Font(name="Arial", bold=True)
    ws["A39"].border = THIN
    _blank(ws, "B39", solved, "=COUNTIF($F$27:$F$34, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C39", solved, "=AVERAGEIF($F$27:$F$34, 1, $B$27:$B$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D39", solved, "=AVERAGEIF($F$27:$F$34, 1, $C$27:$C$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E39"] = "P1, P2, P3, P4 (มี P4 เพิ่มเข้ามา)"
    ws["E39"].font = NOTE
    ws["E39"].border = THIN

    # C2 after iter 2 (mean of P5, P6, P7, P8: x1=7.2500, x2=6.5000)
    ws["A40"] = "กลุ่ม 2 (Cluster 2)"
    ws["A40"].font = Font(name="Arial", bold=True)
    ws["A40"].border = THIN
    _blank(ws, "B40", solved, "=COUNTIF($F$27:$F$34, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C40", solved, "=AVERAGEIF($F$27:$F$34, 2, $B$27:$B$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D40", solved, "=AVERAGEIF($F$27:$F$34, 2, $C$27:$C$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E40"] = "P5, P6, P7, P8"
    ws["E40"].font = NOTE
    ws["E40"].border = THIN

    # ------------------ CONVERGENCE & SUMMARY ------------------
    ws["A42"] = "【การตรวจสอบการลู่เข้า (Convergence Check) & สรุปผลสัมฤทธิ์】"
    ws["A42"].font = SUBBOLD

    checks = [
        ("A43", "จำนวนจุดที่เปลี่ยนกลุ่มในรอบที่ 2:", "D43", '=COUNTIF(H27:H34, "*สลับ*")', "จุด"),
        ("A44", "การลดลงของ WCSS (รอบ 1 → รอบ 2):", "D44", "=G18-G35", "ค่า Inertia ลดลง"),
        ("A45", "สถานะการลู่เข้ารอบที่ 3 (Final State):", "D45", '="ลู่เข้าสมบูรณ์ (Converged) ที่ C1=(2.25, 2.50), C2=(7.25, 6.50) WCSS=17.50"', ""),
    ]

    for lbl_cell, lbl_text, val_cell, formula, unit in checks:
        ws[lbl_cell] = lbl_text
        ws[lbl_cell].font = Font(name="Arial", bold=True, size=10)
        ws.merge_cells(f"{lbl_cell}:{chr(ord(lbl_cell[0])+2)}{lbl_cell[1:]}")
        _blank(ws, val_cell, solved, formula, "0.0000" if "G18" in formula else "@", LIGHT_GREEN_FILL, Font(name="Arial", bold=True, color="065F46"))
        ws.merge_cells(f"{val_cell}:{chr(ord(val_cell[0])+3)}{val_cell[1:]}")

    ws["A47"] = "ข้อสังเกตสำคัญสำหรับการเรียนรู้:"
    ws["A47"].font = Font(name="Arial", bold=True)
    notes = [
        "1. จุด P4 (4, 4) เริ่มต้นอยู่ใกล้ C2 (4, 4) จึงสังกัดกลุ่ม 2 ในรอบแรก",
        "2. เมื่อ C2 ขยับไปทางขวาบนตามจุด P5-P8 ทำให้ระยะห่างจาก P4 ไปยัง C1 ใหม่ใกล้กว่า C2 ใหม่ จุด P4 จึงสลับมาสังกัดกลุ่ม 1 ในรอบที่ 2",
        "3. ค่า WCSS ลดลงจาก 79.00 (จุดเริ่มต้น) → 23.87 (หลังรอบ 1) → 17.50 (หลังรอบ 2) ซึ่งพิสูจน์คุณสมบัติการลดลงทางคณิตศาสตร์ของ K-Means",
    ]
    for r_idx, note_text in enumerate(notes, start=48):
        ws[f"A{r_idx}"] = note_text
        ws[f"A{r_idx}"].font = NOTE
        ws.merge_cells(f"A{r_idx}:I{r_idx}")

    _width(
        ws,
        {
            "A": 16,
            "B": 10,
            "C": 10,
            "D": 14,
            "E": 14,
            "F": 18,
            "G": 18,
            "H": 22,
            "I": 12,
        },
    )


def build_elbow_method(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "02_Elbow_Method"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "การเลือกจำนวนคลัสเตอร์ K ที่เหมาะสมด้วยวิธีข้อศอก (Elbow Method & Inertia)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:F1")

    ws["A3"] = "ทฤษฎี: WCSS (Inertia) จะลดลงเสมอเมื่อ K เพิ่มขึ้น แต่จุดที่เหมาะสมคือจุด 'ข้อศอก' ที่อัตราการลดลงเริ่มชะลอตัวลงอย่างชัดเจน"
    ws["A3"].font = NOTE
    ws.merge_cells("A3:F3")

    _headers(ws, 5, ["จำนวนคลัสเตอร์ (K)", "WCSS (Inertia)", "การลดลงของ WCSS (Δ WCSS)", "อัตราส่วนการลดลง (%)", "ข้อสรุป"], TEAL_FILL)

    elbow_data = [
        (1, 99.50, "-", "-", "ทุกจุดรวมเป็น 1 คลัสเตอร์ (จุดกึ่งกลาง = 4.75, 4.50)"),
        (2, 17.50, "=B6-B7", "=(B6-B7)/B6", "★ จุดข้อศอก (Elbow Point): ลดลงมากถึง 82.41%"),
        (3, 7.83, "=B7-B8", "=(B7-B8)/B7", "เริ่มชะลอตัว การแบ่งกลุ่มย่อยเพิ่มไม่คุ้มค่า"),
        (4, 5.33, "=B8-B9", "=(B8-B9)/B8", "กลุ่มย่อยเกินไป (Overfitting)"),
        (5, 3.67, "=B9-B10", "=(B9-B10)/B9", "ใกล้เคียงศูนย์แต่สูญเสียความหมายทางสถิติ"),
    ]

    for idx, (k_val, wcss_val, delta_f, pct_f, comment) in enumerate(elbow_data, start=6):
        ws[f"A{idx}"] = k_val
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _input(ws, f"B{idx}", wcss_val, CENTER)

        if delta_f == "-":
            ws[f"C{idx}"] = "-"
            ws[f"C{idx}"].alignment = CENTER
            ws[f"C{idx}"].border = THIN
            ws[f"D{idx}"] = "-"
            ws[f"D{idx}"].alignment = CENTER
            ws[f"D{idx}"].border = THIN
        else:
            _blank(ws, f"C{idx}", solved, delta_f, "0.00", YELLOW_FILL, BLACK, CENTER)
            _blank(ws, f"D{idx}", solved, pct_f, "0.0%", YELLOW_FILL, BLACK, CENTER)

        ws[f"E{idx}"] = comment
        ws[f"E{idx}"].font = Font(name="Arial", bold=(k_val == 2), color="047857" if k_val == 2 else "334155")
        ws[f"E{idx}"].border = THIN

    # Add Line Chart for Elbow
    chart = LineChart()
    chart.title = "Elbow Method: WCSS vs Number of Clusters (K)"
    chart.style = 13
    chart.y_axis.title = "WCSS / Inertia"
    chart.x_axis.title = "Number of Clusters (K)"
    chart.width = 16
    chart.height = 10

    data = Reference(ws, min_col=2, min_row=5, max_row=10)
    cats = Reference(ws, min_col=1, min_row=6, max_row=10)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)

    ws.add_chart(chart, "A13")

    _width(ws, {"A": 22, "B": 18, "C": 24, "D": 22, "E": 48, "F": 10})


def build(solved: bool) -> Workbook:
    wb = Workbook()
    build_guide(wb.active)
    build_kmeans_step_by_step(wb.create_sheet(), solved=solved)
    build_elbow_method(wb.create_sheet(), solved=solved)
    return wb


def main() -> None:
    student = OUT_DIR / "KMeans_Clustering_Step_by_Step_TH.xlsx"
    solved = OUT_DIR / "KMeans_Clustering_Step_by_Step_TH_Solved.xlsx"
    build(False).save(student)
    build(True).save(solved)
    print(f"Generated successfully: {student.name} and {solved.name}")


if __name__ == "__main__":
    main()
