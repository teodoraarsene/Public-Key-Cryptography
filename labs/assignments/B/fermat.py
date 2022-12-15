import math
from typing import Union

from utils import Style, Formatting


class Fermat:

    @staticmethod
    def algorithm(number: int, iteration_count: int = 20):
        print("n = " + Style.YELLOW + str(number) + Style.RESET, end="\n\n")

        # math.inqrt() returns the integer square root of the non-negative integer n.
        # Its equivalence would be the floor of the exact square root of n.
        # Reference: https://docs.python.org/3.8/library/math.html#math.isqrt
        t0: int = math.isqrt(number)
        print("Initialization:")
        print("t0 = [√n] = " + Style.YELLOW + str(t0) + Style.RESET, end="\n\n")

        final_s: Union[int, None] = None
        final_t: Union[int, None] = None
        found: bool = False

        print("Iterations:")
        for t in range(t0 + 1, t0 + iteration_count + 1):
            print(f"t = t0 + {t - t0}", end=": ")

            t_squared_minus_n = t ** 2 - number
            print("t" + Formatting.superscript(str(2)) + " - n = "
                  + Style.YELLOW + f"{t_squared_minus_n if not found else 'x'}" + Style.RESET,
                  end="   ")

            s_float = math.sqrt(t_squared_minus_n)
            s_int = math.isqrt(t_squared_minus_n)
            print(f"perfect square (yes/no) = "
                  + Style.YELLOW + f"{'x' if found else 'yes' if s_float == s_int else 'no'}" + Style.RESET)
            if s_float == s_int:
                found = True
                final_s = s_int
                final_t = t
        print("")

        print("Values:")
        print("s = " + Style.YELLOW + str(final_s) + Style.RESET, end="\t")
        print("t = " + Style.YELLOW + str(final_t) + Style.RESET, end="\n\n")

        first_factor: int
        second_factor: int
        first_factor, second_factor = sorted((final_t - final_s, final_t + final_s))
        print("Conclusion:")
        print("The obtained two factors of are (in increasing order!)", end=" ")
        print(Style.YELLOW + f"{first_factor}" + Style.RESET + " and " +
              Style.YELLOW + f"{second_factor}" + Style.RESET)

    @staticmethod
    def show_ui_exam_version(page_count: int = 1):
        for page in range(page_count):
            while True:
                try:
                    user_input = int(input("Use Fermat's method to determine the decomposition of the number into two "
                                           "factors. Number: "))
                    Fermat.algorithm(user_input)
                    break
                except ValueError:
                    print(Style.RED + "ERROR: Input is NOT a number." + Style.RESET, end="\n\n")
