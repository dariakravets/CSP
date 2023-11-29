import random

classes = ["Linear Algebra", "Analytic Geometry", "Discrete mathematics", "Basics of Programming",
           "Object-oriented Programming", "Mathematical Analysis", "Theory of Probability", "Statistics",
           "Data Analysis", "Introduction to AI"]

teachers_classes = {
    "Mr. Smith": {
        "max_hours": 20,
        "preferences": {
            "Linear Algebra": ["8:40-10:15", "10:35-12:10"],
            "Analytic Geometry": ["12:20-13:55"]
        }
    },
    "Mrs. Geller": {
        "max_hours": 10,
        "preferences": {
            "Discrete mathematics": ["8:40-10:15"]
        }
    },
    "Mr. Cooper": {
        "max_hours": 30,
        "preferences": {
            "Basics of Programming": ["10:35-12:10"],
            "Object-oriented Programming": ["14:05-15:40"]
        }
    },
    "Mrs. White": {
        "max_hours": 15,
        "preferences": {
            "Mathematical Analysis": ["8:40-10:15"]
        }
    },
    "Mr. Hawkins": {
        "max_hours": 20,
        "preferences": {
            "Theory of Probability": ["12:20-13:55"],
            "Statistics": ["14:05-15:40"]
        }
    },
    "Mrs. Tucker": {
        "max_hours": 30,
        "preferences": {
            "Data Analysis": ["10:35-12:10"],
            "Introduction to AI": ["8:40-10:15", "14:05-15:40"]
        }
    },
}


groups = ["K-1", "K-2", "K-3", "K-4", "K-5"]
class_hours = {
    "Linear Algebra": 1, "Analytic Geometry": 2, "Discrete mathematics": 2,
    "Basics of Programming": 2, "Object-oriented Programming": 2,
    "Mathematical Analysis": 2, "Theory of Probability": 2,
    "Statistics": 2, "Data Analysis": 2, "Introduction to AI": 1
}

