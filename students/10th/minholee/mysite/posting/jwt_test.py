import  jwt, bcrypt

SECRET = 'secret'

#access_token = jwt.encode({'id':1}, SECRET, algorithm= 'HS256')
#print(access_token)

"""
encoded_jwt = jwt.encode({'user-id' : 5}, SECRET, algorithm = 'HS256')
print(encoded_jwt)
print(type(encoded_jwt))

a = jwt.decode(encoded_jwt, SECRET, algorithms='HS256')
print(a)
print(type(a))
"""

password = '1234'
hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
#print(type(hashed_password))
#print(hashed_password)

bring_password = '1234'
a = bcrypt.checkpw(bring_password.encode('UTF-8'), hashed_password)
print(a)
