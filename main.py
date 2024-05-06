import random 
from generator import *
from minimizer import Minimizer

NUM_PLANS = 50000


if __name__ == "__main__":

	# generate plans

    times_available = [random.randint(3, 5) for i in range(7)]
    max_values = [random.randint(10, 25) for i in range(5)]
    print("max: ", max_values)
    print("times: ", times_available)
    plans = [{"times_available": times_available, "max_values": max_values}]
    for i in range(NUM_PLANS):
        workouts = generate(times_available, max_values, "exercises.json")
        # for workout in workouts:
        #     print(workout)
        # print()
        plans.append(workouts)
    with open('plans.json', 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=4)


    print("====================")

    with open("exercises.json") as f:
        exercises = json.load(f)

	# find the best plan
 
    # expected_values = [random.randint(0, max_values[k]) in range(5)]
    expected_values = [0, 10, 0, 0, 0]

    initial_population = plans[1:]
    minimizer = Minimizer(objective_func=evaluate, initial_population=initial_population, expected_values=expected_values, max_values=max_values, exercises=exercises)

    minimizer.run(gen_count=1000, verbose=1, crossover_rate=0.8, mutation_rate=0.2, early_stop=20)

    best_plan, best_score = minimizer.get()

    print("Best score:", best_score)
    print("Best plan:", best_plan)

    with open('plans.json', 'w', encoding='utf-8') as f:
        json.dump(best_plan, f, ensure_ascii=False, indent=4)

    # print(plans[1])
    # print(plans[2])
    # x, y = crossover(plans[1], plans[2])
    # print(x)
    # print(y)

    # with open("exercises.json") as f:
    #     exercises = json.load(f)

    # print("======================")
    # print(plans[1])
    # print(mutate(plans[1], max_values, exercises))
    # print(json.dumps(mutate(plans[1], max_values, exercises), indent=4))
