#!/usr/bin/env python

#import the CSV module for dealing with CSV files
import csv

csvfile = raw_input('Enter CSV filename: ')
ttlfile = raw_input('Enter TTL output filename: ')
#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = open(csvfile, 'rb')
reader = csv.reader(ifile)

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = open(ttlfile, 'a')

from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF

g = Graph()

n = Namespace("http://www.bbc.co.uk/things/")

pol = Namespace("http://www.bbc.co.uk/ontologies/newspolitics/")

core = Namespace("http://www.bbc.co.uk/ontologies/coreconcepts/")

rownum = 0
for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else:
		id = row[1]
		council = URIRef(n + id)
		g.add( (council, RDF.type, pol.Council) )
		g.add( (council, core.preferredLabel, Literal(row[2])) )
		g.add( (council, core.sameAs, URIRef(row[3])) )
	rownum += 1 # advance the row number so we can loop through again with the next row

d = g.serialize(format='turtle')
outfile.write(d)	# now write the d variable into the file

# finish off by closing the two files we created

outfile.close()
ifile.close()

# to do: add the provenance information at the top of the file
