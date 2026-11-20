"""支持 ``python -m mathdrill``。"""

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
