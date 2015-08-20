__author__ = 'Deedasmi'
import re

# User defined variables. And pi.
udv = {'pi': '3.1415926535'}
# User defined functions. And test function
udf = {'test': (('x', 'y'), "x+2/y")}
# Set of operators
OPERATORS = {"+", "-", "*", "/", "^", "%"}
# Set of all allowed symbols
ALLOWED_SYMBOLS = {"+", "-", "*", "/", "^", "%", "(", ")", "."}

saved = None


def get_udf(equation):
    """
    Get user defined function
    :param equation: The string to handle
    :return: String to be sent through equation_to_list
    """
    temp = equation.split("(")
    func = temp[0]
    all_vars = temp[1][:-1]
    func_vars = all_vars.split(",")
    equation = udf[func][1]
    if len(func_vars) != len(udf[func][0]):
        raise SyntaxWarning("{} variables defined, but {} supplied."
                            .format(str(len(udf[func][0])), str(len(func_vars))))
    for i in range(0, len(udf[func][0])):
        equation = equation.replace(udf[func][0][i], func_vars[i])
    return equation


def handle_user_defined_input(equation, function=False):
    """
    Handles all user defined variables
    :param equation: Equation to print
    :return: On success returns a string to be printed
    """
    equation = equation.replace(" ", "")
    if equation.count("=") > 1:
        raise SyntaxWarning("Unknown operation (too many '=')")
    equation = equation.split("=")
    key = equation[0]
    value = equation[1]

    # Working with User Define Function
    # TODO replace with function variable
    if "(" in key:
        if key.count("(") != 1 or key.count(")") != 1:
            raise SyntaxWarning("Non matching parenthesis in function declaration"
                                " or too many parenthesis")
        func_vars = key[key.index("(") + 1:key.index(")")].split(",")
        for var in func_vars:
            if not var.isalpha():
                raise UserWarning("All variables must be alpha")
        key = key[0:key.index("(")]
        if not key.isalpha():
            raise UserWarning("Function name must be alpha")
        # Delete UDVs with the same name
        if key in udv:
            del udv[key]
            del udv["-" + key]
        udf[key] = func_vars, value
        return '{} added with function {}'.format(key, value)
    else:
        if key.isalpha():
            try:
                float(value)
            except:
                raise UserWarning("Value must be a valid number")
        else:
            raise UserWarning("Key must be alpha")
        # Delete UDFs with the same name
        if key in udf:
            del udf[key]
        udv[key] = value
        udv["-" + key] = float(value) * -1  # allows negative UDV
    return '{} added with value {}'.format(key, value)


def equation_to_list(equation):
    """
    Splits the equation out into a list
    :param equation: The equation to split
    :return: Returns a validated list
    """
    # Replace alternate characters
    equation = equation.replace("\\", "/")
    equation = equation.replace("[", "(")
    equation = equation.replace("{", "(")
    equation = equation.replace("]", ")")
    equation = equation.replace("}", ")")
    # split eq into numbers and special characters
    equation_list = ['']
    # iterate for each char in eq
    for character in equation:
        # if char is a digit, either append it onto the last item (a number)
        # or append it onto the list. Do the same check with alpha
        if character.isdigit() or character is ".":
            if not equation_list[-1].isnumeric() and equation_list[-1] is not ".":
                equation_list.append(character)
            else:
                equation_list[-1] += character
        elif character.isalpha():
            if not equation_list[-1].isalpha():
                equation_list.append(character)
            else:
                equation_list[-1] += character
        # if char is special character, just add to list
        else:
            if character not in ALLOWED_SYMBOLS:
                raise UserWarning("Unknown symbol '{}'".format(character))
            equation_list.append(character)
    # remove empty strings, Nones (and any other False-y things)
    # equation = [x for x in equation if x]
    del equation_list[0]
    return validate_and_format_list(equation_list)


def validate_and_format_list(equation):
    """
    Validates the list as a valid mathematical function
    Additionally adds things to the list in certain situations
    :param equation:
    :return: A list that should work.
    """
    i = 0
    neg = False
    if equation.count("(") != equation.count(")"):
        raise SyntaxWarning("Non-matching parenthesis. {} '(' found and {} ')' found"
                            .format(str(equation.count("(")), str(equation.count(")"))))
    # Loop through list
    # TODO save to new equation so we aren't modifying the duration of loop during loop. I know I'm bad
    while i is not len(equation):
        # Replace alpha strings with their value in UDV
        if equation[i].isalpha():
            if equation[i] in udv:
                equation[i] = udv[equation[i]]
            else:
                raise UserWarning("{} not found in the variable database".format(equation[i]))
        # Replace numeric values with the float of their value
        if equation[i].isnumeric() or "." in equation[i]:
            if isinstance(equation[i-1], float):
                raise SyntaxWarning("Missing operator between values")
            if equation[i].count(".") > 1:
                raise SyntaxWarning("Unknown value. Too many '.'")
            if equation[i] is ".":
                raise SyntaxWarning("Unknown value. '.' without number.")
            equation[i] = float(equation[i])
            if neg:
                equation[i] *= -1
                del equation[i - 1]  # Remove negative sign from list
                i -= 1
                neg = False
        else:
            # Symbol Features
            # Handle equations starting with operators
            if i == 0:
                if equation[i] in OPERATORS:
                    if saved:
                        equation.insert(0, saved)
                        i += 1
                    else:
                        raise UserWarning("No previous value saved.")
                i += 1
                continue
            # Turn 2 * -(2 + 2) into 2 * (0-(2+2))
            if neg and equation[i] is "(":
                right = find_matching_parenthesis(i, equation) + 2
                equation.insert(i-1, "(")
                equation.insert(i, 0)
                equation.insert(right, ")")
                i += 2
                neg = False
            # Handle implied multiplication
            if equation[i] is "(" and isinstance(equation[i - 1], float):
                equation.insert(i, "*")
                i += 1
            # Symbol bug handling
            # Handle empty parenthesis
            if equation[i] is ")" and equation[i - 1] is "(":
                raise SyntaxWarning("Empty parenthesis")
            # Handle operators being next to each other
            if equation[i-1] in ALLOWED_SYMBOLS:
                if equation[i] is "-" and equation[i-1] is not ")":
                    neg = True
                else:
                    if equation[i] is not "(" and equation[i - 1] is not ")":
                        raise SyntaxWarning("Missing value between operators")
        i += 1
    if equation[-1] in OPERATORS:
        raise SyntaxWarning("Equation may not end with an operator")
    return equation


