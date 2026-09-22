"""Automated Forensic Analyzer for Competitor Notebooks.

Dissects code, AST imports, algorithmic patterns, validation splits,
and markdown insights to produce a Competitive Consensus Matrix.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Set


KNOWN_LIBRARIES = [
    "torch", "torch_geometric", "rdkit", "lightgbm", "xgboost", "catboost",
    "sklearn", "numba", "scipy", "pyarrow", "fastparquet", "polars",
    "timm", "transformers", "networkx", "optuna", "cupy", "faiss"
]

KNOWN_TECHNIQUES = {
    "Scaffold Split": [r"scaffold", r"bemis", r"murcko"],
    "Group K-Fold": [r"groupkfold", r"groupsplit", r"grouped"],
    "Modified Cosine / Delta Shift": [r"modified_cosine", r"mass_shift", r"analog_propagation", r"precursor_shift"],
    "Numba Acceleration": [r"@njit", r"@jit", r"numba"],
    "In-Silico Fragmentation": [r"fragmentation", r"metfrag", r"bond_break"],
    "Fingerprint Similarity (Morgan/Tanimoto)": [r"tanimoto", r"morgan", r"fingerprint", r"getmorganfingerprint"],
    "Reciprocal Rank Fusion (RRF)": [r"rrf", r"reciprocal_rank", r"rank_fusion"],
    "Non-Negative Least Squares (NNLS)": [r"nnls", r"non_negative", r"scipy\.optimize\.nnls"],
    "External Database Ingestion": [r"coconut", r"pubchem", r"hmdb", r"mona", r"gnps"],
    "Neural Embedding / Encoder": [r"nn\.Module", r"encoder", r"transformer", r"spectrum2vec", r"spec2vec"]
}


class NotebookAnalyzer:
    """Forensic engine to analyze Jupyter notebooks and python scripts."""

    def __init__(self, notebook_paths: List[Path]):
        self.notebook_paths = notebook_paths
        self.analyses: List[Dict[str, Any]] = []

    def analyze_single_notebook(self, path: Path) -> Dict[str, Any]:
        """Dissect one notebook file."""
        code_cells = []
        md_cells = []

        if path.suffix == ".ipynb":
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
                for cell in data.get("cells", []):
                    text = "".join(cell.get("source", []))
                    if cell.get("cell_type") == "code":
                        code_cells.append(text)
                    elif cell.get("cell_type") == "markdown":
                        md_cells.append(text)
            except Exception as e:
                print(f"[WARN] Error reading {path.name}: {e}")
        elif path.suffix == ".py":
            code_cells.append(path.read_text(encoding="utf-8", errors="ignore"))

        full_code = "\n".join(code_cells).lower()
        full_md = "\n".join(md_cells)

        # 1. Detect Libraries
        detected_libs = set()
        for lib in KNOWN_LIBRARIES:
            if re.search(rf"\b(import|from)\s+{lib}\b", full_code):
                detected_libs.add(lib)

        # 2. Detect Algorithmic Techniques
        detected_techs = set()
        for tech_name, patterns in KNOWN_TECHNIQUES.items():
            for p in patterns:
                if re.search(p, full_code, re.IGNORECASE) or re.search(p, full_md, re.IGNORECASE):
                    detected_techs.add(tech_name)
                    break

        # 3. Extract High-Level Strategy / Insights from Markdown
        key_insights = []
        for line in full_md.splitlines():
            line_str = line.strip()
            if any(k in line_str.lower() for k in ["sota", "mrr", "lb", "cv", "class 1", "class 2", "analog", "retrieval", "ablation"]):
                if len(line_str) > 20 and len(line_str) < 200 and not line_str.startswith("<"):
                    key_insights.append(line_str)

        return {
            "filename": path.name,
            "path": str(path),
            "libraries": sorted(list(detected_libs)),
            "techniques": sorted(list(detected_techs)),
            "insights": key_insights[:6]
        }

    def run_batch_analysis(self) -> Dict[str, Any]:
        """Analyze all notebooks and compute consensus statistics."""
        self.analyses = [self.analyze_single_notebook(p) for p in self.notebook_paths]

        lib_counts = Counter()
        tech_counts = Counter()
        for a in self.analyses:
            for l in a["libraries"]:
                lib_counts[l] += 1
            for t in a["techniques"]:
                tech_counts[t] += 1

        n_total = max(1, len(self.analyses))
        consensus_matrix = {
            "libraries": {lib: count / n_total for lib, count in lib_counts.most_common()},
            "techniques": {tech: count / n_total for tech, count in tech_counts.most_common()},
        }

        return {
            "total_notebooks": n_total,
            "consensus_matrix": consensus_matrix,
            "individual_analyses": self.analyses
        }

    def generate_dossier_markdown(self, competition_slug: str) -> str:
        """Render comprehensive executive intelligence dossier."""
        batch = self.run_batch_analysis()
        consensus = batch["consensus_matrix"]

        md = f"""# 🛰️ DOSSIER DE INTELIGENCIA FORENSE & CONSENSO SOTA
### Competencia: `{competition_slug}`
**Análisis Sistemático de los Top {batch['total_notebooks']} Notebooks de Kaggle**  
*Generado por CMRE Industrial Harvester & Notebook Analyzer Engine*

---

## 📊 1. Matriz de Consenso Técnico (¿Qué usan los Ganadores?)

### Técnicas y Algoritmos Dominantes
| Técnica Identificada | Adopción en Top Notebooks | Nivel de Relevancia |
| :--- | :---: | :--- |
"""
        for tech, freq in consensus["techniques"].items():
            level = "🔥 OBLIGATORIO (Consenso)" if freq >= 0.6 else ("⚡ ALTA VENTAJA" if freq >= 0.3 else "🔬 DIFERENCIADOR NICHO")
            pct = int(freq * 100)
            md += f"| **{tech}** | `{pct}%` | {level} |\n"

        md += """
### Librerías y Frameworks Más Utilizados
| Librería | Frecuencia de Uso |
| :--- | :---: |
"""
        for lib, freq in consensus["libraries"].items():
            pct = int(freq * 100)
            md += f"| `{lib}` | `{pct}%` |\n"

        md += """
---

## 🔍 2. Radiografía Detallada por Notebook

"""
        for a in self.analyses:
            md += f"### 📓 `{a['filename']}`\n"
            md += f"* **Librerías clave:** {', '.join(f'`{l}`' for l in a['libraries']) if a['libraries'] else 'Estándar'}\n"
            md += f"* **Técnicas activadas:** {', '.join(f'**{t}**' for t in a['techniques']) if a['techniques'] else 'Ninguna detectada'}\n"
            if a['insights']:
                md += "* **Afirmaciones / Claims detectados en texto:**\n"
                for ins in a['insights']:
                    md += f"  > *\"{ins}\"*\n"
            md += "\n"

        md += """---
## 🎯 3. Síntesis y Recomendación para Nuestro Pipeline
1. **Piso Común:** Toda solución competitiva debe implementar las técnicas con >60% de adopción.
2. **El Factor Alpha:** Las técnicas en la franja de 30% a 50% (ej. *Mass-Shifted Analog Propagation*, *RRF*, *Bases Externas*) son las que otorgan el salto a la zona de medallas.
"""
        return md
