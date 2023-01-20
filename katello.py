import os
import yaml
import json
import requests
from   requests.auth import HTTPBasicAuth

class KatelloRepos:
  
  def __init__(self, **kwargs):
    self.fullpath = os.path.abspath(os.path.dirname(__file__))
    self.settings = self.load_settings(kwargs['env'])

  def load_settings(self, env):
    try:
      yaml_data = open(f'{self.fullpath}/settings.yaml', 'r').read()
      data = yaml.safe_load(yaml_data)
      return data[env]
    except Exception as err:
      return {
        'messsage' : str(err)
      }, 500

  def get_data_from_api(self, route, params):
    try:
      if not self.settings['use_ssl']:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      req_auth = HTTPBasicAuth(self.settings['username'], self.settings['password'])
      req = requests.get(
        '{}{}'.format(self.settings['api_url'], route), 
        params=params,
        auth=req_auth,
        verify=self.settings['use_ssl'])
      if req.status_code != 200:
        return {
          'message' : f'Failed to get activation keys: {req.reason}'
        }, req.status_code
      else:
        return json.loads(req.text)
    except Exception as err:
      return {
        'messsage' : str(err)
      }, 500

  def get_activation_keys(self):
    try:
      data = self.get_data_from_api(
        route='/katello/api/activation_keys', 
        params={'organization_id': self.settings['organization_id']})
      activation_keys = []
      for ak in data['results']:
        activation_keys.append({
          'id'   : ak['id'],
          'name' : ak['name']})
      return activation_keys
    except Exception as err:
      return {
        'messsage' : str(err)
      }, 500

  def get_repositories_of_an_activation_key(self, activation_key):
    try:
      data = self.get_data_from_api(
          route=f'/katello/api/activation_keys/{activation_key}/product_content', 
          params={
            'organization_id': self.settings['organization_id'],
            'per_page' : 200 })
      repositories = []
      for product_content in data['results']:
        repositories.append(product_content['content']['label'])
      return sorted(repositories)
    except Exception as err:
      return {
        'messsage' : str(err)
      }, 500

''' simulacao '''
k = KatelloRepos(env='nprod')

# escolhendo uma opcao do dropdown acti
ak_id = k.get_activation_keys()[0]['id']

# obtendo as informacoees do produto passando o id da actiovation_key
data = k.get_repositories_of_an_activation_key(activation_key=ak_id)
print(json.dumps(data))