"""
CMRE CANONICAL COMPETITION SOLVERS
Pipelines ejecutables de extremo a extremo para las competencias de élite.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from .enveda_casmi_solver import EnvedaCasmiSolver
from .rsna_mammography_solver import RSNAMammographySolver
from .isic_melanoma_solver import ISICMelanomaSolver
from .richters_predictor_solver import RichtersPredictorSolver
from .zindi_airqo_solver import ZindiAirQoSolver
from .rsna_knee_solver import RSNAKneeSolver
from .arc_agi_hybrid_solver import ArcAgiHybridSolver

__all__ = [
    "EnvedaCasmiSolver",
    "RSNAMammographySolver",
    "ISICMelanomaSolver",
    "RichtersPredictorSolver",
    "ZindiAirQoSolver",
    "RSNAKneeSolver",
    "ArcAgiHybridSolver",
]
