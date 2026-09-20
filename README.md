# ML Learn: Interactive Machine Learning Curriculum & Practical Labs

[![Curriculum](https://img.shields.io/badge/Curriculum-24%20Chapters-blue.svg)](index.html)
[![Labs](https://img.shields.io/badge/Practical%20Labs-Jupyter%20%26%20Colab-orange.svg)](index.html)
[![Interactive](https://img.shields.io/badge/Interactive-Simulations%20%26%20Sandboxes-emerald.svg)](index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

ชุดบทเรียนเชิงปฏิสัมพันธ์และใบงานปฏิบัติการวิชา **การเรียนรู้ของเครื่อง (Machine Learning)** ครอบคลุมตั้งแต่ทฤษฎีพื้นฐาน จนถึงแบบจำลองสมัยใหม่ พร้อมระบบจำลองแบบโต้ตอบ (Interactive Simulations), เครื่องคำนวณคณิตศาสตร์สด (KaTeX Math), โหมดสไลด์บรรยายในตัว (Presentation Slide Mode) และใบงาน Jupyter Notebook / Google Colab ที่เชื่อมโยงกับคลังโค้ดมาตรฐาน

---

## 🌟 จุดเด่นของชุดบทเรียน (Key Features)

- **Interactive Simulations & Sandboxes:** ทุกบทเรียนมีแบบจำลองภาพเคลื่อนไหวหรือกราฟโต้ตอบ (HTML5 Canvas / SVG) เช่น การปรับระนาบไฮเปอร์เพลน, การลู่เข้าของ Gradient Descent, เครื่องคำนวณ Entropy, การจำลอง Q-Learning Gridworld, K-Means 2D Sandbox, 2D Convolution Visualizer, และ System 1 vs System 2 Race Simulator
- **Math Rigor with KaTeX:** สูตรคณิตศาสตร์ถูกเรนเดอร์อย่างสวยงามและคมชัดด้วย KaTeX พร้อมการพิสูจน์ที่มาทีละขั้น (Step-by-step calculus & derivations)
- **Built-in Presentation Slide Mode:** สามารถกดปุ่ม **"นำเสนอสไลด์"** หรือกดปุ่มคีย์บอร์ดเพื่อแปลงหน้าบทเรียนเป็นสไลด์บรรยายเต็มหน้าจอได้ทันที รองรับปุ่ม `Space`, `ArrowRight`, `ArrowLeft` และ `Esc`
- **Dual-Track Learning (Theory + Code):** เชื่อมโยงเนื้อหาภาคทฤษฎีเข้ากับใบงานปฏิบัติการจริงใน Jupyter Notebook ทั้งจากตำรา *Hands-On Machine Learning (3rd Edition)*, *Python ML Notebooks* และ *Microsoft ML-For-Beginners*

---

## 📚 แผนผังหลักสูตร 24 บทเรียน (Curriculum Structure)

| บทที่ | ไฟล์บทเรียน | หัวข้อภาษาไทย | หัวข้อภาษาอังกฤษ / โมเดลหลัก | การทดลองจำลองสด |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [`01-ML-Intro.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/01-ML-Intro.html) | ปฐมบทการเรียนรู้ของเครื่อง | Introduction to ML & Paradigms | เปรียบเทียบ Supervised / Unsupervised / Semi / Self-Supervised |
| **02** | [`02-ML-Models.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/02-ML-Models.html) | การจำแนกรูปแบบโมเดล | Types of ML Models & Causal DAGs | โมเดลกล่องดำ vs กล่องแก้ว, Causal Inference |
| **03** | [`03-ML-Regression.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/03-ML-Regression.html) | การวิเคราะห์การถดถอย | Linear Regression & Gradient Descent | กราฟลู่เข้าของ Gradient Descent vs Normal Equation |
| **04** | [`04-ML-Regression-Classification.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/04-ML-Regression-Classification.html) | ถดถอยเทียบกับจำแนกประเภท | Regression vs. Classification | เปรียบเทียบ Continuous Output vs Decision Threshold |
| **-** | [`04-training-linear-models-code-slides.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/04-training-linear-models-code-slides.html) | *สไลด์โค้ดบรรยายประกอบ* | Companion Code Slides: Linear Models | สไลด์สรุปโค้ดบรรยายและแบบฝึกหัด |
| **05** | [`05-ML-Evaluation.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/05-ML-Evaluation.html) | การวัดประสิทธิภาพโมเดล | Evaluation Metrics & Loss Functions | Confusion Matrix, ROC-AUC vs PR-Curve บนข้อมูล Imbalanced |
| **06** | [`06-ML-Logistics-Regression.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/06-ML-Logistics-Regression.html) | การถดถอยโลจิสติก | Logistic Regression & Logit Derivation | Sigmoid Curve, Log-Odds $\ln(p/(1-p)) = \mathbf{w}^T\mathbf{x} + b$ |
| **07** | [`07-ML-Logistics-Regression-Step-by-Step.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/07-ML-Logistics-Regression-Step-by-Step.html) | โลจิสติกทีละขั้นตอน | Step-by-Step Gradient & Training Loop | การคำนวณแคลคูลัสเกรเดียนต์ $\frac{\partial L}{\partial w_j} = (\hat{y}-y)x_j$ |
| **08** | [`08-ML-Evaluation-3-Classes.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/08-ML-Evaluation-3-Classes.html) | การประเมินผล 3 คลาส | Multiclass Evaluation (OvR / OvO) | Micro vs Macro F1, ทฤษฎี Micro-F1 = Accuracy |
| **09** | [`09-ML-NN.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/09-ML-NN.html) | โครงข่ายประสาทเทียม | Neural Networks & Deep Learning | ฟังก์ชันกระตุ้น ReLU vs Sigmoid, Vanishing Gradient, Chain Rule |
| **10** | [`10-ML-Inductive-Decision-Trees.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/10-ML-Inductive-Decision-Trees.html) | การเรียนรู้ต้นไม้ตัดสินใจ | Decision Trees: ID3, C4.5 & CART | คำนวณ Entropy, Information Gain, Gini Impurity, Hyperparameters |
| **11** | [`11-ML-Bayesian-Learning.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/11-ML-Bayesian-Learning.html) | การเรียนรู้แบบเบย์ | Bayesian Learning & Naive Bayes | ทฤษฎีบทเบย์, GaussianNB, MultinomialNB, BernoulliNB |
| **12** | [`12-ML-Computational-Theory.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/12-ML-Computational-Theory.html) | ทฤษฎีการเรียนรู้เชิงคำนวณ | Computational Theory & VC Dimension | PAC Learning, Sample Complexity, การ Shatter จุดใน 2 มิติ |
| **13** | [`13-ML-Instance-Based.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/13-ML-Instance-Based.html) | การเรียนรู้อิงตัวอย่าง | Instance-Based Learning & k-NN | Interactive k-NN Simulator, ข้อควรระวัง Feature Scaling |
| **14** | [`14-ML-Learning-Set-of-Rules.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/14-ML-Learning-Set-of-Rules.html) | การเรียนรู้เซตของกฎ | Rule Learning & Association Mining | Sequential Covering, Apriori, คำนวณ Support, Confidence, Lift |
| **15** | [`15-ML-Analytical-Combining.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/15-ML-Analytical-Combining.html) | การเรียนรู้เชิงวิเคราะห์ | Analytical & Combined Learning | EBL, KBANN สู่เทคโนโลยีสมัยใหม่: PINNs, Neuro-symbolic AI, RAG |
| **16** | [`16-ML-Reinforcement-Learning.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/16-ML-Reinforcement-Learning.html) | การเรียนรู้แบบเสริมแรง | Reinforcement Learning & Q-Learning | กระบวนการ MDP, การอัปเดตค่า Q-Table ใน Gridworld, DQN |
| **17** | [`17-ML-Evolutionary-PSO.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/17-ML-Evolutionary-PSO.html) | อัลกอริทึมเชิงวิวัฒนาการ | Genetic Algorithms & PSO | จำลองฝูงบินอนุภาค (PSO Simulator), Velocity Clamping, NAS |
| **18** | [`18-ML-Unsupervised-KMeans.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/18-ML-Unsupervised-KMeans.html) | การจัดกลุ่มแบบไม่กำกับดูแล | Unsupervised Learning & K-Means | 2D Live Clustering Sandbox, K-Means++ vs DBSCAN vs GMM |
| **19** | [`19-ML-Ensemble-Boosting.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/19-ML-Ensemble-Boosting.html) | การเรียนรู้แบบรวมกลุ่ม & บูสติง | Ensemble Learning: Bagging & Boosting | จำลอง Ensemble Simulator, Voting, Random Forest, AdaBoost, XGBoost, LightGBM, CatBoost |
| **20** | [`20-ML-SVM.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/20-ML-SVM.html) | ซัพพอร์ตเวกเตอร์แมชชีน | Support Vector Machines (SVM) | จำลองระนาบ Maximum Margin สด, Soft Margin $C$, Kernel Trick (RBF $\gamma$), SVR |
| **21** | [`21-ML-Dimensionality-Reduction.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/21-ML-Dimensionality-Reduction.html) | การลดมิติข้อมูลและสกัดลักษณะเด่น | Dimensionality Reduction: PCA & Manifold | จำลองหมุนแกน PCA 2D สด, Singular Value Decomposition (SVD), Explained Variance, t-SNE vs UMAP |
| **22** | [`22-ML-Pipelines-Feature-Engineering.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/22-ML-Pipelines-Feature-Engineering.html) | ไพป์ไลน์และวิศวกรรมฟีเจอร์ | ML Pipelines & Feature Engineering | ป้องกัน Data Leakage, การจัดการ Missing Values (MICE/KNN), Encoding, Scikit-Learn Pipeline |
| **23** | [`23-ML-Deep-Learning-Architectures.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/23-ML-Deep-Learning-Architectures.html) | สถาปัตยกรรม Deep Learning ยุคใหม่ | Modern Deep Learning: CNNs & Transformers | จำลองการคำนวณ Convolution 2D สด, ResNet Skip Connections, Multi-Head Attention ($Q,K,V$), Transfer Learning |
| **24** | [`24-ML-System1-Decision-Models-Jev.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/24-ML-System1-Decision-Models-Jev.html) | โมเดลการตัดสินใจเชิงโครงสร้าง และ System 1 AI | Structured Decision Models & Jev AI | จำลองการเปรียบเทียบ System 1 vs System 2 Race สด, Kahneman Dual-Process, 3 Typed Primitives, Calibrated Probabilities |

---

## 🚀 แอปพลิเคชันแซนด์บ็อกซ์และแล็บจำลอง (Special Interactive Apps)

- **K-Means Interactive Sandbox App:** [`lab-unsupervised-kmeans/index.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-unsupervised-kmeans/index.html)  
  เว็บแอปพลิเคชันเดี่ยวเต็มหน้าจอสำหรับทดลองอัลกอริทึม K-Means, K-Means++, การคำนวณ Elbow Method / WCSS และ Silhouette Score แบบเรียลไทม์ พร้อมคู่มือปฏิบัติการ [`lab-unsupervised-kmeans/README.md`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-unsupervised-kmeans/README.md)
- **Neural Network Playground:** [`lab-neural-network/index.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-neural-network/index.html)  
  เว็บแอปพลิเคชันสำหรับทดลองสร้างเครือข่ายประสาทเทียม ปรับเปลี่ยน Hidden Layers, Activation Functions, Learning Rate และสังเกต Decision Boundary แบบสด
- **Jev Model Interactive Decision Sandbox:** [`lab-jev-decision/index.html`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-jev-decision/index.html)  
  เว็บแอปพลิเคชันสำหรับทดสอบ **System 1 AI Decision Model (`typesafe/jev-1.13`)** ส่งคำขอผ่าน REST API ทดลองการตัดสินใจแบบมีโครงสร้าง (`choice`, `score`, `noul`) วัด Latency ระดับมิลลิวินาที พร้อมสคริปต์ทดสอบ [`lab-jev-decision/test_jev_api.py`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-jev-decision/test_jev_api.py) และคู่มือ [`lab-jev-decision/README.md`](file:///Users/anusornchaikaew/Work/lecture/ml-learn/lab-jev-decision/README.md)

---

## 💻 วิธีเปิดใช้งานและรันในเครื่อง (Getting Started)

ชุดบทเรียนนี้ถูกพัฒนาเป็น **Pure Web Technology** (HTML5, Tailwind CSS CDN, KaTeX CDN, Vanilla JavaScript) โดยไม่จำเป็นต้องติดตั้ง Node.js หรือคอมไพล์โค้ด

### 1. โคลนคลังข้อมูล
```bash
git clone https://github.com/anusornc/ml-learn.git
cd ml-learn
```

### 2. รันเว็บเซิร์ฟเวอร์แบบง่าย
คุณสามารถใช้โมดูล HTTP ในตัวของ Python:
```bash
# สำหรับ Python 3
python3 -m http.server 8000
```

### 3. เปิดในเบราว์เซอร์
เปิดเบราว์เซอร์แล้วไปที่:
```text
http://localhost:8000/index.html
```

---

## ⌨️ การควบคุมในโหมดสไลด์ (Slide Navigation Shortcuts)

เมื่ออยู่ในหน้าบทเรียนใดๆ สามารถคลิกที่ปุ่ม **"นำเสนอสไลด์"** ด้านบนขวา หรือใช้ปุ่มลัด:
- `Space` หรือ `→` : สไลด์ถัดไป
- `←` : สไลด์ก่อนหน้า
- `Esc` : ออกจากโหมดสไลด์และกลับสู่หน้าบทเรียนปกติ

---

## 📖 การอ้างอิงและบรรณานุกรม (References)

1. **Géron, Aurélien.** (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
2. **Mitchell, Tom M.** (1997). *Machine Learning*. McGraw-Hill Education.
3. **Russell, Stuart, & Norvig, Peter.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
4. **Bishop, Christopher M.** (2006). *Pattern Recognition and Machine Learning*. Springer.
5. **Goodfellow, Ian, Bengio, Yoshua, & Courville, Aaron.** (2016). *Deep Learning*. MIT Press.
6. **Sutton, Richard S., & Barto, Andrew G.** (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
