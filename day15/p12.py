import copy, json, os, math, functools, re

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = {
    os.path.join(DIR, 'input1.txt'): 10,
    os.path.join(DIR, 'input.txt'): 2000000,
}


def add_range(ranges, range):
    min1, max1 = range
    i = 0
    min_placed = False
    placed = False
    while i < len(ranges):
        r2 = ranges[i]
        min2, max2 = r2
        if max2 + 1 < min1:
            i += 1
            continue
        if not min_placed and min2 <= min1 <= max2 + 1:
            min1 = min2
            min_placed = True
        if min1 <= min2 <= max2 <= max1:
            ranges.pop(i)
            continue
        if min2 - 1 <= max1 <= max2:
            max1 = max2
            ranges.pop(i)
            ranges.insert(i, (min1, max1))
            placed = True
            break
        if max1 + 1 < min2:
            ranges.insert(i, (min1, max1))
            placed = True
            break
        i += 1
    if not placed:
        ranges.append((min1, max1))
    return ranges


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            lines = [line.strip() for line in fr.readlines()]

        # part 1
        row_p1 = FILE_PATHS[file_path]
        r_set = set()
        rbx_set = set()
        rsx_set = set()
        for li in lines:
            sx, sy, bx, by = [int(m.group()) for m in re.finditer(r'-?\d+', li)]
            sbm = abs(sx - bx) + abs(sy - by)
            diff = sbm - abs(sy - row_p1)
            if diff >= 0:
                for i in range(sx - diff, sx + diff + 1):
                    r_set.add(i)
            if by == row_p1:
                rbx_set.add(bx)
            if sy == row_p1:
                rsx_set.add(sx)
        r_set = r_set - rbx_set - rsx_set
        r1 = len(r_set)

        # part 2
        max_c = row_p1 * 2
        rows = {ry: [] for ry in range(max_c + 1)}
        for li_idx, li in enumerate(lines):
            print(f"line {li_idx+1}/{len(lines)}")
            sx, sy, bx, by = [int(m.group()) for m in re.finditer(r'-?\d+', li)]
            sbm = abs(sx - bx) + abs(sy - by)
            for ry, ranges in rows.items():
                diff = sbm - abs(sy - ry)
                if diff >= 0:
                    min_x = max(sx - diff, 0)
                    max_x = min(sx + diff, max_c)
                    add_range(ranges, (min_x, max_x))
        row = next((ry, r) for ry, r in rows.items() if len(r) > 1)
        r2 = (sorted(row[1])[0][1] + 1) * 4000000 + row[0]

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
