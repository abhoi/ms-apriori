
# coding: utf-8

# In[34]:

# imports done
import itertools

# Global Declarations
transactionList = []
sdc = 0.0

# Function to read input file

def inputfile():
    del transactionList[:]
    inputFile = open(r'data-2.txt','r')
    transactionString = inputFile.read();
    transactionString = transactionString.replace('{','')
    transactionString = transactionString.replace('}','')
    transactionString = transactionString.replace(' ','')
    initialList = transactionString.split('\n')
    for transaction in initialList:
        transactionList.append(transaction.split(',')) 
    inputFile.close()

# Function to read parameter file
def paramfile():
    param = []
    parameterFile = open(r'para2-1.txt','r')
    parameterString = parameterFile.read()
    misString = parameterString.split('\n')
    s = parameterString.split('SDC')[0].split('\n')
    s1 = parameterString.split('SDC')[1].split('\n')
    sdc = float(str(s1[0].split('=')[1]).strip())
    s.pop()
    for i in range(len(s)):
        s1 = s[i]
        s1 = s1.replace('MIS','')
        s1 = s1.replace('(','')
        s1 = s1.replace(')','')
        s[i] = s1
    mydict = dict((k.strip(), float(v.strip())) for k,v in 
                  (item.split('=') for item in s))
    s1 = parameterString.split('SDC')[1].split('\n')
    sdc = float(str(s1[0].split('=')[1]).strip())
    random = s1[1].split(':')[1].split('}')
    must_have = s1[2].split(':')[1].replace(' ', '').split('or')
    cannot_be_together = []
    for random1 in random:
        random2 = []
        random2 = random1.strip().replace('{','').replace(' ','').replace('\'','').replace(',',' ').strip().split(' ')
        if random2 == ['']:
            pass
        else:
            cannot_be_together.append(random2)
    param.append(mydict)
    param.append(sdc)
    param.append(cannot_be_together)
    param.append(must_have)
    parameterFile.close()
    return param

######## MS - Apriori Algorithm ##############
# Function to Sort the keys based on MIS values
def sort(combined):
    combined_List = [[k,v] for k, v in combined.items()]
    combined_List.sort(key=lambda pair: pair[1][0])
    return combined_List

# Function to generate Level-2 Candidate Generation 
def level2candidate(combined_List, l):
    c2 = []
    # print("L: " + str(l))
    print("L: " + str(l))
    for i in combined_List:
        print(i[0], end=', ')
    for j in range(len(combined_List)):
        if combined_List[j][0] in l and combined_List[j][1][1] >= combined_List[j][1][0]:
            for i in range(j+1, len(combined_List)):
                if combined_List[i][1][1] >= combined_List[j][1][0] and abs(combined_List[i][1][1] - combined_List[j][1][1]) <= sdc:
                    temp = []
                    temp.append(combined_List[j][0])
                    temp.append(combined_List[i][0])
                    c2.append(temp)
    return c2

# Function to get MIS of an element 
def getMIS(element, MIS_List):
        for i in range(len(MIS_List)):
            if element in MIS_List[i]:
                mis = MIS_List[i][1]
                break
        return mis

# Function to get support of an element
def getSupport(element, support_List):
    for i in range(len(support_List)):
        if element[0] in support_List[i]:
            support = support_List[i][1]
            break
    return support
    
# Function to generate candidate set for k > 2
def MS_CandidateGen(ftemp, MIS_List, support_List):
    fjoinlist = []
    fjointemp = []
    for i in range(len(ftemp)):
        f1 = ftemp[i][0:(len(ftemp[i])-1)]
        for j in range(i+1, len(ftemp)):
            f2 = ftemp[j][0:(len(ftemp[j])-1)]
            if f1 == f2 and abs(getSupport(ftemp[j][(len(ftemp[j])-1):], support_List) - getSupport(ftemp[i][(len(ftemp[i])-1):], support_List)) <= sdc:
                fjointemp = ftemp[i] + ftemp[j][(len(ftemp[j])-1):]
                fjoinlist.append(fjointemp)
                fjointemp = []
    i = 0
    while i < len(fjoinlist):
        subsetlist = list(set(itertools.combinations(fjoinlist[i], len(fjoinlist[i])-1)))
        for subset in subsetlist:
            if (fjoinlist[i][0] in subset) or (getMIS(fjoinlist[i][0], MIS_List) == getMIS(fjoinlist[i][1], MIS_List)):
                ftcounter = 0
                for ft in ftemp:
                    if list(subset) == list(ft):
                        ftcounter = ftcounter + 1
                        break
                if ftcounter == 0:
                    fjoinlist.pop(i)
                    i = i - 1
                    break
            if i == len(fjoinlist):
                break
        i = i + 1
    return(fjoinlist)


# In[ ]:

# Calling Input file
inputfile()

# Removing Empty Lists in transactionList
i=0
while(i<len(transactionList)):
    if transactionList[i] == ['']:
        transactionList.pop(i)
        i=i-1
    i=i+1
#print("transactionList")
#print(transactionList)

# Calling Parameter File to read MIS Values
param = paramfile()
mydict = param[0]
sdc = param[1]
cannot_be_together = param[2]
must_have = param[3]

# Creating Lists with MIS values and support values
support = {}
count = 0
for key in mydict:
    for transaction in transactionList:
        if key in transaction:
                count = count + 1
    support[key] = round(count/len(transactionList),2)
    count = 0
