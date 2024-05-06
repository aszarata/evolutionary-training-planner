import random
from generator import mutate, crossover

class Minimizer:
	
	def __init__(self, objective_func, initial_population, expected_values, max_values, exercises):
		
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
	
	def run(self, gen_count, mutation_rate=0.1, crossover_rate=0.8, verbose=-1, early_stop=None):

		for step in range(gen_count):
			# evaluate individuals
			self.__evaluations = self.__individuals_evaluation()

			
			# mutations
			for i in range(self.__population_size):
				if random.random() < mutation_rate:
					self.population[i] = mutate(self.population[i], max_values=self.max_values, exercises=self.exercises)

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
			
			for i in range(0, self.__population_size, 2):
				if random.random() < crossover_rate:
					self.population[i], self.population[i+1] = crossover(parents[i], parents[i+1])

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
		return self.best_x, self.best_score

	def get_history(self):
		return self.__best_score_history

	def __update_best_score(self, new_best_x, new_best_score):
		self.no_change_cnt += 1
		if new_best_score < self.best_score:
			self.best_score, self.best_x = new_best_score, new_best_x
			self.no_change_cnt = 0

	def __find_best_score(self):
		best_idx = min(range(self.__population_size), key=lambda x: self.__evaluations[x])
		return best_idx
		
	def __individuals_evaluation(self):
		return [self.objective_func(individual, self.exercises, self.expected_values) for individual in self.population]



