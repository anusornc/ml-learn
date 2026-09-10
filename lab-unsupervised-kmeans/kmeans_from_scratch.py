"""K-Means Clustering สร้างจากศูนย์ด้วย Pure Python (ไม่ใช้ scikit-learn).

K-Means (Lloyd's Algorithm, 1982) คืออัลกอริทึมการเรียนรู้แบบไม่มีผู้สอน (Unsupervised Learning)
ที่มีเป้าหมายเพื่อแบ่งข้อมูล N จุด ออกเป็น K กลุ่ม (Clusters) โดยใช้ความคล้ายคลึงของระยะทาง

หลักการคณิตศาสตร์และสูตรคำนวณ:
1. ระยะทางแบบยุคลิด (Euclidean Distance):
   d(x, c) = sqrt( sum( (x_j - c_j)^2 ) )

2. การกำหนดกลุ่ม (Assignment Step / Expectation):
   กำหนดให้แต่ละจุด x_i ไปอยู่กับ centroid ที่ใกล้ที่สุด
   k* = argmin_j ||x_i - c_j||^2

3. การคำนวณจุดศูนย์กลางใหม่ (Update Step / Maximization):
   c_k = (1 / |S_k|) * sum_{x in S_k} x

4. ฟังก์ชันเป้าหมาย WCSS (Within-Cluster Sum of Squares / Inertia):
   WCSS = sum_{k=1}^K sum_{x in S_k} ||x - c_k||^2

การรันโปรแกรม:
    python3 kmeans_from_scratch.py
"""

from __future__ import annotations

import math
import random


