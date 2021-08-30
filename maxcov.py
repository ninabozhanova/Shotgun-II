from typing import Tuple, Dict
from itertools import combinations

def greedy(S:Dict[None, set], k:int, remaining:list=None)->Tuple[list,int]:
    if remaining == None: remaining = list(S.keys())
    not_covered = set()
    out = list()
    for Si in S:
        not_covered.update(S[Si])
    covered = set()
    for i in range(k):
        next_choice = sorted(remaining, key=lambda x: len(S[x].intersection(not_covered)), reverse=True)[0]
        not_covered -= S[next_choice]
        covered.update(S[next_choice])
        remaining.remove(next_choice)
        out.append(next_choice)

    return out, len(covered)

def bigStepGreedy(S:Dict[None, set], k:int, p:int, remaining:list=None)->Tuple[list,int]:
    if remaining == None: remaining = list(S.keys()) # S\C
    C = list()           # S
    not_covered = set()  # W
    covered = set()
    for Si in S:
        not_covered.update(S[Si])
    while(len(C) < k):
        if k-len(C) < p:
            q = k-len(C)
        else:
            q = p
        # options = sorted(combinations(remaining, q), key=lambda x:len(set.union(*[S[y] for y in x]).intersection(not_covered)), reverse=True)
        best = 0
        best_choice = None
        for option in combinations(remaining, q):
            val = len(set.union(*[S[y] for y in option]).intersection(not_covered))
            if val > best:
                best = val
                best_choice = option

        next_choices_k = best_choice
        next_choices_v = [S[x] for x in next_choices_k]
        covered.update(set.union(*next_choices_v))
        for x in next_choices_v:
            not_covered -= x
        C.extend(next_choices_k)
        for nk in next_choices_k:
            remaining.remove(nk)
        print(f"{len(C)}")
    return C, len(covered)

def main():
    S = {
        'S1':{'a', 'b', 'c', 'd', 'e', 'f'},
        'S2':{'a', 'b', 'c', 'g', 'h'},
        'S3':{'d', 'e', 'f', 'i', 'j'},
        'S4':{'g', 'h', 'i'},
        'S5':{'k', 'l'}
    }

    greedyResult, greedyCovered = greedy(S, 3)
    print("Greedy")
    print(greedyResult)
    print(greedyCovered)
    print()

    print("Big Step Greedy")
    print(bigStepGreedy(S, 3, 2))

if __name__ == '__main__':
    main()