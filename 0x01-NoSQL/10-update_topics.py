#!/usr/bin/env python3
'''Update all topics of a school document based on the school name
    Returns: None
'''


def update_topics(mongo_collection, name, topics):
    """
    mongo_collection (pymongo.collection.Collection)
    name (str): The school name to update.
    topics (list of str): The list of topics to set for the school.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
