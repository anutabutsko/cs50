#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string s);
int count_words(string s);
int count_sentences(string s);

int main(void)
{
    string text = get_string("Text: ");

    float letters_per_100_words = (float)count_letters(text) / (float)count_words(text) * 100.0;
    float sentences_per_100_words = (float)count_sentences(text) / (float)count_words(text) * 100.0;

    int index = round(0.0588 * letters_per_100_words - 0.296 * sentences_per_100_words - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string s)
{
    float letters = 0.0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isalpha(s[i]))
        {
            letters += 1.0;
        }
    }
    return letters;
}

int count_words(string s)
{
    float words = 1.0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isspace(s[i]))
        {
            words += 1.0;
        }
    }
    return words;
}

int count_sentences(string s)
{
    float sentences = 0.0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == '.' || s[i] == '?' || s[i] == '!')
        {
            sentences += 1.0;
        }
    }
    return sentences;
}