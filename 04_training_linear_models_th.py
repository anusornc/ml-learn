# -*- coding: utf-8 -*-
"""04_training_linear_models.ipynb

โค้ดนี้ถูกแปลงและปรับปรุงจาก Jupyter Notebook บทที่ 4 ของหนังสือ Hands-On Machine Learning (เล่ม 3)
หัวข้อ: การเทรนโมเดลเชิงเส้น (Training Models)
"""

# ==========================================
# 1. ส่วนการตั้งค่าและการเตรียมระบบ (Setup)
# ==========================================

import sys

# ตรวจสอบเวอร์ชันของ Python ว่าต้องเป็นเวอร์ชัน 3.7 ขึ้นไป เพื่อป้องกันปัญหารันโค้ดบางส่วนไม่ได้
assert sys.version_info >= (3, 7)

from packaging import version
import sklearn

# ตรวจสอบเวอร์ชันของไลบรารี Scikit-Learn ว่าต้องเป็นเวอร์ชัน 1.0.1 ขึ้นไป
assert version.parse(sklearn.__version__) >= version.parse("1.0.1")

import matplotlib.pyplot as plt

# ตั้งค่าขนาดฟอนต์มาตรฐานขององค์ประกอบต่าง ๆ ในกราฟเพื่อให้แสดงผลสวยงามและอ่านง่าย
plt.rc('font', size=14)          # ขนาดฟอนต์ทั่วไป
plt.rc('axes', labelsize=14, titlesize=14)  # ขนาดฟอนต์คำอธิบายแกนและชื่อกราฟ
plt.rc('legend', fontsize=14)    # ขนาดฟอนต์ของคำอธิบายสัญลักษณ์ (Legend)
plt.rc('xtick', labelsize=10)    # ขนาดฟอนต์ค่าบนแกน X
plt.rc('ytick', labelsize=10)    # ขนาดฟอนต์ค่าบนแกน Y

from pathlib import Path

# กำหนดโฟลเดอร์ปลายทางสำหรับจัดเก็บรูปภาพกราฟที่จะถูกสร้างขึ้นมาในบทนี้
IMAGES_PATH = Path() / "images" / "training_linear_models"
# สร้างโฟลเดอร์ขึ้นมาจริง ๆ (หากยังไม่มีโฟลเดอร์นี้อยู่ในเครื่อง)
IMAGES_PATH.mkdir(parents=True, exist_ok=True)

# ฟังก์ชันสำหรับการเซฟรูปภาพลงเครื่องคอมพิวเตอร์เป็นไฟล์รูปภาพความละเอียดสูง (.png)
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = IMAGES_PATH / f"{fig_id}.{fig_extension}"  # กำหนดชื่อไฟล์และนามสกุล
    if tight_layout:
        plt.tight_layout()  # ปรับระยะขอบกราฟให้อัตโนมัติเพื่อไม่ให้ข้อความถูกตัดขาด
    plt.savefig(path, format=fig_extension, dpi=resolution)  # สั่งบันทึกภาพด้วยค่าความละเอียดพิกเซลที่ระบุ

# ==========================================
# 2. Linear Regression (การถดถอยเชิงเส้น)
# ==========================================

# --- 2.1 The Normal Equation (สมการปกติทางคณิตศาสตร์) ---

import numpy as np

# กำหนด Seed สุ่มให้เป็นค่าคงที่ (42) เพื่อให้การรันโค้ดทุกครั้งได้ข้อมูลจำลองชุดเดิมเสมอ
np.random.seed(42)  
m = 100  # จำนวนชุดข้อมูลจำลอง (Instances) เท่ากับ 100 จุด
X = 2 * np.random.rand(m, 1)  # สุ่มสร้างค่า X ช่วง 0 ถึง 2 (Matrix แนวตั้ง 100 แถว 1 คอลัมน์)
y = 4 + 3 * X + np.random.randn(m, 1)  # สร้างค่าเป้าหมาย y จากสมการ y = 4 + 3X + Noise (สุ่มกระจายตัวแบบปกติ)

# สร้างรูปภาพ Figure 4–1: กราฟแสดงชุดข้อมูลสุ่มจำลอง
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 4))               # กำหนดขนาดหน้าต่างกราฟ
plt.plot(X, y, "b.")                     # วาดข้อมูล X, y เป็นจุดวงกลมสีน้ำเงิน (blue dots)
plt.xlabel("$x_1$")                      # ชื่อแกน X
plt.ylabel("$y$", rotation=0)            # ชื่อแกน Y (ตั้งตรงไม่เอียง)
plt.axis([0, 2, 0, 15])                  # กำหนดขอบเขตแกน X ที่ 0 ถึง 2 และแกน Y ที่ 0 ถึง 15
plt.grid()                               # แสดงเส้นตาราง (Grid)
save_fig("generated_data_plot")          # บันทึกรูปภาพเก็บไว้
plt.show()                               # แสดงผลกราฟออกหน้าจอ

from sklearn.preprocessing import add_dummy_feature

# เติมค่า x0 = 1 ให้กับทุกๆ แถวของข้อมูล X เพื่อใช้คำนวณค่า Bias (หรือ Intercept θ0) ในรูปแบบ Vector
X_b = add_dummy_feature(X)  
# คำนวณหาพารามิเตอร์ที่ดีที่สุด (theta_best) โดยใช้สมการปกติ: theta = (X^T * X)^-1 * X^T * y
theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

# แสดงผลค่า Theta ที่ได้จากการคำนวณด้วยสมการปกติ (ควรเข้าใกล้ค่าจริงคือ [4, 3])
theta_best

# เตรียมข้อมูลใหม่ 2 จุด (x=0 และ x=2) เพื่อทำการทดสอบทำนายผลลัพธ์
X_new = np.array([[0], [2]])
X_new_b = add_dummy_feature(X_new)  # เติมฟีเจอร์ Bias (x0 = 1) เข้าไปเช่นเดียวกัน
# คำนวณทำนายผลลัพธ์ y โดยการคูณเมทริกซ์ (Matrix Multiplication @) ระหว่าง X และ Theta
y_predict = X_new_b @ theta_best
y_predict  # แสดงค่าที่โมเดลทำนายได้ ณ ตำแหน่ง x = 0 และ x = 2

# สร้างรูปภาพ Figure 4–2: แสดงเส้นการทำนายของโมเดลเปรียบเทียบกับข้อมูลจริง
plt.figure(figsize=(6, 4))
plt.plot(X_new, y_predict, "r-", label="Predictions")  # วาดเส้นพยากรณ์สีแดง (red line)
plt.plot(X, y, "b.")                                   # วาดข้อมูลดิบสีน้ำเงิน
plt.xlabel("$x_1$")
plt.ylabel("$y$", rotation=0)
plt.axis([0, 2, 0, 15])
plt.grid()
plt.legend(loc="upper left")                           # วาดกล่องอธิบายสัญลักษณ์ที่มุมบนซ้าย
save_fig("linear_model_predictions_plot")
plt.show()

from sklearn.linear_model import LinearRegression

# ใช้โมเดลเชิงเส้นสำเร็จรูปจาก Scikit-Learn
lin_reg = LinearRegression()
lin_reg.fit(X, y)                        # สั่งสอน (Train/Fit) โมเดลด้วยข้อมูลจำลอง
# แสดงค่าจุดตัดแกน Y (Intercept) และค่าสัมประสิทธิ์ความชัน (Coefficients)
lin_reg.intercept_, lin_reg.coef_

# ทดลองให้โมเดลทำนายค่า X_new (x=0 และ x=2)
lin_reg.predict(X_new)

# คำนวณพารามิเตอร์โดยใช้ฟังก์ชันกำลังสองน้อยที่สุด (Least Squares SVD) จาก Scipy 
theta_best_svd, residuals, rank, s = np.linalg.lstsq(X_b, y, rcond=1e-6)
theta_best_svd

