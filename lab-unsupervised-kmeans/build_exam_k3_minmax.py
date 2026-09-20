#!/usr/bin/env python3
"""Generate Exam Workbooks for K-Means Clustering (K=3, Min-Max Normalization, 3 Iterations).

Creates:
1. KMeans_Exam_K3_MinMax_Practice.xlsx (Student test workbook with blank formula cells)
2. KMeans_Exam_K3_MinMax_Solved.xlsx (Instructor solution workbook with complete verified formulas and rubric)
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

OUT_DIR = Path(__file__).resolve().parent

# Color Palette & Styles
NAVY_FILL = PatternFill("solid", fgColor="1E3A5F")
TEAL_FILL = PatternFill("solid", fgColor="0F766E")
INDIGO_FILL = PatternFill("solid", fgColor="4338CA")
AMBER_FILL = PatternFill("solid", fgColor="D97706")
YELLOW_FILL = PatternFill("solid", fgColor="FFF3BF")
LIGHT_GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
LIGHT_BLUE_FILL = PatternFill("solid", fgColor="E0F2FE")
LIGHT_PURPLE_FILL = PatternFill("solid", fgColor="F3E8FF")
LIGHT_AMBER_FILL = PatternFill("solid", fgColor="FEF3C7")
ROSE_FILL = PatternFill("solid", fgColor="FFE4E6")
GRAY_FILL = PatternFill("solid", fgColor="F1F5F9")

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
RIGHT = Alignment(horizontal="right", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")


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


def _headers(ws: Worksheet, row: int, values: list[str], fill: PatternFill, start_col: int = 1) -> None:
    for idx, value in enumerate(values, start=start_col):
        cell = ws.cell(row=row, column=idx, value=value)
        cell.font = HEAD
        cell.fill = fill
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        cell.border = THIN
    ws.row_dimensions[row].height = 28


# -------------------------------------------------------------------------
# SHEET 1: 00_Exam_Instructions
# -------------------------------------------------------------------------
def build_instructions_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "00_Exam_Instructions"
    ws.views.sheetView[0].showGridLines = True

    status_tag = "【ฉบับเฉลยสำหรับอาจารย์ผู้ตรวจ - INSTRUCTOR KEY】" if solved else "【ฉบับข้อสอบสำหรับนักศึกษา - STUDENT EXAM】"
    ws["A1"] = f"ข้อสอบปฏิบัติการ: K-Means Clustering ด้วย Min-Max Normalization (K=3, 3 รอบ) {status_tag}"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:H1")

    lines = [
        "วิชา: Machine Learning / Data Mining (ข้อสอบภาคปฏิบัติการวิเคราะห์ข้อมูลด้วย Microsoft Excel)",
        "คำสั่งและข้อตกลงในการทำข้อสอบ:",
        "    1. ให้แสดงวิธีทำทุกขั้นตอนลงในแผ่นงาน (Worksheet) แต่ละแผ่นอย่างเคร่งครัด",
        "    2. เซลล์สีเหลือง + ตัวเลขสีน้ำเงิน = ข้อมูลและค่าคงที่โจทย์กำหนด ห้ามแก้ไข",
        "    3. เซลล์สีเหลืองว่าง = เซลล์ที่นักศึกษาต้องพิมพ์ 'สูตรคำนวณ Excel' ลงไป ห้ามพิมพ์ตัวเลขตรงๆ (Hard-code)",
        "    4. การอ้างอิงตำแหน่งเซลล์ต้องใช้การตรึงเซลล์ ($) ให้ถูกต้อง เพื่อให้สามารถคัดลอกสูตร (Drag-fill) ได้อย่างแม่นยำ",
        "    5. ค่าตัวเลขทศนิยมให้แสดงทศนิยม 4 ตำแหน่ง (เช่น 0.1234)",
        "โครงสร้างข้อสอบ (คะแนนเต็ม 100 คะแนน):",
        "    • แผ่นงาน 01 (01_MinMax_Scaling): การคำนวณสถิติพื้นฐาน และทำ Min-Max Normalization (20 คะแนน)",
        "    • แผ่นงาน 02 (02_KMeans_Iteration_1): การจัดกลุ่ม K-Means รอบที่ 1, คำนวณ WCSS, และหา Centroid ใหม่ (25 คะแนน)",
        "    • แผ่นงาน 03 (03_KMeans_Iteration_2): การจัดกลุ่ม K-Means รอบที่ 2 จาก Centroid ใหม่ของรอบ 1 (25 คะแนน)",
        "    • แผ่นงาน 04 (04_KMeans_Iteration_3): การจัดกลุ่ม K-Means รอบที่ 3, คำนวณ WCSS, และพิสูจน์การลู่เข้า (15 คะแนน)",
        "    • แผ่นงาน 05 (05_Analysis_and_Rubric): คำถามเชิงคิดวิเคราะห์ 3 ข้อ และเกณฑ์คะแนน (15 คะแนน)",
        "สรุปสูตรคณิตศาสตร์และสูตร Excel สำคัญที่ต้องใช้:",
        "    • Min-Max Normalization: X_norm = (X - Min) / (Max - Min)   [สูตร Excel: =(C6-$C$17)/$C$19 ]",
        "    • Euclidean Distance (2D): d(P, C) = √[(X₁ - C₁)² + (X₂ - C₂)²]   [สูตร Excel: =SQRT((C10-$B$5)^2 + (D10-$C$5)^2) ]",
        "    • Cluster Assignment: เลือกคลัสเตอร์ที่มีระยะทางสั้นที่สุด   [สูตร Excel: =IF(AND(E10<=F10, E10<=G10), 1, IF(F10<=G10, 2, 3)) ]",
        "    • WCSS / Inertia: ผลรวมของระยะทางต่ำสุดยกกำลังสอง ∑ (d_min)²   [สูตร Excel: =SUM(I10:I18) โดย I10=MIN(E10:G10)^2 ]",
        "    • New Centroid: ค่าเฉลี่ยของพิกัดในแต่ละคลัสเตอร์   [สูตร Excel: =AVERAGEIF($H$10:$H$18, 1, C$10:C$18) ]",
        "    • Convergence Check: คลัสเตอร์ไม่เปลี่ยนกลุ่ม และ Centroids หยุดการเคลื่อนที่ (ΔC = 0)",
    ]

    for idx, text in enumerate(lines, start=3):
        cell_ref = f"A{idx}"
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=10, bold=(idx in (3, 4, 10, 16)))
        if idx in (6, 7):
            ws[cell_ref].font = WARN
        ws.merge_cells(f"A{idx}:H{idx}")
        ws[cell_ref].alignment = WRAP
        ws.row_dimensions[idx].height = 24 if idx not in (4, 10, 16) else 28

    _width(ws, {"A": 110, "B": 15, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15, "H": 15})


# -------------------------------------------------------------------------
# SHEET 2: 01_MinMax_Scaling
# -------------------------------------------------------------------------
def build_minmax_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "01_MinMax_Scaling"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "ตอนที่ 1: การเตรียมข้อมูลและการทำ Min-Max Feature Scaling (ช่วง 0 ถึง 1)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    ws["A3"] = "【ตารางที่ 1.1: ข้อมูลดิบของลูกค้า 9 ราย (Raw Data: อายุ และ รายได้ต่อเดือน)】"
    ws["A3"].font = SUBBOLD
    ws.merge_cells("A3:D3")

    ws["F3"] = "【ตารางที่ 1.2: ข้อมูลหลังทำ Min-Max Normalization: สูตร (X - Min) / Range】"
    ws["F3"].font = SUBBOLD
    ws.merge_cells("F3:I3")

    # Headers for raw data (A5:D5)
    _headers(ws, 5, ["รหัสลูกค้า", "ชื่อลูกค้า", "อายุ (X1, ปี)", "รายได้ (X2, บาท)"], NAVY_FILL, start_col=1)

    raw_data = [
        ("P1", "สมคิด", 20, 15000),
        ("P2", "สมชาย", 24, 25000),
        ("P3", "สมหมาย", 28, 20000),
        ("P4", "กานดา", 36, 40000),
        ("P5", "เกศรา", 40, 40000),
        ("P6", "ขวัญใจ", 44, 45000),
        ("P7", "ฉัตรชัย", 52, 60000),
        ("P8", "ชัยวัฒน์", 56, 55000),
        ("P9", "ชูศักดิ์", 60, 65000),
    ]

    for idx, (pid, name, age, inc) in enumerate(raw_data, start=6):
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = name
        ws[f"B{idx}"].font = BLACK
        ws[f"B{idx}"].alignment = CENTER
        ws[f"B{idx}"].border = THIN

        _input(ws, f"C{idx}", age, CENTER)
        ws[f"C{idx}"].number_format = "0"

        _input(ws, f"D{idx}", inc, CENTER)
        ws[f"D{idx}"].number_format = "#,##0"

    # Headers for scaled data (F5:I5)
    _headers(ws, 5, ["รหัส", "Age_Norm (0-1)", "Income_Norm (0-1)", "สูตร Excel ที่ใช้คำนวณ"], INDIGO_FILL, start_col=6)

    for idx, (pid, name, age, inc) in enumerate(raw_data, start=6):
        ws[f"F{idx}"] = pid
        ws[f"F{idx}"].font = Font(name="Arial", bold=True)
        ws[f"F{idx}"].alignment = CENTER
        ws[f"F{idx}"].border = THIN

        f_age = f"=(C{idx}-$C$17)/$C$19"
        f_inc = f"=(D{idx}-$D$17)/$D$19"

        _blank(ws, f"G{idx}", solved, f_age, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_inc, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)

        ws[f"I{idx}"] = f"=(C{idx}-$C$17)/$C$19  |  =(D{idx}-$D$17)/$D$19" if solved else "[เขียนสูตร Min-Max Scaling ด้วยตนเอง]"
        ws[f"I{idx}"].font = NOTE
        ws[f"I{idx}"].border = THIN

    # Stats Table (A16:D19)
    _headers(ws, 16, ["ค่าทางสถิติ (Statistics)", "สูตร Excel", "อายุ (X1, ปี)", "รายได้ (X2, บาท)"], TEAL_FILL, start_col=1)

    stats = [
        (17, "Min (ค่าน้อยสุด)", "=MIN(C6:C14)", "=MIN(D6:D14)", "=MIN(C6:C14)", "=MIN(D6:D14)", "0", "#,##0"),
        (18, "Max (ค่ามากสุด)", "=MAX(C6:C14)", "=MAX(D6:D14)", "=MAX(C6:C14)", "=MAX(D6:D14)", "0", "#,##0"),
        (19, "Range (พิสัย = Max - Min)", "=C18-C17", "=D18-D17", "=C18-C17", "=D18-D17", "0", "#,##0"),
    ]

    for r_idx, label, f_hint_c, f_hint_d, f_val_c, f_val_d, fmt_c, fmt_d in stats:
        ws[f"A{r_idx}"] = label
        ws[f"A{r_idx}"].font = Font(name="Arial", bold=True, size=9)
        ws[f"A{r_idx}"].border = THIN

        ws[f"B{r_idx}"] = f"{f_hint_c}  |  {f_hint_d}" if solved else "[เขียนสูตรสถิติด้วยตนเอง]"
        ws[f"B{r_idx}"].font = NOTE
        ws[f"B{r_idx}"].border = THIN

        _blank(ws, f"C{r_idx}", solved, f_val_c, fmt_c, LIGHT_BLUE_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"D{r_idx}", solved, f_val_d, fmt_d, LIGHT_BLUE_FILL if solved else YELLOW_FILL, BLACK, CENTER)

    # Initial Centroids Table (A22:H26)
    ws["A22"] = "【ตารางที่ 1.3: จุดศูนย์กลางเริ่มต้นที่โจทย์กำหนด (Initial Centroids t=0 จากตัวอย่าง P1, P5, P9)】"
    ws["A22"].font = SUBBOLD
    ws.merge_cells("A22:H22")

    _headers(ws, 23, ["Centroid", "จากจุด", "ชื่อตัวอย่าง", "อายุจริง", "รายได้จริง", "X1_norm (เริ่มต้น)", "X2_norm (เริ่มต้น)", "นิยามกลุ่มลูกค้า"], NAVY_FILL, start_col=1)

    init_centroids = [
        (24, "C1 (กลุ่ม 1)", "P1", "สมคิด", 20, 15000, "=G6", "=H6", "กลุ่มวัยเริ่มทำงาน รายได้เริ่มต้น (Young - Entry Level)"),
        (25, "C2 (กลุ่ม 2)", "P5", "เกศรา", 40, 40000, "=G10", "=H10", "กลุ่มวัยทำงานมั่นคง รายได้ปานกลาง (Mid-Career - Moderate)"),
        (26, "C3 (กลุ่ม 3)", "P9", "ชูศักดิ์", 60, 65000, "=G14", "=H14", "กลุ่มวัยผู้ใหญ่ รายได้ระดับสูง (Senior - High Income)"),
    ]

    for r_idx, c_name, pid, name, age, inc, f_age_norm, f_inc_norm, desc in init_centroids:
        ws[f"A{r_idx}"] = c_name
        ws[f"A{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{r_idx}"].border = THIN

        _input(ws, f"B{r_idx}", pid, CENTER)

        ws[f"C{r_idx}"] = name
        ws[f"C{r_idx}"].font = BLACK
        ws[f"C{r_idx}"].alignment = CENTER
        ws[f"C{r_idx}"].border = THIN

        _input(ws, f"D{r_idx}", age, CENTER)
        ws[f"D{r_idx}"].number_format = "0"

        _input(ws, f"E{r_idx}", inc, CENTER)
        ws[f"E{r_idx}"].number_format = "#,##0"

        _blank(ws, f"F{r_idx}", solved, f_age_norm, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"G{r_idx}", solved, f_inc_norm, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)

        ws[f"H{r_idx}"] = desc
        ws[f"H{r_idx}"].font = NOTE
        ws[f"H{r_idx}"].border = THIN

    _width(
        ws,
        {
            "A": 14,
            "B": 14,
            "C": 15,
            "D": 18,
            "E": 12,
            "F": 12,
            "G": 18,
            "H": 18,
            "I": 42,
        },
    )


# -------------------------------------------------------------------------
# Helper for Iteration Sheets (Rounds 1, 2, 3)
# -------------------------------------------------------------------------
def build_iteration_sheet(
    ws: Worksheet,
    round_num: int,
    sheet_title: str,
    centroid_source_desc: str,
    c_refs: list[tuple[str, str]],  # [(ref_x, ref_y), ...]
    *,
    solved: bool,
    prev_sheet_name: str | None = None,
) -> None:
    ws.title = sheet_title
    ws.views.sheetView[0].showGridLines = True

    status_tag = "(เฉลย)" if solved else "(โจทย์)"
    ws["A1"] = f"ตอนที่ {round_num + 1}: การคำนวณ K-Means รอบที่ {round_num} (Iteration {round_num}) {status_tag}"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:J1")

    # Centroids Used in this round (A3:D7)
    ws["A3"] = f"【ตารางที่ {round_num}.1: จุดศูนย์กลาง Centroids ที่ใช้ในรอบที่ {round_num} ({centroid_source_desc})】"
    ws["A3"].font = SUBBOLD
    ws.merge_cells("A3:F3")

    _headers(ws, 4, ["Centroid", "X1_norm (แกนอายุ)", "X2_norm (แกนรายได้)", "แหล่งที่มาของค่าพิกัด"], NAVY_FILL, start_col=1)

    c_labels = [("C1", c_refs[0][0], c_refs[0][1]), ("C2", c_refs[1][0], c_refs[1][1]), ("C3", c_refs[2][0], c_refs[2][1])]

    for idx, (c_name, ref_x, ref_y) in enumerate(c_labels, start=5):
        ws[f"A{idx}"] = c_name
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _blank(ws, f"B{idx}", solved, ref_x, "0.0000", LIGHT_BLUE_FILL, BLACK, CENTER)
        _blank(ws, f"C{idx}", solved, ref_y, "0.0000", LIGHT_BLUE_FILL, BLACK, CENTER)

        ws[f"D{idx}"] = f"พิกัด {c_name} ต้นรอบที่ {round_num} (อ้างอิง: {ref_x})" if solved else f"เชื่อมโยงพิกัด {c_name} จาก Centroid ใหม่รอบก่อนหน้า"
        ws[f"D{idx}"].font = NOTE
        ws[f"D{idx}"].border = THIN

    # Distance & Assignment Table (A9:J18)
    ws["A9"] = f"【ตารางที่ {round_num}.2: คำนวณระยะทาง Euclidean สู่ Centroid, การจัดกลุ่ม (Assignment), และ WCSS】"
    ws["A9"].font = SUBBOLD
    ws.merge_cells("A9:J9")

    headers_table = [
        "รหัส",
        "ชื่อลูกค้า",
        "Age_Norm (X1)",
        "Income_Norm (X2)",
        "d(P, C1)",
        "d(P, C2)",
        "d(P, C3)",
        "กลุ่มที่ได้ (Cluster)",
        "d_min²",
        "สถานะกลุ่ม / คำอธิบาย",
    ]
    _headers(ws, 10, headers_table, TEAL_FILL, start_col=1)

    raw_names = ["สมคิด", "สมชาย", "สมหมาย", "กานดา", "เกศรา", "ขวัญใจ", "ฉัตรชัย", "ชัยวัฒน์", "ชูศักดิ์"]

    for i in range(9):
        r_idx = 11 + i
        pid = f"P{i+1}"
        name = raw_names[i]

        ws[f"A{r_idx}"] = pid
        ws[f"A{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{r_idx}"].alignment = CENTER
        ws[f"A{r_idx}"].border = THIN

        ws[f"B{r_idx}"] = name
        ws[f"B{r_idx}"].font = BLACK
        ws[f"B{r_idx}"].alignment = CENTER
        ws[f"B{r_idx}"].border = THIN

        # Pull normalized coords from 01_MinMax_Scaling
        src_row = 6 + i
        ws[f"C{r_idx}"] = f"='01_MinMax_Scaling'!G{src_row}"
        ws[f"C{r_idx}"].font = BLACK
        ws[f"C{r_idx}"].alignment = CENTER
        ws[f"C{r_idx}"].border = THIN
        ws[f"C{r_idx}"].number_format = "0.0000"

        ws[f"D{r_idx}"] = f"='01_MinMax_Scaling'!H{src_row}"
        ws[f"D{r_idx}"].font = BLACK
        ws[f"D{r_idx}"].alignment = CENTER
        ws[f"D{r_idx}"].border = THIN
        ws[f"D{r_idx}"].number_format = "0.0000"

        # Euclidean Distances to C1 ($B$5, $C$5), C2 ($B$6, $C$6), C3 ($B$7, $C$7)
        f_d1 = f"=SQRT((C{r_idx}-$B$5)^2 + (D{r_idx}-$C$5)^2)"
        f_d2 = f"=SQRT((C{r_idx}-$B$6)^2 + (D{r_idx}-$C$6)^2)"
        f_d3 = f"=SQRT((C{r_idx}-$B$7)^2 + (D{r_idx}-$C$7)^2)"

        # Assignment Formula
        f_assign = f"=IF(AND(E{r_idx}<=F{r_idx}, E{r_idx}<=G{r_idx}), 1, IF(F{r_idx}<=G{r_idx}, 2, 3))"
        f_dmin_sq = f"=MIN(E{r_idx}:G{r_idx})^2"

        if round_num == 1:
            f_status = f'=IF(H{r_idx}=1, "กลุ่ม 1 (C1)", IF(H{r_idx}=2, "กลุ่ม 2 (C2)", "กลุ่ม 3 (C3)"))'
        else:
            f_status = f'=IF(H{r_idx}=\'{prev_sheet_name}\'!H{r_idx}, "✓ คงเดิม (กลุ่ม " & H{r_idx} & ")", "⚠️ เปลี่ยนกลุ่มเป็น " & H{r_idx})'

        _blank(ws, f"E{r_idx}", solved, f_d1, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{r_idx}", solved, f_d2, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"G{r_idx}", solved, f_d3, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{r_idx}", solved, f_assign, "0", LIGHT_AMBER_FILL if solved else YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
        _blank(ws, f"I{r_idx}", solved, f_dmin_sq, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"J{r_idx}", solved, f_status, "@", GRAY_FILL, BLACK, CENTER)

    # WCSS Total Row (Row 20)
    ws["A20"] = f"ผลรวม WCSS รอบที่ {round_num} (Inertia = ∑ d_min²):"
    ws["A20"].font = Font(name="Arial", bold=True, size=11)
    ws.merge_cells("A20:H20")
    ws["A20"].alignment = RIGHT
    ws["A20"].border = DOUBLE_BOTTOM

    for col in ["B", "C", "D", "E", "F", "G", "H"]:
        ws[f"{col}20"].border = DOUBLE_BOTTOM

    _blank(ws, "I20", solved, "=SUM(I11:I19)", "0.000000", ROSE_FILL, Font(name="Arial", bold=True, size=11), CENTER)
    ws["I20"].border = DOUBLE_BOTTOM

    if round_num > 1 and prev_sheet_name:
        ws["J20"] = f"='{prev_sheet_name}'!I20 - I20" if solved else None
        ws["J20"].font = Font(name="Arial", bold=True, color="047857", size=9)
        ws["J20"].alignment = CENTER
        ws["J20"].border = DOUBLE_BOTTOM
        ws["J20"].number_format = '"ลดลง "0.0000;;"คงเดิม (0.0000)"'
    else:
        ws["J20"] = "ค่าเริ่มต้นรอบ 1" if solved else None
        ws["J20"].font = NOTE
        ws["J20"].alignment = CENTER
        ws["J20"].border = DOUBLE_BOTTOM

    # Updated Centroids Table (A22:F26)
    ws["A22"] = f"【ตารางที่ {round_num}.3: การคำนวณจุดศูนย์กลางใหม่หลังจบรอบที่ {round_num} (Update Centroids: หาค่าเฉลี่ย AVERAGEIF)】"
    ws["A22"].font = SUBBOLD
    ws.merge_cells("A22:F22")

    _headers(ws, 23, ["Centroid ใหม่", "จำนวนสมาชิก (N)", "X1_norm ใหม่ (เฉลี่ย)", "X2_norm ใหม่ (เฉลี่ย)", "สูตร Excel ที่ใช้", "การเคลื่อนที่ (Shift)"], INDIGO_FILL, start_col=1)

    for k in range(1, 4):
        r_idx = 23 + k
        c_name = f"C{k} (ใหม่)"
        f_count = f"=COUNTIF($H$11:$H$19, {k})"
        f_mean_x1 = f"=AVERAGEIF($H$11:$H$19, {k}, C$11:C$19)"
        f_mean_x2 = f"=AVERAGEIF($H$11:$H$19, {k}, D$11:D$19)"
        f_hint = f"=AVERAGEIF($H$11:$H$19, {k}, C$11:C$19)"
        f_shift = f"=SQRT((C{r_idx}-$B${4+k})^2 + (D{r_idx}-$C${4+k})^2)"

        ws[f"A{r_idx}"] = c_name
        ws[f"A{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{r_idx}"].alignment = CENTER
        ws[f"A{r_idx}"].border = THIN

        _blank(ws, f"B{r_idx}", solved, f_count, "0", LIGHT_BLUE_FILL, BLACK, CENTER)
        _blank(ws, f"C{r_idx}", solved, f_mean_x1, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
        _blank(ws, f"D{r_idx}", solved, f_mean_x2, "0.0000", LIGHT_GREEN_FILL if solved else YELLOW_FILL, Font(name="Arial", bold=True), CENTER)

        ws[f"E{r_idx}"] = f_hint if solved else "[เขียนสูตรคำนวณค่าเฉลี่ย AVERAGEIF]"
        ws[f"E{r_idx}"].font = NOTE
        ws[f"E{r_idx}"].border = THIN

        _blank(ws, f"F{r_idx}", solved, f_shift, "0.0000", GRAY_FILL, BLACK, CENTER)

    # If round 3, add Convergence Assessment Section
    if round_num == 3:
        ws["A28"] = "【ตารางที่ 3.4: การตรวจสอบและสรุปผลการลู่เข้าของอัลกอริทึม (Convergence Assessment)】"
        ws["A28"].font = SUBBOLD
        ws.merge_cells("A28:F28")

        _headers(ws, 29, ["เกณฑ์การตรวจสอบ (Convergence Criteria)", "ค่าที่ได้จากการคำนวณ", "เกณฑ์การตัดสิน", "ผลการประเมิน", "ความหมาย"], NAVY_FILL, start_col=1)

        conv_items = [
            (30, "1. การเปลี่ยนกลุ่มของข้อมูล (Reassignments)", '=COUNTIF(J11:J19, "*เปลี่ยนกลุ่ม*") & " จุด"', "ต้องเท่ากับ 0 จุด", "ผ่าน (ไม่มีจุดใดย้ายกลุ่ม)", "คลัสเตอร์คงที่ 100%"),
            (31, "2. การเคลื่อนที่ของ Centroids (Total Shift ΔC)", "=F24+F25+F26", "ΔC = 0.0000", "ผ่าน (Centroids หยุดการเคลื่อนที่)", "จุดศูนย์กลางนิ่งสนิท"),
            (32, "3. การเปลี่ยนแปลงของ WCSS (ΔWCSS)", "='03_KMeans_Iteration_2'!I20 - I20", "ΔWCSS = 0.0000", "ผ่าน (WCSS คงที่)", "ฟังก์ชันเป้าหมายลู่เข้าสู่จุดต่ำสุด"),
        ]

        for r_idx, crit, val_f, req, eval_res, interp in conv_items:
            ws[f"A{r_idx}"] = crit
            ws[f"A{r_idx}"].font = Font(name="Arial", bold=True, size=9)
            ws[f"A{r_idx}"].border = THIN

            _blank(ws, f"B{r_idx}", solved, val_f, "0.0000", LIGHT_BLUE_FILL, BLACK, CENTER)

            ws[f"C{r_idx}"] = req
            ws[f"C{r_idx}"].alignment = CENTER
            ws[f"C{r_idx}"].border = THIN
            ws[f"C{r_idx}"].font = NOTE

            ws[f"D{r_idx}"] = eval_res if solved else None
            ws[f"D{r_idx}"].font = SUCCESS
            ws[f"D{r_idx}"].alignment = CENTER
            ws[f"D{r_idx}"].border = THIN
            ws[f"D{r_idx}"].fill = LIGHT_GREEN_FILL

            ws[f"E{r_idx}"] = interp if solved else None
            ws[f"E{r_idx}"].font = NOTE
            ws[f"E{r_idx}"].border = THIN

        ws["A34"] = "★ สรุปผลการทดสอบ: อัลกอริทึม K-Means บรรลุภาวะการลู่เข้า (Convergence) โดยสมบูรณ์ในรอบที่ 3 ไม่จำเป็นต้องทำรอบต่อไป"
        ws["A34"].font = Font(name="Arial", bold=True, color="047857", size=11)
        ws.merge_cells("A34:F34")

    _width(
        ws,
        {
            "A": 16,
            "B": 15,
            "C": 18,
            "D": 22,
            "E": 14,
            "F": 14,
            "G": 14,
            "H": 18,
            "I": 15,
            "J": 26,
        },
    )


# -------------------------------------------------------------------------
# SHEET 6: 05_Analysis_and_Rubric
# -------------------------------------------------------------------------
def build_analysis_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "05_Analysis_and_Rubric"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "ตอนที่ 5: คำถามเชิงคิดวิเคราะห์และการประยุกต์ใช้จริง (Conceptual & Business Questions)"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:G1")

    # Q1
    ws["A3"] = "【ข้อที่ 1】 ปัญหาของสเกลข้อมูล (The Scale Dominance Problem) [5 คะแนน]"
    ws["A3"].font = SUBBOLD
    ws.merge_cells("A3:G3")

    ws["A4"] = "คำถาม: หากนำข้อมูลดิบของลูกค้าทั้ง 9 คน (อายุ 20-60 ปี และ รายได้ 15,000-65,000 บาท) ไปคำนวณ K-Means โดย 'ไม่ทำ Feature Scaling' จะส่งผลเสียอย่างไรต่อการวัดระยะทางและการจัดกลุ่ม? อธิบายเชิงคณิตศาสตร์อย่างชัดเจน"
    ws["A4"].font = BLACK
    ws["A4"].alignment = WRAP
    ws.merge_cells("A4:G4")
    ws.row_dimensions[4].height = 36

    ws["A5"] = "แนวคำตอบเฉลย:" if solved else "พื้นที่พิมพ์คำตอบของนักศึกษา:"
    ws["A5"].font = Font(name="Arial", bold=True, color="047857" if solved else "0000FF")

    ans1_text = (
        "แนวคำตอบที่สมบูรณ์ (5/5 คะแนน):\n"
        "1. ในสูตร Euclidean Distance: d = √[(X_age - C_age)² + (X_income - C_income)²]\n"
        "2. ตัวแปร 'อายุ' มีผลต่างยกกำลังสองสูงสุดเพียง (60 - 20)² = 1,600\n"
        "3. ในขณะที่ตัวแปร 'รายได้' มีผลต่างยกกำลังสองสูงสุดถึง (65,000 - 15,000)² = 2,500,000,000 (ต่างกันกว่า 1.5 ล้านเท่า!)\n"
        "4. ผลลัพธ์: ตัวแปรรายได้จะครอบงำ (Dominate) ระยะทางทั้งหมด ทำให้ K-Means จัดกลุ่มตามรายได้เพียงอย่างเดียว และมองไม่เห็นความแตกต่างของอายุเลย\n"
        "5. การทำ Min-Max Normalization จึงจำเป็นอย่างยิ่งในการปรับทั้งสองแกนให้อยู่ในช่วง [0, 1] เท่ากัน เพื่อให้ทั้งสองฟีเจอร์มีน้ำหนักในการตัดสินใจอย่างยุติธรรม"
        if solved
        else "(ให้นักศึกษาอธิบายผลกระทบของขนาดตัวเลขต่อสูตร Euclidean Distance และการครอบงำของตัวแปรรายได้)"
    )
    ws["A6"] = ans1_text
    ws["A6"].font = Font(name="Arial", size=9) if solved else NOTE
    ws["A6"].fill = LIGHT_GREEN_FILL if solved else YELLOW_FILL
    ws["A6"].border = THIN
    ws["A6"].alignment = WRAP
    ws.merge_cells("A6:G6")
    ws.row_dimensions[6].height = 95

    # Q2
    ws["A8"] = "【ข้อที่ 2】 การแปลความหมายกลุ่มลูกค้าและกลยุทธ์ทางธุรกิจ (Customer Segmentation Insights) [5 คะแนน]"
    ws["A8"].font = SUBBOLD
    ws.merge_cells("A8:G8")

    ws["A9"] = "คำถาม: จากผลลัพธ์การจัดกลุ่มทั้ง 3 กลุ่ม (Cluster 1, 2, 3) ในรอบที่ 3 จงอธิบายคุณลักษณะเด่นของลูกค้าแต่ละกลุ่ม (Customer Persona) พร้อมเสนอแนะผลิตภัณฑ์หรือกลยุทธ์ทางการตลาดที่เหมาะสม 1 กลยุทธ์ต่อกลุ่ม"
    ws["A9"].font = BLACK
    ws["A9"].alignment = WRAP
    ws.merge_cells("A9:G9")
    ws.row_dimensions[9].height = 36

    ws["A10"] = "แนวคำตอบเฉลย:" if solved else "พื้นที่พิมพ์คำตอบของนักศึกษา:"
    ws["A10"].font = Font(name="Arial", bold=True, color="047857" if solved else "0000FF")

    ans2_text = (
        "แนวคำตอบที่สมบูรณ์ (5/5 คะแนน):\n"
        "• กลุ่มที่ 1 (P1, P2, P3): 'First Jobber / วัยเริ่มทำงาน รายได้เริ่มต้น' (อายุเฉลี่ย 24 ปี, รายได้เฉลี่ย 20,000 บ.)\n"
        "   → กลยุทธ์: บัตรเครดิตใบแรกค่าธรรมเนียมฟรี, สินเชื่อดิจิทัลผ่อนสินค้าดอกเบี้ยต่ำ, แอปออมเงินอัตโนมัติ\n"
        "• กลุ่มที่ 2 (P4, P5, P6): 'Mid-Career / วัยสร้างครอบครัว รายได้ปานกลาง' (อายุเฉลี่ย 40 ปี, รายได้เฉลี่ย 41,667 บ.)\n"
        "   → กลยุทธ์: สินเชื่อบ้าน/รถยนต์, ประกันชีวิตคุ้มครองครอบครัว, กองทุนรวมเพื่อการลดหย่อนภาษี (SSF/RMF)\n"
        "• กลุ่มที่ 3 (P7, P8, P9): 'Senior Wealth / วัยผู้ใหญ่มั่นคง รายได้สูง' (อายุเฉลี่ย 56 ปี, รายได้เฉลี่ย 60,000 บ.)\n"
        "   → กลยุทธ์: บริการ Wealth Management / Private Banking, ประกันสุขภาพเหมาจ่ายพรีเมียม, วางแผนส่งต่อมรดก"
        if solved
        else "(ให้นักศึกษาสรุปพฤติกรรมลูกค้าทั้ง 3 กลุ่ม พร้อมเสนอแนวทางการตลาดที่สอดคล้องกับโปรไฟล์ของลูกค้า)"
    )
    ws["A11"] = ans2_text
    ws["A11"].font = Font(name="Arial", size=9) if solved else NOTE
    ws["A11"].fill = LIGHT_GREEN_FILL if solved else YELLOW_FILL
    ws["A11"].border = THIN
    ws["A11"].alignment = WRAP
    ws.merge_cells("A11:G11")
    ws.row_dimensions[11].height = 105

    # Q3
    ws["A13"] = "【ข้อที่ 3】 ภาวะการลู่เข้าและเงื่อนไขการหยุด (Convergence & Stopping Criteria) [5 คะแนน]"
    ws["A13"].font = SUBBOLD
    ws.merge_cells("A13:G13")

    ws["A14"] = "คำถาม: ในการรัน K-Means รอบที่ 3 พบว่าค่า Centroids และการจัดกลุ่มเหมือนกับรอบที่ 2 ทุกประการ จงอธิบายว่าทำไมอัลกอริทึมจึงหยุดทำงาน และหากเขียนโค้ดภาษา Python เอง จะตั้งเงื่อนไขการหยุด (Stopping Criteria) อย่างไรได้บ้าง?"
    ws["A14"].font = BLACK
    ws["A14"].alignment = WRAP
    ws.merge_cells("A14:G14")
    ws.row_dimensions[14].height = 36

    ws["A15"] = "แนวคำตอบเฉลย:" if solved else "พื้นที่พิมพ์คำตอบของนักศึกษา:"
    ws["A15"].font = Font(name="Arial", bold=True, color="047857" if solved else "0000FF")

    ans3_text = (
        "แนวคำตอบที่สมบูรณ์ (5/5 คะแนน):\n"
        "1. เหตุผลที่หยุด: เมื่อการจัดกลุ่มไม่เปลี่ยน จุดศูนย์กลางใหม่ที่คำนวณได้ก็จะอยู่ที่เดิม (ΔC = 0) และ WCSS จะคงที่ หากทำรอบต่อไปผลลัพธ์ก็จะเหมือนเดิม 100% จึงถือว่าเข้าสู่ภาวะเสถียร (Convergence)\n"
        "2. เงื่อนไขการหยุด (Stopping Criteria) 3 ข้อที่นิยมใช้ในการเขียนโปรแกรม:\n"
        "   • No Reassignment: สมาชิกในทุกคลัสเตอร์ไม่มีการย้ายกลุ่มเลย (np.array_equal(prev_labels, current_labels))\n"
        "   • Centroid Tolerance: การขยับของ Centroid น้อยกว่าค่าพิกัดความคลาดเคลื่อนที่กำหนด เช่น ||C_new - C_old|| < 1e-4 (tol)\n"
        "   • Max Iterations: กำหนดรอบสูงสุดป้องกัน Infinite Loop เช่น max_iter=300 กรณีข้อมูลแกว่งตัว"
        if solved
        else "(ให้นักศึกษาอธิบายกลไกทางคณิตศาสตร์ของการลู่เข้า และเงื่อนไข Stopping Criteria 3 ประการ)"
    )
    ws["A16"] = ans3_text
    ws["A16"].font = Font(name="Arial", size=9) if solved else NOTE
    ws["A16"].fill = LIGHT_GREEN_FILL if solved else YELLOW_FILL
    ws["A16"].border = THIN
    ws["A16"].alignment = WRAP
    ws.merge_cells("A16:G16")
    ws.row_dimensions[16].height = 95

    # RUBRIC TABLE
    ws["A18"] = "【ตารางเกณฑ์การให้คะแนนอย่างละเอียด (Grading Rubric รวม 100 คะแนน)】"
    ws["A18"].font = SUBBOLD
    ws.merge_cells("A18:G18")

    _headers(ws, 19, ["ส่วนของข้อสอบ", "หัวข้อประเมิน", "คะแนนเต็ม", "เกณฑ์การได้คะแนนเต็ม", "ข้อผิดพลาดที่มักถูกหักคะแนน"], NAVY_FILL, start_col=1)

    rubric_rows = [
        ("ตอนที่ 1 (Scaling)", "สถิติ Min, Max, Range", 6, "ใช้สูตร MIN, MAX, และผลต่างได้ถูกต้องทั้ง 2 ตัวแปร", "พิมพ์ตัวเลขตรงๆ โดยไม่ใช้สูตร (-2)"),
        ("ตอนที่ 1 (Scaling)", "สูตร Min-Max Normalization", 10, "ใช้สูตร =(X-Min)/Range และตรึง $ เซลล์ Min/Range ถูกต้อง", "ไม่ตรึง $ เซลล์ทำให้ลากสูตรแล้วเพี้ยน (-5)"),
        ("ตอนที่ 1 (Scaling)", "พิกัด Initial Centroids (t=0)", 4, "อ้างอิงค่าพิกัดจาก P1, P5, P9 ในตารางที่ทำ Scaling แล้วได้ถูกต้อง", "ดึงค่าจากข้อมูลดิบมาใส่โดยไม่ได้ดึงจากสเกล 0-1 (-3)"),
        ("ตอนที่ 2 (Round 1)", "ระยะทาง Euclidean สู่ C1, C2, C3", 10, "ใช้สูตร =SQRT((X1-$Bx)^2+(X2-$By)^2) ตรึง Centroid ถูกต้อง", "ลืมยกกำลังสอง หรือตรึงแถว/หลัก Centroid ผิด (-4)"),
        ("ตอนที่ 2 (Round 1)", "การจัดกลุ่ม Cluster Assignment", 5, "ใช้สูตร IF/AND หรือ MATCH/MIN เพื่อเลือกกลุ่มระยะทางต่ำสุด", "จัดกลุ่มผิด หรือไม่ได้ใช้สูตรอัตโนมัติ (-3)"),
        ("ตอนที่ 2 (Round 1)", "การคำนวณ WCSS และ New Centroids", 10, "คำนวณ d_min² และ SUM ถูกต้อง (0.2300) พร้อมเฉลี่ยจุดใหม่ด้วย AVERAGEIF", "ลืมยกกำลังสองระยะทางก่อนรวม WCSS (-4)"),
        ("ตอนที่ 3 (Round 2)", "การนำ Centroid ใหม่มาคำนวณต่อ", 10, "ดึง New Centroids จากรอบ 1 มาเป็น Centroid ตั้งต้นของรอบ 2", "นำ Initial Centroid เดิมมาคำนวณซ้ำ (-8)"),
        ("ตอนที่ 3 (Round 2)", "ระยะทาง, การจัดกลุ่ม, WCSS รอบ 2", 10, "คำนวณระยะทางใหม่ถูกต้อง ได้ WCSS ลดลงเหลือ 0.1067", "คำนวณระยะทางผิด หรือไม่ได้อัปเดต Centroid (-5)"),
        ("ตอนที่ 3 (Round 2)", "การอัปเดต New Centroids รอบ 2", 5, "คำนวณ New Centroids รอบ 2 ถูกต้อง (C1: 0.1,0.1 | C2: 0.5,0.5333 | C3: 0.9,0.9)", "คำนวณค่าเฉลี่ยผิด (-3)"),
        ("ตอนที่ 4 (Round 3)", "การคำนวณรอบ 3 และ WCSS", 10, "คำนวณระยะทางรอบ 3 ถูกต้อง ได้ WCSS = 0.1067 เท่าเดิม", "คำนวณผิดพลาด (-5)"),
        ("ตอนที่ 4 (Round 3)", "การตรวจสอบ Convergence", 5, "ตรวจสอบและสรุปครบ 3 มิติ: จุดไม่ย้ายกลุ่ม, ΔC=0, ΔWCSS=0", "สรุปเพียงว่ากลุ่มเหมือนเดิมโดยไม่อ้างอิง Centroid (-2)"),
        ("ตอนที่ 5 (วิเคราะห์)", "ข้อ 1: Scale Dominance Problem", 5, "อธิบายการครอบงำของหน่วยรายได้หลักหมื่นต่ออายุหลักสิบเชิงคณิตศาสตร์", "ตอบไม่ตรงประเด็นหรือไม่พูดถึง Euclidean Distance (-2)"),
        ("ตอนที่ 5 (วิเคราะห์)", "ข้อ 2: Customer Personas & Strategy", 5, "บรรยายคุณลักษณะของทั้ง 3 กลุ่มได้สอดคล้องกับพฤติกรรมจริง พร้อมเสนอกลยุทธ์", "เสนอแนะกลยุทธ์ไม่ตรงกับกลุ่มเป้าหมาย (-2)"),
        ("ตอนที่ 5 (วิเคราะห์)", "ข้อ 3: Stopping Criteria", 5, "อธิบายกลไกการลู่เข้าและระบุเงื่อนไขการหยุด 3 ประการได้ชัดเจน", "ระบุเงื่อนไขการหยุดไม่ครบถ้วน (-2)"),
    ]

    for idx, (part, topic, pts, criteria, mistake) in enumerate(rubric_rows, start=20):
        ws[f"A{idx}"] = part
        ws[f"A{idx}"].font = Font(name="Arial", bold=True, size=9)
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = topic
        ws[f"B{idx}"].font = BLACK
        ws[f"B{idx}"].border = THIN

        ws[f"C{idx}"] = pts
        ws[f"C{idx}"].font = Font(name="Arial", bold=True)
        ws[f"C{idx}"].alignment = CENTER
        ws[f"C{idx}"].border = THIN

        ws[f"D{idx}"] = criteria
        ws[f"D{idx}"].font = NOTE
        ws[f"D{idx}"].border = THIN

        ws[f"E{idx}"] = mistake
        ws[f"E{idx}"].font = Font(name="Arial", italic=True, color="B91C1C", size=9)
        ws[f"E{idx}"].border = THIN

    # Total Score Row (Row 34)
    ws["A34"] = "คะแนนรวมทั้งสิ้น:"
    ws["A34"].font = BOLD
    ws.merge_cells("A34:B34")
    ws["A34"].alignment = RIGHT
    ws["A34"].border = DOUBLE_BOTTOM

    ws["C34"] = 100
    ws["C34"].font = Font(name="Arial", bold=True, size=13, color="B91C1C")
    ws["C34"].alignment = CENTER
    ws["C34"].fill = LIGHT_AMBER_FILL
    ws["C34"].border = DOUBLE_BOTTOM

    ws["D34"] = "ข้อสอบ 5 ตอน ครอบคลุมทั้งทฤษฎี การปฏิบัติการด้วย Excel และการคิดวิเคราะห์เชิงธุรกิจ"
    ws["D34"].font = NOTE
    ws.merge_cells("D34:E34")
    ws["D34"].border = DOUBLE_BOTTOM

    _width(
        ws,
        {
            "A": 22,
            "B": 32,
            "C": 12,
            "D": 50,
            "E": 45,
            "F": 15,
            "G": 15,
        },
    )


# -------------------------------------------------------------------------
# BUILD WORKBOOKS
# -------------------------------------------------------------------------
def create_exam_workbooks() -> tuple[Path, Path]:
    for solved in (False, True):
        wb = Workbook()
        wb.remove(wb.active)  # remove default sheet

        # Sheet 00: Instructions
        ws_inst = wb.create_sheet()
        build_instructions_sheet(ws_inst, solved=solved)

        # Sheet 01: MinMax Scaling
        ws_scale = wb.create_sheet()
        build_minmax_sheet(ws_scale, solved=solved)

        # Sheet 02: Iteration 1
        ws_r1 = wb.create_sheet()
        build_iteration_sheet(
            ws_r1,
            round_num=1,
            sheet_title="02_KMeans_Iteration_1",
            centroid_source_desc="Initial Seeds t=0: P1, P5, P9 จากชีต 01",
            c_refs=[
                ("='01_MinMax_Scaling'!F24", "='01_MinMax_Scaling'!G24"),
                ("='01_MinMax_Scaling'!F25", "='01_MinMax_Scaling'!G25"),
                ("='01_MinMax_Scaling'!F26", "='01_MinMax_Scaling'!G26"),
            ],
            solved=solved,
        )

        # Sheet 03: Iteration 2
        ws_r2 = wb.create_sheet()
        build_iteration_sheet(
            ws_r2,
            round_num=2,
            sheet_title="03_KMeans_Iteration_2",
            centroid_source_desc="Updated Centroids จาก New C1, C2, C3 ของรอบที่ 1",
            c_refs=[
                ("='02_KMeans_Iteration_1'!C24", "='02_KMeans_Iteration_1'!D24"),
                ("='02_KMeans_Iteration_1'!C25", "='02_KMeans_Iteration_1'!D25"),
                ("='02_KMeans_Iteration_1'!C26", "='02_KMeans_Iteration_1'!D26"),
            ],
            solved=solved,
            prev_sheet_name="02_KMeans_Iteration_1",
        )

        # Sheet 04: Iteration 3
        ws_r3 = wb.create_sheet()
        build_iteration_sheet(
            ws_r3,
            round_num=3,
            sheet_title="04_KMeans_Iteration_3",
            centroid_source_desc="Updated Centroids จาก New C1, C2, C3 ของรอบที่ 2",
            c_refs=[
                ("='03_KMeans_Iteration_2'!C24", "='03_KMeans_Iteration_2'!D24"),
                ("='03_KMeans_Iteration_2'!C25", "='03_KMeans_Iteration_2'!D25"),
                ("='03_KMeans_Iteration_2'!C26", "='03_KMeans_Iteration_2'!D26"),
            ],
            solved=solved,
            prev_sheet_name="03_KMeans_Iteration_2",
        )

        # Sheet 05: Analysis & Rubric
        ws_ans = wb.create_sheet()
        build_analysis_sheet(ws_ans, solved=solved)

        out_name = "KMeans_Exam_K3_MinMax_Solved.xlsx" if solved else "KMeans_Exam_K3_MinMax_Practice.xlsx"
        out_path = OUT_DIR / out_name
        wb.save(out_path)
        print(f"Generated: {out_path}")

    return (
        OUT_DIR / "KMeans_Exam_K3_MinMax_Practice.xlsx",
        OUT_DIR / "KMeans_Exam_K3_MinMax_Solved.xlsx",
    )


if __name__ == "__main__":
    create_exam_workbooks()
