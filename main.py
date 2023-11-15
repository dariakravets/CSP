import random
from dataclasses import dataclass

POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GENERATIONS = 100

CLASSES = ['TPR', 'DPS', 'IT', 'IS', 'AI', 'MPO']
ROOMS = ['Room 1', 'Room 2', 'Room 3']
GROUPS = ['TK-41', 'TK-42', 'TTP-41', 'TTP-42', 'MI-4']
CLASSES_PER_DAY = 4


@dataclass
class Class:
    name: str
    room: str
    group: str
    timeslot: int


def generate_schedule():
    schedule = []
    for group in GROUPS:
        for _ in range(CLASSES_PER_DAY):
            random_class = Class(
                name=random.choice(CLASSES),
                room=random.choice(ROOMS),
                group=group,
                timeslot=0
            )
            schedule.append(random_class)
    return schedule


def fitness(schedule):
    conflicts = 0
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if schedule[i].timeslot == schedule[j].timeslot and schedule[i].room == schedule[j].room:
                conflicts += 1
    return conflicts


def mutate(schedule):
    mutated_schedule = schedule.copy()
    random_class_index = random.randint(0, len(mutated_schedule) - 1)
    mutated_schedule[random_class_index].timeslot = random.randint(0, CLASSES_PER_DAY - 1)
    return mutated_schedule


def crossover(parent1, parent2):
    split_point = random.randint(1, len(parent1) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child


def genetic_algorithm():
    population = [generate_schedule() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        fitness_scores = [fitness(schedule) for schedule in population]

        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])
        selected_indices = sorted_indices[:int(0.5 * POPULATION_SIZE)]
        selected_population = [population[i] for i in selected_indices]

        new_population = selected_population.copy()

        while len(new_population) < POPULATION_SIZE:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)

            child = crossover(parent1, parent2)

            if random.random() < MUTATION_RATE:
                child = mutate(child)

            new_population.append(child)

        population = new_population

        best_schedule_index = min(range(len(population)), key=lambda k: fitness_scores[k])
        best_fitness = fitness_scores[best_schedule_index]
        print(f"Iteration {generation + 1}/{GENERATIONS} - Best Fitness: {best_fitness}")

    best_schedule_index = min(range(len(population)), key=lambda k: fitness_scores[k])
    best_schedule = population[best_schedule_index]

    return best_schedule


best_schedule = genetic_algorithm()

print("\nBest Schedule:")
for class_obj in best_schedule:
    print(f"{class_obj.group} - {class_obj.name} - {class_obj.room} - Timeslot {class_obj.timeslot}")