# แสดงการหาคำตอบด้วย Pseudoinverse (Moore-Penrose Inverse) ของเมทริกซ์ X
np.linalg.pinv(X_b) @ y


# ==========================================
# 3. Gradient Descent (การปรับลดตามค่าความชัน)
# ==========================================

# --- 3.1 Batch Gradient Descent (อัปเดตโดยใช้ข้อมูลทั้งหมดพร้อมกัน) ---

eta = 0.1       # กำหนดค่าอัตราการเรียนรู้ (Learning Rate)
n_epochs = 1000 # จำนวนรอบการทำงานในการเทรนโมเดล
m = len(X_b)    # ดึงค่าจำนวนข้อมูลตัวอย่างทั้งหมด

np.random.seed(42)
theta = np.random.randn(2, 1)  # เริ่มต้นสุ่มพารามิเตอร์ θ (Theta) จากการกระจายตัวแบบปกติ

# เริ่มวนลูปทำการเทรนโมเดลแบบ Batch Gradient Descent
for epoch in range(n_epochs):
    # คำนวณเวกเตอร์ความชัน (Gradients) จากข้อมูลทั้งหมดในคราวเดียว
    gradients = 2 / m * X_b.T @ (X_b @ theta - y)
    # ปรับปรุงพารามิเตอร์ Theta โดยขยับไปในทิศทางตรงกันข้ามกับค่าความชัน
    theta = theta - eta * gradients

# แสดงผลพารามิเตอร์สุดท้ายหลังจากการเทรนครบ 1,000 รอบ
theta

# ฟังก์ชันเสริมสำหรับจำลองขั้นตอนการขยับของเส้นทำนายตามแต่ละค่าของ Learning Rate (eta) เพื่อบันทึกเป็นรูปภาพ
import matplotlib as mpl

def plot_gradient_descent(theta, eta):
    m = len(X_b)
    plt.plot(X, y, "b.")
    n_epochs = 1000
    n_shown = 20  # กำหนดจำนวนเส้นเริ่มต้นที่จะพล็อตให้เห็นการเคลื่อนตัว (20 เส้นแรก)
    theta_path = []
    for epoch in range(n_epochs):
        if epoch < n_shown:
            y_predict = X_new_b @ theta
            # กำหนดไล่เฉดสีส้ม-แดงเพื่อแทนความก้าวหน้าของรอบการเรียนรู้ (ยิ่งแดงยิ่งเรียนรู้ไปไกล)
            color = mpl.colors.rgb2hex(plt.cm.OrRd(epoch / n_shown + 0.15))
            plt.plot(X_new, y_predict, linestyle="solid", color=color)
        # คำนวณ Gradients และอัปเดต Theta
        gradients = 2 / m * X_b.T @ (X_b @ theta - y)
        theta = theta - eta * gradients
        theta_path.append(theta)  # บันทึกพิกัดเส้นทางการเดินของ Theta ไว้วาดกราฟสรุป
    plt.xlabel("$x_1$")
    plt.axis([0, 2, 0, 15])
    plt.grid()
    plt.title(fr"$\eta = {eta}$") # แสดงค่า Learning Rate ในชื่อกราฟด้วยสูตร LaTeX
    return theta_path

np.random.seed(42)
theta = np.random.randn(2, 1)  # สุ่มค่าเริ่มต้นให้กับ Theta อีกครั้ง

# วาดรูปจำลอง Figure 4–8: เปรียบเทียบผลลัพธ์ของ Learning Rate 3 ระดับ (น้อยไป, กำลังดี, และมากเกินไป)
plt.figure(figsize=(10, 4))
plt.subplot(131)
plot_gradient_descent(theta, eta=0.02)  # Learning rate ต่ำเกินไป (ลู่เข้าสู่เป้าหมายช้ามาก)
plt.ylabel("$y$", rotation=0)
plt.subplot(132)
theta_path_bgd = plot_gradient_descent(theta, eta=0.1) # Learning rate กำลังดี (ลู่เข้าเป้าหมายอย่างรวดเร็วและแม่นยำ)
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplot(133)
plt.gca().axes.yaxis.set_ticklabels([])
plot_gradient_descent(theta, eta=0.5)  # Learning rate สูงเกินไป (กระโดดข้ามเป้าหมายและลู่ออกไปเรื่อยๆ)
save_fig("gradient_descent_plot")
plt.show()


# --- 3.2 Stochastic Gradient Descent (อัปเดตพารามิเตอร์ทีละจุดข้อมูล) ---

theta_path_sgd = []  # ลิสต์สำหรับเก็บพิกัดของ Theta ในแต่ละสเต็ป เพื่อนำไปเทียบประสิทธิภาพในตอนท้าย

n_epochs = 50       # เทรนเพียงแค่ 50 รอบใหญ่ (เนื่องจากรันอัปเดตพารามิเตอร์รวดเร็วมากต่อ 1 จุด)
t0, t1 = 5, 50      # พารามิเตอร์ที่ใช้ควบคุมตารางการปรับลด Learning Rate (Learning Schedule)

# ฟังก์ชันกำหนดอัตราการเรียนรู้ให้ค่อย ๆ ลดลง เพื่อไม่ให้เกิดการกระโดดรุนแรงเกินไปเมื่อเข้าใกล้จุดต่ำสุด
def learning_schedule(t):
    return t0 / (t + t1)

np.random.seed(42)
theta = np.random.randn(2, 1)  # สุ่มค่าเริ่มต้นให้กับ Theta

n_shown = 20  
plt.figure(figsize=(6, 4))  

# วนลูปตามรอบ Epoch
for epoch in range(n_epochs):
    # ในแต่ละรอบหลัก จะวนลูปย่อยเท่ากับจำนวนข้อมูลที่มี (m)
    for iteration in range(m):

        # วาดพล็อตเส้นพยากรณ์ในช่วงเริ่มต้นรอบแรก (Epoch 0) จำนวน 20 จุดแรก เพื่อให้เห็นพฤติกรรมของ SGD
        if epoch == 0 and iteration < n_shown:
            y_predict = X_new_b @ theta
            color = mpl.colors.rgb2hex(plt.cm.OrRd(iteration / n_shown + 0.15))
            plt.plot(X_new, y_predict, color=color)

        # สุ่มหยิบดัชนีของจุดข้อมูลขึ้นมา 1 จุดแบบสุ่ม (Stochastic)
        random_index = np.random.randint(m)
        xi = X_b[random_index : random_index + 1]
        yi = y[random_index : random_index + 1]
        # คำนวณค่าความชันเฉพาะจุดข้อมูลนั้นจุดเดียว (ไม่ต้องหารด้วย m ทั้งหมดเหมือน Batch GD)
        gradients = 2 * xi.T @ (xi @ theta - yi)  
        # คำนวณหาค่า Learning Rate ของสเต็ปปัจจุบัน
        eta = learning_schedule(epoch * m + iteration)
        # อัปเดตพารามิเตอร์ Theta
        theta = theta - eta * gradients
        theta_path_sgd.append(theta)  # บันทึกความเคลื่อนไหว

# ตกแต่งกราฟแสดงผลการสุ่มอัปเดตเส้นทำนายของ SGD (Figure 4–10)
plt.plot(X, y, "b.")
plt.xlabel("$x_1$")
plt.ylabel("$y$", rotation=0)
plt.axis([0, 2, 0, 15])
plt.grid()
save_fig("sgd_plot")
plt.show()

theta # แสดงผลลัพธ์พารามิเตอร์ที่คำนวณจากวิธี SGD

from sklearn.linear_model import SGDRegressor

# ใช้โมเดลสำเร็จรูป SGDRegressor ของ Scikit-Learn แบบปิดการทำ Regularization (penalty=None)
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-5, penalty=None, eta0=0.01,
                       n_iter_no_change=100, random_state=42)
# สั่งเทรนโมเดล โดยใช้ y.ravel() เพื่อแปลง Target Vector ให้เป็นรูปทรง 1 มิติตามโครงสร้างของคลาส
sgd_reg.fit(X, y.ravel())  

