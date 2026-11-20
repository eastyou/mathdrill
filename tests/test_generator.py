"""测试题目生成、去重与参数校验。"""

from __future__ import annotations

import unittest

from mathdrill.generator import describe_ops, generate, parse_ops
from mathdrill.model import DrillError


class ParseOpsTests(unittest.TestCase):
    def test_parses_names(self) -> None:
        self.assertEqual(parse_ops("add, sub"), ("add", "sub"))

    def test_parses_symbols(self) -> None:
        self.assertEqual(parse_ops("+,-,×,÷"), ("add", "sub", "mul", "div"))

    def test_removes_duplicates(self) -> None:
        self.assertEqual(parse_ops("add,+"), ("add",))

    def test_empty_rejected(self) -> None:
        with self.assertRaises(DrillError):
            parse_ops("  ")

    def test_unknown_rejected(self) -> None:
        with self.assertRaises(DrillError):
            parse_ops("add,pow")


class GenerateTests(unittest.TestCase):
    def test_count_and_unique(self) -> None:
        problems = generate(("add", "sub", "mul", "div"), count=60, max_value=20, seed=1)
        self.assertEqual(len(problems), 60)
        keys = {item.key for item in problems}
        self.assertEqual(len(keys), 60)

    def test_ops_are_balanced(self) -> None:
        problems = generate(("add", "sub"), count=9, max_value=50, seed=2)
        self.assertEqual(sum(1 for p in problems if p.op == "add"), 5)
        self.assertEqual(sum(1 for p in problems if p.op == "sub"), 4)

    def test_addition_bounds(self) -> None:
        for problem in generate(("add",), count=40, max_value=20, seed=3):
            self.assertGreaterEqual(problem.left, 1)
            self.assertLessEqual(problem.left, 20)
            self.assertGreaterEqual(problem.right, 1)
            self.assertLessEqual(problem.right, 20)
            self.assertEqual(problem.answer, problem.left + problem.right)

    def test_subtraction_never_negative(self) -> None:
        for problem in generate(("sub",), count=40, max_value=20, seed=4):
            self.assertGreater(problem.left, problem.right)
            self.assertEqual(problem.answer, problem.left - problem.right)
            self.assertGreaterEqual(problem.answer, 1)

    def test_multiplication_uses_table(self) -> None:
        for problem in generate(("mul",), count=30, max_value=100, seed=5):
            self.assertTrue(2 <= problem.left <= 9)
            self.assertTrue(2 <= problem.right <= 9)
            self.assertEqual(problem.answer, problem.left * problem.right)

    def test_division_is_exact(self) -> None:
        for problem in generate(("div",), count=30, max_value=100, seed=6):
            self.assertEqual(problem.left % problem.right, 0)
            self.assertEqual(problem.answer, problem.left // problem.right)

    def test_seed_is_reproducible(self) -> None:
        first = generate(("add", "mul"), count=20, max_value=30, seed=7)
        second = generate(("add", "mul"), count=20, max_value=30, seed=7)
        self.assertEqual([p.key for p in first], [p.key for p in second])

    def test_too_few_combinations_raise(self) -> None:
        with self.assertRaises(DrillError):
            generate(("mul",), count=50, max_value=2, seed=8)


class ValidationTests(unittest.TestCase):
    def test_zero_count(self) -> None:
        with self.assertRaises(DrillError):
            generate(("add",), count=0)

    def test_huge_count(self) -> None:
        with self.assertRaises(DrillError):
            generate(("add",), count=501)

    def test_tiny_max(self) -> None:
        with self.assertRaises(DrillError):
            generate(("add",), count=5, max_value=1)

    def test_empty_ops(self) -> None:
        with self.assertRaises(DrillError):
            generate((), count=5)

    def test_unknown_op(self) -> None:
        with self.assertRaises(DrillError):
            generate(("pow",), count=5)

    def test_describe_ops(self) -> None:
        self.assertEqual(describe_ops(("add", "sub")), "加、减法")
        self.assertEqual(describe_ops(("mul",)), "乘法")
        self.assertEqual(describe_ops(()), "")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
