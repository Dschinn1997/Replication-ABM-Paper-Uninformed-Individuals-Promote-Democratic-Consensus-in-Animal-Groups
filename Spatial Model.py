# Defining of the group individuals by their current position, motion direction, preffered
# target direction, weighting term, and group membership (if part of majority, minority or uninformed)
class Individual:
    def __init__(self, x_position, y_position, x_direction, y_direction, x_preferred_direction,
                 y_preferred_direction, weight, membership):
        self.position = [x_position, y_position]
        self.direction = [x_direction, y_direction]
        self.preferred_direction = [x_preferred_direction, y_preferred_direction]
        self.weight = weight
        self.membership = membership

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def get_preferred_direction(self):
        return self.preferred_direction

    def get_weight(self):
        return self.weight

    def get_membership(self):
        return self.membership

    def set_position(self, x_position, y_position):
        self.position = [x_position, y_position]

    def set_preferred_direction(self, x_preferred_direction, y_preferred_direction):
        self.preferred_direction = [x_preferred_direction, y_preferred_direction]


# Function that calculates a random starting position for the individual i
def calculate_position():
    x_position = random.uniform(-1, 1)
    y_position = random.uniform(-1, 1)

    return x_position, y_position


# Function that calculates a random motion direction for the individual i
# Choose to base the calculation on random angles, as a naive solution would be supoptimal, for further explanations see
# https://towardsdatascience.com/the-best-way-to-pick-a-unit-vector-7bd0cc54f9b
def calculate_direction():
    angle = random.uniform(0, 2 * math.pi)
    x_direction = math.cos(angle)
    y_direction = math.sin(angle)

    return x_direction, y_direction


# Function calculates the preferred travel (target) direction for individual i, that changes constantly
def calculate_preferred_direction(x_position, y_position, target: list):
    x_difference = target[0] - x_position
    y_difference = target[1] - y_position
    vector_length = math.sqrt(math.pow(x_difference, 2) + math.pow(y_difference, 2))
    x_preferred_direction = x_difference / vector_length
    y_preferred_direction = y_difference / vector_length

    return x_preferred_direction, y_preferred_direction


