#!/usr/bin/env python3
"""
    Insert a new document into a MongoDB collection based on kwargs.
    Returns:
    The _id of the newly inserted document.
"""


def insert_school(mongo_collection, **kwargs):
    ''' Parameters:
        mongo_collection (pymongo.collection.Collection):
        The pymongo collection object.
        **kwargs: The fields and values for the new document.
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
