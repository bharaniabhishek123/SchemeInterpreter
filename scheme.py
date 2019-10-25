# scheme.py
#
# Challenge:  Can you implement a mini-scheme interpreter capable of 
# executing the following code:

env = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y,
    '=': lambda x, y: x == y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
}


# Procedures:  f(x) = x*x    # What is this? How would you represent it?
# Explain f(2)  -->  substitute 2 for x

def substitute(expr, name, value):
    # Replace all occurrences of name with value
    if isinstance(expr, str) and expr == name:
        return value
    elif isinstance(expr, tuple):
        return tuple([substitute(part, name, value) for part in expr])
    else:
        return expr


# What is a "procedure?"  (think objects)
class Procedure:
    def __init__(self, parameters, body):
        self.parameters = parameters  # ('x',)
        self.body = body  # ('*', 'x', 'x')

    def __call__(self, *args):  # Make it look like a python function
        # How does it work?
        expr = self.body
        for name, val in zip(self.parameters, args):
            expr = substitute(expr, name, val)
        return seval(expr)

    # substitute(('*', 'x', 'x'), 'x', 2) ---> ('*', 2, 2)


def seval(sexp):
    # Primitives.  Do nothing
    if isinstance(sexp, int):
        return sexp
    # A name. Look up in the environment
    elif isinstance(sexp, str):
        return env[sexp]
    # Otherwise a "procedure"
    elif isinstance(sexp, tuple):
        op, *args = sexp
        if op == 'define':  # Special form
            name, val = args
            env[name] = seval(val)
        # (if, test, consequence, alternative)
        elif op == 'if':
            test, consequence, alternative = args
            if seval(test):
                return seval(consequence)
            else:
                return seval(alternative)

        # (lambda (params) body)
        # (lambda (x y) (+ x y))
        # ('lambda', ('x','y',), ('+', 'x', 'y'))
        elif op == 'lambda':
            parameters = args[0]
            body = args[1]
            return Procedure(parameters, body)

        else:  # Regular procedure call.  Evaluate the arguments. Then call procedure.
            eargs = [seval(arg) for arg in args]
            return seval(op)(*eargs)  # Works with any procedure
    else:
        return sexp


print(seval(('if', ('<', 2, 3), 10, 20)))  # -> should print 10
print(seval(('if', ('>', 2, 3), 10, 20)))  # -> 20

# raise SystemExit()

# A function definition expressed as a S-expression (in tuples)
fact = ('define', 'fact',
        ('lambda', ('n',), ('if', ('=', 'n', 1), 1, ('*', 'n', ('fact', ('-', 'n', 1))))))

# Some test code
seval(fact)
seval(('define', 'n', 5))
result = seval(('fact', 'n'))
assert result == 120

# Does that procedural cons work?   Exercise 2.4?

seval(('define', 'cons', ('lambda', ('x', 'y'), ('lambda', ('m',), ('m', 'x', 'y')))))
seval(('define', 'car', ('lambda', ('z',), ('z', ('lambda', ('p','q'), 'p')))))
seval(('define', 'cdr', ('lambda', ('z',), ('z', ('lambda', ('p','q'), 'q')))))


seval(('define','a',('cons', 1 ,2)))
print(seval('a'))
assert seval(('car','a')) == 1