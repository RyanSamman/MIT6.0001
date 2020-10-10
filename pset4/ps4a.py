# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from math import sqrt
from os import get_exec_path


def get_permutations(sequence: str, i=1):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

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
    print(get_permutations("abcdefghijklmnopqrstuvwxyz"))
    print("All tests pass!")
    