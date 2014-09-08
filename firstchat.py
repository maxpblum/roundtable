from flask import Flask, render_template, url_for, request, json
import datetime
import random

chatapp = Flask(__name__)
lastuser = ''
chats = ''
usernames = []

firsts = ['When', 'Wen', 'Ev', 'Dun', 'Flum', 'Flun', 'Floun', 'Durn']
seconds = ['del', 'ding', 'ber', 'den', 'ber', 'sing']
thirds = ['ton', 'don', 'buns', 'bin', 'ren', 'ren']

def makename():
	return '%s%s%s %s%s%s'%(random.choice(firsts), random.choice(seconds), random.choice(thirds), \
		random.choice(firsts), random.choice(seconds), random.choice(thirds))

@chatapp.route('/roundtable')
def roundtable():
	return render_template('firstchat.html', usernames_length=len(usernames))

@chatapp.route('/getnew',methods=['POST'])
def givestuff():
	global chats
	usernum = int(request.form['user'])
	if usernum >= len(usernames):
		usernames.append((makename(), 0))
	toreturn = chats[usernames[usernum][1]:]
	usernames[usernum] = (usernames[usernum][0], len(chats))
	return toreturn

@chatapp.route('/newchat',methods=['POST'])
def getstuff():
	global chats
	usernum = int(request.form['user'])
	if usernum >= len(usernames):
		usernames.append((makename(), 0))
	chats += '%s\t%s\n'%(usernames[usernum][0], request.form['input'])
	return str(datetime)

if __name__ == '__main__':
	chatapp.run(debug=True);

