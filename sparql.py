from rdflib import Graph, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib import Namespace
from rdflib.plugins import sparql

from SPARQLWrapper import SPARQLWrapper, JSON, XML, TURTLE

from prettytable import PrettyTable



endpoint_url = "http://192.168.56.1:9999/blazegraph/namespace/kb/sparql"
g = Graph()
url = URIRef(endpoint_url)
g.parse(url, format='turtle')

##################################################
# Checking the length of my CybersecurityOntology#
##################################################

count_query = prepareQuery('''
PREFIX : <http://cnam.com/CybersecurityOntology/>
    SELECT (COUNT(*) AS ?count)
    WHERE {
        ?s ?p ?o .
    }
''', initNs={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

count_result = g.query(count_query)
print("##### PRINTING NUMBER OF TRIPLES IN 'CybersecurityOntology' ######")
for row in count_result:
    print("Number of Triples:", row[0])

print("***************************************************")
print("***************************************************")


#########################################################
# Querying the ontology and get the names of researchers#
#########################################################
sparql_select_query = """
PREFIX : <http://cnam.com/CybersecurityOntology/>

SELECT ?n
WHERE {
  ?c a :Chercheur ;
       :hasName ?n .
}
"""
sparql = SPARQLWrapper(endpoint_url)
sparql.setQuery(sparql_select_query)

sparql.setReturnFormat(JSON)

res = sparql.query().convert()

print("##### PRINTING SELECT RES VALUES ######")
table = PrettyTable(["fullname"])
for binding in res['results']['bindings']:
    table.add_row([binding['n']['value']])

print(table)