# Function calculates the individuals desired motion direction for the next time step t and rotates them by theta.
# It then updates the individuals positions and preferred travel (target) directions.
def update(individuals: list):
    # Second list of individuals to iterate over and find out for which individual pairs the
    # repulsion and attraction rule applies
    individuals_copy = individuals.copy()

    # Lists that note for which individual pairs, which rule apply
    # List structure [[individual i's index][individual j's index in i's zone, individual j's index in i's zone, ...]]
    repulsion_applies = []
    attraction_applies = []
    nothing_applies = []

    # Lists hold the social and normalized social component of an individual i
    # List structure [[individual i's index][individual i's component]]
    social_components = []
    norm_social_components = []

    # Lists hold the combined social and goal and normalized social and goal component of an individual i
    # List structure [[individual i's index][individual i's component]]
    goal_social_components = []
    norm_goal_social_components = []

    # List holds the rotated normalized social and goal component of an individual i
    # List structure [[individual i's index][individual i's rotated component]]
    random_goal_social_components = []

    # Get the information in which cases the repulsion rule, attraction rule, or no rule applies and save it
    # in the respective lists
    # For finding out how to spot if coordiantes of individual j are in the circular zones of i see
    # https://stackoverflow.com/questions/12262017/python-checking-if-coordinates-are-within-circle
    for individual in individuals:
        temp_repulsion = []
        temp_attraction = []

        # Find pairings for which the repulsion rule applies
        for copy in individuals_copy:
            if ((copy.position[0] - individual.position[0]) ** 2 + (
                    copy.position[1] - individual.position[1]) ** 2) <= alpha ** 2 \
                    and individuals.index(individual) != individuals_copy.index(copy):
                temp_repulsion.append(individuals_copy.index(copy))

        if temp_repulsion:
            repulsion_applies.append([individuals.index(individual), temp_repulsion])

        # Find pairings for which the attraction rule applies
        if not temp_repulsion:
            for copy in individuals_copy:
                if ((copy.position[0] - individual.position[0]) ** 2 + (
                        copy.position[1] - individual.position[1]) ** 2) <= rho ** 2 \
                        and individuals.index(individual) != individuals_copy.index(copy):
                    temp_attraction.append(individuals_copy.index(copy))

        if temp_attraction:
            attraction_applies.append([individuals.index(individual), temp_attraction])

        # Find individuals for which the no rule applies
        if not temp_repulsion and not temp_attraction:
            nothing_applies.append(individuals.index(individual))

    # Calculation individuals' social components
    # For individuals for which the repulsion rule applies
    if repulsion_applies:
        for indices in repulsion_applies:
            x_social_component, y_social_component = 0, 0

            for index in indices[1]:
                x_difference = individuals[index].position[0] - individuals[indices[0]].position[0]
                y_difference = individuals[index].position[1] - individuals[indices[0]].position[1]
                vector_length = math.sqrt(math.pow(x_difference, 2) + math.pow(y_difference, 2))
                x_social_component = x_social_component + x_difference / vector_length
                y_social_component = y_social_component + y_difference / vector_length

            x_social_component = -x_social_component
            y_social_component = -y_social_component
            social_component = [x_social_component, y_social_component]
            social_components.append([indices[0], social_component])

    # For individuals for which the attraction rule applies
    if attraction_applies:
        for indices in attraction_applies:
            x1_social_component, y1_social_component = 0, 0
            x2_social_component, y2_social_component = 0, 0

            for index in indices[1]:
                x1_difference = individuals[index].position[0] - individuals[indices[0]].position[0]
                y1_difference = individuals[index].position[1] - individuals[indices[0]].position[1]
                vector_length = math.sqrt(math.pow(x1_difference, 2) + math.pow(y1_difference, 2))
                x1_social_component = x1_social_component + x1_difference / vector_length
                y1_social_component = y1_social_component + y1_difference / vector_length

                x2_social_component = x2_social_component + individuals[index].direction[0]
                y2_social_component = y2_social_component + individuals[index].direction[1]

            x_social_component = x1_social_component + x2_social_component
            y_social_component = y1_social_component + y2_social_component
            social_component = [x_social_component, y_social_component]
            social_components.append([indices[0], social_component])

    # For individuals for which the no rule applies
    if nothing_applies:
        for indices in nothing_applies:
            x_social_component, y_social_component = 0, 0
            social_component = [x_social_component, y_social_component]
            social_components.append([indices, social_component])

    # Calculation individuals' normalized social components
    for social_component in social_components:
        if social_component[1][0] == 0 and social_component[1][1] == 0:
            norm_x_social_component = 0
            norm_y_social_component = 0
        else:
            vector_length = math.sqrt(math.pow(social_component[1][0], 2) + math.pow(social_component[1][1], 2))
            norm_x_social_component = social_component[1][0] / vector_length
            norm_y_social_component = social_component[1][1] / vector_length

        norm_social_component = [norm_x_social_component, norm_y_social_component]
        norm_social_components.append([social_component[0], norm_social_component])

    # Calculation individuals' combined social and goal components (travel direction)
    for norm_social_component in norm_social_components:
        x_goal_social_component = norm_social_component[1][0] + individuals[norm_social_component[0]].weight * \
                                  individuals[norm_social_component[0]].preferred_direction[0]
        y_goal_social_component = norm_social_component[1][1] + individuals[norm_social_component[0]].weight * \
                                  individuals[norm_social_component[0]].preferred_direction[1]

        goal_social_component = [x_goal_social_component, y_goal_social_component]
        goal_social_components.append([norm_social_component[0], goal_social_component])

    # Calculation individuals' normalized combined social and goal components (normalized travel direction)
    for goal_social_component in goal_social_components:
        if goal_social_component[1][0] == 0 and goal_social_component[1][1] == 0:
            norm_x_goal_social_component = 0
            norm_y_goal_social_component = 0
        else:
            vector_length = math.sqrt(
                math.pow(goal_social_component[1][0], 2) + math.pow(goal_social_component[1][1], 2))
            norm_x_goal_social_component = goal_social_component[1][0] / vector_length
            norm_y_goal_social_component = goal_social_component[1][1] / vector_length

        norm_goal_social_component = [norm_x_goal_social_component, norm_y_goal_social_component]
        norm_goal_social_components.append([goal_social_component[0], norm_goal_social_component])

    # Calculation individuals' rotated travel direction, for insight how to rotate vector see
    # https://matthew-brett.github.io/teaching/rotation_2d.html
    for norm_goal_social_component in norm_goal_social_components:
        x_random_goal_social_component = norm_goal_social_component[1][0] * math.cos(theta) - \
                                         norm_goal_social_component[1][1] * math.sin(theta)
        y_random_goal_social_component = norm_goal_social_component[1][0] * math.sin(theta) + \
                                         norm_goal_social_component[1][1] * math.cos(theta)

        random_goal_social_component = [x_random_goal_social_component, y_random_goal_social_component]
        random_goal_social_components.append([norm_goal_social_component[0], random_goal_social_component])

    # Updating the individuals' current positions by their travel directions and their
    # preferred travel (target) directions
    for individual in individuals:

        # Updating current positions by their travel directions
        for random_goal_social_component in random_goal_social_components:
            if individuals.index(individual) == random_goal_social_component[0]:
                x_position = individual.position[0] + random_goal_social_component[1][0]
                y_position = individual.position[1] + random_goal_social_component[1][1]
                individual.set_position(x_position, y_position)

        # Updating preferred travel (target) directions based on new positions
        if individual.membership == "Group 1":
            x_preferred_direction, y_preferred_direction = calculate_preferred_direction(individual.position[0],
                                                                                         individual.position[1],
                                                                                         target1)
            individual.set_preferred_direction(x_preferred_direction, y_preferred_direction)
        elif individual.membership == "Group 2":
            x_preferred_direction, y_preferred_direction = calculate_preferred_direction(individual.position[0],
                                                                                         individual.position[1],
                                                                                         target2)
            individual.set_preferred_direction(x_preferred_direction, y_preferred_direction)
        else:
            x_preferred_direction, y_preferred_direction = 0, 0
            individual.set_preferred_direction(x_preferred_direction, y_preferred_direction)


