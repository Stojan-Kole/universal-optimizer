""" 
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_linear` module describes the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_linear.SaTemperatureLinear`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from sa_temperature import SaTemperature

class SaTemperatureLinear(SaTemperature):
    def __init__(self, initial_temp: float, decay_rate: float):
        super().__init__(initial_temp)
        self.decay_rate = decay_rate

    def calculate(self, k: int) -> float:
        return max(0, self.initial_temperature - self.decay_rate * k)