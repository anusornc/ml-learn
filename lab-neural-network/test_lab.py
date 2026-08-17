"""Lock the teaching contracts used by the 1-epoch worksheet and lecture."""

from __future__ import annotations

from perceptron import Perceptron, accuracy
from mlp_xor import MLP, sigmoid

AND_X = [[0, 0], [0, 1], [1, 0], [1, 1]]
AND_Y = [0, 0, 0, 1]
XOR_X = [[0, 0], [0, 1], [1, 0], [1, 1]]
XOR_Y = [0, 1, 1, 0]


def test_step_includes_zero() -> None:
    assert Perceptron.step_function(0.0) == 1
    assert Perceptron.step_function(-1e-9) == 0


def test_and_converges_from_zero_weights() -> None:
    model = Perceptron(n_features=2, learning_rate=0.1, n_epochs=20)
    model.fit(AND_X, AND_Y, verbose=False)
    assert accuracy(model, AND_X, AND_Y) == 1.0


def test_and_first_epoch_matches_worksheet() -> None:
    model = Perceptron(n_features=2, learning_rate=0.1, n_epochs=1)
    model.fit(AND_X, AND_Y, verbose=False)
    assert model.weights == [0.1, 0.1]
    assert model.bias == 0.0


def test_perceptron_cannot_learn_xor() -> None:
    model = Perceptron(n_features=2, learning_rate=0.1, n_epochs=100)
    model.fit(XOR_X, XOR_Y, verbose=False)
    assert accuracy(model, XOR_X, XOR_Y) < 1.0


def test_mlp_seed_zero_solves_xor() -> None:
    model = MLP(layer_sizes=[2, 2, 1], learning_rate=2.0, seed=0)
    model.fit(XOR_X, XOR_Y, n_epochs=10000, log_every=10000)
    predicted = [1 if model.predict(x) >= 0.5 else 0 for x in XOR_X]
    assert predicted == XOR_Y


def test_mlp_seed_42_plateaus() -> None:
    model = MLP(layer_sizes=[2, 2, 1], learning_rate=2.0, seed=42)
    model.fit(XOR_X, XOR_Y, n_epochs=10000, log_every=10000)
    predicted = [1 if model.predict(x) >= 0.5 else 0 for x in XOR_X]
    assert predicted != XOR_Y


def test_worksheet_forward_numbers() -> None:
    a_h1 = sigmoid(0.5)
    a_h2 = sigmoid(-0.5)
    a_out = sigmoid(0.5 * a_h1 + 0.5 * a_h2)
    assert abs(a_h1 - 0.622459) < 1e-5
    assert abs(a_h2 - 0.377541) < 1e-5
    assert abs(a_out - 0.622459) < 1e-5


if __name__ == "__main__":
    test_step_includes_zero()
    test_and_converges_from_zero_weights()
    test_and_first_epoch_matches_worksheet()
    test_perceptron_cannot_learn_xor()
    test_mlp_seed_zero_solves_xor()
    test_mlp_seed_42_plateaus()
    test_worksheet_forward_numbers()
    print("all teaching contracts passed")
