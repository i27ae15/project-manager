import pymongo
import certifi
ca = certifi.where()
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://userTestOne:aM2ex0Wde9Hy7C7v@cluster0.m226z.mongodb.net/sample_restaurants?retryWrites=true&w=majority", tlsCAFile=ca)
# First define the database name
db_name = client['ProjectManager']
# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)
collection_name = db_name["user"]
details = collection_name.find({'_id': ObjectId('61d7f53865836bdcfd1664ef')})
# details = collection_name.find({'first_name': 'Andres'})

# for n in details:
print('-------------')
print('-------------')
print(details[0]['first_name'])
print('-------------')
print('-------------')

# public lvfipusv
# private 76c90faf-dad0-42be-b16a-5f9fb061b907
