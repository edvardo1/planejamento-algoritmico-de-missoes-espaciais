import json
import os
from urllib.request import Request, urlopen

arq_cache = "corpos.json"

def carregar_dados_api():
    if os.path.exists(arq_cache):
        with open(arq_cache, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    url = "https://api.le-systeme-solaire.net/rest/bodies/?data=name,rel,bodyType"

    requisicao = Request(
        url,
        headers={
            "Authorization": "Bearer " + os.environ["SOLAIRETOKEN"]
        }
    )

    with urlopen(requisicao) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))

    corpos = dados["bodies"]

    with open(arq_cache, "w", encoding="utf-8") as arquivo:
        json.dump(corpos, arquivo, ensure_ascii=False, indent=2)

    return corpos


def carregar_dados_corpo(rel):
    requisicao = Request(
        rel,
        headers={
            "Authorization": "Bearer " + os.environ["SOLAIRETOKEN"]
        }
    )

    with urlopen(requisicao) as resposta:
        return json.loads(resposta.read().decode("utf-8"))
