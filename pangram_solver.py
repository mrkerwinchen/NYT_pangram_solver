from nltk.corpus import words
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import string

allwords = pd.DataFrame({'words':words.words()})
allwords = allwords.loc[allwords['words'].str.len() >= 4]
allwords['words'] = allwords['words'].str.lower()
allwords = allwords.reset_index()

mlb = MultiLabelBinarizer()
split_words = [list(i) for i in allwords['words']]
dummy = pd.DataFrame(mlb.fit_transform(split_words))
dummy.columns = mlb.classes_

def build_query(letters):
    return (query_builder(list(letters), 1) + ' & ' +
            query_builder(
            [letter for letter in string.ascii_lowercase if letter not in letters], 0))

def query_builder(letters, val):
    if len(letters) == 0:
        return ''
    return '(' + letters[0] + ' == ' + str(val) + ')' \
    if len(letters) == 1 \
    else '(' + letters[0] + ' == ' +str(val) + ') & ' + query_builder(letters[1:], val)

def score(word):
    return 7 + len(word) - 3

def solver(letters):
    letters = letters.lower()
    if not letters.isalpha():
        print("non-letters found")
        return
    terms = allwords.loc[dummy.query(build_query(letters)).index].words
    if len(terms) == 0:
        print('no solutions found')
        return
    max_length = max(terms.apply(len)) + 3
    print(f'Term{ (max_length - len("term")) * " " } | Score')
    print('-' * (max_length + 10))
    for i in terms:
        print(f'{i + (max_length - len(i) - 1) * " "}* |  {score(i)}')

def main():
    while True:
        print("\ntype '\\exit' to exit")
        puzzle = input('input pangram letters: ')
        if puzzle != "\\exit":
            solver(puzzle)
        else:
            print("exited\n")
            break


if __name__ == "__main__":
    main()
