..  _Algorithm_Simulated_Annealing:

Simulated Annealing
============================

Basic information 
-----------------

Simulated Annealing (SA) is a probabilistic metaheuristic inspired by the annealing process in metallurgy. It is used for finding an approximate global optimum of a given function in a large search space. The algorithm explores the solution space by probabilistically accepting not only improvements but also, with a certain probability, worse solutions. This allows it to escape local optima and increases the chance of finding a global optimum.

The probability of accepting worse solutions decreases over time, controlled by a "temperature" parameter that is gradually reduced according to a cooling schedule.

Structure of the algorithm
--------------------------

The main steps in Simulated Annealing are:

1. **Initialization**: Start with an initial solution and set the initial temperature.
2. **Main Loop**:
   - Generate a neighbor solution using a neighborhood structure.
   - Evaluate the neighbor solution.
   - If the neighbor is better than the current solution, accept it.
   - If the neighbor is worse, accept it with a probability that depends on the temperature and the difference in solution quality.
   - Update the temperature according to the cooling schedule.
3. **Termination**: The algorithm stops when a stopping criterion is met (e.g., maximum number of iterations, time limit, or temperature threshold).

Implementation notes
--------------------

Implementation of this optimization method is given within the class :ref:`SaOptimizer<py_sa_optimizer>`.

- **Neighborhoods**: The neighborhood structure is defined by subclasses of :class:`SaNeighbourhood`, such as :class:`SaNeighbourhoodInt` for integer-encoded solutions and :class:`SaNeighbourhoodBitArray` for bit array-encoded solutions.
- **Temperature Schedules**: Several temperature schedules are available, including constant, linear, and exponential decay, implemented in classes such as :class:`SaTemperatureConst`, :class:`SaTemperatureLinear`, and :class:`SaTemperatureExponential`.
- **Extensibility**: You can implement custom neighborhoods or temperature schedules by subclassing the appropriate base classes.
- **Usage**: To use the SA optimizer, construct an instance of :class:`SaOptimizer` with the desired neighborhood, temperature schedule, problem, and other parameters.

References
----------

.. [Kirkpatrick1983] Kirkpatrick, S.; Gelatt, C. D.; Vecchi, M. P. (1983). "Optimization by Simulated Annealing". Science. 220 (4598): 671–680. doi:10.1126/science.220.4598.671.

.. [Aarts1988] Aarts, E.; Korst, J. (1988). "Simulated Annealing and Boltzmann Machines". Wiley.

.. [BurKen2005] Burke, EK.; Kendall, G. (2005). Burke, Edmund K; Kendall, Graham (eds.). Search methodologies. Introductory tutorials in optimization and decision support techniques. Springer. doi:10.1007/978-1-4614-6940-7. ISBN 978-1-4614-6939-1.

