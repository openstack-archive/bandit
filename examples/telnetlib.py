import telnetlib
import getpass

import six

host = sys.argv[1]

username = six.moves.input('Username:')
password = getpass.getpass()
tn = telnetlib.Telnet(host)

tn.read_until("login: ")
tn.write(username + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("ls\n")
tn.write("exit\n")

print(tn.read_all())
