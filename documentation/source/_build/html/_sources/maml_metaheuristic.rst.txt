MAML Metaheuristic
===================

.. _maml_algorithm_page:

The **Model-Agnostic Meta-Learning (MAML)** metaheuristic learns reusable
initialization parameters (``theta``) that can be quickly adapted to new
optimization tasks. It is useful in few-shot optimization where each task has
limited data.

Main idea
---------

- Use a set of training tasks (objective functions).
- For each task perform a small number of inner-loop gradient steps starting
  from a shared initialization ``theta``.
- Accumulate the meta-gradient across tasks and update ``theta`` in the outer
  loop.

Parameters
----------

- ``alpha``: inner-loop learning rate
- ``beta``: outer-loop learning rate
- ``inner_steps``: number of gradient steps per task
- ``outer_steps``: number of meta-iterations

Usage example
-------------

.. code-block:: python

   from uo.algorithm.metaheuristic.maml_metaheuristic.maml_metaheuristic import MAMLMetaheuristic
   import numpy as np

   def task1(x: np.ndarray) -> float:
       return float(np.sum((x - 3.0) ** 2))

   def task2(x: np.ndarray) -> float:
       return float(np.sum((x + 5.0) ** 2))

   maml = MAMLMetaheuristic(tasks=[task1, task2], alpha=0.1, beta=0.01, inner_steps=1, outer_steps=10)
   theta = maml.run(dim=1)
   print(theta)

Notes
-----

The implementation uses numerical finite-difference gradients by default; if
your tasks provide analytic gradients, prefer using them for better stability.
