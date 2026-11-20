"""把口算题渲染成一页可打印的 A4 练习纸与答案页。"""

from __future__ import annotations

import html
from typing import Sequence

from .model import DrillError, Problem

PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 18px 22px 24px;
    background: #f8fafc;
    color: #0f172a;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  }
  header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 10px;
    margin-bottom: 6px;
  }
  h1 { font-size: 22px; margin: 0; letter-spacing: 1px; }
  .meta { color: #64748b; font-size: 12px; margin-top: 4px; }
  .fields {
    display: flex;
    gap: 18px;
    color: #334155;
    font-size: 12px;
    white-space: nowrap;
  }
  .fields span { border-bottom: 1px solid #94a3b8; padding: 0 6px 2px; }
  .hint {
    color: #64748b;
    font-size: 11px;
    margin: 8px 0 12px;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
    gap: 8px 14px;
  }
  .item {
    display: flex;
    align-items: baseline;
    gap: 6px;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background: #fff;
    font-size: 15px;
    break-inside: avoid;
  }
  .no {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    flex: none;
    border-radius: 50%;
    background: #e2e8f0;
    color: #475569;
    font-size: 11px;
  }
  .expr { font-family: "SFMono-Regular", Consolas, monospace; letter-spacing: 0.5px; }
  .blank {
    flex: 1;
    min-width: 34px;
    border-bottom: 1px solid #94a3b8;
    transform: translateY(-3px);
  }
  .answers { break-before: page; }
  .answers h2 {
    font-size: 16px;
    margin: 0 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #cbd5e1;
  }
  .answer-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 6px 14px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    color: #334155;
  }
  footer {
    margin-top: 16px;
    color: #94a3b8;
    font-size: 11px;
    display: flex;
    justify-content: space-between;
  }
  @page { size: A4 portrait; margin: 10mm; }
  @media print {
    body { background: #fff; padding: 0; }
    .item { border-color: #94a3b8; }
    * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
</style>
</head>
<body>
<header>
  <div>
    <h1>__TITLE__</h1>
    <div class="meta">__META__</div>
  </div>
  <div class="fields">
    <div>姓名<span>&nbsp;</span></div>
    <div>日期<span>&nbsp;</span></div>
    <div>用时<span>&nbsp;</span></div>
    <div>得分<span>&nbsp;</span></div>
  </div>
</header>
<div class="hint">请在横线上写出得数，书写工整，做完后检查一遍。</div>
<div class="grid" style="--cols: __COLS__">
__ITEMS__
</div>
__ANSWERS__
<footer>
  <span>mathdrill · 共 __COUNT__ 题</span>
  <span>A4 纵向打印，建议缩放 100%</span>
</footer>
</body>
</html>
"""

ANSWER_TEMPLATE = """<section class="answers">
  <h2>参考答案</h2>
  <div class="answer-grid">
__ITEMS__
  </div>
</section>"""


def render_page(
    problems: Sequence[Problem],
    title: str = "口算练习",
    columns: int = 3,
    show_answers: bool = True,
    meta: str = "",
) -> str:
    """生成练习纸 HTML；参数越界或题目为空时抛出 ``DrillError``。"""
    if not title.strip():
        raise DrillError("标题不能为空")
    if not 2 <= columns <= 4:
        raise DrillError("列数必须在 2 到 4 之间")
    if not problems:
        raise DrillError("至少需要一道题才能生成练习纸")

    items = []
    for index, problem in enumerate(problems, start=1):
        items.append(
            '<div class="item"><span class="no">%d</span>'
            '<span class="expr">%s</span><span class="blank"></span></div>'
            % (index, html.escape(problem.text))
        )

    answers = ""
    if show_answers:
        answer_items = [
            "<div>%d. %s</div>" % (index, html.escape(problem.answer_text))
            for index, problem in enumerate(problems, start=1)
        ]
        answers = ANSWER_TEMPLATE.replace("__ITEMS__", "\n".join(answer_items))

    replacements = {
        "__TITLE__": html.escape(title.strip()),
        "__META__": html.escape(meta.strip()),
        "__COLS__": str(columns),
        "__ITEMS__": "\n".join(items),
        "__ANSWERS__": answers,
        "__COUNT__": str(len(problems)),
    }
    page = PAGE_TEMPLATE
    for key, value in replacements.items():
        page = page.replace(key, value)
    return page
