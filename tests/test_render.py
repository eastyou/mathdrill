"""测试练习纸 HTML 输出。"""

from __future__ import annotations

import unittest

from mathdrill.generator import generate
from mathdrill.model import DrillError
from mathdrill.render import render_page


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.problems = generate(("add",), count=12, max_value=20, seed=11)

    def test_contains_every_item(self) -> None:
        page = render_page(self.problems, title="一年级口算")
        self.assertEqual(page.count('class="item"'), 12)
        self.assertIn("一年级口算", page)
        self.assertIn("参考答案", page)

    def test_answer_page_can_be_disabled(self) -> None:
        page = render_page(self.problems, show_answers=False)
        self.assertNotIn("参考答案", page)

    def test_columns_applied(self) -> None:
        page = render_page(self.problems, columns=4)
        self.assertIn("--cols: 4", page)

    def test_title_is_escaped(self) -> None:
        page = render_page(self.problems, title="<script>alert(1)</script>")
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_answers_contain_results(self) -> None:
        page = render_page(self.problems)
        for problem in self.problems[:3]:
            self.assertIn(problem.answer_text, page)

    def test_empty_problems_rejected(self) -> None:
        with self.assertRaises(DrillError):
            render_page([])

    def test_columns_out_of_range(self) -> None:
        for columns in (1, 5):
            with self.assertRaises(DrillError):
                render_page(self.problems, columns=columns)

    def test_blank_title_rejected(self) -> None:
        with self.assertRaises(DrillError):
            render_page(self.problems, title="   ")

    def test_total_count_rendered(self) -> None:
        page = render_page(self.problems)
        self.assertIn("共 12 题", page)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
