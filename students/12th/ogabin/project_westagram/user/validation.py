import re

def check_email(email):
    ck = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    if not ck.match(email):
        return True

lambdas = [lambda password : 'True' if len(password) < 8 else None,
           lambda password : 'True' if not any(c.isupper() for c in password) else None
           ]

def check_password(password):

    for f in lambdas:
        if f(password) is not None:
            return f(password)

    return False