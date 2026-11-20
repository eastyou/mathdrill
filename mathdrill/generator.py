"""口算题生成：按题型、数值范围和数量生成不重复的题目。"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Set, Tuple

from .model import OPS, DrillError, Problem

# 每个题型最多尝试的生成次数，防止参数过窄时死循环
MAX_ATTEMPTS_PER_PROBLEM = 200

OP_ALIASES: Dict[str, str] = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "x": "mul",
    "×": "mul",
    "/": "div",
    "÷": "div",
    "加": "add",
    "减": "sub",
    "乘": "mul",
    "除": "div",
}


def parse_ops(value: str) -> Tuple[str, ...]:
    """把 ``add,sub`` 或 ``+,-`` 解析成规范的题型元组，并去除重复。"""
    if not isinstance(value, str) or not value.strip():
        raise DrillError("--ops 不能为空，可用 add, sub, mul, div")

    result: List[str] = []
    for raw in value.split(","):
        token = raw.strip().lower()
        if not token:
            continue
        op = OP_ALIASES.get(token, token)
        if op not in OPS:
            raise DrillError(
                "不支持的运算 %r，可用 add, sub, mul, div（也可写 + - × ÷）"
                % raw.strip()
            )
        if op not in result:
            result.append(op)
    if not result:
        raise DrillError("--ops 至少要包含一种运算")
    return tuple(result)


def _factor_limit(max_value: int) -> int:
    """乘法与除法使用 9 以内的口诀表范围，避免出现两位数乘法。"""
    return max(2, min(9, max_value))


def _make_problem(op: str, max_value: int, rng: random.Random) -> Problem:
    if op == "add":
        left = rng.randint(1, max_value)
        right = rng.randint(1, max_value)
        return Problem(left, right, op, left + right)

    if op == "sub":
        left = rng.randint(2, max_value)
        right = rng.randint(1, left - 1)
        return Problem(left, right, op, left - right)

    limit = _factor_limit(max_value)
    if op == "mul":
        left = rng.randint(2, limit)
        right = rng.randint(2, limit)
        return Problem(left, right, op, left * right)

    # 除法保证整除：先定商和除数，再反推被除数
    divisor = rng.randint(2, limit)
    quotient = rng.randint(2, limit)
    return Problem(divisor * quotient, divisor, op, quotient)


def generate(
    ops: Sequence[str] = ("add", "sub"),
    count: int = 40,
    max_value: int = 20,
    seed: Optional[int] = None,
) -> List[Problem]:
    """生成 ``count`` 道不重复的口算题。

    :raises DrillError: 题型为空、数量或范围越界、可选题目不足。
    """
    if not ops:
        raise DrillError("至少要选择一种运算")
    for op in ops:
        if op not in OPS:
            raise DrillError("不支持的运算类型: %r" % (op,))
    if not isinstance(count, int) or count < 1:
        raise DrillError("题目数量必须是正整数")
    if count > 500:
        raise DrillError("题目数量不能超过 500，建议分成多页练习")
    if not isinstance(max_value, int) or max_value < 2:
        raise DrillError("数值范围至少为 2")

    rng = random.Random(seed)
    problems: List[Problem] = []
    seen: Set[Tuple[str, int, int]] = set()
    attempts: Dict[str, int] = {op: 0 for op in ops}

    while len(problems) < count:
        op = ops[len(problems) % len(ops)]
        attempts[op] += 1
        if attempts[op] > count * MAX_ATTEMPTS_PER_PROBLEM:
            raise DrillError(
                "可选题目不足，无法生成 %d 道不重复的题，请增大--max或减少--count"
                % count
            )
        problem = _make_problem(op, max_value, rng)
        if problem.key in seen:
            continue
        seen.add(problem.key)
        problems.append(problem)

    return problems


def describe_ops(ops: Sequence[str]) -> str:
    """把题型元组描述成中文，例如「加、减法」。"""
    names = {"add": "加", "sub": "减", "mul": "乘", "div": "除"}
    if not ops:
        return ""
    return "、".join(names[op] for op in ops) + "法"
