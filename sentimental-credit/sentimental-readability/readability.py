import re


def letters_count(text):
    total = 0
    for i in text:
        if i.isalpha():
            total += 1
    return total


def words_count(text):
    return len(text.split())


def sentences_count(text):
    return len(re.split('[.!?]', text)) - 1


text = input("Enter your text: ")

index = round(0.0588 * (letters_count(text) / words_count(text) * 100) -
              0.296 * (sentences_count(text) / words_count(text) * 100) - 15.8)

if index < 1:
    print('Before Grade 1')
elif index > 16:
    print('Grade 16+')
else:
    print(f'Grade {index}')
