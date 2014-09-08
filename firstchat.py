from flask import Flask, render_template, url_for, request
import datetime
import random

chatapp = Flask(__name__)
lastuser = ''
chats = []
usernames = []

firsts = ['When', 'Wen', 'Ev', 'Dun', 'Flum', 'Flun', 'Floun', 'Durn']
seconds = ['del', 'ding', 'ber', 'den', 'ber', 'sing']
thirds = ['ton', 'don', 'buns', 'bin', 'ren', 'ren']

def makename():
	return '%s%s%s %s%s%s'%(random.choice(firsts), random.choice(seconds), random.choice(thirds), \
		random.choice(firsts), random.choice(seconds), random.choice(thirds))

def makenewchat(username, text):
	newchatstring = ''
	if len(chats) == 0 or chats[-1][0] != username:
		newchatstring += "</div></div><div class='monologue'><div class='username'>%s:</div><div class='usertext'>"%(username)
	newchatstring += "<p>%s</p>"%(text)
	chats.append((username, newchatstring))

@chatapp.route('/roundtable')
def roundtable():
	return render_template('firstchat.html', usernames_length=len(usernames))

@chatapp.route('/getnew',methods=['POST'])
def givestuff():
	usernum = int(request.form['user'])
	if usernum >= len(usernames):
		usernames.append((makename(), 0))
	startpoint = usernames[usernum][1]
	num_chats = (len(chats) - startpoint) if (startpoint + 100) >= len(chats) else 100
	usernames[usernum] = (usernames[usernum][0], startpoint + num_chats)
	print num_chats
	return ''.join([c[1] for c in chats[startpoint:startpoint+num_chats]])

@chatapp.route('/newchat',methods=['POST'])
def getstuff():
	usernum = int(request.form['user'])
	if usernum >= len(usernames):
		usernames.append((makename(), 0))
	makenewchat(usernames[usernum][0], request.form['input'])
	return str(datetime)

if __name__ == '__main__':
	chatapp.run(debug=True);

