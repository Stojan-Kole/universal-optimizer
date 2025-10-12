from __future__ import annotations
from typing import Callable, Sequence, Optional
import numpy as np
import copy
import matplotlib.pyplot as plt

from uo.algorithm.metaheuristic.population_based_metaheuristic import PopulationBasedMetaheuristic
from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl
from uo.problem.problem import Problem


# -----------------------------
# Dummy Problem za MAML
# -----------------------------
class DummyProblem(Problem):
    def __init__(self):
        self.dim = 1
        self.best = None

    def __str__(self):
        return "DummyProblem"

    def __repr__(self):
        return self.__str__()

    def __format__(self, format_spec):
        return str(self)

    def copy(self):
        return DummyProblem()


# -----------------------------
# MAML Metaheuristic
# -----------------------------
class MAMLMetaheuristic(PopulationBasedMetaheuristic):
    """
    Model-Agnostic Meta-Learning (MAML) metaheuristic for few-shot optimization.
    Learns initialization parameters that can be quickly adapted to new tasks.
    """

    def __init__(
        self,
        tasks: Sequence[Callable[[np.ndarray], float]],
        alpha: float = 0.01,
        beta: float = 0.001,
        inner_steps: int = 1,
        outer_steps: int = 1000,
        seed: Optional[int] = None,
    ) -> None:

        # -----------------------------
        # Dummy Problem instance
        # -----------------------------
        problem = DummyProblem()

        # -----------------------------
        # Base class initialization
        # -----------------------------
        super().__init__(
            finish_control=FinishControl(),
            output_control=OutputControl(),
            additional_statistics_control=AdditionalStatisticsControl(),
            problem=problem,
            solution_template=None,
            name="MAMLMetaheuristic",
            random_seed=seed
        )

        # -----------------------------
        # Parameters of MAML algorithm
        # -----------------------------
        self.tasks = list(tasks)
        self.alpha = alpha
        self.beta = beta
        self.inner_steps = inner_steps
        self.outer_steps = outer_steps
        self.theta: Optional[np.ndarray] = None  # global parameters

        if seed is not None:
            np.random.seed(seed)

    # -----------------------------
    # Implement abstract methods
    # -----------------------------
    def init(self) -> None:
        """Initialize global parameters (theta)."""
        if self.theta is None:
            self.theta = np.random.randn(1)  # default 1D, može se promeniti u run(dim)

    def main_loop_iteration(self) -> None:
        """Perform one outer loop iteration over all tasks."""
        if self.theta is None:
            self.init()

        meta_grad = np.zeros_like(self.theta)

        for f in self.tasks:
            theta_i = self.theta.copy()
            # inner loop
            for _ in range(self.inner_steps):
                grad = self._grad(f, theta_i)
                theta_i -= self.alpha * grad
            meta_grad += self._grad(f, theta_i)

        # outer update
        self.theta -= self.beta * meta_grad / len(self.tasks)

        #print(f"After outer iteration: {self}")

    def copy(self) -> MAMLMetaheuristic:
        """Return a shallow copy of this instance."""
        return copy.copy(self)

    def __str__(self) -> str:
        """Lep ispis trenutnog stanja theta."""
        if self.theta is not None:
            theta_str = np.array2string(self.theta, precision=4, floatmode='fixed')
            return f"MAMLMetaheuristic(theta={theta_str})"
        return "MAMLMetaheuristic(theta=None)"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec) -> str:
        return str(self)

    # -----------------------------
    # Helper methods
    # -----------------------------
    def _grad(self, f: Callable[[np.ndarray], float], x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
        """Approximate gradient using finite differences."""
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x1 = x.copy()
            x2 = x.copy()
            x1[i] += eps
            x2[i] -= eps
            grad[i] = (f(x1) - f(x2)) / (2 * eps)
        return grad

    # -----------------------------
    # Run method
    # -----------------------------
    def run(self, dim: int = 1) -> np.ndarray:
        """
        Run MAML metaheuristic optimization.
        Returns learned initialization vector.
        """
        self.theta = np.random.randn(dim)
        theta_history = []

        for _ in range(self.outer_steps):
            self.main_loop_iteration()
            theta_history.append(self.theta.copy())

        return self.theta