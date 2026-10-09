import json
import os
from urllib.request import Request, urlopen

class TrieNode:
    def __init__(self):
        self.filhos = {}
        self.conteudo = None
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.nos_visitados = 0

    def insert(self, nome, conteudo):
        no = self.root

        for char in nome.lower():
            if char not in no.filhos:
                no.filhos[char] = TrieNode()
            no = no.filhos[char]
        no.end = True
        no.conteudo = conteudo

    def pesquisa(self, nome):
        no = self.root
        self.nos_visitados = 1
        for char in nome.lower():
            if char not in no.filhos:
                return None
            no = no.filhos[char]
            self.nos_visitados += 1
        if no.end:
            return no.conteudo
        return None
   
    def comeca_com(self, prefixo):
        no = self.root
        self.nos_visitados = 1
        for char in prefixo.lower():
            if char not in no.filhos:
                return []
            no = no.filhos[char]
            self.nos_visitados += 1
        return self.coleta(no)
   
    def coleta(self, no):
        bodies = []
        if no.end:
            bodies.append(no.conteudo)
        for child in no.filhos.values():
            self.nos_visitados += 1
            bodies.extend(self.coleta(child))
        return bodies


#def carregar_dados():
#    with open("bodies.json", "r", encoding="utf-8") as f:
#        return json.load(f)["bodies"]

class HuffmanNode:
    def __init__(self, char, freq, esq=None, dir=None):
        self.char = char
        self.freq = freq
        self.esq = esq
        self.dir = dir


def huffman(texto):
    freq = {}

    for c in texto:
        freq[c] = freq.get(c, 0) + 1

    if not freq:
        return {
            "frequencias": freq,
            "arvore": None,
            "codigos": {},
            "codificado": "",
            "bits_originais": 0,
            "bits_comprimidos": 0,
            "razao": 0
        }

    nodes = [
        HuffmanNode(c, f)
        for c, f in freq.items()
    ]

    while len(nodes) > 1:
        nodes.sort(key=lambda n: n.freq)

        a = nodes.pop(0)
        b = nodes.pop(0)

        pai = HuffmanNode(
            None,
            a.freq + b.freq,
            a,
            b
        )

        nodes.append(pai)

    raiz = nodes[0]
    codigos = {}

    def gerar_codigos(no, codigo=""):
        if no.char is not None:
            codigos[no.char] = codigo if codigo else "0"
            return

        gerar_codigos(no.esq, codigo + "0")
        gerar_codigos(no.dir, codigo + "1")

    gerar_codigos(raiz)

    codificado = "".join(codigos[c] for c in texto)

    bits_originais = len(texto.encode("utf-8")) * 8
    bits_comprimidos = len(codificado)

    razao = (
        bits_comprimidos / bits_originais
        if bits_originais > 0
        else 0
    )

    return {
        "frequencias": freq,
        "arvore": raiz,
        "codigos": codigos,
        "codificado": codificado,
        "bits_originais": bits_originais,
        "bits_comprimidos": bits_comprimidos,
        "razao": razao
    }


def mostrar_arvore(no, nivel=0):
    if no is None:
        return

    if no.char is not None:
        print("  " * nivel + repr(no.char) +
              " (" + str(no.freq) + ")")
    else:
        print("  " * nivel + "* (" + str(no.freq) + ")")

    mostrar_arvore(no.esq, nivel + 1)
    mostrar_arvore(no.dir, nivel + 1)

def mostrar_huffman(texto):
    resultado = huffman(texto)
    assert sum(resultado["frequencias"].values()) == len(texto)
    assert sum(
        resultado["frequencias"][c] * len(codigo)
        for c, codigo in resultado["codigos"].items()
    ) == resultado["bits_comprimidos"]
    print("\nfrequencias")
    for char, freq in sorted(
        resultado["frequencias"].items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(repr(char), ":", freq)
    print("\narvore de huffman")
    mostrar_arvore(resultado["arvore"])
    print("\n=== codigos ===")
    for char, codigo in sorted(
        resultado["codigos"].items()
    ):
        print(repr(char), ":", codigo)
    print("\ncompressao")
    print("bits originais:", resultado["bits_originais"])
    print("bits codificados:", resultado["bits_comprimidos"])
    if resultado["bits_originais"] > 0:
        percentual = resultado["razao"] * 100
        economia = (1 - resultado["razao"]) * 100

        print("tamanho relativo: {:.2f}%".format(percentual))
        print("reducao teorica: {:.2f}%".format(economia))

    print("\ntexto codificado:")
    print(resultado["codificado"][:200] + "..." if len(resultado["codificado"]) > 200 else resultado["codificado"])
    print("(mostrando no maximo 200 bits)")
    return resultado

def carregar_dados_api():
    url = "https://api.le-systeme-solaire.net/rest/bodies/?data=name,rel,bodyType"
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

print("carregando dados")
corpos = carregar_dados_api()

trie = Trie()

for corpo in corpos:
    trie.insert(corpo["name"], corpo)

def listar_corpos():
    for corpo in corpos:
        print(corpo["name"])


def pesquisar_corpo():
    nome = input("nome do corpo: ")
    corpo = trie.pesquisa(nome)
    if corpo:
        print("nome:", corpo["name"])
        print("url:", corpo["rel"])
    else:
        print("corpo nao encontrado.")

def detalhes_corpo():
    nome = input("Nome do corpo: ")
    resultados = trie.comeca_com(nome)

    exatos = [
        corpo for corpo in resultados
        if corpo["name"].lower() == nome.lower()
    ]

    if not exatos:
        print("Corpo nao encontrado.")
        return

    corpo = carregar_dados_corpo(exatos[0]["rel"])

    print("{")
    for atributo, valor in corpo.items():
        print("  " + atributo + ":", valor)
    print("}")

def filtrar_tipo():
    tipo = input("tipo de corpo (Planet, Moon, Asteroid...): ").strip().lower()
    encontrados = 0
    for corpo in corpos:
        if corpo.get("bodyType", "").lower() == tipo:
            print(corpo["name"])
            encontrados += 1
    print("total encontrados:", encontrados)

def comprimir_corpo():
    nome = input("Nome do corpo: ")
    corpo = trie.pesquisa(nome)
    if corpo is None:
        print("Corpo nao encontrado.")
        return
    detalhes = carregar_dados_corpo(corpo["rel"])
    texto = json.dumps(
        detalhes,
        ensure_ascii=False,
        separators=(",", ":")
    )
    mostrar_huffman(texto)

def main():
    while True:
        print("l. listar corpos")
        print("p. pesquisar por nome exato")
        print("i. pesquisar por prefixo")
        print("d. ver detalhes de um corpo")
        print("f. filtrar por tipo")
        print("h. comprimir dados com Huffman")
        print("q. sair")

        i = input("> ").lower()

        if i == "q":
            break
        elif i == "l":
            listar_corpos()
        elif i == "p":
            pesquisar_corpo()
        elif i == "i":
            prefixo = input("prefixo: ")
            resultados = trie.comeca_com(prefixo)

            if resultados:
                for corpo in resultados:
                    print(corpo["name"])
            else:
                print("nenhum corpo encontrado.")
            print("nos visitados:", trie.nos_visitados)
        elif i == "d":
            detalhes_corpo()
        elif i == "f":
            filtrar_tipo()
        elif i == "h":
            comprimir_corpo()

main()
