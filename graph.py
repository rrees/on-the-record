from py2neo import neo4j
from py2neo import cypher

db_uri = "http://localhost:7474/db/data/"

gdb = neo4j.GraphDatabaseService(db_uri)

people_index = gdb.get_or_create_index(neo4j.Node, "people")

def all_nodes():
	nodes, metadata = cypher.execute(gdb, "START z=node(*) RETURN z")
	return [node.pop().get_properties() for node in nodes]

def people():
	return [node for node in all_nodes() if 'name' in node]
