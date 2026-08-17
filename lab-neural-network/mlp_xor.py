"""Multi-Layer Perceptron (MLP) สร้างจากศูนย์เพื่อแก้ปัญหา XOR (ไม่ใช้ไลบรารีภายนอก).

Perceptron แบบเดี่ยว (ดู perceptron.py) ไม่สามารถเรียนรู้ XOR ได้เพราะ XOR ไม่สามารถ
แบ่งแยกได้เชิงเส้น การเพิ่มชั้นซ่อน (hidden layer) หนึ่งชั้นพร้อมฟังก์ชันการกระตุ้นแบบไม่เชิงเส้น
(sigmoid) ช่วยแก้ปัญหานี้ได้: นิวรอนในชั้นซ่อนจะสร้างตัวแทนภายใน (internal representation) ใหม่
ของอินพุตซึ่งเป็นแบบที่นิวรอนเอาต์พุตสามารถแบ่งแยกได้เชิงเส้น

สถาปัตยกรรมโครงข่าย (2 - 2 - 1):

    x1 ─┬─► [hidden 1] ─┐
        │    sigmoid    ├─► [output] ─► y_hat
    x2 ─┴─► [hidden 2] ─┘     sigmoid
              sigmoid

การเทรน = backpropagation ด้วย gradient descent:

    1. Forward pass:  คำนวณการกระตุ้น (activations) ทีละชั้น
    2. Loss:          MSE = 0.5 * (y_hat - y)^2
    3. Backward pass: กฎลูกโซ่ (chain rule) โดยใช้ sigmoid'(z) = sigmoid(z)*(1-sigmoid(z))
    4. Update:        w -= learning_rate * dLoss/dw

การรันโปรแกรม:  python3 mlp_xor.py
"""

import math
import random


def sigmoid(z: float) -> float:
    """ฟังก์ชันการกระตุ้นแบบ Sigmoid: ปรับย่อขนาดค่าใดๆ ให้เข้าสู่ช่วง (0, 1) ได้อย่างราบรื่น

    ต่างจากฟังก์ชันขั้นบันได (step function) แบบเด็ดขาดของ perceptron ฟังก์ชัน sigmoid
    จะมีความราบรื่นและสามารถหาอนุพันธ์ได้ทุกจุด ความราบรื่นนี้เป็นสิ่งจำเป็น: backpropagation
    จำเป็นต้องใช้อนุพันธ์เพื่อรู้ว่าควรขยับ weight แต่ละตัวไปในทิศทางใด
    ถ้า z ใกล้ 0 เอาต์พุตจะใกล้ 0.5; z บวกมาก → ใกล้ 1; z ลบมาก → ใกล้ 0
    """
    return 1.0 / (1.0 + math.exp(-z))


def sigmoid_derivative(a: float) -> float:
    """อนุพันธ์ของ sigmoid เขียนในรูปของเอาต์พุต a (ไม่ใช่จากอินพุต z)

    ถ้า a = sigmoid(z) แล้ว ตามหลักแคลคูลัสจะได้ d(sigmoid)/dz = a * (1 - a)
    เราใช้สิ่งนี้ในขั้นตอน backward pass: ซึ่งจะบอกว่าเอาต์พุตของนิวรอนมีความไว (sensitive)
    ต่ออินพุตของมันมากแค่ไหน นิวรอนที่อิ่มตัวใกล้ 0 หรือ 1 อยู่แล้วจะมีอนุพันธ์ใกล้ 0
    หมายความว่ามันแทบจะไม่เกิดการเรียนรู้ (ปัญหา "vanishing gradient")
    """
    return a * (1.0 - a)


