my_details = '''
Author: Osariemen Osaretin Frank
Hackaton: SunHack - Major League hacking(MLH)
Timeline: 9th-11th October 2020
Project-Completed: 10th October 2020
'''

from bs4 import BeautifulSoup
import requests
import csv
import datetime
import selenium
import smtplib, ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = 'https://zindi.africa/hackathons'
user_agent = {'User': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
filename = 'Zindi_Hackantons.csv'
web_data = requests.get(url, headers = user_agent).content

class WebScraper:

	def __init__(self, url = url, header = user_agent, filename = filename, web_data = web_data):
		self.url = url
		self.header = user_agent
		self.web_data = requests.get(url, headers = user_agent).content
		self.filename = filename
		self.file = open(self.filename, 'w')
		self.first_row = ['COUNTRY', 'TITLE', 'SUB-TITLE', 'LINK', 'TIMELINE', 'DURATION', 'PRIZE']
		self.csv_writer = csv.writer(self.file)
		self.csv_writer.writerow(self.first_row)

		self.soup = BeautifulSoup(self.web_data, 'lxml')



	def ScrapeDetails(self):
		self.details = self.soup.find('div', class_ = 'Competitions__container___1nb7I')
		self.hackathon_urls = self.details.find_all('a', class_ = 'Competition__container___2HXU0 Competition__box___1MoUq')
		self.titles = self.details.find_all('div', class_ = 'Competition__title___3-dFW')
		self.countries = self.details.find_all('div', class_ = 'Competition__placeAndOrganization___2xIM-')
		self.prizes = self.details.find_all('div', class_ = 'Competition__reward___1uNAt')
		self.timelines = self.details.find_all('div', class_ = 'Competition__dates___3GsCG')
		self.durations = self.details.find_all('div', class_ = 'Competition__duration___3BUIw')
		self.subs = self.details.find_all('div', class_ = 'Competition__subtitle___2h_hP')
		self.data = []

		for links, title, country, prize, timeline, duration, sub in zip(self.hackathon_urls, self.titles, 
									self.countries, self.prizes, self.timelines, self.durations, self.subs):
			country, title, sub, links = country.text, title.text, sub.text, 'https://zindi.africa{}'.format(links.get('href'))
			timeline, duration, prize = timeline.text, duration.text, prize.text

			self.data.append((country, title, sub, links, timeline, duration, prize))

		for tuple_  in self.data:
			self.csv_writer.writerow(tuple_)
		self.file.close()
		print('***WEBSCRAPING COMPLETED***')



	@staticmethod
	def SendEmail():
		port = 465
		password = input('Enter Google Mail Password: ')
		sender_mail = input('Enter Sender Google Email: ')
		receiver_mail = input('Enter Receiver Google Email: ')
		message = MIMEMultipart('alternative')
		message['From'] = 'Frank_Osaretin-Python-Project'
		message['To'] = receiver_mail
		message['Subject'] = 'Zindi Hackathon Alert'

		text_msg = '''\
		Zindi Hackaton Update
		Attached to this Electronic Mail is an Update of the Active Hackactons on Zindi
		with their respective Regions. All updates are contained in a CSV file.
		'''
		html_msg = ''' \
		<html>
			<head>
			    <link href="https://fonts.googleapis.com/css2?family=Caveat|Montserrat:wght@400;600&display=swap" rel="stylesheet">
				<style> 
					body {
						font-family: 'Montserrat', sans-serif;
						font-size: 15px;
						color: blue;
					}
					h1 {
						font-size: 25px;
		 				line-height: 1;
		 				font-family: 'Caveat', cursive;
		 				font-weight: 400;
		 				margin: 0;
					}
				</style>
			</head>
			<body>
				<h1> Zindi Hackaton Update </h1>
				<p> Attached to this Electronic Mail is an Update of the Active Hackactons on Zindi
					with their respective Regions. All updates are contained in a CSV file.
				 </p>
			</body>
		</html>
		'''
		body1 = MIMEText(text_msg, 'plain')
		body2 = MIMEText(html_msg, 'html')
		#message.attach(body1)
		message.attach(body2)

		filename = 'Zindi_Hackantons.csv'
		file = open(filename, 'rb')
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(file.read())

		encoders.encode_base64(part)

		part.add_header('Content-Disposition', 'attachment; filename= {}'.format(filename))
		message.attach(part)



		# Create a Secure SSL Context
		context = ssl.create_default_context()

		with smtplib.SMTP_SSL('smtp.gmail.com', port, context = context) as server:
			server.login(sender_mail, password)
			# TODO: send email here
			server.sendmail(sender_mail, receiver_mail, message.as_string())


WebScraper().ScrapeDetails()
WebScraper().SendEmail()

				