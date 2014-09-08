#
#CREATE SCHEMA `logbot` ;
#
#CREATE TABLE `logbot`.`tbl_archive` (
#  `time` DATETIME NOT NULL,
#  `message` VARCHAR(512) NOT NULL,
#  `user` VARCHAR(45) NOT NULL,
#  `channel` VARCHAR(45) NOT NULL,
#  `pm` TINYINT(1)  NULL);


import time, sys
import webbrowser
import urllib2

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task
from twisted.enterprise import adbapi
from twisted.web import server, resource
from twisted.enterprise.adbapi import Transaction

#Do you want console output of all logged messages?
ConsoleLog = True

#Special watch message
watch = "!search"
watchMSG = "You can find my logs at: "
searchURL = "http://nowhere.local"

#IRC Setting
irchost = "127.0.0.1"
ircport = 6667
#Primary IRC channel - required - don't forget #
pChan = "#development"
#Alternate IRC channels to join - comma separated, no spaces.  Again don't forget #
#aChans = "#development2,#development3"
botName = "LogBot"
ircServerPass = ""

#MySQL Settings
host = "127.0.0.1"
port = 3306
db =  "logbot"
writeUser = "i_can_write"
writepw = "4theWorld!"

#Enable PSA message
enablePSA = True
#PSA Timer - in seconds
timerTime = 300
#PSA Messagge
psaMessage = "PSA:  I log all channel communications!"
#Log PSA Messages (likely not, but who knows)
logPSA = False


wmysql = adbapi.ConnectionPool(
    "MySQLdb",
    db = db,
    port = port,
    user = writeUser,
    passwd = writepw,
    host = host,
    )


def LogIt(self, user, msg, channel, pm):
    user = user.split('!', 1)[0]
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    if ConsoleLog == True:
        print timestamp + " " + channel + " " + user + " " + msg 
    msg = msg.replace("'", "''")
    msg = msg.replace(chr(92), chr(92)+chr(92))
    wmysql.runQuery("INSERT INTO tbl_archive(time, message, user, channel, pm) VALUES ('%s', '%s', '%s', '%s', '%s')" % (timestamp, msg, user, channel, pm))
    
class LogBot(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)
    password = ircServerPass
         
    def signedOn(self):
        self.announceLoop = task.LoopingCall(self.psaAnnounce)
        if enablePSA == True:
            self.announceLoop.start(timerTime)
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)
        msg = "Bot signed on"
        user = self.nickname
        channel = "Server"
        LogIt(self, user, msg, channel, 0)        
        channels = aChans.split(",")
        for chan in channels:
            self.join(chan)
            jchannel = "Server"
            LogIt(self, user, msg, jchannel, 0)
            
    def psaAnnounce(self):
        channels = aChans.split(",")
        chan = pChan
        self.msg(chan, psaMessage)
        for chan in channels:
            self.msg(chan, psaMessage)
            if logPSA == True:
                LogIt(self, botName, psaMessage, chan , 1)

    def joined(self, channel):
        print "Joined %s." % (channel,)
        msg = "Bot joined channel"
        user = self.nickname
        LogIt(self, user, msg, channel, 0)

    def privmsg(self, user, channel, msg):
        LogIt(self, user, msg, channel, 0)
        if channel == self.nickname:
            replymsg = "Be polite, share with the team. This message is also publicly searchable hope you didn't say something naughty"
            self.msg(user, replymsg)
            LogIt(self, botName, replymsg, channel , 1)
            return
        if (msg.startswith("@" + self.nickname)) or (msg.startswith(self.nickname+":")) or (msg.startswith(self.nickname)):
            replymsg = "I'm only a log bot, don't confuse me. " + watch
            self.msg(channel, replymsg)
            LogIt(self, botName, replymsg, channel, 0)
            return
        if msg == watch:
            replymsg = watchMSG + " "+ searchURL
            self.msg(channel, replymsg)
            return
                        
    def userJoined(self, user, channel):
        msg = "User joined channel"
        LogIt(self, user, msg, channel, 0)
        
    def userLeft(self, user, channel):
        msg = "User left channel"
        LogIt(self, user, msg, channel, 0) 


    def userQuit(self, user, channel):
        msg = "User quit and left channel"
        LogIt(self, user, msg, channel, 0)  
        
       
class LogBotFactory(protocol.ClientFactory):
    protocol = LogBot

    def __init__(self, channel, nickname=botName):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
       
if __name__ == "__main__":
    reactor.connectTCP(irchost, ircport, LogBotFactory(pChan))
    reactor.run()        