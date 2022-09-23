# 111062693_HW1

## 增加Accuracy

- 一開始沒什麼方向，所以參考了Peter Norvig內關於**Future Work**的部分，其中最可能做出來的部分就是改進error model，所以我在`edits1`以及`edits2`之前增加了兩個`Priority`

```python
def Priority_1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 1: single letter -> doubling letters (ex. aple -> apple)"
    doubling   = [L + R[0] + R               for L, R in splits if R]
    return doubling

def Priority_2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in Priority_1(word) for e2 in Priority_1(e1))
```

增加之後在`development_set.txt`的測試上有增加2%的精確度

`77% of 270 correct (6% unknown) at 84 words per second`

---

- 經過觀察**output**，發現樣本有很多單字只缺少一個字母，所以把`edits1`的inserts單獨拿出來改成`Priority_3`

```python
def Priority_3(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 3: insert letter (ex. juce -> juice)"
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return inserts
```

增加之後在`development_set.txt`的測試上有增加3%的精確度，相較原本提升5%

`80% of 270 correct (6% unknown) at 84 words per second`

---

- try and error的過程中發現，把`known([word])`的位置移到`[word]`之前，居然可以增加準確度，猜測是把一些語料庫內不存在的字直接輸出反而會是正確的答案？

```python
def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known(Priority_1(word)) or known(Priority_2(word)) or known(Priority_3(word)) 
or known(edits1(word)) or  known(edits2(word)) or [word] or known([word]))
```

增加之後在`development_set.txt`的測試上有增加1%的精確度，相較原本提升6%

`81% of 270 correct (6% unknown) at 82 words per second`

---

## 增加Accuracy？

- 以上前兩點都是透過觀察原本`development_set.txt`的結果做 improvement ，我猜結果會跟真實的數據差很多，後來做了許多資料查詢，發現錯誤單字裡有很高的機率是因為母音（a、e、i、o、u）輸入錯誤，所以增加`Priority_4`

```python
def Priority_4(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    "Priority 4: vowel replace (ex. juuce -> juice)"
    vowels    = 'aeiou'
    replaces   = [L + c + R[1:]           for L, R in splits if R if R[0] == 'a' or R[0] == 'e' or R[0] == 'i' or R[0] == 'o' or R[0] == 'u' for c in vowels]
    return replaces
```

增加之後在`development_set.txt`的測試上反而減少1%的精確度

`80% of 270 correct (6% unknown) at 84 words per second`

---

## 減少Accuracy

- 觀察發現有很多錯字是拚音錯誤，像是`correction(lauf) => last (565); expected laugh (70)`，嘗試一個一個修改，結果卻造成精確度下降，猜測這些都是少數例子，更改反而會讓大部分一般的情況跑不到`edits1`以及`edits2`所以造成準確度下降。

---