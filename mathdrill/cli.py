"""命令行入口：生成可打印的口算练习纸。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .generator import describe_ops, generate, parse_ops
from .model import DrillError
from .render import render_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mathdrill",
        description="口算题生成器：按题型和数值范围出题，输出可打印的 A4 练习纸",
    )
    parser.add_argument("--version", action="version", version="mathdrill 0.1.0")
    parser.add_argument(
        "--ops",
        default="add,sub",
        help="题型，逗号分隔：add, sub, mul, div，默认 add,sub",
    )
    parser.add_argument(
        "--max", type=int, default=20, help="加减法的数值上限，默认 20"
    )
    parser.add_argument("--count", type=int, default=40, help="题目数量，默认 40")
    parser.add_argument(
        "--columns", type=int, default=3, help="每行题数，2~4，默认 3"
    )
    parser.add_argument("--title", default="口算练习", help="练习纸标题")
    parser.add_argument("--seed", type=int, default=None, help="随机种子，便于复现")
    parser.add_argument(
        "--no-answers", action="store_true", help="不生成参考答案页"
    )
    parser.add_argument(
        "-o", "--output", default="口算练习.html", help="输出 HTML 路径"
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        ops = parse_ops(args.ops)
        problems = generate(
            ops=ops, count=args.count, max_value=args.max, seed=args.seed
        )
        meta = "%s · %d 以内 · 共 %d 题" % (
            describe_ops(ops),
            args.max,
            len(problems),
        )
        page = render_page(
            problems,
            title=args.title,
            columns=args.columns,
            show_answers=not args.no_answers,
            meta=meta,
        )
    except DrillError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    try:
        Path(args.output).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1

    print(
        "已生成 %s：%d 题（%s，%d 以内）"
        % (args.output, len(problems), describe_ops(ops), args.max)
    )
    if not args.no_answers:
        print("答案页已附在练习纸之后")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
