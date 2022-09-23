"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re
from collections import Counter
import os

def words(text): return re.findall(r'\w+', text.lower())

path = "{}".format(os.getcwd())
WORDS = Counter(words(open(path + '/hw1/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known(Priority_1(word)) or known(Priority_2(word)) or known(Priority_3(word)) or known(Priority_4(word)) or known(edits1(word)) or  known(edits2(word)) or [word] or known([word]))

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def Priority_1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 1: single letter -> doubling letters (ex. aple -> apple)"
    doubling   = [L + R[0] + R               for L, R in splits if R]
    return doubling

def Priority_2(word): 
    "Priority 2: two edits of Priority 1"
    return (e2 for e1 in Priority_1(word) for e2 in Priority_1(e1))

def Priority_3(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 3: insert letter (ex. juce -> juice)"
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return inserts

def Priority_4(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 4: vowel replace (ex. juuce -> juice)"
    vowels    = 'aeiou'
    replaces   = [L + c + R[1:]           for L, R in splits if R if R[0] == 'a' or R[0] == 'e' or R[0] == 'i' or R[0] == 'o' or R[0] == 'u' for c in vowels]
    return replaces

################ Test Code 

def unit_tests():
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(WORDS) == 32192
    assert sum(WORDS.values()) == 1115504
    assert WORDS.most_common(10) == [
     ('the', 79808),
     ('of', 40024),
     ('and', 38311),
     ('to', 28765),
     ('in', 22020),
     ('a', 21124),
     ('that', 12512),
     ('he', 12401),
     ('was', 11410),
     ('it', 10681)]
    assert WORDS['the'] == 79808
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.perf_counter()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.perf_counter() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


spelltest(Testset(open(path + '/hw1/spell-testset1.txt')))

