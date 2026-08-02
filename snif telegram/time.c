#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int n = 10000000;
    char *prime = malloc(n + 1);

    time_t start = time(NULL);

    for (int i = 0; i <= n; i++)
        prime[i] = 1;

    prime[0] = prime[1] = 0;

    for (int i = 2; i * i <= n; i++) {
        if (prime[i]) {
            for (int j = i * 2; j <= n; j += i) {
                prime[j] = 0;
            }
        }
    }

    time_t end = time(NULL);

    printf("Done in %.2f seconds.\n", difftime(end, start));

    free(prime);
    return 0;
}
