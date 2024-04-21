from enum import Enum
import json
import random
import copy

# aaa
class Skill(Enum):
    cardio = 0
    endurance = 1
    strength = 2
    flexibility = 3
    agility = 4


def generate(times_available, max_values, exercises_filename):
    with open(exercises_filename) as f:
        exercises = json.load(f)

    days = len(times_available)
    workouts = []

    for i in range(days):
        cur_workout = []
        cur_values = [0, 0, 0, 0, 0]
        time_taken = 0
        trials = 0

        while time_taken < times_available[i] and trials < len(exercises):
            exceeds_max = False
            exercise = random.choice(exercises)
            for j, skill in enumerate(Skill):
                if cur_values[j] + exercise[skill.name] > max_values[j]:
                    exceeds_max = True
                    break

            if exceeds_max:
                # print("exceed")
                trials += 1
                continue

            trials = 0
            time_taken += 1
            for j, skill in enumerate(Skill):
                cur_values[j] += exercise[skill.name.lower()]

            cur_workout.append(exercise)

        workouts.append(cur_workout)

    return workouts


"""
Function takes two training plans, crosses them with each other and returns the result
It will perform at least one switch and at most one less than all days, unless the switched day(s) are exactly the same (low probability)
"""
def crossover(weekA, weekB):
    size = len(weekA)

    selector = [1, 0] + [random.randint(0, 1) for _ in range(size-2)]
    random.shuffle(selector)

    weekC = [weekA[i] if selector[i] == 1 else weekB[i] for i in range(size)]
    weekD = [weekA[i] if selector[i] == 0 else weekB[i] for i in range(size)]

    return weekC, weekD


"""
Function mutates at most one training at least in one day
It takes a training plan, a list of max values and a list of exercises
"""
def mutate(week, max_values, exercises):
    week = copy.deepcopy(week)
    size = len(week)
    selector = [1] + [random.randint(0, 1) for _ in range(size - 1)]
    counter = 0
    for i in range(size):
        if selector[i] == 0:
            continue
        # current category values
        cur_values = [sum(exercise[skill.name.lower()] for exercise in week[i]) for skill in Skill]

        # random order of exercises in a day
        order = [i for i in range(len(week[i]))]
        random.shuffle(order)

        for j in order:
            exceeds_max = False
            exercise = random.choice(exercises)
            for k, skill in enumerate(Skill):
                if cur_values[k] + exercise[skill.name] - week[i][j][skill.name] > max_values[k]:
                    exceeds_max = True
                    break
            if not exceeds_max:
                week[i][j] = exercise
                counter += 1
                break
    return week


def evaluate(week, exercises, max_values):
	n = len(Skill)
	m = len(exercises)
	p = 7

	value = 0
	for i in range(n):
		for j in range(m):
			for k in range(p):
				a = 1 if exercises[j] in week[k] else 0
				v = list(exercises[j].values())[i+1]
				x = max_values[i]

				value += abs(a * v - x)
	
	return value
