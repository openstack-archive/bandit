from subprocess import Popen as pop

pop('gcc --version', shell=False)
pop('/bin/gcc --version', shell=False)
pop(var, shell=False)

pop(['ls', '-l'], shel=True)
pop(['/bin/ls', '-l'], shel=False)
