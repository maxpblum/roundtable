from flask import Flask, render_template, url_for, request, json
import datetime, random, string
from bs4 import BeautifulSoup

chatapp = Flask(__name__)
lastuser = ''
chats = ''
usernames = []



firsts = ['When', 'Wen', 'Ev', 'Dun', 'Flum', 'Flun', 'Floun', 'Durn']
seconds = ['del', 'ding', 'ber', 'den', 'ber', 'sing']
thirds = ['ton', 'don', 'buns', 'bin', 'ren', 'ren']

befores = ['Forsooth', 'By my troth', 'Sirrah']
afters = ['my liege', 'my lady', 'my lord', "i' faith", 'I pray thee']
exclamations = ['How now, how now, mad wag!', "'Zounds!", 'O rare!', 'I care not.', 'Anon, anon.', 'Good morrow!', 'What, ho!']

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'b', 'i']

def sanitize_html(value):

    soup = BeautifulSoup(value)

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True

    return soup.renderContents()

def makename():
	return '%s%s%s %s%s%s'%(random.choice(firsts), random.choice(seconds), random.choice(thirds), \
		random.choice(firsts), random.choice(seconds), random.choice(thirds))

def checkuser(num):
	global chats
	if num >= len(usernames):
		usernames.append((makename(), len(chats)))


def findLastNonPunct(text):
    i = len(text) - 1
    while i >= 0:
        if text[i] in (string.ascii_letters + string.digits):
            return i
        i -= 1
    return i

def knight_convert(raw_speech):
	speech = sanitize_html(raw_speech)
	if speech == '':
		return random.choice(exclamations)
	s = findLastNonPunct(speech)
	if s == -1:
		return speech
	elif random.randint(0, 2) == 0:
		return '%s, %s%s'%(speech[:(s+1)], random.choice(afters), speech[s+1:])
	else:
		return random.choice(befores) + ', ' + speech

@chatapp.route('/roundtable')
def roundtable():
	return render_template('firstchat.html', usernames_length=len(usernames))

@chatapp.route('/getnew',methods=['POST'])
def givestuff():
	usernum = int(request.form['user'])
	checkuser(usernum)
	toreturn = chats[usernames[usernum][1]:]
	usernames[usernum] = (usernames[usernum][0], len(chats))
	return toreturn

@chatapp.route('/newchat',methods=['POST'])
def getstuff():
	global chats
	usernum = int(request.form['user'])
	checkuser(usernum)
	chats += '%s\t%s\n'%(usernames[usernum][0], knight_convert(request.form['input']))
	return str(datetime)

if __name__ == '__main__':
	chatapp.run(host='0.0.0.0');

