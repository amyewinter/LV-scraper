#importing libraries
import os
from os.path import join
from bs4 import BeautifulSoup
import codecs
import cStringIO
import csv
import json

#setting up lists
tag_list = list()
content_list = list()
contents_final = list()
subject_list = list()
LCSH_list = list()
url_string = list()

#functions
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


#walking through collection and processing xml files
for (dirname, dirs, files) in os.walk('.'): #starts in current directory

    for filename in files:
        if filename.endswith('.xml') :
            #construct file name & assign to variable
            thefile = os.path.join(dirname, filename)
            #open file, process contents, and add to list
            with codecs.open (thefile, "r", "utf-8-sig") as fhand:

                for line in fhand:
                #modify the following to match tags in your XML that you want to skip
                    if '<?xml version' in line :  continue
                    if 'dublin_core' in line: continue
                    if 'qualifier="json"' in line :  continue

                #doing replacements to clean up XML
                    line = line.strip()
                    line = line.replace('language="en_US"','')
                    line = line.replace('language="en"','')
                    line = line.replace('language="','')
                    line = line.replace(' schema="dc"', '')
                    line = line.replace('<dcvalue element="', '<')
                    line = line.replace('" qualifier="', '_')
                    line = line.replace('">','>')
                    line = line.replace('" >','>')

                    #print line
                    
     #subject headings were listed in a single comma-delimited field and had to be handled separately to the rest of the metadata
                    
                    #finding start and end locations for user-entered subject headings
                    if line.startswith('<subject_none>'):
                        idend = line.find('</')
                        #print idend
                        subj_content = line[14:idend]
                        subj_content = subj_content.replace("&#x20;", " ")
                        #print itemid

                        subject_list.append(subj_content)

                    #print subject_list
                    
                    #finding start and end locations for LCSH subject headings
                    if line.startswith('<subject_lcsh>'):
                        idend = line.find('</')
                        #print idend
                        lcsh_str = line[14:idend]
                        lcsh_str = lcsh_str.replace("&#x20;", " ")

                        #print itemid
                        LCSH_list.append(lcsh_str)


                    else:
                        #modify the below 2 lines to reflect lines in your XML that you want to skip
                        if line.startswith('<subject_none>'): continue
                        if line.startswith('<subject_lcsh>'): continue
                        soup = BeautifulSoup(line, 'html.parser')
                        #print soup

                        #creating list of tag names for "header" row
                        for tag in soup.find_all(True):      
                            tag_list.append(tag.name)

                        #print tag_list
                        
                        #converting strings for space and character problems
                        for string in soup.stripped_strings:
                            content_list.append(repr(string))

                        content_str = '|'.join(content_list)
                        
                        #doing lots of character replacements that were unnecessary -- instead, import CSV into Excel using UTF-8 encoding option in wizard
                        content_str = content_str.replace("u'","'")
                        content_str = content_str.replace("\\r\\n", " ")
                        content_str = content_str.replace("\\n", " ")
                        content_str = content_str.replace("\\t", " ")
                        content_str = content_str.replace("&#x20;", " ")
                        content_str = content_str.replace("\\u201c","'")
                        content_str = content_str.replace("\\u201d","'")
                        content_str = content_str.replace("\\u2013","&#8212;")
                        content_str = content_str.replace("\\u2014","&#8212;")
                        content_str = content_str.replace("\\u2019","'")
                        content_str = content_str.replace("\\u2018","'")
                        content_str = content_str.replace("\\u2206","&#916;")
                        content_str = content_str.replace("\\xae","&#174;")
                        content_str = content_str.replace("\\xd7","x")
                        content_str = content_str.replace("\\xfc","&#252;")
                        content_str = content_str.replace("\\xe1","&aacute;")
                        content_str = content_str.replace("\\xe0","&agrave;")
                        content_str = content_str.replace("\\xe2","&acirc;")
                        content_str = content_str.replace("\\xc0","&Agrave;")
                        content_str = content_str.replace("\\xc1","&Aacute;")
                        content_str = content_str.replace("\\xc2","&Acirc;")
                        content_str = content_str.replace("\\xc3","&Atilde;")
                        content_str = content_str.replace("\\xc9","&Eacute;")
                        content_str = content_str.replace("\\xca","&Ecirc;")
                        content_str = content_str.replace("\\xcd","&Iacute;")
                        content_str = content_str.replace("\\xd1","&Ntilde;")
                        content_str = content_str.replace("\\xd3","&Oacute;")
                        content_str = content_str.replace("\\xd4","&Oacute;")
                        content_str = content_str.replace("\\xe3","&auml;")
                        content_str = content_str.replace("\\xe4","&atilde;")
                        content_str = content_str.replace("\\xe8","&egrave;")
                        content_str = content_str.replace("\\xda","&Uacute;")
                        content_str = content_str.replace("\\xd5","&Otilde;")
                        content_str = content_str.replace("\\xe7","&Ccedil;")
                        content_str = content_str.replace("\\xc7","&ccedil;")
                        content_str = content_str.replace("\\xe9","&eacute;")
                        content_str = content_str.replace("\\xea","&ecirc;")
                        content_str = content_str.replace("\\xed","&iacute;")
                        content_str = content_str.replace("\\xfa","&uacute;")
                        content_str = content_str.replace("\\xf4","&ocirc;")
                        content_str = content_str.replace("\\xf1","&ntilde;")
                        content_str = content_str.replace("\\xf3","&oacute;")
                        content_str = content_str.replace("\\xf5","&otilde;")
                        content_str = content_str.replace("\\xf6","&ouml;")
                        content_str = content_str.replace("\\u03bb","&#955;")
                        content_str = content_str.replace("\\u0394","&#916;")
                        content_str = content_str.replace("\\u03bc","&#956;")
                        content_str = content_str.replace("\\u03c1","&#961;")
                        content_str = content_str.replace("\\xb5","&#956;")
                        content_str = content_str.replace("\\u2030","&#8240;")
                        content_str = content_str.replace("\\u03a8","&#968;")
                        content_str = content_str.replace("\\xb0","&#176;")
                        content_str = content_str.replace("\\xb7","&#8901;")
                        content_str = content_str.replace("\\u03b1","&#945;")
                        content_str = content_str.replace("\\u03b2","&#946;")
                        content_str = content_str.replace("\\u03b3","&#947;")
                        content_str = content_str.replace("\\u03b4","&#948;")
                        content_str = content_str.replace("\\u03b5","&#949;")
                        content_str = content_str.replace("\\u03b8","&#952;")
                        content_str = content_str.replace("\\u2264","&#8804;")
                        content_str = content_str.replace("\\xb1", "&#177;")
                        content_str = content_str.replace("\\u02da","&#176;")
                        content_str = content_str.replace("\\u03ba","&#954;")
                        content_str = content_str.replace("\\u2022","&#8226;")
                        content_str = content_str.replace("\\u2212","&#8722;")
                        content_str = content_str.replace("\\u2261","&#8801;")
                        content_str = content_str.replace("\\uf062","&#914;")
                        content_str = content_str.replace("\\uf067","&#947;")
                        content_str = content_str.replace("\\u2192","&#8594;")
                        content_str = content_str.replace("\\xb4","'")
                        content_str = content_str.replace("\\u0113","&emacr;")

                        contents_final = content_str.split("|")

                else:
                    ## no more lines to be read from file; print tags and content to file
                    ## be sure file does not already exist in directory, because file is being opened in append mode and you will get duplicates

                    f = open('collection_data.csv' , 'ab')

                    ##write main content lines to csv file
                    wr = UnicodeWriter(f, delimiter='|', lineterminator='\r\n')
                    wr.writerow(tag_list)
                    wr.writerow(contents_final)

                    ##write collapsed subject lines to csv file
                    wr = UnicodeWriter(f, delimiter=',', lineterminator='\r\n')
                    wr.writerow(subject_list)
                    wr.writerow(LCSH_list)  #not migrating LCSH data at this time

                    ##empty lists for next pass
                    del tag_list[:]
                    del content_list[:]
                    del contents_final[:]
                    del subject_list[:]
                    del LCSH_list[:]

        ##Processing URLs of items; the item ID will be sliced and concatenated in, in Excel
        if filename.endswith('.pdf') or filename.endswith('.doc') or filename.endswith('.docx'):
    		##or filename.endswith('.jpg') or filename.endswith('.tif'):
        ##or filename.endswith('.xls') or filename.endswith('.xlsx') or filename.endswith('.html'):
            url_string.append('http://repository.unm.edu/bitstream/handle/1928/')
            url_string.append(filename)

            #print url_string
            ##write url string to csv file
            f = open('url_data.csv' , 'ab')
            wr = csv.writer(f, delimiter=';',lineterminator='\r\n')
            wr.writerow(url_string)
            ##empty the list for the next pass
            del url_string[:]
