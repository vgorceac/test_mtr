import json
import subprocess
import telepot

#Telegram settings
TOKEN = ''
chat = ''
bot = telepot.Bot(TOKEN)

#MTR settings
dst = '8.8.8.8'
count = '100'
lost_thrashold = '20'
command = ['mtr', '-n', '-j', '-c', count, dst]

#Get MTR result to json
result = subprocess.run(command, capture_output=True, text=True).stdout.strip()

#Load result in json
data = json.loads(result)

#Get lost% packets from json
loss = data['report']['hubs'][-1]['Loss%']

#Condition if percent of lost pacckets is more than value in lost_trashold
if float(loss) > float(lost_thrashold):
    #Get data from json and create readable table for notification
    src = data['report']['mtr']['src']
    hubs = data['report']['hubs']
    headers = hubs[0].keys()
    table = 'MTR from: %s to %s Lost: %s%s' %(src, dst, loss, '%') + '\n'
    table += ' '.join(headers) + '\n'
    for hub in hubs:
        row = ' | '.join(str(value) for value in hub.values()) + '\n'
        table += row
    #Send notify to telegram
    bot.sendMessage(chat, table, parse_mode='HTML')