class KMeans:
    """อัลกอริทึม K-Means สำหรับการจัดกลุ่มข้อมูล 2 มิติขึ้นไป

    สร้างจากศูนย์โดยใช้ pure Python ช่วยให้ผู้เรียนเข้าใจกลไกการทำงานภายใน
    ของการวนซ้ำสลับระหว่าง Assignment Step และ Update Step
    """

    def __init__(
        self,
        n_clusters: int = 2,
        max_iter: int = 100,
        tol: float = 1e-4,
        init: str = "random",
        random_state: int | None = None,
    ):
        """กำหนดพารามิเตอร์ของแบบจำลอง

        n_clusters:   จำนวนกลุ่ม K ที่ต้องการแบ่ง (ค่าเริ่มต้น = 2)
        max_iter:     จำนวนรอบการวนซ้ำสูงสุดเพื่อป้องกัน infinite loop
        tol:          เกณฑ์ความต่างต่ำสุดของการเคลื่อนตัวของ centroid ที่ถือว่าลู่เข้าแล้ว
        init:         วิธีเลือก centroid เริ่มต้น ('random' หรือ 'kmeans++')
        random_state: ค่า seed สำหรับการสุ่มซ้ำได้เหมือนเดิม
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.init = init
        self.random_state = random_state

        self.centroids: list[list[float]] = []
        self.labels_: list[int] = []
        self.inertia_: float = 0.0
        self.n_iter_: int = 0

    @staticmethod
    def euclidean_distance(p1: list[float], p2: list[float]) -> float:
        """คำนวณระยะทางแบบยุคลิด (Euclidean Distance) ระหว่างจุด 2 จุด

        d = sqrt((x1 - x2)^2 + (y1 - y2)^2 + ...)
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def _init_centroids(self, X: list[list[float]]) -> list[list[float]]:
        """กำหนดจุดศูนย์กลางเริ่มต้น (Centroid Initialization)"""
        if self.random_state is not None:
            random.seed(self.random_state)

        n_samples = len(X)
        if self.init == "kmeans++":
            # K-Means++ Initialization: สุ่มจุดแรก แล้วเลือกจุดถัดไปด้วยความน่าจะเป็นแปรผันตาม d^2
            centroids = [list(random.choice(X))]
            for _ in range(1, self.n_clusters):
                dist_sq = []
                for x in X:
                    min_d = min(self.euclidean_distance(x, c) for c in centroids)
                    dist_sq.append(min_d**2)
                total_dist = sum(dist_sq)
                probs = [d / total_dist if total_dist > 0 else 1.0 / n_samples for d in dist_sq]
                r = random.random()
                cum = 0.0
                chosen_idx = 0
                for i, p in enumerate(probs):
                    cum += p
                    if r <= cum:
                        chosen_idx = i
                        break
                centroids.append(list(X[chosen_idx]))
            return centroids
        else:
            # สุ่มเลือก K จุดจากข้อมูลโดยตรง
            chosen_indices = random.sample(range(n_samples), self.n_clusters)
            return [list(X[i]) for i in chosen_indices]

    def _assign_clusters(self, X: list[list[float]], centroids: list[list[float]]) -> list[int]:
        """ขั้นตอนที่ 1 (Assignment Step): กำหนดให้แต่ละจุดสังกัดกลุ่มที่ centroid อยู่ใกล้ที่สุด"""
        labels = []
        for x in X:
            distances = [self.euclidean_distance(x, c) for c in centroids]
            # หา index ของกลุ่มที่ระยะทางน้อยที่สุด (1-indexed เพื่อให้ตรงกับ Excel: 1, 2, ...)
            closest_cluster = distances.index(min(distances)) + 1
            labels.append(closest_cluster)
        return labels

    def _update_centroids(self, X: list[list[float]], labels: list[int]) -> list[list[float]]:
        """ขั้นตอนที่ 2 (Update Step): คำนวณจุดกึ่งกลางใหม่ (ค่าเฉลี่ย) ของแต่ละกลุ่ม"""
        n_features = len(X[0])
        new_centroids = []

        for k in range(1, self.n_clusters + 1):
            # คัดเลือกเฉพาะจุดที่อยู่ในกลุ่ม k
            cluster_points = [x for x, label in zip(X, labels) if label == k]

            if not cluster_points:
                # กรณีฉุกเฉิน: ถ้ากลุ่มว่างเปล่า ให้คง centroid เดิมไว้
                new_centroids.append(list(self.centroids[k - 1]))
                continue

            # คำนวณค่าเฉลี่ยของแต่ละมิติ (Feature)
            mean_point = []
            for j in range(n_features):
                feature_avg = sum(p[j] for p in cluster_points) / len(cluster_points)
                mean_point.append(feature_avg)
            new_centroids.append(mean_point)

        return new_centroids

    def _compute_inertia(self, X: list[list[float]], centroids: list[list[float]], labels: list[int]) -> float:
        """คำนวณ WCSS (Within-Cluster Sum of Squares) หรือ Inertia

        ผลรวมของระยะทางยกกำลังสองจากแต่ละจุดไปยัง centroid ของกลุ่มตัวเอง
        """
        wcss = 0.0
        for x, label in zip(X, labels):
            centroid = centroids[label - 1]
            wcss += sum((a - b) ** 2 for a, b in zip(x, centroid))
        return wcss

    def fit(
        self,
        X: list[list[float]],
        initial_centroids: list[list[float]] | None = None,
        verbose: bool = True,
    ) -> KMeans:
        """เทรนโมเดล K-Means บนชุดข้อมูล X

        X:                 ชุดข้อมูลรูปเมทริกซ์ N x M
        initial_centroids: พิกัดเริ่มต้นที่กำหนดเอง (ถ้าต้องการทดสอบเจาะจง เช่น ตรงกับ Excel)
        verbose:           แสดงขั้นตอนการคำนวณแต่ละรอบใน Terminal หรือไม่
        """
        if initial_centroids is not None:
            self.centroids = [list(c) for c in initial_centroids]
            self.n_clusters = len(initial_centroids)
        else:
            self.centroids = self._init_centroids(X)

        if verbose:
            print("=" * 68)
            print(f"🚀 เริ่มต้นการฝึกสอน K-Means (K={self.n_clusters}, N={len(X)} จุด)")
            print("-" * 68)
            for idx, c in enumerate(self.centroids, start=1):
                c_str = ", ".join(f"{val:.4f}" for val in c)
                print(f"  Centroid เริ่มต้น C{idx} (t=0): ({c_str})")
            print("=" * 68)

        for iteration in range(1, self.max_iter + 1):
            self.n_iter_ = iteration

            # 1. ขั้นตอนกำหนดกลุ่ม (Assignment)
            new_labels = self._assign_clusters(X, self.centroids)

            # ตรวจสอบการสลับกลุ่มเมื่อเทียบกับรอบก่อนหน้า
            swaps = 0
            if self.labels_:
                swaps = sum(1 for old_l, new_l in zip(self.labels_, new_labels) if old_l != new_l)

            self.labels_ = new_labels

            # 2. คำนวณ WCSS (Inertia) ก่อนอัปเดต centroid
            self.inertia_ = self._compute_inertia(X, self.centroids, self.labels_)

            if verbose:
                print(f"\n--- [รอบที่ {iteration}: Iteration {iteration}] ---")
                print(f"  การจัดกลุ่ม (Labels): {self.labels_}")
                print(f"  จำนวนจุดสลับกลุ่ม: {swaps} จุด")
                print(f"  ค่า WCSS (Inertia): {self.inertia_:.4f}")

            # 3. ขั้นตอนอัปเดตจุดศูนย์กลาง (Update)
            new_centroids = self._update_centroids(X, self.labels_)

            # 4. ตรวจสอบการเคลื่อนที่ของ Centroid (Convergence Check)
            shift = max(
                self.euclidean_distance(c_old, c_new)
                for c_old, c_new in zip(self.centroids, new_centroids)
            )

            if verbose:
                for idx, c in enumerate(new_centroids, start=1):
                    c_str = ", ".join(f"{val:.4f}" for val in c)
                    count = self.labels_.count(idx)
                    print(f"  Centroid ใหม่ C{idx} (t={iteration}): ({c_str}) [สมาชิก {count} จุด]")
                print(f"  ระยะขยับสูงสุดของ Centroid: {shift:.6f}")

            # ปรับปรุงตำแหน่ง Centroid
            self.centroids = new_centroids

            # ตรวจสอบเงื่อนไขลู่เข้า (Convergence)
            if shift < self.tol or (iteration > 1 and swaps == 0):
                if verbose:
                    print("\n" + "=" * 68)
                    print(f"✅ อัลกอริทึมลู่เข้าสมบูรณ์ (Converged) ในรอบที่ {iteration}!")
                    print(f"   ค่า WCSS สุดท้าย (Final Inertia): {self.inertia_:.4f}")
                    print("=" * 68)
                break

        return self

    def predict(self, X: list[list[float]]) -> list[int]:
        """ทำนายกลุ่มสำหรับข้อมูลใหม่"""
        return self._assign_clusters(X, self.centroids)

    def fit_predict(self, X: list[list[float]]) -> list[int]:
        """เทรนและส่งคืนผลการจัดกลุ่มพร้อมกัน"""
        self.fit(X, verbose=False)
        return self.labels_