def do_math(equation):
    """
    Recursively solve equation
    :param equation: The equation to solve
    :return: Float - the solved number
    """
    while "(" in equation:
        # Please
        # Pops out from first ( to matching ) and recursively solves the sub equation
        left_paren = equation.index("(")
        right_paren = find_matching_parenthesis(left_paren, equation)
        sub_equation = []
        for i in range(left_paren, right_paren + 1):  # Second value of range non-inclusive
            sub_equation.append(equation.pop(left_paren))
        del sub_equation[0]  # removed left parenthesis from sub_equation
        del sub_equation[len(sub_equation) - 1]  # and removed the right
        equation.insert(left_paren, do_math(sub_equation))  # recursively calls to handle nested parenthesis

    while len(equation) > 1:
        i = 0
        # Excuse
        if "^" in equation:
            i = equation.index("^")
        # My Dear
        elif "*" in equation or "/" in equation or "%" in equation:
            i = min(mdm_what_to_min(equation))
        # Aunt Sally
        elif "+" in equation and "-" in equation:
            i = min(equation.index("+"), equation.index("-"))
        elif "+" in equation:
            i = equation.index("+")
        elif "-" in equation:
            i = equation.index("-")

        # Math time
        i -= 1  # makes popping simple
        number1 = equation.pop(i)
        operator = equation.pop(i)
        number2 = equation.pop(i)
        equation.insert(i, do_simple_math(number1, number2, operator))
    global saved
    saved = equation[0]
    return saved


def mdm_what_to_min(equation):
    """
    Creates a list of indexes of * / %
    :param equation: The equation to work with
    :return: List to min()
    """
    to_min = []
    if "*" in equation:
        to_min.append(equation.index("*"))
    if "/" in equation:
        to_min.append(equation.index("/"))
    if "%" in equation:
        to_min.append(equation.index("%"))
    return to_min


def find_matching_parenthesis(left, equation):
    """
    Ghetto function to find ) that matches (
    When p = 0 after finding a ), it should be the matching paren
    :param left: The parenthesis to match
    :param equation: The equation to match it in
    :return: int. Index of right paren
    """
    nested_parenthesis = 0
    for i in range(left, len(equation)):  # skip leftmost parenthesis
        if equation[i] == "(":
            nested_parenthesis += 1
        elif equation[i] == ")":
            nested_parenthesis -= 1
            if nested_parenthesis == 0:
                return i
    raise SyntaxWarning("No matching parenthesis found")  # should never happen because handling in equation_to_list


def do_simple_math(number1, number2, operator):
    """
    Does simple math between two numbers and an operator
    :param number1: The first number
    :param number2: The second number
    :param operator: The operator (string)
    :return: Float
    """
    ans = 0
    if operator is "*":
        ans = number1 * number2
    elif operator is "/":
        ans = number1 / number2
    elif operator is "+":
        ans = number1 + number2
    elif operator is "-":
        ans = number1 - number2
    elif operator is "^":
        ans = number1 ** number2
    elif operator is "%":
        ans = number1 % number2
    return ans


def calculate(*args):
    """
    Wrapper function
    Takes a single string and runs through equation_to_list and doMath
    or
    Takes 3 arguments for doSimpleMath

    Relies on other functions to do error handling
    :param args:
    :return: Answer
    """

    if isinstance(args[0], str) and len(args) == 1:
        # remove white space
        equation = args[0].replace(" ", "")
        # Check if function
        if equation[0].isalpha():  # Check this first because re.match is slow
            # TODO support inline function calls (i.e: 2 + test(2, 5) / 5)
            if re.match(r"(^[a-zA-z]*)\(([\d\,]*)\)$", equation):
                equation = get_udf(equation)
        equation = equation_to_list(equation)
        return do_math(equation)
    if len(args) == 3:
        return do_simple_math(args[0], args[1], args[2])
    raise TypeError("Function handles single strings, or group of 3 arguments (n1, n2, o)")

if __name__ == "__main__":  # for speed testing
    for r in range(1000):
        calculate("4 * 10 / 15 + ( 6 - 2 * 3 )")
        calculate("2 +5/1 + (2* 5)/2")
        calculate("7^2+16 / (4^4)")
        calculate("(1+2)+(2+3)")
        calculate("1+ ( ( ( 3 + 2) * 2) - 4)")
        calculate("pi*2")
        calculate("(2*.5)^3")
        handle_user_defined_input("Matt = 20")
        calculate("Matt * pi")
        calculate(5, 2, "-")
        handle_user_defined_input("func(x, y) = x * y / 2")
        calculate("func(2,4)")
        calculate("test ( 4, 2)")
