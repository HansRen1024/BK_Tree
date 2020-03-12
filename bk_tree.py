import pickle, editdistance, sys
from collections import deque
from operator import itemgetter
sys.setrecursionlimit(100000)
_getitem0 = itemgetter(0)

def hamming_distance(x, y):
    return bin(x ^ y).count('1')

def edit_distance(x,y):
    return editdistance.eval(x,y)

class BKTree(object):
    def __init__(self, distance_func, items=None):
        if items is None:
            items = []
        self.distance_func = distance_func
        self.tree = None

        _add = self.add
        for item in items:
            _add(item)

    def add(self, item):
        node = self.tree
        if node is None:
            self.tree = (item, {})
            return
        # Slight speed optimization -- avoid lookups inside the loop
        _distance_func = self.distance_func
        while True:
            parent, children = node
            distance = _distance_func(item, parent)
            node = children.get(distance)
            if node is None:
                children[distance] = (item, {})
                break

    def find(self, item, n):
        if self.tree is None:
            return []
        candidates = deque([self.tree])
        found = []
        # Slight speed optimization -- avoid lookups inside the loop
        _candidates_popleft = candidates.popleft
        _candidates_extend = candidates.extend
        _found_append = found.append
        _distance_func = self.distance_func
        while candidates:
            candidate, children = _candidates_popleft()
            distance = _distance_func(candidate, item)
            if distance <= n:
                _found_append((distance, candidate))
            if children:
                lower = distance - n
                upper = distance + n
                _candidates_extend(c for d, c in children.items() if lower <= d <= upper)
        found.sort(key=_getitem0)
        return found

    def __iter__(self):
        if self.tree is None:
            return
        candidates = deque([self.tree])
        # Slight speed optimization -- avoid lookups inside the loop
        _candidates_popleft = candidates.popleft
        _candidates_extend = candidates.extend
        while candidates:
            candidate, children = _candidates_popleft()
            yield candidate
            _candidates_extend(children.values())

    def __repr__(self):
        return '<{} using {} with {} top-level nodes>'.format(
            self.__class__.__name__,
            self.distance_func.__name__,
            len(self.tree[1]) if self.tree is not None else 'no',
        )

def saveTree():
    path = ""
    tree = BKTree(edit_distance, [])
    with open(path + "corpus.txt", 'r', encoding='utf-8') as fout:
        nameList = fout.readlines()
    for num, Name in enumerate(nameList):
        if num%10000==0: print(f"{num}/{len(nameList)}")
        # if num == 5000: break
        tree.add(Name.strip("\n"))
    sorted(tree)
    with open(path+"BKTree_data.bin", 'wb') as f:
        pickle.dump(tree.tree, f)

class bk_tree(object):
    def __init__(self, treeFile):
        self.tree = BKTree(edit_distance, [])
        with open(treeFile, 'rb') as f:
            self.tree.tree = pickle.load(f)
    def eval(self, item, distance):
        return self.tree.find(item, distance)

def testTree():
    asd = bk_tree("BKTree_data.bin")
    with open("corpus.txt", 'r', encoding='utf-8') as fout:
        nameList = fout.readlines()
    for num, Name in enumerate(nameList):
        if num % 10000 == 0: print(f"{num}/{len(nameList)}")
        a = asd.eval(Name.strip("\r\n"), 0)
        if a[0][0] > 1:
            print(a)

if __name__=='__main__':
    # saveTree()
    testTree()

