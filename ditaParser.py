#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Axel
#
# Created:     06/02/2014
# Copyright:   (c) Axel 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import re
import pdb
import pickle
import json
import xml.etree.ElementTree as ET

def pickleData(path,data):
    """Save object to a file"""
    f=open(path,'w')
    pickle.dump(data, f)
    f.close()

def unpickleData(path):
    """Load object from a file"""
    f=open(path,'r')
    data=pickle.load(f)
    f.close()
    return data

def jsonSave(path,data):
    with open(path, 'wb') as fp:
        json.dump(data, fp)

def jsonLoad(path,data):
    with open(path, 'rb') as fp:
        data = json.load(fp)
    return data

def main():
    #extractClassificationData('../Data/January',True)
    pass

if __name__ == '__main__':
    main()

def extractClassificationDataAllDirs(directory,singleFile,directoryPrefix):
#directory is where all the books are (includes trailing '/')
#singlefile is whether we want to extract all the text and put it in a single file or not
#directoryPrefix is the directory where we want to write the results (it is created if it doesn't exist)

    dirs = os.listdir(directory)
    cont = 0
    dictionaryTopics = {} #contains a mapping from name to integer (topic id)
    conrefReuse = {} #contains a mapping from integer (topic id) to integer (topic id)
    keyrefReuse = {} #contains a mapping from integer (topic id) to list of keywords
    for dir in dirs:
        print "Extracting docs from " + dir
        cont = extractClassificationData(directory + dir + '/',singleFile, cont, directoryPrefix, dictionaryTopics, conrefReuse, keyrefReuse)

    for keyconref in conrefReuse:
        conrefReuse[keyconref] = dictionaryTopics[conrefReuse[keyconref]]
    jsonSave(directoryPrefix + 'conref',conrefReuse)
    jsonSave(directoryPrefix + 'keyref',keyrefReuse)
    jsonSave(directoryPrefix + 'topics',dictionaryTopics)
    return conrefReuse, keyrefReuse, dictionaryTopics


def extractClassificationData(directory,singleFile, cont,directoryPrefix, dictionaryTopics, conrefReuse, keyrefReuse):
#directory of a particular book
#singlefile is whether we want to extract all the text and put it in a single file or not
#directoryPrefix is the directory where we want to write the results (it is created if it doesn't exist
#dictionaryTopics contains a mapping from name to an integer
#contains a mapping from integer (topic id) to name
#contains a mapping from integer (topic id) to list of keywords

	#Set output file names
    labelFileName = 'topicLabels' #Indicates topic type (one topic per row)
    idBookTopicFileName = 'idBookTopic' #Indicates id, book, topic name (one  per row)
    dataFileName = 'data' #text of all topics (Used in case singleFile is true)
	
	#set comment tags regular expression
    regexComments = re.compile(".*comment.*")

	#Extract book name
    r = re.match(".*/(.*)/",directory)
    bookName = r.group(1)

	#get topic file names
    files = os.listdir(directory)

	#create output directory if necessary
    if not (os.path.exists('./' + directoryPrefix)):
        os.makedirs('./' + directoryPrefix)

	#create output files if they don't exits (if they do they will be appended)
    if not(os.path.exists('./' + directoryPrefix + labelFileName)):
        labelFile = open(directoryPrefix + labelFileName,'w')
        idBookTypeFile = open(directoryPrefix + idBookTopicFileName,'w')
        labelFile.close()
        idBookTypeFile.close()

	#In case we want all the text in a single file (not useful anymore)
    if singleFile:
        dataFile = open(dataFileName,'w')
        dataFile.close()

    for f in files:
		#Pragmatic way of checking that is a dita file
        if (len(f)>=5) and (f[-5:]=='.dita'):


            #check if not repeated update dictionary
            if not(dictionaryTopics.has_key(f)):
                #update dictionary
                dictionaryTopics[f] = cont

                #extract topic name
                topicName = f[0:-5]

                #get the root of the topic xml
                root = extractTopicTypeFromFile(directory + f)

                #Append data to output files (labelFile, idBookTypeFile)
                labelFile = open(directoryPrefix +labelFileName,'a')
                labelFile.write(root.tag + '\n')
                labelFile.close()

                idBookTypeFile = open(directoryPrefix +idBookTopicFileName,'a')
                idBookTypeFile.write(str(cont) + ', ' + bookName + ', ' + topicName + '\n')
                idBookTypeFile.close()

                #Get the text from the xml content
                text = extractTextContentFromTree(root,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
                if not(singleFile):
                    #Content goes in separate files
                    if not os.path.exists('./' + directoryPrefix + bookName):
                        #Check if book directory has been created
                        os.makedirs('./' + directoryPrefix + bookName)
                    if not os.path.exists('./' + directoryPrefix + bookName + '/' + root.tag):
                        #Check if topic type directory has been created
                        os.makedirs('./' + directoryPrefix + bookName + '/' + root.tag)
                    #dataFile = open('./' + root.tag + '/' + dataFileName + str(cont).zfill(4),'w')
                    dataFile = open('./' + directoryPrefix + bookName + '/' + root.tag + '/' + topicName,'w')
                else:
                    #content goes in a same file (Not mantained)
                    if not os.path.exists(root.tag):
                        os.makedirs(root.tag)
                    dataFile = open('./' + root.tag + '/' + dataFileName,'a')

                if not(singleFile):
                    dataFile.write(text)
                else:
                    dataFile.write(text + '\n*****\n')
                dataFile.close()

                cont = cont + 1
    return cont


def extractTextContentFromTree(root,directory, cont, dictionaryTopics,  conrefReuse, keyrefReuse, regexComments):
    #f = open(filePath,'r')
    #tree = ET.parse(filePath)
    #root = tree.getroot()
    text = ''
    array=[]
    for node in root.findall('*'):
        #pdb.set_trace()
        #print text.decode('utf-8')
##        if node.tag=='title':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
##        if node.tag=='shortdesc':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
##        if node.tag=='conbody':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
##        if node.tag=='taskbody':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
##        if node.tag=='refbody':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
##        if node.tag=='body':
##            text = text + ET.tostring(node,encoding = 'UTF-8', method='text')

        if node.tag=='title':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
        if node.tag=='shortdesc':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
        if node.tag=='conbody':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
        if node.tag=='taskbody':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
        if node.tag=='refbody':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)
        if node.tag=='body':
            text = text + printXMLwithParagraph(node,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)


    #text = text.replace('\t','')
    return text

