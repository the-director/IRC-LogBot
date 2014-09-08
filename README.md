IRC-LogBot
==========

Framework for simple IRC logging and web searching.  A basic starting point as further security *should* be applied in production.


Bot logs Entries, exits, disconnects, and PM's to and from into a MySQL Database

Required for bot:

python-zope.interface python-twisted python-twisted-web python-mysqldb mysql-server

python ./bot.py to start

Required for search website (Web folder):

PHP and connection to MySQL