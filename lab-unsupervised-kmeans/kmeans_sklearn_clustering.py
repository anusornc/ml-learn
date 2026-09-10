"""ใบงานปฏิบัติการ K-Means Clustering ด้วย Scikit-Learn: การแบ่งกลุ่มลูกค้า (Customer Segmentation).

โจทย์ประยุกต์จริงในธุรกิจ:
ร้านค้าต้องการแบ่งกลุ่มลูกค้า 200 ราย ตามพฤติกรรม 2 มิติ:
1. รายได้ต่อปี (Annual Income in k$)
2. คะแนนพฤติกรรมการใช้จ่าย (Spending Score 1-100)

ขั้นตอนการปฏิบัติการ:
1. สร้างชุดข้อมูลลูกค้าจำลอง (Synthetic Customer Dataset)
2. การเตรียมข้อมูลและสเกลลิ่ง (Feature Scaling ด้วย StandardScaler)
3. การหาจำนวนกลุ่มที่เหมาะสม (Optimal K) ด้วย:
   - Elbow Method (Inertia / WCSS)
   - Silhouette Score (ความกระชับและความห่างระหว่างกลุ่ม)
4. การสร้างโมเดล K-Means ด้วย scikit-learn (K-Means++ Initialization)
5. การวิเคราะห์ข้อมูลเชิงลึก (Cluster Profiling & Business Personas)
6. บันทึกผลเป็นภาพกราฟิกสรุปผลสำหรับการนำเสนอ

การรันโปรแกรม:
    lab-week2/.venv/bin/python kmeans_sklearn_clustering.py
    หรือ python3 kmeans_sklearn_clustering.py (หากติดตั้ง scikit-learn และ matplotlib แล้ว)
"""

from __future__ import annotations

import sys
from pathlib import Path

# ตรวจสอบแพ็กเกจที่จำเป็น
try:
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler
except ImportError as e:
    print(f"⚠️ ไม่พบโมดูล: {e}")
    print("กรุณาติดตั้ง scikit-learn และ numpy หรือรันด้วย:")
    print("    lab-week2/.venv/bin/python kmeans_sklearn_clustering.py")
    sys.exit(1)

OUT_DIR = Path(__file__).resolve().parent


def generate_customer_data(n_samples: int = 200, random_state: int = 42) -> tuple[np.ndarray, list[str]]:
    """สร้างชุดข้อมูลลูกค้าจำลอง 5 กลุ่มพฤติกรรมมาตรฐานในห้างสรรพสินค้า (Mall Customers)"""
    # กำหนดจุดกึ่งกลางของ 5 กลุ่มในโลกความเป็นจริง:
    # 1. รายได้ต่ำ - ใช้จ่ายต่ำ (Sensible)
    # 2. รายได้ต่ำ - ใช้จ่ายสูง (Careless)
    # 3. รายได้ปานกลาง - ใช้จ่ายปานกลาง (Standard)
    # 4. รายได้สูง - ใช้จ่ายต่ำ (Careful)
    # 5. รายได้สูง - ใช้จ่ายสูง (Target / Premium)
    centers = [
        [25, 20],  # Low Income, Low Spend
        [25, 80],  # Low Income, High Spend
        [55, 50],  # Mid Income, Mid Spend
        [85, 20],  # High Income, Low Spend
        [85, 80],  # High Income, High Spend
    ]
    cluster_std = [4.5, 5.0, 6.0, 5.0, 4.8]

    X, _ = make_blobs(
        n_samples=n_samples,
        centers=centers,
        cluster_std=cluster_std,
        random_state=random_state,
    )
    # Clip ให้อยู่ในช่วงที่มีความหมาย
    X[:, 0] = np.clip(X[:, 0], 15, 130)  # Income (k$)
    X[:, 1] = np.clip(X[:, 1], 1, 99)    # Spending Score (1-100)

    feature_names = ["Annual Income (k$)", "Spending Score (1-100)"]
    return X, feature_names


