import pickle, os

logins = 1
path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 9/"

database = pickle.load(open(path + 'userData/database.p','rb'))

userName = raw_input('Please enter your name: ')
if userName in database:
    print('welcome back ' + userName + '.')
    database[userName] = "logins: " + str(int(database.get(userName)[8:]) + 1)
else:
    database[userName] = {}
    print('welcome ' + userName + '.')
    database[userName] = "logins: " + str(logins)

print(database)

pickle.dump(database, open(path + 'userData/database.p', 'wb'))