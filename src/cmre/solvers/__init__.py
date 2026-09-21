"""
CMRE CANONICAL COMPETITION SOLVERS
Pipelines ejecutables de extremo a extremo para las 5 competencias doradas.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from .enveda_casmi_solver import EnvedaCasmiSolver
from .rsna_mammography_solver import RSNAMammographySolver
from .isic_melanoma_solver import ISICMelanomaSolver
from .richters_predictor_solver import RichtersPredictorSolver
from .zindi_airqo_solver import ZindiAirQoSolver

__all__ = [
    "EnvedaCasmiSolver",
    "RSNAMammographySolver",
    "ISICMelanomaSolver",
    "RichtersPredictorSolver",
    "ZindiAirQoSolver",
]
