import os
from itertools import islice

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    def group_to_points(group):
        wrong_items = set.intersection(*[set(line) for line in group])
        assert len(wrong_items) == 1
        wrong_item = next(iter(wrong_items))
        ascii_val = ord(wrong_item)
        pts = ascii_val - 96 if ascii_val > 96 else ascii_val - 38
        # print(wrong_item, pts)
        return pts

    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip() for line in f.readlines()]

        group_size = 3
        groups = [lines[i:i + group_size] for i in range(0, len(lines), group_size)]

        result = sum(map(group_to_points, groups))
        print(file_path, result)


if __name__ == "__main__":
    main()
