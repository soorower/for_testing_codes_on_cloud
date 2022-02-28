from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/885747859687866378/XZJEkus2I98yXl6Xuep0d_ckPeQz1msU9zs9INvomU3c8TAdvI6oiWSkln3SXd0dUK3y', username="Exchange Scraped File")
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import json as JSON
from time import sleep
import os
import re
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

links = pd.read_excel('datafromapi.xlsx')['api_link'].tolist()
# links = ['https://hub.docker.com/v2/repositories/balenalib/artik10-ubuntu']
data = {}
lists = []

list_not_working = []
count = 1
for link in links:
    sleep(0.4)
    print(count)
    count = count +1
    try:
        r = requests.get(link,headers = headers)
        soup = bs(r.content,'html.parser')
        print(r.status_code)
        if r.status_code != 200:
            sleep(10)
            r = requests.get(link,headers = headers)
            soup = bs(r.content,'html.parser')
            print(r.status_code)


        s = str(soup)
        # if s[-1]=='}':
        #     pass
        # else:
        #     s = s[:-34]
            
            
        user = s.split('{"user": ')[1].split(', "name"')[0][1:-1]
        name  = s.split('"name": ')[1].split(', "namespace"')[0][1:-1]
        namespace = s.split('"namespace": ')[1].split(', "repository_type"')[0][1:-1]
        rep_type = s.split('"repository_type": ')[1].split(', "status"')[0][1:-1]
        status = s.split('"status":')[1].split(', "description"')[0]
        
        
        description = s.split('"description": ')[1].split('", "is_private')[0][1:-1]
        is_private = s.split('"is_private":')[1].split(', "is_automated"')[0]
        is_automated = s.split('"is_automated":')[1].split(', "can_edit"')[0]
        can_edit = s.split('"can_edit":')[1].split(', "star_count"')[0]
        
        star_count = s.split('"star_count":')[1].split(', "pull_count"')[0]
        pull_count = s.split('"pull_count":')[1].split(', "last_updated"')[0]
        last_updated = s.split('"last_updated": ')[1].split(', "is_migrated"')[0][1:-1]
        is_migrated = s.split('"is_migrated":')[1].split(', "collaborator_count"')[0]
        
        collaborator_count = s.split('"collaborator_count":')[1].split(', "affiliation"')[0]
        affiliation = s.split('"affiliation":')[1].split(', "hub_user"')[0]
        hub_user = s.split('"hub_user": ')[1].split(', "has_starred"')[0][1:-1]
        has_starred = s.split('"has_starred":')[1].split(', "full_description"')[0]
        
        full_description = s.split('"full_description": ')[1].split(', "permissions"')[0]
        read_permissions = s.split('{"read":')[1].split(', "write"')[0]
        write_permissions = s.split('"write":')[1].split(', "admin"')[0]
        admin_permissions = s.split('"admin":')[1].split('}}')[0]

        print(name)
        data = {
            'user': user,
            'name':name,
            'namespace':namespace,
            'repository_type': rep_type,
            'status':status,
            'description':description,
            'is_private': is_private,
            'is_automated':is_automated,
            'can_edit': can_edit,
            'star_count':star_count,
            'pull_count':pull_count,
            'last_updated':last_updated,
            'is_migrated': is_migrated,
            'callaborator_count':collaborator_count,
            'affiliation':affiliation,
            'hub_user':hub_user,
            'has_starred':has_starred,
            'full_description':full_description,
            'read_permissions': read_permissions,
            'write_permissions': write_permissions,
            'admin_permissions': admin_permissions
         }
        lists.append(data)
    except:
        user = '-'
        name = '-'
        namespace = '-'
        rep_type = '-'
        status = '-'
        description = '-'
        is_private = '-'
        is_automated = '-'
        can_edit = '-'
        star_count = '-'
        pull_count ='-'
        last_updated = '-'
        is_migrated  = '-'
        collaborator_count = '-'
        affiliation = '-'
        hub_user = '-'
        has_starred = '-'
        full_description = '-'
        read_permissions = '-'
        write_permissions = '-'
        admin_permissions = '-'
        
        
        data = {
            'user': user,
            'name':name,
            'namespace':namespace,
            'repository_type': rep_type,
            'status':status,
            'description':description,
            'is_private': is_private,
            'is_automated':is_automated,
            'can_edit': can_edit,
            'star_count':star_count,
            'pull_count':pull_count,
            'last_updated':last_updated,
            'is_migrated': is_migrated,
            'callaborator_count':collaborator_count,
            'affiliation':affiliation,
            'hub_user':hub_user,
            'has_starred':has_starred,
            'full_description':full_description,
            'read_permissions': read_permissions,
            'write_permissions': write_permissions,
            'admin_permissions': admin_permissions
        }
        lists.append(data)
        list_not_working.append(link)
        print(link)
    
df = pd.DataFrame(lists)
df1 = pd.read_excel('datafromapi.xlsx')

df1.user = df.user
df1.name = df.name
df1.namespace = df.namespace
df1.repository_type = df.repository_type
df1.status = df.status

df1.description = df.description
df1.is_private = df.is_private
df1.is_automated = df.is_automated
df1.can_edit = df.can_edit
df1.star_count = df.star_count

df1.pull_count = df.pull_count
df1.last_updated = df.last_updated
df1.is_migrated = df.is_migrated
df1.callaborator_count = df.callaborator_count
df1.affiliation = df.affiliation

df1.hub_user = df.hub_user
df1.has_starred = df.has_starred
df1.full_description = df.full_description
df1.read_permissions = df.read_permissions
df1.write_permissions = df.write_permissions
df1.admin_permissions = df.admin_permissions
    
df1.to_excel('datafromapi_output.xlsx',encoding = 'utf-8-sig',index = False)

 

embed = DiscordEmbed(title='datafromapi_output', description=f'''Scraping Done!''')
with open(f'datafromapi_output.xlsx', "rb") as f:
    webhook.add_file(file=f.read(), filename=f'datafromapi_output.xlsx')
webhook.add_embed(embed)
response = webhook.execute()
webhook.remove_embeds()
webhook.remove_files()
    

    