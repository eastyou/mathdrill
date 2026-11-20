"""测试命令行入口的退出码与输出文件。"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from mathdrill.cli import main


def run_cli(args: list) -> tuple:
    stdout, stderr = io.StringIO(), io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(args)
    return code, stdout.getvalue(), stderr.getvalue()


class CliTests(unittest.TestCase):
    def test_generates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "drill.html"
            code, stdout, _ = run_cli(
                ["--ops", "add,sub", "--count", "10", "--max", "20", "-o", str(output)]
            )
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            content = output.read_text(encoding="utf-8")
            self.assertEqual(content.count('class="item"'), 10)
            self.assertIn("参考答案", content)
            self.assertIn("已生成", stdout)

    def test_no_answers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "drill.html"
            code, _, _ = run_cli(["--count", "5", "--no-answers", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertNotIn("参考答案", output.read_text(encoding="utf-8"))

    def test_invalid_ops(self) -> None:
        code, _, stderr = run_cli(["--ops", "pow", "-o", "/tmp/x.html"])
        self.assertEqual(code, 2)
        self.assertIn("不支持的运算", stderr)

    def test_invalid_columns(self) -> None:
        code, _, stderr = run_cli(["--columns", "9", "-o", "/tmp/x.html"])
        self.assertEqual(code, 2)
        self.assertIn("列数", stderr)

    def test_invalid_count(self) -> None:
        code, _, _ = run_cli(["--count", "0", "-o", "/tmp/x.html"])
        self.assertEqual(code, 2)

    def test_write_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, stderr = run_cli(["--count", "3", "-o", tmp])
            self.assertEqual(code, 1)
            self.assertIn("写入文件失败", stderr)

    def test_seed_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "a.html", Path(tmp) / "b.html"
            run_cli(["--count", "8", "--seed", "42", "-o", str(first)])
            run_cli(["--count", "8", "--seed", "42", "-o", str(second)])
            self.assertEqual(
                first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
