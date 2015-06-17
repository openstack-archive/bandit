import paramiko

# this is not
paramiko.exec_command('something; reallly; unsafe')

# this is safe
paramiko.connect('somehost')

# this should not be detected
somelib.exec_command('this; is; indeterminately; unsafe')

