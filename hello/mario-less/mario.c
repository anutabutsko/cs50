#include <cs50.h>
#include <stdio.h>

int getValue();
void draw(int h);

int main(void)
{
    int h = getValue();
    draw(h);
}

int getValue()
{
    int n;
    do
    {
        n = get_int("Choose the height of the Pyramid. Positive Number between 1 and 8: ");
    }
    while (n < 1 || n > 8);;

    return n;
}

void draw(int h)
{
   for (int r = 0; r < h; r++)
{
    for (int s = r + 1; s < h; s++)
    {
        printf(" ");
    }

    for (int hash = h + r + 1; hash > h; hash--)
    {
        printf("#");
    }
    printf("\n");
}
}
