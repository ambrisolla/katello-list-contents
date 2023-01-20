# Simulação

```python
k = KatelloRepos(env='nprod')
```

### escolhendo uma opcao do dropdown: "activation key"
```python
ak_id = k.get_activation_keys()[0]['id']
```

### obtendo as informacoees do produto passando o id da activation_key
```python
data = k.get_repositories_of_an_activation_key(activation_key=ak_id)
print(json.dumps(data))
```