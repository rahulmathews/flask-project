import os

import neo4j
from neo4j import GraphDatabase, basic_auth

driver = None
def get_driver():
    if (driver is not None):
        return driver


url = os.environ["NEO4J_URI"]
username = os.environ["NEO4J_USER"]
password = os.environ["NEO4J_PASSWORD"]

print("NEO4J_URI....", os.environ['NEO4J_URI'])

try:
    if 'NEO4J_URI' in os.environ:
        driver = GraphDatabase.driver(url, auth=basic_auth(username, password))
    else:
        raise "Local DB is not enforceable" 

    print("Successfully connected to DB")

except:
    print("Error Connecting to DB")
