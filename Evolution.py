import cv2
import numpy as np
import matplotlib.pyplot as plot
import time
import math

# Globale Variablen
#
# secondsperframe & framespersecond

fps = 25
spf = 1 / fps

# definiert die ausgangsattribute

base_speed = 20  # pixel/second
base_health = 200
base_fov = 30
base_met_speed = 0.04
base_met_fov = 0.01
base_variance = 0.2  # mutation rate
base_foodamount = 30
base_foodgenerationrate = 10

# zähler für die lebenden viecher und essen

critters_alive = 0
food_alive = 0

# map size definition

size_x = 1000
size_y = 1000

# erschafft array für die critterdaten mit 1000 spalten 8 reihen
array_critters = np.zeros([1000, 7])

#array für die fooddaten
array_food = np.zeros([1000, 4])

# anfangsbedingungen
food_initial = 200
critters_initial = 200


# Create function for distance between two points
def math_calc_dist(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) +
                     math.pow((p2[1] - p1[1]), 2))


# Create function for normalisation of a vector
def normalize(a, b):
    math.pow(a, 2) + math.pow(b, 2)
    return [a / math.sqrt(math.pow(a, 2) + math.pow(b, 2)), b / math.sqrt(math.pow(a, 2) + math.pow(b, 2))]


# critters erschaffen

for f in range(critters_initial):
    # health auf zwei dezimalstellen gerundet
    array_critters[critters_alive, 0] = np.around(base_health + base_variance * base_health * np.random.uniform(-1, 1),
                                                  2)

    # speed auf zwei dezimalstellen gerundet
    array_critters[critters_alive, 1] = np.around(base_speed + base_variance * base_speed * np.random.uniform(-1, 1), 2)

    # fov auf eine dezimalstelle gerundet
    array_critters[critters_alive, 2] = np.around(base_fov + base_variance * base_fov * np.random.uniform(-1, 1), 1)

    # Coordiantes 3 = x 4 = y
    array_critters[critters_alive, 3] = np.random.uniform() * size_x
    array_critters[critters_alive, 4] = np.random.uniform() * size_y

    # Directions
    rnddirection = np.random.uniform(0, 2 * math.pi)
    array_critters[critters_alive, 5] = math.sin(rnddirection)
    array_critters[critters_alive, 6] = math.cos(rnddirection)

    critters_alive += 1

# ESSEN erschaffen und random auf der map verteilen

for f in range(food_initial):
    # Koordinaten
    array_food[food_alive, 0] = np.random.uniform() * size_x
    array_food[food_alive, 1] = np.random.uniform() * size_y
    array_food[food_alive, 2] = base_foodamount

# starttheloop

while True:

    for critter in range(critters_alive):

        critter_pos = [array_critters[critter, 3], array_critters[critter, 4]]

        # Find the Food

        for food in range(food_alive):

            food_pos = [array_food[food, 0], array_food[food, 1]]

            # if distance to food is smaller than fov set new normalized walking direction:
            if math_calc_dist(critter_pos, food_pos) < array_critters[critter, 2]:
                direction = normalize(food_pos[0] - critter_pos[0], food_pos[1] - critter_pos[1])

                array_critters[critter, 5] = direction[0]
                array_critters[critter, 6] = direction[1]

                # wenn das essen näher ist als der walking speed wird es gegessen
                if math_calc_dist(critter_pos, food_pos) < array_critters[critter, 1]:
                    array_critters[critter, 0] += array_food[food, 2]
                    break
                break

        # Critter loses health through metabolism:
        array_critters[critter, 0] += -(1 + base_met_speed * array_critters[critter, 1] + base_met_fov * array_critters[
            critter, 2])

        # If health at or below zero, critter dies:
        if array_critters[critter, 0] <= 0:
            array_critters[critter, 0:8] = array_critters[critters_alive, 0:8]
            critters_alive += -1

        # Wenn Health über 300 wird ein neuer Critter gemacht:
        if array_critters[critter, 0] >= 300:
            array_critters[critter, 0] = 300 - base_health

            # health auf zwei dezimalstellen gerundet
            array_critters[critters_alive, 0] = np.around(
            base_health + base_variance * base_health * np.random.uniform(-1, 1),
            2)

        # speed auf zwei dezimalstellen gerundet
            array_critters[critters_alive, 1] = np.around(
            array_critters[critter, 1] + base_variance * array_critters[critter, 1] * np.random.uniform(-1, 1), 2)

        # fov auf eine dezimalstelle gerundet
            array_critters[critters_alive, 2] = np.around(
            array_critters[critter, 2] + base_variance * array_critters[critter, 2] * np.random.uniform(-1, 1), 1)

        # Coordiantes 3 = x 4 = y
            array_critters[critters_alive, 3] = array_critters[critter, 3]
            array_critters[critters_alive, 4] = array_critters[critter, 4]

        # Directions
            rnddirection = np.random.uniform(0, 2 * math.pi)
            array_critters[critters_alive, 5] = math.sin(rnddirection)
            array_critters[critters_alive, 6] = math.cos(rnddirection)

            critters_alive += 1

        # Movement testing if critter runs off map and then moving:
        movement_vector = [array_critters[critter, 5], array_critters[critter, 6]]
        movement_vector *= spf * array_critters[critter, 1]
        testingpos = critter_pos + movement_vector


        #critter changes direction instead of running out of map
        if testingpos[0] <= 0 or testingpos[0] >= size_x:
            movement_vector[0] -= 2 * movement_vector[0]

        if testingpos[1] <= 0 or testingpos[1] >= size_y:
            movement_vector[1] -= 2 * movement_vector[1]

        critter_pos += np.around(movement_vector, 2)
        array_critters[critter, 3:5] = critter_pos

    #draw

    #TODO

    #FPS CONTROL

    time.sleep(spf)

    # Exit function:

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pause function:

    if cv2.waitKey(1) & 0xFF == ord('p'):
        time.sleep(0.3)
        while True:
            time.sleep(0.3)
            if cv2.waitKey(1) & 0xFF == ord('p'):
                break

# plot the distribution of speed, fov

# plot.hist(array_critters[:, 0], 40, [100, 300])
plot.hist(array_critters[:, 1], 40, [1, 30], edgecolor=[0, 0, 0])
plot.hist(array_critters[:, 2], 40, [1, 30], edgecolor=[0, 0, 0])

plot.show()
