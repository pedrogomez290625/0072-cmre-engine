1. **[CMRE-118] Mitigación de UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION**
   - Use `write_file` to create `tests/test_cmre_118.py` containing a test for `MultiViewOrthogonalAligner` to confirm latency bounded upstream pruning handles multi-view data efficiently. Verify the file was created using `cat tests/test_cmre_118.py`.

2. **[CMRE-119] Mitigación de SCAFFOLD_ANALOG_MEMORIZATION_LEAK**
   - Use `write_file` to create `tests/test_cmre_119.py` containing a test for `molecular_scaffold_split` to test scaffold disjunction to guard against analog memorization leak. Verify the file was created using `cat tests/test_cmre_119.py`.

3. **[CMRE-120] Mitigación de SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE**
   - Use `write_file` to create `tests/test_cmre_120.py` containing a test for `ArcAgiHybridSolver` verifying it handles timeouts and symbolic failures by enforcing non-identity fallbacks strictly. Verify the file was created using `cat tests/test_cmre_120.py`.

4. **[CMRE-121] Mitigación de UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD**
   - Use `write_file` to create `tests/test_cmre_121.py` containing a test for `SIRIUSAbsenceAxiomOptimizer` checking the massive decoy pruning using this biophysical filter rule. Verify the file was created using `cat tests/test_cmre_121.py`.

5. **[CMRE-122] Mitigación de THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT**
   - Use `write_file` to create `tests/test_cmre_122.py` containing a test for `NelderMeadThresholdOptimizer` checking the alignment of optimized thresholds for minority classes using Nelder-Mead to avoid metric misalignment collapse. Verify the file was created using `cat tests/test_cmre_122.py`.

6. **Update JULES_DYNAMIC_TASKS.md**
   - Use a Python script via `run_in_bash_session` to mark CMRE-118 through CMRE-122 as completed in `JULES_DYNAMIC_TASKS.md`. Verify the changes using `cat JULES_DYNAMIC_TASKS.md`.

7. **Update JULES_EXECUTION_LOG.md**
   - Use a Python script via `run_in_bash_session` to append a new entry to `JULES_EXECUTION_LOG.md` detailing the achievements for CMRE-118 through CMRE-122. Verify the changes using `tail -n 30 JULES_EXECUTION_LOG.md`.

8. **Update .specify/tasks/latest.md**
   - Use a Python script via `run_in_bash_session` to add a completed task entry for CMRE-118 through CMRE-122 in `.specify/tasks/latest.md`. Verify the changes using `tail -n 30 .specify/tasks/latest.md`.

9. **Update ARQUITECTURA_ESTADO.md**
    - Use a Python script via `run_in_bash_session` to update `ARQUITECTURA_ESTADO.md` noting the new capabilities for CMRE-118 through CMRE-122. Verify the changes using `tail -n 30 ARQUITECTURA_ESTADO.md`.

10. **Run Tests**
   - Use `run_in_bash_session` to execute `PYTHONPATH=src uv run pytest tests/`. Verify that all tests pass.

11. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
    - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

12. **Submit changes**
    - Call `submit` to commit and push to `main` with title `feat(jules): [TASK-ID] <descripción breve>`.