def printXMLwithParagraph(nodeInit,directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments):
    #pdb.set_trace()
    text = ''
    tree=nodeInit.findall('./*')
    if (len(tree)==0):
        #no children
        node = nodeInit
        #if node.tag == 'p':
        #    text = text + '<p>' + ET.tostring(node,encoding = 'UTF-8', method='text') + '</p>'
        #else:
        text = text + ET.tostring(node,encoding = 'UTF-8', method='text')
    else:
		#tree has children
        allText = ET.tostring(nodeInit,encoding = 'UTF-8', method='text')
        count=0
        for node in tree:
            #pdb.set_trace()
            if (count ==0):
                #copy the text until the first tag
                indexToShow = allText.find(ET.tostring(node,encoding = 'UTF-8', method='text'))
                text = text + allText[0:indexToShow]
                count = count + 1

            if node.attrib.has_key('conref'):
                #check if there is a conref reuse case
                conrefURI = node.attrib['conref'].split('#')
                reusedNode = getConrefReuse(conrefURI[0],conrefURI[1], directory)
                text = text + '<p>' + printXMLwithParagraph(reusedNode, directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments) + '</p>'

                #add entry to the dictionary to be used as ground truth
                conrefReuse[cont] = conrefURI[0]
                #print node.tag #wondering what tags are used for reuse?
            else:
                if (node.tag == 'p') or (node.tag == 'li') or (node.tag == 'step'):
                #these tags are used to split in "paragraphs" we call paragraphs anything that can be reused
                        text = text + '<p>' + printXMLwithParagraph(node, directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments) + '</p>'
                else:
                    if node.tag == 'keyword':
                    #keyref reuse case
                        #pdb.set_trace()
                        keyref = node.attrib['keyref']
                        keyword = getKeyRef(keyref, directory)
                        text = text + " " + keyword + printXMLwithParagraph(node, directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)

                        #add entry to the dictionary to be used as ground truth
                        if not(keyrefReuse.has_key(cont)):
                            keyrefReuse[cont] = [keyword]
                        else:
                            keyrefReuse[cont].append(keyword)
                    elif regexComments.match(node.tag):
                        pass
                    else:
                        text = text + printXMLwithParagraph(node, directory, cont, dictionaryTopics, conrefReuse, keyrefReuse, regexComments)

    return text


def extractTopicTypeFromFile(filePath):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(filePath,parser)
    root = tree.getroot()
    return root

def getConrefReuse(fileName,idValue,directory):
    node = extractTopicTypeFromFile(directory+fileName)
    #pdb.set_trace()
    #select the element (at any level) that has the given id
    return node.find('.//*[@id="'+idValue+'"]')

def getKeyRef(keyref, directory):
    files = os.listdir(directory)
    for f in files:
        #Pragmatic way of checking that is a ditamap file
        if (len(f)>=8) and (f[-8:]=='.ditamap'):
			#extract topic name
            topicName = f[0:-8]

            #get the root of the topic xml
            root = extractTopicTypeFromFile(directory + f)
            element = root.find('.//keydef[@keys="'+keyref+'"]')
            return ET.tostring(element,encoding = 'UTF-8', method='text')