roundtable
==========

A simple, knightly chatroom.

This was an early Hacker School project, my first-ever interactive web app. I never deployed it, but with some simple changes to replace SQLite with MySQL (to handle frequent requests better), it could be deployed.

All requests are made using HTTP and AJAX. This makes the chatroom rather inefficient, as each client has to check back every couple of seconds to find out whether new chat messages have been sent.

The **real magic** is in the user names, and in how user chat messages are displayed.

Runs on Flask and Python 2.x, and uses BeautifulSoup to sanitize user inputs. Currently requires SQLite3. See requirements.txt for precise versions.

To use, run firstchatsql.py, then connect to port 5000, URL /roundtable, e.g. http://localhost:5000/roundtable
