"""Static QA for the SCMS EDA notebook. Run from the project root: python tools/qa_check.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB = ROOT / "notebooks" / "SCMS_Complete_EDA_Project.ipynb"
nb = json.loads(NB.read_text(encoding="utf-8"))
cells = nb["cells"]
src = lambda c: "".join(c["source"])
results = []

def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

code = [c for c in cells if c["cell_type"] == "code"]
md = [c for c in cells if c["cell_type"] == "markdown"]

# Charts = code cells that save a figure to visualizations/NN_name.png
chart_cells = [c for c in code if re.search(r'save_fig\(.*"\d\d_|plot_\w+\(.*"\d\d_|loglog_scatter\(.*"\d\d_', src(c), re.S)]
check("charts >= 24", len(chart_cells) >= 24, f"({len(chart_cells)} chart cells)")

triplets = [c for c in md if all(k in src(c) for k in ("**Why this chart:**", "**Insight:**", "**Business impact:**"))]
check("Why/Insight/Impact cells == charts", len(triplets) == len(chart_cells), f"({len(triplets)} vs {len(chart_cells)})")

# Each chart cell must be immediately followed by its insight cell
adjacent = all(
    cells[i + 1]["cell_type"] == "markdown" and "**Why this chart:**" in src(cells[i + 1])
    for i, c in enumerate(cells) if c in chart_cells
)
check("insight cell directly after every chart", adjacent)

headings = ["Project Name", "Project Type", "Team Members", "Project Summary", "Problem Statement",
            "Business Objective", "Conclusion", "GitHub Link"]
found = {h: any(re.match(rf"#+\s*{h}\b", src(c).lstrip()) for c in md) for h in headings}
check("required headings", all(found.values()), str([h for h, ok in found.items() if not ok]))

summ = next(src(c) for c in md if src(c).lstrip().startswith("## Project Summary"))
words = len(summ.split("\n", 1)[1].split())
check("summary 500-600 words", 500 <= words <= 600, f"({words} words)")

abs_pat = re.compile(r"((?<![A-Za-z])[A-Za-z]:[\\/]|/home/|/mnt/|/Users/)")  # drive letters, not words ending in ":\\n"
bad = [i for i, c in enumerate(code) if abs_pat.search(src(c))]
check("no absolute paths in code", not bad, str(bad))

errors = [o for c in code for o in c.get("outputs", []) if o.get("output_type") == "error"]
check("no error outputs", not errors)
check("outputs saved", all(c.get("outputs") is not None and c.get("execution_count") for c in code))

pngs = sorted((ROOT / "visualizations").glob("[0-9][0-9]_*.png"))
check("PNGs present", len(pngs) >= 24, f"({len(pngs)})")
check("cleaned CSV present", (ROOT / "data" / "processed" / "SCMS_Delivery_History_Cleaned.csv").exists())
check("requirements.txt present", (ROOT / "requirements.txt").exists())

print("\nOVERALL:", "PASS" if all(results) else "FAIL")
sys.exit(0 if all(results) else 1)
