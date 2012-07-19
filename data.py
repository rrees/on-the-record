from py2neo import neo4j

db_uri = "http://localhost:7474/db/data/"

gdb = neo4j.GraphDatabaseService(db_uri)

people_index = gdb.get_or_create_index(neo4j.Node, "people")

people = [
	{"name" : "Jeremy Paxman" , "id" : "798f1780-d187-11e1-acb4-2c4138a8ba9b"},
	{"name" : "Chloe Smith", "id" : "97a1251a-d187-11e1-acb4-2c4138a8ba9b"},]

for person in people:
	p_node = people_index.get_or_create("id", person['id'], person)	
	print "Created {0}".format(person['name'])

quote_index = gdb.get_or_create_index(neo4j.Node, "quotes")

quotes = [
	{"id" : '17643a0c-d189-11e1-acb4-2c4138a8ba9b',
	"quote" : "Do you ever think you're incompetent?", 
	"source" : "798f1780-d187-11e1-acb4-2c4138a8ba9b"},
]

for quote in quotes:
	quote_node = quote_index.get_or_create("id", quote['id'], quote)
	quotee = people_index.get("id", quote['source'])[0]
	quotee.create_relationship_to(quote_node, "quote")

