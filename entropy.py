# Python class to compute the entropy of words from the text in the pdfs.
# Must be executed after scraper.py writes word_freqs.txt

WORD_FREQ_FILE= 'word_freqs.txt'
PARAGRAPH_NUM_WORDS = 30
FREQUENCY_PATH = "/freqs/"

K = 1.0
import math
import numpy as np
from alphabet_detector import AlphabetDetector
from os import listdir
from os.path import isfile, join


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

# return a list of the frequency a word per file
def get_all_freq_files():
    files = [f for f in listdir(FREQUENCY_PATH) if isfile(join(FREQUENCY_PATH, f))]

    word_prob_all_files = []
    for file in files:
        file_word_prob = {}
        path = FREQUENCY_PATH + file
        with open(path,'r') as f:
            line = f.readline()
            while line:
                tokens = line.split()
                word = tokens[0]
                prob = float(tokens[1])
                file_word_prob[word] = prob
                line = f.readline()
        word_prob_all_files.append(file_word_prob)
    return word_prob_all_files



def compute_entropy_random_word_random_paper(words,word_prob_all_files):
    H = 0
    # iterate over all the words
    num_words = len(words)
    num_files = len(word_prob_all_files)
    for word in words:
        p = 0
        # iterate over the word distribution per file
        for word_prob in word_prob_all_files:
            # all files are equally likely, so divide by the number of files
            prob = word_prob.get(word,0) * 1.0 / num_files
            p += prob
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
    words = all_word_probs.keys()
    word_prob_all_files = get_all_freq_files()
    H = compute_entropy_random_word_random_paper(words,word_prob_all_files)
    print("The computed entropy for the pdf text is {}".format(H))
    print(first_order_synthesized_paragraph(get_word_prob(False),PARAGRAPH_NUM_WORDS))

if __name__=='__main__':
    main()

