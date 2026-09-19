# ADCdb 数据分析

将 ADC（抗体偶联药物）数据库 `ADCdb_1.0.xlsx` 中的原始表格转化为 **pandas** 对象，
并进行数据清洗、探索性分析与可视化，最终通过 Jupyter Notebook 展示分析结果。

## 项目结构

```
ADC_Analysis/
├── ADCdb_Analysis.ipynb   # 主交付物：数据分析 Notebook（108 行）
├── ADCdb_1.0.xlsx         # 原始数据（1431 行 × 13 列）
├── gen_notebook.py        # Notebook 生成脚本（可复现）
├── verify_nb.py           # Notebook 执行校验脚本
├── requirements.txt       # 依赖清单
└── README.md              # 项目说明
```

## 快速开始

```bash
# 1. 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动并运行
jupyter notebook ADCdb_Analysis.ipynb
# 或命令行复现（自动执行全部单元格）
jupyter nbconvert --to notebook --execute ADCdb_Analysis.ipynb
```

## 分析内容

1. **载入数据**：使用 `pandas.read_excel` 将 Excel 工作表转为 DataFrame；
2. **数据清洗**：缺失值统计、主键（ADC ID）唯一性校验、去除重复记录；
3. **探索性分析**：抗体平台、偶联方式、载荷与连接子的频数统计与交叉分析；
4. **可视化**：抗体 Top 8、偶联方式分布、载荷占比等图表。

## 主要结论

- 原始数据共 **1431 行、13 列**，`ADC ID` 可作为主键；
- **Trastuzumab** 是最常用抗体骨架（73 条记录）；
- 偶联方式以「随机半胱氨酸还原偶联」为主（845 条）；
- 最常用载荷为 **Monomethyl auristatin E**（259 条）。

## 版本管理

本项目要求使用 Git 进行版本管理，并添加标签：

```bash
git init
git add .
git commit -m "feat: ADCdb 数据转化为 pandas 对象分析"
git tag -a v1.0 -m "homework submission"
git remote add origin <你的仓库地址>
git push origin main --tags
```