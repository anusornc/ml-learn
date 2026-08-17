"""Perceptron สร้างจากศูนย์ (ไม่ใช้ไลบรารีภายนอก).

Perceptron (Rosenblatt, 1958) คือหน่วยประมวลผลของโครงข่ายประสาทเทียมที่ก้าวหน้าพื้นฐานที่สุด:

    z = bias + w1*x1 + w2*x2 + ... + wn*xn     (ผลรวมถ่วงน้ำหนัก)
    y_hat = step(z)                             (ฟังก์ชันการกระตุ้น)

โดยใช้ฟังก์ชันการกระตุ้นแบบขั้นบันได (Heaviside step function):

    step(z) = 1  ถ้า z >= 0
              0  ถ้า z <  0

กฎการเรียนรู้ (ต่อหนึ่งตัวอย่างข้อมูล):

    error  = y - y_hat
    weights += learning_rate * error * x
    bias    += learning_rate * error

Perceptron แบบเดี่ยวสามารถเรียนรู้ได้เฉพาะปัญหาที่แบ่งแยกได้เชิงเส้น (linearly separable) เท่านั้น
(ฟังก์ชัน AND, OR ทำงานได้; XOR ทำงานไม่ได้)

การรันโปรแกรม:  python3 perceptron.py
"""


