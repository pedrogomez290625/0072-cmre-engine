import pytest
import time
import numpy as np
import torch
from cmre.solvers.rsna_knee_solver import RSNAKneeSolver
from cmre.solvers.enveda_casmi_solver import EnvedaCasmiSolver
from cmre.solvers.arc_agi_hybrid_solver import ArcAgiHybridSolver

def test_benchmark_rsna_knee_solver():
    start_time = time.time()

    solver = RSNAKneeSolver()

    # Mocking a synthetic validation case
    y_true = np.random.randint(0, 2, size=(100, 12))

    n_models = 3
    multi_preds = [np.random.rand(100, 12) for _ in range(n_models)]
    study_views = {"dummy": np.random.rand(100, 12)}
    out = solver.run_pipeline(
        study_views_dict=study_views,
        models_preds_list=multi_preds,
        y_true=y_true,
        clinical_priors=None
    )

    end_time = time.time()

    assert out is not None
    assert (end_time - start_time) < 5.0

def test_benchmark_enveda_casmi_solver():
    start_time = time.time()

    solver = EnvedaCasmiSolver()

    smiles = ["CC", "CCO", "CCN"]
    query_bitsets = [1010, 1100, 1110]
    candidate_bitsets = [1010, 1100, 1110]
    candidate_masses = [30.0, 46.0, 45.0]
    query_mass = 30.0

    out = solver.run_pipeline(
        smiles_list=smiles,
        query_bitsets=query_bitsets,
        candidate_bitsets=candidate_bitsets,
        candidate_masses=candidate_masses,
        query_mass=query_mass
    )

    end_time = time.time()

    assert out is not None
    assert (end_time - start_time) < 5.0

def test_benchmark_arc_agi_hybrid_solver():
    start_time = time.time()

    solver = ArcAgiHybridSolver()

    task_data = {
        "train": [{"input": [[0, 1], [1, 0]], "output": [[1, 0], [0, 1]]}],
        "test": [{"input": [[1, 1], [0, 0]]}]
    }

    preds = solver.run_task(task_data)

    end_time = time.time()

    assert preds is not None
    assert (end_time - start_time) < 5.0