class MLP:
    """โครงข่ายประสาทเทียมหลายชั้นแบบเชื่อมต่อกันสมบูรณ์ (Fully-connected multi-layer perceptron) พร้อมการกระตุ้นด้วย sigmoid

    "เชื่อมต่อกันสมบูรณ์" หมายความว่าทุกนิวรอนในชั้นหนึ่งจะเชื่อมต่อกับทุกนิวรอนในชั้นถัดไป
    ข้อมูลจะไหลไปในทิศทางเดียว (อินพุต -> ชั้นซ่อน -> เอาต์พุต) ในระหว่างการทำนาย
    ส่วนระหว่างการเทรน สัญญาณข้อผิดพลาดจะไหลย้อนกลับเพื่อปรับแต่ง weights
    นี่คือโครงสร้างหลักเบื้องหลังโครงข่ายประสาทเทียมแบบคลาสสิกส่วนใหญ่
    """

    def __init__(self, layer_sizes: list[int], learning_rate: float = 2.0, seed: int = 0):
        """สร้างโครงข่ายประสาทเทียมและสุ่มค่าเริ่มต้นสำหรับ weights

        layer_sizes:    จำนวนนิวรอนในแต่ละชั้น เรียงตามลำดับ
                        เช่น [2, 2, 1] = 2 อินพุต, 2 นิวรอนชั้นซ่อน, 1 เอาต์พุต
        learning_rate:  ขนาดก้าวในการเดินของ gradient-descent
        seed:           ตรึงการสุ่มค่าเริ่มต้นของ weight เพื่อให้การรันในแต่ละครั้งได้ผลซ้ำเดิม
                        (seed เดียวกัน -> weight เริ่มต้นเหมือนกัน)
        """
        rng = random.Random(seed)
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate

        # weights[l][j][i] = weight จากนิวรอน i ในชั้น l ไปยังนิวรอน j ในชั้น l+1
        # biases[l][j]     = bias ของนิวรอน j ในชั้น l+1
        #
        # เราต้องเริ่มต้นด้วย weight แบบสุ่ม (ไม่ใช่ศูนย์) ถ้านิวรอนชั้นซ่อนทุกตัว
        # เริ่มต้นด้วย weight เท่ากันหมด พวกมันจะคำนวณได้ผลลัพธ์เหมือนกันและ
        # ได้รับการอัปเดตเท่ากันทุกประการ -- ชั้นซ่อนจะยุบรวมเหลือเทียบเท่ากับ
        # นิวรอนเดียว การตั้งค่าเริ่มต้นแบบสุ่มช่วย "ทำลายความสมมาตร" (breaks symmetry)
        self.weights = []
        self.biases = []
        # zip(layer_sizes[:-1], layer_sizes[1:]) จับคู่แต่ละชั้นกับชั้นถัดไป:
        # สำหรับ [2,2,1] จะได้ (2,2) จากนั้น (2,1) -> เมทริกซ์ weight สองชุด
        for n_in, n_out in zip(layer_sizes[:-1], layer_sizes[1:]):
            # หนึ่งแถวต่อนิวรอนปลายทาง; หนึ่งสมาชิกต่อนิวรอนต้นทาง
            w = [[rng.uniform(-1.0, 1.0) for _ in range(n_in)] for _ in range(n_out)]
            # ค่า bias เริ่มต้นที่ศูนย์; พวกมันจะถูกเรียนรู้เช่นเดียวกับ weight
            b = [0.0] * n_out
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x: list[float]) -> list[list[float]]:
        """Forward pass: ส่งอินพุตผ่านทุกชั้นเพื่อทำนายผลลัพธ์

        คืนค่าการกระตุ้น (activations) ของทุกชั้น (อินพุต, ชั้นซ่อน, ..., เอาต์พุต)
        ไม่ใช่เฉพาะคำตอบสุดท้าย เพราะขั้นตอน backward pass จำเป็นต้องใช้การกระตุ้น
        ของแต่ละชั้นเพื่อคำนวณค่าเกรเดียนต์ (gradients)

        สำหรับแต่ละนิวรอนเราคำนวณ: activation = sigmoid(weighted_sum + bias)
        """
        # activations[0] คืออินพุตดิบ; activations[-1] คือเอาต์พุตสุดท้าย
        activations = [list(x)]
        for w, b in zip(self.weights, self.biases):
            # สร้างการกระตุ้นของชั้นถัดไป ทีละนิวรอน
            x = [
                sigmoid(sum(wi * ai for wi, ai in zip(row, x)) + bj)
                for row, bj in zip(w, b)
            ]
            activations.append(x)
        return activations

    def backward(self, activations: list[list[float]], y: float) -> list[list[float]]:
        """Backward pass (backpropagation): คำนวณสัญญาณข้อผิดพลาด (error signal) ของแต่ละนิวรอน

        ค่า "delta" ของนิวรอนวัดว่านิวรอนตัวนั้นรับผิดชอบต่อข้อผิดพลาดสุดท้ายมากเพียงใด
        เราคำนวณค่า delta จากชั้นเอาต์พุตและส่งแพร่ย้อนกลับทีละชั้น
        โดยใช้กฎลูกโซ่ (chain rule) ทางแคลคูลัส

        ชั้นเอาต์พุต: delta = (y_hat - y) * sigmoid'(z)
                      (ทำนายผิดพลาดเท่าใด ปรับขนาดตามความไวของนิวรอน)
        ชั้นซ่อน:   delta = (ผลรวมของ deltas ชั้นถัดไป * weights) * sigmoid'(z)
                      (ความผิดของแต่ละนิวรอนชั้นซ่อน = ส่วนแบ่งข้อผิดพลาดของชั้นถัดไป
                      ถ่วงน้ำหนักตามความแรงของสัญญาณที่ส่งไปชั้นนั้น)

        คืนค่า deltas[l] = รายการค่า delta สำหรับนิวรอนในชั้น l+1
        """
        # --- ชั้นเอาต์พุต ---
        a_out = activations[-1]  # การกระตุ้นที่ทำนายได้ของโครงข่าย
        # (a - y) คือข้อผิดพลาดดิบ; คูณด้วย sigmoid' เพื่อให้ได้เกรเดียนต์
        deltas = [[(a - y) * sigmoid_derivative(a) for a in a_out]]

        # --- ชั้นซ่อน ย้อนกลับจากชั้นที่อยู่ใกล้เอาต์พุตที่สุด ---
        for l in range(len(self.weights) - 2, -1, -1):
            w_next = self.weights[l + 1]      # weights ที่ออกจากชั้นนี้
            delta_next = deltas[0]            # deltas ของชั้นถัดจากชั้นนี้
            a = activations[l + 1]            # การกระตุ้นของชั้นนี้
            # delta ของแต่ละนิวรอนชั้นซ่อน = ความไวของมัน (sigmoid') คูณด้วย
            # ผลรวมถ่วงน้ำหนักของ deltas ที่มันมีส่วนร่วมในชั้นถัดไป
            deltas.insert(0, [
                sigmoid_derivative(a_j) * sum(
                    w_next[k][j] * delta_next[k] for k in range(len(delta_next))
                )
                for j, a_j in enumerate(a)
            ])
        return deltas

    def update_weights(self, activations: list[list[float]], deltas: list[list[float]]) -> None:
        """ขั้นตอน Gradient descent: ปรับขยับ weight และ bias ทุกตัวเพื่อลดข้อผิดพลาด

        เกรเดียนต์ของความสูญเสีย (loss) เทียบกับ weight เท่ากับ
        (delta ของนิวรอนปลายทาง) * (activation ของนิวรอนต้นทาง)
        เราเคลื่อน weight แต่ละตัวไปในทิศทางตรงกันข้ามกับเกรเดียนต์ของมัน (จึงมีเครื่องหมายลบ)
        ปรับขนาดตาม learning rate
        """
        for l, (w, b) in enumerate(zip(self.weights, self.biases)):
            a_prev = activations[l]           # อินพุตที่มาถึงชั้น l+1
            delta = deltas[l]                 # ข้อผิดพลาดของนิวรอนในชั้น l+1
            for j in range(len(b)):           # สำหรับนิวรอนปลายทางแต่ละตัว...
                for i in range(len(a_prev)):  # ...และจุดเชื่อมต่อขาเข้าแต่ละเส้น...
                    w[j][i] -= self.learning_rate * delta[j] * a_prev[i]
                # การอัปเดต bias: เหมือนกับ weight ที่การกระตุ้นขาเข้าเป็น 1 เสมอ
                b[j] -= self.learning_rate * delta[j]

    def fit(self, X: list[list[float]], y: list[float], n_epochs: int = 10000,
            log_every: int = 1000) -> None:
        """เทรนโครงข่ายโดยทำซ้ำขั้นตอน forward/backward/update บนข้อมูล

        หนึ่ง epoch = การวนลูปผ่านตัวอย่างข้อมูลเทรนทุกตัวครบหนึ่งรอบ สำหรับแต่ละตัวอย่างเราจะ:
            1. forward()        -> ได้รับผลการทำนาย
            2. วัดค่า loss     -> วัดความผิดพลาดของการทำนาย (MSE)
            3. backward()       -> คำนวณส่วนแบ่งข้อผิดพลาดของนิวรอนแต่ละตัว
            4. update_weights() -> ปรับขยับ weights เพื่อลดข้อผิดพลาดนั้น
        การทำซ้ำเช่นนี้หลายพันครั้งจะค่อยๆ สร้างคำตอบสำหรับ XOR ขึ้นมา
        """
        for epoch in range(1, n_epochs + 1):
            epoch_loss = 0.0  # สะสมค่าความสูญเสียของ epoch นี้ เพื่อการบันทึก log เท่านั้น
            for xi, yi in zip(X, y):
                activations = self.forward(xi)      # ขั้นตอนที่ 1: ทำนาย
                y_hat = activations[-1][0]          # เอาต์พุตเดียวของโครงข่าย
                epoch_loss += 0.5 * (y_hat - yi) ** 2  # ขั้นตอนที่ 2: MSE loss
                deltas = self.backward(activations, yi)  # ขั้นตอนที่ 3: ระบุส่วนแบ่งข้อผิดพลาด
                self.update_weights(activations, deltas)  # ขั้นตอนที่ 4: เรียนรู้

            # พิมพ์ความคืบหน้าใน epoch แรกและทุกๆ log_every epoch
            if epoch == 1 or epoch % log_every == 0:
                print(f"epoch {epoch:>5} | loss: {epoch_loss / len(X):.6f}")

    def predict(self, x: list[float]) -> float:
        """คืนค่าเอาต์พุตดิบของโครงข่ายสำหรับหนึ่งอินพุต เป็นค่าในช่วง (0, 1)

        นี่คือคะแนนคล้ายความน่าจะเป็น ไม่ใช่คลาส หากต้องการเลเบล 0/1
        ให้ใช้เกณฑ์ตัดสินที่ 0.5 (ดูบล็อก __main__ ด้านล่าง)
        """
        return self.forward(x)[-1][0]


