from webexteamssdk import WebexTeamsAPI
import requests
import json
import time

#Ask the user to use either the hard-coded token (access token within the code)
accessToken = input("Please enter your access token: ")
accessToken = "Bearer " + accessToken

# Access the room's API Endpoint
resp = requests.get( "https://webexapis.com/v1/rooms",
                  headers={"Authorization": accessToken}
                  )
headers={"Authorization": accessToken, "Content-type" : "application/json"}

# Handling responses
jsonData = resp.json()
rooms = jsonData["items"]
for room in rooms:
    userId = room["creatorId"] # Assign a var to store user Id  

# Function to display menu
def menu():
    print("\nOption 0: Test the connection with webex server")
    print("Option 1: Display information")
    print("Option 2: Display 5 rooms")
    print("Option 3: Create a room")
    print("Option 4: Send messages to a room")
    option = input("Please enter option (0/1/2/3/4) or (q to exit): ")
    print("\n")

    if option == "0":
        opt0() # Call function for option 0
            
    elif option == "1":
        opt1() # Call function for option 1
            
    elif option == "2":
        opt2() # Call function for option 2

    elif option == "3":
        opt3() # Call function for option 3
            
    elif option == "4":
        opt4() # Call function for option 4

    elif option == "q" or option == "Q":
        exit # Exit

    else:
        print("Wrong input") # If user enter the wrong option

# Function to test the connection to the Webex server
def opt0():
    
    # Check if the response from the API call was OK (resp. code 200)
    if not resp.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(resp.status_code, resp.text)) #Display Error message
    
    #If successful
    else:
        print("Connection successful! \n") 

    menu() # Call function menu to display an option
        
# Function to display user information.
def opt1():
    url= "https://webexapis.com/v1/people/me" # Get person details using user ID
    
    resp = requests.get(url, headers=headers)
    jsonData = resp.json()
    userEmails = resp.json()['emails']
    for userEmail in userEmails:
        print("User email: "+ userEmail)

    print("Nickname: " + jsonData['nickName'])
    print("Displayed name: " + jsonData['displayName'])
    menu() # Call function menu to display an option

# Function to Displays a 5 rooms.
def opt2():
    i = 1
    for room in rooms:
            j = str(i) #convert i to string j
            print (j + ". Room Id: " + room["id"])
            print ("Room title: " + room["title"])
            print ("Date created: " + room["created"])
            print ("Last activity: " + room["lastActivity"] + "\n")
            
            i += 1
            if i == 6:
                break
    menu() # Call function menu to display an option

# Function to create a new room.
def opt3():
    title = input("Enter the new room title: ")
    params = {
        'title' : title #create new room title baased on user input (title)
    }
    
    url = "https://webexapis.com/v1/rooms"
                  
    res = requests.post(url, headers=headers, json=params) #method to create a room
    print("Room has been created!")
    menu() # Call function menu to display an option

# Function to send a message to the selected room
def opt4():

    #To get the new room list if user create a new one
    resp = requests.get( "https://webexapis.com/v1/rooms",
                  headers={"Authorization": accessToken}
                  )

    headers={"Authorization": accessToken, "Content-type" : "application/json"}

    jsonData = resp.json()
    rooms = jsonData["items"] 

    #looping
    i = 0
    while i < 5:
        for room in rooms:
            print ("Room title: " + room["title"])
            i += 1
            
    print("\n")
    # User input a room title to send a message
    messageRoom = input("Choose a room to send message: ")
    for room in rooms:
        if(room["title"].find(messageRoom) != -1):
            roomId = room["id"]
    
    #Input message
    message = input("Enter the message that you want to send: ")

    url = 'https://webexapis.com/v1/messages'
    params = {
        'roomId' : roomId,
        'markdown' : message
    }
    res = requests.post(url, headers=headers, json=params) # POST method to send the message
    # Acknowledgement once the message has been sent
    print("Message has been sent !")
    
    menu() # Call function menu to display an option

# Call function menu to display option
print(menu())
