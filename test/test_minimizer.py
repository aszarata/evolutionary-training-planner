import sys
import os, shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
import json
import random
import os
import matplotlib.pyplot as plt
from src.generator import generate, evaluate
from src.minimizer import Minimizer

exercises_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'exercises.json'))
output_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'outputs'))

class TestMinimizer(unittest.TestCase):

    def setUp(self):
        """
        Set up common data for tests.
        """
        self.times_available = [random.randint(3, 5) for _ in range(7)]
        self.max_values = [random.randint(10, 25) for _ in range(5)]
        
        self.basic_values = [5, 10, 10, 15, 30]
        self.zeros_values = [0, 0, 0, 0, 0]
        self.one_skill = [30, 0, 0, 0, 0]

        # Generate initial population
        self.plans = [{"times_available": self.times_available, "max_values": self.max_values}]
        for _ in range(20):
            workouts = generate(self.times_available, self.max_values, exercises_file_path)
            self.plans.append(workouts)

        with open(exercises_file_path) as f:
            self.exercises = json.load(f)


    def test_minimizer_basic(self):
        """
        Test basic functionality of the minimizer.
        """
        minimizer = Minimizer(
            objective_func=evaluate,
            initial_population=self.plans[1:],
            expected_values=self.basic_values,
            max_values=self.max_values,
            exercises=self.exercises
        )
        minimizer.run(gen_count=1000)
        best_plan, best_score = minimizer.get()
        history = minimizer.get_history()

        # Check if best score is a number and not None
        self.assertIsNotNone(best_score)
        self.assertIsInstance(best_score, (int, float))


    def __run_different_params(self, expected_values, dir_name):
        """
        Run minimizer with different parameters and save results and plots.
        Args:
            expected_values: The expected values for evaluation.
            dir_name: The name of the directory to save results and plots.
        """
        results = []
        history = []

        for mutation_rate in [0.1, 0.3, 0.7, 0.9, 0.95]:
            for crossover_rate in [0.6, 0.8, 0.95]:
                print(f"Testing: mutation_rate = {mutation_rate}; crossover_rate = {crossover_rate}")
                minimizer = Minimizer(
                    objective_func=evaluate,
                    initial_population=self.plans[1:],
                    expected_values=expected_values,
                    max_values=self.max_values,
                    exercises=self.exercises
                )
                minimizer.run(gen_count=10000, crossover_rate=crossover_rate, mutation_rate=mutation_rate, early_stop=500)
                best_plan, best_score = minimizer.get()
                results.append((mutation_rate, crossover_rate, best_score))
                history.append(minimizer.get_history())


        print("\n----------------------------------------------------------------------")
        
        for mutation_rate, crossover_rate, best_score in results:
            print(f"Mutation rate: {mutation_rate}, Crossover rate: {crossover_rate}, Best score: {best_score}")
        
        print("--------------------------------------------------------\n")

        self.__save_results_and_plots(results, history, dir_name)


    def test_minimizer_different_params_basic_values(self):
        """
        Test minimizer with different parameters using basic values.
        """
        self.__run_different_params(expected_values=self.basic_values, dir_name='basic_values')
        
    
    def test_minimizer_different_params_zeros(self):
        """
        Test minimizer with different parameters using zero values.
        """
        self.__run_different_params(expected_values=self.zeros_values, dir_name='zeros')

    
    def test_minimizer_different_params_one_skill(self):
        """
        Test minimizer with different parameters using only one skill.
        """
        self.__run_different_params(expected_values=self.one_skill, dir_name='one_skill')


    def test_minimizer_early_stopping(self):
        """
        Test minimizer with early stopping mechanism.
        """

        minimizer = Minimizer(
            objective_func=evaluate,
            initial_population=self.plans[1:],
            expected_values=self.basic_values,
            max_values=self.max_values,
            exercises=self.exercises
        )
        minimizer.run(gen_count=10000, crossover_rate=0.95, mutation_rate=0.2, early_stop=50)
        best_plan, best_score = minimizer.get()
        history = minimizer.get_history()

        # Check if best_score is a number and not None
        self.assertIsNotNone(best_score)
        self.assertIsInstance(best_score, (int, float))

    def __save_results_and_plots(self, results, history, dirname):
        """
        Save results and plots to files.
        Args:
            results: The results of minimization.
            history: The history of scores during minimization.
            dirname: The name of the directory to save results and plots.
        """

        output_dir = os.path.join(output_dir_path, dirname)
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

        for i, (mutation_rate, crossover_rate, best_score) in enumerate(results):
            # Save results to file
            with open(f'{output_dir}/results', 'a') as f:
                f.write(f"Mutation rate: {mutation_rate}, Crossover rate: {crossover_rate}, Best score: {best_score}\n")

            # Generate and save plot
            generations = range(len(history[i]))
            plt.plot(generations, history[i])
            plt.xlabel('Generation')
            plt.ylabel('Best Score')
            plt.title(f'Convergence of Minimizer (Mutation rate: {mutation_rate}, Crossover rate: {crossover_rate})')

            plt.savefig(f'{output_dir}/convergence_plot_{mutation_rate}_{crossover_rate}.png')
            plt.close()

if __name__ == '__main__':
    if os.path.exists(output_dir_path):
        shutil.rmtree(output_dir_path)
    unittest.main()

