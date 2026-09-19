# -*- coding: utf-8 -*-
"""顺序执行 Notebook 中所有代码单元格，验证其可复现。"""
import json
import io
import sys

OUT = r"e:\project\ADC_Analysis\ADCdb_Analysis.ipynb"
CWD = r"e:\project\ADC_Analysis"
sys.path.insert(0, CWD)
sys.path.insert(0, "")

with open(OUT, encoding="utf-8") as fh:
    nb = json.load(fh)

for i, cell in enumerate(nb["cells"], 1):
    if cell["cell_type"] != "code":
        continue
    src = cell["source"]
    print(f"\n=== 代码单元格 {i} ===")
    try:
        exec(compile(src, f"<cell{i}>", "exec"))
    except Exception as exc:  # noqa: BLE001
        print(f"执行失败: {exc}")
        raise