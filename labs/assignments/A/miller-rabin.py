import string
from assignments.utils import Style, Formatting


def is_set(number, n):
    # We use the binary "and" operator to mask the given number
    # and see if the Nth bit is set or not (a.k.a. is different than 0).
    # Reference: https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    return number & (1 << n) != 0


def repeated_squaring_modular_exponentiation(base: int, exponent: int, modulus: int):
    result: int = 1
    if exponent == 0:
        return result

    fragment: int = base

    if is_set(exponent, 0):
        result = fragment
    for bit_position in range(1, exponent.bit_length()):
        fragment = (fragment * fragment) % modulus
        if is_set(exponent, bit_position):
            result = (result * fragment) % modulus

    return result


def compute_from_number_exponent_of_factor(number: int, factor: int):
    # This computes the exponent of a given number's given factor.
    # 24 = 2^3 * 3 ==> compute_exponent_of_factor_from_number(24, 2) = 3
    exponent = 0
    while number % factor == 0:
        exponent += 1
        number /= factor
    return exponent


def binary_representation_of_number(number: int):
    return bin(number)[2:]


def print_necessary_powers_of_two(modulus: int, t: int):
    for necessary_power in range(10):
        end_type: string
        computed_value: string

        if necessary_power == 4 or necessary_power == 9:
            end_type = "\n"
        else:
            end_type = "\t\t\t"

        if necessary_power < t.bit_length():
            computed_value = str(2 ** (2 ** necessary_power) % modulus)
        else:
            computed_value = "x"

        print("2{} = ".format(Formatting.superscript(f"(2^{necessary_power})"))
              + Style.YELLOW + f"{computed_value}" + Style.RESET,
              end=end_type)


def miller_rabin(number: int, expected_sequence_size: int = 5):
    print("n = " + Style.YELLOW + str(number) + Style.RESET, end="\n\n")

    if number <= 2:
        print(Style.RED + "ERROR: Condition not met. (" + Style.CYAN + "n >= 3" + Style.RED + ")" + Style.RESET)
        return
    elif number % 2 == 0:
        print(Style.RED + "ERROR: Condition not met. (" + Style.CYAN + "n odd" + Style.RED + ")" + Style.RESET)
        return

    print("Decomposition:")

    # In order to get s and t, we know that:
    # n - 1 = 2^s * t
    s: int = compute_from_number_exponent_of_factor(number - 1, 2)
    print("s = " + Style.YELLOW + str(s) + Style.RESET, end="\t\t\t")

    t: int = (number - 1) >> s
    # It's similar to (n-1)/2^s.
    # Reference: https://wiki.python.org/moin/BitwiseOperators
    print("t = " + Style.YELLOW + str(t) + Style.RESET, end="\t\t\t")
    print("t (in binary) = " + Style.YELLOW + binary_representation_of_number(t) + Style.RESET, end="\n\n")

    iteration_count = 1
    is_not_prime_lazy_check: bool = False
    for a in [2, 3, 5]:
        is_possibly_prime: bool = False

        print("Iteration "
              + Style.YELLOW + f"k = {iteration_count}" + Style.RESET
              + " for "
              + Style.YELLOW + f"a = {a}" + Style.RESET
              + " (results mod "
              + Style.YELLOW + "n" + Style.RESET
              + "):")

        sequence = []

        # we need to compute a^t, a^(2t), a^(4t), ..., a^(2^s * t)
        # Step 2 of https://moodle.cs.ubbcluj.ro/pluginfile.php/46227/mod_resource/content/1/pkc-c03.pdf#page=20
        if a == 2:
            print_necessary_powers_of_two(number, t)
            print()

        # The Sequence Size will ALWAYS BE s + 1.
        # The quiz contains an expected Sequence Size of 5, but populates the remaining with "x"
        for r in range(expected_sequence_size):
            current_sequence_value: string
            if r < s + 1 and not is_not_prime_lazy_check:
                current_sequence_value = repeated_squaring_modular_exponentiation(a, 2 ** r * t, number)
                sequence.append(current_sequence_value)
            else:
                current_sequence_value = "x"

            end_type: string
            if r == expected_sequence_size - 1:
                end_type = "\n"
            else:
                end_type = "\t\t\t"

            print("{}{} = ".format(a, Formatting.superscript(f"2^{r}t"))
                  + Style.YELLOW + f"{current_sequence_value}" + Style.RESET, end=end_type)

        # Step 3 of https://moodle.cs.ubbcluj.ro/pluginfile.php/46227/mod_resource/content/1/pkc-c03.pdf#page=20
        if not is_not_prime_lazy_check:
            if sequence[0] == 1:
                is_possibly_prime = True
            else:
                for pair in list(zip(sequence[:-1], sequence[1:])):
                    if pair[0] == number - 1 and pair[1] == 1:
                        is_possibly_prime = True
                        break
            if not is_possibly_prime:
                is_not_prime_lazy_check = True

        iteration_count += 1
        print()

    print("Conclusion:", end="\n\n")
    print("n is prime (yes/no)= " + Style.YELLOW + ("yes" if is_possibly_prime else "no") + Style.RESET)
    print(Style.MAGENTA + f"Don't trust me? Try a Miller-Rabin calculator https://planetcalc.com/8995/" + Style.RESET,
          end="\n\n\n")


# This Function is used STRICTLY for solving Assignment A on Moodle,
# taking into account the amount of pages the test contains.
#
# You can also simply hardcode the number into the main function.
def show_ui_exam_version(page_count: int = 2):
    for page in range(page_count):
        while True:
            try:
                print(f"PAGE {page + 1}/2")
                user_input = int(input("Use the Miller-Rabin test to decide whether the number is prime or not. "
                                       "Number: "))
                miller_rabin(user_input)
                break
            except ValueError:
                print(Style.RED + "ERROR: Input is NOT a number." + Style.RESET, end="\n\n")
    print(Style.BLUE + "GOOD LUCK!" + Style.RESET)


if __name__ == '__main__':
    show_ui_exam_version()

    # The hardcoded variants as alternative. Uncomment them and replace them with whatever numbers you have.
    # miller_rabin(7121)
    # miller_rabin(1521)
