"""口算题的数据结构与异常定义。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

OPS: Tuple[str, ...] = ("add", "sub", "mul", "div")

OP_NAMES = {
    "add": "加法",
    "sub": "减法",
    "mul": "乘法",
    "div": "除法",
}

OP_SYMBOLS = {
    "add": "+",
    "sub": "-",
    "mul": "×",
    "div": "÷",
}


class DrillError(ValueError):
    """题目参数不合法，或无法生成足够的不重复题目。"""


@dataclass(frozen=True)
class Problem:
    """一道口算题。

    ``answer`` 由生成器保证正确；构造时只校验运算符是否受支持。
    """

    left: int
    right: int
    op: str
    answer: int

    def __post_init__(self) -> None:
        if self.op not in OPS:
            raise DrillError("不支持的运算类型: %r" % (self.op,))

    @property
    def symbol(self) -> str:
        return OP_SYMBOLS[self.op]

    @property
    def text(self) -> str:
        """题面，例如 ``3 + 5 =``。"""
        return "%d %s %d =" % (self.left, self.symbol, self.right)

    @property
    def answer_text(self) -> str:
        """完整算式，例如 ``3 + 5 = 8``。"""
        return "%s %d" % (self.text, self.answer)

    @property
    def key(self) -> Tuple[str, int, int]:
        """去重键；加法和乘法视为可交换，3+5 与 5+3 算同一题。"""
        if self.op in ("add", "mul"):
            first, second = sorted((self.left, self.right))
            return (self.op, first, second)
        return (self.op, self.left, self.right)
