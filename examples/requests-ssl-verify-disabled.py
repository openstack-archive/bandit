import requests

requests.get('https://gmail.com', verify=True)
requests.get('https://gmail.com', verify=False)
requests.post('https://gmail.com', verify=True)
requests.post('https://gmail.com', verify=False)
requests.put('https://gmail.com', verify=True)
requests.put('https://gmail.com', verify=False)
requests.delete('https://gmail.com', verify=True)
requests.delete('https://gmail.com', verify=False)
requests.patch('https://gmail.com', verify=True)
requests.patch('https://gmail.com', verify=False)
requests.options('https://gmail.com', verify=True)
requests.options('https://gmail.com', verify=False)
requests.head('https://gmail.com', verify=True)
requests.head('https://gmail.com', verify=False)

requests.get('https://gmail.com',
             verify=False, #nosec
             other_arg=abc)
