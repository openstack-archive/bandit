Avoid spawning subprocess with partial paths
=====================
When launching a subprocess from within Python, care should be taken over
executable paths. The search path, normally the 'PATH' environment variable will
be used to discover a executable binary if a fully qualified path is not given.
This can allow an attacker to place a similarly named executable into an early
point in the search path, such that is will be executed in preference to the
expected executable.

Paths should be given either fully qualified from the filesystem root, or
relative to the running processes working directory. If it is desirable to use unqualified executable names for the perposes of location independent
deployments then consider using relative paths to the deployment directory or
deducing the paths using mechanisms such as `os.cwd()`

### Correct
fully qualified paths, or relative paths:
```python

os.Popen('/bin/ls -l', shell=False)
os.Popen(['/bin/ls', '-l'], shell=False)
os.Popen(['../ls', '-l'], shell=False)

```

### Incorrect
Unqaulified executable names:
```python

os.Popen('ls -l', shell=False)
os.Popen(['ls', '-l'], shell=False)

```

## Consequences
The following consequences may arise from the use of unqualified paths

* Unintended execution of malicious binaries

## References
