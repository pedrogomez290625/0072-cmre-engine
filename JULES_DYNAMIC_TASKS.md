# JULES DYNAMIC TASKS
Registro de super-tareas de ingeniería autónoma generadas dinámicamente.

- [ ] CMRE-268: Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano. (Mitigación FAIL_06 - TARGET_ENCODING_HIGH_CARDINALITY_LEAKAGE).
- [ ] CMRE-269: Cálculo de desvíos relativos (Delta Trick) y normalización robusta intercuartílica (IQR). (Mitigación FAIL_07 - UNSCALED_COUNT_FEATURE_LEAKAGE_AND_CONSTANT_SHIFT).
- [ ] CMRE-270: Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers. (Mitigación FAIL_08 - LABEL_NOISE_MEMORIZATION_AND_GRADIENT_CORRUPTION).
- [ ] CMRE-271: Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras. (Mitigación FAIL_11 - SYMBOLIC_TIMEOUT_IDENTITY_FALLBACK_COLLAPSE).
- [ ] CMRE-272: LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio. (Mitigación FAIL_12 - UPSTREAM_ENSEMBLE_LATENCY_EXPLOSION).
- [ ] CMRE-273: Sanitización explícita forzando tensores y buffers de normalización a .float() antes del autocast a .half(). (Mitigación FAIL_13 - CUDA_FP16_DOUBLE_PRECISION_TYPE_MISMATCH).
- [ ] CMRE-274: Axioma de Ausencia SIRIUS que penaliza severamente candidatos que carecen de heteroátomos (O, N) requeridos para las pérdidas neutrales observadas (H2O, CO2, NH3). (Mitigación FAIL_14 - UNCONSTRAINED_CANDIDATE_DECOY_OVERLOAD).
