#!/usr/bin/env python3
"""Generate Supplementary Exam Review Workbooks for K-Means Clustering.

Creates:
1. KMeans_Exam_Practice_TH.xlsx (Student practice workbook for pre-exam review)
2. KMeans_Exam_Practice_TH_Solved.xlsx (Instructor solutions with formulas & explanations)
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

OUT_DIR = Path(__file__).resolve().parent

# Color Palette & Fonts
NAVY_FILL = PatternFill("solid", fgColor="1E3A5F")
TEAL_FILL = PatternFill("solid", fgColor="0F766E")
INDIGO_FILL = PatternFill("solid", fgColor="4338CA")
AMBER_FILL = PatternFill("solid", fgColor="D97706")
YELLOW_FILL = PatternFill("solid", fgColor="FFF3BF")
LIGHT_GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
LIGHT_BLUE_FILL = PatternFill("solid", fgColor="E0F2FE")
LIGHT_PURPLE_FILL = PatternFill("solid", fgColor="F3E8FF")
LIGHT_AMBER_FILL = PatternFill("solid", fgColor="FEF3C7")
GRAY_ROW_FILL = PatternFill("solid", fgColor="F8FAFC")

BLUE = Font(name="Arial", color="0000FF", bold=True)
BLACK = Font(name="Arial", color="000000")
BOLD = Font(name="Arial", bold=True, size=13)
SUBBOLD = Font(name="Arial", bold=True, size=11)
HEAD = Font(name="Arial", bold=True, color="FFFFFF", size=10)
NOTE = Font(name="Arial", italic=True, color="334155", size=9)
WARN = Font(name="Arial", bold=True, color="B91C1C", size=9)
SUCCESS = Font(name="Arial", bold=True, color="047857", size=10)

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


# -------------------------------------------------------------------------
# SHEET 1: 00_Exam_Guide
# -------------------------------------------------------------------------
def build_exam_guide(ws: Worksheet) -> None:
    ws.title = "00_Exam_Guide"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "แบบฝึกหัดเสริมทบทวนก่อนสอบ: K-Means Clustering (Pre-Exam Practice)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:G1")

    lines = [
        "วัตถุประสงค์: เอกสารชุดนี้จัดทำขึ้นเพื่อเป็นแบบฝึกหัดทบทวนความเข้าใจเชิงคำนวณและทฤษฎี สำหรับเตรียมตัวสอบวิชา Machine Learning",
        "คำชี้แจงการทำแบบฝึกหัด:",
        "    • เซลล์สีเหลือง + ตัวเลขสีน้ำเงิน = ข้อมูลที่โจทย์กำหนดให้ (ค่าคงที่)",
        "    • เซลล์สีเหลืองว่าง (ในไฟล์โจทย์) = ให้นักศึกษาเขียนสูตรการคำนวณด้วยตนเอง",
        "    • มีทั้งหมด 3 ส่วน: (1) การคำนวณมือทีละรอบ (2) การวิเคราะห์วิธีข้อศอก Elbow Method (3) ข้อสอบแนวคิดทฤษฎี",
        "หัวใจสำคัญและสูตรที่ต้องแม่นก่อนเข้าห้องสอบ:",
        "    1. ระยะทางแบบยุคลิด (Euclidean Distance): d(P, C) = √[(x₁ - c₁)² + (x₂ - c₂)²]  (Excel: =SQRT((x1 - c1)^2 + (x2 - c2)^2))",
        "    2. การเลือกกลุ่ม (Assignment): เลือกคลัสเตอร์ที่มีระยะทางสั้นที่สุด d_min (Excel: =IF(d_C1 <= d_C2, 1, 2))",
        "    3. การอัปเดต Centroid (Update): หาค่าเฉลี่ยของพิกัดในกลุ่ม  (Excel: =AVERAGEIF(Cluster_Range, k, Feature_Range))",
        "    4. ฟังก์ชันเป้าหมาย WCSS / Inertia: WCSS = ∑ (d_min)²  (Excel: =SUM(d_min_sq))",
        "    5. จุดข้อศอก (Elbow Point): คือจุดที่อัตราการลดลงของ WCSS ชะลอตัวลงอย่างมีนัยสำคัญ (Diminishing Return)",
        "ข้อควรระวังที่นักศึกษามักผิดในห้องสอบ (Common Pitfalls):",
        "    ⚠️ ห้ามนำ Centroid ใหม่ที่เพิ่งคำนวณได้ไปคำนวณซ้ำกับข้อมูลของรอบเดิมทันที ต้องขึ้นรอบใหม่เสมอ",
        "    ⚠️ อย่าลืมยกกำลังสองก่อนรวมเป็นค่า WCSS (WCSS คือ Squared Distance ไม่ใช่ผลรวมระยะทางธรรมดา)",
        "    ⚠️ ระวังการปัดเศษทศนิยมก่อนคำนวณจบ หากใช้เครื่องคิดเลขให้ใช้ทศนิยมอย่างน้อย 4 ตำแหน่ง",
    ]

    for idx, text in enumerate(lines, start=3):
        cell_ref = f"A{idx}"
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=10, bold=(idx in (3, 4, 8, 14)))
        if idx >= 15:
            ws[cell_ref].font = WARN
        ws.merge_cells(f"A{idx}:G{idx}")
        ws[cell_ref].alignment = WRAP
        ws.row_dimensions[idx].height = 24 if idx not in (4, 8, 14) else 28

    _width(ws, {"A": 105, "B": 15, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15})


# -------------------------------------------------------------------------
# SHEET 2: 01_KMeans_Calculation
# -------------------------------------------------------------------------
def build_exam_calculation(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "01_KMeans_Calculation"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "โจทย์คำนวณมือ: การจัดกลุ่มนักศึกษา 8 คน (N=8) ตามคะแนนสอบกลางภาค (X1) และ ปลายภาค (X2)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    # Parameters
    ws["A3"] = "พารามิเตอร์โจทย์:"
    ws["A3"].font = SUBBOLD
    ws["A4"] = "จำนวนกลุ่ม (K)"
    ws["B4"] = 2
    ws["B4"].font = BLUE
    ws["B4"].fill = YELLOW_FILL
    ws["B4"].border = THIN
    ws["B4"].alignment = CENTER

    ws["A5"] = "จำนวนข้อมูล (N)"
    ws["B5"] = 8
    ws["B5"].font = BLUE
    ws["B5"].fill = YELLOW_FILL
    ws["B5"].border = THIN
    ws["B5"].alignment = CENTER

    _label(ws, "D3", "จุดศูนย์กลางเริ่มต้นที่โจทย์กำหนด (Initial Centroids t=0):", SUBBOLD)
    _headers(ws, 4, ["Centroid", "เลือกจากจุด", "X1 (กลางภาค)", "X2 (ปลายภาค)", "คำอธิบาย"], NAVY_FILL)

    centroid_specs = [
        (5, "C1 (กลุ่ม 1)", "S1", 2.0, 2.0, "คะแนนกลุ่มนักศึกษาเรียนช้า"),
        (6, "C2 (กลุ่ม 2)", "S4", 4.0, 4.0, "คะแนนกลุ่มนักศึกษาเรียนเร็ว"),
    ]
    for r, name, pt, x1, x2, desc in centroid_specs:
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
        "รหัสนักศึกษา",
        "X1 (กลางภาค)",
        "X2 (ปลายภาค)",
        "d(S, C1)",
        "d(S, C2)",
        "กลุ่มที่ได้ (Cluster)",
        "d_min² (สำหรับ WCSS)",
        "กลุ่มที่สังกัด",
    ]
    _headers(ws, 9, headers_iter1, TEAL_FILL)

    data_points = [
        ("S1", 2.0, 2.0),
        ("S2", 3.0, 1.0),
        ("S3", 1.0, 3.0),
        ("S4", 4.0, 4.0),
        ("S5", 6.0, 7.0),
        ("S6", 7.0, 8.0),
        ("S7", 8.0, 6.0),
        ("S8", 9.0, 8.0),
    ]

    for idx, (pname, x1, x2) in enumerate(data_points, start=10):
        ws[f"A{idx}"] = pname
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _input(ws, f"B{idx}", x1, CENTER)
        _input(ws, f"C{idx}", x2, CENTER)

        f_d1 = f"=SQRT((B{idx}-$F$5)^2 + (C{idx}-$G$5)^2)"
        f_d2 = f"=SQRT((B{idx}-$F$6)^2 + (C{idx}-$G$6)^2)"
        f_cluster = f"=IF(D{idx}<=E{idx}, 1, 2)"
        f_dmin_sq = f"=IF(F{idx}=1, D{idx}^2, E{idx}^2)"
        f_cname = f'=IF(F{idx}=1, "กลุ่ม 1", "กลุ่ม 2")'

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
    ws["A20"] = "【Centroid ใหม่หลังรอบที่ 1】: คำนวณค่าเฉลี่ยพิกัดสมาชิกในแต่ละกลุ่ม (C1 สมาชิก: S1..S3, C2 สมาชิก: S4..S8)"
    ws["A20"].font = SUBBOLD

    headers_centroids = ["กลุ่ม (Cluster)", "จำนวนสมาชิก", "Centroid X1 ใหม่", "Centroid X2 ใหม่", "สูตรคำนวณที่ใช้"]
    _headers(ws, 21, headers_centroids, INDIGO_FILL)

    # C1 after iter 1: mean of S1, S2, S3 = (6/3, 6/3) = (2.0, 2.0)
    ws["A22"] = "กลุ่ม 1 (Cluster 1)"
    ws["A22"].font = Font(name="Arial", bold=True)
    ws["A22"].border = THIN
    _blank(ws, "B22", solved, "=COUNTIF($F$10:$F$17, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C22", solved, "=AVERAGEIF($F$10:$F$17, 1, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D22", solved, "=AVERAGEIF($F$10:$F$17, 1, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E22"] = "=AVERAGEIF($F$10:$F$17, 1, Feature_Range) -> ได้ (2.0, 2.0)"
    ws["E22"].font = NOTE
    ws["E22"].border = THIN

    # C2 after iter 1: mean of S4..S8 = (34/5, 33/5) = (6.8, 6.6)
    ws["A23"] = "กลุ่ม 2 (Cluster 2)"
    ws["A23"].font = Font(name="Arial", bold=True)
    ws["A23"].border = THIN
    _blank(ws, "B23", solved, "=COUNTIF($F$10:$F$17, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C23", solved, "=AVERAGEIF($F$10:$F$17, 2, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D23", solved, "=AVERAGEIF($F$10:$F$17, 2, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E23"] = "=AVERAGEIF($F$10:$F$17, 2, Feature_Range) -> ได้ (6.8, 6.6)"
    ws["E23"].font = NOTE
    ws["E23"].border = THIN

    # ------------------ ITERATION 2 ------------------
    ws["A25"] = "【รอบที่ 2: Iteration 2】 — คำนวณระยะทาง Euclidean สู่ Centroid ใหม่ (C1: C22,D22=(2,2) และ C2: C23,D23=(6.8,6.6))"
    ws["A25"].font = SUBBOLD

    headers_iter2 = [
        "รหัสนักศึกษา",
        "X1",
        "X2",
        "d(S, C1_new)",
        "d(S, C2_new)",
        "กลุ่มใหม่ (Cluster 2)",
        "d_min²",
        "สถานะการสลับกลุ่ม",
    ]
    _headers(ws, 26, headers_iter2, TEAL_FILL)

    for idx, (pname, x1, x2) in enumerate(data_points, start=27):
        prev_idx = idx - 17
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
        f_change = f'=IF(F{idx}=F{prev_idx}, "คงเดิม", "★ สลับกลุ่ม!")'

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
    ws["A37"] = "【Centroid หลังรอบที่ 2】: S4 (4, 4) ได้สลับจากกลุ่ม 2 ไปกลุ่ม 1 ทำให้พิกัดจุดกึ่งกลางเคลื่อนที่อีกครั้ง"
    ws["A37"].font = SUBBOLD

    _headers(ws, 38, ["กลุ่ม (Cluster)", "จำนวนสมาชิก", "Centroid X1 ใหม่", "Centroid X2 ใหม่", "จุดสมาชิกในกลุ่ม"], INDIGO_FILL)

    # C1 after iter 2: mean of S1..S4 = (10/4, 10/4) = (2.5, 2.5)
    ws["A39"] = "กลุ่ม 1 (Cluster 1)"
    ws["A39"].font = Font(name="Arial", bold=True)
    ws["A39"].border = THIN
    _blank(ws, "B39", solved, "=COUNTIF($F$27:$F$34, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C39", solved, "=AVERAGEIF($F$27:$F$34, 1, $B$27:$B$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D39", solved, "=AVERAGEIF($F$27:$F$34, 1, $C$27:$C$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E39"] = "S1, S2, S3, S4 (ได้พิกัดสมมาตร 2.50, 2.50)"
    ws["E39"].font = NOTE
    ws["E39"].border = THIN

    # C2 after iter 2: mean of S5..S8 = (30/4, 29/4) = (7.5, 7.25)
    ws["A40"] = "กลุ่ม 2 (Cluster 2)"
    ws["A40"].font = Font(name="Arial", bold=True)
    ws["A40"].border = THIN
    _blank(ws, "B40", solved, "=COUNTIF($F$27:$F$34, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C40", solved, "=AVERAGEIF($F$27:$F$34, 2, $B$27:$B$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D40", solved, "=AVERAGEIF($F$27:$F$34, 2, $C$27:$C$34)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E40"] = "S5, S6, S7, S8 (ได้พิกัด 7.50, 7.25)"
    ws["E40"].font = NOTE
    ws["E40"].border = THIN

    # Convergence & Evaluation Summary
    ws["A42"] = "【การตรวจสอบเงื่อนไขการลู่เข้า (Convergence Check) & สรุปผลสำหรับการสอบ】"
    ws["A42"].font = SUBBOLD

    summary_items = [
        ("A43", "จำนวนจุดที่เปลี่ยนกลุ่มในรอบที่ 2:", "D43", '=COUNTIF(H27:H34, "*สลับ*")', "จุด (จุด S4 สลับจาก 2 -> 1)"),
        ("A44", "การลดลงของ WCSS (รอบ 1 → รอบ 2):", "D44", "=G18-G35", "ค่าลดลงอย่างต่อเนื่อง"),
        ("A45", "สถานะการลู่เข้ารอบที่ 3 (Final State):", "D45", '="ลู่เข้าสมบูรณ์ (Converged) ที่ C1=(2.50, 2.50), C2=(7.50, 7.25), WCSS=17.75"', ""),
    ]
    for lbl_cell, lbl_text, val_cell, formula, unit in summary_items:
        ws[lbl_cell] = lbl_text
        ws[lbl_cell].font = Font(name="Arial", bold=True, size=10)
        ws.merge_cells(f"{lbl_cell}:{chr(ord(lbl_cell[0])+2)}{lbl_cell[1:]}")
        _blank(ws, val_cell, solved, formula, "0.0000" if "G18" in formula else "@", LIGHT_GREEN_FILL, Font(name="Arial", bold=True, color="065F46"))
        ws.merge_cells(f"{val_cell}:{chr(ord(val_cell[0])+3)}{val_cell[1:]}")

    ws["A47"] = "ข้อสังเกตและคำตอบเชิงวิเคราะห์สำหรับห้องสอบ:"
    ws["A47"].font = Font(name="Arial", bold=True)
    notes = [
        "1. ในรอบที่ 1 จุด S4 (4, 4) มีระยะทาง d(S4, C2) = 0 จึงสังกัดกลุ่ม 2",
        "2. แต่เมื่อ Centroid C2 ขยับขึ้นไปที่ (6.8, 6.6) ตามกลุ่มก้อนใหญ่ S5-S8 ทำให้ S4 อยู่ใกล้ C1=(2,2) มากกว่า จึงย้ายกลุ่มมาอยู่กลุ่ม 1",
        "3. WCSS ลดลงจาก 68.00 (รอบ 0) → 30.00 (รอบ 1) → 17.75 (รอบ 2) สะท้อนคุณสมบัติ Monotonic Convergence ของ K-Means",
    ]
    for r_idx, note_text in enumerate(notes, start=48):
        ws[f"A{r_idx}"] = note_text
        ws[f"A{r_idx}"].font = NOTE
        ws.merge_cells(f"A{r_idx}:I{r_idx}")

    _width(
        ws,
        {
            "A": 18,
            "B": 14,
            "C": 14,
            "D": 14,
            "E": 14,
            "F": 18,
            "G": 18,
            "H": 20,
            "I": 12,
        },
    )


# -------------------------------------------------------------------------
# SHEET 3: 02_Exam_Elbow_Analysis
# -------------------------------------------------------------------------
def build_exam_elbow(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "02_Exam_Elbow_Analysis"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "การวิเคราะห์วิธีข้อศอก (The Elbow Method) สำหรับการเลือกจำนวนคลัสเตอร์ K ในข้อสอบ"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:F1")

    ws["A3"] = "โจทย์: จงวิเคราะห์ตารางค่า WCSS ที่ค่า K ต่างๆ เพื่อหาค่า K ที่เหมาะสมที่สุด พร้อมแสดงเหตุผลทางคณิตศาสตร์"
    ws["A3"].font = NOTE
    ws.merge_cells("A3:F3")

    _headers(ws, 5, ["จำนวนคลัสเตอร์ (K)", "WCSS (Inertia)", "การลดลงของ WCSS (Δ WCSS)", "อัตราส่วนการลดลง (%)", "การประเมินผลสำหรับห้องสอบ"], TEAL_FILL)

    elbow_data = [
        (1, 112.88, "-", "-", "ทุกจุดรวมเป็น 1 กลุ่มใหญ่ (Centroid รวม = 5.00, 4.88)"),
        (2, 17.75, "=B6-B7", "=(B6-B7)/B6", "★ จุดข้อศอกที่เหมาะสม (Elbow Point): ลดลงถึง 84.28%"),
        (3, 11.75, "=B7-B8", "=(B7-B8)/B7", "อัตราการลดลงชะลอตัวลงอย่างชัดเจน (ลดลงเพียง 33.8%)"),
        (4, 7.50, "=B8-B9", "=(B8-B9)/B8", "กลุ่มย่อยเกินไป เสี่ยงต่อการ Overfitting"),
        (5, 4.50, "=B9-B10", "=(B9-B10)/B9", "กลุ่มเล็กเกินไปและสูญเสียความหมายในเชิงการจัดกลุ่ม"),
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
    chart.title = "Pre-Exam Review: Elbow Method Curve (WCSS vs K)"
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

    _width(ws, {"A": 22, "B": 18, "C": 24, "D": 22, "E": 52, "F": 10})


# -------------------------------------------------------------------------
# SHEET 4: 03_Exam_Theory_Q&A
# -------------------------------------------------------------------------
def build_exam_theory(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "03_Exam_Theory_Q&A"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "คำถามทบทวนเชิงทฤษฎีและข้อควรจำสำหรับห้องสอบ (K-Means Exam Q&A)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:F1")

    _headers(ws, 3, ["ข้อที่", "ประเด็นคำถามที่มักออกสอบ", "ตัวเลือกคำตอบ", "คำตอบของคุณ", "เฉลยและเหตุผลทางคณิตศาสตร์", "สถานะ"], INDIGO_FILL)

    questions = [
        (
            1,
            "เหตุใดการทำ Feature Scaling (เช่น StandardScaler) จึงเป็นขั้นตอนจำเป็นอย่างยิ่งก่อนนำข้อมูลเข้า K-Means?",
            "A: เพื่อให้ข้อมูลมีการกระจายตัวแบบ Normal เสมอ\nB: เพราะสูตร Euclidean Distance ไวต่อขนาดตัวเลข ฟีเจอร์ที่หน่วยใหญ่กว่าจะครอบงำผลลัพธ์ทั้งหมด\nC: เพื่อลดจำนวนจุดข้อมูลลงครึ่งหนึ่ง\nD: เพื่อป้องกันไม่ให้เกิดค่าติดลบ",
            "B",
            "ตอบ B: สูตร d = √∑(x₁ - c₁)² ใช้ผลต่างตัวเลขโดยตรง หากตัวแปรหนึ่งมีหน่วยเป็น 10,000 อีกตัวแปรมีหน่วยเป็น 1-5 ตัวแปรแรกจะกลายเป็นตัวตัดสิน 99.9% ของระยะทางทั้งหมด",
        ),
        (
            2,
            "หากรัน K-Means ซ้ำด้วยชุดข้อมูลเดิม แต่เปลี่ยนวิธีสุ่ม Centroid เริ่มต้น ผลลัพธ์ที่ได้จะเหมือนเดิมเสมอไปหรือไม่?",
            "A: เหมือนเดิมเสมอ เพราะ K-Means รับประกัน Global Optimum\nB: อาจไม่เหมือนเดิม เพราะ K-Means ลู่เข้าสู่ Local Optimum ตามจุดเริ่มต้น\nC: เหมือนเดิมถ้า K มีค่าน้อยกว่า 5\nD: ไม่เหมือนเดิมเฉพาะเมื่อข้อมูลมีมิติมากกว่า 10 มิติ",
            "B",
            "ตอบ B: Lloyd's Algorithm รับประกันเพียงว่าจะลู่เข้าสู่ Local Minimum หากจุดเริ่มต้นสุ่มตกไปอยู่ผิดกลุ่ม อาจเกิด bad clustering จึงเป็นที่มาของการคิดค้น K-Means++",
        ),
        (
            3,
            "อัลกอริทึม K-Means++ มีหลักการเลือกจุด Centroid ถัดไปอย่างไรหลังจากสุ่มจุดแรกแล้ว?",
            "A: เลือกจุดที่อยู่ใกล้จุดแรกมากที่สุด\nB: สุ่มแบบ Uniform Random จากจุดที่เหลือทั้งหมด\nC: เลือกด้วยความน่าจะเป็นที่แปรผันตามระยะทางกำลังสอง D(x)² จาก Centroid ที่ใกล้ที่สุด\nD: เลือกจุดที่มีค่าเฉลี่ยของทุกมิติสูงสุด",
            "C",
            "ตอบ C: K-Means++ ให้น้ำหนักความน่าจะเป็น P(x) ∝ D(x)² เพื่อบังคับให้จุดศูนย์กลางเริ่มต้นกระจายตัวห่างจากกันมากที่สุด ลดโอกาสติด Local Minima อย่างมีนัยสำคัญ",
        ),
        (
            4,
            "ชุดข้อมูลลักษณะใดต่อไปนี้ที่ K-Means จะทำงานล้มเหลว (ไม่เหมาะสมที่จะนำ K-Means ไปใช้งาน)?",
            "A: ข้อมูลที่กระจายตัวเป็นกลุ่มทรงกลม 3 กลุ่มที่มีขนาดใกล้เคียงกัน\nB: ข้อมูลลูกค้าห้างสรรพสินค้า 2 มิติที่ทำสเกลลิ่งแล้ว\nC: ข้อมูลรูปร่างวงกลมซ้อนกัน 2 ชั้น (Concentric Circles) หรือพระจันทร์เสี้ยว (Moons)\nD: ข้อมูลที่มีค่าตัวเลขจำนวนเต็มบวกทั้งหมด",
            "C",
            "ตอบ C: K-Means มีข้อสมมติฐานทางเรขาคณิตว่าคลัสเตอร์เป็นทรงกลม (Spherical & Convex) หากข้อมูลเป็นรูปร่างอิสระที่ซ้อนกัน K-Means จะตัดแบ่งด้วยเส้นตรง Voronoi ทำให้แยกกลุ่มผิด (ควรใช้ DBSCAN หรือ Spectral Clustering แทน)",
        ),
        (
            5,
            "ค่า Silhouette Score มีขอบเขตค่าอยู่ในช่วงใด และค่าที่ติดลบ (Negative Score) มีความหมายอย่างไร?",
            "A: ช่วง [0, 1] ค่าติดลบเป็นไปไม่ได้\nB: ช่วง [-1, 1] โดยค่าติดลบหมายถึงจุดนั้นถูกจัดกลุ่มผิด (อยู่ใกล้กลุ่มอื่นมากกว่ากลุ่มตัวเอง)\nC: ช่วง [-∞, +∞] ค่าติดลบหมายถึง WCSS มีค่าต่ำมาก\nD: ช่วง [0, 100%] ค่าติดลบหมายถึงโมเดลยังไม่ลู่เข้า",
            "B",
            "ตอบ B: Silhouette Score คำนวณจาก (b - a)/max(a, b) มีค่าระหว่าง -1 ถึง +1 หากค่าติดลบแสดงว่าระยะห่างเฉลี่ยสู่กลุ่มอื่น (b) สั้นกว่าระยะห่างสู่เพื่อนในกลุ่มตัวเอง (a) ซึ่งบ่งบอกว่าจัดกลุ่มผิดพลาด",
        ),
    ]

    for idx, (q_num, q_text, options, ans, explanation) in enumerate(questions, start=4):
        ws[f"A{idx}"] = f"ข้อที่ {q_num}"
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = q_text
        ws[f"B{idx}"].font = Font(name="Arial", size=10, bold=True)
        ws[f"B{idx}"].border = THIN
        ws[f"B{idx}"].alignment = WRAP

        ws[f"C{idx}"] = options
        ws[f"C{idx}"].font = Font(name="Arial", size=9)
        ws[f"C{idx}"].border = THIN
        ws[f"C{idx}"].alignment = WRAP

        # Column D: Student Answer
        ws[f"D{idx}"] = ans if solved else None
        ws[f"D{idx}"].font = BLUE
        ws[f"D{idx}"].fill = YELLOW_FILL
        ws[f"D{idx}"].alignment = CENTER
        ws[f"D{idx}"].border = THIN

        # Column E: Explanation
        ws[f"E{idx}"] = explanation if solved else "ซ่อนไว้สำหรับตรวจคำตอบหลังทำเสร็จ"
        ws[f"E{idx}"].font = Font(name="Arial", size=9, color="047857" if solved else "64748B")
        ws[f"E{idx}"].border = THIN
        ws[f"E{idx}"].alignment = WRAP

        # Column F: Auto checker formula
        if solved:
            ws[f"F{idx}"] = "ถูกต้อง (Correct)"
            ws[f"F{idx}"].font = SUCCESS
            ws[f"F{idx}"].fill = LIGHT_GREEN_FILL
        else:
            ws[f"F{idx}"] = f'=IF(D{idx}="","รอตอบ",IF(UPPER(D{idx})="{ans}","ถูกต้อง ✓","ยังไม่ถูก ✗"))'
            ws[f"F{idx}"].font = Font(name="Arial", bold=True)
            ws[f"F{idx}"].fill = LIGHT_AMBER_FILL
        ws[f"F{idx}"].alignment = CENTER
        ws[f"F{idx}"].border = THIN

        ws.row_dimensions[idx].height = 60

    _width(
        ws,
        {
            "A": 10,
            "B": 42,
            "C": 48,
            "D": 14,
            "E": 52,
            "F": 18,
        },
    )


def build(solved: bool) -> Workbook:
    wb = Workbook()
    build_exam_guide(wb.active)
    build_exam_calculation(wb.create_sheet(), solved=solved)
    build_exam_elbow(wb.create_sheet(), solved=solved)
    build_exam_theory(wb.create_sheet(), solved=solved)
    return wb


def main() -> None:
    student = OUT_DIR / "KMeans_Exam_Practice_TH.xlsx"
    solved = OUT_DIR / "KMeans_Exam_Practice_TH_Solved.xlsx"
    build(False).save(student)
    build(True).save(solved)
    print(f"Generated successfully: {student.name} and {solved.name}")


if __name__ == "__main__":
    main()
