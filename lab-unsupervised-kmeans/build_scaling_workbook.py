#!/usr/bin/env python3
"""Generate Feature Scaling + K-Means practice workbooks.

Creates:
1. KMeans_Scaling_Practice_TH.xlsx (Student practice workbook with blank formula cells)
2. KMeans_Scaling_Practice_TH_Solved.xlsx (Complete solved version with formulas and explanations)
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
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


def _headers(ws: Worksheet, row: int, values: list[str], fill: PatternFill, start_col: int = 1) -> None:
    for idx, value in enumerate(values, start=start_col):
        cell = ws.cell(row=row, column=idx, value=value)
        cell.font = HEAD
        cell.fill = fill
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        cell.border = THIN
    ws.row_dimensions[row].height = 28


# -------------------------------------------------------------------------
# SHEET 1: 00_Guide
# -------------------------------------------------------------------------
def build_guide_sheet(ws: Worksheet) -> None:
    ws.title = "00_Guide"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "แบบฝึกหัดการทำ Feature Scaling กับ K-Means Clustering"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:G1")

    lines = [
        "วัตถุประสงค์: ศึกษาผลกระทบของการไม่ทำ Scaling vs การทำ Scaling ต่ออัลกอริทึม K-Means ผ่านโจทย์ตัวเลขจริง",
        "ปัญหาเมื่อไม่ทำ Feature Scaling (The Scale Dominance Problem):",
        "    • สูตร Euclidean Distance: d = √[(X₁ - C₁)² + (X₂ - C₂)²]",
        "    • หาก X₁ มีค่า 20-50 (อายุ) แต่ X₂ มีค่า 20,000-80,000 (เงินเดือน)",
        "    • ผลต่างของ X₂ ยกกำลังสองจะมีค่าหลัก 100,000,000 ในขณะที่ X₁ ยกกำลังสองมีค่าเพียงหลัก 10-100",
        "    • ผลลัพธ์: K-Means จะจัดกลุ่มโดยดูเฉพาะ 'เงินเดือน' เพียงอย่างเดียว และละเลย 'อายุ' ไปโดยสิ้นเชิง!",
        "สองวิธีทำ Scaling ที่นิยมใช้ใน Machine Learning:",
        "    1. Min-Max Normalization (ช่วง 0 ถึง 1): X_scaled = (X - Min) / (Max - Min)  → เหมาะเมื่อต้องการขอบเขตแน่นอน",
        "    2. Z-Score Standardization (StandardScaler): Z = (X - Mean) / Stdev  (Excel: =STANDARDIZE(X, Mean, Stdev))",
        "คำชี้แจงและลำดับการทำแบบฝึกหัด:",
        "    • แผ่นงาน 01 (01_Step_by_Step_Tutorial): ชีตสอนและทดลองทำตามทีละขั้นตอน (Step 1-7) มีสูตรคณิตศาสตร์และสูตร Excel อธิบายกำกับชัดเจน",
        "    • แผ่นงาน 02 (02_Scaling_Calculation): แบบฝึกหัดคำนวณสถิติและแปลงค่า Min-Max / Z-Score ด้วยตนเองบนชุดข้อมูล 8 ตัวอย่าง (ไม่บอก Step)",
        "    • แผ่นงาน 03 (03_KMeans_Unscaled): สาธิตการรัน K-Means บนข้อมูลดิบ (Unscaled) เพื่อเห็นความผิดพลาดจากตัวแปรเงินเดือนที่ครอบงำอายุ",
        "    • แผ่นงาน 04 (04_KMeans_Scaled): คำนวณ K-Means บนข้อมูลที่ผ่านการทำ Min-Max Scaling ด้วยตนเอง (ไม่บอก Step) และหาค่า WCSS",
        "    • แผ่นงาน 05 (05_Comparison_Summary): สรุปเปรียบเทียบผลลัพธ์แบบจุดต่อจุด (Unscaled vs Scaled) และ 3 ประเด็นสำคัญสำหรับห้องสอบ",
    ]

    for idx, text in enumerate(lines, start=3):
        cell_ref = f"A{idx}"
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=10, bold=(idx in (3, 4, 10, 14)))
        if idx in (6, 7):
            ws[cell_ref].font = WARN
        ws.merge_cells(f"A{idx}:G{idx}")
        ws[cell_ref].alignment = WRAP
        ws.row_dimensions[idx].height = 24 if idx not in (4, 10, 14) else 28

    _width(ws, {"A": 105, "B": 15, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15})


# -------------------------------------------------------------------------
# SHEET 2: 01_Step_by_Step_Tutorial (Guided Walkthrough)
# -------------------------------------------------------------------------
def build_step_by_step_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "01_Step_by_Step_Tutorial"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "ชีตทดลองทำตามทีละขั้นตอน (Step-by-Step Guided Tutorial): Feature Scaling และ K-Means"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    ws["A2"] = "★ คำแนะนำ: ให้นักศึกษาฝึกพิมพ์สูตรตามคำแนะนำในคอลัมน์ขวาลงในเซลล์สีเหลือง (Step 1 ถึง Step 7) เพื่อสร้างความเข้าใจก่อนไปทำแบบฝึกหัดจริงในแผ่นงาน 02 - 04"
    ws["A2"].font = SUCCESS
    ws.merge_cells("A2:I2")

    # =========================================================================
    # SECTION 1: Feature Scaling (Steps 1 to 3)
    # =========================================================================
    ws["A4"] = "【ส่วนที่ 1: ขั้นตอนการคำนวณ Feature Scaling (Min-Max และ Z-Score)】"
    ws["A4"].font = SUBBOLD
    ws.merge_cells("A4:I4")

    # STEP 1: Raw Data & Stats (Cols A-D)
    _label(ws, "A5", "📌 STEP 1: เตรียมข้อมูลดิบและหาค่าสถิติพื้นฐาน (Min, Max, Range, Mean, Stdev)")
    ws.merge_cells("A5:D5")

    _headers(ws, 6, ["รหัส", "ชื่อตัวอย่าง", "อายุ (X1)", "เงินเดือน (X2)"], NAVY_FILL, start_col=1)

    tutorial_samples = [
        ("S1", "สมชาย (จุด Min)", 20.0, 30000.0),
        ("S2", "สมศักดิ์ (จุดกลางล่าง)", 25.0, 40000.0),
        ("S3", "ประเสริฐ (จุดเปลี่ยนผ่าน)", 45.0, 60000.0),
        ("S4", "วิภา (จุด Max)", 50.0, 90000.0),
    ]

    for idx, (pid, name, age, sal) in enumerate(tutorial_samples, start=7):
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = name
        ws[f"B{idx}"].font = Font(name="Arial", size=9)
        ws[f"B{idx}"].border = THIN

        _input(ws, f"C{idx}", age, CENTER)
        ws[f"C{idx}"].number_format = "0"

        _input(ws, f"D{idx}", sal, CENTER)
        ws[f"D{idx}"].number_format = "#,##0"

    _headers(ws, 12, ["ค่าทางสถิติ", "สูตร Excel ที่ใช้", "อายุ (X1)", "เงินเดือน (X2)"], TEAL_FILL, start_col=1)

    stats_tutorial = [
        ("13", "Min (ค่าน้อยสุด)", "=MIN(C7:C10)", "=MIN(C7:C10)", "=MIN(D7:D10)", "0", "#,##0"),
        ("14", "Max (ค่ามากสุด)", "=MAX(C7:C10)", "=MAX(C7:C10)", "=MAX(D7:D10)", "0", "#,##0"),
        ("15", "Range (พิสัย = Max-Min)", "=C14-C13", "=C14-C13", "=D14-D13", "0", "#,##0"),
        ("16", "Mean (ค่าเฉลี่ย)", "=AVERAGE(C7:C10)", "=AVERAGE(C7:C10)", "=AVERAGE(D7:D10)", "0.0", "#,##0"),
        ("17", "Stdev (ส่วนเบี่ยงเบน)", "=STDEV.S(C7:C10)", "=STDEV.S(C7:C10)", "=STDEV.S(D7:D10)", "0.00", "#,##0.00"),
    ]

    for r_str, label_th, f_hint, f_age, f_sal, fmt_age, fmt_sal in stats_tutorial:
        ws[f"A{r_str}"] = label_th
        ws[f"A{r_str}"].font = Font(name="Arial", bold=True, size=9)
        ws[f"A{r_str}"].border = THIN

        ws[f"B{r_str}"] = f_hint
        ws[f"B{r_str}"].font = NOTE
        ws[f"B{r_str}"].border = THIN

        _blank(ws, f"C{r_str}", solved, f_age, fmt_age, LIGHT_BLUE_FILL, BLACK, CENTER)
        _blank(ws, f"D{r_str}", solved, f_sal, fmt_sal, LIGHT_BLUE_FILL, BLACK, CENTER)

    # STEP 2: Min-Max Normalization (Cols F to I, Rows 5 to 10)
    _label(ws, "F5", "📌 STEP 2: Min-Max Scaling: สูตร =(X - Min) / Range (ช่วง 0 ถึง 1)")
    ws.merge_cells("F5:I5")

    _headers(ws, 6, ["รหัส", "Age_Norm (0-1)", "Salary_Norm (0-1)", "สูตร Excel ที่ต้องพิมพ์ (สังเกตเครื่องหมาย $)"], INDIGO_FILL, start_col=6)

    minmax_tutorial = [
        ("S1", 7, "=(C7-$C$13)/$C$15", "=(D7-$D$13)/$D$15"),
        ("S2", 8, "=(C8-$C$13)/$C$15", "=(D8-$D$13)/$D$15"),
        ("S3", 9, "=(C9-$C$13)/$C$15", "=(D9-$D$13)/$D$15"),
        ("S4", 10, "=(C10-$C$13)/$C$15", "=(D10-$D$13)/$D$15"),
    ]

    for pid, r_idx, f_age, f_sal in minmax_tutorial:
        ws[f"F{r_idx}"] = pid
        ws[f"F{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"F{r_idx}"].alignment = CENTER
        ws[f"F{r_idx}"].border = THIN

        _blank(ws, f"G{r_idx}", solved, f_age, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{r_idx}", solved, f_sal, "0.0000", YELLOW_FILL, BLACK, CENTER)

        ws[f"I{r_idx}"] = f"พิมพ์: =(C{r_idx}-$C$13)/$C$15  |  =(D{r_idx}-$D$13)/$D$15"
        ws[f"I{r_idx}"].font = NOTE
        ws[f"I{r_idx}"].border = THIN

    # STEP 3: Z-Score Standardization (Cols F to I, Rows 12 to 17)
    _label(ws, "F12", "📌 STEP 3: Z-Score Standardization: สูตร =(X - Mean) / Stdev")
    ws.merge_cells("F12:I12")

    _headers(ws, 13, ["รหัส", "Z_Age (Mean=0, SD=1)", "Z_Salary (Mean=0, SD=1)", "สูตรทางเลือก: ฟังก์ชัน =STANDARDIZE(...)"], AMBER_FILL, start_col=6)

    zscore_tutorial = [
        ("S1", 14, 7, "=(C7-$C$16)/$C$17", "=(D7-$D$16)/$D$17"),
        ("S2", 15, 8, "=(C8-$C$16)/$C$17", "=(D8-$D$16)/$D$17"),
        ("S3", 16, 9, "=(C9-$C$16)/$C$17", "=(D9-$D$16)/$D$17"),
        ("S4", 17, 10, "=(C10-$C$16)/$C$17", "=(D10-$D$16)/$D$17"),
    ]

    for pid, r_idx, src_idx, f_age, f_sal in zscore_tutorial:
        ws[f"F{r_idx}"] = pid
        ws[f"F{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"F{r_idx}"].alignment = CENTER
        ws[f"F{r_idx}"].border = THIN

        _blank(ws, f"G{r_idx}", solved, f_age, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{r_idx}", solved, f_sal, "0.0000", YELLOW_FILL, BLACK, CENTER)

        ws[f"I{r_idx}"] = f"สูตร: =(C{src_idx}-$C$16)/$C$17  หรือใช้  =STANDARDIZE(C{src_idx}, $C$16, $C$17)"
        ws[f"I{r_idx}"].font = NOTE
        ws[f"I{r_idx}"].border = THIN

    # =========================================================================
    # SECTION 2: K-Means on Scaled Data (Steps 4 to 7)
    # =========================================================================
    ws["A19"] = "【ส่วนที่ 2: ขั้นตอนการรัน K-Means บนข้อมูลที่ทำ Min-Max Scaling แล้ว (Step 4 ถึง Step 7)】"
    ws["A19"].font = SUBBOLD
    ws.merge_cells("A19:I19")

    # STEP 4: Initial Centroids (Rows 20 to 23)
    _label(ws, "A20", "📌 STEP 4: กำหนด Centroid เริ่มต้น (C1 = S1, C2 = S4 ในพิกัดที่สเกลแล้ว)")
    ws.merge_cells("A20:E20")

    _headers(ws, 21, ["Centroid", "เลือกจากจุด", "Age_Norm (0-1)", "Salary_Norm (0-1)", "สูตร Excel ที่ดึงพิกัดมาใช้"], NAVY_FILL, start_col=1)

    ws["A22"] = "C1 (กลุ่ม 1)"
    ws["A22"].font = Font(name="Arial", bold=True)
    ws["A22"].border = THIN
    ws["B22"] = "S1"
    ws["B22"].font = BLUE
    ws["B22"].alignment = CENTER
    ws["B22"].border = THIN
    _blank(ws, "C22", solved, "=G7", "0.0000", YELLOW_FILL, BLACK, CENTER)
    _blank(ws, "D22", solved, "=H7", "0.0000", YELLOW_FILL, BLACK, CENTER)
    ws["E22"] = "สูตร: =G7 และ =H7 (ดึงพิกัด Min-Max ของจุด S1: 0, 0)"
    ws["E22"].font = NOTE
    ws["E22"].border = THIN

    ws["A23"] = "C2 (กลุ่ม 2)"
    ws["A23"].font = Font(name="Arial", bold=True)
    ws["A23"].border = THIN
    ws["B23"] = "S4"
    ws["B23"].font = BLUE
    ws["B23"].alignment = CENTER
    ws["B23"].border = THIN
    _blank(ws, "C23", solved, "=G10", "0.0000", YELLOW_FILL, BLACK, CENTER)
    _blank(ws, "D23", solved, "=H10", "0.0000", YELLOW_FILL, BLACK, CENTER)
    ws["E23"] = "สูตร: =G10 และ =H10 (ดึงพิกัด Min-Max ของจุด S4: 1, 1)"
    ws["E23"].font = NOTE
    ws["E23"].border = THIN

    # STEP 5 & 6: Distance, Assignment, d_min^2, WCSS (Rows 25 to 31)
    _label(ws, "A25", "📌 STEP 5 & 6: คำนวณระยะทาง Euclidean (SQRT), เลือกลุ่มที่ใกล้ที่สุด (IF), หา d_min² และ WCSS")
    ws.merge_cells("A25:I25")

    _headers(ws, 26, ["รหัส", "Age_Norm", "Salary_Norm", "d(P, C1)", "d(P, C2)", "กลุ่มที่ได้", "d_min²", "สูตรคำนวณระยะ d(P, C1)", "สูตรกำหนดกลุ่ม (IF) & d_min²"], TEAL_FILL, start_col=1)

    kmeans_tutorial = [
        ("S1", 27, 7),
        ("S2", 28, 8),
        ("S3", 29, 9),
        ("S4", 30, 10),
    ]

    for pid, r_idx, src_idx in kmeans_tutorial:
        ws[f"A{r_idx}"] = pid
        ws[f"A{r_idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{r_idx}"].alignment = CENTER
        ws[f"A{r_idx}"].border = THIN

        # Linked from Min-Max Table
        ws[f"B{r_idx}"] = f"=G{src_idx}"
        ws[f"B{r_idx}"].font = BLACK
        ws[f"B{r_idx}"].number_format = "0.0000"
        ws[f"B{r_idx}"].alignment = CENTER
        ws[f"B{r_idx}"].border = THIN

        ws[f"C{r_idx}"] = f"=H{src_idx}"
        ws[f"C{r_idx}"].font = BLACK
        ws[f"C{r_idx}"].number_format = "0.0000"
        ws[f"C{r_idx}"].alignment = CENTER
        ws[f"C{r_idx}"].border = THIN

        f_d1 = f"=SQRT((B{r_idx}-$C$22)^2 + (C{r_idx}-$D$22)^2)"
        f_d2 = f"=SQRT((B{r_idx}-$C$23)^2 + (C{r_idx}-$D$23)^2)"
        f_cl = f"=IF(D{r_idx}<=E{r_idx}, 1, 2)"
        f_dmin2 = f"=IF(F{r_idx}=1, D{r_idx}^2, E{r_idx}^2)"

        _blank(ws, f"D{r_idx}", solved, f_d1, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"E{r_idx}", solved, f_d2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{r_idx}", solved, f_cl, "0", YELLOW_FILL, Font(name="Arial", bold=True, color="047857"), CENTER)
        _blank(ws, f"G{r_idx}", solved, f_dmin2, "0.0000", LIGHT_GREEN_FILL, BLACK, CENTER)

        ws[f"H{r_idx}"] = f"=SQRT((B{r_idx}-$C$22)^2 + (C{r_idx}-$D$22)^2)  |  ไปยัง C2 ใช้ $C$23, $D$23"
        ws[f"H{r_idx}"].font = NOTE
        ws[f"H{r_idx}"].border = THIN

        ws[f"I{r_idx}"] = f"กลุ่ม: =IF(D{r_idx}<=E{r_idx}, 1, 2)  |  d_min²: =IF(F{r_idx}=1, D{r_idx}^2, E{r_idx}^2)"
        ws[f"I{r_idx}"].font = NOTE
        ws[f"I{r_idx}"].border = THIN

    # WCSS Row
    ws["A31"] = "รวมค่า WCSS รอบที่ 1 (ผลรวม d_min²):"
    ws["A31"].font = Font(name="Arial", bold=True, size=10)
    ws.merge_cells("A31:F31")
    ws["A31"].alignment = Alignment(horizontal="right", vertical="center")
    _blank(
        ws,
        "G31",
        solved,
        "=SUM(G27:G30)",
        "0.0000",
        LIGHT_PURPLE_FILL,
        Font(name="Arial", bold=True, color="4338CA", size=11),
        CENTER,
    )
    ws["G31"].border = DOUBLE_BOTTOM

    ws["H31"] = "สูตร: =SUM(G27:G30)"
    ws["H31"].font = NOTE
    ws["H31"].border = THIN

    ws["I31"] = "ค่ายิ่งน้อย แสดงว่าจุดรวมกลุ่มกันแน่นหนาดี"
    ws["I31"].font = NOTE
    ws["I31"].border = THIN

    # STEP 7: Centroid Update & Inverse Scaling (Rows 33 to 36)
    ws["A33"] = "📌 STEP 7: คำนวณ Centroid ใหม่ด้วย =AVERAGEIF(...) และแปลงกลับเป็นหน่วยจริง (Inverse Scaling)"
    ws["A33"].font = Font(name="Arial", bold=True, size=10)
    ws.merge_cells("A33:I33")

    _headers(ws, 34, ["กลุ่ม (Cluster)", "จำนวนสมาชิก", "Centroid Age_Norm", "Centroid Sal_Norm", "แปลงกลับเป็นหน่วยจริง (Inverse)", "สูตร AVERAGEIF และสูตรแปลงกลับหน่วยจริง"], INDIGO_FILL, start_col=1)

    ws["A35"] = "กลุ่ม 1 (อายุน้อย รายได้เริ่มต้น)"
    ws["A35"].font = Font(name="Arial", bold=True)
    ws["A35"].border = THIN
    _blank(ws, "B35", solved, "=COUNTIF($F$27:$F$30, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C35", solved, "=AVERAGEIF($F$27:$F$30, 1, $B$27:$B$30)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D35", solved, "=AVERAGEIF($F$27:$F$30, 1, $C$27:$C$30)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E35"] = '="อายุ ~ " & TEXT($C$13+C35*$C$15, "0.0") & " ปี / เงินเดือน ~ " & TEXT($D$13+D35*$D$15, "#,##0") & " บาท"' if solved else "สูตรแปลงกลับหน่วยจริง"
    ws["E35"].font = NOTE
    ws["E35"].border = THIN
    ws["F35"] = "สูตร Centroid: =AVERAGEIF($F$27:$F$30, 1, B27:B30)  |  แปลงกลับ: =$C$13 + C35 * $C$15"
    ws["F35"].font = NOTE
    ws["F35"].border = THIN

    ws["A36"] = "กลุ่ม 2 (อายุมาก รายได้สูง)"
    ws["A36"].font = Font(name="Arial", bold=True)
    ws["A36"].border = THIN
    _blank(ws, "B36", solved, "=COUNTIF($F$27:$F$30, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C36", solved, "=AVERAGEIF($F$27:$F$30, 2, $B$27:$B$30)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D36", solved, "=AVERAGEIF($F$27:$F$30, 2, $C$27:$C$30)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E36"] = '="อายุ ~ " & TEXT($C$13+C36*$C$15, "0.0") & " ปี / เงินเดือน ~ " & TEXT($D$13+D36*$D$15, "#,##0") & " บาท"' if solved else "สูตรแปลงกลับหน่วยจริง"
    ws["E36"].font = NOTE
    ws["E36"].border = THIN
    ws["F36"] = "สูตร Centroid: =AVERAGEIF($F$27:$F$30, 2, B27:B30)  |  แปลงกลับ: =$C$13 + C36 * $C$15"
    ws["F36"].font = NOTE
    ws["F36"].border = THIN

    # SECTION 3: 4 Exam Tips & Cheatsheet (Rows 38 to 44)
    ws["A38"] = "💡 4 ข้อควรระวังและเทคนิคการเขียนสูตร Excel สำหรับห้องสอบ:"
    ws["A38"].font = Font(name="Arial", bold=True, size=11, color="1E3A5F")

    tips = [
        "1. การล็อกเซลล์ ($ Absolute Reference): เวลาคำนวณ Min-Max หรือ Z-Score ต้องใส่ $ หน้าเลขแถวของ Min/Range/Mean/Stdev เสมอ เช่น $C$13 หากไม่ใส่ เมื่อลากสูตรลงมา ตำแหน่งเซลล์จะเลื่อนลงตาม ทำให้ผลลัพธ์เป็น #DIV/0! หรือคำนวณผิด",
        "2. สรุปความต่างของสูตร Scaling: Min-Max = (X - Min) / Range ได้ช่วงแน่นอน [0, 1] ส่วน Z-Score = (X - Mean) / Stdev ได้ค่าเฉลี่ย 0 ส่วนเบี่ยงเบน 1 (Excel มีฟังก์ชัน =STANDARDIZE(X, Mean, Stdev))",
        "3. การเลือกกลุ่มด้วย =IF(d1 <= d2, 1, 2): ตรวจสอบว่าระยะทางไปยัง C1 น้อยกว่าหรือเท่ากับ C2 หรือไม่ ถ้าใช่ให้อยู่กลุ่ม 1 ถ้าไม่ใช่ให้อยู่กลุ่ม 2 (หากระยะทางเท่ากัน ให้เลือกกลุ่มแรก)",
        "4. การแปลง Centroid กลับเป็นหน่วยจริง (Inverse Formula): นำพิกัดที่ได้คูณด้วยพิสัยเดิม แล้วบวกด้วยค่าน้อยสุด: Real = Min + (Scaled_Centroid * Range) เพื่อให้สื่อสารกับผู้บริหารหรือลูกค้าเข้าใจในหน่วยจริง (ปี, บาท)",
    ]
    for idx, tip_text in enumerate(tips, start=39):
        ws[f"A{idx}"] = tip_text
        ws[f"A{idx}"].font = Font(name="Arial", size=9)
        ws[f"A{idx}"].alignment = WRAP
        ws.merge_cells(f"A{idx}:I{idx}")
        ws.row_dimensions[idx].height = 28

    _width(
        ws,
        {
            "A": 10,
            "B": 24,
            "C": 18,
            "D": 20,
            "E": 28,
            "F": 12,
            "G": 18,
            "H": 28,
            "I": 42,
        },
    )


# -------------------------------------------------------------------------
# SHEET 3: 02_Scaling_Calculation (Independent Practice)
# -------------------------------------------------------------------------
def build_scaling_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "02_Scaling_Calculation"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "การคำนวณ Feature Scaling: แปลงข้อมูลดิบ (อายุ & เงินเดือน) ด้วย Min-Max และ Z-Score"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    # Raw Data Table
    ws["A3"] = "【ตารางข้อมูลดิบ (Raw Data)】"
    ws["A3"].font = SUBBOLD

    _headers(ws, 4, ["รหัส", "ชื่อตัวแทน", "อายุ X1 (ปี)", "เงินเดือน X2 (บาท)"], NAVY_FILL)

    raw_samples = [
        ("P1", "สมชาย (วัยรุ่น รายได้เริ่มต้น)", 20.0, 25000.0),
        ("P2", "สมศักดิ์ (วัยรุ่น รายได้เริ่มต้น)", 22.0, 30000.0),
        ("P3", "สมหญิง (วัยรุ่น รายได้เริ่มต้น)", 24.0, 28000.0),
        ("P4", "วิชัย (คนรุ่นใหม่ รายได้สูง)", 26.0, 52000.0),
        ("P5", "ประเสริฐ (วัยกลางคน รายได้ปานกลาง)", 44.0, 50000.0),
        ("P6", "มานะ (วัยทำงาน รายได้สูง)", 46.0, 70000.0),
        ("P7", "กมล (ผู้บริหาร รายได้สูงมาก)", 48.0, 75000.0),
        ("P8", "วิภา (ผู้บริหาร รายได้สูงสุด)", 50.0, 80000.0),
    ]

    for idx, (pid, name, age, sal) in enumerate(raw_samples, start=5):
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = name
        ws[f"B{idx}"].font = Font(name="Arial", size=9)
        ws[f"B{idx}"].border = THIN

        _input(ws, f"C{idx}", age, CENTER)
        ws[f"C{idx}"].number_format = "0"

        _input(ws, f"D{idx}", sal, CENTER)
        ws[f"D{idx}"].number_format = "#,##0"

    # Statistics Summary Table
    ws["A14"] = "【สรุปค่าทางสถิติสำหรับใช้ในการสเกล】"
    ws["A14"].font = SUBBOLD

    _headers(ws, 15, ["ค่าทางสถิติ", "สูตร Excel", "อายุ (X1)", "เงินเดือน (X2)"], TEAL_FILL)

    stats = [
        ("16", "ค่าน้อยสุด (Minimum)", "=MIN(...)", "=MIN(C5:C12)", "=MIN(D5:D12)", "0", "#,##0"),
        ("17", "ค่ามากสุด (Maximum)", "=MAX(...)", "=MAX(C5:C12)", "=MAX(D5:D12)", "0", "#,##0"),
        ("18", "พิสัย (Range = Max - Min)", "=Max - Min", "=C17-C16", "=D17-D16", "0", "#,##0"),
        ("19", "ค่าเฉลี่ย (Mean)", "=AVERAGE(...)", "=AVERAGE(C5:C12)", "=AVERAGE(D5:D12)", "0.00", "#,##0.00"),
        ("20", "ส่วนเบี่ยงเบนมาตรฐาน (Stdev.s)", "=STDEV.S(...)", "=STDEV.S(C5:C12)", "=STDEV.S(D5:D12)", "0.0000", "#,##0.00"),
    ]

    for r_str, label_th, formula_hint, f_age, f_sal, fmt_age, fmt_sal in stats:
        ws[f"A{r_str}"] = label_th
        ws[f"A{r_str}"].font = Font(name="Arial", bold=True, size=9)
        ws[f"A{r_str}"].border = THIN

        ws[f"B{r_str}"] = formula_hint
        ws[f"B{r_str}"].font = NOTE
        ws[f"B{r_str}"].border = THIN

        _blank(ws, f"C{r_str}", solved, f_age, fmt_age, LIGHT_BLUE_FILL, BLACK, CENTER)
        _blank(ws, f"D{r_str}", solved, f_sal, fmt_sal, LIGHT_BLUE_FILL, BLACK, CENTER)

    # Scaled Output Tables (Columns F to I)
    ws["F3"] = "【ตารางที่ 1: Min-Max Scaling (ช่วง 0 ถึง 1)】: สูตร =(X - Min) / Range"
    ws["F3"].font = SUBBOLD

    _headers(ws, 4, ["รหัส", "Age_Norm (0-1)", "Salary_Norm (0-1)", "คำอธิบายพิกัดสเกล"], INDIGO_FILL, start_col=6)

    for idx in range(5, 13):
        pid = ws[f"A{idx}"].value
        ws[f"F{idx}"] = pid
        ws[f"F{idx}"].font = Font(name="Arial", bold=True)
        ws[f"F{idx}"].alignment = CENTER
        ws[f"F{idx}"].border = THIN

        f_norm_age = f"=(C{idx}-$C$16)/$C$18"
        f_norm_sal = f"=(D{idx}-$D$16)/$D$18"

        _blank(ws, f"G{idx}", solved, f_norm_age, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_norm_sal, "0.0000", YELLOW_FILL, BLACK, CENTER)

        ws[f"I{idx}"] = f'=IF(G{idx}>0.5, "สูงวัย", "วัยรุ่น") & " / " & IF(H{idx}>0.5, "รายได้สูง", "รายได้ปานกลาง-น้อย")' if solved else "สูตรแสดง Persona"
        ws[f"I{idx}"].font = NOTE
        ws[f"I{idx}"].border = THIN

    # Z-Score Table (Columns F to I from Row 15)
    ws["F14"] = "【ตารางที่ 2: Z-Score Standardization】: สูตร =(X - Mean) / Stdev"
    ws["F14"].font = SUBBOLD

    _headers(ws, 15, ["รหัส", "Z_Age (Mean=0, SD=1)", "Z_Salary (Mean=0, SD=1)", "ฟังก์ชัน Excel ทางเลือก"], AMBER_FILL, start_col=6)

    for idx in range(16, 24):
        src_row = idx - 11  # maps 16->5, 17->6 ...
        pid = ws[f"A{src_row}"].value
        ws[f"F{idx}"] = pid
        ws[f"F{idx}"].font = Font(name="Arial", bold=True)
        ws[f"F{idx}"].alignment = CENTER
        ws[f"F{idx}"].border = THIN

        f_z_age = f"=(C{src_row}-$C$19)/$C$20"
        f_z_sal = f"=(D{src_row}-$D$19)/$D$20"

        _blank(ws, f"G{idx}", solved, f_z_age, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_z_sal, "0.0000", YELLOW_FILL, BLACK, CENTER)

        ws[f"I{idx}"] = f'=STANDARDIZE(C{src_row}, $C$19, $C$20)' if solved else "=STANDARDIZE(X, Mean, Stdev)"
        ws[f"I{idx}"].font = NOTE
        ws[f"I{idx}"].border = THIN

    _width(
        ws,
        {
            "A": 8,
            "B": 32,
            "C": 18,
            "D": 22,
            "E": 4,
            "F": 8,
            "G": 22,
            "H": 22,
            "I": 36,
        },
    )


# -------------------------------------------------------------------------
# SHEET 4: 03_KMeans_Unscaled (Demonstrates the problem)
# -------------------------------------------------------------------------
def build_unscaled_kmeans_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "03_KMeans_Unscaled"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "การรัน K-Means บนข้อมูลดิบ (Unscaled) — แสดงข้อผิดพลาดจากแกนเงินเดือนที่ครอบงำอายุ"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    ws["A3"] = "กำหนด Centroid เริ่มต้นจากข้อมูลดิบ: C1 = P1 (20 ปี, 25,000 บาท) และ C2 = P8 (50 ปี, 80,000 บาท)"
    ws["A3"].font = SUBBOLD
    ws.merge_cells("A3:I3")

    # Centroids header
    _headers(ws, 4, ["Centroid", "เลือกจากจุด", "อายุ X1 (ปี)", "เงินเดือน X2 (บาท)", "คำอธิบาย"], NAVY_FILL)
    _label(ws, "A5", "C1 (กลุ่ม 1)")
    _input(ws, "B5", "P1", CENTER)
    _input(ws, "C5", 20.0, CENTER)
    _input(ws, "D5", 25000.0, CENTER)
    ws["D5"].number_format = "#,##0"
    ws["E5"] = "จุดเริ่มต้นกลุ่มที่ 1 (อายุน้อย รายได้น้อย)"
    ws["E5"].font = NOTE

    _label(ws, "A6", "C2 (กลุ่ม 2)")
    _input(ws, "B6", "P8", CENTER)
    _input(ws, "C6", 50.0, CENTER)
    _input(ws, "D6", 80000.0, CENTER)
    ws["D6"].number_format = "#,##0"
    ws["E6"] = "จุดเริ่มต้นกลุ่มที่ 2 (อายุมาก รายได้สูง)"
    ws["E6"].font = NOTE

    for r in (5, 6):
        ws[f"A{r}"].border = THIN
        ws[f"E{r}"].border = THIN

    # Iteration 1
    ws["A8"] = "【รอบที่ 1 (Iteration 1: Unscaled)】: สังเกตระยะห่างของจุด P5 (อายุ 44 ปี แต่เงินเดือน 50,000 บาท)"
    ws["A8"].font = SUBBOLD

    headers_unscaled = [
        "รหัส",
        "อายุ X1",
        "เงินเดือน X2",
        "d(P, C1)",
        "d(P, C2)",
        "กลุ่มที่ได้",
        "(Δ Age)² เทียบ C1",
        "(Δ Salary)² เทียบ C1",
        "ข้อสังเกตการครอบงำ",
    ]
    _headers(ws, 9, headers_unscaled, ROSE_FILL)
    for c in range(1, 10):
        ws.cell(row=9, column=c).font = Font(name="Arial", bold=True, color="991B1B", size=9)

    raw_data = [
        ("P1", 20.0, 25000.0),
        ("P2", 22.0, 30000.0),
        ("P3", 24.0, 28000.0),
        ("P4", 26.0, 52000.0),
        ("P5", 44.0, 50000.0),
        ("P6", 46.0, 70000.0),
        ("P7", 48.0, 75000.0),
        ("P8", 50.0, 80000.0),
    ]

    for idx, (pid, age, sal) in enumerate(raw_data, start=10):
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        _input(ws, f"B{idx}", age, CENTER)
        ws[f"B{idx}"].number_format = "0"
        _input(ws, f"C{idx}", sal, CENTER)
        ws[f"C{idx}"].number_format = "#,##0"

        f_d1 = f"=SQRT((B{idx}-$C$5)^2 + (C{idx}-$D$5)^2)"
        f_d2 = f"=SQRT((B{idx}-$C$6)^2 + (C{idx}-$D$6)^2)"
        f_cl = f"=IF(D{idx}<=E{idx}, 1, 2)"
        f_dage2 = f"=(B{idx}-$C$5)^2"
        f_dsal2 = f"=(C{idx}-$D$5)^2"

        _blank(ws, f"D{idx}", solved, f_d1, "#,##0.0", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"E{idx}", solved, f_d2, "#,##0.0", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{idx}", solved, f_cl, "0", YELLOW_FILL, Font(name="Arial", bold=True, color="991B1B"), CENTER)
        _blank(ws, f"G{idx}", solved, f_dage2, "0", LIGHT_BLUE_FILL, BLACK, CENTER)
        _blank(ws, f"H{idx}", solved, f_dsal2, "#,##0", LIGHT_AMBER_FILL, BLACK, CENTER)

        obs = "⚠️ ถูกดึงเข้ากลุ่ม 1 เพราะเงินเดือนใกล้กว่า ทั้งที่อายุ 44 ปี!" if pid == "P5" else "เงินเดือนเป็นตัวตัดสิน"
        ws[f"I{idx}"] = obs
        ws[f"I{idx}"].font = Font(name="Arial", bold=(pid == "P5"), color="B91C1C" if pid == "P5" else "475569", size=9)
        ws[f"I{idx}"].border = THIN

    # Centroids after round 1
    ws["A19"] = "【Centroid ใหม่หลังรอบที่ 1 (Unscaled)】: สังเกตพิกัดกลุ่มที่ 1 มีอายุเฉลี่ยโดดขึ้นเป็น 27.2 ปี"
    ws["A19"].font = SUBBOLD

    _headers(ws, 20, ["กลุ่ม (Cluster)", "จำนวนสมาชิก", "Centroid อายุ (ปี)", "Centroid เงินเดือน (บาท)", "สมาชิกในกลุ่ม"], NAVY_FILL)

    ws["A21"] = "กลุ่ม 1 (Cluster 1)"
    ws["A21"].font = Font(name="Arial", bold=True)
    ws["A21"].border = THIN
    _blank(ws, "B21", solved, "=COUNTIF($F$10:$F$17, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C21", solved, "=AVERAGEIF($F$10:$F$17, 1, $B$10:$B$17)", "0.0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D21", solved, "=AVERAGEIF($F$10:$F$17, 1, $C$10:$C$17)", "#,##0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E21"] = "P1, P2, P3, P4, P5 (มี P5 วัย 44 ปีปนอยู่ด้วย!)"
    ws["E21"].font = WARN
    ws["E21"].border = THIN

    ws["A22"] = "กลุ่ม 2 (Cluster 2)"
    ws["A22"].font = Font(name="Arial", bold=True)
    ws["A22"].border = THIN
    _blank(ws, "B22", solved, "=COUNTIF($F$10:$F$17, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C22", solved, "=AVERAGEIF($F$10:$F$17, 2, $B$10:$B$17)", "0.0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D22", solved, "=AVERAGEIF($F$10:$F$17, 2, $C$10:$C$17)", "#,##0", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E22"] = "P6, P7, P8 (มีเฉพาะคนเงินเดือน 70,000+)"
    ws["E22"].font = NOTE
    ws["E22"].border = THIN

    ws["A24"] = "📌 บทสรุปข้อผิดพลาดของการไม่ทำ Scaling:"
    ws["A24"].font = Font(name="Arial", bold=True, color="991B1B")
    reasons = [
        "1. ดูคอลัมน์ G เทียบกับ H: (Δ Age)² มีค่าสูงสุดเพียง 576 แต่ (Δ Salary)² มีค่าสูงถึง 625,000,000 (ต่างกันกว่า 1,000,000 เท่า!)",
        "2. อายุจึงแทบไม่มีผลใดๆ ต่อการคำนวณระยะทาง ราวกับว่าเราตัดคอลัมน์อายุทิ้งไปจากการวิเคราะห์",
        "3. จุด P5 (อายุ 44 ปี) จึงถูกจับไปรวมกับเด็กจบใหม่อายุ 20-24 ปี เพียงเพราะเงินเดือน 50,000 ใกล้ 25,000 มากกว่า 80,000",
    ]
    for r_idx, text in enumerate(reasons, start=25):
        ws[f"A{r_idx}"] = text
        ws[f"A{r_idx}"].font = Font(name="Arial", size=9, color="7F1D1D")
        ws.merge_cells(f"A{r_idx}:I{r_idx}")

    _width(
        ws,
        {
            "A": 8,
            "B": 12,
            "C": 16,
            "D": 16,
            "E": 16,
            "F": 12,
            "G": 14,
            "H": 18,
            "I": 46,
        },
    )


# -------------------------------------------------------------------------
# SHEET 5: 04_KMeans_Scaled (Corrected with Min-Max Scaling)
# -------------------------------------------------------------------------
def build_scaled_kmeans_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "04_KMeans_Scaled"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "การรัน K-Means บนข้อมูลที่ทำ Scaling แล้ว (Min-Max: 0 ถึง 1) — ทั้งอายุและเงินเดือนมีน้ำหนักสมดุล"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:I1")

    ws["A3"] = "กำหนด Centroid เริ่มต้นในสเกลปกติ: C1 = P1 (0.00, 0.00) และ C2 = P8 (1.00, 1.00)"
    ws["A3"].font = SUBBOLD
    ws.merge_cells("A3:I3")

    _headers(ws, 4, ["Centroid", "เลือกจากจุด", "Age_Norm (0-1)", "Salary_Norm (0-1)", "ความหมายในโลกจริง"], NAVY_FILL)
    _label(ws, "A5", "C1 (กลุ่ม 1)")
    _input(ws, "B5", "P1", CENTER)
    _input(ws, "C5", 0.0, CENTER)
    ws["C5"].number_format = "0.0000"
    _input(ws, "D5", 0.0, CENTER)
    ws["D5"].number_format = "0.0000"
    ws["E5"] = "ตัวแทนกลุ่มอายุน้อย รายได้น้อย (อายุ 20, เงินเดือน 25,000)"
    ws["E5"].font = NOTE

    _label(ws, "A6", "C2 (กลุ่ม 2)")
    _input(ws, "B6", "P8", CENTER)
    _input(ws, "C6", 1.0, CENTER)
    ws["C6"].number_format = "0.0000"
    _input(ws, "D6", 1.0, CENTER)
    ws["D6"].number_format = "0.0000"
    ws["E6"] = "ตัวแทนกลุ่มอายุมาก รายได้สูง (อายุ 50, เงินเดือน 80,000)"
    ws["E6"].font = NOTE

    for r in (5, 6):
        ws[f"A{r}"].border = THIN
        ws[f"E{r}"].border = THIN

    # Iteration 1 Scaled
    ws["A8"] = "【รอบที่ 1 (Iteration 1: Scaled)】: ทั้งแกนอายุและเงินเดือนอยู่ในช่วง 0-1 ทำให้คำนวณระยะทางได้อย่างยุติธรรม"
    ws["A8"].font = SUBBOLD

    headers_scaled = [
        "รหัส",
        "Age_Norm",
        "Salary_Norm",
        "d(P, C1)",
        "d(P, C2)",
        "กลุ่มที่ได้",
        "d_min²",
        "การเปรียบเทียบ P5",
    ]
    _headers(ws, 9, headers_scaled, TEAL_FILL)

    # Normalized coords from sheet 02
    points_norm = [
        ("P1", "='02_Scaling_Calculation'!G5", "='02_Scaling_Calculation'!H5", 0.0, 0.0),
        ("P2", "='02_Scaling_Calculation'!G6", "='02_Scaling_Calculation'!H6", 0.0667, 0.0909),
        ("P3", "='02_Scaling_Calculation'!G7", "='02_Scaling_Calculation'!H7", 0.1333, 0.0545),
        ("P4", "='02_Scaling_Calculation'!G8", "='02_Scaling_Calculation'!H8", 0.2000, 0.4909),
        ("P5", "='02_Scaling_Calculation'!G9", "='02_Scaling_Calculation'!H9", 0.8000, 0.4545),
        ("P6", "='02_Scaling_Calculation'!G10", "='02_Scaling_Calculation'!H10", 0.8667, 0.8182),
        ("P7", "='02_Scaling_Calculation'!G11", "='02_Scaling_Calculation'!H11", 0.9333, 0.9091),
        ("P8", "='02_Scaling_Calculation'!G12", "='02_Scaling_Calculation'!H12", 1.0000, 1.0000),
    ]

    for idx, (pid, f_age, f_sal, v_age, v_sal) in enumerate(points_norm, start=10):
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        # Linked to sheet 01
        ws[f"B{idx}"] = f_age
        ws[f"B{idx}"].font = Font(name="Arial", size=9)
        ws[f"B{idx}"].number_format = "0.0000"
        ws[f"B{idx}"].alignment = CENTER
        ws[f"B{idx}"].border = THIN

        ws[f"C{idx}"] = f_sal
        ws[f"C{idx}"].font = Font(name="Arial", size=9)
        ws[f"C{idx}"].number_format = "0.0000"
        ws[f"C{idx}"].alignment = CENTER
        ws[f"C{idx}"].border = THIN

        f_d1 = f"=SQRT((B{idx}-$C$5)^2 + (C{idx}-$D$5)^2)"
        f_d2 = f"=SQRT((B{idx}-$C$6)^2 + (C{idx}-$D$6)^2)"
        f_cl = f"=IF(D{idx}<=E{idx}, 1, 2)"
        f_dmin2 = f"=IF(F{idx}=1, D{idx}^2, E{idx}^2)"

        _blank(ws, f"D{idx}", solved, f_d1, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"E{idx}", solved, f_d2, "0.0000", YELLOW_FILL, BLACK, CENTER)
        _blank(ws, f"F{idx}", solved, f_cl, "0", YELLOW_FILL, Font(name="Arial", bold=True, color="047857"), CENTER)
        _blank(ws, f"G{idx}", solved, f_dmin2, "0.0000", LIGHT_GREEN_FILL, BLACK, CENTER)

        cmt = "★ ถูกจัดอยู่กลุ่ม 2 อย่างสมเหตุผล (ใกล้ C2 มากกว่า)" if pid == "P5" else "กลุ่มปกติ"
        ws[f"H{idx}"] = cmt
        ws[f"H{idx}"].font = Font(name="Arial", bold=(pid == "P5"), color="047857" if pid == "P5" else "64748B", size=9)
        ws[f"H{idx}"].border = THIN

    # WCSS
    ws["A18"] = "รวม WCSS รอบที่ 1 (Scaled):"
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

    # Centroids Table
    ws["A20"] = "【Centroid ใหม่หลังรอบที่ 1 (Scaled)】: กลุ่มที่ 1 มีสมาชิก 4 คน (P1-P4) และกลุ่มที่ 2 มี 4 คน (P5-P8)"
    ws["A20"].font = SUBBOLD

    _headers(ws, 21, ["กลุ่ม (Cluster)", "จำนวนสมาชิก", "Centroid Age_Norm", "Centroid Sal_Norm", "แปลงกลับเป็นหน่วยจริง (Inverse)"], INDIGO_FILL)

    ws["A22"] = "กลุ่ม 1 (วัยรุ่นและคนรุ่นใหม่)"
    ws["A22"].font = Font(name="Arial", bold=True)
    ws["A22"].border = THIN
    _blank(ws, "B22", solved, "=COUNTIF($F$10:$F$17, 1)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C22", solved, "=AVERAGEIF($F$10:$F$17, 1, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D22", solved, "=AVERAGEIF($F$10:$F$17, 1, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E22"] = '="อายุ ~ " & TEXT(\'02_Scaling_Calculation\'!C16+C22*\'02_Scaling_Calculation\'!C18, "0.0") & " ปี / เงินเดือน ~ " & TEXT(\'02_Scaling_Calculation\'!D16+D22*\'02_Scaling_Calculation\'!D18, "#,##0") & " บาท"' if solved else "สูตรแปลงกลับหน่วยจริง"
    ws["E22"].font = NOTE
    ws["E22"].border = THIN

    ws["A23"] = "กลุ่ม 2 (วัยกลางคนและผู้บริหาร)"
    ws["A23"].font = Font(name="Arial", bold=True)
    ws["A23"].border = THIN
    _blank(ws, "B23", solved, "=COUNTIF($F$10:$F$17, 2)", "0", LIGHT_BLUE_FILL, BLACK, CENTER)
    _blank(ws, "C23", solved, "=AVERAGEIF($F$10:$F$17, 2, $B$10:$B$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    _blank(ws, "D23", solved, "=AVERAGEIF($F$10:$F$17, 2, $C$10:$C$17)", "0.0000", YELLOW_FILL, Font(name="Arial", bold=True), CENTER)
    ws["E23"] = '="อายุ ~ " & TEXT(\'02_Scaling_Calculation\'!C16+C23*\'02_Scaling_Calculation\'!C18, "0.0") & " ปี / เงินเดือน ~ " & TEXT(\'02_Scaling_Calculation\'!D16+D23*\'02_Scaling_Calculation\'!D18, "#,##0") & " บาท"' if solved else "สูตรแปลงกลับหน่วยจริง"
    ws["E23"].font = NOTE
    ws["E23"].border = THIN

    _width(
        ws,
        {
            "A": 16,
            "B": 16,
            "C": 18,
            "D": 16,
            "E": 16,
            "F": 12,
            "G": 16,
            "H": 36,
        },
    )


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# SHEET 6: 05_Comparison_Summary
# -------------------------------------------------------------------------
def build_comparison_sheet(ws: Worksheet, *, solved: bool) -> None:
    ws.title = "05_Comparison_Summary"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = "สรุปเปรียบเทียบผลลัพธ์: Unscaled vs Scaled K-Means และประเด็นข้อสอบ"
    ws["A1"].font = BOLD
    ws.merge_cells("A1:G1")

    _headers(ws, 3, ["รหัส", "อายุ (ปี)", "เงินเดือน (บาท)", "กลุ่มเมื่อไม่ทำ Scaling", "กลุ่มเมื่อทำ Min-Max Scaling", "การเปลี่ยนแปลง", "คำอธิบายเชิงธุรกิจ"], INDIGO_FILL)

    rows = [
        ("P1", 20, 25000, 1, 1, "คงเดิม", "วัยรุ่น รายได้เริ่มต้น"),
        ("P2", 22, 30000, 1, 1, "คงเดิม", "วัยรุ่น รายได้เริ่มต้น"),
        ("P3", 24, 28000, 1, 1, "คงเดิม", "วัยรุ่น รายได้เริ่มต้น"),
        ("P4", 26, 52000, 1, 1, "คงเดิม", "คนรุ่นใหม่ รายได้เติบโตเร็ว"),
        ("P5", 44, 50000, 1, 2, "★ ย้ายไปกลุ่ม 2!", "วัยกลางคน: เมื่อสเกลแล้วความใกล้เคียงด้านอายุพาไปอยู่กลุ่ม 2"),
        ("P6", 46, 70000, 2, 2, "คงเดิม", "ผู้บริหาร/วัยทำงาน รายได้สูง"),
        ("P7", 48, 75000, 2, 2, "คงเดิม", "ผู้บริหาร รายได้สูงมาก"),
        ("P8", 50, 80000, 2, 2, "คงเดิม", "ผู้บริหาร รายได้สูงสุด"),
    ]

    for idx, (pid, age, sal, _un_cl, _sc_cl, _chg, desc) in enumerate(rows, start=4):
        src = idx + 6  # maps row 4 -> 10 (P1) ... row 8 -> 14 (P5) ... row 11 -> 17 (P8)
        ws[f"A{idx}"] = pid
        ws[f"A{idx}"].font = Font(name="Arial", bold=True)
        ws[f"A{idx}"].alignment = CENTER
        ws[f"A{idx}"].border = THIN

        ws[f"B{idx}"] = age
        ws[f"B{idx}"].font = BLACK
        ws[f"B{idx}"].alignment = CENTER
        ws[f"B{idx}"].border = THIN

        ws[f"C{idx}"] = sal
        ws[f"C{idx}"].font = BLACK
        ws[f"C{idx}"].number_format = "#,##0"
        ws[f"C{idx}"].alignment = CENTER
        ws[f"C{idx}"].border = THIN

        f_un = f'=IF(\'03_KMeans_Unscaled\'!F{src}="","-", "กลุ่ม " & \'03_KMeans_Unscaled\'!F{src})'
        f_sc = f'=IF(\'04_KMeans_Scaled\'!F{src}="","-", "กลุ่ม " & \'04_KMeans_Scaled\'!F{src})'
        f_chg = f'=IF(OR(\'03_KMeans_Unscaled\'!F{src}="", \'04_KMeans_Scaled\'!F{src}=""), "-", IF(\'03_KMeans_Unscaled\'!F{src}=\'04_KMeans_Scaled\'!F{src}, "คงเดิม", "★ ย้ายไปกลุ่ม " & \'04_KMeans_Scaled\'!F{src} & "!"))'

        ws[f"D{idx}"] = f_un
        ws[f"D{idx}"].font = Font(name="Arial", bold=True, color="991B1B" if pid == "P5" else "000000")
        ws[f"D{idx}"].alignment = CENTER
        ws[f"D{idx}"].border = THIN

        ws[f"E{idx}"] = f_sc
        ws[f"E{idx}"].font = Font(name="Arial", bold=True, color="047857" if pid == "P5" else "000000")
        ws[f"E{idx}"].alignment = CENTER
        ws[f"E{idx}"].border = THIN

        ws[f"F{idx}"] = f_chg
        ws[f"F{idx}"].font = Font(name="Arial", bold=(pid == "P5"), color="B91C1C" if pid == "P5" else "475569")
        ws[f"F{idx}"].alignment = CENTER
        ws[f"F{idx}"].border = THIN

        ws[f"G{idx}"] = desc
        ws[f"G{idx}"].font = NOTE
        ws[f"G{idx}"].border = THIN

    # Key Takeaways for exams
    ws["A14"] = "🎓 3 ประเด็นสำคัญที่ต้องจำสำหรับห้องสอบ:"
    ws["A14"].font = Font(name="Arial", bold=True, size=11, color="1E3A5F")

    exam_points = [
        "1. เหตุผลที่ K-Means ต้องทำ Feature Scaling เสมอ: เพราะการวัดระยะทางแบบ Euclidean เป็น isotropic (ให้น้ำหนักทุกมิติเท่ากันในทางคณิตศาสตร์) หากมิติใดมีสเกลตัวเลขที่ใหญ่กว่า (เช่น เงินเดือน vs อายุ) มิตินั้นจะครอบงำผลการตัดสินใจทั้งหมด",
        "2. จุดที่เปลี่ยนกลุ่มชัดเจนที่สุดคือ P5 (นายประเสริฐ): ในแบบไม่สเกล P5 ถูกจัดเข้ากลุ่มคนหนุ่มสาวเพราะเงินเดือน 50,000 ใกล้ 25,000 มากกว่า แต่ในแบบสเกล P5 ถูกย้ายไปอยู่กลุ่มคนสูงวัยอย่างถูกต้อง เพราะอายุ 44 ปีสะท้อนพฤติกรรมในชีวิตจริงได้ดีกว่า",
        "3. ข้อสอบมักถามว่า 'อัลกอริทึมใดต้องทำ Feature Scaling บ้าง?': คำตอบคือ โมเดลที่อาศัยระยะทาง (Distance-based) ทั้งหมด เช่น K-Means, k-NN, SVM, PCA ส่วนโมเดลประเภท Decision Tree และ Random Forest ไม่จำเป็นต้องทำ Scaling",
    ]
    for idx, pt in enumerate(exam_points, start=15):
        ws[f"A{idx}"] = pt
        ws[f"A{idx}"].font = Font(name="Arial", size=9)
        ws[f"A{idx}"].alignment = WRAP
        ws.merge_cells(f"A{idx}:G{idx}")
        ws.row_dimensions[idx].height = 36

    _width(
        ws,
        {
            "A": 8,
            "B": 12,
            "C": 18,
            "D": 22,
            "E": 26,
            "F": 18,
            "G": 48,
        },
    )


def build(solved: bool) -> Workbook:
    wb = Workbook()
    build_guide_sheet(wb.active)
    build_step_by_step_sheet(wb.create_sheet(), solved=solved)
    build_scaling_sheet(wb.create_sheet(), solved=solved)
    build_unscaled_kmeans_sheet(wb.create_sheet(), solved=solved)
    build_scaled_kmeans_sheet(wb.create_sheet(), solved=solved)
    build_comparison_sheet(wb.create_sheet(), solved=solved)
    return wb


def main() -> None:
    student = OUT_DIR / "KMeans_Scaling_Practice_TH.xlsx"
    solved = OUT_DIR / "KMeans_Scaling_Practice_TH_Solved.xlsx"
    build(False).save(student)
    build(True).save(solved)
    print(f"Generated successfully: {student.name} and {solved.name}")


if __name__ == "__main__":
    main()
