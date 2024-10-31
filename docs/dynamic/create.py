import iesopt
from pathlib import Path


DYNAMIC = Path(__file__).parent


def create_md(items):
    for it in items:
        with open(DYNAMIC / "out" / f"{it[0]}.md", "w") as f:
            f.write("`````{attribute} " + it[2] + "\n")
            f.write(iesopt.get_jl_docstr(it[1]))
            f.write("\n`````")