def find_optimal_k(X_scaled: np.ndarray, max_k: int = 8) -> tuple[list[float], list[float], int]:
    """คำนวณ WCSS (Inertia) และ Silhouette Score เพื่อหาค่า K ที่ดีที่สุด"""
    k_range = list(range(1, max_k + 1))
    inertias = []
    silhouette_scores = [0.0]  # k=1 ไม่สามารถคำนวณ silhouette ได้

    print("\n🔍 การประเมินเพื่อหาจำนวนกลุ่มที่เหมาะสม (Optimal K):")
    print("┌──────┬──────────────────┬────────────────────────┐")
    print("│  K   │  Inertia (WCSS)  │    Silhouette Score    │")
    print("├──────┼──────────────────┼────────────────────────┤")

    for k in k_range:
        kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

        if k >= 2:
            score = silhouette_score(X_scaled, kmeans.labels_)
            silhouette_scores.append(score)
            print(f"│  {k:<3} │   {kmeans.inertia_:<14.2f} │       {score:<16.4f} │")
        else:
            print(f"│  {k:<3} │   {kmeans.inertia_:<14.2f} │       -                │")

    print("└──────┴──────────────────┴────────────────────────┘")

    # หา K ที่ได้ Silhouette Score สูงสุด (ตั้งแต่ k=2 ขึ้นไป)
    optimal_k = k_range[1:][int(np.argmax(silhouette_scores[1:]))]
    print(f"💡 คำแนะนำ: ค่า K ที่มี Silhouette Score สูงที่สุดคือ K = {optimal_k}")

    return inertias, silhouette_scores, optimal_k


def train_and_profile_clusters(
    X: np.ndarray,
    X_scaled: np.ndarray,
    k: int,
) -> tuple[KMeans, np.ndarray, dict[int, str]]:
    """เทรนโมเดล K-Means และสร้างโปรไฟล์วิเคราะห์พฤติกรรมของแต่ละคลัสเตอร์"""
    kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = kmeans.fit_predict(X_scaled)

    # นิยาม Persona ทางธุรกิจสำหรับ 5 กลุ่ม
    persona_names = {
        0: "กลุ่มประหยัด (Sensible): รายได้ต่ำ / ใช้จ่ายน้อย",
        1: "กลุ่มใช้จ่ายเกินตัว (Careless): รายได้ต่ำ / ใช้จ่ายสูง",
        2: "กลุ่มคนส่วนใหญ่ (Standard): รายได้ปานกลาง / ใช้จ่ายปานกลาง",
        3: "กลุ่มมัธยัสถ์ (Careful): รายได้สูง / ใช้จ่ายน้อย",
        4: "กลุ่มเป้าหมายหลัก (Premium/VIP): รายได้สูง / ใช้จ่ายสูง",
    }

    # จับคู่ persona ให้ตรงกับ centroid จริง
    centroids_original = []
    for cluster_id in range(k):
        pts = X[labels == cluster_id]
        centroids_original.append(pts.mean(axis=0))

    # จับคู่ตามพิกัดรายได้และคะแนน
    mapped_names = {}
    for cluster_id, (inc, spd) in enumerate(centroids_original):
        if inc < 40 and spd < 40:
            name = "กลุ่มประหยัด (Sensible): รายได้ต่ำ / ใช้จ่ายน้อย"
        elif inc < 40 and spd >= 40:
            name = "กลุ่มใช้จ่ายสูง (Careless): รายได้ต่ำ / ใช้จ่ายสูงมาก"
        elif inc >= 70 and spd < 40:
            name = "กลุ่มมัธยัสถ์ (Careful): รายได้สูง / ระวังการใช้จ่าย"
        elif inc >= 70 and spd >= 40:
            name = "กลุ่มพรีเมียม (Premium VIP): รายได้สูง / ช้อปหนัก"
        else:
            name = "กลุ่มมาตรฐาน (Standard): รายได้ปานกลาง / ใช้จ่ายสมเหตุผล"
        mapped_names[cluster_id] = name

    print(f"\n📊 ผลการวิเคราะห์โปรไฟล์ลูกค้าแยกตามคลัสเตอร์ (K = {k}):")
    print("=" * 82)
    for cluster_id in range(k):
        pts = X[labels == cluster_id]
        count = len(pts)
        pct = (count / len(X)) * 100
        mean_inc = pts[:, 0].mean()
        mean_spd = pts[:, 1].mean()
        print(f"👑 คลัสเตอร์ที่ {cluster_id + 1}: {mapped_names[cluster_id]}")
        print(f"   • สมาชิก: {count} คน ({pct:.1f}% ของลูกค้าทั้งหมด)")
        print(f"   • รายได้เฉลี่ย: {mean_inc:.2f} k$/ปี | คะแนนใช้จ่ายเฉลี่ย: {mean_spd:.2f} / 100")
        print("-" * 82)

    return kmeans, labels, mapped_names


