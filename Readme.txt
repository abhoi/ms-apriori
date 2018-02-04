Code is in single file:

DataMiningProject1.py

To run program:

Input file names and location have to be mentioned in the following place:

Input Transaction.txt file - Line 17(inputFile = open(r'inputdata.txt','r'))
Input Parameter.txt file - Line 30(parameterFile = open(r'parameters1.txt','r'))

Output file name and location:

Ouput file - Line 316(outputfile = open(r'outputpatterns.txt','w+'))

If these are not specified:

Python will search for the files in the current working directory and if present will create
the output file in the same current working directory