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

def person(person_id):
	person_node = people_index.get("id", person_id).pop()
	print person_node
	person_data = person_node.get_properties()

	person_data['quotes'] = [q_node.get_properties() for q_node in person_node.get_related_nodes(neo4j.Direction.OUTGOING, "quote")]

	return person_data