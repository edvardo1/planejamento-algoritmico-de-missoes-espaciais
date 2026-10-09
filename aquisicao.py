import json
import os
from urllib.request import Request, urlopen

def carregar_dados_api():
    url = "https://api.le-systeme-solaire.net/rest/bodies/?data=name,rel,bodyType,aroundPlanet"
    requisicao = Request(
        url,
        headers={
            "Authorization": "Bearer " + os.environ["SOLAIRETOKEN"]
        }
    )
    with urlopen(requisicao) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))
    return dados["bodies"]

def carregar_dados_corpo(rel):
    url = rel
    requisicao = Request(
        url,
        headers={
            "Authorization": "Bearer " + os.environ["SOLAIRETOKEN"]
        }
    )
    with urlopen(requisicao) as resposta:
        return json.loads(resposta.read().decode("utf-8"))
