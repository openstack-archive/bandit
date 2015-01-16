''' Example dangerous usage of urllib[2] opener functions

The urllib and urllib2 opener functions and object can open http, ftp,
and file urls. Often, the abilit to open file urls is overlooked leading
to code that can unexpectedly open files on the local server. This
could be used by an attacker to leak information about the server.
'''


import urllib
import urllib2

def test_urlopen():
    urllib.urlopen('file:///bin/ls', 'blah', 32)
    urllib.urlretrieve('file:///bin/ls', '/bin/ls2')
    opener = urllib.URLopener()
    opener.open('file:///bin/ls')
    opener.retrieve('file:///bin/ls')
    opener = urllib.FancyURLopener()
    opener.open('file:///bin/ls')
    opener.retrieve('file:///bin/ls')
    urllib2.urlopen('file:///bin/ls')
    urllib2.Request('file:///bin/ls')