# แสดงผลค่าพารามิเตอร์ที่เทรนสำเร็จ
sgd_reg.intercept_, sgd_reg.coef_


# --- 3.3 Mini-batch Gradient Descent (อัปเดตทีละกลุ่มย่อย) ---

from math import ceil

n_epochs = 50           # ตั้งค่าเทรนจำนวน 50 รอบใหญ่
minibatch_size = 20     # กำหนดขนาดกลุ่มข้อมูลย่อยในการอัปเดตพารามิเตอร์แต่ละครั้งเป็น 20 จุด
n_batches_per_epoch = ceil(m / minibatch_size)  # คำนวณจำนวนกลุ่มย่อยต่อ 1 รอบใหญ่

np.random.seed(42)
theta = np.random.randn(2, 1)  # สุ่มค่าเริ่มต้นให้กับพารามิเตอร์

t0, t1 = 200, 1000  # พารามิเตอร์กำหนดอัตราการย่อลงของ Learning Rate ใน Mini-batch

def learning_schedule(t):
    return t0 / (t + t1)

theta_path_mgd = [] # ลิสต์เก็บประวัติความเปลี่ยนแปลงของพารามิเตอร์สำหรับวิธี Mini-batch

for epoch in range(n_epochs):
    # สับเปลี่ยน (Shuffle) ข้อมูลทั้งหมดแบบสุ่มทุกรอบใหญ่ ป้องกันลำดับข้อมูลส่งผลต่อการเรียนรู้
    shuffled_indices = np.random.permutation(m)
    X_b_shuffled = X_b[shuffled_indices]
    y_shuffled = y[shuffled_indices]
    
    # แบ่งกลุ่มย่อยและอัปเดตค่าความชันไปเรื่อยๆ จนครบทุกกลุ่มข้อมูล
    for iteration in range(0, n_batches_per_epoch):
        idx = iteration * minibatch_size
        xi = X_b_shuffled[idx : idx + minibatch_size]
        yi = y_shuffled[idx : idx + minibatch_size]
        # คำนวณความชันเฉลี่ยตามขนาดของกลุ่มย่อย (minibatch_size)
        gradients = 2 / minibatch_size * xi.T @ (xi @ theta - yi)
        eta = learning_schedule(epoch * n_batches_per_epoch + iteration)
        theta = theta - eta * gradients
        theta_path_mgd.append(theta) # บันทึกสเต็ปของพารามิเตอร์

# แปลงประวัติที่เก็บไว้ของทั้ง 3 วิธีให้เป็นอาเรย์ของ NumPy เพื่อนำไปวาดเปรียบเทียบแนวทางวิ่งหาจุดที่ดีที่สุด
theta_path_bgd = np.array(theta_path_bgd)
theta_path_sgd = np.array(theta_path_sgd)
theta_path_mgd = np.array(theta_path_mgd)

# วาดกราฟ Figure 4–11: แสดงสเต็ปแนวทางการเดินเข้าหาเป้าหมายพารามิเตอร์ใน Parameter Space
plt.figure(figsize=(7, 4))
plt.plot(theta_path_sgd[:, 0], theta_path_sgd[:, 1], "r-s", linewidth=1, label="Stochastic") # สีแดง: แกว่งมากสุดแต่เร็วมาก
plt.plot(theta_path_mgd[:, 0], theta_path_mgd[:, 1], "g-+", linewidth=2, label="Mini-batch") # สีเขียว: แกว่งปานกลาง สบายตา
plt.plot(theta_path_bgd[:, 0], theta_path_bgd[:, 1], "b-o", linewidth=3, label="Batch")      # สีน้ำเงิน: เดินนิ่ง มุ่งตรงหาจุดต่ำสุด
plt.legend(loc="upper left")
plt.xlabel(r"$\theta_0$")
plt.ylabel(r"$\theta_1$   ", rotation=0)
plt.axis([2.6, 4.6, 2.3, 3.4])
plt.grid()
save_fig("gradient_descent_paths_plot")
plt.show()


# ==========================================
# 4. Polynomial Regression (การถดถอยเชิงพหุนาม)
# ==========================================

np.random.seed(42)
m = 100
X = 6 * np.random.rand(m, 1) - 3                                  # สุ่มค่า X ในช่วง -3 ถึง 3
y = 0.5 * X ** 2 + X + 2 + np.random.randn(m, 1)                 # สร้าง y จากพหุนามกำลังสองพร้อมใส่ Noise

# วาดกราฟพล็อตชุดข้อมูลพหุนามจำลอง (Figure 4–12)
plt.figure(figsize=(6, 4))
plt.plot(X, y, "b.")
plt.xlabel("$x_1$")
plt.ylabel("$y$", rotation=0)
plt.axis([-3, 3, 0, 10])
plt.grid()
save_fig("quadratic_data_plot")
plt.show()

from sklearn.preprocessing import PolynomialFeatures

# แปลงฟีเจอร์เดี่ยวให้เป็นฟีเจอร์พหุนามยกกำลังสอง (degree=2)
poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X) # เรียนรู้โครงสร้างและสกัดฟีเจอร์ยกกำลังสองออกมา
X[0]      # ค่าจริงตำแหน่งแรกสุด

X_poly[0] # ค่าใหม่ในรูปพหุนาม [X, X^2] ของจุดข้อมูลจุดแรก

# นำข้อมูลที่ถูกแปลงพหุนามเรียบร้อยแล้วไปเทรนด้วย LinearRegression เพื่อทำนายผลเชิงพหุนาม
lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)
lin_reg.intercept_, lin_reg.coef_  # แสดงผลค่าคงที่ที่โมเดลค้นพบ (ควรมีค่าประมาณ 2, 1, 0.5)

# สร้างข้อมูลเส้นเรียบ (100 จุด) เพื่อใช้วาดทับและทำนายเส้นทางพหุนามสวยงาม (Figure 4–13)
X_new = np.linspace(-3, 3, 100).reshape(100, 1)
X_new_poly = poly_features.transform(X_new)
y_new = lin_reg.predict(X_new_poly)

plt.figure(figsize=(6, 4))
plt.plot(X, y, "b.")
plt.plot(X_new, y_new, "r-", linewidth=2, label="Predictions")
plt.xlabel("$x_1$")
plt.ylabel("$y$", rotation=0)
plt.legend(loc="upper left")
plt.axis([-3, 3, 0, 10])
plt.grid()
save_fig("quadratic_predictions_plot")
plt.show()

# เปรียบเทียบผลลัพธ์ของสมการพหุนามหลายระดับดีกรี (ดีกรี 1, ดีกรี 2 และ ดีกรี 300) (Figure 4–14)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

plt.figure(figsize=(6, 4))

# ลูปพล็อตทับเปรียบเทียบในรูปเดียว
for style, width, degree in (("r-+", 2, 1), ("b--", 2, 2), ("g-", 1, 300)):
    # สร้างโมเดลแปลงพหุนามของดีกรีปัจจุบัน
    polybig_features = PolynomialFeatures(degree=degree, include_bias=False)
    # คลาสสำหรับทำ Feature Scaling เพื่อปรับขนาดตัวแปรให้เท่ากัน ป้องกันดีกรี 300 เกิดค่ามหาศาลเกินไป
    std_scaler = StandardScaler()
    lin_reg = LinearRegression()
    # สร้าง Pipeline เพื่อมัดรวมขั้นตอนการทำงานไว้ด้วยกันเพื่อความสะดวก
    polynomial_regression = make_pipeline(polybig_features, std_scaler, lin_reg)
    polynomial_regression.fit(X, y) # สอนพารามิเตอร์
    y_newbig = polynomial_regression.predict(X_new)
    label = f"{degree} degree{'s' if degree > 1 else ''}"
    plt.plot(X_new, y_newbig, style, label=label, linewidth=width)

