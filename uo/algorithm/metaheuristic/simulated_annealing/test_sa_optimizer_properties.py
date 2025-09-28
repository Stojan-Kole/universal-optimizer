import unittest
import unittest.mock as mocker

from uo.problem.problem import Problem
from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.simulated_annealing.sa_optimizer import SaOptimizer
from uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood import SaNeighbourhood
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature import SaTemperature
from uo.solution.solution_void_representation_int import SolutionVoidInt

class TestSaOptimizerProperties(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass TestSaOptimizerProperties\n")

    def setUp(self):
        self.output_control_stub = mocker.MagicMock(spec=OutputControl)

        self.problem_mock = mocker.MagicMock(spec=Problem)
        type(self.problem_mock).name = mocker.PropertyMock(return_value='some_problem')
        type(self.problem_mock).is_minimization = mocker.PropertyMock(return_value=True)
        type(self.problem_mock).file_path = mocker.PropertyMock(return_value='some file path')
        type(self.problem_mock).dimension = mocker.PropertyMock(return_value=42)
        self.problem_mock.copy = mocker.Mock(return_value=self.problem_mock)

        self.sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
        type(self.sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
        self.sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
        type(self.sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")

        self.evaluations_max = 42
        self.iterations_max = 42
        self.seconds_max = 42
        self.finish_control_mock = mocker.MagicMock(spec=FinishControl)
        type(self.finish_control_mock).evaluations_max = mocker.PropertyMock(return_value=self.evaluations_max)
        type(self.finish_control_mock).iterations_max = mocker.PropertyMock(return_value=self.iterations_max)
        type(self.finish_control_mock).seconds_max = mocker.PropertyMock(return_value=self.seconds_max)
        self.finish_control_mock.copy = mocker.Mock(return_value=self.finish_control_mock)

        self.random_seed = 42

        self.sa_optimizer = SaOptimizer(
            sa_neighbourhood=self.sa_neighbourhood_stub,
            sa_temperature=self.sa_temperature_stub,
            finish_control=self.finish_control_mock,
            problem=self.problem_mock,
            solution_template=SolutionVoidInt(43, 0, 0, False),
            output_control=self.output_control_stub,
            random_seed=self.random_seed
        )

    def test_name_should_be_sa(self):
        self.assertEqual(self.sa_optimizer.name, 'sa')

    def test_evaluations_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.finish_control.evaluations_max, self.finish_control_mock.evaluations_max)

    def test_iterations_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.finish_control.iterations_max, self.finish_control_mock.iterations_max)

    def test_random_seed_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.random_seed, self.random_seed)

    def test_seconds_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.finish_control.seconds_max, self.finish_control_mock.seconds_max)

    def test_problem_name_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.problem.name, self.problem_mock.name)

    def test_problem_is_minimization_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.problem.is_minimization, self.problem_mock.is_minimization)

    def test_problem_file_path_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.problem.file_path, self.problem_mock.file_path)

    def test_problem_dimension_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.sa_optimizer.problem.dimension, self.problem_mock.dimension)

    def test_create_with_invalid_problem_type_should_raise_value_exception_with_proper_message(self):
        with self.assertRaises(TypeError) as context:
            problem = "invalid"
            sa_neighbourhood_stub = mocker.MagicMock(spec=SaNeighbourhood)
            type(sa_neighbourhood_stub).copy = mocker.CallableMixin(spec="return self")
            sa_temperature_stub = mocker.MagicMock(spec=SaTemperature)
            type(sa_temperature_stub).copy = mocker.CallableMixin(spec="return self")
            sa_optimizer = SaOptimizer(
                sa_neighbourhood=sa_neighbourhood_stub,
                sa_temperature=sa_temperature_stub,
                finish_control=self.finish_control_mock,
                problem=problem,
                solution_template=SolutionVoidInt(43, 0, 0, False),
                output_control=self.output_control_stub,
                random_seed=self.random_seed
            )
        self.assertEqual("Parameter 'problem' must be 'Problem'.", context.exception.args[0])

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        print("\ntearDownClass TestSaOptimizerProperties")

if __name__ == '__main__':
    unittest.main()