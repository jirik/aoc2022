import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]

LETTERS = {
    'A': 0,
    'B': 1,
    'C': 2,
    'X': 2,
    'Y': 0,
    'Z': 1,
}


def main():
    def line_to_points(line):
        him, res = [LETTERS[ltr] for ltr in line.split(' ')]
        me = (res + him) % 3
        return ((res + 1) % 3) * 3 + me + 1

    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip() for line in f.readlines()]

        result = sum(map(line_to_points, lines))
        print(file_path, result)


if __name__ == "__main__":
    main()
