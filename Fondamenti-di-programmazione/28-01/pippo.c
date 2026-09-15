#include <stdio.h>
int main(int argc, char const *argv[])
{
    printf("Testing continue statement\n");
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0)
        {
            printf("This is an even number: %d\n", i); // Skip even numbers
            continue; // Skip the rest of the loop for even numbers
        }
         printf("This is an odd number: %d\n", i); // This will only print for odd numbers
    }
    
}
