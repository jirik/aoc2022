from puzzle_input import STRINGS


def get_idx(msg, ln):
    return next(i for i in range(len(msg)) if len(set((list(msg[i:i + ln])))) == ln) + ln


for msg in STRINGS:
    idx_p1 = get_idx(msg, 4)
    idx_p2 = get_idx(msg, 14)

    print(idx_p1, idx_p2)
