# Simulação

Obs: Alterar configurações de acesso a API do Foreman/Katello no arquivo : <a href='settings.yaml'>settings.yaml</b><b>

```python
k = KatelloRepos(env='nprod')

# escolhendo uma opcao do dropdown: "activation key"
ak_id = k.get_activation_keys()[0]['id']

# obtendo as informacoees do produto passando o id da activation_key
data = k.get_repositories_of_an_activation_key(activation_key=ak_id)

print(json.dumps(data))
```
### output
```json
[
  "CentOS_7_base",
  "CentOS_7_el7-zabbix-6",
  "CentOS_7_extras",
  "CentOS_7_plus",
  "CentOS_7_remi-php74",
  "CentOS_7_sclo",
  "CentOS_7_updates"
]
```