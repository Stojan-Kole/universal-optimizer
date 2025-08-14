""" 
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature` module describes the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature.SaTemperature`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from abc import ABCMeta, abstractmethod

class SaTemperature( metaclass=ABCMeta):
    
    def __init__(self, initial_temp: float):
        if not (0 <= initial_temp <= 1):
            raise ValueError("Initial temperature must be between 0 and 1.")
        self.initial_temperature = initial_temp
    
    @abstractmethod
    def calculate(k: int)->float:
        """
        Calculate the temperature or probability of accepting a worse solution.
        
        The temperature function typically decreases as the number of iterations (k) increases,
        lowering the likelihood of accepting worse solutions as the algorithm converges.

        :param int k: Current iteration on the Simulated Annealing algorithm
        :return: Probability of taking worse solution. Number in range [0,1]
        :rtype: float
        :raises NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError