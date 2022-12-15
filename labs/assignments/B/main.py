from B.fermat import Fermat
from B.pollard import Pollard
from utils import Style


def show_ui_exam_version():
    while True:
        try:
            user_input = input("If the first problem is Fermat-related, type "
                               + "\"" + Style.GREEN + "F" + Style.RESET + "\""
                               + " else if the first problem is Pollard-related, type "
                               + "\"" + Style.GREEN + "P" + Style.RESET + "\""
                               + ": ")
            if user_input == "F":
                print("", end="\n\n")
                Fermat.show_ui_exam_version()
                print("", end="\n\n")
                Pollard.show_ui_exam_version()
                break
            elif user_input == "P":
                print("", end="\n\n")
                Pollard.show_ui_exam_version()
                print("", end="\n\n")
                Fermat.show_ui_exam_version()
                break
            else:
                raise RuntimeError()
        except RuntimeError:
            print(Style.RED + "ERROR: Invalid Option." + Style.RESET, end="\n\n")
    print(Style.BLUE + "GOOD LUCK!" + Style.RESET)


if __name__ == '__main__':
    show_ui_exam_version()

    # The hardcoded variants as alternative. Uncomment them and replace them with whatever numbers you have.
    # Fermat.algorithm(9699)
    # Pollard.algorithm(9983)
    #
    # Fermat.algorithm(7097)
    # Pollard.algorithm(6641)
