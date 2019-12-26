import json
import subprocess
import sys
import requests

username = sys.argv[1]


existing_users = subprocess.run(['bash', './namechk.sh', username, '-fu'], stdout=subprocess.PIPE).stdout.decode('utf-8')
existing_users = existing_users.replace('[0m', '').replace('[1;36m', '').replace('[1;32m', '').replace('[1m', '').replace('\x1b', '')
existing_users = existing_users.split('-------------------------------------------------------------')
existing_users.pop(0)
existing_users_data = []
for user in existing_users:
    data = user.splitlines()
    website = ''
    profile_url = ''
    for line in data:
        if '[+] Username found on: ' in line:
            website = line.split(':', 1)[1].strip()
        elif '[+] Profile url:' in line:
            profile_url = line.split(':', 1)[1].strip()
            break
    if profile_url != '':
        if requests.get(profile_url).status_code == 404:
            profile_url = 'not found'
    else:
        profile_url = 'not found'
    existing_users_data.append({
        'website': website,
        'profile_url': profile_url,
    })

with open('existing_users.json', 'w') as f:
    json.dump(existing_users_data, f)


available_usernames = subprocess.run(['bash', './namechk.sh', username, '-au'], stdout=subprocess.PIPE).stdout.decode('utf-8')
available_usernames = available_usernames.replace('[0m', '').replace('[1;36m', '').replace('[1;32m', '').replace('[1m', '').replace('\x1b', '')

available_usernames = available_usernames.splitlines()

websites = []
for line in available_usernames:
    if '[+] Username available on:' in line:
        website = line.split(':', 1)[1].strip()
        if website != '':
            websites.append({
                'website': website
            })
with open('available_usernames.json', 'w') as f:
    json.dump(websites, f)