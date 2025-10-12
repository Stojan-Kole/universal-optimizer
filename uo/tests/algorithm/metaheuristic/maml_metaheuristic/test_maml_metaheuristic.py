import unittest
import numpy as np
import matplotlib.pyplot as plt

from uo.algorithm.metaheuristic.maml_metaheuristic.maml_metaheuristic import MAMLMetaheuristic

def quadratic_task1(x: np.ndarray) -> float:
    return float((x[0] - 1.0) ** 2)

def quadratic_task2(x: np.ndarray) -> float:
    return float((x[0] + 2.0) ** 2)

def quadratic_task3(x: np.ndarray) -> float:
    return float((x[0] - 0.5) ** 2)

def quadratic_task4(x: np.ndarray) -> float:
    return float(2.0 * (x[0] - 3.0) ** 2 + 1.0)

def linear_task(x: np.ndarray) -> float:
    return float(2.0 * x[0] + 1.0)

def abs_task(x: np.ndarray) -> float:
    return float(np.abs(x[0] - 1.5))

def sinus_task(x: np.ndarray) -> float:
    return float(np.sin(x[0]))

def multidim_quadratic_task(x: np.ndarray) -> float:
    if x.shape[0] < 2:
        return (x[0] - 1.0) ** 2
    return (x[0] - 1.0) ** 2 + (x[1] + 1.0) ** 2


class TestMAMLMetaheuristicNumeric(unittest.TestCase):
    def test_maml_various_tasks(self):

        tasks = [quadratic_task4, linear_task, abs_task, sinus_task]

        maml = MAMLMetaheuristic(
            tasks=tasks,
            alpha=0.1,
            beta=0.01,
            inner_steps=1,
            outer_steps=150,
            seed=123
        )

        def evaluate_tasks(maml, tasks):
            values = []
            for f in tasks:
                theta_i = maml.theta.copy()
                for _ in range(maml.inner_steps):
                    theta_i -= maml.alpha * maml._grad(f, theta_i)
                values.append(f(theta_i))
            return values

        errors_history = []
        for _ in range(maml.outer_steps):
            maml.main_loop_iteration()
            errors_history.append(evaluate_tasks(maml, tasks))

        errors_history = np.array(errors_history)
        avg_errors = errors_history.mean(axis=1)
        self.assertTrue(
            avg_errors[-1] < avg_errors[0],
            msg="Average error has not decreased!"
        )
        print(f"Test with various functions has passed! Starting error: {avg_errors[0]:.4f}, Final error: {avg_errors[-1]:.4f}")

    def test_maml_quadratic_tasks_numeric(self):
        tasks = [quadratic_task1, quadratic_task2, quadratic_task3]

        # -----------------------------
        # MAML init
        # -----------------------------
        maml = MAMLMetaheuristic(
            tasks=tasks,
            alpha=0.1,
            beta=0.01,
            inner_steps=1,
            outer_steps=200, 
            seed=42
        )

        # -----------------------------
        # Evaluation
        # -----------------------------
        def evaluate_tasks(maml, tasks):
            values = []
            for f in tasks:
                theta_i = maml.theta.copy()
                for _ in range(maml.inner_steps):
                    theta_i -= maml.alpha * maml._grad(f, theta_i)
                values.append(f(theta_i))
            return values

        theta_history = []
        errors_history = []

        for _ in range(maml.outer_steps):
            maml.main_loop_iteration()
            theta_history.append(maml.theta.copy())
            errors_history.append(evaluate_tasks(maml, tasks))

        theta_history = np.array(theta_history)
        errors_history = np.array(errors_history)

        final_theta = maml.theta[0]
        expected_theta = np.mean([1.0, -2.0, 0.5])  # ≈ -0.1667
        self.assertAlmostEqual(
            final_theta,
            expected_theta,
            delta=0.15,
            msg=f"Final θ={final_theta} is not close enough to {expected_theta}"
            
        )

        print(f"\nTest passed! Final θ={final_theta}, expected θ≈{expected_theta}")

        avg_errors = errors_history.mean(axis=1)
        self.assertTrue(
            avg_errors[-1] < avg_errors[0],
            msg="Average error has not decreased!"
        )
        print(f"Average error has decreased from {avg_errors[0]:.4f} to {avg_errors[-1]:.4f}")






if __name__ == "__main__":
    unittest.main()