plt.plot(X, y, "b.", linewidth=3)
plt.legend(loc="upper left")
plt.xlabel("$x_1$")
plt.ylabel("$y$", rotation=0)
plt.axis([-3, 3, 0, 10])
plt.grid()
save_fig("high_degree_polynomials_plot") # จะเห็นว่าดีกรี 300 เกิดอาการโอเวอร์ฟิต (Overfitting) อย่างชัดเจน
plt.show()


# ==========================================
# 5. Learning Curves (เส้นกราฟการเรียนรู้)
# ==========================================

from sklearn.model_selection import learning_curve

# สร้างเส้นการเรียนรู้เพื่อประเมินจุดตัดประสิทธิภาพและวิเคราะห์ความคลาดเคลื่อน (RMSE) ของโมเดลเชิงเส้นตรงธรรมดา
train_sizes, train_scores, valid_scores = learning_curve(
    LinearRegression(), X, y, train_sizes=np.linspace(0.01, 1.0, 40), cv=5,
    scoring="neg_root_mean_squared_error")
# แปลงค่าคะแนนติดลบให้กลายเป็นค่า RMSE (Error บวก) โดยหาค่าเฉลี่ยข้ามพับ (Cross-validationfolds)
train_errors = -train_scores.mean(axis=1)
valid_errors = -valid_scores.mean(axis=1)

# วาดกราฟ Figure 4–15: ปัญหา Underfitting จากการใช้ Linear Model ทำนายข้อมูลพหุนาม
plt.figure(figsize=(6, 4))
plt.plot(train_sizes, train_errors, "r-+", linewidth=2, label="train")
plt.plot(train_sizes, valid_errors, "b-", linewidth=3, label="valid")
plt.xlabel("Training set size")
plt.ylabel("RMSE")
plt.grid()
plt.legend(loc="upper right")
plt.axis([0, 80, 0, 2.5])
save_fig("underfitting_learning_curves_plot")
plt.show()

# วิเคราะห์หาเส้นโค้งการเรียนรู้ของโมเดลดีกรี 10 (ซึ่ง Overfit ข้อมูลพหุนามดีกรี 2)
polynomial_regression = make_pipeline(
    PolynomialFeatures(degree=10, include_bias=False),
    LinearRegression())

train_sizes, train_scores, valid_scores = learning_curve(
    polynomial_regression, X, y, train_sizes=np.linspace(0.01, 1.0, 40), cv=5,
    scoring="neg_root_mean_squared_error")

train_errors = -train_scores.mean(axis=1)
valid_errors = -valid_scores.mean(axis=1)

# วาดกราฟ Figure 4–16: แสดงการวิเคราะห์แบบ Overfitting
plt.figure(figsize=(6, 4))
plt.plot(train_sizes, train_errors, "r-+", linewidth=2, label="train")
plt.plot(train_sizes, valid_errors, "b-", linewidth=3, label="valid")
plt.legend(loc="upper right")
plt.xlabel("Training set size")
plt.ylabel("RMSE")
plt.grid()
plt.axis([0, 80, 0, 2.5])
save_fig("learning_curves_plot") # สังเกตช่องว่าง (Gap) ระหว่างเส้น Train และ Valid
plt.show()


# ==========================================
# 6. Regularized Linear Models (โมเดลเชิงเส้นที่มีการควบคุมพารามิเตอร์)
# ==========================================

# --- 6.1 Ridge Regression (L2 Regularization) ---

np.random.seed(42)
m = 20
X = 3 * np.random.rand(m, 1)
y = 1 + 0.5 * X + np.random.randn(m, 1) / 1.5                    # สุ่มข้อมูลตัวอย่างขนาดเล็กที่มีความแปรปรวนสูง
X_new = np.linspace(0, 3, 100).reshape(100, 1)

# พล็อตตัวอย่างข้อมูลสุ่มขนาดเล็ก 20 จุด
plt.figure(figsize=(6, 4))
plt.plot(X, y, ".")
plt.xlabel("$x_1$")
plt.ylabel("$y$  ", rotation=0)
plt.axis([0, 3, 0, 3.5])
plt.grid()
plt.show()

from sklearn.linear_model import Ridge

# เทรนโมเดลแบบ Ridge (L2) ด้วยวิธี Cholesky Matrix Factorization โดยมีไฮเปอร์พารามิเตอร์คุมความตึงเครียด (alpha=0.1)
ridge_reg = Ridge(alpha=0.1, solver="cholesky")
ridge_reg.fit(X, y)
ridge_reg.predict([[1.5]]) # ลองทดสอบพยากรณ์ค่าที่ตำแหน่ง x=1.5

# ฟังก์ชันอรรถประโยชน์วาดผลกระทบของโมเดลเมื่อปรับแต่งพารามิเตอร์ควบคุม Alpha ค่าน้อยไปหามาก (Figure 4–17)
def plot_model(model_class, polynomial, alphas, **model_kwargs):
    plt.plot(X, y, "b.", linewidth=3)
    # วนลูปวาดกราฟเส้นผลลัพธ์ของแต่ละ Alpha (สัญลักษณ์: จุดประ, แดชขีด, เส้นทึบ)
    for alpha, style in zip(alphas, ("b:", "g--", "r-")):
        if alpha > 0:
            model = model_class(alpha, **model_kwargs)
        else:
            model = LinearRegression() # ถ้า alpha=0 จะได้ LinearRegression ปกติ
        if polynomial:
            model = make_pipeline(
                PolynomialFeatures(degree=10, include_bias=False),
                StandardScaler(),
                model)
        model.fit(X, y)
        y_new_regul = model.predict(X_new)
        plt.plot(X_new, y_new_regul, style, linewidth=2,
                 label=fr"$\alpha = {alpha}$")
    plt.legend(loc="upper left")
    plt.xlabel("$x_1$")
    plt.axis([0, 3, 0, 3.5])
    plt.grid()

# แสดงผลเปรียบเทียบความยืดหยุ่นของโมเดลฝั่งซ้าย (Linear) และฝั่งขวา (Polynomial ดีกรี 10) ของ Ridge
plt.figure(figsize=(9, 3.5))
plt.subplot(121)
plot_model(Ridge, polynomial=False, alphas=(0, 10, 100), random_state=42)
plt.ylabel("$y$  ", rotation=0)
plt.subplot(122)
plot_model(Ridge, polynomial=True, alphas=(0, 10**-5, 1), random_state=42)
plt.gca().axes.yaxis.set_ticklabels([])
save_fig("ridge_regression_plot")
plt.show()

# ทำงานในรูปแบบ SGDRegressor ที่ใส่บทลงโทษโทษปรับแบบ "l2" เพื่อทำ Ridge Regression
sgd_reg = SGDRegressor(penalty="l2", alpha=0.1 / m, tol=None,
                       max_iter=1000, eta0=0.01, random_state=42)
sgd_reg.fit(X, y.ravel())
sgd_reg.predict([[1.5]])

# ใช้โมเดล Ridge อีกหนึ่งตัวทำนายผ่าน Solver แบบ Stochastic Average Gradient descent (sag)
ridge_reg = Ridge(alpha=0.1, solver="sag", random_state=42)
ridge_reg.fit(X, y)
ridge_reg.predict([[1.5]])

# แสดงการคำนวณหาสูตรสมการปิดของ Ridge ทางคณิตศาสตร์โดยตรงและนำไปเปรียบเทียบกับโมเดลจริงด้านบน
alpha = 0.1
A = np.array([[0., 0.], [0., 1.]])
X_b = np.c_[np.ones(m), X]
np.linalg.inv(X_b.T @ X_b + alpha * A) @ X_b.T @ y

# แสดงจุดตัดแกนและสัมประสิทธิ์พารามิเตอร์ที่คำนวณเสร็จสิ้น
ridge_reg.intercept_, ridge_reg.coef_


# --- 6.2 Lasso Regression (L1 Regularization) ---

from sklearn.linear_model import Lasso

