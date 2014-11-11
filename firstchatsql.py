from flask import Flask, render_template, url_for, request
import datetime, random, string, sqlite3
from bs4 import BeautifulSoup

chatapp = Flask(__name__)

firsts = ['When', 'Wen', 'Ev', 'Dun', 'Flum', 'Flun', 'Floun', 'Durn']
seconds = ['del', 'ding', 'ber', 'den', 'ber', 'sing']
thirds = ['ton', 'don', 'buns', 'bin', 'ren', 'ren']

befores = ['Hear ye, hear ye', 'Forsooth', 'By my troth', 'Sirrah', 'Alas']
afters = ['my liege', 'my lady', 'my lord', "i' faith", 'I pray thee']
exclamations = ['How now, how now, mad wag!', "'Zounds!", 'O rare!', 'I care not.', 'Anon, anon.', 'Good morrow!', 'What, ho!', "Blessed fig's end!", 'Marry trap with you!']

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'b', 'i']

DATETIME_TEXT_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def text_to_datetime(textdt):
    return datetime.datetime.strptime(textdt,DATETIME_TEXT_FORMAT)

def datetime_to_text(dt):
    return datetime.datetime.strftime(dt,DATETIME_TEXT_FORMAT)

OLD_DATE = datetime_to_text(datetime.datetime(2000,1,1,1,1,1,1))

def sanitize_html(value):

    soup = BeautifulSoup(value)

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True

    return soup.renderContents()

def makename():
    return '%s%s%s %s%s%s'%(random.choice(firsts), random.choice(seconds), random.choice(thirds), \
        random.choice(firsts), random.choice(seconds), random.choice(thirds))

def get_sql():
    chatdb = sqlite3.connect('data/chatdata.db',detect_types=sqlite3.PARSE_DECLTYPES)
    cur = chatdb.cursor()
    return (chatdb, cur)

def sql_select(cond, table, *cols):
    """ cond is a tuple, ordered like a lisp comparison
    e.g. ('<' 'time' datetime.datetime.now()) """
    chatdb, cur = get_sql()
    column_list = string.join(cols,sep=',')
    exec_string = 'SELECT %s FROM %s'%(column_list,table)
    if cond:
        exec_string += ' WHERE %s%s?'%(cond[1],cond[0])
        print exec_string
        exec_tuple = (cond[2],)
        cur.execute(exec_string, exec_tuple)
    else:
        cur.execute(exec_string)
    l = cur.fetchall()
    chatdb.close()
    return l

def sql_insert(table, cols, *values):
    """ (string, tuple or None, varying number of values) """
    chatdb, cur = get_sql()
    col_string = '' if not cols else '%s '%(string.join(cols,sep=','))
    questionmarks = '(%s?)'%('?,'*(len(values) - 1))
    exec_string = 'INSERT INTO %s %s VALUES %s'%(table,col_string,questionmarks)
    cur.execute(exec_string,values)
    chatdb.commit()

def sql_update(table, col, val, cond):
    chatdb, cur = get_sql()
    cur.execute('UPDATE %s SET %s = ? WHERE %s%s?'%(table,col,cond[1],cond[0]),(val,cond[2]))
    chatdb.commit()

def used_nums():
    return [user[0] for user in sql_select(None, 'users', 'num')]

def insert_new_user(num):
    sql_insert('users',None,num,makename(),OLD_DATE)

# USE AUTOINCREMET INSTEAD
def new_user_num():
    n = 1
    while n in used_nums():
        n += 1
    insert_new_user(n)
    return n

def username(num):
    if not num in used_nums():
        insert_new_user(num)
        #usernames.append((makename(), len(chats)))
    return sql_select(('=','num',num), 'users', 'username')[0][0]

def findLastNonPunct(text):
    i = len(text) - 1
    while i >= 0:
        if text[i] in (string.ascii_letters + string.digits):
            return i
        i -= 1
    return i

def knight_convert(raw_speech):
    speech = sanitize_html(raw_speech)
    if not speech:
        return random.choice(exclamations)
    s = findLastNonPunct(speech)
    if s == -1:
        return speech
    elif random.randint(0, 2) == 0:
        return '%s, %s%s'%(speech[:(s+1)], random.choice(afters), speech[s+1:])
    else:
        return random.choice(befores) + ', ' + speech

def add_chat(usernum, text):
    name = username(usernum)
    sql_insert('chats', None, name, datetime.datetime.now(), knight_convert(text))

def get_lastcheck(usernum):
    #print sql_select(('=','num',usernum),'users','lastcheck')
    #return sql_select(('=','num',usernum),'users','lastcheck')[0][0]
    #return OLD_DATE
    chatdb, cur = get_sql()
    cur.execute('SELECT lastcheck FROM users WHERE num=?',(usernum,))
    #r = text_to_datetime(cur.fetchone()[0])
    r = cur.fetchone()
    chatdb.close()
    return r[0]

def set_time(usernum,new_time):
    sql_update('users','lastcheck',new_time,('=','num',usernum))

def get_chats(usernum):
    new_time = datetime_to_text(datetime.datetime.now())
    dt = get_lastcheck(usernum)
    chatdb, cur = get_sql()
    cur.execute('SELECT user,chat FROM chats WHERE time>? AND time<=?',(dt,new_time))
    r = cur.fetchall()[-100:]
    chatdb.close()
    set_time(usernum,new_time)
    return r

@chatapp.route('/roundtable')
def roundtable():
    return render_template('firstchat.html', newusernum=new_user_num())

@chatapp.route('/getnew',methods=['POST'])
def givestuff():
    usernum = int(request.form['user'])
    username(usernum)
    chat_tuples = get_chats(usernum)
    #usernames[usernum] = (usernames[usernum][0], len(chats))
    return string.join([string.join(t,sep='\t') for t in chat_tuples],sep='\n')

@chatapp.route('/newchat',methods=['POST'])
def getstuff():
    usernum = int(request.form['user'])
    #chats += '%s\t%s\n'%(usernames[usernum][0], knight_convert(request.form['input']))
    add_chat(usernum, request.form['input'])
    return str(datetime)

if __name__ == '__main__':
    chatapp.run(host='0.0.0.0');

