from bayes import NaiveBayesClassifier
from string import punctuation


def clean_data(texts):
    texts = [i.lower() for i in texts]
    texts = [i.replace('\n', ' ').replace('\r', ' ') for i in texts]
    texts = [i.split() for i in texts]
    texts = [[word for word in i if word not in punctuation] for i in texts]
    texts = [' '.join(i) for i in texts]
    return texts


def split_data(X, y):
    X_train = X[:int(len(X) * 0.7)]
    y_train = y[:int(len(y) * 0.7)]
    X_test = X[int(len(X) * 0.7):]
    y_test = y[int(len(y) * 0.7):]
    return X_train, y_train, X_test, y_test


def main():
    with open("data/SMSSpamCollection", "r", encoding="utf-8") as f:
        data = f.readlines()
    types = [data.split("\t")[1].strip() for data in data]
    texts = [data.split("\t")[0].strip() for data in data]
    texts = clean_data(texts)
    X_train, y_train, X_test, y_test = split_data(types, texts)
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    print("Accuracy: ", model.score(X_test, y_test))


if __name__ == "__main__":
    main()
