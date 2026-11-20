"""mathdrill：零依赖的口算题生成器。"""

from .generator import describe_ops, generate, parse_ops
from .model import OPS, DrillError, Problem
from .render import render_page

__version__ = "0.1.0"

__all__ = [
    "OPS",
    "DrillError",
    "Problem",
    "describe_ops",
    "generate",
    "parse_ops",
    "render_page",
    "__version__",
]
