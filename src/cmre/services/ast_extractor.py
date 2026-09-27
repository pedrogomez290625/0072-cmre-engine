import ast
from typing import Dict, List

class ASTExtractor:
    def __init__(self):
        self.modules = {
            "MOD_INGEST": ["Dataset", "DataLoader", "read_csv", "load_image"],
            "MOD_SIGNAL": ["Transform", "augment", "Normalize"],
            "MOD_VALIDATION": ["KFold", "GroupKFold", "split"],
            "MOD_BACKBONE": ["nn.Module", "forward", "resnet", "efficientnet", "transformer"],
            "MOD_LOSS": ["Loss", "criterion", "BCE", "MSE", "CrossEntropy"],
            "MOD_ENSEMBLE": ["blend", "average", "ensemble"]
        }

    def parse_script(self, script_content: str) -> Dict[str, List[str]]:
        """Parses a Python script and classifies functions/classes into CMRE modules."""
        tree = ast.parse(script_content)
        extracted = {k: [] for k in self.modules.keys()}

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                node_code = ast.get_source_segment(script_content, node)
                if not node_code:
                    continue
                node_lower = node_code.lower()
                for mod, keywords in self.modules.items():
                    if any(kw.lower() in node_lower for kw in keywords):
                        extracted[mod].append(node.name)

        # Deduplicate
        return {k: list(set(v)) for k, v in extracted.items()}
