import re, os
from itertools import chain


DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


class Node:
    def __init__(self):
        self.name = ''
        self.parent = None
        self.size = 0
        self.children = []

    def get_size(self):
        return self.size + sum(ch.get_size() for ch in self.children)

    def __iter__(self):
        yield self
        for ch in chain(*map(iter, self.children)):
            yield ch

    def __str__(self):
        return (f"{self.parent}/" if self.parent else '') + self.name


for file_path in FILE_PATHS:
    with open(file_path) as fr:
        inp = fr.read()

    root = Node()
    node = root

    for m in re.finditer(r'\$ (\w+)(?: (\w+|\/|..))?\n([\na-zA-Z0-9. ]*)?', inp, flags=re.DOTALL):
        cmd, arg, lines_str = m.groups()
        lines = [li for li in lines_str.split('\n') if li]
        assert cmd in ('cd', 'ls')
        if cmd == 'cd':
            assert not lines
            if arg == '/':
                node = root
            elif arg == '..':
                node = node.parent
            else:
                node = next(ch for ch in node.children if ch.name == arg)
            assert node
        else:
            assert lines
            for line in lines:
                p1, p2 = line.split(' ')
                ch = next((ch for ch in node.children if ch.name == p2), None)
                assert not ch
                ch = Node()
                ch.name = p2
                ch.parent = node
                node.children.append(ch)
                if p1 != 'dir':
                    ch.size = int(p1)

    dirs = [n for n in iter(root) if n.size == 0]
    result_p1 = sum(d.get_size() for d in dirs if d.get_size() <= 100000)

    avail_space = 70000000 - root.get_size()
    space_to_delete = 30000000 - avail_space
    sorted_dirs = sorted(dirs, key=lambda d: d.get_size())
    dir_to_delete = next(d for d in sorted_dirs if d.get_size() >= space_to_delete)
    result_p2 = dir_to_delete.get_size()

    print(file_path, result_p1, result_p2)
