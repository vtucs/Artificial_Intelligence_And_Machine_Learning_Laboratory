"""
2. For a given set of training data examples stored in a '.CSV file', implement and
demonstrate the Candidate-Elimination algorithm to output a description of the set
of all hypotheses consistent with the training examples.
"""

import csv

with open('ds1.csv') as csvFile:
    data = [tuple(line) for line in csv.reader(csvFile)]


def domain():
    D = []
    for i in range(len(data[0])):
        D.append(list(set([ele[i] for ele in data])))
    return D


D = domain()


def is_consistent(h1, h2):
    for x, y in zip(h1, h2):
        if x != "?" and (x == "o" or x != y):
            return False
    return True


def candidate_elimination():
    G = {('?',) * (len(data[0]) - 1), }
    S = ['o'] * (len(data[0]) - 1)
    no = 0
    print("\n G[{0}]:".format(no), G)
    print("\n S[{0}]:".format(no), S)
    for item in data:
        no += 1
        inp, res = item[:-1], item[-1]
        if res in "Yy":
            i = 0
            G = {g for g in G if is_consistent(g, inp)}
            for s, x in zip(S, inp):
                if not s == x:
                    S[i] = '?' if s != 'o' else x
                i += 1
        else:
            Gprev = G.copy()
            for g in Gprev:
                if g not in G:
                    continue
                for i in range(len(g)):
                    if g[i] == "?":
                        for val in D[i]:
                            if inp[i] != val and val == S[i]:
                                g_new = g[:i] + (val,) + g[i + 1:]
                                G.add(g_new)
                    else:
                        G.add(g)
                G.difference_update([h for h in G if
                                     any([is_consistent(h, g1) for g1 in G if h != g1])])
        print("\n G[{0}]:".format(no), G)
        print("\n S[{0}]:".format(no), S)


if __name__ == '__main__':
    candidate_elimination()

"""
Output:

 G[0]: {('?', '?', '?', '?', '?', '?')}

 S[0]: ['o', 'o', 'o', 'o', 'o', 'o']

 G[1]: {('?', '?', '?', '?', '?', '?')}

 S[1]: ['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same']

 G[2]: {('?', '?', '?', '?', '?', '?')}

 S[2]: ['Sunny', 'Warm', '?', 'Strong', 'Warm', 'Same']

 G[3]: {('?', '?', '?', '?', '?', 'Same'), ('?', 'Warm', '?', '?', '?', '?'), ('Sunny', '?', '?', '?', '?', '?')}

 S[3]: ['Sunny', 'Warm', '?', 'Strong', 'Warm', 'Same']

 G[4]: {('?', 'Warm', '?', '?', '?', '?'), ('Sunny', '?', '?', '?', '?', '?')}

 S[4]: ['Sunny', 'Warm', '?', 'Strong', '?', '?']
"""
