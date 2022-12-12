from functools import reduce
import re, os, math, copy
from dataclasses import dataclass

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_ch_pos(ch, lines, fst=True):
    res = []
    for ri, li in enumerate(lines):
        cis = [i for i in range(len(li)) if li[i] == ch]
        if cis and fst:
            return cis[0], ri
        else:
            res += [(c, ri) for c in cis]
    return res


def get_best_path_len(sp, tps, lines):
    paths = [(sp,)]
    queued = {sp}
    while next((p for p in paths if p[-1] in tps), None) is None:
        npaths = []
        while len(paths):
            pth = paths.pop()
            cp = pth[-1]
            xx, yy = cp
            nps = [
                np for np in [(xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1)]
                if 0 <= np[0] < len(lines[0]) and 0 <= np[1] < len(lines) and
                    ord(lines[np[1]][np[0]]) + 1 >= ord(lines[yy][xx]) and
                    np not in queued
            ]
            for np in nps:
                queued.add(np)
                npaths.append(pth + (np,))
        paths = npaths

    return len(paths[0]) - 1


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            lines = [line.strip() for line in fr.readlines()]

        sp = get_ch_pos('S', lines)
        tp = get_ch_pos('E', lines)
        lines[sp[1]] = lines[sp[1]].replace('S', 'a')
        lines[tp[1]] = lines[tp[1]].replace('E', 'z')
        sps = get_ch_pos('a', lines, False)

        result_p1 = get_best_path_len(tp, [sp], lines)
        result_p2 = get_best_path_len(tp, sps, lines)
        print(file_path, result_p1, result_p2)


if __name__ == "__main__":
    main()
