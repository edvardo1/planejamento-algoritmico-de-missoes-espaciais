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
        self.nos_visitados = 0
        for char in nome.lower():
            self.nos_visitados += 1
            if char not in no.filhos:
                return None
            no = no.filhos[char]
        self.nos_visitados += 1
        if no.end:
            return no.conteudo
        return None

    def comeca_com(self, prefixo):
        no = self.root
        self.nos_visitados = 0

        for char in prefixo.lower():
            self.nos_visitados += 1
            if char not in no.filhos:
                return []
            no = no.filhos[char]
        return self.coleta(no)

    def coleta(self, no):
        bodies = []
        if no.end:
            bodies.append(no.conteudo)
        for child in no.filhos.values():
            bodies.extend(self.coleta(child))
        return bodies


def carregar_dados():
    with open("bodies.json", "r", encoding="utf-8") as f:
        return json.load(f)["bodies"]

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
    nodes = [HuffmanNode(c, f) for c, f in freq.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda n: n.freq)
        a = nodes.pop(0)
        b = nodes.pop(0)
        nodes.append(HuffmanNode(None, a.freq + b.freq, a, b))
    codes = {}
    def generate(node, code=""):
        if node.char is not None:
            codes[node.char] = code
        else:
            generate(node.esq, code + "0")
            generate(node.dir, code + "1")
    generate(nodes[0])
    return codes

import json

corpos = carregar_dados()

trie = Trie()

for corpo in corpos:
    trie.insert(corpo["name"], corpo)

corpo = trie.pesquisa("La Terre")

print(corpo)
print("Nós visitados:", trie.nos_visitados)

resultados = trie.comeca_com("Mar")

for corpo in resultados:
    print(corpo["name"])

print("Nós visitados:", trie.nos_visitados)
