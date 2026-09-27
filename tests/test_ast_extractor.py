import pytest
from cmre.services.ast_extractor import ASTExtractor

@pytest.fixture
def sample_script():
    return """
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def load_image(self, idx):
        return self.data[idx]

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

def custom_bce_loss(y_pred, y_true):
    return nn.BCELoss()(y_pred, y_true)

def simple_blend(preds1, preds2):
    return (preds1 + preds2) / 2
"""

def test_ast_extractor_classification(sample_script):
    extractor = ASTExtractor()
    extracted = extractor.parse_script(sample_script)

    assert "MyDataset" in extracted["MOD_INGEST"]
    assert "load_image" in extracted["MOD_INGEST"]

    assert "MyModel" in extracted["MOD_BACKBONE"]
    assert "forward" in extracted["MOD_BACKBONE"]

    assert "custom_bce_loss" in extracted["MOD_LOSS"]

    assert "simple_blend" in extracted["MOD_ENSEMBLE"]

def test_ast_extractor_empty():
    extractor = ASTExtractor()
    extracted = extractor.parse_script("x = 1\ny = 2")
    for mod_list in extracted.values():
        assert len(mod_list) == 0
