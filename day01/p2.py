import bisect
import os

DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    max_cals = []
    with open(os.path.join(DIR, 'input.txt'), 'r') as f:
        curr_cal = 0
        for line in f:
            stripped = line.strip()
            if stripped:
                curr_cal += int(stripped)
            if not stripped or stripped == line:
                if len(max_cals) < 3 or curr_cal > max_cals[0]:
                    bisect.insort_right(max_cals, curr_cal)
                if len(max_cals) > 3:
                    max_cals.pop(0)
                curr_cal = 0
    print(f"result={sum(max_cals)}")


if __name__ == "__main__":
    main()
