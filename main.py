import auto_correct as ac
from numpy import genfromtxt
import streamlit as st

arr = genfromtxt('vocab_frequencies.csv', delimiter=',', dtype=None)
freqs = {}
for word in arr:
    freqs[word[0]] = word[1]
vocab = list(freqs.keys())
print(len(vocab))
ac = ac.autocorrect()
word = st.text_input('Check spelling: ', '')
corrections = ac.get_corrections(word, freqs, vocab, n=4)
st.write('Most likely fixes: ')
for x in range(0, len(corrections)):
    st.write(str(x+1)+": ", corrections[x][0])
