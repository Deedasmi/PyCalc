__author__ = 'Deedasmi'
from calculator import calc

def main():
    '''
    The main program loop
    '''
    print("Welcome to the Calculator")
    while True:
        print("Please input an equation")
        try:
            eq = take_input()
            if eq: #If returned an equation
                print_ans(calc.calculate(eq))
        except(UserWarning, SyntaxWarning) as e:
            print(e)
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
    eq = ""
    while not eq.strip():
        eq = input()
    if eq.lower() == "done":
        exit(0)
    elif "=" in eq: #Handle User defined variables (and possibly functions) separately
        print(calc.handle_user_defined_input(eq))
        return None
    return eq


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