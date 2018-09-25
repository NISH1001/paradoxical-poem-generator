import random
import re

from collections import defaultdict

import sys

class MarkovChain:
    def __init__(self, lookback=2):
        self.trie = defaultdict(lambda : defaultdict(int))
        self.lookback = lookback
        self.lines = []

    def train(self, lines):
        """
            Build markov model
        """
        self.lines += lines
        for title in lines:
            tokens = title.split()
            if len(tokens) > self.lookback:
                for i in range(len(tokens) + 1):
                    a = ' '.join(tokens[max(0, i-self.lookback) : i])
                    b = ' '.join(tokens[i : i+1])
                    self.trie[a][b] += 1
        self._build_probabilities()

    def _build_probabilities(self):
        """
            Calculate probabilities
        """
        for word, following in self.trie.items():
            total = float(sum(following.values()))
            for key in following:
                following[key] /= total

    def _sample(self, items):
        next_word = None
        t = 0.0
        for k, v in items:
            t += v
            if t and random.random() < v/t:
                next_word = k
        return next_word

    def generate(self, n):
        sentences = []
        while len(sentences) < n:
            sentence = []
            next_word = self._sample(self.trie[''].items())
            while next_word != '':
                sentence.append(next_word)
                next_word = self._sample(self.trie[' '.join(sentence[-self.lookback:])].items())
            sentence = ' '.join(sentence)
            flag = True
            for title in self.lines: #Prune lines that are substrings of actual lines
                if sentence in title:
                    flag = False
                    break
            if flag:
                sentences.append(sentence)
        return sentences

def load_data(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line.strip())
    return lines


def main():
    n = sys.argv[1:]
    msg = "LOL! You have to supply the total number of lines to generate."\
            + "Or else humanity will go extinct right now..."
    if not n:
        print(msg.strip())
    else:
        n = int(n[0])
        data = load_data("data/poem")
        mc = MarkovChain(lookback=1)
        mc.train(data)

        lines = mc.generate(n)
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()