timeslots = ["8:40-10:15", "10:35-12:10", "12:20-13:55", "14:05-15:40"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


population_size = 100
generations = 200
mutation_rate = 0.2
crossover_rate = 0.7


def generate_schedule_1():
    schedule = {}

    for day in days_of_week:
        schedule[day] = {}

        for timeslot in timeslots:
            schedule[day][timeslot] = {}

            for teacher, info in teachers_classes.items():
                max_hours = info["max_hours"]
                preferences = info.get("preferences", {})

                if max_hours > 0:
                    available_classes = [
                        class_name
                        for class_name, class_preferences in preferences.items()
                        if class_preferences and timeslot in class_preferences
                    ]

                    if available_classes:
                        class_name = random.choice(available_classes)
                        schedule[day][timeslot][teacher] = {
                            "class": class_name,
                            "group": random.choice(groups),
                        }
                        max_hours -= 1
                    else:
                        class_name = random.choice(list(preferences.keys()))
                        schedule[day][timeslot][teacher] = {
                            "class": class_name,
                            "group": random.choice(groups),
                        }
                        max_hours -= 1

    return schedule


def generate_schedule_2():
    schedule = {}

    for day in days_of_week:
        schedule[day] = {}

        for timeslot in timeslots:
            schedule[day][timeslot] = {}

            for teacher, info in teachers_classes.items():
                max_hours = info["max_hours"]
                available_classes = list(teachers_classes[teacher]["preferences"].keys())

                if max_hours > 0 and available_classes:
                    class_name = random.choice(available_classes)
                    schedule[day][timeslot][teacher] = {
                        "class": class_name,
                        "group": random.choice(groups),
                    }
                    max_hours -= class_hours[class_name]

    return schedule


def crossover(parent1, parent2):
    child = parent1.copy()

    point1, point2 = sorted(random.sample(range(len(parent1)), 2))

    for day in days_of_week:
        for timeslot in timeslots[point1:point2]:
            for teacher in teachers_classes.keys():
                child[day][timeslot][teacher] = {
                    "class": parent2[day][timeslot][teacher]["class"],
                    "group": parent2[day][timeslot][teacher]["group"],
                }

    return child


def mutate(schedule):
    mutated_schedule = schedule.copy()

    day = random.choice(days_of_week)
    timeslot = random.choice(timeslots)
    teacher = random.choice(list(teachers_classes.keys()))

    class_name = mutated_schedule[day][timeslot][teacher]["class"]
    group = mutated_schedule[day][timeslot][teacher]["group"]

    max_hours = teachers_classes[teacher]["max_hours"]
    preferences = teachers_classes[teacher].get("preferences", {})

    if max_hours > 0:
        available_classes = [
            c for c, class_preferences in preferences.items() if class_preferences and timeslot in class_preferences
        ]

        if available_classes:
            new_class = random.choice(available_classes)
        else:
            new_class = random.choice(list(preferences.keys()))

        mutated_schedule[day][timeslot][teacher] = {
            "class": new_class,
            "group": group,
        }

    return mutated_schedule


def calculate_fitness(schedule):
    max_classes_per_week = {teacher: teachers_classes[teacher]["max_hours"] for teacher in teachers_classes}

    teacher_classes_count = {teacher: 0 for teacher in teachers_classes}
    group_class_count = {group: {cls: 0 for cls in class_hours} for group in groups}
    conflicts = 0

    for day in days_of_week:
        for timeslot in timeslots:
            for teacher, info in schedule[day][timeslot].items():
                class_name = info["class"]
                group = info["group"]

                # Teacher Time Preference Constraint
                if (
                    "preferences" in teachers_classes[teacher]
                    and class_name in teachers_classes[teacher]["preferences"]
                    and timeslot not in teachers_classes[teacher]["preferences"][class_name]
                ):
                    conflicts += 1

                # Teacher Load Constraint
                teacher_classes_count[teacher] += 1
                if teacher_classes_count[teacher] > max_classes_per_week[teacher]:
                    conflicts += 1

                # Class Load Balancing Constraint for Student Groups
                if class_hours[class_name] > 0:
                    group_class_count[group][class_name] += class_hours[class_name]
                    if group_class_count[group][class_name] > class_hours[class_name]:
                        conflicts += 1

    fitness = conflicts + sum(teacher_classes_count.values())
    return fitness


def class_availability_heuristic(schedule):
    conflicts = 0

    for day in days_of_week:
        for timeslot in timeslots:
            for teacher, info in schedule[day][timeslot].items():
                class_name = info["class"]

                # Penalize if a class is scheduled during non-preferred time slots
                if "preferences" in teachers_classes[teacher] and class_name in teachers_classes[teacher]["preferences"] and timeslot not in teachers_classes[teacher]["preferences"][class_name]:
                    conflicts += 1

                # Add more conditions based on your specific class availability heuristic

    return conflicts


def teacher_group_compatibility_heuristic(schedule):
    conflicts = 0

    for day in days_of_week:
        for timeslot in timeslots:
            for teacher, info in schedule[day][timeslot].items():
                group = info["group"]

                # Penalize if a teacher is assigned to a non-preferred group
                if "group_preferences" in teachers_classes[teacher] and group not in teachers_classes[teacher]["group_preferences"]:
                    conflicts += 1

                # Add more conditions based on your specific teacher-group compatibility heuristic

    return conflicts


def total_fitness(schedule):
    primary_fitness = calculate_fitness(schedule)
    heuristic_fitness = class_availability_heuristic(schedule) + teacher_group_compatibility_heuristic(schedule)

    # Weighted combination of primary fitness and heuristics (adjust weights as needed)
    fitness = primary_fitness + 0.1 * heuristic_fitness

    return fitness


def genetic_algorithm_with_heuristics():
    population = []

    # Generate the first half of the population with the original function
    population += [generate_schedule_1() for _ in range(population_size // 2)]

    # Generate the second half of the population with the new smart function
    population += [generate_schedule_2() for _ in range(population_size // 2)]

    for generation in range(generations):
        fitness_scores = [calculate_fitness(schedule) for schedule in population]

        top_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])[:int(population_size * 0.3)]

        new_population = [population[i] for i in top_indices]

        while len(new_population) < population_size:
            v1 = random.random()
            v2 = random.random()
            if v1 < crossover_rate and v2 < mutation_rate:
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                child = crossover(parent1, parent2)

                child = mutate(child)

                new_population.append(child)

            if v1 >= crossover_rate and v2 < mutation_rate:
                child = mutate(random.choice(population))

                new_population.append(child)

            if v1 < crossover_rate and v2 >= mutation_rate:
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                child = crossover(parent1, parent2)

                new_population.append(child)

        population = new_population
        best_fitness = min(fitness_scores)
        worst_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")
        print(f"Generation {generation + 1}: Worst Fitness = {worst_fitness}")

    best_individual_index = fitness_scores.index(max(fitness_scores))
    return population[best_individual_index]


best_schedule_with_heuristics = genetic_algorithm_with_heuristics()

print("\nBest Schedule with Heuristics:")
for day in days_of_week:
    for timeslot in timeslots:
        for teacher, info in best_schedule_with_heuristics[day][timeslot].items():
            print(f"{day}, {timeslot}, Class: {info['class']}, Teacher: {teacher}, Group: {info['group']}")
