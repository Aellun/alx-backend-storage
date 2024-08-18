#!/usr/bin/env python3
'''Python function that returns all students sorted by average score
    Parameters:
    - mongo_collection: pymongo collection object
'''


def top_students(mongo_collection):
    '''
   Prototype: def top_students(mongo_collection):
    Returns:
    - A list of students with their average scores, sorted in descending order.
    '''
    # Aggregation pipeline to calculate average scores and sort them
    return mongo_collection.aggregate([
        {
            "$project": {
                # Include the name field
                "name": 1,
                # Calculate average score
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {
                # Sort by average score in descending order
                "averageScore": -1
            }
        }
    ])
