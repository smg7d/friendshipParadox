from InstagramAPI import InstagramAPI
import sys
import requests
import os
import time
from safe import sendMessage, accts

#get a userID associated with a username. API requires userIDs but only provides usernames from friends
def getUserID(username):
        route = 'https://www.instagram.com/web/search/topsearch/?context=user&count=0&query=' + username
        res = requests.get(route)
        return res.json()['users'][0]['user']['pk']

#get a list of all followers for a given username
def getFollowerList(username):
	user_id = getUserID(username)
	followers = api.getTotalFollowers(user_id)
	return followers

#get an integer representing the number of followers for a given username
def getFollowerCount(username):
	user_id = getUserID(username)
	api.getUsernameInfo(user_id)
	info = api.LastJson
	return info['user']['follower_count']

#average a list of integers or floats
def average(avList):
	total = 0
	for num in avList:
		total += num
	return total/len(avList)

#save a text file in the local directory. assumes only one dict in the file
def saveFile(filename, dictToAdd):
	newDict= {}

	if os.path.exists(filename): #if there is already a text file there
		#open the file as read only
		with open(filename, 'r') as f:
			string = f.read() #read the dict as a string
			newDict = eval(string) #convert it to a dictionary
			f.close() #close the file
		
		newDict.update(dictToAdd) #merge the two dictionaries
		f = open(filename, 'w') #open the file
		f.write(str(newDict)) #place the dictionary in the file
		f.close() #close the file
				
	else: 
		f = open(filename, 'w') #open the file
		f.write(str(dictToAdd)) #place the dictionary in the file
		f.close() #close the file

def getNextDictKey(mydict, curKey):
	if len(mydict.keys()) <= 1:
		return "not_found"

	found = False
	for item in mydict.keys():
		if item == curKey:
			found = True
		elif found == True:
			print("nextKey is " + str(item))
			return str(item)

	return "not_found"

#switch to the next account defined in a dict of accounts to avoid API call limit
def switchAccount(dictToSave):
	global api
	
	cur_acct = api.username #get the current username

	if cur_acct == "trial_acct_number_one": #if its the last name in the accts dict, sleep for an hour
		sendMessage("last account hit. sleeping for an hour")
		time.sleep(60*60) #sleep for an hour
		
	#get the next name in the dict and login
	nextKey = getNextDictKey(accts, cur_acct)
	if not nextKey == "not_found": #if we successfully got the next key
		api.logout() #log out the other account
		api = InstagramAPI(nextKey, accts[nextKey]) #define the new API object
		api.login() #log in the new one

def getMasterDict():
	if os.path.exists("masterDict.txt"): #if we have a master dict file already
		with open("masterDict.txt", 'r') as f:
			string = f.read() #read the dict as a string
			masterDict = eval(string) #convert it to a dictionary
			f.close() #close the file
	else:
		masterDict = {} #define the master lookup dictionary

	return masterDict

def getRatio(username, masterDict): #take a username, returns username # of friends / average of friends # of friends
	global api

	#get followers, follower count
	try:
		followers = getFollowerList(username) #get list of friends
	except:
		follower = [] #error occured. simply move on
		return
	myCount = len(followers) #get number of friends
	
	#set up to get followers friend count
	followersCount = {} #initialize friends' friendcount dict

	#populate list of followers' follower count
	for follower in followers: #for each friend
		if follower in masterDict: #if its in the master dict, then use that
			followersCount[follower] = masterDict[follower]
			print("used cache!")
		else:
			#else, try to get the data and add it to both dicts
			try:
				num = getFollowerCount(follower)
				followersCount[follower] = num #add the friend and his/her friend count to the dict
				masterDict[follower] = num
			except: #if error
				saveFile(username + ".txt", followersCount) #save data down to a file
				saveFile("masterDict.txt", masterDict) #save cached Dict down to a file
				switchAccount(followersCount) #switch usernames
				
		print(follower + " success")

	#when done with each friend
	followersCount['average'] = average(followersCount.values()) #add the average of the friend values to the dict for easy reference
	followersCount['ratio'] = myCount / followersCount['average'] #and add the ratio for easy reference as well
	saveFile(username + ".txt", followersCount) #save the users count dict
	saveFile("masterDict.txt", masterDict) #save the masterDict

	sendMessage("analysis done for " + str(username)) #send a message to my phone
	return followersCount['ratio']


if __name__ == "__main__":
	
	#initial login
	api = InstagramAPI(first_acct['username'], first_acct['password'])
	if (api.login()):
	    print("Login success!")
	else:
	    print("Can't login!")

	#get the full list
	friends = getFollowerList("smg7d")
	masterDict = getMasterDict() #get the hash table

	print(getRatio("smg7d", masterDict)) #run the analysis for me

	#getRatioList = getFollowerList("smg7d") #list of others to get Ratio of
	for friend in friends:
		masterDict = getMasterDict() #update the master hash table
		print(getRatio(friend, masterDict)) #run the analysis for the friend





