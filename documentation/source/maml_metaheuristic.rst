MAML Metaheuristic
===================

.. _maml_algorithm_page:

The **Model-Agnostic Meta-Learning (MAML)** metaheuristic is an optimization algorithm
designed to learn good initial parameters (`theta`) that can be quickly adapted to solve new tasks.

This algorithm is especially useful in **few-shot optimization** settings, where data is limited.

**Main Idea**:
- Use a set of training tasks (objective functions)
- Perform inner gradient steps on each task
- Accumulate meta-gradient across tasks
- Update the shared parameters (`theta`) via outer loop

**Parameters**:
- `alpha`: Inner loop learning rate
- `beta`: Outer loop learning rate
- `inner_steps`: Number of gradient steps per task
- `outer_steps`: Total meta-iterations

**Code Reference**:
- :class:`uo.algorithm.metaheuristic.maml_metaheuristic.MAMLMetaheuristic`

**Usage Example**:

.. code-block:: python

   from uo.algorithm.metaheuristic.maml_metaheuristic import MAMLMetaheuristic

   def task1(x): return (x[0] - 3) ** 2
   def task2(x): return (x[0] + 5) ** 2

   maml = MAMLMetaheuristic(tasks=[task1, task2])
   result = maml.run(dim=1)
   print(result)

.. note::

   This algorithm requires tasks to be differentiable (at least numerically).
