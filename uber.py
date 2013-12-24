#!/usr/bin/env python

# uber.py is an attempt to combine three things, before I try and seperate them out into various functions.
# it is designed to create a dataset, import from a CSV file, convert the CSV to a graph pattern, then write the resulting TTL to a file.

# Ask for various inputs
product = raw_input('Which BBC Online product is this dataset for? ')
label = raw_input('Enter a label describing the dataset: ')
location = raw_input('Enter the canonical location for the dataset: ')
change_reason = raw_input('Enter a reason for the dataset change: ')
version_no = raw_input('Enter the version number for the dataset: ')
ttlfile = raw_input('Enter TTL output filename: ')

# Set up the graph pattern (this should probably be abstracted into a 'graphTemplate' function at some point)

from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS

datasetGraph = Graph()

n = Namespace("http://www.bbc.co.uk/contexts/")

b = Namespace("http://www.bbc.co.uk/ontologies/bbc/")

c = Namespace("http://www.bbc.co.uk/ontologies/provenance/")

datasetGraph.namespace_manager.bind('provenance', URIRef(c))
datasetGraph.namespace_manager.bind('bbc', URIRef(b))

# Generate a UUID to use for the dataset URI

import uuid

x = uuid.uuid4()

y = str(x)

# Create the dataset URI by combining the relevant namespace with the UUID

datasetURI = URIRef(n + y)

# Create the relevant BBC Product URI by combining the appropriate namespace with the specified product

z = URIRef(b + product)

# Add detail to the dataset Graph

datasetGraph.add( (datasetURI, RDF.type, c.Dataset) )
datasetGraph.add( (datasetURI, RDFS.label, Literal(label)) )
datasetGraph.add( (datasetURI, c.canonicalLocation, Literal(location)) )
datasetGraph.add( (datasetURI, c.changeReason, Literal(change_reason)) )
datasetGraph.add( (datasetURI, c.product, z ) )
datasetGraph.add( (datasetURI, c.version, Literal(version_no)) )

# Serialise the graph in Turtle

d = datasetGraph.serialize(format='turtle')

# Create a file and pass the TTL into it

outfile = open(ttlfile, 'a')

outfile.write(d)

# Now, import the CSV, create a new graph and append it to the same file.

import csv

csvfile = raw_input('Enter CSV filename: ')

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = open(csvfile, 'rb')
reader = csv.reader(ifile)

g = Graph()

thingNamespace = Namespace("http://www.bbc.co.uk/things/")

pol = Namespace("http://www.bbc.co.uk/ontologies/politicsnews/")

core = Namespace("http://www.bbc.co.uk/ontologies/coreconcepts/")

g.namespace_manager.bind('core', URIRef(core))
g.namespace_manager.bind('pnews', URIRef(pol))

rownum = 0
for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else:
		id = row[1]
		council = URIRef(thingNamespace + id)
		g.add( (council, RDF.type, pol.Council) )
		g.add( (council, core.preferredLabel, Literal(row[2])) )
		g.add( (council, core.sameAs, URIRef(row[3])) )
	rownum += 1 # advance the row number so we can loop through again with the next row

h = g.serialize(format='turtle')

outfile.write(h)
# finish off by closing the two files we created

outfile.close()
ifile.close()	

# Only thing to change, aside from breaking these out into functions, is to stop the repeating namespaces.