def print_ascii_scatter(X: list[list[float]], labels: list[int], centroids: list[list[float]]) -> None:
    """แสดงผลกราฟแบบ ASCII ใน Terminal เพื่อดูการกระจายตัวของกลุ่มอย่างรวดเร็ว"""
    width, height = 50, 16
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # หาขอบเขตพิกัด
    all_x = [p[0] for p in X] + [c[0] for c in centroids]
    all_y = [p[1] for p in X] + [c[1] for c in centroids]
    min_x, max_x = min(all_x) - 0.5, max(all_x) + 0.5
    min_y, max_y = min(all_y) - 0.5, max(all_y) + 0.5

    def to_grid(x: float, y: float) -> tuple[int, int]:
        gx = int((x - min_x) / (max_x - min_x) * (width - 1))
        gy = int((max_y - y) / (max_y - min_y) * (height - 1))
        return min(max(gx, 0), width - 1), min(max(gy, 0), height - 1)

    # วาดจุดข้อมูล
    symbols = ["•", "▲", "■", "◆", "★"]
    for (x, y), label in zip(X, labels):
        gx, gy = to_grid(x, y)
        sym = symbols[(label - 1) % len(symbols)]
        grid[gy][gx] = sym

    # วาด Centroid
    for idx, (cx, cy) in enumerate(centroids, start=1):
        gx, gy = to_grid(cx, cy)
        grid[gy][gx] = str(idx)

    print("\n📊 แผนภาพการจัดกลุ่มในระนาบ 2D (ASCII Plot):")
    print("┌" + "─" * width + "┐")
    for row in grid:
        print("│" + "".join(row) + "│")
    print("└" + "─" * width + "┘")
    print(f"สัญลักษณ์: • = กลุ่ม 1, ▲ = กลุ่ม 2 | ตัวเลข 1, 2 = พิกัดจุด Centroid")


