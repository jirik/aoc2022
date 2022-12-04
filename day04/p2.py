import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    def line_to_points(line):
        mn1, mx1, mn2, mx2 = (int(coord) for pair in line.split(',') for coord in pair.split('-'))
        pts = int(mn2 <= mn1 <= mx2 or mn2 <= mx1 <= mx2 or mn1 <= mn2 <= mx1 or mn1 <= mx2 <= mx1)
        # print(line, pts)
        return pts

    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip() for line in f.readlines()]

        result = sum(map(line_to_points, lines))
        print(file_path, result)


if __name__ == "__main__":
    main()
