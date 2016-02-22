import ftplib
import getpass

host = sys.argv[1]

username = raw_input('Username:')
password = getpass.getpass()

# Insecure
ftp = ftplib.FTP(host, username, password)
ftp.login()
ftps.retrlines('LIST')
ftp.quit()

# Secure
ftps = ftplib.FTP_TLS(host, username, password)
ftps.login()
ftps.prot_p()
ftps.retrlines('LIST')
ftps.quit()
