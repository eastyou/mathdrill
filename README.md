# mathdrill

[![CI](https://github.com/eastyou/mathdrill/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/mathdrill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

给小学老师和家长用的口算题生成器：选好题型、数值范围和题目数量，一条命令生成一页 A4 练习纸，附参考答案。**零依赖，不联网，单文件 HTML，直接打印。**

题目保证不重复，加法和乘法自动把 `3 + 5` 与 `5 + 3` 视为同一题，不会把同一道题换个顺序再出一次。

## 特性

- **四种运算**：加、减、乘、除，可任意组合，按顺序轮流出题
- **难度可控**：`--max` 控制加减法数值上限，乘除法固定使用 9 以内口诀表
- **减法不出负数**：被减数始终大于减数
- **除法保证整除**：先定商和除数，再反推被除数
- **自动去重**：生成时按题目指纹去重，可选题目不足会明确报错
- **可复现**：`--seed` 固定随机种子，同一份练习可以重新生成
- **答案页**：默认附参考答案，可用 `--no-answers` 关闭
- **A4 打印**：2~4 列排版，题卡不跨页，页眉留姓名、日期、用时、得分
- **41 个单元测试**：覆盖生成规则、去重、参数校验与 HTML 输出

## 安装

```bash
pip install mathdrill
```

也可以直接下载源码，在项目目录里运行：

```bash
python -m mathdrill --help
```

## 用法

生成 40 道 20 以内的加减法：

```bash
mathdrill --ops add,sub --max 20 --count 40 -o 口算练习.html
```

生成 60 道混合运算，两列排版的乘法口诀练习：

```bash
mathdrill --ops mul --max 9 --count 60 --columns 2 --title "乘法口诀练习" -o 乘法.html
```

固定种子，方便家长和老师生成两份相同的卷子：

```bash
mathdrill --ops add,sub,mul,div --count 50 --seed 2026 -o 综合练习.html
```

不要答案页，方便直接发给学生：

```bash
mathdrill --ops add,sub --count 30 --no-answers -o 学生版.html
```

## 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--ops` | `add,sub` | 运算类型，逗号分隔，支持 `add` `sub` `mul` `div`，也可写 `+ - × ÷` |
| `--max` | `20` | 加减法数值上限，至少为 2 |
| `--count` | `40` | 题目数量，1~500 |
| `--columns` | `3` | 每行题数，2~4 |
| `--title` | `口算练习` | 练习纸标题 |
| `--seed` | 无 | 随机种子，用于复现 |
| `--no-answers` | 关闭 | 不生成参考答案页 |
| `-o, --output` | `口算练习.html` | 输出文件路径 |

## 出题规则

| 题型 | 取值范围 | 说明 |
| --- | --- | --- |
| 加法 | 两个加数都在 `1 ~ max` | 和可能超过 `max` |
| 减法 | 被减数 `2 ~ max`，减数小于被减数 | 结果至少为 1，不出现负数 |
| 乘法 | 两个因数都在 `2 ~ min(9, max)` | 对应乘法口诀表 |
| 除法 | 除数与商都在 `2 ~ min(9, max)` | 被除数 = 除数 × 商，保证整除 |

如果可选题目不够，例如只要 9 以内的乘法却要求 100 道不重复的题，程序会提示增大 `--max` 或减少 `--count`，不会悄悄出重复题。

## 输出

`mathdrill` 生成一个自包含的 HTML 文件：

- 练习页：页眉含姓名、日期、用时、得分，下方是带序号的题卡
- 答案页：自动另起一页，四列排布完整算式

用浏览器打开后按 `Ctrl/Cmd + P`，纸张选 A4 纵向即可打印。打印时建议开启「背景图形」，题卡边框才会显示。

## 开发

```bash
python -m unittest discover -s tests -v
```

## License

[MIT](LICENSE) © 2026 eastyou
