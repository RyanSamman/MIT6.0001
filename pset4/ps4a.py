# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from math import sqrt
from os import get_exec_path


def get_permutations(sequence: str, i=1):
    # TODO: Learn backtracking in detail
    if len(sequence) == 1:
        return [sequence]

    permutations = []

    for i, c in enumerate(sequence):
        possibilitySpace = sequence.replace(c, "", 1) # Remove 1 of current character
        for p in get_permutations(possibilitySpace):
            permutations.append(c + p)

    return permutations

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    def testPerms(generated, actual):
        if len(generated) != len(actual):
            return False
        
        return all(i1 == i2 for i1, i2 in zip(generated, actual))

    assert testPerms(get_permutations("a"), ["a"])
    assert testPerms(get_permutations("ab"), ["ab", "ba"])
    assert testPerms(get_permutations("abc"), ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print("All tests pass!")

    s = input("Get Permutations of: ")
    print(get_permutations(s))

    