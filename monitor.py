import requests
import os
import pprint
import json
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage
from datetime import date


today = date.today()

address = os.environ.get('Mail_Address')

mail_password = os.environ.get('Mail_Login')

api_pass = os.environ.get('EMAIL ADDRESS')
api_host = os.environ.get('Email Login')

# The os module is optional for users, who wish to hide their email Login.


url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/ga/topgainers"

querystring = {"start":"0"}

headers = {'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com",

'x-rapidapi-key': "9efd0f3e52mshd859f5daf34a429p11cb2ajsn2b0e421d681e"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()


def new_stock(data):
	new_market = []

	for item in data ['quotes']:
		new_name = item.get ('longName')
		new_price = item.get ('regularMarketPrice')
		res_price = (f'{new_price} Dollars')
		change = item.get('regularMarketChange')
		change2 = (f'+{change}')
		Percentchange = item.get('regularMarketChangePercent')
		percent = (f'+{Percentchange}%')
		cap =item.get('marketCap')
		if cap >= 1000000000:
			cap = f'{cap} billion dollars'
		else:
			cap = f'{cap} million dollars'
		new_market.append((new_name, res_price, change2, percent, cap))

	return new_market

value = new_stock(data)


df = pd.DataFrame(value, columns =['Company Name', 'Share Price','Change', 'Percentage change','Market Capitalization'])
df.to_csv('stockPrices.csv', index = False)



Time = today.strftime("%B %d, %Y")



contacts = [# The contacts you are trying the mail to ]




email = EmailMessage()
email['from'] ='Stock update today'
email['to']= ','.join(contacts)
email['subject'] = f'Stock Market Highest Earners Update for {Time}'

email. set_content(f''' Dear Valued User Kindly find Stock Market Update for {Time} winks \n\n\n\n 
	
The trick is not to learn to trust your gut feelings, but rather to discipline yourself to ignore them. Stand by your stocks as long as the fundamental story of the company hasn’t changed


 ''')




Files = ['stockPrices.csv']

for file in Files:
	with open('stockPrices.csv', 'rb') as f:
		file_data = f.read( )
		file_name = f.name

	email.add_attachment(file_data, maintype = 'application',  subtype = 'octet-stream', filename = file_name)




with smtplib.SMTP(host = 'smtp.gmail.com', port=587) as smtp:
	smtp.ehlo()
	smtp.starttls()
	smtp.login(address, mail_password)
	smtp.send_message(email)
	print('Stock market update sent successfully to your mail')