import re
from collections import Counter
import streamlit as st

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    
    return WORDS[word] / N

def correction(word): 
    
    return max(candidates(word), key=P)

def candidates(word): 
    
    return (known(Priority_1(word)) or known(Priority_2(word)) or known(Priority_3(word)) or known(Priority_4(word)) or known(edits1(word)) or  known(edits2(word)) or [word] or known([word]))

def known(words): 
    
    return set(w for w in words if w in WORDS)

def edits1(word):
    
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def Priority_1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
   
    doubling   = [L + R[0] + R               for L, R in splits if R]
    return doubling

def Priority_2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in Priority_1(word) for e2 in Priority_1(e1))

def Priority_3(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return inserts

def Priority_4(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    
    vowels    = 'aeiou'
    replaces   = [L + c + R[1:]           for L, R in splits if R if R[0] == 'a' or R[0] == 'e' or R[0] == 'i' or R[0] == 'o' or R[0] == 'u' for c in vowels]
    return replaces

def Priority_5(word):
    return (e2 for e1 in Priority_4(word) for e2 in Priority_4(e1))

st.title("Spellchecker Demo")

original_word = st.sidebar.checkbox("Show original word")

select_word = st.selectbox('Choose a word or...', ('', 'apple', 'aple', 'banana', 'baanana'))

input_word = st.text_input('type your own!', value=select_word)


if (original_word):
    if input_word:
        st.text('Original word: ' + input_word)

if input_word:
    if correction(input_word) == input_word:
        st.success(input_word + ' is the correct spelling!')
    else:
        st.error('Correction:' + correction(input_word))


