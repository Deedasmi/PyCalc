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


def get_udf(eq):
    """
    Get user defined function
    :param eq: The string to handle
    :return: String to be sent through equation_to_list
    """
    temp = eq.split("(")
    func = temp[0]
    all_vars = temp[1][:-1]
    func_vars = all_vars.split(",")
    eq = udf[func][1]
    if len(func_vars) != len(udf[func][0]):
        raise SyntaxWarning("{} variables defined, but {} supplied."
                            .format(str(len(udf[func][0])), str(len(func_vars))))
    for i in range(0, len(udf[func][0])):
        eq = eq.replace(udf[func][0][i], func_vars[i])
    return eq


def handle_user_defined_input(eq, function=False):
    """
    Handles all user defined variables
    :param eq: Equation to print
    :return: On success returns a string to be printed
    """
    eq = eq.replace(" ", "")
    if eq.count("=") > 1:
        raise SyntaxWarning("Unknown operation (too many '=')")
    eq = eq.split("=")
    key = eq[0]
    value = eq[1]

    # Working with User Define Function
    # TODO replace with function variable
    if "(" in key:
        if key.count("(") != 1 or key.count(")") != 1:
            raise SyntaxWarning("Non matching parenthesis in function declaration or too many parenthesis")
        func_vars = key[key.index("(") + 1:key.index(")")].split(",")
        for f in func_vars:
            if not f.isalpha():
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


def equation_to_list(eq):
    """
    Splits the equation out into a list
    :param eq: The equation to split
    :return: Returns a validated list
    """
    # Replace alternate characters
    eq = eq.replace("\\", "/")
    eq = eq.replace("[", "(")
    eq = eq.replace("{", "(")
    eq = eq.replace("]", ")")
    eq = eq.replace("}", ")")
    # split eq into numbers and special characters
    equation = ['']
    # iterate for each char in eq
    for c in eq:
        # if char is a digit, either append it onto the last item (a number)
        # or append it onto the list. Do the same check with alpha
        if c.isdigit() or c is ".":
            if not equation[-1].isnumeric() and equation[-1] is not ".":
                equation.append(c)
            else:
                equation[-1] += c
        elif c.isalpha():
            if not equation[-1].isalpha():
                equation.append(c)
            else:
                equation[-1] += c
        # if char is special character, just add to list
        else:
            if c not in ALLOWED_SYMBOLS:
                raise UserWarning("Unknown symbol '{}'".format(c))
            equation.append(c)
    # remove empty strings, Nones (and any other False-y things)
    # equation = [x for x in equation if x]
    del equation[0]
    return validate_and_format_list(equation)


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


def do_math(eq):
    """
    Recursively solve equation
    :param eq: The equation to solve
    :return: Float - the solved number
    """
    while "(" in eq:
        # Please
        # Pops out from first ( to matching ) and recursively solves the sub equation
        left_paren = eq.index("(")
        right_paren = find_matching_parenthesis(left_paren, eq)
        sub_equation = []
        for i in range(left_paren, right_paren + 1):  # Second value of range non-inclusive
            sub_equation.append(eq.pop(left_paren))
        del(sub_equation[0])  # removed left parenthesis from sub_equation
        del(sub_equation[len(sub_equation) - 1])  # and removed the right
        eq.insert(left_paren, do_math(sub_equation))  # recursively calls to handle nested parenthesis
    else:
        while len(eq) > 1:
            i = 0
            # Excuse
            if "^" in eq:
                i = eq.index("^")
            # My Dear
            elif "*" in eq or "/" in eq or "%" in eq:
                i = min(mdm_what_to_min(eq))
            # Aunt Sally
            elif "+" in eq and "-" in eq:
                i = min(eq.index("+"), eq.index("-"))
            elif "+" in eq:
                i = eq.index("+")
            elif "-" in eq:
                i = eq.index("-")

            # Math time
            i -= 1  # makes popping simple
            n1 = eq.pop(i)
            o = eq.pop(i)
            n2 = eq.pop(i)
            eq.insert(i, do_simple_math(n1, n2, o))
        global saved
        saved = eq[0]
        return saved


def mdm_what_to_min(eq):
    """
    Creates a list of indexes of * / %
    :param eq: The equation to work with
    :return: List to min()
    """
    to_min = []
    if "*" in eq:
        to_min.append(eq.index("*"))
    if "/" in eq:
        to_min.append(eq.index("/"))
    if "%" in eq:
        to_min.append(eq.index("%"))
    return to_min


def find_matching_parenthesis(left, eq):
    """
    Ghetto function to find ) that matches (
    When p = 0 after finding a ), it should be the matching paren
    :param left: The parenthesis to match
    :param eq: The equation to match it in
    :return: int. Index of right paren
    """
    p = 1
    for i in range(left + 1, len(eq)):  # skip leftmost parenthesis
        if eq[i] == "(":
            p += 1
        elif eq[i] == ")":
            p -= 1
            if p == 0:
                return i
    raise SyntaxWarning("No matching parenthesis found")  # should never happen because handling in equation_to_list


def do_simple_math(n1, n2, o):
    """
    Does simple math between two numbers and an operator
    :param n1: The first number
    :param n2: The second number
    :param o: The operator (string)
    :return: Float
    """
    ans = 0
    if o is "*":
        ans = n1 * n2
    elif o is "/":
        ans = n1 / n2
    elif o is "+":
        ans = n1 + n2
    elif o is "-":
        ans = n1 - n2
    elif o is "^":
        ans = n1 ** n2
    elif o is "%":
        ans = n1 % n2
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
        eq = args[0].replace(" ", "")
        # Check if function
        if eq[0].isalpha():  # Check this first because re.match is slow
            # TODO support inline function calls (i.e: 2 + test(2, 5) / 5)
            if re.match("(^[a-zA-z]*)\(([\d\,]*)\)$", eq):
                eq = get_udf(eq)
        eq = equation_to_list(eq)
        return do_math(eq)
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
