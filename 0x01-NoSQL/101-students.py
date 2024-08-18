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
    pipeline = [
        {
            # Unwind the scores array to deconstruct each score
            "$unwind": "$scores"
        },
        {
            # Group by student id and name, calculate the average score
            "$project": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$scores.score"}
            }
        },
        {
            # Sort the results by averageScore in descending order
            "$sort": {"averageScore": -1}
        }
    ]
