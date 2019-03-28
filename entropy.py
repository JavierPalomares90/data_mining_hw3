# Python class to compute the entropy of words from the text in the pdfs.
# Must be executed after scraper.py writes word_freqs.txt

WORD_FREQ_FILE= 'word_freqs.txt'
K = 1.0
import math


def get_word_prob():
    word_probs = {}
    total_word_count = 0
    with open(WORD_FREQ_FILE,'r') as f:
        line = f.readline()
        while line:
            tokens = line.split()
            word = tokens[0]
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

def main():
    word_probs = get_word_prob()
    H = compute_entropy(word_probs)
    print("The computed entropy for the pdf text is {}".format(H))

if __name__=='__main__':
    main()

