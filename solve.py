from collections import defaultdict

graph_matrix = []
cars = []
street_weights = dict()

def defaultValue():
    return 0
street_frequencies = defaultdict(defaultValue)

'''
Modelling the car as an entity.
For the moment it contains only the list of streets it traverses
but maybe in future it may be useful to keep track of other things
(I'm thinking about simulating in real time so we need to keep track
of the position, if it's going or is stopped and things like that)
'''
class Car:
    def __init__(self, line):
        self.streets = line.split()[1:]


def makeSchedules(nodes, graph, street_freq):
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
        
        '''
        These frequencies are the time the traffic light for that street will
        stay green in the schedule. This is an arbitrary metric, here the times
        are halved if bigger than one but we should try other metrics since this
        is far from optimal, but it's at least something ¯\_(ツ)_/¯
        '''
        local_freq = list(map(lambda x: x // 2 if x > 1 else 1, local_freq))

        # now we build the schedule to in its form for the output file
        schedule = []
        # first we need the node ID
        schedule.append(str(i))
        # then we need the number of elements in the schedule
        schedule.append(str(len(node_streets)))
        # then for each element we add a line with the name of the street and the time it will stay green
        for i, h in enumerate(node_streets):
            schedule.append(f"{h} {local_freq[i]}")

        # then append this schedule to the list of schedules
        schedules.append(schedule)

    return schedules


def compute(lines):

    line = [int(x) for x in lines[0].split()]
    duration, nodes_n, streets_n, cars_n, extra_points = line

    graph_matrix = [[None] * nodes_n for _ in range(nodes_n)]
    ''' graph_matrix
    This is a square matrix of size node_n and represents a directed graph.
    Each row and each column are the node at that index and the intersections
    are the links between them where we are going to place the name of the street.
    In the rows are the nodes of destination while in the columns the origins.
    For example a street from node 3 to node 5 will be placed in graph_matrix[5][3].
    So if we take graph_matrix[5] and filter out the None values we can get
    all the streets coming into the node 5 and all the traffic lights of the node.
    '''

    # this index will keep track of the line in the file (first line already parsed)
    line_index = 1 

    # parsing the lines related to the streets and making the graph
    for _ in range(streets_n):
        line_value = lines[line_index].split()
        origin_node = int(line_value[0])
        destination_node = int(line_value[1])
        street_name = line_value[2]
        graph_matrix[destination_node][origin_node] = street_name
        street_weights[street_name] = int(line_value[3])
        line_index += 1

    # parsing the cars
    for _ in range(cars_n):
        cars.append(Car(lines[line_index]))
        line_index += 1

    # for each street get the number of cars that will traverse it
    for car in cars:
        for street in car.streets:
            street_frequencies[street] += 1

    # for each node lets make a schedule and create a list of schedules to output
    schedules = makeSchedules(nodes_n, graph_matrix, street_frequencies)

    output_list = [str(len(schedules))]
    for sched in schedules:
        output_list.extend(sched)

    return output_list


##############################################################################


'''
Main function called when launching the script.
It takes the input file path as command line argument,
converts this file into a list of strings (one for each line)
and passes this list to the compute() function, 
which generates another list of strings.
Then it dumps those strings into the output file.
The output file will have '-out' after the name and placed in
the same path as the input file.
'''
def main():
    import os
    import sys
    import time

    assert len(sys.argv) > 1, "Input file path is required"

    input_path = sys.argv[1]
    assert os.path.exists(input_path), "File not found" 

    output_path = input_path[:-4] + "-out.txt"

    print("RUNNING...")
    start_time = time.perf_counter()
    
    with open(input_path, "r") as input_file:
        input_lines = [x.strip() for x in input_file.readlines()]

    output_lines = compute(input_lines)

    with open(output_path, "w") as output_file:
        output_file.write("\n".join(output_lines))

    elapsed_time = time.perf_counter() - start_time
    print(f"COMPLETED IN {elapsed_time:0.4f}s")


if __name__ == "__main__":
    main()