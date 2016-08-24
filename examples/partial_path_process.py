import subprocess

subprocess.Popen('gcc --version', shell=False)
subprocess.Popen('/bin/gcc --version', shell=False)
subprocess.Popen(var, shell=False)

subprocess.Popen(['ls', '-l'], shell=False)
subprocess.Popen(['/bin/ls', '-l'], shell=False)

subprocess.Popen('../ls -l', shell=False)
