import json, os, math, functools

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input.txt'),
]


def sign(n):
    return n if not n else math.copysign(1, n)


def compare(l, r):
    lt = type(l)
    rt = type(r)
    if lt == int and rt == int:
        return sign(l - r)
    l = l if lt == list else [l]
    r = r if rt == list else [r]
    for lc, rc in zip(l, r):
        cres = compare(lc, rc)
        if cres:
            return cres
    return sign(len(l) - len(r))


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            lines = [line.strip() for line in fr.readlines()]

        pairs = [(json.loads(lines[i*3]), json.loads(lines[i*3+1])) for i in range(len(lines)//3)]

        r1 = sum(idx + 1 if b == -1 else 0 for idx, b in enumerate([compare(*p) for p in pairs]))

        pairs = [pp for p in pairs for pp in p]
        divs = [[[2]], [[6]]]
        pairs.extend(divs)
        pairs.sort(key=functools.cmp_to_key(compare))

        divs = [json.dumps(d) for d in divs]
        idxs = [i+1 for i in range(len(pairs)) if json.dumps(pairs[i]) in divs]
        r2 = idxs[0] * idxs[1]
        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
