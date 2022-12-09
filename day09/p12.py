import math
import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input_sample2.txt'),
    os.path.join(DIR, 'input.txt'),
]


def sign(n):
    return n if not n else math.copysign(1, n)


def get_next_pos(head, tail):
    deltas = [h - tail[idx] for idx, h in enumerate(head)]
    if max(abs(d) for d in deltas) > 1:
        tail = tuple(t + int(sign(deltas[idx])) for idx, t in enumerate(tail))
    return tail


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip().split(' ') for line in f.readlines()]

        cmds = [ch for ch, nch in lines for _ in range(int(nch))]

        tps = [(0, 0)] * 10
        tail_set_p1 = {(0, 0)}
        tail_set_p2 = {(0, 0)}
        tail_idx_p1 = 1
        tail_idx_p2 = 9
        for cmd in cmds:
            xx, yy = tps[0]
            yy += cmd == 'U'
            yy -= cmd == 'D'
            xx += cmd == 'R'
            xx -= cmd == 'L'
            tps[0] = (xx, yy)
            for idx in range(1, len(tps)):
                tps[idx] = get_next_pos(tps[idx - 1], tps[idx])
            tail_set_p1.add(tps[tail_idx_p1])
            tail_set_p2.add(tps[tail_idx_p2])

        result_p1 = len(tail_set_p1)
        result_p2 = len(tail_set_p2)
        print(file_path, result_p1, result_p2)


if __name__ == "__main__":
    main()
