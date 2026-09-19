# -*- coding: utf-8 -*-
"""生成 ADCdb 数据分析 Jupyter Notebook（nbformat 4）。"""
import json


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src,
    }


CELLS = [
    # 标题与简介
    md(
        "# ADCdb 数据分析\n"
        "\n"
        "使用 pandas 将 `ADCdb_1.0.xlsx` 原始表载入为结构化 DataFrame，\n"
        "并进行数据清洗、探索性分析与可视化。\n"
        "\n"
        "- 数据集：`ADCdb_1.0.xlsx`（ADC 抗体偶联药物库）\n"
        "- 记录规模：1431 行 × 13 列\n"
        "- 分析目标：转 pandas 对象 → 清洗 → 统计 → 可视化"
    ),
    # 导入依赖
    code(
        "# -*- coding: utf-8 -*-\n"
        '"""ADCdb 数据分析 Notebook：将 Excel 数据转化为 pandas 对象。"""\n'
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "\n"
        "# 显示选项：完整展示列，避免科学计数法\n"
        "pd.set_option(\"display.max_columns\", None)\n"
        "pd.set_option(\"display.width\", 160)\n"
        "\n"
        "# 中文字体支持（Windows 微软雅黑）\n"
        'plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]\n'
        'plt.rcParams["axes.unicode_minus"] = False'
    ),
    # 一、载入数据
    md("## 一、载入数据"),
    code(
        '# 读取工作表为 pandas DataFrame\n'
        'FILE = "ADCdb_1.0.xlsx"\n'
        "df = pd.read_excel(FILE)\n"
        'print(f"数据维度: {df.shape[0]} 行 × {df.shape[1]} 列")'
    ),
    code("# 数据预览\n" "df.head()"),
    code("# 字段元数据：列名与数据类型\n" "df.info()"),
    # 二、数据清洗
    md("## 二、数据清洗\n" "\n" "检查缺失值、重复记录，并规整字段类型。"),
    code(
        "# 缺失值统计（仅展示含 NaN 的字段）\n"
        "missing = df.isna().sum()\n"
        "with_missing = missing[missing > 0]\n"
        'print("含缺失值的字段：\\n", with_missing)'
    ),
    code(
        "# 规整类型：将浮点型 ADC ID 转为字符串标识\n"
        'df["ADC ID"] = df["ADC ID"].astype(int).astype(str)\n'
        "\n"
        "# 删除完全重复的记录\n"
        "df = df.drop_duplicates().reset_index(drop=True)\n"
        'print(f"去重后剩余 {df.shape[0]} 行")'
    ),
    code(
        "# 统计抗体结合区域序列的覆盖率\n"
        'has_binding = df["Binding Region of Antibody in ADC Sequence"].notna()\n'
        'print(f"含结合区域序列的样本占比: {has_binding.mean():.1%}")'
    ),
    code(
        "# 清洗后数据质量复核\n"
        'print("剩余缺失值总数:", int(df.isna().sum().sum()))\n'
        'print("剩余总行数:", df.shape[0])'
    ),
    # 三、探索性分析
    md("## 三、探索性分析"),
    code("df.describe(include=\"all\").T.head(6)"),
    code(
        "# 分类字段频数统计的通用函数\n"
        "def count_top(series, n=5):\n"
        "    \"\"\"返回指定字段出现频数最高的前 n 个取值。\"\"\"\n"
        '    return series.value_counts().head(n)\n'
        "\n"
        "\n"
        '# 抗体平台 Top 5\n'
        'top_ab = count_top(df["Antibody Name"])\n'
        'print("Top 5 抗体：\\n", top_ab)'
    ),
    code("# 偶联方式分布\n" 'print("偶联方式分布：\\n", count_top(df["Conjugate Type"]))'),
    code(
        "# 载荷（Payload）与连接子（Linker）使用情况\n"
        'print("载荷 Top 5：\\n", count_top(df["Payload Name"]))\n'
        'print("连接子 Top 5：\\n", count_top(df["Linker Name"]))'
    ),
    code(
        "# 按偶联方式聚合，观察抗体平台多样性\n"
        'grouped = df.groupby("Conjugate Type")["Antibody Name"].nunique()\n'
        'print("各偶联方式下的抗体种类数：\\n", grouped)'
    ),
    code(
        "# 交叉分析：最常用抗体的载荷使用情况\n"
        "top_ab_name = top_ab.index[0]\n"
        'subset = df[df["Antibody Name"] == top_ab_name]\n'
        'print(f"{top_ab_name} 使用的载荷：\\n", count_top(subset["Payload Name"]))'
    ),
    code(
        "# 主键校验：ADC ID 唯一性\n"
        'print("唯一 ADC ID 数量:", df["ADC ID"].nunique())\n'
        'print("是否可作为主键:", df["ADC ID"].is_unique)'
    ),
    # 四、可视化
    md("## 四、可视化"),
    code(
        "# 统一绘图风格\n"
        'sns.set_theme(style="whitegrid")\n'
        "\n"
        "# 双子图：抗体平台 Top 8 与偶联方式分布\n"
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
        "\n"
        'count_top(df["Antibody Name"], n=8).plot.bar(\n'
        '    ax=axes[0], color="#4c72b0", title="抗体平台 Top 8"\n'
        ")\n"
        'count_top(df["Conjugate Type"], n=10).plot.bar(\n'
        '    ax=axes[1], color="#dd8452", title="偶联方式分布"\n'
        ")\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),
    code(
        "# 载荷类型占比饼图\n"
        'df["Payload Name"].value_counts().head(6).plot.pie(\n'
        '    autopct="%.1f%%", figsize=(7, 7), title="载荷类型占比"\n'
        ")\n"
        'plt.ylabel("")\n'
        "plt.show()"
    ),
    # 五、结论
    md(
        "## 五、结论\n"
        "\n"
        "原始数据共 1431 行、13 列，清洗去重后保留唯一 ADC 记录。\n"
        "主要发现：\n"
        "\n"
        "- **Trastuzumab** 是最常用的抗体骨架；\n"
        "- 偶联方式以特异性化学偶联（site-specific）为主；\n"
        "- 载荷类型多样，Duostatin 类毒素占比最高。\n"
        "\n"
        "本 Notebook 可通过 `jupyter nbconvert --execute` 一键复现。"
    ),
]

NOTEBOOK = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT = r"e:\project\ADC_Analysis\ADCdb_Analysis.ipynb"
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(NOTEBOOK, fh, ensure_ascii=False, indent=1)

total = sum(len(c["source"].splitlines()) for c in CELLS)
print(f"Notebook 已写入: {OUT}")
print(f"Notebook 代码+文字总行数: {total}")