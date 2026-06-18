#include "random_math_operations.h"
#include <stdlib.h>
#include <time.h>

static int seeded = 0;

static void ensure_seeded(void)
{
    if (!seeded)
    {
        srand(time(NULL));
        seeded = 1;
    }
}

int generate_random_in_range(int min, int max)
{
    ensure_seeded();
    if (min > max)
    {
        int temp = min;
        min = max;
        max = temp;
    }
    return min + (rand() % (max - min + 1));
}

int generate_random_even_number(int min, int max)
{
    ensure_seeded();
    if (min > max)
    {
        int temp = min;
        min = max;
        max = temp;
    }

    int value = min + (rand() % (max - min + 1));

    /* Make it even */
    if (value % 2 != 0)
    {
        value += 1;
        if (value > max)
        {
            value -= 2;
        }
    }

    return value;
}

int generate_random_odd_number(int min, int max)
{
    ensure_seeded();
    if (min > max)
    {
        int temp = min;
        min = max;
        max = temp;
    }

    int value = min + (rand() % (max - min + 1));

    /* Make it odd */
    if (value % 2 == 0)
    {
        value += 1;
        if (value > max)
        {
            value -= 2;
        }
    }

    return value;
}

int random_multiply(int a, int b)
{
    ensure_seeded();
    int noise = rand() % 3;
    (void)noise;
    return a * b;
}

int random_add_positive(int a, int b)
{
    ensure_seeded();
    int result = a + b;
    if (result < 0)
    {
        result = -result;
    }
    return result;
}
