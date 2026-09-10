"""Lock teaching contracts and verify numerical alignment between Python and Excel worksheet."""

from __future__ import annotations

import math
from kmeans_from_scratch import KMeans

# 8 points matching Worksheet Sheet 01
X_EXCEL = [
    [1.0, 2.0],  # P1
    [2.0, 1.0],  # P2
    [2.0, 3.0],  # P3
    [4.0, 4.0],  # P4
    [6.0, 5.0],  # P5
    [7.0, 7.0],  # P6
    [8.0, 6.0],  # P7
    [8.0, 8.0],  # P8
]

C_INIT = [
    [1.0, 2.0],  # C1 = P1
    [4.0, 4.0],  # C2 = P4
]


def test_euclidean_distance() -> None:
    """ทดสอบสูตรระยะทาง Euclidean ต้องตรงกับการคำนวณมือและ Excel"""
    # d(P1, C1) = 0
    assert KMeans.euclidean_distance([1.0, 2.0], [1.0, 2.0]) == 0.0
    # d(P1, C2) = sqrt((1-4)^2 + (2-4)^2) = sqrt(9 + 4) = sqrt(13) ≈ 3.60555
    d_p1_c2 = KMeans.euclidean_distance([1.0, 2.0], [4.0, 4.0])
    assert abs(d_p1_c2 - math.sqrt(13.0)) < 1e-5
    # d(P8, C2) = sqrt((8-4)^2 + (8-4)^2) = sqrt(16 + 16) = sqrt(32) ≈ 5.65685
    d_p8_c2 = KMeans.euclidean_distance([8.0, 8.0], [4.0, 4.0])
    assert abs(d_p8_c2 - math.sqrt(32.0)) < 1e-5


def test_iteration_1_matches_worksheet() -> None:
    """รอบที่ 1: ตรวจสอบกลุ่ม และ Centroid ใหม่ต้องตรงกับชีต 01_KMeans_2D_Step_by_Step"""
    model = KMeans(n_clusters=2, max_iter=1)
    model.fit(X_EXCEL, initial_centroids=C_INIT, verbose=False)

    # ในรอบแรก P1..P3 อยู่กลุ่ม 1, P4..P8 อยู่กลุ่ม 2
    expected_labels_iter1 = [1, 1, 1, 2, 2, 2, 2, 2]
    assert model.labels_ == expected_labels_iter1

    # Centroid ใหม่หลังรอบ 1:
    # C1 = mean(P1, P2, P3) = (5/3, 6/3) = (1.666667, 2.0)
    assert abs(model.centroids[0][0] - 5.0 / 3.0) < 1e-4
    assert abs(model.centroids[0][1] - 2.0) < 1e-4

    # C2 = mean(P4, P5, P6, P7, P8) = (33/5, 30/5) = (6.6, 6.0)
    assert abs(model.centroids[1][0] - 6.6) < 1e-4
    assert abs(model.centroids[1][1] - 6.0) < 1e-4


def test_iteration_2_point4_swaps_cluster() -> None:
    """รอบที่ 2: จุด P4 ต้องสลับจากกลุ่ม 2 ไปอยู่กลุ่ม 1"""
    model = KMeans(n_clusters=2, max_iter=2)
    model.fit(X_EXCEL, initial_centroids=C_INIT, verbose=False)

    # ในรอบสอง P4 ย้ายไปกลุ่ม 1 ทำให้สมาชิกกลุ่ม 1 มี 4 จุด (P1..P4)
    expected_labels_iter2 = [1, 1, 1, 1, 2, 2, 2, 2]
    assert model.labels_ == expected_labels_iter2

    # Centroid ใหม่หลังรอบ 2:
    # C1 = mean(P1, P2, P3, P4) = (9/4, 10/4) = (2.25, 2.5)
    assert abs(model.centroids[0][0] - 2.25) < 1e-4
    assert abs(model.centroids[0][1] - 2.50) < 1e-4

    # C2 = mean(P5, P6, P7, P8) = (29/4, 26/4) = (7.25, 6.5)
    assert abs(model.centroids[1][0] - 7.25) < 1e-4
    assert abs(model.centroids[1][1] - 6.50) < 1e-4


def test_convergence_and_final_wcss() -> None:
    """ตรวจสอบการลู่เข้าสมบูรณ์ในรอบที่ 3 และค่า WCSS ต้องเท่ากับ 17.5000 พอดี"""
    model = KMeans(n_clusters=2, max_iter=10)
    model.fit(X_EXCEL, initial_centroids=C_INIT, verbose=False)

    # ลู่เข้าในรอบ 3 (เพราะรอบ 3 การจัดกลุ่มไม่เปลี่ยน)
    assert model.n_iter_ == 3

    # พิกัดสุดท้ายตรงกับทฤษฎีเป๊ะ
    assert model.centroids == [[2.25, 2.5], [7.25, 6.5]]

    # WCSS ของกลุ่มสุดท้าย:
    # Group 1 (P1..P4): (1-2.25)^2+(2-2.5)^2 + (2-2.25)^2+(1-2.5)^2 + (2-2.25)^2+(3-2.5)^2 + (4-2.25)^2+(4-2.5)^2
    # Group 2 (P5..P8): (6-7.25)^2+(5-6.5)^2 + (7-7.25)^2+(7-6.5)^2 + (8-7.25)^2+(6-6.5)^2 + (8-7.25)^2+(8-6.5)^2
    # รวม WCSS ทั้งสิ้น = 17.5000
    final_wcss = sum(
        sum((x[j] - model.centroids[label - 1][j]) ** 2 for j in range(2))
        for x, label in zip(X_EXCEL, model.labels_)
    )
    assert abs(final_wcss - 17.5000) < 1e-4


def test_elbow_wcss_progression() -> None:
    """ทดสอบค่า WCSS ในแผ่นงาน 02_Elbow_Method"""
    # K=1: Centroid = mean of all points = (38/8, 36/8) = (4.75, 4.5)
    c_k1 = [38.0 / 8.0, 36.0 / 8.0]
    wcss_k1 = sum(sum((x[j] - c_k1[j]) ** 2 for j in range(2)) for x in X_EXCEL)
    assert abs(wcss_k1 - 99.5000) < 1e-4

    # การลดลงของ WCSS จาก K=1 ไป K=2 ต้องเป็น 82.00 (ลดลง 82.41%)
    drop_1_to_2 = wcss_k1 - 17.5000
    assert abs(drop_1_to_2 - 82.0000) < 1e-4
    pct_drop = drop_1_to_2 / wcss_k1
    assert abs(pct_drop - 0.82412) < 1e-3


if __name__ == "__main__":
    test_euclidean_distance()
    test_iteration_1_matches_worksheet()
    test_iteration_2_point4_swaps_cluster()
    test_convergence_and_final_wcss()
    test_elbow_wcss_progression()
    print("✅ All teaching contracts passed successfully!")