# Function calculates the centroid of the whole group
def calculate_centroid(individuals: list):
    x_sum = 0
    y_sum = 0
    for individual in individuals:
        x_sum = x_sum + individual.position[0]
        y_sum = y_sum + individual.position[1]

    x_center = x_sum / len(individuals)
    y_center = y_sum / len(individuals)
    centroid = [x_center, y_center]

    return centroid


# Function checks if the group centroid falls in one of the defined areas around the targets,
# hence function registers if a target got approach and if so which one (1 = target majority, 2 = target minority)
def decision_making_inner(individuals: list, centroid: list, target1: list, target2: list):
    if ((centroid[0] - target1[0]) ** 2 + (centroid[1] - target1[1]) ** 2) <= target_rad ** 2:
        return 1
    elif ((centroid[0] - target2[0]) ** 2 + (centroid[1] - target2[1]) ** 2) <= target_rad ** 2:
        return 2
    else:
        return None


# Function updates the individuals' positions and their preferred travel (target) directions by calling update(),
# afterwards it checks if the new group centroid falls in the target areas by calling decision_making_inner().
# The function updates the individuals as long until a target got approached or the individuals were updated
# 10000 times and still no target was approached. The function returns either the approached target or None
# if no target was apprached after 10000 update processes.
def decision_making(individuals: list, target1: list, target2: list):
    result = None
    counter = 0
    while result == None and counter < 10000:
        update(individuals)
        centroid = calculate_centroid(individuals)
        result = decision_making_inner(individuals, centroid, target1, target2)
        counter = counter + 1

    return result


##### Settings to plot Figure 1A of the paper
# Load needed packages
import random
import math
import matplotlib.pyplot as plt

# Parameters and settings
# Group characteristics
N1 = 6  # group size 1, size of the majority
N2 = 5  # group size 2, size of the minority
N3 = 2  # group size 3, here redundant as compution is without uninformed individuals
uninformed = False  # bool indicator if uninformed individuals exist, for plot not existend

if uninformed:
    N = N1 + N2 + N3  # group size with uninformed individuals
else:
    N = N1 + N2  # group size without uninformed individuals

