from collections import defaultdict

graph = []
cars = []
weights = dict()
street_names = dict()


def def_value():
    return 0


street_freq = defaultdict(def_value)


class Street:
    def __init__(self, line):
        parsed = line.split()
        self.start = int(parsed[0])
        self.stop = int(parsed[1])
        self.id = hash(parsed[2])
        self.duration = int(parsed[3])


class Node:
    def __init__(self, id):
        self.id = id
        self.in_streets = []
        self.out_streets = []


class Car:
    def __init__(self, line):
        self.streets = [hash(x) for x in line.split()[1:]]


def getStreetName(hash):
    return street_names[hash]


def getStreetWeight(hash):
    return weights[hash]


def hash(x):
    return x


def updateFrequency(street_freq, cars):
    for car in cars:
        for street in car.streets:
            if street in street_freq.keys():
                street_freq[street] += 1
            else:
                street_freq[street] = 1


def makeSchedules(nodes, duration, graph, street_freq, street_names):
    schedules = []
    for i in range(nodes):
        #print(graph)
        #print(i)
        node_streets = [x for x in graph[i] if x is not None]
        node_streets.sort(key=lambda x: street_freq[x], reverse=True)
        node_streets = [x for x in node_streets if street_freq[x] != 0]
        if len(node_streets) == 0:
            continue
        local_freq = []
        for street in node_streets:
            local_freq.append(street_freq[street])

        total = sum(local_freq)
        while total > duration:
            old_sum = total
            local_freq.map(lambda x: 1 if x // 2 == 0 else x // 2)
            total = sum(local_freq)
            if total == old_sum:
                break

        schedule = []
        schedule.append(str(i))
        for i, h in enumerate(node_streets):
            schedule.append(f"{street_names[h]} {local_freq[i]}")

        schedules.append(schedule)

    return schedules


def compute(lines):
    line = [int(x) for x in lines[0].split()]
    duration, nodes, streets_n, cars_n, extra_points = line

    #print(duration, nodes, streets_n, cars_n, extra_points)

    graph = [[None] * nodes for i in range(nodes)]

    index = 0

    for _ in range(streets_n):
        index += 1
        line_value = lines[index].split()
        start = int(line_value[0])
        stop = int(line_value[1])
        weight = int(line_value[3])
        name_hash = hash(line_value[2])
        street_names[name_hash] = line_value[2]
        weights[name_hash] = weight
        graph[stop][start] = name_hash

    for _ in range(cars_n):
        index += 1
        cars.append(Car(lines[index]))

    updateFrequency(street_freq, cars)
    #print(graph)
    schedules = makeSchedules(nodes, duration, graph, street_freq,
                              street_names)

    output_list = [str(len(schedules))]
    for index, sched in enumerate(schedules):
        output_list.append(sched[0])
        output_list.append(str(len(sched)-1))
        for line in sched[1:]:
            output_list.append(line)

    return output_list


# add up path weights for each car (does not include the first path since the car starts at the end)
# ie Car_1 = 3 + 1 = 4
# ie Car_2 = 1 + 3 + 2 = 6

# ignore any sums over the duration time D
# find the lights that are always green (have one street passing through)
# find the lights that have multiple streets passing through
# at least for example A, if cars are at an intersection, prioritize the one with the longest time left in its path
'''

number of nodes to apply the schedule

node id
number of streets
name of street, time
name of street, time

node id
number of streets
name of street, time
name of street, time


'''
