#!/usr/bin/env python3
'''Return the list of schools that have a specific topic.
    Returns:
    list: A list of schools (documents) that have the specific topic.
'''


def schools_by_topic(mongo_collection, topic):
    """
    Parameters:
    mongo_collection (pymongo.collection.Collection)
    topic (str):The topic to search for in the schools' topics field.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
