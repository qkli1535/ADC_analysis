# ADCdb 数据分析

将 ADC（抗体偶联药物）数据库 `ADCdb_1.0.xlsx` 中的原始表格转化为 pandas 的 DataFrame，
并进行数据清洗、统计与可视化，在 Jupyter Notebook 中展示分析结果。

## 项目结构

```
ADC_Analysis/
├── ADCdb_Analysis.ipynb   # 分析 Notebook（数据转 pandas → 清洗 → 统计 → 出图）
├── analysis.py            # 等同流程的独立脚本，可直接运行
├── cleaned_adcdb.csv      # 清洗后数据（由脚本生成）
├── antibody_conjugate.png # 可视化结果（Top 8 横向条形图，数值标注）
├── requirements.txt       # 依赖清单
└── README.md              # 项目说明
```

## 快速开始

```bash
pip install -r requirements.txt

# 方式一：运行脚本
python analysis.py

# 方式二：在 Jupyter 中逐格运行
jupyter notebook ADCdb_Analysis.ipynb
```

运行后自动生成清洗数据 `cleaned_adcdb.csv` 与可视化图 `antibody_conjugate.png`。

## 分析内容

1. 用 `pandas.read_excel` 把 Excel 读成 DataFrame；
2. 缺失值统计、ADC ID 类型规整、去除重复记录；
3. 抗体、偶联方式、连接子、载荷的频数统计；
4. 四类字段各取 **Top 8**，绘制**横向条形图**并标注具体数值，长名称自动换行，保存为 PNG。

## 主要结论

- 原始数据 **1431 行、13 列**，清洗后无重复；
- 最常用抗体：**Trastuzumab**（73 条）；
- 主要偶联方式：随机还原链间二硫键偶联（845 条）；
- 最常见连接子：**Mc-Val-Cit-PABC**（236 条）；
- 最常见载荷：**Monomethyl auristatin E**（259 条）。