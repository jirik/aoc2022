import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [[int(c) for c in line.strip()] for line in f.readlines()]

        visible_count = 0
        max_score = 0
        for r_idx, row in enumerate(lines):
            for c_idx, value in enumerate(row):
                # part 1
                groups = [row[:c_idx], row[c_idx+1:], [r[c_idx] for r in lines[:r_idx]], [r[c_idx] for r in lines[r_idx+1:]]]
                visibles = [g for g in groups if all(t < value for t in g)]
                if len(visibles):
                    visible_count += 1

                # part 2
                left = c_idx - next((i for i in reversed(range(c_idx)) if row[i] >= value), 0)
                top = r_idx - next((i for i in reversed(range(r_idx)) if lines[i][c_idx] >= value), 0)
                right = next((i for i in range(c_idx+1, len(row)) if row[i] >= value), len(row) - 1) - c_idx
                bottom = next((i for i in range(r_idx+1, len(lines)) if lines[i][c_idx] >= value), len(lines) - 1) - r_idx
                max_score = max(max_score, left*top*right*bottom)

        result_p1 = visible_count
        result_p2 = max_score
        print(file_path, result_p1, result_p2)


if __name__ == "__main__":
    main()
