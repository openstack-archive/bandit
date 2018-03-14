from paramiko import client

client.set_missing_host_key_policy(client.AutoAddPolicy)