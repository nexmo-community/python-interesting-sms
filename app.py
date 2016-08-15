# -*- coding: UTF-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import nexmo
from unidecode import unidecode
import urllib
import emoji

nexmo_apikey = 'xxx'
nexmo_secret = 'xxx'

longtext = "Bacon ipsum dolor amet tail bresaola pork loin kielbasa sirloin pancetta. Pork chop bacon beef ribs, picanha t-bone ground round kevin drumstick prosciutto corned beef. Prosciutto tongue capicola, t-bone biltong turducken tail pastrami ham doner. Bacon beef ribs ham hock chuck kielbasa tongue boudin tenderloin shoulder pastrami short loin leberkas kevin drumstick. Meatloaf pig pork loin tri-tip ball tip. Turducken venison leberkas kielbasa boudin ball tip, sausage tenderloin beef ribs short loin frankfurter. Corned beef pork picanha bresaola sausage."


class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.content_type = 'text/plan'
		self.write("SMS Demo App")
		self.finish()
		
class SMSHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		msgtype=self.get_argument("type", None)
		msisdn=self.get_argument("msisdn", None)
		text = self.get_argument("text", None)
		keyword = self.get_argument("keyword", None)
		to=self.get_argument("to", None)
		if to == None:
			self.content_type = 'text/plain'
			self.write('ok')
			self.finish()
		else:
			client = nexmo.Client(key=nexmo_apikey, secret=nexmo_secret)
			if keyword.lower() == 'hello':
				client.send_message({'from':  to, 'to': msisdn, 'text': 'Hello World'})
			elif keyword.lower() == 'emoji':
				client.send_message({'from':  to, 'to': msisdn, 'text': 'Have a Free Puppy 🐶', 'type' :'unicode'})
			elif msgtype == 'unicode':
				client.send_message({'from':  to, 'to': msisdn, 'text': 'Are you getting your 5 a day 🍌🌽🍊🍏🍒', 'type' :'unicode'})
			elif keyword.lower() == 'long':
				client.send_message({'from':  to, 'to': msisdn, 'text': longtext})
			elif keyword.lower() == 'flash':
				client.send_message({'from':  to, 'to': msisdn, 'text': 'ah ha. he\'ll save everyone of us', 'message-class' : '0'})
			elif keyword.lower() == 'voicemail':
				client.send_message({'from':  to, 'to': msisdn, 'type': 'binary', 'udh': '0401028099', 'body' : ''})
			elif keyword.lower() == 'clear':
				client.send_message({'from':  to, 'to': msisdn, 'type': 'binary', 'udh': '0401020000', 'body' : ''})
			elif keyword.lower() == 'show':
				client.send_message({'from':  to, 'to': msisdn, 'type': 'binary',  'udh': '050003CC0101', 'body' : '57494E', 'protocol-id' : '65'})
			elif keyword.lower() == 'replace':
				client.send_message({'from':  to, 'to': msisdn, 'type': 'binary', 'udh': '050003CC0101', 'body' : '4C4F5345',  'protocol-id' : '65'})
			self.write('ok')
			self.finish()


def main():
	static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	print static_path
	application = tornado.web.Application([(r"/", MainHandler),
											(r"/sms", SMSHandler),
											(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
											])
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 5000))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	
	

