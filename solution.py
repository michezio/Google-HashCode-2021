from collections import defaultdict

graph = []
cars = []
weights = dict()
street_names = dict()

def def_value():
    return 0
street_freq = defaultdict(def_value)


class Car:
    def __init__(self, line):
        self.streets = [hash(x) for x in line.split()[1:]]


def updateFrequency(street_freq, cars):
    # here we compute how many cars will traverse each street
    for car in cars:
        for street in car.streets:
            if street in street_freq.keys():
                street_freq[street] += 1
            else:
                street_freq[street] = 1


def makeSchedules(nodes, duration, graph, street_freq, street_names):
    schedules = []
    # lets make a schedule for each node
    for i in range(nodes):

        # get the streets coming into the node (so the ones with a traffic light)
        node_streets = [x for x in graph[i] if x is not None]

        # sort the streets by the number of cars that will traverse them (decrescing)
        node_streets.sort(key=lambda x: street_freq[x], reverse=True)

        # remove the streets that will never be traversed, those will stay red all the time
        node_streets = [x for x in node_streets if street_freq[x] != 0]

        # if there are no street left just skip this schedule, this node is never traversed
        if len(node_streets) == 0:
            continue

        # lets build the metric for the schedule
        # create a list of frequencies from the street that will be part of the schedule 
        local_freq = []
        for street in node_streets:
            local_freq.append(street_freq[street])
        
        # these frequencies are the time the traffic light for that street will stay green in the schedule
        # this is an arbitrary metric, here the times are halved if bigger than one
        # we should try other metrics since this is far from optimal, but it at least works
        local_freq = list(map(lambda x: x // 2 if x > 1 else 1, local_freq))

        # now we build the schedule to in its form for the output file
        schedule = []
        # first we need the node ID
        schedule.append(str(i))
        # then we need the number of elements in the schedule
        schedule.append(str(len(node_streets)))
        # then for each element we add a line with the name of the street and the time it will stay green
        for i, h in enumerate(node_streets):
            schedule.append(f"{street_names[h]} {local_freq[i]}")

        # then append this schedule to the list of schedules
        schedules.append(schedule)

    return schedules


def compute(lines):
    line = [int(x) for x in lines[0].split()]
    duration, nodes, streets_n, cars_n, extra_points = line

    graph = [[None] * nodes for i in range(nodes)]

    index = 0

    # parsing the streets and making the graph
    for _ in range(streets_n):
        index += 1
        line_value = lines[index].split()
        name_hash = hash(line_value[2])
        graph[int(line_value[1])][int(line_value[0])] = name_hash
        street_names[name_hash] = line_value[2]
        weights[name_hash] = int(line_value[3])

    # parsing the cars
    for _ in range(cars_n):
        index += 1
        cars.append(Car(lines[index]))

    # for each street get the number of cars that will traverse it
    updateFrequency(street_freq, cars)

    # for each node lets make a schedule and create a list of schedules to output
    schedules = makeSchedules(nodes, duration, graph, street_freq, street_names)

    output_list = [str(len(schedules))]
    for sched in schedules:
        output_list.extend(sched)

    return output_list


# add up path weights for each car (does not include the first path since the car starts at the end)
# ie Car_1 = 3 + 1 = 4
# ie Car_2 = 1 + 3 + 2 = 6

# ignore any sums over the duration time D
# find the lights that are always green (have one street passing through)
# find the lights that have multiple streets passing through
# at least for example A, if cars are at an intersection, prioritize the one with the longest time left in its path
