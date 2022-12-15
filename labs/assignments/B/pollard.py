from typing import Callable, Union

from utils import Style, Formatting


def greatest_common_divisor(a: int, b: int) -> int:
    # A more efficient method is the Euclidean algorithm, a variant in which the difference of the two numbers a and
    # b is replaced by the remainder of the Euclidean division (also called division with remainder) of a by b.
    if b == 0:
        return a
    else:
        # Denoting this remainder as a mod b, the algorithm replaces (a, b) by (b, a mod b) repeatedly until the pair
        # is (d, 0), where d is the greatest common divisor.
        return greatest_common_divisor(b, a % b)


class Pollard:

    @staticmethod
    def algorithm(number: int, x0: int = 2, f: Callable[[int], int] = lambda x: x ** 2 + 1):
        print("n = " + Style.YELLOW + str(number) + Style.RESET, end="\n\n")

        x_sequence: dict[int, int] = {0: x0}

        print("Iterations (results mod "
              + Style.YELLOW + "n" + Style.RESET
              + "):")

        final_divisor: Union[int, None] = None
        found: bool = False

        for index in range(1, 20 + 1, 2):
            x_sequence[index] = f(x_sequence[index - 1]) % number
            print(f"x{Formatting.subscript(str(index))} = "
                  + Style.YELLOW + f"{x_sequence[index] if not found else 'x'}" + Style.RESET, end="  ")

            x_sequence[index + 1] = f(x_sequence[index]) % number
            print(f"x{Formatting.subscript(str(index))} = "
                  + Style.YELLOW + f"{x_sequence[index + 1] if not found else 'x'}" + Style.RESET, end="  ")

            divisor = greatest_common_divisor(abs(x_sequence[index + 1] - x_sequence[(index + 1) // 2]), number)

            print(f"(x{Formatting.subscript(str(index + 1))} - x{Formatting.subscript(str((index + 1) // 2))}, n) = "
                  + Style.YELLOW + f"{divisor if not found else 'x'}" + Style.RESET)

            if 1 < divisor < number:
                found = True
                final_divisor = divisor
        print("")

        first_factor: int
        second_factor: int
        first_factor, second_factor = sorted((final_divisor, number // final_divisor))
        print("Conclusion:")
        print("The obtained two factors of are (in increasing order!)", end=" ")
        print(Style.YELLOW + f"{first_factor}" + Style.RESET + " and " +
              Style.YELLOW + f"{second_factor}" + Style.RESET)

    @staticmethod
    def show_ui_exam_version(page_count: int = 1):
        for page in range(page_count):
            while True:
                try:
                    user_input = int(input("Use Pollard's method with "
                                           + "x" + Formatting.subscript("0") + " = 2"
                                           + " and "
                                           + "f(x) = x" + Formatting.superscript("2") + " + 1"
                                           + " to determine the decomposition of the number into two factors. Number: "))
                    Pollard.algorithm(user_input)
                    break
                except ValueError:
                    print(Style.RED + "ERROR: Input is NOT a number." + Style.RESET, end="\n\n")
