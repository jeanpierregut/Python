import dropbox
import csv
import pandas as pd
import requests
import json
from datetime import datetime
import pdb #debugger

######
# FUNCTIONS
######

def WriteTeamMembers(dbx): #under dropbox.dropbox

	membersList = []
	membersID = []
	
	thisdict = {
		"members": '',
		"ID": ''
	}
	
	dbevents = dbx.team_members_list().members #list of [TeamMemberInfo] objects

	for x in dbevents:
		membersList.append(x.profile.email)
		membersID.append(x.profile.team_member_id)
		thisdict[x.profile.email] = x.profile.team_member_id

	df = pd.DataFrame.from_dict(thisdict, orient='index')
	df.to_csv('members.csv')

	return thisdict


def GetUsage(dbx): #under dropbox.dropbox

	dbevents = dbx.team_reports_get_storage().total_usage #list of [ints] but what specifically does this denote?

	#with open ("usage.csv", 'w', newline='') as myfile:
		#wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		#wr.writerow(dbevents)

def LogEvents(dbx): #under dropbox.dropbox

	dbevents = dbx.team_log_get_events().events #list of [TeamEvents] objects

	timeStamp = []
	eventType = []
	users = []


	for x in dbevents:
		
		timeStamp.append(x.timestamp)
		eventType.append(x.event_type)
		# print(x.timestamp.str() + " --- " + x.event_type.str())


	#with open ("events.csv", 'w', newline='') as myfile:
		#wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		#wr.writerow(dbevents)

def ListFiles(dbx):


	cursor = ""
	has_more = True
	initial_call_made = False

	while has_more:

		get_member_files_result = None

		if initial_call_made:
			get_member_files_result = dbx.files_list_folder_continue(cursor)

		else:
			get_member_files_result = dbx.files_list_folder("",recursive=True)
			initial_call_made = True

		for i in get_member_files_result.entries:
			
			print("File Name: ", i.name)
			print("File Path: ", i.path_lower)

			path = i.path_lower

			try:
				filedate = findModified(path)

			except KeyError:
				filedate = None

			print("File Date: ",filedate)

			print(" -- ")

		cursor = get_member_files_result.cursor
		has_more = get_member_files_result.has_more

def findModified(file_path):

	datetimeobject = ''
	
	url = "https://api.dropboxapi.com/2/files/get_metadata"

	headers = {
	    "Authorization": <REDACTED>,
	    "Content-Type": "application/json"
	}

	data = {
	    "path": file_path
	}

	r = requests.post(url, headers=headers, data=json.dumps(data))
	file = r.json()
	string = file['server_modified']
	string = string.replace("T"," ")
	string = string.replace("Z","")
		
	datetimeobject = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

	return datetimeobject


def getOldDate(dbx):

	result = dbx.files_list_folder("",recursive=True);
	
	currentdate = datetime.now()
	oldestdate = currentdate

	for i in result.entries: #result.entries = metadata object

		print("File Name: ", i.name)

		path = i.path_lower

	
		filedate = findModified(path)

		print("Last Modified Date: ", filedate)

		if (filedate < oldestdate):
			oldestdate = filedate

		print("-")

	print("The oldest file in this account is ", oldestdate)


#######
# MAIN
#######

TOKEN = 'REDACTED'
PERSONAL = 'REDACTED'

dbx = dropbox.DropboxTeam(TOKEN)
#dbx = dropbox.Dropbox(PERSONAL)

#membersList = WriteTeamMembers(dbx)
#GetUsage(dbx)
#LogEvents(dbx)
ListFiles(dbx.as_user(PERSONAL))
#getOldDate(dbx.as_user(PERSONAL))
