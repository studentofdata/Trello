import trello
import requests
import json
############################################
# Purpose of file goes here, inputs and outputs listed, functionality TODO
#
#<script src="https://api.trello.com/1/client.js?key=04a84b15c26fef1d7145a61cc1c48a22"></script>


API_KEY = '04a84b15c26fef1d7145a61cc1c48a22'
API_TOKEN = '169780f1bd281ee68f4819fd382094aa8edbde41632856226c12e58f74631f98'
O_AUTH = 'd5e32347118a51db16e311083d9608402281b3a88549926326b6d08199a9d41c'

board_url = 'https://trello.com/b/SiE5d0Ic/todo-daily'
board_id = '57a918baa38e9b4b94e18b7b/'

base_path = 'https://api.trello.com/1/'
boards = 'boards/'
cards = 'cards/'

requests.get('https://api.trello.com/1/client.js?key=04a84b15c26fef1d7145a61cc1c48a22')

resp = requests.get(base_path + boards + board_id + cards)
json_data = json.loads(resp.text)



def generateTrelloData():
    # ADD IN PROPER DOCUMENTATION FOR THIS FUNCTION HERE
    # PROPOSE TWO AMENDMENTS
    work_object = []
    i = 0
    for card in json_data:
        current_card = card
        task_name = current_card['name']
        id_labels = current_card['id']
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
        work_object[i]['name'] = task_name
        work_object[i]['labels'] = ','.join(work_type)
        work_object[i]['ids'] = id_labels
        
    
        print task_name, " ", id_labels
        card_id = str(id_labels)
        cards_response = requests.get(base_path + cards + card_id + "/actions")
        
        cards_data = json.loads(cards_response.text)
        hrs = []
        for c in cards_data:
            card_action_type = c['type']
            if card_action_type == "commentCard":
                card_text = c['data']['text']
                if 'hrs' in card_text:
                    hrs.append(card_text)
      
        work_object[i]['hrs'] = ','.join(hrs)
    
        i+=1

    return work_object



