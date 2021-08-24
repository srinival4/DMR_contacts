#!/usr/bin/env python
# coding: utf-8



import sys
import os.path
import json
import numpy as np
import pandas as pd
import requests
from pandas.io.json import json_normalize





print("Lastest Contacts Tool")
print ("Syntax RadioIdTrimmed  <x>")
print("")





#Function to figure out validity of JSON
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True





#Query to get data from radioid.net
apiurl = "https://www.radioid.net/static/users.json" 
apireq = requests.get(apiurl)
radioidlist = json.loads(apireq.text)





df_radiolist = json_normalize(radioidlist, record_path=['users'])





#Export “Last Heard” contacts from brandmeister.network contact export tool for Talkgroups of interest.
# into BrandMeister_Contacts_export_for_specific_talkgroups.csv
df_BM = pd.read_csv("/home/patna/hamradio/BrandMeister_Contacts_export_for_specific_talkgroups.csv")



# Identify Radio_ID records for those who have transmitted recently by 
# by matching the radio_ids between radio_id records and BrandMeister records.
final_df = df_radiolist.loc[df_radiolist['radio_id'].isin(df_BM['ID'])]




#create final json to match the RadioID json format
str_json= final_df.to_json(orient = 'records')
edit_str_json = '{' + '"users"'  +': ' + str_json + '}'




#If valid JSON, write to file

if (is_json(edit_str_json)):
    save_path = '/home/patna/hamradio/'
    completeFileName = os.path.join(save_path, "edited_users_in_python.json")
    text_file = open(completeFileName, "w")
    text_file.write(edit_str_json)
    text_file.close()
    







