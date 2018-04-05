import requests
import json
import time
from requests.compat import urljoin
from config import CORE_API_KEY, BASE_URL

class API(object):

  def __init__(self):
    self.url = BASE_URL
    self.key = CORE_API_KEY
    self.articles_url = urljoin(BASE_URL, r'articles/search/')
    self.default_params = {'apiKey':CORE_API_KEY}
    return 

  def make_params(self, new_params):
    params = self.default_params
    params.update(new_params)
    return params

  def query_journals(self, query, **kwargs):
    params = self.make_params(kwargs)
    r = requests.get(urljoin(self.articles_url, query), 
                     params=params).json()
    if r['status'] != 'OK':
      print(r['status'])
    return r['data']

def make_json_file(filepath, query, numpages=1, pageSize=100, pageStart=60):
  a = API()

  data = []

  for i in range(pageStart,pageStart+numpages):
    print i
    r = a.query_journals(query, page=i+1, pageSize=pageSize)
    data.append(r)
    time.sleep(.1)


  with open(filepath, 'w') as f:
    json.dump(data, f)
  return

#1522841

if __name__=='__main__':
  print(make_json_file(r'data/descriptions121_180.json', 
    '(_exists_:description AND language.name:English AND _exists_:title)', 
    numpages=60, pageSize=100, pageStart=120))
