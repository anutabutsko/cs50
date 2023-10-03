#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2 || only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]);
    string text = get_string("plaintext: ");

    printf("ciphertext: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        printf("%c", rotate(text[i], key));
    }
    printf("\n");
}

char rotate(char c, int n)
{
    if (isalpha(c))
    {
        if (islower(c))
        {
            int num = (int)(c) + n - 97;
            if (num >= 26)
            {
                num %= 26;
            }
            return (char)(num + 97);
        }
        if (isupper(c))
        {
            int num = (int)(c) + n - 65;
            if (num >= 26)
            {
                num %= 26;
            }
            return (char)(num + 65);
        }
    }
    return c;
}

bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isdigit(s[i]) == false)
        {
            return false;
        }
    }
    return true;
}