import math
import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input2.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip().split(' ') for line in f.readlines()]

        cmds = [0 if not p_idx else int(n) for parts in lines for p_idx, n in enumerate(parts)]

        sprite = 1
        w = 40
        print(file_path)
        for r_idx in range(math.ceil(len(cmds) / w)):
            s = ''
            for c_idx, cmd in enumerate(cmds[r_idx*w:(r_idx+1)*w]):
                ch = '#' if sprite - 1 <= c_idx <= sprite + 1 else '.'
                s += ch
                sprite += cmd
            print(s)


if __name__ == "__main__":
    main()
