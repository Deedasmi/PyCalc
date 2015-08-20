'''
Simple input/output for PyCalc
'''
__author__ = 'Deedasmi'
from pycalc import calc


def main():
    '''
    The main program loop
    '''
    print("Welcome to the Calculator")
    while True:
        print("Please input an equation")
        try:
            equation = take_input()
            if equation: #If returned an equation
                print_ans(calc.calculate(equation))
        except(UserWarning, SyntaxWarning) as error:
            print(error)
        except ZeroDivisionError:
            print("Cannot divide by Zero, numbnuts")
        except KeyboardInterrupt:
            print("Exiting")
            exit()

def take_input():
    '''
    Grabs user input split into a list
    :return: List if ready for math or None to skip math
    '''
    equation = ""
    while not equation.strip():
        equation = input()
    if equation.lower() == "done":
        exit(0)
    elif "=" in equation: #Handle User defined variables (and possibly functions) separately
        print(calc.handle_user_defined_input(equation))
        return None
    return equation


def print_ans(ans):
    '''
    Format answer to be printed
    :param ans: The answer
    '''
    if ans.is_integer():
        print(int(ans))
    else:
        print(round(ans, 4))

if __name__ == "__main__":
    main()
