from icinga2api.client import Client
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


client = Client('https://172.20.20.73:5665', 'felix', 'felix22')

print(client.objects.list('Service'))

