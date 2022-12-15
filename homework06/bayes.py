import collections
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.words_count = 0
        self.types = set()
        self.words_enters = dict()
        self.types_enters = dict()

    def fit(self, texts_list, types_list):
        self.types = set(types_list)
        for type in self.types:
            self.types_enters[type] = 0
            self.words_enters[type] = collections.Counter()
        for text in range(len(texts_list)):
            self.types_enters[types_list[text]] += 1
            for word in texts_list[text].split(" "):
                self.words_count += 1
                self.words_enters[types_list[text]][word] += 1

    def predict(self, texts):
        guess = []
        for i in range(len(texts)):
            max_prob_type = None
            max_prob = -math.inf
            for type in self.types:
                prob = math.log(self.types_enters[type] / sum(self.types_enters.values()))
                for word in texts[i].split():
                    prob += math.log(
                        (self.words_enters[type][word] + self.alpha)
                        / (sum(self.words_enters[type].values()) + self.alpha * self.words_count)
                    )
                if prob > max_prob:
                    max_prob = prob
                    max_prob_type = type
            guess.append(max_prob_type)
        return guess

    def score(self, texts, types):
        guess = self.predict(texts)
        sum = 0
        for i in range(len(guess)):
            if guess[i] == types[i]:
                sum += 1
        return sum / len(guess)