class Perceptron:
    """นิวรอน Perceptron แบบเดี่ยวพร้อมฟังก์ชันการกระตุ้นแบบขั้นบันได (step activation function)

    คิดว่าเป็นผู้ทำการตัดสินใจขนาดเล็ก: รับอินพุตหลายตัว คูณแต่ละตัวด้วยค่า "ความสำคัญ" (weight)
    บวกด้วยค่าเบี่ยงเบน (bias) และจะทำงาน (ส่งผลลัพธ์เป็น 1) ต่อเมื่อผลรวมข้ามผ่านศูนย์ไป
    การเทรน = ปรับแต่ง weights และ bias จนกระทั่งการตัดสินใจตรงกับเลเบล (labels) ที่เรากำหนดไว้
    """

    def __init__(self, n_features: int, learning_rate: float = 0.1, n_epochs: int = 100):
        """สร้าง perceptron และกำหนดพารามิเตอร์เริ่มต้น

        n_features:     จำนวนอินพุตที่นิวรอนได้รับ (เช่น 2 สำหรับประตูลอจิก)
        learning_rate:  ขนาดการปรับ weight ในแต่ละครั้ง ถ้าใหญ่เกินไป -> อาจปรับเกิน (overshoot)
                        และแกว่งไปมา; ถ้าเล็กเกินไป -> เรียนรู้ช้ามาก
        n_epochs:       จำนวนรอบสูงสุดในการวนลูปเรียนรู้ข้อมูลเทรนนิ่งทั้งหมด
        """
        # น้ำหนักหนึ่งค่าต่อหนึ่งอินพุต เริ่มต้นที่ 0.0 -- กฎของ perceptron รับประกันว่า
        # จะลู่เข้า (converge) สำหรับข้อมูลที่แบ่งแยกได้ไม่ว่าจะเริ่มจากค่าใด ดังนั้นเริ่มที่ศูนย์จึงใช้ได้
        self.weights = [0.0] * n_features
        # ค่า bias ช่วยให้เส้นแบ่งการตัดสินใจ (decision boundary) เลื่อนออกจากจุดกำเนิดได้
        self.bias = 0.0
        # ขนาดก้าว (step size) สำหรับการอัปเดต weight/bias ทุกครั้ง (ดู fit())
        self.learning_rate = learning_rate
        # ขีดจำกัดความปลอดภัย เพื่อให้การเทรนสิ้นสุดลงเสมอแม้ว่าข้อมูลจะไม่สามารถแบ่งแยกเชิงเส้นได้
        self.n_epochs = n_epochs

    @staticmethod
    def step_function(z: float) -> int:
        """ฟังก์ชันการกระตุ้น: แปลงผลรวมถ่วงน้ำหนักให้เป็นการตัดสินใจแบบ 0/1

        นี่คือกฎ "ทำงานหรือไม่ทำงาน" ถ้าอินพุตผลรวม z มีค่าอย่างน้อยเป็นศูนย์
        นิวรอนจะส่งออก 1 ไม่เช่นนั้นส่งออก 0 เป็นเกณฑ์การตัดสินใจแบบเด็ดขาด (hard threshold)
        ซึ่งทำให้ perceptron เป็นตัวจำแนกประเภท (classifier) ไม่ใช่ตัวถดถอย (regressor)
        """
        return 1 if z >= 0 else 0

    def _raw_output(self, x: list[float]) -> float:
        """คำนวณผลรวมถ่วงน้ำหนัก z = bias + sum(w_i * x_i) ก่อนผ่านฟังก์ชันการกระตุ้น

        นี่คือ "คะแนนหลักฐาน" ของนิวรอน อินพุตแต่ละตัว x_i ถูกปรับขนาดตามความสำคัญ
        (ค่าน้ำหนัก w_i) แล้วบวกเข้าด้วยกันทั้งหมด
        เราแยกส่วนนี้ออกจาก predict() เพื่อให้การทำงานของ step function ชัดเจน
        """
        z = self.bias  # เริ่มจากค่า bias แล้วบวกด้วยอินพุตถ่วงน้ำหนักแต่ละตัว
        for w, xi in zip(self.weights, x):
            z += w * xi
        return z

    def predict(self, x: list[float]) -> int:
        """คืนค่าคลาสที่ทำนาย (0 หรือ 1) สำหรับหนึ่งตัวอย่างอินพุต

        มีสองขั้นตอน: (1) รวมอินพุตถ่วงน้ำหนักเพื่อให้ได้ z จากนั้น (2) ส่ง z
        ผ่าน step function เพื่อให้ได้คำตอบเด็ดขาดเป็น 0/1
        """
        return self.step_function(self._raw_output(x))

    def fit(self, X: list[list[float]], y: list[int], verbose: bool = True) -> None:
        """เทรน perceptron บนตัวอย่างข้อมูล X พร้อมเลเบล y (แต่ละตัวเป็น 0 หรือ 1)

        กฎการเรียนรู้ของ perceptron ที่นำมาใช้กับตัวอย่างที่จำแนกผิดพลาดทุกตัว:
            error   = true label - prediction     (เป็นไปได้ทั้ง -1, 0, หรือ +1)
            weights += learning_rate * error * x  (สะกิด/ปรับไปในทิศทางของคำตอบที่ถูกต้อง)
            bias    += learning_rate * error

        หลักการ: ถ้าทำนายได้ 0 แต่คำตอบคือ 1 (error = +1) เราจะปรับดัน
        weights ไปในทิศทางของอินพุตนี้เพื่อให้ผลรวม z เพิ่มขึ้นในครั้งถัดไป
        ถ้าทำนายได้ 1 แต่คำตอบคือ 0 (error = -1) เราจะปรับดันในทิศทางตรงกันข้าม
        ตัวอย่างที่จำแนกถูกต้องแล้ว (error = 0) จะไม่มีการเปลี่ยนแปลงใดๆ

        หยุดการทำงานก่อนกำหนดทันทีเมื่อวนลูปครบรอบ (epoch) โดยไม่มีข้อผิดพลาดเลย (converged)
        """
        for epoch in range(1, self.n_epochs + 1):
            errors = 0  # จำนวนตัวอย่างที่ทายผิดใน epoch นี้
            for xi, yi in zip(X, y):
                y_hat = self.predict(xi)   # การทายปัจจุบันของนิวรอน
                error = yi - y_hat         # ข้อผิดพลาดแบบมีเครื่องหมาย: -1, 0, หรือ +1
                if error != 0:             # เรียนรู้เฉพาะจากข้อผิดพลาดเท่านั้น
                    errors += 1
                    for j in range(len(self.weights)):
                        # ปรับ weight แต่ละตัวเข้าหา (หรือออกจาก) อินพุตนี้
                        self.weights[j] += self.learning_rate * error * xi[j]
                    # ค่า bias เปรียบเสมือน weight ที่มีอินพุตเป็น 1 เสมอ
                    self.bias += self.learning_rate * error

            if verbose:
                print(f"epoch {epoch:>3} | errors: {errors} | "
                      f"weights: {[round(w, 3) for w in self.weights]} | "
                      f"bias: {round(self.bias, 3)}")
            if errors == 0:
                if verbose:
                    print("-> converged (no errors), stopping early.")
                break