def plot_results(
    X: np.ndarray,
    labels: np.ndarray,
    k: int,
    mapped_names: dict[int, str],
    inertias: list[float],
    silhouette_scores: list[float],
) -> None:
    """สร้างกราฟและบันทึกเป็นรูปภาพ PNG"""
    try:
        import matplotlib
        matplotlib.use("Agg")  # ไม่ต้องเปิดหน้าต่าง GUI
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️ ไม่พบ matplotlib ข้ามขั้นตอนการเซฟภาพกราฟ")
        return

    # 1. แผนภาพ Elbow & Silhouette
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # กราฟซ้าย: Elbow Curve
    k_vals = list(range(1, len(inertias) + 1))
    ax1.plot(k_vals, inertias, "o-", color="#4f46e5", linewidth=2.5, markersize=8)
    ax1.set_title("Elbow Method (Inertia vs K)", fontsize=13, fontweight="bold", pad=10)
    ax1.set_xlabel("Number of Clusters (K)", fontsize=11)
    ax1.set_ylabel("Inertia (Within-Cluster Sum of Squares)", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.axvline(x=k, color="#dc2626", linestyle=":", label=f"Selected K={k}")
    ax1.legend()

    # กราฟขวา: Silhouette Score
    k_sil = list(range(2, len(silhouette_scores) + 1))
    ax2.plot(k_sil, silhouette_scores[1:], "s-", color="#059669", linewidth=2.5, markersize=8)
    ax2.set_title("Silhouette Score vs K", fontsize=13, fontweight="bold", pad=10)
    ax2.set_xlabel("Number of Clusters (K)", fontsize=11)
    ax2.set_ylabel("Silhouette Score (higher is better)", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.axvline(x=k, color="#dc2626", linestyle=":", label=f"Optimal K={k}")
    ax2.legend()

    plt.tight_layout()
    elbow_path = OUT_DIR / "kmeans_elbow_silhouette.png"
    plt.savefig(elbow_path, dpi=200)
    plt.close()
    print(f"📈 บันทึกกราฟ Elbow & Silhouette: {elbow_path.name}")

    # 2. แผนภาพ Customer Clusters Scatter Plot
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]

    # English persona names for clean chart rendering without missing font glyphs
    persona_en = {
        "กลุ่มประหยัด": "Sensible (Low Inc, Low Spend)",
        "กลุ่มใช้จ่ายสูง": "Careless (Low Inc, High Spend)",
        "กลุ่มมัธยัสถ์": "Careful (High Inc, Low Spend)",
        "กลุ่มพรีเมียม": "Premium VIP (High Inc, High Spend)",
        "กลุ่มมาตรฐาน": "Standard (Mid Inc, Mid Spend)",
    }

    for c_id in range(k):
        pts = X[labels == c_id]
        thai_title = mapped_names[c_id].split(":")[0]
        en_title = next((v for k_thai, v in persona_en.items() if k_thai in thai_title), "Cluster")
        ax.scatter(
            pts[:, 0],
            pts[:, 1],
            s=55,
            c=colors[c_id % len(colors)],
            alpha=0.75,
            edgecolors="white",
            linewidth=0.5,
            label=f"Cluster {c_id + 1}: {en_title}",
        )
        # คำนวณและพล็อตจุดศูนย์กลางในสเกลเดิม
        centroid = pts.mean(axis=0)
        ax.scatter(
            centroid[0],
            centroid[1],
            s=220,
            c=colors[c_id % len(colors)],
            marker="X",
            edgecolors="black",
            linewidth=1.5,
        )

    ax.set_title("Customer Segmentation: K-Means Clustering (K=5)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Annual Income (k$)", fontsize=11)
    ax.set_ylabel("Spending Score (1-100)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", frameon=True, facecolor="#f8fafc", framealpha=0.9)

    cluster_path = OUT_DIR / "kmeans_customer_clusters.png"
    plt.tight_layout()
    plt.savefig(cluster_path, dpi=200)
    plt.close()
    print(f"🎨 บันทึกกราฟการแบ่งกลุ่มลูกค้า: {cluster_path.name}")


def main() -> None:
    print("=" * 68)
    print("🛍️ การทดลอง K-Means Customer Segmentation ด้วย Scikit-Learn")
    print("=" * 68)

    # 1. เตรียมข้อมูล
    X, feature_names = generate_customer_data(n_samples=200, random_state=42)
    print(f"สร้างชุดข้อมูลจำลองสำเร็จ: {len(X)} ตัวอย่าง, ฟีเจอร์: {feature_names}")

    # 2. ทำ Feature Scaling (ข้อปฏิบัติที่ดีมากสำหรับ K-Means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. หาค่า K ที่ดีที่สุด
    inertias, silhouette_scores, optimal_k = find_optimal_k(X_scaled, max_k=8)

    # 4. เทรนโมเดลและวิเคราะห์โปรไฟล์ (ใช้ K=5 สำหรับโจทย์แบ่งกลุ่มลูกค้า)
    chosen_k = 5
    kmeans, labels, mapped_names = train_and_profile_clusters(X, X_scaled, k=chosen_k)

    # 5. วาดกราฟและบันทึกไฟล์
    plot_results(X, labels, chosen_k, mapped_names, inertias, silhouette_scores)

    print("\n✅ การทดลองเสร็จสมบูรณ์!")


if __name__ == "__main__":
    main()
