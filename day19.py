import sys
import re

import numpy as np
from scipy.spatial import KDTree

INT_REGEX = r'-?\d+'

RES = ['ore', 'clay', 'obs', 'geo']
RES_IDX = {r: i for i, r in enumerate(RES)}


# prune based on obviously better nodes amongst the nearest neighbors
def prune(nodes):
    if len(nodes) <= 1:
        return nodes

    potentials = np.array([resources + robots for resources, robots in nodes])
    potentials_kdtree = KDTree(potentials)
    k = min(len(nodes), 15)

    pruned_nodes = []
    for idx, (node, potential) in enumerate(zip(nodes, potentials)):
        if not any(np.all(potential <= potentials[nidx])
                   for nidx in potentials_kdtree.query(potential, k=k)[1] if nidx != idx):
            pruned_nodes.append(node)

    return pruned_nodes


def eval_blueprint(blueprint, time_limit=24):
    start_resources = [0, 0, 0, 0]  # RES order
    start_robots = [1, 0, 0, 0]  # RES order
    nodes = [(start_resources, start_robots)]
    new_nodes = []

    for t in range(time_limit - 1):
        for resources, robots in nodes:
            after_resources = list(resources)
            for idx, count in enumerate(robots):
                after_resources[idx] += count

            # make new robots branches
            for ri, recipe in enumerate(blueprint):
                # check cost
                if not all(resources[RES_IDX[resource_name]] >= cost for resource_name, cost in recipe.items()):
                    continue

                # make a robot
                new_robots = list(robots)
                new_robots[ri] += 1

                # deduct costs
                new_resources = list(after_resources)
                for resource_name, cost in recipe.items():
                    new_resources[RES_IDX[resource_name]] -= cost

                new_nodes.append((new_resources, new_robots))
            new_nodes.append((after_resources, robots))  # or just wait and don't make any robot

        nodes = prune(new_nodes)
        new_nodes = []

    # include the resources generated in the last timestep
    return max(resources[RES_IDX['geo']] + robots[RES_IDX['geo']] for resources, robots in nodes)


if __name__ == '__main__':
    blueprints = []
    with open(sys.argv[1]) as f:
        for line in f:
            id, ore_rob_cost, clay_rob_cost, obs_rob_ocost, obs_rob_ccost, geo_rob_ocost, geo_rob_obscost \
                = map(int, re.findall(INT_REGEX, line))
            blueprints.append(
                [{'ore': ore_rob_cost}, {'ore': clay_rob_cost}, {'ore': obs_rob_ocost, 'clay': obs_rob_ccost},
                 {'ore': geo_rob_ocost, 'obs': geo_rob_obscost}])  # RESOURCES order

    # part 1
    quality_sum = 0
    for i, blueprint in enumerate(blueprints):
        quality_sum += (i + 1) * eval_blueprint(blueprint)
        print(f"{i + 1}/{len(blueprints)} blueprints evaluated")
    print(quality_sum)

    # part 2
    quality_mul = 1
    for i, blueprint in enumerate(blueprints[:3]):
        quality_mul *= eval_blueprint(blueprint, time_limit=32)
        print(f"{i + 1}/3 blueprints evaluated")
    print(quality_mul)
