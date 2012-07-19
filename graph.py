from py2neo import neo4j
from py2neo import cypher

from urlparse import urlparse
import os

def first(list):
	if list:
		return list[0]
	return None

def setup_db():
	if os.environ.get('NEO4J_REST_URL'):
		#return neo4j.GraphDatabaseService(os.environ.get('NEO4J_REST_URL'))
		#db_uri = "{host}:{port}/db/data/".format(host = os.environ['NEO4J_HOST'], port=os.environ['NEO4J_PORT'])
		#return neo4j.GraphDatabaseService(db_uri, user_name = os.environ['NEO4J_LOGIN'], password = os.environ['NEO4J_PASSWORD'])
		graph_db_url = urlparse(os.environ.get('NEO4J_REST_URL'))
		return neo4j.GraphDatabaseService('http://{host}:{port}{path}/'.format(host=graph_db_url.hostname, port=graph_db_url.port, path=graph_db_url.path), auth_username=graph_db_url.username, auth_password=graph_db_url.password)

	return neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

gdb = setup_db()

people_index = gdb.get_or_create_index(neo4j.Node, "people")

def all_nodes():
	nodes, metadata = cypher.execute(gdb, "START z=node(*) RETURN z")
	return [node.pop().get_properties() for node in nodes]

def people():
	nodes, metadata = cypher.execute(gdb, "START z=node(*) MATCH z-[:person]->p RETURN p")
	return [node.pop().get_properties() for node in nodes]

def resolve_quotes(person_node):
	quotes = person_node.get_related_nodes(neo4j.Direction.OUTGOING, "quote")

	def generate_quote(quote_node):
		data = quote_node.get_properties()
		
		if quote_node.has_relationship(neo4j.Direction.OUTGOING, "context"):
			context = quote_node.get_related_nodes(neo4j.Direction.OUTGOING, "context").pop()
			data['context'] = context.get_properties()

		if quote_node.has_relationship(neo4j.Direction.OUTGOING, "interaction"):
			interactions = quote_node.get_relationships(neo4j.Direction.OUTGOING, "interaction")

			data['interactions'] = []
			for interaction in interactions:
				data['interactions'].append({
					"person" : interaction.end_node.get_properties(),
					"label" : interaction['label']
					})

		return data

	return [generate_quote(q_node) for q_node in quotes]

def person(person_id):
	person_node = people_index.get("id", person_id)

	if not person_node: return None

	person_node = first(person_node)

	person_data = person_node.get_properties()

	person_data['quotes'] = resolve_quotes(person_node)

	return person_data