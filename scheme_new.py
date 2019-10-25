# scheme.py
#
# Challenge:  Can you implement a mini-scheme interpreter capable of
# executing the following code:

# Global environment. Built-in functions
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

# What is a "procedure?"  (think objects)
class Procedure:
    def __init__(self, parameters, body, env):
        self.parameters = parameters  # ('x',)
        self.body = body  # ('*', 'x', 'x')
        self.env = env  # Reference to env where the function was defined

    def __call__(self, *args):  # Make it look like a python function
        # How does it work?
        newenv = make_new_environment(self.env)  # Need to make a new environment
        # that's nested within the definition env
        for name, val in zip(self.parameters, args):
            # expr = substitute(expr, name, val)
            newenv[name] = val
        return seval(self.body, newenv)

def make_new_environment(env):
    newenv = {'__parent__': env}
    return newenv

def seval(sexp, env):
    # Primitives.  Do nothing
    if isinstance(sexp, int):
        return sexp
    # A name. Look up in the environment
    elif isinstance(sexp, str):
        e = env
        while e:
            if sexp in e:
                return e[sexp]
            e = e.get('__parent__')
        raise NameError("unknown name")
    # Otherwise a "procedure"
    elif isinstance(sexp, tuple):
        op, *args = sexp
        if op == 'define':  # Special form
            name, val = args
            env[name] = seval(val, env)
        elif op == 'set!':
            name, val = args
            # SET does not create new definitions. Always updates an existing definition
            e = env
            while e:
                if name in e:
                    e[name] = seval(val, env)
                    return
                e = e.get('__parent__')
            raise NameError("Unknown name")

        # (if, test, consequence, alternative)
        elif op == 'if':
            test, consequence, alternative = args
            if seval(test, env):
                return seval(consequence, env)
            else:
                return seval(alternative, env)

# (lambda (params) body)
# (lambda (x y) (+ x y))
# ('lambda', ('x','y',), ('+', 'x', 'y'))
        elif op == 'lambda':

            parameters = args[0]
            body = args[1]
            return Procedure(parameters, body, env)
        else:
        # Regular procedure call.  Evaluate the arguments. Then call procedure.
            eargs = [seval(arg, env) for arg in args]
            return seval(op, env)(*eargs)  # Works with any procedure
    else:
        return sexp

print(seval(('if', ('<', 2, 3), 10, 20), env))  # -> should print 10
print(seval(('if', ('>', 2, 3), 10, 20), env))  # -> 20


# raise SystemExit()
# ​
# A function definition expressed as a S-expression (in tuples)
fact = ('define', 'fact',
        ('lambda', ('n',), ('if', ('=', 'n', 1), 1, ('*', 'n', ('fact', ('-', 'n', 1))))))
# Some test code
seval(fact, env)
seval(('define', 'n', 5), env)
result = seval(('fact', 'n'), env)
assert result == 120

seval(('set!', 'n', 10), env)
assert seval('n', env) == 10
# Does that procedural cons work?   Exercise 2.4?​
seval(('define', 'cons', ('lambda', ('x', 'y'), ('lambda', ('m',), ('m', 'x', 'y')))), env)
seval(('define', 'car', ('lambda', ('z',), ('z', ('lambda', ('p', 'q'), 'p')))), env)
seval(('define', 'cdr', ('lambda', ('z',), ('z', ('lambda', ('p', 'q'), 'q')))), env)