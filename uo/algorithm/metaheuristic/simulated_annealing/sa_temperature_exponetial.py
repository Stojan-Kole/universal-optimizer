""" 
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponentional` module describes the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponentional.SaTemperatureExponentional`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)


from sa_temperature import SaTemperature

class SaTemperatureExponential(SaTemperature):
    def __init__(self, initial_temp: float, decay_factor: float):
        super().__init__(initial_temp)
        if not (0 < decay_factor < 1):
            raise ValueError("Decay factor must be between 0 and 1.")
        self.decay_factor = decay_factor

    def calculate(self, k: int) -> float:
        return self.initial_temperature * (self.decay_factor ** k)