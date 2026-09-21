"""
CMRE ADVANCED HPC & COMPETITIVE ALGORITHMIA MODULE
Implementaciones de alto rendimiento inspiradas en Codeforces, ICPC Gold (KACTL) y AtCoder Library (ACL).

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
import math
import random
import time
from typing import List, Tuple, Callable, Optional


class SegmentTreeLazy:
    """
    Segment Tree con Lazy Propagation para consultas y actualizaciones en rango O(log N).
    Optimizado para microestructura de mercado (Optiver), agregaciones de volatilidad
    y series biomédicas (ECG/EEG).
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(self, size_or_data: int | List[float], op: str = "sum"):
        self.op = op.lower()
        if isinstance(size_or_data, list):
            self.n = len(size_or_data)
            self.tree = [0.0] * (4 * self.n)
            self.lazy = [0.0] * (4 * self.n)
            if self.n > 0:
                self._build(size_or_data, 1, 0, self.n - 1)
        else:
            self.n = size_or_data
            self.tree = [0.0] * (4 * self.n)
            self.lazy = [0.0] * (4 * self.n)

    def _merge(self, a: float, b: float) -> float:
        if self.op == "sum":
            return a + b
        elif self.op == "max":
            return max(a, b)
        elif self.op == "min":
            return min(a, b)
        raise ValueError(f"Operación desconocida: {self.op}")

    def _build(self, data: List[float], node: int, start: int, end: int):
        if start == end:
            self.tree[node] = float(data[start])
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self._merge(self.tree[2 * node], self.tree[2 * node + 1])

    def _push(self, node: int, start: int, end: int):
        if self.lazy[node] != 0.0:
            val = self.lazy[node]
            mid = (start + end) // 2
            
            # Aplicar a hijo izquierdo
            if self.op == "sum":
                self.tree[2 * node] += val * (mid - start + 1)
                self.tree[2 * node + 1] += val * (end - mid)
            elif self.op in ("max", "min"):
                self.tree[2 * node] += val
                self.tree[2 * node + 1] += val
                
            self.lazy[2 * node] += val
            self.lazy[2 * node + 1] += val
            self.lazy[node] = 0.0

    def update_range(self, l: int, r: int, val: float, node: int = 1, start: int = 0, end: int = -1):
        if end == -1:
            end = self.n - 1
        if l > end or r < start or self.n == 0:
            return
        if l <= start and end <= r:
            if self.op == "sum":
                self.tree[node] += val * (end - start + 1)
            else:
                self.tree[node] += val
            self.lazy[node] += val
            return

        self._push(node, start, end)
        mid = (start + end) // 2
        self.update_range(l, r, val, 2 * node, start, mid)
        self.update_range(l, r, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = self._merge(self.tree[2 * node], self.tree[2 * node + 1])

    def query_range(self, l: int, r: int, node: int = 1, start: int = 0, end: int = -1) -> float:
        if end == -1:
            end = self.n - 1
        if l > end or r < start or self.n == 0:
            if self.op == "sum":
                return 0.0
            elif self.op == "max":
                return -float("inf")
            elif self.op == "min":
                return float("inf")
        if l <= start and end <= r:
            return self.tree[node]

        self._push(node, start, end)
        mid = (start + end) // 2
        left_val = self.query_range(l, r, 2 * node, start, mid)
        right_val = self.query_range(l, r, 2 * node + 1, mid + 1, end)
        return self._merge(left_val, right_val)


class SimulatedAnnealingSelector:
    """
    Selección combinatoria de variables de ultra-alta velocidad mediante Recocido Simulado (SA).
    Implementa patch-based mutation con reversión de estado en O(1) ante transiciones rechazadas.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(
        self,
        n_features: int,
        k_target: int,
        max_steps: int = 1000,
        initial_temp: float = 10.0,
        cooling_rate: float = 0.995,
        seed: int = 42
    ):
        self.n_features = n_features
        self.k_target = min(k_target, n_features)
        self.max_steps = max_steps
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.rng = random.Random(seed)

    def fit(self, eval_fn: Callable[[List[int]], float]) -> Tuple[List[int], float]:
        """
        Optimiza buscando maximizar eval_fn(selected_indices).
        Devuelve (mejores_indices, mejor_score).
        """
        all_features = list(range(self.n_features))
        current_set = set(self.rng.sample(all_features, self.k_target))
        current_score = eval_fn(sorted(list(current_set)))
        
        best_set = set(current_set)
        best_score = current_score
        
        t = self.initial_temp
        
        for step in range(self.max_steps):
            if t <= 1e-6:
                break
                
            # Mutación local O(1): quitar un elemento activo y añadir un inactivo
            u_out = self.rng.choice(list(current_set))
            inactive = [f for f in all_features if f not in current_set]
            if not inactive:
                break
            u_in = self.rng.choice(inactive)
            
            # Aplicar mutación
            current_set.remove(u_out)
            current_set.add(u_in)
            
            new_score = eval_fn(sorted(list(current_set)))
            delta = new_score - current_score
            
            # Criterio de aceptación Metropolis
            if delta > 0.0 or math.exp(delta / t) > self.rng.random():
                current_score = new_score
                if current_score > best_score:
                    best_score = current_score
                    best_set = set(current_set)
            else:
                # Reversión en O(1)
                current_set.remove(u_in)
                current_set.add(u_out)
                
            t *= self.cooling_rate
            
        return sorted(list(best_set)), best_score


class ChokudaiSearchOptimizer:
    """
    Chokudai Beam Search con profundización iterativa multi-nivel y presupuesto estricto de tiempo.
    Inspirado en AtCoder Heuristic Contests (AHC) para calibración de pesos de ensamble y poda combinatoria.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    def __init__(
        self,
        n_models: int,
        beam_width: int = 5,
        max_depth: int = 10,
        time_limit_sec: float = 0.5
    ):
        self.n_models = n_models
        self.beam_width = beam_width
        self.max_depth = max_depth
        self.time_limit_sec = time_limit_sec

    def optimize(self, eval_weights_fn: Callable[[List[float]], float]) -> Tuple[List[float], float]:
        """
        Encuentra pesos discretizados en el simplex [0, 1] que sumen 1.0 maximizando eval_weights_fn.
        """
        start_time = time.time()
        
        # beams[depth] almacena los mejores estados encontrados a esa profundidad
        # estado: (score, weights)
        beams: List[List[Tuple[float, List[int]]]] = [[] for _ in range(self.max_depth + 1)]
        
        init_weights = [0] * self.n_models
        init_score = -float("inf")
        beams[0].append((init_score, init_weights))
        
        best_score = -float("inf")
        best_weights = [1.0 / self.n_models] * self.n_models
        
        while time.time() - start_time < self.time_limit_sec:
            updated = False
            for d in range(self.max_depth):
                if not beams[d]:
                    continue
                
                # Expandir mejor estado en beams[d]
                state_score, state_weights = beams[d].pop(0)
                
                for m in range(self.n_models):
                    next_weights = list(state_weights)
                    next_weights[m] += 1
                    
                    # Normalizar a flotantes
                    total_mass = sum(next_weights)
                    norm_weights = [w / total_mass for w in next_weights]
                    
                    score = eval_weights_fn(norm_weights)
                    if score > best_score:
                        best_score = score
                        best_weights = norm_weights
                        
                    next_beam = beams[d + 1]
                    next_beam.append((score, next_weights))
                    next_beam.sort(key=lambda x: x[0], reverse=True)
                    if len(next_beam) > self.beam_width:
                        next_beam.pop()
                    updated = True
                    
            if not updated:
                break
                
        return best_weights, best_score
