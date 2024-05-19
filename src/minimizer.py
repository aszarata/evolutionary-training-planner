import random
from src.generator import mutate, crossover

class Minimizer:
	
	def __init__(self, objective_func, initial_population, expected_values, max_values, exercises):
		"""
        Initialize the Minimizer object.
        Args:
            objective_func: The objective function to minimize.
            initial_population: The initial population of individuals.
            expected_values: The expected values for evaluation.
            max_values: The maximum values for individuals.
            exercises: The exercises data.
        """

		self.objective_func = objective_func
		
		self.expected_values = expected_values
		self.max_values = max_values
		self.exercises = exercises  

		self.population = initial_population
		self.__population_size = len(initial_population)
		self.__evaluations = [] 
		
		self.__best_score_history = []
		self.best_x = None
		self.best_score = 10**10

		self.no_change_cnt = 0
	
	def run(self, gen_count, mutation_rate=0.3, crossover_rate=0.95, verbose=-1, early_stop=None):
		"""
        Run the minimization process.
        Args:
            gen_count: The number of generations to run.
            mutation_rate: The mutation rate.
            crossover_rate: The crossover rate.
            verbose: Verbosity level (-1 for no output, 0 for every generation, 1 for every 10 generations, and so on).
            early_stop: Number of generations with no improvement to trigger early stopping.
        """

		for step in range(gen_count):
			# evaluate individuals
			self.__evaluations = self.__individuals_evaluation()


			# choose the parents in tournament
			parents = []
			for _ in range(self.__population_size):
				i1 = random.randint(0, self.__population_size-1)
				i2 = random.randint(0, self.__population_size-1)


				if self.__evaluations[i1] < self.__evaluations[i2]:
					parents.append(self.population[i1])

				else:
					parents.append(self.population[i2])


			# crossover
			new_population = []
			for i in range(0, self.__population_size, 2):
				if random.random() < crossover_rate:
					individual1, individual2 = crossover(parents[i], parents[i+1])
					new_population += [individual1, individual2]
				
			# mutations
			for i in range(len(new_population)):
				if random.random() < mutation_rate:
					new_population[i] = mutate(new_population[i], max_values=self.max_values, exercises=self.exercises)

			# replace weakest individuals with new population
			self.population = [self.population[i] for i in sorted(range(len(self.__evaluations)), key=lambda x: self.__evaluations[x], reverse=False)]
			self.population = new_population + self.population[len(new_population):]

			

			best_idx = self.__find_best_score()

			best_x = self.population[best_idx]
			best_score = self.__evaluations[best_idx]
			
			self.__update_best_score(best_x, best_score)

			self.__best_score_history.append(best_score)

			if verbose != -1 and step % 10**verbose==0:
				print(f"Step {step}: {best_score}")

			if early_stop != None and early_stop < self.no_change_cnt:
				break
			
				

	def get(self):
		"""
        Get the best individual and its score.
        Returns:
            best_x: The best individual.
            best_score: The best score achieved.
        """
		return self.best_x, self.best_score

	def get_history(self):
		"""
        Get the history of best scores during the minimization process.
        Returns:
            list: A list containing the history of best scores.
        """
		return self.__best_score_history

	def __update_best_score(self, new_best_x, new_best_score):
		"""
        Update the best score and best individual.
        Args:
            new_best_x: The new best individual.
            new_best_score: The new best score.
        """

		self.no_change_cnt += 1
		if new_best_score < self.best_score:
			self.best_score, self.best_x = new_best_score, new_best_x
			self.no_change_cnt = 0

	def __find_best_score(self):
		"""
        Find the index of the individual with the best score.
        Returns:
            int: The index of the individual with the best score.
        """

		best_idx = min(range(self.__population_size), key=lambda x: self.__evaluations[x])
		return best_idx
		
	def __individuals_evaluation(self):
		"""
        Evaluate all individuals in the population using the objective function.
        Returns:
            list: A list containing the scores of all individuals.
        """
		
		return [self.objective_func(individual, self.exercises, self.expected_values) for individual in self.population]



