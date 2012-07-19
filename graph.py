from py2neo import neo4j
from py2neo import cypher

import os

def setup_db():
	if os.environ.get('NEO4J_REST_URL'):
		db_uri = "{host}:{port}/db/data/".format(host = os.environ['NEO4J_HOST'], port=os.environ['NEO4J_PORT'])
		return neo4j.GraphDatabaseService(db_uri, user_name = os.environ['NEO4J_LOGIN'], password = os.environ['NEO4J_PASSWORD'])

	return neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

gdb = setup_db()

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