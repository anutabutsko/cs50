import random

word_list = ['management', 'user', 'language', 'complaint', 'series', 'manufacturer', 'airport', 'percentage',
             'disk', 'aspect', 'solution', 'imagination', 'session', 'ladder', 'poetry', 'historian', 'variety',
             'pie', 'birthday', 'family', 'depression', 'photo', 'understanding', 'satisfaction', 'reflection',
             'depth', 'hair', 'chest', 'law', 'army', 'disease', 'inspector', 'application', 'maintenance', 'two',
             'basket', 'interaction', 'people', 'lake', 'marriage', 'opportunity', 'presence', 'paper', 'speaker',
             'chemistry', 'basis', 'psychology', 'government', 'guitar', 'revolution', 'setting', 'bonus',
             'consequence',
             'selection', 'student', 'awareness', 'child', 'college', 'disease', 'signature', 'operation',
             'competition',
             'beer', 'potato', 'distribution', 'midnight', 'growth', 'internet', 'king', 'environment', 'reaction',
             'extent', 'bath', 'passenger', 'depth', 'apartment', 'bathroom', 'employer', 'responsibility',
             'restaurant',
             'tale', 'worker', 'farmer', 'criticism', 'concept', 'health', 'celebration', 'grocery', 'area', 'actor',
             'church', 'month', 'mode', 'atmosphere', 'recipe', 'topic', 'vehicle', 'pollution', 'phone']


# function that generates a random word
def get_word(words):
    return random.choice(words).upper()


# function that returns current state of the hangman
def display_hangman(tries):
    stages = [  # end state: head, body, both arms and both legs
        '''
           +------+
           |      |
           |      Ọ
           |     ⎛▼⎞
           |     ⎛ ⎞
           |
           =============+
           ================+
        ''',
        # head, body, both arms and one leg
        '''
           +------+
           |      |
           |      Ọ
           |     ⎛▼⎞
           |     ⎛
           |
           =============+
           ================+
        ''',
        # head, body and both arms
        '''
           +------+
           |      |
           |      Ọ
           |     ⎛▼⎞
           |
           |
           =============+
           ================+
        ''',
        # head, body and one arm
        '''
           +------+
           |      |
           |      Ọ
           |     ⎛▼
           |
           |
           =============+
           ================+
        ''',
        # head and body
        '''
           +------+
           |      |
           |      Ọ
           |      ▼
           |
           |
           =============+
           ================+
        ''',
        # head
        '''
           +------+
           |      |
           |      Ọ
           |
           |
           |
           =============+
           ================+
        ''',
        # beginning state
        '''
           +------+
           |      |
           |
           |
           |
           |
           =============+
           ================+
        '''
    ]
    return stages[tries]


word = get_word(word_list)


def play(word):
    word_completion = '_' * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    sym = '!@#$%^&*()-=+/\\.?,'
    name = input('What is your name?   ')
    print(f'''Hello, {name}! Welcome to "Hangman"!
        The Bot has chosen a word for you, and now your task is to guess it.
        Remember: 6 mistakes - and you\'ll find yourself hanging on the gallows.
        Good luck!''')
    print(f'The chosen word has {len(word)} letters. Let\'s begin!')
    print(display_hangman(tries))
    print(word_completion)

    while tries != 0 and guessed is False:
        print('Enter the letter, you think, is in the hidden word: ')
        a = input().upper()
        if a.isalpha() is False or a in sym:
            a = input('You must enter a letter!').upper()
            print()
        elif a in guessed_letters or a in guessed_words:
            a = input('You have already named this letter. Try another one:   ').upper()
            print()
        if a in word and len(a) == 1:
            guessed_letters.append(a)
            for i in range(len(word)):
                if word[i] == a:
                    word_completion = word_completion[:i] + a + word_completion[i + 1:]
            print(word_completion)
            if word_completion == word:
                guessed = True
                return print('Congratulations, you guessed the word. You win!')
        elif a == word:
            guessed = True
            return print('Congratulations, you guessed the word. You win!')
        elif a != word and len(a) == len(word):
            tries -= 1
            print("Wrong guess :( Try again!")
            print(display_hangman(tries))
            guessed_words.append(a)
        elif a not in word and len(a) == 1:
            guessed_letters.append(a)
            tries -= 1
            print("Wrong guess :( Try again!")
            print(display_hangman(tries))

    return print(f'You lose!\nThe hidden word was {word}')


play(word)
