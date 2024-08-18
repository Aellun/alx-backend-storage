#!/usr/bin/env python3
'''Improve 12-log_stats.py by adding the top 10
    of the most present IPs in the collection nginx of the database logs
'''
from pymongo import MongoClient
# Connect to the MongoDB server;the logs database and nginx collection
if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs.nginx

    # Count the total number of logs in the nginx collection
    num_logs = db.count_documents({})
    print(f"{num_logs} logs")

    # Count the number of logs for each HTTP method
    get = db.count_documents({'method': 'GET'})
    post = db.count_documents({'method': 'POST'})
    put = db.count_documents({'method': 'PUT'})
    patch = db.count_documents({'method': 'PATCH'})
    delete = db.count_documents({'method': 'DELETE'})

    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")

    # Count where the method is GET and the path is /status
    status = db.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status} status check")
