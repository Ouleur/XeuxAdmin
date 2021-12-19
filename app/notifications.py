"""
Title: Mercure publisher 
Description: Implemantation of mercure protocole publisher in python3
Version: 0.0.1
Author: ADOU VIANNEY <Ouleur>
Mail: adoujmv@gmail.com
Date: 30 / 06 / 2020
City: Abidjan
"""

import requests
import jwt
import json
import socket
from flask import current_app,g


#Mercure Payload, do you add information in subscribe or in publish
payload = {
 "mercure": {
  "subscribe": [
  ],
  "publish": [
  ]
 }
}

#jwt header
header = {
 "typ": "JWT",
 "alg": "HS256"
}

#The secret key used to run mercure on server
secret= "OmarksMerconSysteme"

# use decode("utf-8") for convert b'' value in string value
DEMO_JWT = jwt.encode(payload, secret, algorithm='HS256',headers=header)

#Mercure instance url

headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer {}".format(DEMO_JWT )
}

#use the 'headers' parameter to set the HTTP headers:
def execute(postData):
    app = current_app._get_current_object()
    print(app.config['MERCURE_URL'])
    url = "{}/.well-known/mercure".format(app.config['MERCURE_URL'])

    x = requests.post(url, data = postData, headers = headers)
    # show request value
    print('Publish #ID ',x.text)
    # print(DEMO_JWT)

def sinistre_notification(data,id):
    #the Data you will to send id the content on data key and topic is the topic on that you publish data
    print(str(data))
    postData = {
        'topic': 'https://example.com/notif/{}'.format(id),
        'data' : json.dumps(data),
    }
    execute(url,postData)

def ticket_ecran_notification(data,id):
    #the Data you will to send id the content on data key and topic is the topic on that you publish data
    print(str(data))
    postData = {
        'topic': 'https://example.com/notif/',
        'data' : json.dumps(data),
    }
    execute(postData)

def ticket_client_notification(data,id):
    #La notification sur l'ecran d'appel lorsqu'on appel un client 
    print(str(data))
    postData = {
        'topic': 'https://example.com/notif/',
        'data' : json.dumps(data),
    }
    execute(postData)

def ticket_guichet_device(topic,data):
    #La notification des guichet du service lorsqu'un client prend un ticket
    print(str(data))
    postData = {
        'topic': 'https://example.com/tickets/{}'.format(topic),
        'data' : json.dumps(data),
    }
    execute(postData)

def ticket_client_device(topic,data):
    #La notification divice du client lorsqu'on l'appel

    return ""

def publicite_media_notification(topic,data):
    #La notification des medias de la publicité
     
    return ""

