class autocorrect:
    def __init__(self):
        self.letters = 'abcdefghijklmnopqrstuvwxyz'

    def split(self, word):
        """
        accepts:
        word: Word to insert letters into 
        outputs:
        split_list: list of tuples that have been split
        """
        split_list = [(word[:i + 1], word[i + 1:]) for i in range(len(word) - 1)]
        return split_list

    def insert(self, word):
        """
        accepts:
        split_word: list of tuples that have been split by each letter
        outputs:
        insert_list: list of words that have letters inserted into them
        """
        def insert_letter(L, letter, R):
            if len(R) > 0:
                return L + letter + R
            else:
                return L + R + letter 
        split_word = [(word[:i], word[i:]) for i in range(len(word))]
        insert_list = [insert_letter(L, letter, R) for L, R in split_word for letter in self.letters]
        return insert_list

    def delete(self, word):
        """
        accepts:
        word: list of tuples that have been split by each letter
        outputs:
        delete_list: list of words with letter deleted
        """
        split_word = [(word[:i], word[i:]) for i in range(len(word))]
        delete_list = [L + R[1:] for L, R in split_word]
        return delete_list


    def switch(self, word):
        """
        accepts:
        split_word: list of tuples that have been split by each letter
        outputs:
        switch_list: list of words with each letter switched
        """
        split_word = self.split(word)
        switch_list = [L[0:-1] + R[0] + L[-1] + R[1:] for L, R in split_word if R]
        return switch_list

    def replace(self, word):
        """
        accepts:
        split_word: list of tuples that have been split by each letter
        outputs:
        replace_list: List of words with replaced letters
        """
        split_word = [(word[:i], word[i:]) for i in range(len(word))]
        replace_list = [L + l + R[1:] for L, R in split_word if R for l in self.letters]
        replace_set = [value for value in replace_list if value != word]
        replace_list = sorted(list(replace_set))
        return replace_list

    def edit_one_letter(self, word, allow_switches = True):
        """
        Input:
            word: the string/word for which we will generate all possible wordsthat are one edit away.
        Output:
            edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
        """
        
        edit_one_set = set()
        
        i = self.insert(word)
        r = self.replace(word)
        d = self.delete(word)
        if allow_switches:
            s = self.switch(word)
            edit_one_set = i + r + d + s
        else:
            edit_one_set = i + r + d
        
        return set(edit_one_set)

    def edit_two_letters(self, word, allow_switches = True):
        '''
        Input:
            word: the input string/word 
        Output:
            edit_two_set: a set of strings with all possible two edits
        '''
        
        edit_two_set = set()
        first = self.edit_one_letter(word, allow_switches)
        for word in first:
            edit_two_set = edit_two_set.union(self.edit_one_letter(word, allow_switches))
        return set(edit_two_set)

    def get_corrections(self, word, probs, vocab, n=2):
        '''
        Input: 
            word: a user entered string to check for suggestions
            probs: a dictionary that maps each word to its probability in the corpus
            vocab: a set containing all the vocabulary
            n: number of possible word corrections you want returned in the dictionary
        Output: 
            n_best: a list of tuples with the most probable n corrected words and their probabilities.
        '''
        
        suggestions = []
        n_best = []
        
        most_likely = [word if word in vocab else self.edit_one_letter(word) or self.edit_two_letters(word) or word]
        suggestions = [word for word in most_likely[0] if word in vocab]
        suggestions.sort()
        probabilities = [(suggest, probs.get(suggest)) for suggest in suggestions]
        probabilities.sort(key = lambda x: x[1], reverse=True)
        n_best = probabilities[:n]

        return n_best
