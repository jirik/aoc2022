import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    def line_to_points(line):
        comp1 = line[:len(line)//2]
        comp2 = line[len(line)//2:]
        wrong_items = set(comp1).intersection(comp2)
        assert len(wrong_items) == 1
        wrong_item = next(iter(wrong_items))
        ascii_val = ord(wrong_item)
        pts = ascii_val - 96 if ascii_val > 96 else ascii_val - 38
        # print(wrong_item, pts)
        return pts

    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip() for line in f.readlines()]

        result = sum(map(line_to_points, lines))
        print(file_path, result)


if __name__ == "__main__":
    main()