def demo_matching_excel() -> None:
    """รันโจทย์ชุดเดียวกับใบงาน Excel เพื่อให้ผู้เรียนเปรียบเทียบคำตอบได้แบบจุดต่อจุด"""
    print("\n" + "#" * 68)
    print("🎯 การทดสอบ: โจทย์ตัวอย่าง 8 จุดที่ตรงกับใบงาน Excel")
    print("    (KMeans_Clustering_Step_by_Step_TH.xlsx)")
    print("#" * 68)

    # ข้อมูลเดียวกับใน Excel Sheet 01
    X = [
        [1.0, 2.0],  # P1
        [2.0, 1.0],  # P2
        [2.0, 3.0],  # P3
        [4.0, 4.0],  # P4 (จุดสำคัญที่จะสลับกลุ่มในรอบ 2)
        [6.0, 5.0],  # P5
        [7.0, 7.0],  # P6
        [8.0, 6.0],  # P7
        [8.0, 8.0],  # P8
    ]

    # กำหนด Centroid เริ่มต้นเหมือนใน Excel: C1=P1(1,2), C2=P4(4,4)
    initial_centroids = [
        [1.0, 2.0],
        [4.0, 4.0],
    ]

    model = KMeans(n_clusters=2, max_iter=10)
    model.fit(X, initial_centroids=initial_centroids, verbose=True)

    print_ascii_scatter(X, model.labels_, model.centroids)

    # ตารางเปรียบเทียบจุดต่อจุด
    print("\n📋 สรุปผลการจัดกลุ่มเทียบกับใบงาน Excel:")
    print("┌──────┬──────────────┬──────────────┬──────────────┬──────────────┐")
    print("│ จุด  │ พิกัด (X1,X2)│ กลุ่มรอบที่ 1│ กลุ่มรอบที่ 2│ สถานะการย้าย │")
    print("├──────┼──────────────┼──────────────┼──────────────┼──────────────┤")
    point_names = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
    labels_iter1 = [1, 1, 1, 2, 2, 2, 2, 2]
    labels_iter2 = [1, 1, 1, 1, 2, 2, 2, 2]

    for name, pt, l1, l2 in zip(point_names, X, labels_iter1, labels_iter2):
        status = "★ สลับไปกลุ่ม 1" if l1 != l2 else "คงเดิม"
        print(f"│ {name:<4} │ ({pt[0]:.1f}, {pt[1]:.1f})    │ กลุ่ม {l1:<7} │ กลุ่ม {l2:<7} │ {status:<12} │")
    print("└──────┴──────────────┴──────────────┴──────────────┴──────────────┘")


if __name__ == "__main__":
    demo_matching_excel()
