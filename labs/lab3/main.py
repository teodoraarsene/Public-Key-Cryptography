"""
generalized Fermat's algorithm
it will first consider k = 1 and, if not successful, it will consider k = 2, 3, ... until getting a factor
    - input: an odd composite number n (which is not a square) and a suitable bound B
    - output: a non-trivial factor of n

algorithm:
    for k = 1, 2, ... do
        let t0 = [(k*n)^(1/2)]
        for t = t0 + 1, ..., t0 + B do
            if t^2 - k*n is a square s^2, then
                s^2 = t^2 - k*n
                n = 1/k * (t - s) * (t + s)
"""


def is_square(no: int) -> bool:
    return no ** (1 / 2) % 1 == 0


def generalized_fermat_algorithm(n: int, bound: int) -> tuple[int, int, int]:
    if n % 2 == 0:
        print(f'{n} must be an odd number!')
        return -1, -1, -1

    k = 1
    while True:
        t0 = int((k * n) ** (1 / 2))

        for b in range(1, bound + 1):
            t = t0 + b
            if is_square(t ** 2 - k * n):
                s = (t ** 2 - k * n) ** (1 / 2)
                n = (1 / k) * (t - s) * (t + s)
                return int(n), t, int(s)

        k += 1


if __name__ == '__main__':
    n, t, s = generalized_fermat_algorithm(200819, 5)
    print(f'{n} = ({t} + {s}) * ({t} - {s}) = {t + s} * {t - s}')

    n, t, s = generalized_fermat_algorithm(141467, 50)
    print(f'{n} = ({t} + {s}) * ({t} - {s}) = {t + s} * {t - s}')
