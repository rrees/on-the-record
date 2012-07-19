from py2neo import neo4j

db_uri = "http://localhost:7474/db/data/"

gdb = neo4j.GraphDatabaseService(db_uri)

base_node = gdb.get_reference_node()

def relate(a, b, rtype):
	if not a.has_relationship_with(b, neo4j.Direction.OUTGOING, rtype):
		a.create_relationship_to(b, rtype)
	return (a, b)

people_index = gdb.get_or_create_index(neo4j.Node, "people")

people = [
	{"name" : "Jeremy Paxman" , "id" : "798f1780-d187-11e1-acb4-2c4138a8ba9b"},
	{"name" : "Chloe Smith", "id" : "97a1251a-d187-11e1-acb4-2c4138a8ba9b"},
	{"name" : "Michael Howard", "id" : '724b7080-d1ba-11e1-acb4-2c4138a8ba9b'},]

for person in people:
	p_node = people_index.get_or_create("id", person['id'], person)
	relate(base_node, p_node, "person")
	print "Created {0}".format(person['name'])

quote_index = gdb.get_or_create_index(neo4j.Node, "quotes")

quotes = [
	{"id" : '17643a0c-d189-11e1-acb4-2c4138a8ba9b',
	"quote" : "Do you ever think you're incompetent?",},
	{"id" : '4ddbbf48-d1ba-11e1-acb4-2c4138a8ba9b',
	"quote" : "Did you overrule him?"}
]

for quote in quotes:
	quote_node = quote_index.get_or_create("id", quote['id'], quote)

quote_attributations = [
	("798f1780-d187-11e1-acb4-2c4138a8ba9b", '17643a0c-d189-11e1-acb4-2c4138a8ba9b'),
	("798f1780-d187-11e1-acb4-2c4138a8ba9b", '4ddbbf48-d1ba-11e1-acb4-2c4138a8ba9b'), ]

for attributation in quote_attributations:
	speaker, quote = attributation

	speaker_node = people_index.get("id", speaker)[0]
	quote_node = quote_index.get("id", quote)[0]

	relate(speaker_node, quote_node, "quote")

context_index = gdb.get_or_create_index(neo4j.Node, "contexts")

contexts = [
	("Newsnight", ['17643a0c-d189-11e1-acb4-2c4138a8ba9b', '4ddbbf48-d1ba-11e1-acb4-2c4138a8ba9b']),
	("Treasury Select Committee", [])]

for context, relevant_quotes in contexts:
	context_node = context_index.get_or_create("name", context, {"name" : context})
	for quote in relevant_quotes:
		quote_node = quote_index.get("id", quote)[0]
		relate(quote_node, context_node, "context")
	relate(base_node, context_node, "quote_context")

	print "Created {context}".format(context = context)
