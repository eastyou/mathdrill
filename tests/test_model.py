"""测试数据结构与去重键。"""

from __future__ import annotations

import unittest

from mathdrill.model import DrillError, Problem


class ProblemTests(unittest.TestCase):
    def test_text_uses_symbol(self) -> None:
        problem = Problem(3, 5, "add", 8)
        self.assertEqual(problem.text, "3 + 5 =")
        self.assertEqual(problem.answer_text, "3 + 5 = 8")

    def test_mul_symbol_is_fullwidth(self) -> None:
        problem = Problem(6, 7, "mul", 42)
        self.assertEqual(problem.symbol, "×")
        self.assertEqual(problem.text, "6 × 7 =")

    def test_add_key_is_commutative(self) -> None:
        first = Problem(3, 5, "add", 8)
        second = Problem(5, 3, "add", 8)
        self.assertEqual(first.key, second.key)

    def test_sub_key_is_not_commutative(self) -> None:
        first = Problem(9, 4, "sub", 5)
        second = Problem(4, 9, "sub", -5)
        self.assertNotEqual(first.key, second.key)

    def test_unknown_operator_rejected(self) -> None:
        with self.assertRaises(DrillError):
            Problem(1, 2, "pow", 3)

    def test_problem_is_immutable(self) -> None:
        problem = Problem(1, 2, "add", 3)
        with self.assertRaises(AttributeError):
            problem.left = 9  # type: ignore[misc]


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
