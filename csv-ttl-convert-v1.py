#!/usr/bin/env python

#import the CSV module for dealing with CSV files
import csv

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = open('councils-data.csv', 'rb')
reader = csv.reader(ifile)

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = open('councils.ttl', 'a')

#get python to loop through each row in the CSV, and ignore the first row.
rownum = 0
for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else: # if it's not the first row, place the contents of the row into the 'c' variable, then create a 'd' variable with the stuff we want in the file.
		c = row
		d = '<' + c[0] + c[1] + '> a pol:Council ;\n core:preferredLabel "' + c[2] + '" ;\n core:sameAs <' + c[3] + '> .\n \n'
		outfile.write(d)	# now write the d variable into the file
	rownum += 1 # advance the row number so we can loop through again with the next row

# finish off by closing the two files we created

outfile.close()
ifile.close()
