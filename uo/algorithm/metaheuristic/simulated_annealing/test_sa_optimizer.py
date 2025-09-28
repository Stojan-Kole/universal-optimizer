import unittest
import unittest.mock as mocker
from datetime import datetime

from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl
from uo.problem.problem import Problem
from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.simulated_annealing.sa_optimizer import SaOptimizer
from uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood import SaNeighbourhood
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature import SaTemperature
from uo.problem.problem_void_min_so import ProblemVoidMinSO
from uo.solution.solution_void_representation_int import SolutionVoidInt

class TestSaOptimizer(unittest.TestCase):

    def test_sa_optimizer_initialized_with_valid_parameters(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        # Act
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        # Assert
        self.assertIsInstance(sa_optimizer, SaOptimizer)

    def test_sa_optimizer_initialized_with_none_solution_template(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 0, 0, False)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        self.assertIsInstance(sa_optimizer, SaOptimizer)

    def test_sa_optimizer_initialized_with_none_random_seed(self):
        finish_control = FinishControl()
        random_seed = None
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 0, 0, False)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        self.assertIsInstance(sa_optimizer, SaOptimizer)

    def test_sa_optimizer_initialized_without_sa_neighbourhood(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = None
        sa_neighbourhood = None
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

    def test_sa_optimizer_initialized_without_sa_temperature(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = None
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature = None
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

    def test_sa_optimizer_init(self):
        finish_control = FinishControl()
        random_seed = None
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        sa_optimizer.execution_started = datetime.now()
        sa_optimizer.init()
        self.assertEqual(sa_optimizer.evaluation, 1)

    def test_string_rep(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_neighbourhood_stub).string_rep = mocker.Mock(return_value="")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_temperature_stub).string_rep = mocker.Mock(return_value="")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        string_representation = sa_optimizer.string_rep('|')
        self.assertIn("name=sa|", string_representation)
        self.assertIn("|finish_control=", string_representation)
        self.assertIn("|random_seed=123|", string_representation)
        self.assertIn("|additional_statistics_control=", string_representation)
        self.assertIn("|problem=", string_representation)
        self.assertIn("|current_solution=", string_representation)
        self.assertIn("|__sa_temperature=", string_representation)
        self.assertIn("|__sa_neighbourhood=", string_representation)

    def test_str(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_neighbourhood_stub).string_rep = mocker.Mock(return_value="")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_temperature_stub).string_rep = mocker.Mock(return_value="")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        string_representation = str(sa_optimizer)
        self.assertIn("name=sa|", string_representation)
        self.assertIn("|finish_control=", string_representation)
        self.assertIn("|random_seed=123|", string_representation)
        self.assertIn("|additional_statistics_control=", string_representation)
        self.assertIn("|problem=", string_representation)
        self.assertIn("|current_solution=", string_representation)
        self.assertIn("|__sa_temperature=", string_representation)
        self.assertIn("|__sa_neighbourhood=", string_representation)

    def test_repr_method(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_neighbourhood_stub).string_rep = mocker.Mock(return_value="")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        type(sa_temperature_stub).string_rep = mocker.Mock(return_value="")
        sa_optimizer = SaOptimizer(
            sa_neighbourhood=sa_neighbourhood_stub,
            sa_temperature=sa_temperature_stub,
            finish_control=finish_control,
            problem=problem,
            solution_template=solution_template,
            output_control=None,
            random_seed=random_seed
        )
        repr_string = repr(sa_optimizer)
        self.assertIsInstance(repr_string, str)
        self.assertIn("name=", repr_string)
        self.assertIn("finish_control=", repr_string)
        self.assertIn("random_seed=123", repr_string)
        self.assertIn("additional_statistics_control=", repr_string)
        self.assertIn("problem=", repr_string)
        self.assertIn("current_solution=", repr_string)
        self.assertIn("__sa_temperature=", repr_string)
        self.assertIn("__sa_neighbourhood=", repr_string)

    def test_finish_control_type_error(self):
        finish_control = "not a FinishControl"
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

    def test_random_seed_type_error(self):
        finish_control = FinishControl()
        random_seed = "not an int"
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

    def test_additional_statistics_control_type_error(self):
        finish_control = FinishControl()
        random_seed = 123
        additional_statistics_control = "not a valid type"
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed,
                additional_statistics_control=additional_statistics_control
            )

    def test_solution_template_parameter_type_error(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = ProblemVoidMinSO("a problem", True)
        solution_template = "not a Solution"
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

    def test_problem_parameter_type_error(self):
        finish_control = FinishControl()
        random_seed = 123
        problem = "not a Problem"
        solution_template = SolutionVoidInt(43, 43, 43, True)
        sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
        with self.assertRaises(TypeError):
            SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                output_control=None,
                random_seed=random_seed
            )

if __name__ == '__main__':
    unittest.main()