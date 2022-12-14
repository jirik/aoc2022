import copy, json, os, math, functools, re

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input.txt'),
]

AIR = 0
STONE = 1
SAND = 2


def print_cave(cave):
    for li in cave:
        print(''.join('#' if c == STONE else 'o' if c == SAND else '.' for c in li))


def get_sand_coord(cave, s_pos):
    x, y = s_pos
    for nx, ny in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
        if not 0 <= nx < len(cave[0]):
            return nx, len(cave) - 2
        if ny == len(cave):
            return None
        if cave[ny][nx] == AIR:
            return get_sand_coord(cave, (nx, ny))
    return x, y


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            lines = [line.strip() for line in fr.readlines()]

        paths = []
        for li in lines:
            cs = [int(m.group()) for m in re.finditer(r'\d+', li)]
            ts = [(cs[i*2], cs[i*2+1]) for i in range(len(cs)//2)]
            paths.append(ts)

        sand_start = [500, 0]
        x_coords = {t[0] for p in paths for t in p}.union({sand_start[0]})
        y_coords = {t[1] for p in paths for t in p}.union({sand_start[1]})
        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)

        cave = [[AIR] * (x_max - x_min + 1) for i in range(y_max - y_min + 1)]

        for p in paths:
            for t_idx in range(len(p) - 1):
                t1 = p[t_idx]
                t2 = p[t_idx+1]
                same_idx = next(i for i in range(2) if t1[i] == t2[i])
                diff_idx = 0 if same_idx == 1 else 1
                diff_min = min(t1[diff_idx], t2[diff_idx])
                diff_max = max(t1[diff_idx], t2[diff_idx])
                for c in range(diff_min, diff_max + 1):
                    x_idx = (c if diff_idx == 0 else t1[same_idx]) - x_min
                    y_idx = (c if diff_idx == 1 else t1[same_idx]) - y_min
                    cave[y_idx][x_idx] = STONE

        ss = (sand_start[0] - x_min, sand_start[1] - y_min)
        cave[ss[1]][ss[0]] = SAND
        empty_cave = copy.deepcopy(cave)
        print_cave(cave)

        r1 = 0
        sp = get_sand_coord(cave, ss)
        while sp is not None and 0 <= sp[0] < len(cave[0]):
            cave[sp[1]][sp[0]] = SAND
            r1 += 1
            sp = get_sand_coord(cave, ss)
        print_cave(cave)

        cave = copy.deepcopy(empty_cave)
        cave.append([AIR] * len(cave[0]))
        cave.append([STONE] * len(cave[0]))

        r2 = 1
        ss = (sand_start[0] - x_min, sand_start[1] - y_min)
        sp = get_sand_coord(cave, ss)
        while sp != ss:
            x, y = sp
            if x < 0:
                cave = [[AIR] + r for r in cave]
                ss = (ss[0] + 1, ss[1])
                x = 0
                cave[len(cave) - 1][x] = STONE
            if x >= len(cave[0]):
                cave = [r + [0] for r in cave]
                cave[len(cave) - 1][x] = STONE
            cave[y][x] = SAND
            r2 += 1
            sp = get_sand_coord(cave, ss)
        cave = [r[x_min + ss[0] - sand_start[0]:ss[0] - sand_start[0] + x_max + 1] for r in cave]
        print_cave(cave)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()