# ใช้โมเดล Lasso (L1 Regularization) ซึ่งโดดเด่นในการตัดค่าฟีเจอร์ที่ไม่จำเป็นให้กลายเป็น 0 โดยตรง (Sparse Model)
lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(X, y)
lasso_reg.predict([[1.5]])

# พล็อตภาพ Figure 4–18: เปรียบเทียบผลลัพธ์การบีบพารามิเตอร์ของ Lasso
plt.figure(figsize=(9, 3.5))
plt.subplot(121)
plot_model(Lasso, polynomial=False, alphas=(0, 0.1, 1), random_state=42)
plt.ylabel("$y$  ", rotation=0)
plt.subplot(122)
plot_model(Lasso, polynomial=True, alphas=(0, 1e-2, 1), random_state=42)
plt.gca().axes.yaxis.set_ticklabels([])
save_fig("lasso_regression_plot")
plt.show()

# -------------------------------------------------------------
# ส่วนของโค้ดสคริปต์ขนาดใหญ่สำหรับพล็อตภาพทางทฤษฎีเปรียบเทียบพฤติกรรมการอัปเดตน้ำหนัก (Weights)
# ระหว่าง l1 และ l2 ในกราฟ Contour (Figure 4–19)
# -------------------------------------------------------------

t1a, t1b, t2a, t2b = -1, 3, -1.5, 1.5

t1s = np.linspace(t1a, t1b, 500)
t2s = np.linspace(t2a, t2b, 500)
t1, t2 = np.meshgrid(t1s, t2s)
T = np.c_[t1.ravel(), t2.ravel()]
Xr = np.array([[1, 1], [1, -1], [1, 0.5]])
yr = 2 * Xr[:, :1] + 0.5 * Xr[:, 1:]

J = (1 / len(Xr) * ((T @ Xr.T - yr.T) ** 2).sum(axis=1)).reshape(t1.shape)

N1 = np.linalg.norm(T, ord=1, axis=1).reshape(t1.shape)
N2 = np.linalg.norm(T, ord=2, axis=1).reshape(t1.shape)

t_min_idx = np.unravel_index(J.argmin(), J.shape)
t1_min, t2_min = t1[t_min_idx], t2[t_min_idx]

t_init = np.array([[0.25], [-1]])

# ฟังก์ชันคำนวณพาธทางเดินหาความชันแบบ BGD สำหรับวาดเส้นเปรียบเทียบ
def bgd_path(theta, X, y, l1, l2, core=1, eta=0.05, n_iterations=200):
    path = [theta]
    for iteration in range(n_iterations):
        gradients = (core * 2 / len(X) * X.T @ (X @ theta - y)
                     + l1 * np.sign(theta) + l2 * theta)
        theta = theta - eta * gradients
        path.append(theta)
    return np.array(path)

fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10.1, 8))

for i, N, l1, l2, title in ((0, N1, 2.0, 0, "Lasso"), (1, N2, 0, 2.0, "Ridge")):
    JR = J + l1 * N1 + l2 * 0.5 * N2 ** 2

    tr_min_idx = np.unravel_index(JR.argmin(), JR.shape)
    t1r_min, t2r_min = t1[tr_min_idx], t2[tr_min_idx]

    levels = np.exp(np.linspace(0, 1, 20)) - 1
    levelsJ = levels * (J.max() - J.min()) + J.min()
    levelsJR = levels * (JR.max() - JR.min()) + JR.min()
    levelsN = np.linspace(0, N.max(), 10)

    path_J = bgd_path(t_init, Xr, yr, l1=0, l2=0)
    path_JR = bgd_path(t_init, Xr, yr, l1, l2)
    path_N = bgd_path(theta=np.array([[2.0], [0.5]]), X=Xr, y=yr,
                      l1=np.sign(l1) / 3, l2=np.sign(l2), core=0)
    ax = axes[i, 0]
    ax.grid()
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    ax.contourf(t1, t2, N / 2.0, levels=levelsN)
    ax.plot(path_N[:, 0], path_N[:, 1], "y--")
    ax.plot(0, 0, "ys")
    ax.plot(t1_min, t2_min, "ys")
    ax.set_title(fr"$\ell_{i + 1}$ penalty")
    ax.axis([t1a, t1b, t2a, t2b])
    if i == 1:
        ax.set_xlabel(r"$\theta_1$")
    ax.set_ylabel(r"$\theta_2$", rotation=0)

    ax = axes[i, 1]
    ax.grid()
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    ax.contourf(t1, t2, JR, levels=levelsJR, alpha=0.9)
    ax.plot(path_JR[:, 0], path_JR[:, 1], "w-o")
    ax.plot(path_N[:, 0], path_N[:, 1], "y--")
    ax.plot(0, 0, "ys")
    ax.plot(t1_min, t2_min, "ys")
    ax.plot(t1r_min, t2r_min, "rs")
    ax.set_title(title)
    ax.axis([t1a, t1b, t2a, t2b])
    if i == 1:
        ax.set_xlabel(r"$\theta_1$")

save_fig("lasso_vs_ridge_plot")
plt.show()


# --- 6.3 Elastic Net (ลูกผสมระหว่าง L1 และ L2) ---

from sklearn.linear_model import ElasticNet

# ใช้โมเดล ElasticNet ซึ่งผสานจุดแข็งระหว่าง Ridge และ Lasso ไว้ด้วยกัน โดยมี l1_ratio=0.5 เป็นสัดส่วนการผสม
elastic_net = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic_net.fit(X, y)
elastic_net.predict([[1.5]])


# --- 6.4 Early Stopping (หยุดเทรนล่วงหน้าเมื่อประสิทธิภาพแย่ลง) ---

# ใช้โครงสร้างบล็อก Try/Except ตรวจสอบพาทของเมตริกประเมินผล RMSE จาก Scikit-learn
try:
    from sklearn.metrics import root_mean_squared_error
except ImportError:
    # หากเป็น Scikit-learn เวอร์ชันเก่าที่ไม่มีฟังก์ชันโดยตรง ให้แปลงผ่านโมดูลคำนวณกำลังสองเฉลี่ยและถอดรูทแทน
    from sklearn.metrics import mean_squared_error

    def root_mean_squared_error(labels, predictions):
        return mean_squared_error(labels, predictions, squared=False)

