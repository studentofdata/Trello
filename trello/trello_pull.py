import trello
import requests
import json
"""This module grabs the "TODO DAILY" Trello board.

rename so it says "extraction" rather than pull.

Here we take a board url as well as credentials to access the board via Trello. With this
we take down the board and process the cards into a data structure. Each card title is going
to represent a task and each card can have attributes and content associated with it. A card in our
case has comments which we use to post hours and labels which denote the type of task and the department
the task is being performed for. This will give us insight into how I am spending my time and clear on what
I am accomplishing.


"""

#Hardcode in credentials
API_KEY = '04a84b15c26fef1d7145a61cc1c48a22'
API_TOKEN = '169780f1bd281ee68f4819fd382094aa8edbde41632856226c12e58f74631f98'
O_AUTH = 'd5e32347118a51db16e311083d9608402281b3a88549926326b6d08199a9d41c'

#The board url I grabbed from trello
board_url = 'https://trello.com/b/SiE5d0Ic/todo-daily'
board_id = '57a918baa38e9b4b94e18b7b/'


#Trello API calls
base_path = 'https://api.trello.com/1/'
boards = 'boards/'
cards = 'cards/'

#Authorize
requests.get('https://api.trello.com/1/client.js?key=04a84b15c26fef1d7145a61cc1c48a22')

#Grab all cards from the entire board
resp = requests.get(base_path + boards + board_id + cards)
json_data = json.loads(resp.text)



#Here is the function that will generate a data structure parsing the json_data 
def generateTrelloData():
    """ The initial Trello grab, data is immediately parsed into a 'work_object' and 
    returned. work_object only contains the data pieces needed for the current analysis
    because all data is available anyways with timestamps, no need to download and store
    entire copies of trello boards every day,week,month. This is the Extraction process """
    
    work_object = []
    i = 0
    for card in json_data:
        current_card = card
        task_name = current_card['name']
        card_id = str(current_card['id'])
        try:
            labels = current_card['labels']
            num_labels = len(labels)
            work_type = []
            for l in labels:
                work_type.append(l['name'])
        except:
            print "List Index is probably out of range"
        
        work_object.append(task_name)
        work_object[i] = {}
        work_object[i]['task_name'] = task_name
        work_object[i]['labels'] = ','.join(work_type)
        work_object[i]['ids'] = card_id
        
        print task_name, " ", card_id
        cards_response = requests.get(base_path + cards + card_id + "/actions")
    
        cards_data = json.loads(cards_response.text)
        hrs = []
        name = []
        date = []
        for c in cards_data:
            
            card_action_type = c['type']
            if card_action_type == "commentCard":
                
                card_text = c['data']['text']
                card_date = c['date']
                board_name= c['data']['board']['name']
                
                if 'hrs' in card_text:
                    hrs.append(card_text)
                    date.append(card_date)
      
        work_object[i]['hrs'] = ','.join(hrs)
        work_object[i]['date'] = ','.join(date)
        work_object[i]['board_name'] = board_name
    
        i+=1
    
    return work_object



