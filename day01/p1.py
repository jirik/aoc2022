import os

DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    max_cal = 0
    with open(os.path.join(DIR, 'input.txt'), 'r') as f:
        curr_cal = 0
        for line in f:
            stripped = line.strip()
            if stripped:
                curr_cal += int(stripped)
            if not stripped or stripped == line:
                max_cal = max(max_cal, curr_cal)
                curr_cal = 0
    print(f"result={max_cal}")


if __name__ == "__main__":
    main()