from copy import deepcopy
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
m = 100
X = 6 * np.random.rand(m, 1) - 3
y = 0.5 * X ** 2 + X + 2 + np.random.randn(m, 1)
# แบ่งกลุ่มย่อยสำหรับ Train (50%) และ Validation (50%)
X_train, y_train = X[: m // 2], y[: m // 2, 0]
X_valid, y_valid = X[m // 2 :], y[m // 2 :, 0]

# ทำการสกัดข้อมูลเป็นพหุนามดีกรี 90 (ซับซ้อนจัด) และปรับค่าข้อมูลให้เข้าเกณฑ์มาตรฐาน
preprocessing = make_pipeline(PolynomialFeatures(degree=90, include_bias=False),
                              StandardScaler())
X_train_prep = preprocessing.fit_transform(X_train)
X_valid_prep = preprocessing.transform(X_valid)

# สร้าง SGDRegressor แบบไม่ใส่ Regularization (ความซับซ้อนทั้งหมดจะขึ้นอยู่กับการจบรอบการเรียนรู้)
sgd_reg = SGDRegressor(penalty=None, eta0=0.002, random_state=42)
n_epochs = 500
best_valid_rmse = float('inf') # ตั้งตัวแปรเปรียบเทียบที่ค่าอนันต์อินฟินิตี้
train_errors, val_errors = [], []

# เริ่มกระบวนการเทรนและสังเกตเพื่อทำ Early Stopping
for epoch in range(n_epochs):
    sgd_reg.partial_fit(X_train_prep, y_train) # ฟิตข้อมูลเพิ่มทีละรอบ
    y_valid_predict = sgd_reg.predict(X_valid_prep)
    val_error = root_mean_squared_error(y_valid, y_valid_predict)
    
    # ตรวจสอบว่าความคลาดเคลื่อนฝั่ง Validation ดีที่สุดแล้วหรือยัง หากใช่จะบันทึกโมเดลนี้ไว้ (โมเดลที่ดีที่สุด)
    if val_error < best_valid_rmse:
        best_valid_rmse = val_error
        best_model = deepcopy(sgd_reg) # ทำการ Deep Copy เก็บสถานะโมเดล ณ จุดที่เกิดความคลาดเคลื่อนต่ำสุด

    # เก็บสะสมค่าความผิดพลาดไว้ทำแผนภูมิแสดงผลเปรียบเทียบในภายหลัง
    y_train_predict = sgd_reg.predict(X_train_prep)
    train_error = root_mean_squared_error(y_train, y_train_predict)
    val_errors.append(val_error)
    train_errors.append(train_error)

# พล็อตภาพ Figure 4–20: แสดงจุดตัดและสเต็ปการทำหยุดทำงานก่อนล่วงหน้า (Early Stopping)
best_epoch = np.argmin(val_errors)
plt.figure(figsize=(6, 4))
plt.annotate('Best model',
             xy=(best_epoch, best_valid_rmse),
             xytext=(best_epoch, best_valid_rmse + 0.5),
             ha="center",
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.plot([0, n_epochs], [best_valid_rmse, best_valid_rmse], "k:", linewidth=2)
plt.plot(val_errors, "b-", linewidth=3, label="Validation set")
plt.plot(best_epoch, best_valid_rmse, "bo")
plt.plot(train_errors, "r--", linewidth=2, label="Training set")
plt.legend(loc="upper right")
plt.xlabel("Epoch")
plt.ylabel("RMSE")
plt.axis([0, n_epochs, 0, 3.5])
plt.grid()
save_fig("early_stopping_plot")
plt.show()


# ==========================================
# 7. Logistic Regression (การถดถอยโลจิสติก)
# ==========================================

# --- 7.1 Estimating Probabilities (การประเมินความน่าจะเป็น / ฟังก์ชันซิกมอยด์) ---

# โค้ดสำหรับพล็อตฟังก์ชัน Logistic/Sigmoid เพื่อเปรียบเทียบค่าทางสถิติ (Figure 4–21)
lim = 6
t = np.linspace(-lim, lim, 100)
sig = 1 / (1 + np.exp(-t)) # ฟังก์ชันคณิตศาสตร์สลับปรับระดับค่าให้บีบลงตัวระหว่าง 0 ถึง 1

plt.figure(figsize=(8, 3))
plt.plot([-lim, lim], [0, 0], "k-")
plt.plot([-lim, lim], [0.5, 0.5], "k:")
plt.plot([-lim, lim], [1, 1], "k:")
plt.plot([0, 0], [-1.1, 1.1], "k-")
plt.plot(t, sig, "b-", linewidth=2, label=r"$\sigma(t) = \dfrac{1}{1 + e^{-t}}$")
plt.xlabel("t")
plt.legend(loc="upper left")
plt.axis([-lim, lim, -0.1, 1.1])
plt.gca().set_yticks([0, 0.25, 0.5, 0.75, 1])
plt.grid()
save_fig("logistic_function_plot")
plt.show()


# --- 7.2 Decision Boundaries (เส้นแบ่งขอบเขตการตัดสินใจ) ---

from sklearn.datasets import load_iris

# ดึงชุดข้อมูลทดสอบทางพฤกษศาสตร์ที่มีชื่อเสียงมากคือ ดอกไม้ไอริส (Iris Dataset)
iris = load_iris(as_frame=True)
list(iris) # ตรวจสอบรายการคีย์ฟิลด์ของชุดข้อมูล

print(iris.DESCR)  # แสดงคำอธิบายโครงสร้างและรายละเอียดของข้อมูลไอริส

iris.data.head(3) # แอบดูข้อมูลฟีเจอร์ตัวอย่าง 3 แถวแรก

iris.target.head(3)  # แอบดูฉลากเฉลยเป้าหมายคลาส (ยังไม่ได้ถูกสลับสับสุ่มตำแหน่ง)

iris.target_names # ตรวจชื่อสายพันธุ์ดอกไม้ ['setosa', 'versicolor', 'virginica']

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# สนใจสกัดเฉพาะตัวแปร 'ความกว้างของกลีบดอก (petal width)' ไปวิเคราะห์
X = iris.data[["petal width (cm)"]].values
# กำหนดเงื่อนไขแปลงผลลัพธ์ให้ตอบ True/False หากสายพันธุ์คือ 'virginica' (ทำ Binary Classification)
y = iris.target_names[iris.target] == 'virginica'
# แบ่งกลุ่มสำหรับทำ Train และ Test
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# ติดตั้งบิลด์และเทรนโมเดล LogisticRegression
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)

# สุ่มชุดข้อมูลทำพล็อตและคำนวณคาดการณ์ความน่าจะเป็น
X_new = np.linspace(0, 3, 1000).reshape(-1, 1)  # สุ่มข้อมูลความกว้างกลีบ 0 ถึง 3 ซม. จำนวน 1000 จุด
y_proba = log_reg.predict_proba(X_new)         # ทำนายค่าความน่าจะเป็นในแต่ละจุดสุ่ม (ผลลัพธ์เป็น 2 คอลัมน์)
# สกัดตำแหน่งขอบเขตการตัดสินใจ (Decision Boundary) ที่พารามิเตอร์โอกาสผ่านเกณฑ์ร้อยละ 50 (>= 0.5)
decision_boundary = X_new[y_proba[:, 1] >= 0.5][0, 0]

# พล็อตรูปภาพขอบเขตและการวิเคราะห์โอกาสน่าจะเป็น (Figure 4–23)
plt.figure(figsize=(8, 3))
plt.plot(X_new, y_proba[:, 0], "b--", linewidth=2,
         label="Not Iris virginica proba")
plt.plot(X_new, y_proba[:, 1], "g-", linewidth=2, label="Iris virginica proba")
plt.plot([decision_boundary, decision_boundary], [0, 1], "k:", linewidth=2,
         label="Decision boundary")

# เติมแต่งรายละเอียดองค์ประกอบกราฟสัญลักษณ์ลูกศรและพิกัดความหนาแน่นจุดข้อมูลจริงในอดีตเพื่อความเข้าใจง่าย
plt.arrow(x=decision_boundary, y=0.08, dx=-0.3, dy=0,
          head_width=0.05, head_length=0.1, fc="b", ec="b")
plt.arrow(x=decision_boundary, y=0.92, dx=0.3, dy=0,
          head_width=0.05, head_length=0.1, fc="g", ec="g")
plt.plot(X_train[y_train == 0], y_train[y_train == 0], "bs") # จุดเหลี่ยมสีน้ำเงินแทนคลาสที่ไม่ใช่ Virginica
plt.plot(X_train[y_train == 1], y_train[y_train == 1], "g^") # สามเหลี่ยมสีเขียวแทนคลาสที่เป็น Virginica
plt.xlabel("Petal width (cm)")
plt.ylabel("Probability")
plt.legend(loc="center left")
plt.axis([0, 3, -0.02, 1.02])
plt.grid()
save_fig("logistic_regression_plot")
plt.show()

decision_boundary # พิกัดความกว้างกลีบที่เป็นจุดตัดสินใจ (ประมาณ 1.61 ซม.)

log_reg.predict([[1.7], [1.5]]) # ตรวจการจำแนกผล (กว้าง 1.7 ซม. คือ True เป็นพันธุ์ Virginica, ส่วน 1.5 ซม. เป็น False)

# -------------------------------------------------------------
# โค้ดส่วนนี้ประยุกต์ดึงตัวแปร 2 มิติ (ความยาวและกว้างกลีบดอก) มาวิเคราะห์ร่วมกัน
# เพื่อหาพิกัดพื้นที่เชิงระนาบในการตัดกรอบการตัดสินใจของ Logistic (Figure 4–24)
# -------------------------------------------------------------

X = iris.data[["petal length (cm)", "petal width (cm)"]].values
y = iris.target_names[iris.target] == 'virginica'
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# เทรนโลจิสติกส์โดยใส่ค่า C=2 คอยปรับโทษความตึงเครียด (C สูงควบคุมพารามิเตอร์เบาลง)
log_reg = LogisticRegression(C=2, random_state=42)
log_reg.fit(X_train, y_train)

# สร้างแกนตาข่ายเมทริกซ์ 2 มิติ
x0, x1 = np.meshgrid(np.linspace(2.9, 7, 500).reshape(-1, 1),
                     np.linspace(0.8, 2.7, 200).reshape(-1, 1))
X_new = np.c_[x0.ravel(), x1.ravel()]
y_proba = log_reg.predict_proba(X_new)
zz = y_proba[:, 1].reshape(x0.shape)

# ตรรกะหาสมการพยากรณ์เส้นตัดขอบเขตแบบเส้นตรง 2 มิติ
left_right = np.array([2.9, 7])
boundary = -((log_reg.coef_[0, 0] * left_right + log_reg.intercept_[0])
             / log_reg.coef_[0, 1])

# พล็อตพื้นที่ขอบเขตการตัดสินใจและการกระจายจุดข้อมูล
plt.figure(figsize=(10, 4))
plt.plot(X_train[y_train == 0, 0], X_train[y_train == 0, 1], "bs")
plt.plot(X_train[y_train == 1, 0], X_train[y_train == 1, 1], "g^")
contour = plt.contour(x0, x1, zz, cmap=plt.cm.brg) # วาดเส้นคอนทัวร์ไล่ระดับความน่าจะเป็น
plt.clabel(contour, inline=1)
plt.plot(left_right, boundary, "k--", linewidth=3)
plt.text(3.5, 1.27, "Not Iris virginica", color="b", ha="center")
plt.text(6.5, 2.3, "Iris virginica", color="g", ha="center")
plt.xlabel("Petal length")
plt.ylabel("Petal width")
plt.axis([2.9, 7, 0.8, 2.7])
plt.grid()
save_fig("logistic_regression_contour_plot")
plt.show()


# --- 7.3 Softmax Regression (การพยากรณ์กรณีมากกว่าสองคลาส) ---

X = iris.data[["petal length (cm)", "petal width (cm)"]].values
y = iris["target"] # ใช้เป้าหมาย 3 คลาสทั้งหมด (0, 1, 2)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# เทรนแบบ LogisticRegression สำหรับ Multi-class โดยอัตโนมัติ (Softmax / Multinomial)
softmax_reg = LogisticRegression(C=30, random_state=42)
softmax_reg.fit(X_train, y_train)

softmax_reg.predict([[5, 2]]) # พยากรณ์ดอกไม้ที่มีความยาวกลีบ 5 ซม. และกว้าง 2 ซม. (คลาส 2 คือ Virginica)

softmax_reg.predict_proba([[5, 2]]).round(2) # แสดงสัดส่วนโอกาสความน่าจะเป็นในแต่ละคลาส


# โค้ดพล็อตพื้นที่จำแนกของโมเดล Softmax แบบแบ่งกลุ่มเฉดสีแยก 3 สายพันธุ์ (Figure 4–25)
from matplotlib.colors import ListedColormap

# แถบสีพื้นหลังของแต่ละคลาส
custom_cmap = ListedColormap(["#fafab0", "#9898ff", "#a0faa0"])

x0, x1 = np.meshgrid(np.linspace(0, 8, 500).reshape(-1, 1),
                     np.linspace(0, 3.5, 200).reshape(-1, 1))
X_new = np.c_[x0.ravel(), x1.ravel()]

y_proba = softmax_reg.predict_proba(X_new)
y_predict = softmax_reg.predict(X_new)

zz1 = y_proba[:, 1].reshape(x0.shape)
zz = y_predict.reshape(x0.shape)

plt.figure(figsize=(10, 4))
plt.plot(X[y == 2, 0], X[y == 2, 1], "g^", label="Iris virginica")
plt.plot(X[y == 1, 0], X[y == 1, 1], "bs", label="Iris versicolor")
plt.plot(X[y == 0, 0], X[y == 0, 1], "yo", label="Iris setosa")

plt.contourf(x0, x1, zz, cmap=custom_cmap)
contour = plt.contour(x0, x1, zz1, cmap="hot")
plt.clabel(contour, inline=1)
plt.xlabel("Petal length")
plt.ylabel("Petal width")
plt.legend(loc="center left")
plt.axis([0.5, 7, 0, 3.5])
plt.grid()
save_fig("softmax_regression_contour_plot")
plt.show()


# =============================================================
# 8. คำตอบและโค้ดเฉลยแบบฝึกหัดข้อ 12 (Softmax ด้วย Numpy แมนนวล)
# =============================================================

# --- นำเข้าข้อมูลและจัดเตรียมพิกดขอบเขตข้อมูลสำหรับคำนวณแมนนวล ---
X = iris.data[["petal length (cm)", "petal width (cm)"]].values
y = iris["target"].values

# สร้างเวกเตอร์ x0 = 1 เข้าไปแมนนวลเพื่อทำตัวแปรเสริม Bias
X_with_bias = np.c_[np.ones(len(X)), X]

# แบ่งกลุ่มเซ็ตข้อมูลออกเป็น Train (60%), Validation (20%) และ Test (20%) แบบแมนนวล
test_ratio = 0.2
validation_ratio = 0.2
total_size = len(X_with_bias)

test_size = int(total_size * test_ratio)
validation_size = int(total_size * validation_ratio)
train_size = total_size - test_size - validation_size

np.random.seed(42)
rnd_indices = np.random.permutation(total_size) # สลับดัชนีแบบสุ่ม

# จัดแถวสับเปลี่ยนข้อมูลตามกลุ่มต่าง ๆ
X_train = X_with_bias[rnd_indices[:train_size]]
y_train = y[rnd_indices[:train_size]]
X_valid = X_with_bias[rnd_indices[train_size:-test_size]]
y_valid = y[rnd_indices[train_size:-test_size]]
X_test = X_with_bias[rnd_indices[-test_size:]]
y_test = y[rnd_indices[-test_size:]]

# ฟังก์ชันแปลงตัวแปรเป้าหมาย (Class Indices) เป็น One-Hot Vector (ความน่าจะเป็นเป้าหมาย 1.0 หรือ 0.0)
def to_one_hot(y):
    return np.diag(np.ones(y.max() + 1))[y]

y_train[:10]  # ดึงข้อมูล Target 10 แถวแรก

to_one_hot(y_train[:10]) # แอบทดลองระบบฟังก์ชัน One-hot ดึงดูความถูกต้อง

# แปลงเฉลยเป็น One-hot ครบถ้วนทุกชุดย่อย
Y_train_one_hot = to_one_hot(y_train)
Y_valid_one_hot = to_one_hot(y_valid)
Y_test_one_hot = to_one_hot(y_test)

# ทำ Feature Scaling ข้อมูลตัวอย่างแมนนวล โดยคำนวณหา Mean และ Standard Deviation ของแกน X จากฝั่ง Train
mean = X_train[:, 1:].mean(axis=0)
std = X_train[:, 1:].std(axis=0)
X_train[:, 1:] = (X_train[:, 1:] - mean) / std
X_valid[:, 1:] = (X_valid[:, 1:] - mean) / std
X_test[:, 1:] = (X_test[:, 1:] - mean) / std

# ฟังก์ชันทางคณิตศาสตร์คำนวณสัดส่วนเฉลี่ยของ Softmax
def softmax(logits):
    exps = np.exp(logits)
    exp_sums = exps.sum(axis=1, keepdims=True)
    return exps / exp_sums

# กำหนดมิติข้อมูลขาเข้า (Inputs) และ ขาออก (Outputs)
n_inputs = X_train.shape[1]  # == 3 ฟีเจอร์ (2 ฟีเจอร์หลักบวก Bias)
n_outputs = len(np.unique(y_train))  # == 3 คลาสตามชนิดพรรณไม้

# --- เริ่มเทรนแมนนวล Batch GD สำหรับ Softmax Regression ครั้งแรก ---
eta = 0.5
n_epochs = 5001
m = len(X_train)
epsilon = 1e-5 # ตัวเลขจำลองป้องกันจุดหลุดเป็น 0 เมื่อนำไปคำนวณ Log

np.random.seed(42)
Theta = np.random.randn(n_inputs, n_outputs) # สุ่มพารามิเตอร์เริ่มต้น

# วนลูปคำนวณ
for epoch in range(n_epochs):
    logits = X_train @ Theta
    Y_proba = softmax(logits)
    # แสดงค่าความสูญเสียในหน้าต่าง Console ทุก ๆ 1000 รอบหลัก
    if epoch % 1000 == 0:
        Y_proba_valid = softmax(X_valid @ Theta)
        xentropy_losses = -(Y_valid_one_hot * np.log(Y_proba_valid + epsilon))
        print(epoch, xentropy_losses.sum(axis=1).mean())
    error = Y_proba - Y_train_one_hot
    gradients = 1 / m * X_train.T @ error
    Theta = Theta - eta * gradients # ปรับน้ำหนักพารามิเตอร์

Theta # ผลลัพธ์เมทริกซ์พารามิเตอร์ที่คิดแมนนวลได้สำเร็จ

# ประเมินวัดผลความแม่นยำบนชุด Validation Set
logits = X_valid @ Theta
Y_proba = softmax(logits)
y_predict = Y_proba.argmax(axis=1) # สกัดเลือกเอาคลาสที่มีโอกาสคาดการณ์สูงสุดออกมา

accuracy_score = (y_predict == y_valid).mean()
accuracy_score # แสดงค่าสัดส่วนความแม่นยำ (Accuracy)


# --- เทรนแมนนวลแบบบวกเพิ่ม L2 Regularization เข้าช่วยบีบความหนาพารามิเตอร์ ---
eta = 0.5
n_epochs = 5001
m = len(X_train)
epsilon = 1e-5
alpha = 0.01  # ไฮเปอร์พารามิเตอร์บทลงโทษน้ำหนัก

np.random.seed(42)
Theta = np.random.randn(n_inputs, n_outputs)

for epoch in range(n_epochs):
    logits = X_train @ Theta
    Y_proba = softmax(logits)
    if epoch % 1000 == 0:
        Y_proba_valid = softmax(X_valid @ Theta)
        xentropy_losses = -(Y_valid_one_hot * np.log(Y_proba_valid + epsilon))
        l2_loss = 1 / 2 * (Theta[1:] ** 2).sum() # คำนวณโทษปรับยกกำลังสองของน้ำหนัก (ไม่นับส่วน Bias ในแถวแรก)
        total_loss = xentropy_losses.sum(axis=1).mean() + alpha * l2_loss
        print(epoch, total_loss.round(4))
    error = Y_proba - Y_train_one_hot
    gradients = 1 / m * X_train.T @ error
    # บวกเพิ่ม Gradients ของบทลงโทษตัวแปรลงไป
    gradients += np.r_[np.zeros([1, n_outputs]), alpha * Theta[1:]]
    Theta = Theta - eta * gradients

# ทวนประเมินผลอีกครั้งหลังคุมความกว้างพารามิเตอร์เสร็จสิ้น
logits = X_valid @ Theta
Y_proba = softmax(logits)
y_predict = Y_proba.argmax(axis=1)

accuracy_score = (y_predict == y_valid).mean()
accuracy_score


# --- เทรนแมนนวลขั้นสุดท้ายโดยผสาน L2 Regularization และเพิ่มเงื่อนไขหยุดเมื่อล้มเหลว (Early Stopping) ---
eta = 0.5
n_epochs = 50_001
m = len(X_train)
epsilon = 1e-5
C = 100  # ค่ากลับของความเข้มงวดในการปรับพารามิเตอร์บทลงโทษ (1/C)
best_loss = np.inf

np.random.seed(42)
Theta = np.random.randn(n_inputs, n_outputs)

for epoch in range(n_epochs):
    logits = X_train @ Theta
    Y_proba = softmax(logits)
    Y_proba_valid = softmax(X_valid @ Theta)
    xentropy_losses = -(Y_valid_one_hot * np.log(Y_proba_valid + epsilon))
    l2_loss = 1 / 2 * (Theta[1:] ** 2).sum()
    total_loss = xentropy_losses.sum(axis=1).mean() + 1 / C * l2_loss
    
    if epoch % 1000 == 0:
        print(epoch, total_loss.round(4))
        
    # เงื่อนไขตรวจการหยุดแบบ Early Stopping: หากค่าความสูญเสียรอบปัจจุบันเริ่มถอยหลังและแย่ลงกว่ารอบที่ดีที่สุด
    if total_loss < best_loss:
        best_loss = total_loss
    else:
        # สั่งตัดวงจรหยุดทำงานและแสดงผลลัพธ์รอบที่ทำงานที่ดีที่สุด
        print(epoch - 1, best_loss.round(4))
        print(epoch, total_loss.round(4), "early stopping!")
        break
    error = Y_proba - Y_train_one_hot
    gradients = 1 / m * X_train.T @ error
    gradients += np.r_[np.zeros([1, n_outputs]), 1 / C * Theta[1:]]
    Theta = Theta - eta * gradients

# แสดงพยากรณ์และวัดค่าชุด Validation
logits = X_valid @ Theta
Y_proba = softmax(logits)
y_predict = Y_proba.argmax(axis=1)

accuracy_score = (y_predict == y_valid).mean()
accuracy_score


# --- การแสดงพื้นที่ขอบเขตการตัดสินใจของโมเดลแมนนวล Softmax บนแผนภูมิสองมิติ ---
custom_cmap = mpl.colors.ListedColormap(['#fafab0', '#9898ff', '#a0faa0'])

x0, x1 = np.meshgrid(np.linspace(0, 8, 500).reshape(-1, 1),
                     np.linspace(0, 3.5, 200).reshape(-1, 1))
X_new = np.c_[x0.ravel(), x1.ravel()]
X_new = (X_new - mean) / std # ต้องปรับสเกลของชุดข้อมูลพล็อตให้ตรงสถิติเดิมของ Train เสมอ
X_new_with_bias = np.c_[np.ones(len(X_new)), X_new]

logits = X_new_with_bias @ Theta
Y_proba = softmax(logits)
y_predict = Y_proba.argmax(axis=1)

zz1 = Y_proba[:, 1].reshape(x0.shape)
zz = y_predict.reshape(x0.shape)

plt.figure(figsize=(10, 4))
plt.plot(X[y == 2, 0], X[y == 2, 1], "g^", label="Iris virginica")
plt.plot(X[y == 1, 0], X[y == 1, 1], "bs", label="Iris versicolor")
plt.plot(X[y == 0, 0], X[y == 0, 1], "yo", label="Iris setosa")

plt.contourf(x0, x1, zz, cmap=custom_cmap)
contour = plt.contour(x0, x1, zz1, cmap="hot")
plt.clabel(contour, inline=1)
plt.xlabel("Petal length")
plt.ylabel("Petal width")
plt.legend(loc="upper left")
plt.axis([0, 7, 0, 3.5])
plt.grid()
plt.show()


# --- ทำการประเมินรอบสุดท้ายของที่สุดแห่งพารามิเตอร์บนข้อมูลชุดที่ไม่เคยเห็นมาก่อน (Test Set) ---
logits = X_test @ Theta
Y_proba = softmax(logits)
y_predict = Y_proba.argmax(axis=1)

accuracy_score = (y_predict == y_test).mean()
accuracy_score # แสดงค่าคะแนนความถูกต้องขั้นสมบูรณ์ของโมเดลคณิตศาสตร์