combined = dict([(k,[mydict[k],support[k]]) for k in mydict])
MIS_List = [ [k,v] for k, v in mydict.items() ]
support_List = [ [k,v] for k, v in support.items() ]
print("MIS_List")
# print(MIS_List)
print("support_List")
# print(support_List)

# MS - Apriori Algorithm Starts
# Step 1 - Sorting the list based on MIS values
combined_List = sort(combined)
print("combined_List with MIS and support -- Sorted based on MIS")
# print(combined_List)

# Step 2: Init-Pass
l = []
f = []
f1 = []
f2 = []
f3 = []
j = -1

for i in range(len(combined_List)):
    if combined_List[i][1][1] >= combined_List[i][1][0]:
        j = i
        break

for i in range(len(combined_List)):
    if combined_List[i][1][1] >= combined_List[i][1][0]:
        f1.append(combined_List[i][0])
    if j >= 0:
        if combined_List[i][1][1] >= combined_List[j][1][0]:
            l.append(combined_List[i][0])
print("l after init pass")
print(l)
i = 0
print("F1 before musthave: " + str(f1) + str(len(f1)))
while i < len(f1):
    if f1[i] in must_have:
        pass
    else:
        f1.pop(i)
        i = i - 1
    i = i + 1
print("f1 after init pass")
print(f1)
for f1obj in f1:
    count = 0
    for transaction in transactionList:
        if f1obj in transaction:
            count = count + 1
    f2.append([f1obj,count])
f.append(f2)

# Creating the loop to run the MS-Apriori Algorithm
k = 2
ftemp = []
while(k == 2 or len(ftemp) > 1):
    if k == 2:
        # Calling level 2 candidate Generation function
        print("COMBINED LIST: " + str(combined_List))
        c = level2candidate(combined_List, l)
        print("Level 2 Candidate Generation")
        print("C2: " + str(c))       
    else:
        # Calling candidate generation function for k > 2
        c = MS_CandidateGen(ftemp, MIS_List, support_List)
        print('Level K > 2 Candidate Generation')
        print(c)
    # Checking each c value and calculating f value
    count = 0
    mis = 0
    ftemp = []
    ftempwithcount = []
    ffinal = []
    for cg in c:
        for transaction in transactionList:
            if set(cg) < set(transaction):
                count = count + 1
        for i in range(len(MIS_List)):
            if cg[0] in MIS_List[i]:
                mis = MIS_List[i][1]
                break
        if count/len(transactionList) >= mis:
            ftemp.append(cg)
            ftempwithcount.append([cg,count])
        count = 0
    
    # Removing Cannot be together items
    i=0
    while i < len(ftemp):
        for eachset in cannot_be_together:
            if(set(eachset) <= set(ftemp[i])):
                ftemp.pop(i)
                ftempwithcount.pop(i)
                i = i - 1
                break
        i = i + 1

    # Removing sets without Must Have
    #i=0
    #while i < len(ftemp):
    #    must_have_counter = 0
    #    for eachvalue in must_have:
    #        if eachvalue in ftemp[i]:
    #            must_have_counter = must_have_counter + 1
    #            break
    #    if must_have_counter == 0:
    #        ftemp.pop(i)
    #        ftempwithcount.pop(i)
    #        i = i - 1
    #    i = i + 1

    print("for the count")
    print(ftempwithcount)
    print(ftemp)

    # Generating Frequency set with tail count
    count = 0
    freqsetwithtail = []
    ftemp0 = ftempwithcount
    for ftemp1 in ftemp0:
        ftemp2 = ftemp1[0][1:]
        ftemp3 = []
        for transaction in transactionList:
            if set(ftemp2) < set(transaction):
                count = count + 1
        ftemp3.append(ftemp1)
        ftemp3.append(count)
        freqsetwithtail.append(ftemp3)
        count = 0
    print("Frequent set with tail count")
    print(freqsetwithtail)
    print("Generated Frequency Set --- F" + str(k))
    if(len(freqsetwithtail) > 0):
        f.append(freqsetwithtail)
    j = 0
    for i in range(len(f)):
        if i == 0:
            pass
        else:
            while j < len(f[i]):
                counter = 0
                for subset in must_have:
                    if str(subset) in f[i][j][0][0]:
                        counter = 1
                        break
                if counter == 0:
                    f[i].pop(j)
                    j = j - 1
                j = j + 1
    print(f)
    k = k + 1

# Writing into output file	
outputfile = open(r'outputpatterns.txt','w+')

i = 0
while(i<len(f)):
    outputfile.write('Frequent '+str(i + 1)+'-itemsets\n')
    outputfile.write('\n')
    if i == 0:
        j = 0
        while j < len(f[i]):
            outputfile.write('\t'+str(f[i][j][1])+' : {'+str(f[i][j][0])+'}\n')
            j = j + 1
    else:
        j = 0
        while j < len(f[i]):
            outputfile.write('\t'+str(f[i][j][0][1])+' : {'+str(f[i][j][0][0]).replace("[","").replace("]","").replace("'","")+'}\n')
            outputfile.write('Tail count ='+str(f[i][j][1])+'\n')
            j = j + 1
    outputfile.write('\n\tTotal number of frequent '+str(i + 1)+'-itemsets = '+str(len(f[i]))+'\n\n')
    i = i + 1

outputfile.close()

