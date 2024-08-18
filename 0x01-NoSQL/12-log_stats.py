#!/usr/bin/env python3
'''script that provides some stats about Nginx logs stored in MongoDB:
    Database: logs
    Collection: nginx

    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with
    the method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method=GET
    path=/status
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
