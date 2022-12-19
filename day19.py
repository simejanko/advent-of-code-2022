import sys
import re

INT_REGEX = r'-?\d+'

RES = ['ore', 'clay', 'obs', 'geo']
RES_IDX = {r: i for i, r in enumerate(RES)}

blueprints = []
with open(sys.argv[1]) as f:
    for line in f:
        id, ore_rob_cost, clay_rob_cost, obs_rob_ocost, obs_rob_ccost, geo_rob_ocost, geo_rob_obscost \
            = map(int, re.findall(INT_REGEX, line))
        blueprints.append([{'ore': ore_rob_cost}, {'ore': clay_rob_cost}, {'ore': obs_rob_ocost, 'clay': obs_rob_ccost},
                           {'ore': geo_rob_ocost, 'obs': geo_rob_obscost}])  # RESOURCES order

time_limit = 24
blueprint = blueprints[1]
start_resources = [0, 0, 0, 0]  # RESOURCES order
start_robots = [1, 0, 0, 0]  # RESOURCES order
nodes = [(start_resources, start_robots)]
new_nodes = []
for i in range(time_limit):
    print(len(nodes))
    for node in nodes:
        resources, robots = node

        after_resources = list(resources)
        for ri, count in enumerate(robots):
            after_resources[ri] += count

        for ri, recipe in enumerate(blueprint):
            if not all(resources[RES_IDX[resource_name]] >= cost for resource_name, cost in recipe.items()):
                continue
            new_robots = list(robots)
            new_robots[ri] += 1

            new_resources = list(after_resources)
            for resource_name, cost in recipe.items():
                new_resources[RES_IDX[resource_name]] -= cost

            # TODO: data structure to make this query efficient
            if any(all(r1 <= r2 for r1, r2 in zip(new_resources, existing_res)) and
                   all(r1 <= r2 for r1, r2 in zip(new_robots, existing_rob))
                   for existing_res, existing_rob in new_nodes):
                continue

            new_nodes.append((new_resources, new_robots))
        else:
            new_nodes.append((after_resources, robots))
    nodes = new_nodes
    new_nodes = []

print(max(resources[RES_IDX['geo']] for resources, _ in nodes))
