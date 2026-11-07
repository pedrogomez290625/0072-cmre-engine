# JULES DYNAMIC TASKS
Registro de super-tareas de ingeniería autónoma generadas dinámicamente.

- [ ] CMRE-262: Implementar optimización simplex Nelder-Mead continua del umbral sobre predicciones OOF restringiendo recall mínimo (Mitigación FAIL_01 - THRESHOLD_COLLAPSE_AND_METRIC_DISALIGNMENT).
- [ ] CMRE-263: Desarrollar PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test (Mitigación FAIL_02 - TEMPORAL_LOOKAHEAD_AUTOCORRELATION_BIAS).
- [ ] CMRE-264: Integrar corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning (Mitigación FAIL_03 - EDGE_SEAM_BOUNDARY_DEGRADATION).
- [ ] CMRE-265: Construir particionado disjunto por esqueletos moleculares de Bemis-Murcko - BemisMurckoScaffoldSplit (Mitigación FAIL_04 - SCAFFOLD_ANALOG_MEMORIZATION_LEAK).
- [ ] CMRE-266: Implementar StratifiedGroupKFold agrupado estrictamente por patient_id combinado con la normalización de Patito Feo (Mitigación FAIL_05 - PATIENT_IDENTITY_COHORT_LEAKAGE).
- [ ] CMRE-267: Integrar Mínimos Cuadrados No Negativos (Non-Negative Least Squares / NNLS) forzando pesos w_i >= 0 y suma(w) = 1.0 para stacking (Mitigación FAIL_09 - NEGATIVE_WEIGHT_MULTICOLLINEARITY_COLLAPSE).
