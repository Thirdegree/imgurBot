import praw
from time import sleep
from collections import deque
import re

r = praw.Reddit("ImgurBot by /u/Thirdegree")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

Trying = True
while Trying:
	try:
		USERNAME = _login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

done = deque(maxlen=200)

def find_imgur(body):
	pattern = "imgur.com/[\w]+"
	s = re.findall(pattern, body)
	return ["http://i."+i+".jpg" for i in s]

def main():
	comments = r.get_comments('Thirdegree')
	for post in comments:
		if post.id not in done and post.author.name.lower() != USERNAME.lower():	
			done.append(post.id)
			imgurs = find_imgur(post.body)
			if imgurs:
				post.reply("\n\n".join(imgurs))
				sleep(2)

while True:
	try:	
		print "here"
		main()
		sleep(10)
	except praw.errors.RateLimitExceeded:
		print "Rate limit exceeded, sleeping 1 min"