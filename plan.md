1. Use `cat ACTIVE_COMPETITIONS.json` to read the active competitions, modalities, and metrics.
2. Use `cat ARQUITECTURA_ESTADO.md` and `cat JULES_DYNAMIC_TASKS.md` to understand the state of the 6 canonical modules and pending super-tasks.
3. Use `grep -C 5 "ENTRADA 073" JULES_EXECUTION_LOG.md` to review the execution log for learned lessons or pending warnings from the previous session.
4. Use `ls data/knowledge/` and `ls knowledge_db/` to verify the state of catalogs, respecting the anti-collision rule (additive reading/integration, no overwriting or deleting).
5. Run the full test suite using `PYTHONPATH=src uv run pytest tests/` to validate the initial state of the repository, maintaining 100% green tests (132+ passed).
6. Create a temporary Python script to append a new initialization entry to `JULES_EXECUTION_LOG.md` signed by `Perez, Ernesto Rafael ("Rafa")` recording the completed steps. Run the script and delete it afterward.
7. Use `git diff JULES_EXECUTION_LOG.md` to verify the changes made to the log.
8. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
9. Use the submit tool to open a Pull Request to the main branch with the title `feat(jules): Rutina de Inicialización y Memoria Dinámica` and description. No explicit task ID is listed in `.specify/tasks/latest.md` for this initialisation, so no `[TASK-ID]` prefix will be used.