w1 = 0.3  # preference of the majority for specific target 1
w2 = [0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5]  # preference of the minority for specific target 2
w3 = 0  # preference of the uninformed

# Individual's rules
alpha = 1  # radius of the repulsion zone
rho = 6  # radius of the attraction zone

# "Random", here fixed influence
theta = 114.591  # rotation of desired movement for the next time step t by 2.00 rad ≈ 114.591 degree

# Spatial settings
target1 = [100, -50]  # target 1, majority target
target2 = [100, 50]  # target 2, minority target
target_rad = 4  # radius around the targets, that defines target area

# Time settings
transition_time = 200  # transition period for group forming
replications = 100  # number of replicates for parameter values,
                    # actually 20000 but reduced due computational restrictions

# Set seed to make computation replicable
random.seed(30)

# List for saving results of individuals simulations
results = []  # group status after centroid is around one of the targets with distance 4

for element in w2:
    temp_results = []

    for replication in range(replications):

        # Initialize individuals
        individuals = []

        # Initializing the majority
        for i in range(N1):
            x_position, y_position = calculate_position()
            x_direction, y_direction = calculate_direction()
            x_preferred_direction, y_preferred_direction = calculate_preferred_direction(x_position, y_position,
                                                                                         target1)
            weight = w1
            membership = "Group 1"
            individual = Individual(x_position, y_position, x_direction, y_direction, x_preferred_direction,
                                    y_preferred_direction, weight, membership)

            individuals.append(individual)

        # Initializing the minority
        for i in range(N2):
            x_position, y_position = calculate_position()
            x_direction, y_direction = calculate_direction()
            x_preferred_direction, y_preferred_direction = calculate_preferred_direction(x_position, y_position,
                                                                                         target2)
            weight = element
            membership = "Group 2"
            individual = Individual(x_position, y_position, x_direction, y_direction, x_preferred_direction,
                                    y_preferred_direction, weight, membership)

            individuals.append(individual)

        # Initializing if wished the uninformed, for this plot it was not wished
        if uninformed:
            for i in range(N3):
                x_position, y_position = calculate_position()
                x_direction, y_direction = calculate_direction()
                x_preferred_direction, y_preferred_direction = 0, 0
                # Either have no preferred direction or randomized, but not of importance since weighting term is 0
                weight = w3
                membership = "Group 3"
                individual = Individual(x_position, y_position, x_direction, y_direction, x_preferred_direction,
                                        y_preferred_direction, weight, membership)

                individuals.append(individual)

        # Update the individuals 200times, approximate transition time form group that was
        # state by Couzin et al. (2011)
        for time_step in range(transition_time):
            update(individuals)

        # Recenter the group to (0, 0) so that starting conditions are independent of any
        # initial drift and let them approach the target
        centroid = calculate_centroid(individuals)

        # For how to recenter data points see https://www.statology.org/center-data-in-python/
        for individual in individuals:
            x_position = individual.position[0] - centroid[0]
            y_position = individual.position[1] - centroid[1]
            individual.set_position(x_position, y_position)

        # Let group approach target and save approached (or not approached) target of the simulation
        result = decision_making(individuals, target1, target2)
        temp_results.append(result)

    # Save all the simulations for the individual parameter values
    results.append(temp_results)

# print(results)

# Calculate the proportion reaching the majority target (number of times the majority-preferred
# target is reached divided by the number of times a minority or majority target was reached
# (i.e., only consensus decisions were evaluated)
majority_proportions = []
splits = []

for ls in results:
    target_reached = 0
    majority_target = 0

    split = 0

    for element in ls:
        if element == 1 or element == 2:
            target_reached = target_reached + 1

            if element == 1:
                majority_target = majority_target + 1

        else:
            split = split + 1

    majority_proportion = majority_target / target_reached
    majority_proportions.append(majority_proportion)
    splits.append(split)



##### Recreating plot Figure 1A of the paper
default_x_ticks = range(len(w2))
plt.plot(default_x_ticks, majority_proportions, 'r--')
plt.xticks(default_x_ticks, w2)

plt.xlabel('Strength of minority preference, w2')
plt.ylabel('Proportion of groups that reached the majority target')
plt.show()

print(majority_proportions)
print(splits)
