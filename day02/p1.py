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
    'X': 0,
    'Y': 1,
    'Z': 2,
}


def main():
    def line_to_points(line):
        him, me = [LETTERS[ltr] for ltr in line.split(' ')]
        res = (me - him + 1) % 3
        return res * 3 + me + 1

    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip() for line in f.readlines()]

        result = sum(map(line_to_points, lines))
        print(file_path, result)


if __name__ == "__main__":
    main()
