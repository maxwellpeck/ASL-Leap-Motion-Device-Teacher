import pickle, os

path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 9/"

database = {}

pickle.dump(database, open(path + 'userData/database.p', 'wb'))