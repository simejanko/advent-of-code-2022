import math
import sys
from collections import deque
import re
import networkx as nx
from itertools import combinations


def optimal_cumulative_flow(valve_graph, start_valve, time_limit=30, node_filter=None):
    shortest_paths = nx.floyd_warshall(valve_graph)
    unopen_valves = {v for v in valve_graph.nodes if valve_graph.nodes[v]['flow'] > 0 and
                     (node_filter is None or v in node_filter)}

    stack = deque([(start_valve, time_limit, 0, 0, unopen_valves)])
    best_cumulative_flow = 0
    while stack:
        valve, time_limit, flow_rate, total_flow, unopen_valves = stack.pop()
        if not unopen_valves or time_limit <= 0:
            total_flow += flow_rate * time_limit
            # time_limit = 0
            best_cumulative_flow = max(best_cumulative_flow, total_flow)
            continue

        # open valve
        if valve in unopen_valves:
            total_flow += flow_rate  # still old flow while opening
            time_limit -= 1

            flow_rate += valve_graph.nodes[valve]['flow']
            unopen_valves_new = set(unopen_valves)
            unopen_valves_new.remove(valve)
        else:
            unopen_valves_new = unopen_valves

        if not unopen_valves_new:  # no more valves to open
            stack.append((valve, time_limit, flow_rate, total_flow, unopen_valves_new))

        for v in unopen_valves_new:
            travel_time = round(shortest_paths[valve][v])
            stack.append((v, time_limit - travel_time, flow_rate, total_flow + travel_time * flow_rate,
                          unopen_valves_new))

    return best_cumulative_flow


if __name__ == '__main__':
    INT_REGEX = r'-?\d+'
    VALVE_REGEX = r'[A-Z][A-Z]'

    valve_graph = nx.Graph()
    with open(sys.argv[1]) as f:
        for line in f:
            valves = re.findall(VALVE_REGEX, line)
            flow_rate = int(re.search(INT_REGEX, line).group(0))
            source = valves[0]

            valve_graph.add_edges_from(((source, v) for v in valves[1:]))
            valve_graph.nodes[source]['flow'] = flow_rate

    # part 1
    print(optimal_cumulative_flow(valve_graph, 'AA'))

    # part 2
    best_flow = 0
    # all possible ways to split the positive flow nodes between two people
    unopen_valves = {v for v in valve_graph.nodes if valve_graph.nodes[v]['flow'] > 0}
    for n_p1 in range(1, math.ceil(len(unopen_valves) / 2)):
        for valves_p1 in combinations(unopen_valves, n_p1):
            valves_p1 = set(valves_p1)
            valves_p2 = unopen_valves - valves_p1
            best_flow = max(best_flow,
                            optimal_cumulative_flow(valve_graph, 'AA', time_limit=26, node_filter=valves_p1) + \
                            optimal_cumulative_flow(valve_graph, 'AA', time_limit=26, node_filter=valves_p2))
    print(best_flow)