if __name__ == "__main__":
    # XOR: เอาต์พุตเป็น 1 เฉพาะเมื่ออินพุตแตกต่างกัน (ไม่สามารถแบ่งแยกได้เชิงเส้น)
    # สี่แถวนี้คือตารางความจริงสมบูรณ์ของฟังก์ชัน XOR
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 0]

    print("Training MLP (2-2-1) on XOR\n" + "=" * 50)
    # XOR มีที่ราบความสูญเสีย (loss plateaus): ด้วย learning_rate=2.0 และ seed นี้
    # โครงข่ายจะหลุดออกจากที่ราบได้ ลองใช้ seed=42 แล้วคอยดูว่ามันจะหยุดนิ่งที่ความแม่นยำ ~75%
    model = MLP(layer_sizes=[2, 2, 1], learning_rate=2.0, seed=0)
    model.fit(X, y, n_epochs=10000, log_every=1000)

    print("\nXOR truth table vs. prediction:")
    correct = 0  # นับจำนวนตัวอย่างที่จำแนกได้ถูกต้อง
    for xi, yi in zip(X, y):
        y_hat = model.predict(xi)          # เอาต์พุตดิบของโครงข่ายในช่วง (0, 1)
        y_class = 1 if y_hat >= 0.5 else 0  # แปลงคะแนนให้เป็นเลเบล 0/1
        correct += y_class == yi           # True นับเป็น 1, False นับเป็น 0
        print(f"  inputs {xi} -> target {yi} | output {y_hat:.4f} -> class {y_class}")
    print(f"\naccuracy: {correct / len(y):.0%}")

    print("\nLearned parameters:")
    # แสดง weights/biases สุดท้าย เพื่อให้นักศึกษาสามารถตรวจสอบสิ่งที่เรียนรู้ได้
    for l, (w, b) in enumerate(zip(model.weights, model.biases)):
        print(f"  layer {l + 1}: weights = {[list(map(lambda v: round(v, 3), row)) for row in w]}, "
              f"bias = {[round(v, 3) for v in b]}")
