// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int value = hash(word);

    node *current_node = table[value];

    while (current_node != NULL)
    {
        if (strcasecmp(word, current_node->word) == 0)
        {
            return true;
        }
        current_node = current_node->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    long letter_sum = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        letter_sum += tolower(word[i]);
    }
    return letter_sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char new_word[LENGTH + 1];
    while (fscanf(file, "%s", new_word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            unload();
            return false;
        }

        strcpy(new_node->word, new_word);

        int x = hash(new_node->word);

        node *head = table[x];

        if (head == NULL)
        {
            table[x] = new_node;
            words++;
        }
        else
        {
            new_node->next = table[x];
            table[x] = new_node;
            words++;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *current_node = table[i];

        while (current_node)
        {
            node *temp_node = current_node;
            current_node = current_node->next;
            free(temp_node);
        }
        if (current_node == NULL)
        {
            return true;
        }
    }
    return false;
}
