import pprint
import zulip
import sys
from crypto import Crypto
from pnr import Pnr
from mustread import Mustread
from screenshot import Ss
from poll import Poll

p = pprint.PrettyPrinter()
BOT_MAIL = "chunkzz-bot@chunkzz.zulipchat.com"

class ZulipBot(object):
	def __init__(self):
		self.client = zulip.Client(site="https://chunkzz.zulipchat.com/api/")
		self.subscribe_all()
		self.pnr = Pnr()
		self.mustread = Mustread()
		self.ss = Ss()
		self.poll = Poll()

	def subscribe_all(self):
		json = self.client.get_streams()["streams"]
		streams = [{"name": stream["name"]} for stream in json]
		self.client.add_subscriptions(streams)

	def process(self, msg):
		content = msg["content"].split()
		sender_email = msg["sender_email"]
		ttype = msg["type"]

		print(content)

		if sender_email == BOT_MAIL:
			return 


		if content[0] == "omega" or content[0] == "@**omega**":
			if content[1] == "pnr":
				message = self.pnr.get_pnr(content[2])
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})
			elif content[1] == "read":
				email = self.mustread.get_email(self.client.get_members(),msg["content"])
				senderusername = self.mustread.get_username(self.client.get_members(),msg["sender_email"])
				print(email)
				self.client.send_message({
				"type": "private",
				"to": email,
				"content": "**"+senderusername+"** mentioned you in must read ! \nThe message says : "+" ".join(content[2:])
			})
			elif content[1] == "screenshot":
				result = self.ss.get_ss(content[2])
				print(result)
				self.client.send_message({
				"type": "stream",
				"subject": msg["subject"],
				"to": msg["display_recipient"],
				"content": "Screenshot taken :wink:\n[Screenshot Link]("+result+")"
				})
			elif content[1] == "poll":
				if content[2] == "create":
					print(",".join(content[4:]))
					idno = self.poll.create_poll(content[3],content[4:])
					self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Poll Successfully Created and id is :"+str(idno)
					})
				elif content[2] == "show":
					polldetails = self.poll.show_poll(content[3])
					self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Poll ID:"+polldetails["id"]+"\n Question :"+polldetails["pollname"]+"\nOption :"+polldetails["options"]+"\n Votes :"+polldetails["votes"]
					})
				elif content[2] == "vote":
					vote = self.poll.vote_poll(content[3],content[4])
					self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Your Vote Has Been Recorded!"
					})

		else:
			return

def main():
	bot = ZulipBot()
	bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Thanks for using Omega Bot. Bye!")
		sys.exit(0)