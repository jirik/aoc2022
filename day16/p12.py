import copy, json, os, math, functools, re, itertools
from queue import PriorityQueue

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input.txt'),
]


def dijkstra(distances, start_v):
    # thanks to https://stackoverflow.com/a/22899400
    nodes = tuple(distances)

    unvisited = {node: None for node in nodes}  # using None as +inf
    visited = {}
    current = start_v
    curr_dist = 0
    unvisited[current] = curr_dist

    while True:
        for nb, dist in distances[current].items():
            if nb not in unvisited:
                continue
            new_dist = curr_dist + dist
            if unvisited[nb] is None or unvisited[nb] > new_dist:
                unvisited[nb] = new_dist
        visited[current] = curr_dist
        del unvisited[current]
        if not unvisited:
            break
        candidates = [node for node in unvisited.items() if node[1]]
        current, curr_dist = sorted(candidates, key=lambda x: x[1])[0]

    return visited


def get_path_bonus(graph, pth, start_idx, rnd):
    bonus = 0
    for to_idx in range(start_idx, len(pth)):
        fr_id = pth[to_idx - 1]
        to_id = pth[to_idx]
        fr = graph[fr_id]
        to = graph[to_id]
        dist = fr['distances'][to_id]
        rnd -= dist
        rnd -= 1
        if rnd <= 0:
            break
        bonus += to['pressure'] * rnd
    return bonus, rnd


def get_best_path_bonus(pth, rnd):
    # all distances are 1 in best path
    bonus = 0
    for idx, v in enumerate(pth):
        rnd -= 2
        if rnd <= 0:
            break
        bonus += v['pressure'] * rnd
    return bonus


def get_max_remaining_bonus_if_best_paths_exist(graph, visited, rnds):
    r = 0
    rnds = sorted(rnds, reverse=True)
    best_pth = sorted([v for v in graph.values() if v['id'] not in visited], key=lambda v: v['pressure'], reverse=True)
    for rnd_idx, rnd in enumerate(rnds):
        best_path = best_pth[rnd_idx::len(rnds)]
        best_bonus = get_best_path_bonus(best_path, rnd)
        r += best_bonus
    return r


def get_max_bonus(paths, graph):
    max_bonus = 0
    best_paths = paths[0]
    n_iter = 0
    while len(paths):
        n_iter += 1
        if n_iter % 10000 == 0:
            print(f"Iteration {n_iter}, max_bonus={max_bonus}, best_paths={best_paths}, all paths={len(paths)}")
        prev_path_rnds, prev_bonus, prev_maybe_max_bonus = paths.pop(0)
        if prev_bonus + prev_maybe_max_bonus < max_bonus:
            continue
        prev_paths, prev_rnds = zip(*prev_path_rnds)
        prev_valves = {v for p in prev_paths for v in p}
        for next_parts in itertools.permutations([v_id for v_id in graph.keys() if v_id not in prev_valves],
                                                 len(prev_paths)):
            new_bonus = 0
            next_paths = []
            rnds = []
            for idx, next_part in enumerate(next_parts):
                prev_path = prev_paths[idx]
                prev_rnd = prev_rnds[idx]
                next_path = prev_path + (next_part,)
                new_bns, rnd = get_path_bonus(graph, next_path, len(prev_path), prev_rnd)
                new_bonus += new_bns
                next_paths.append(next_path)
                rnds.append(rnd)
            bonus = prev_bonus + new_bonus
            maybe_max_bonus = get_max_remaining_bonus_if_best_paths_exist(graph, tuple(prev_valves) + next_parts, rnds)
            if bonus + maybe_max_bonus < max_bonus:
                continue
            next_paths_def = (tuple(zip(next_paths, rnds)), bonus, maybe_max_bonus)
            if bonus > max_bonus:
                print(f"Increasing bonus from {max_bonus} to {bonus}, best paths are now {next_paths}")
                best_paths = next_paths_def
                max_bonus = bonus
            paths.append(next_paths_def)
    print(f"max_bonus={max_bonus}, best_paths={best_paths}")
    return max_bonus


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            lines = [line.strip() for line in fr.readlines()]

        start_v = 'AA'
        full_graph = {}
        graph = {}  # graph with only important valves, e.g. start valve and valves with pressure > 0
        for li in lines:
            m = re.match(r'^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)$', li)
            v = m.group(1)
            p = int(m.group(2))
            tos = m.group(3).split(', ')
            full_graph[v] = {
                'id': v,
                'pressure': p,
                'distances': {to: 1 for to in tos}
            }
            if p > 0 or v == start_v:
                graph[v] = {
                    'id': v,
                    'pressure': p,
                    'distances': {}
                }

        full_graph_for_dijkstra = {v['id']: v['distances'] for v in full_graph.values()}

        for fr in graph.values():
            distances = fr['distances']
            for to, cost in dijkstra(full_graph_for_dijkstra, fr['id']).items():
                if to in graph and to != start_v:
                    distances[to] = cost

        r1 = get_max_bonus([((((start_v,), 30),), 0, 0)], graph)
        r2 = get_max_bonus([((((start_v,), 26), ((start_v,), 26)), 0, 0)], graph)
        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
