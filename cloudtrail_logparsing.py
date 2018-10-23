import boto3
import os
import gzip
import json
import time
from datetime import date
import decimal
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
  s3 = boto3.client("s3")
  dynamodb = boto3.resource('dynamodb')
  if event:
      print("Event : ", event)
      file_obj = event["Records"][0]
      filename = str(file_obj['s3']['object']['key'])
      print("filename: ", filename)
      fileObj = s3.download_file("traillog-parse", filename, "/tmp/" + filename.split('/')[-1])
      print("reading the file {0}".format(filename))
      with gzip.open("/tmp/" + filename.split('/')[-1],'r') as f:
          file_cont = f.read()
          file_content=json.loads(file_cont.decode('utf-8'))
      
      d = {}
      temp_dict = {}
      for record in file_content['Records']:
        if 'eventName' in record: 
          eventName = record['eventName']
          if eventName in d:
             value = d[eventName]
             value = value+1
             d[eventName] = value
          else:
             d[eventName] = 1
             
      for key, value in d.items():
        temp_dict[key] = value
        print(temp_dict)
    
      grouped_events = {}
      for key, value in d.items():
        if key.startswith("Describe"):
          if "Describe" in grouped_events:
            new_value = grouped_events["Describe"] + value
            grouped_events["Describe"] = new_value
            del temp_dict[key]
          else:
            grouped_events["Describe"] = value
            del temp_dict[key]
        
        elif key.startswith("Get"):
          if "Get" in grouped_events:
            new_value = grouped_events["Get"] + value
            grouped_events["Get"] = new_value
            del temp_dict[key]
          else:
            grouped_events["Get"] = value
            del temp_dict[key]
            
        elif key.startswith("List"):
          if "List" in grouped_events:
            new_value = grouped_events["List"] + value
            grouped_events["List"] = new_value
          else:
            grouped_events["List"] = value
            del temp_dict[key]
            
        elif key.startswith("Assume"):
          if "Assume" in grouped_events:
            new_value = grouped_events["Assume"] + value
            grouped_events["Assume"] = new_value
          else:
            grouped_events["Assume"] = value
            del temp_dict[key]
            
      print("Temp-dict:", temp_dict)
      print("Grouped:", grouped_events)      
      html_head = "<html>\n<body>\n<h2>Event Summary</h2>\n<table style=\"width:100%\">\n <tr>\n   <th>EventName</th>\n   <th>Occurence</th>\n </tr>\n"
      body_top = " <tr>\n"
      body_bottom = " </tr>\n"
      
      for event, value in grouped_events.items():
        event_name = "    <td>" + event + "</td>\n"
        event_value = "    <td>" + str(value) + "</td>\n"
        html_head = html_head + body_top + event_name + event_value + body_bottom
        
      #s3 = boto3.client("s3")
      TIME = time.strftime("%H:%M:%S")
      DATE = str(date.today())
      EXTENSION = ".html"
      EVENT_FILE_NAME = DATE + TIME + EXTENSION
      #object = s3.Object('8k-trailview', 'EVENT_FILE_NAME')
      #bject.put(Body=html_head)
      s3.put_object(Body=html_head, Bucket='8k-trailview', Key=EVENT_FILE_NAME)
      
      html_head = "<html>\n<body>\n<h2>Event Summary</h2>\n<table style=\"width:100%\">\n <tr>\n   <th>EventName</th>\n   <th>Occurence</th>\n </tr>\n"
      body_top = " <tr>\n"
      body_bottom = " </tr>\n"
      
      for event, value in temp_dict.items():
        event_name = "    <td>" + event + "</td>\n"
        event_value = "    <td>" + str(value) + "</td>\n"
        html_head = html_head + body_top + event_name + event_value + body_bottom
        
      #s3 = boto3.client("s3")
      TIME = time.strftime("%H:%M:%S")
      DATE = str(date.today())
      EXTENSION = ".html"
      EVENT_FILE_NAME = DATE + TIME + EXTENSION
      #object = s3.Object('other-events', 'EVENT_FILE_NAME')
      #bject.put(Body=html_head)
      s3.put_object(Body=html_head, Bucket='8k-nongrouped-events', Key=EVENT_FILE_NAME)

      
      
      