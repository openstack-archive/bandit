import twisted

if __name__ == "__main__":
    resource = twisted.web.twcgi.CGIScript("/var/www/cgi-bin/somescript.sh")