def accuracy(model: Perceptron, X: list[list[float]], y: list[int]) -> float:
    """คืนค่าสัดส่วนของตัวอย่างข้อมูลที่โมเดลทำนายได้ถูกต้อง (0.0-1.0)

    นับว่าตัวอย่างถูกต้องเมื่อคลาสที่ทำนายตรงกับเลเบลจริงพอดี
    จากนั้นหารด้วยจำนวนตัวอย่างทั้งหมด 1.0 = สมบูรณ์แบบ
    """
    correct = sum(1 for xi, yi in zip(X, y) if model.predict(xi) == yi)
    return correct / len(y)


def demo(name: str, X: list[list[float]], y: list[int], verbose: bool = True) -> None:
    """เทรน perceptron ตัวใหม่บนชุดข้อมูลหนึ่งชุดและพิมพ์ผลลัพธ์การทำงาน

    ฟังก์ชันนี้เป็นฟังก์ชันช่วยเหลือเพื่อให้บล็อก __main__ ด้านล่างสั้นและอ่านง่าย
    โดยจะสร้างโมเดลใหม่ (เพื่อให้แต่ละเกตเริ่มจากจุดเริ่มต้นใหม่) แล้วเทรนโมเดล
    จากนั้นแสดงตารางความจริงเทียบกันข้างๆ กับผลการทำนายของโมเดล
    """
    print(f"\n{'=' * 60}\nTraining on {name} gate\n{'=' * 60}")
    # n_features อ่านจากข้อมูล: ความยาวของแต่ละตัวอย่าง = จำนวนอินพุต
    model = Perceptron(n_features=len(X[0]), learning_rate=0.1, n_epochs=100)
    model.fit(X, y, verbose=verbose)

    print(f"\n{name} truth table vs. prediction:")
    for xi, yi in zip(X, y):
        print(f"  inputs {xi} -> target {yi}, predicted {model.predict(xi)}")
    print(f"accuracy: {accuracy(model, X, y):.0%}")
    print(f"learned weights: {model.weights}, bias: {model.bias}")


if __name__ == "__main__":
    # ประตูลอจิกแต่ละตัวถูกกำหนดโดยคู่อินพุตที่เป็นไปได้ 4 คู่และเอาต์พุตที่คาดหวัง
    # นี่คือโจทย์ตัวอย่างคลาสสิกสำหรับ perceptron

    # เกต AND: เอาต์พุตเป็น 1 เฉพาะเมื่ออินพุตทั้งสองเป็น 1 (แบ่งแยกได้เชิงเส้น)
    X_and = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_and = [0, 0, 0, 1]
    demo("AND", X_and, y_and)

    # เกต OR: เอาต์พุตเป็น 1 เมื่อมีอินพุตอย่างน้อยหนึ่งตัวเป็น 1 (แบ่งแยกได้เชิงเส้น)
    X_or = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_or = [0, 1, 1, 1]
    demo("OR", X_or, y_or)

    # เกต XOR: เอาต์พุตเป็น 1 เฉพาะเมื่ออินพุตแตกต่างกัน ปัญหานี้ไม่สามารถแบ่งแยกได้เชิงเส้น
    # ดังนั้น perceptron เดียวจึงไม่สามารถเรียนรู้ได้ เรายังคงรันเพื่อสาธิตให้เห็นถึง
    # ข้อจำกัดพื้นฐานนี้ ซึ่งเป็นแรงจูงใจในการสร้างโครงข่ายหลายชั้น (multi-layer networks)
    # และอัลกอริทึม backpropagation (ดู mlp_xor.py)
    X_xor = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_xor = [0, 1, 1, 0]
    demo("XOR (expected to fail)", X_xor, y_xor, verbose=False)
