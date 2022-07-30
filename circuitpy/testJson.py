
import json

with open('tides.json', 'r') as f:
  data = json.load(f)
  print (data)
