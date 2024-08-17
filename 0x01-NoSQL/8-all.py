#!/usr/bin/env python3
"""
    List all documents in a MongoDB collection.
    Returns:
    list: A list of documents in the collection.
    Returns an empty list if no documents are found.
"""


def list_all(mongo_collection):
    '''
    Prototype: def list_all(mongo_collection)
    '''
    documents = list(mongo_collection.find())
    return documents
