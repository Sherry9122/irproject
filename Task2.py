import math
import task_1_a

# Task 2
# The function takes in 2 variables, the searching corpus in terms of inverted index and the query, and returns a list of docids and its cosine score
def cosine(invIdx, qwords):
    doclist = findDocs(invIdx, qwords)
    print "dealing " + str(len(doclist)) + " docs"
    for doc in doclist:
        print "dealing " + str(doc)
        doclist[doc] = calCosine(invIdx, qwords, doc)
    return doclist

# The function deals with the query, the input is a txt file and the reuturn is a list of list of query words
def dealQuery(querytxt):
    query = []
    file = open(querytxt + ".txt", "r")
    querys = file.readlines()
    for line in querys:
        qwords = line.split(" ")
        qwords = qwords[: len(qwords) - 1]
        query.append(qwords)
    return query

# The function finds the list of all the documents that comtain at least one of the query word
# The input is the inverted index and qurey, and the return value is a set of docids which contain the query word
def findDocs(invIdx, qwords):
    doclist = {}
    for qword in qwords:
        if qword in invIdx.keys():
            for docid in invIdx[qword]:
                doclist[docid] = 0
    return doclist

# The function calculates the cosine score of a specific document
# input: invIdx: inverted index, qwords: the parsed query words, doc: the docid of the document
# return: a float number which is the cosine score of the input document
def calCosine(invIdx, qwords, doc):
    # fractions: fenzi
    frasum = 0
    # numerator: fenmu  numsum
    dijsum = 0
    qjsum = 0
    dij = []
    qj = []
    i = 0
    dijnum = calDijNum(invIdx, doc)
    for term in invIdx:
        dij.append(calDijFra(term, invIdx, doc) / dijnum)
        qj.append(calQj(term, qwords))
    while i < len(dij):
        frasum = frasum + dij[i] * qj[i]
        dijsum = dijsum + dij[i] * dij[i]
        qjsum = qjsum + qj[i] * qj[i]
        i = i + 1
    numsum = (dijsum * qjsum) ** 0.5
    return frasum / numsum

# The function calculates the fraction of the dij of a specific term in a specific document
# input: invIdx: inverted index, term: the word, doc: the docid of the document
# return: a float number which is the fraction of the dij
def calDijFra(term, invIdex, docid):
    N = 3204.0
    nk = len(invIdex[term])
    if docid in invIdex[term]:
        fik = invIdex[term][docid]
    else:
        fik = 0.0
    dijfra = (math.log10(fik + 1.0)) * math.log10(N / nk)
    return dijfra

# The function calculates the numerator of the dij of a specific document
# input: invIdx: inverted index, doc: the docid of the document
# return: a float number which is the numerator of the dij
def calDijNum(invIdex, docid):
    N = 3204.0
    dijnum = 0
    for word in invIdex:
        nk1 = len(invIdex[word])
        if docid in invIdex[word]:
            fik1 = invIdex[word][docid]
        else:
            fik1 = 0.0
        temp = (math.log10(fik1 + 1.0)) * math.log10(N / nk1)
        dijnum = dijnum + temp * temp
    dijnum = dijnum ** 0.5
    return dijnum

# The function calculates qj of a term
# input: qterm: the word, qwords: the parsed queries
# return: 0 or 1 which is the the qj the term
def calQj(qterm, qwords):
    if qterm in qwords:
        return 1
    else:
        return 0

# The function write the search result in txt files
# input: result: dict of docids and cosine score, fileid: the dict that stroes the docid and its corresponding filename
#        filename: the new created file name that stores the result, queryId: mainly a number like 1, 2, 3
def writeresult(result, filename, queryId):
    fo = open(filename + ".txt", "a")
    counter = 1
    for stuff in sorted(result, key=result.get, reverse=True):
        if counter < 101:
            print result[stuff]
            fo.write(str(queryId) + " Q0 " + " CACM-" + stuff + " " + str(counter) + " " + str(result[stuff]) + " CosineSim")
            fo.write('\n')
            counter = counter + 1
        else:
            fo.close()
            return
    fo.close()



invedI = task_1_a.index()

querys = dealQuery("cacm_query")

qnum = 0
fo = open("Cosine_Res.txt", "a")
fo.write("query_id Q0 doc_id rank CosineSim_score system_name: CosineSim" + "\n")
fo.close()
# for query in querys:

result = cosine(invedI, querys[3])
writeresult(result, "Cosine_Res", qnum)
qnum = qnum + 1

# doclist1 = cosine(inved, "global warming potential")
# # write doclist1
# writeresult(doclist1, fileid, "resQ1", 1)
# print doclist1
#
# doclist2 = cosine(inved, "green power renewable energy")
# # write doclist1
# writeresult(doclist2, fileid, "resQ2", 2)
# print doclist2
#
# doclist3 = cosine(inved, "solar energy california")
# # write doclist1
# writeresult(doclist3, fileid, "resQ3", 3)
# print doclist3
#
# doclist4 = cosine(inved, "light bulb bulbs alternative alternatives")
# # write doclist1
# writeresult(doclist4, fileid, "resQ4", 4)
# print doclist4

