import pytest
from cmre.connectors.kaggle_writeups import KaggleWriteupConnector

@pytest.fixture
def sample_writeup():
    return """
# Solution to Example Competition

## Validation Scheme
We used a 5-fold StratifiedKFold based on patient IDs.

## Feature Engineering
We extracted TF-IDF features and normalized the tabular data.

## Model Architecture
We used an EfficientNet-B4 combined with a 2-layer MLP.

## Loss Function
Focal loss with gamma=2.0 and alpha=0.25 was used.

## Ensemble
We blended the predictions using a simple average of 5 seeds.
"""

def test_kaggle_writeup_connector_parsing(sample_writeup):
    connector = KaggleWriteupConnector()
    resource = connector.parse_writeup(
        text=sample_writeup,
        url="https://kaggle.com/discussion/123",
        title="1st Place Solution",
        author="Kaggle Grandmaster"
    )

    assert resource.platform == "kaggle"
    assert resource.title == "1st Place Solution"
    assert resource.author == "Kaggle Grandmaster"
    assert "5-fold StratifiedKFold" in resource.cv_scheme
    assert "TF-IDF" in resource.feature_engineering
    assert "EfficientNet-B4" in resource.architecture
    assert "Focal loss" in resource.loss
    assert "simple average" in resource.ensemble

def test_kaggle_writeup_connector_missing_sections():
    connector = KaggleWriteupConnector()
    text = "Just a quick note that I used Random Forest."
    resource = connector.parse_writeup(text, "url", "title")

    assert resource.cv_scheme is None
    assert resource.feature_engineering is None
    assert resource.architecture is None
    assert resource.loss is None
    assert resource.ensemble is None
