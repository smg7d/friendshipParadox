import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

ratioList = []
nameList = []
totalFollowerCount = []

errors = 0
#get the master dict

for subdir, dirs, files in os.walk("./results"):
	for file in files: #for each file in the results directory
		if file[-3:]=="txt": #if it's a text file
			f = open(str(os.getcwd() + "/results/" + file), 'r')  #open it
			tempString = f.read()  #read it
			tempDict = eval(tempString)  #add the ratio to the ratioList
			f.close()  #close the file
			try:
				ratioList.append(tempDict['ratio'])
				totalFollowerCount.append(tempDict['ratio'] * tempDict['average'])
				nameList.append(file[:-4])
			except:
				errors += 1

data = pd.DataFrame({'name' : nameList, 'total_followers' : totalFollowerCount, 'ratio' : ratioList})

print(data.head(5))
newplot = sns.scatterplot(x="total_followers", y="ratio", data=data)
plt.show()


sns.distplot(ratioList)
plt.show()

