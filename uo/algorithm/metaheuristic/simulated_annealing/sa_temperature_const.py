""" 
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_const` module describes the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_const.SaTemperatureConst`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from sa_temperature import SaTemperature

class SaTemperatureConst(SaTemperature):
    def calculate(self, k: int) -> float:
        return self.initial_temperature
