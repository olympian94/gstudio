''' imports from installed packages '''
from django.core.management.base import BaseCommand, CommandError

from mongokit import IS

from django_mongokit import get_database

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

''' imports from application folders/files '''
from gnowsys_ndf.ndf.models import Node

####################################################################################################################

class Command(BaseCommand):

    help = " This script will add the access_policy field to all created documents in your database."

    def handle(self, *args, **options):
        db = get_database()
        collection = db[Node.collection_name] 
        
        # As considering default access_policy of all documents is PUBLIC 
        
        collection.update({'_type': 'Group', 'group_type': 'PRIVATE'}, {'$set': {'access_policy': u"PRIVATE"}}, upsert=False, multi=True)
        collection.update({'_type': 'Group', 'group_type': 'PUBLIC'}, {'$set': {'access_policy': u"PUBLIC"}}, upsert=False, multi=True)
        
        collection.update({'_type': {'$nin': ['Group']}, 'access_policy': {'$exists': False}}, {'$set': {'access_policy': u"PUBLIC"}}, upsert=False, multi=True)
        
        collection.update({'_type': {'$nin': ['Group']}, 'access_policy': {'$in': [None, "PUBLIC"]}}, {'$set': {'access_policy': u"PUBLIC"}}, upsert=False, multi=True)
        collection.update({'_type': {'$nin': ['Group']}, 'access_policy': "PRIVATE"}, {'$set': {'access_policy': u"PRIVATE"}}, upsert=False, multi=True)

        # As _type field values is a list of those who all are inherited Node collection, as access_policy field is placed in Node collection
  		