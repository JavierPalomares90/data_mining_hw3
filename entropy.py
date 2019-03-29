# Python class to compute the entropy of words from the text in the pdfs.
# Must be executed after scraper.py writes word_freqs.txt

WORD_FREQ_FILE= 'word_freqs.txt'
PARAGRAPH_NUM_WORDS = 30
K = 1.0
import math
import numpy as np
from alphabet_detector import AlphabetDetector


def get_word_prob(all_words=False):
    ad = AlphabetDetector()
    word_probs = {}
    total_word_count = 0
    with open(WORD_FREQ_FILE,'r') as f:
        line = f.readline()
        while line:
            tokens = line.split()
            word = tokens[0]
            # Only consider latin words by default
            if all_words or ad.only_alphabet_chars(word,"LATIN"):
                count = int(tokens[1])
                word_probs[word] = count
                total_word_count += count
            line = f.readline()
    # convert the count to a prob by dividing by the total count
    for word,count in word_probs.items():
        word_probs[word] = count / total_word_count
    return word_probs

def compute_entropy(word_probs):
    H = 0
    for word,p in word_probs.items():
        h = -1.0 * K * p * math.log(p,2)
        H += h
    return H

def verify_word_probs(word_probs):
    # verify the word probs sum up to 1.0
    s = 0.0
    for word,p in word_probs.items():
        s += p
    print("total prob: {}".format(s))

def first_order_synthesized_paragraph(word_probs,par_len):
    # synthesize a paragraph of the given length with the
    # given word probabilities
    words = list(word_probs.keys())
    weights = list(word_probs.values())
    paragraph = np.random.choice(words,par_len,p=weights)
    return ' '.join(paragraph)



def main():
    all_word_probs = get_word_prob(True)
    verify_word_probs(all_word_probs)
    H = compute_entropy(all_word_probs)
    print("The computed entropy for the pdf text is {}".format(H))
    print(first_order_synthesized_paragraph(get_word_prob(False),PARAGRAPH_NUM_WORDS))

if __name__=='__main__':
    main()

