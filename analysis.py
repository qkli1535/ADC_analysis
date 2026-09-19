"""ADCdb 数据分析：把 Excel 转成 DataFrame，清洗、统计并出图。"""

import textwrap

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


df = pd.read_excel("ADCdb_1.0.xlsx")
df["ADC ID"] = df["ADC ID"].astype(int).astype(str)    # 类型规整
df = df.drop_duplicates().reset_index(drop=True)       # 去重

print("维度:", df.shape)
print("缺失值:\n", df.isna().sum()[df.isna().sum() > 0])
print("Top 8 抗体:\n", df["Antibody Name"].value_counts().head(8))
print("Top 8 偶联方式:\n", df["Conjugate Type"].value_counts().head(8))
print("Top 8 连接子:\n", df["Linker Name"].value_counts().head(8))
print("Top 5 载荷:\n", df["Payload Name"].value_counts().head(5))

df.to_csv("cleaned_adcdb.csv", index=False)            # 保存清洗结果


def top_counts(series, n=8):
    """取频数最高的前 n 项。"""
    return series.value_counts().head(n)


def wrap(label, width=30, maxlines=2):
    """长名称最多拆成两行，超出加省略号。"""
    lines = textwrap.wrap(label, width=width)
    if len(lines) <= maxlines:
        return "\n".join(lines)
    return "\n".join(lines[:maxlines]) + "…"


fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("ADCdb 常见字段 Top 8", fontsize=16)
parts = [
    (axes[0, 0], df["Antibody Name"], "Top 8 抗体"),
    (axes[0, 1], df["Conjugate Type"], "Top 8 偶联方式"),
    (axes[1, 0], df["Linker Name"], "Top 8 连接子"),
    (axes[1, 1], df["Payload Name"], "Top 8 载荷"),
]
for ax, col, title in parts:
    counts = top_counts(col)
    bars = ax.barh(counts.index.map(wrap), counts.values)
    ax.bar_label(bars, fmt="%d", padding=3)
    ax.set_title(title, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel("记录数")
plt.tight_layout(rect=(0, 0, 1, 0.96))
plt.savefig("antibody_conjugate.png", dpi=120, bbox_inches="tight")