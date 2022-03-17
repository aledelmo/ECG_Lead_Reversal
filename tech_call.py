#!/usr/bin/env python
# coding:utf-8

"""

Author : Alessandro Delmonte
Contact : alessandro.delmonte@institutimagine.org

Questions:
Given a string. What is the first unique character?

1. Implement the first_unique() function
2. What is the complexity of this function ?
Write down one or two comment lines explaining why.
"""


def first_unique(s):
    first_time = set()
    deja_vu = set()
    for c in s:
        if c not in first_time:
            first_time.add(c)
        else:
            deja_vu.add(c)
    uniques = first_time - deja_vu
    for c in s:
        if c in uniques:
            return c
    return None


if __name__ == '__main__':
    assert first_unique('aba') == 'b', "Failed test 1"
    assert first_unique('abca') == 'b', "Failed test 2"
    assert first_unique('aa') is None, "Failed test 3"
    print("OK")

