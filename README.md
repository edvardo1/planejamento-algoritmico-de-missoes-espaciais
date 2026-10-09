Integrantes do grupo: Eduardo Beloni Mailan
Linguagem escolhida: Python
Estrutura de dados escolhida: Trie
estratégia gulosa: Huffman

# Documentação da API (Fonte de dados)
nome da API: The Solar System OpenData
endereço: https://api.le-systeme-solaire.net/en/
recursos/endpoints utilizados: https://api.le-systeme-solaire.net/rest/bodies/

Foi escolhida a API "The Solar System OpenData", porque apresenta os corpos do sistema solar.
recursos/endpoints utilizados: https://api.le-systeme-solaire.net/rest/bodies/

exemplos de requisições:
+ Aquisição feita inicialmente: "https://api.le-systeme-solaire.net/rest/bodies/?data=name,rel,bodyType"
+ Exemplo de aquisição feita dinâmicamente (para Saturno): https://api.le-systeme-solaire.net/rest/bodies/saturne

Estrutura de dados obtidos:
Para a aquisição feita inicialmente, a estrutura de dados obtida é uma array JSON, com objetos JSON contendo o nome, a url, e o bodyType de todos os corpos.
Para a aquisição dinâmica que é feita quando é requisitado a descrição detalhada do corpo, é um objeto JSON com todos os fields do corpo.

# Modelagem
Os elementos são representados como uma varíavel global "corpos" que contêm o nome, a url para mais informações, e o tipo de corpo.

Os atributos utilizados são os seguintes: "name", "rel", e "bodyType".

As operações implementadas são:
+ Listagem de corpos;
+ Pesquisa por nome exato;
+ Pesquisa por prefixo;
+ Ver detalhes de um corpo;
+ Filtrar por tipo (lista os nomes de todos os corpos de um certo tipo)
+ Comprimir dados com Huffman

As decisões do projeto, sem contar as decisões feitas para escolher a api, o algoritmo guloso, e a estrutura de dados escolhida, foram: optar por não guardar muitos dados dentro da estrutura de dados exceto os necessários para a aquisição de outros dados e filtragem, os dados completos são requisitados apenas quando necessários, como, por exemplo, se o usuário quiser visualizar os detalhes de um corpo, ou comprimir esses dados com Huffmann.

# Estrutura de dados escolhida
A estrutura escolhida foi a Trie, implementada em Python. Que armazena os nomes dos corpos celestes caractere por caractere, utilizando nós que possuem uma lista de filhos e um campo para guardar o conteúdo associado ao nome completo.
Essa estrutura foi escolhida porque pode facilmente implementar pesquisa por prefixo, o que é muito útil caso o usuário queira pesquisar por um nome, mas não queira digitar o nome completo/não saiba o nome completo.
As operações implementadas foram inserção e busca.

## Analise amortizada pelo método da contabilidade
Na Trie, o custo de inserir um nome depende de seu comprimento e da quantidade de nós novos que precisam ser criados. Definimos a função de potencial Φ(i) como a quantidade de nós existentes na árvore após a inserção (i). A variação do potencial é dada por:

ΔΦ(i) = Φ(i)-Φ(i-1)

Como cada nó novo aumenta o potencial, essa variação depende da quantidade de nós criados durante a inserção. Quando o prefixo do nome já existe na Trie, menos nós precisam ser criados e, por isso, o aumento do potencial é menor.

O custo amortizado é calculado por:

ĉ(i)=c(i)+ΔΦ(i)

em que c(i) é o custo real da inserção. O compartilhamento de prefixos reduz a criação de nós, por mais que seja necessário percorrer os caracteres do nome para fazer a inserção. Por isso, para um nome de comprimento L, o custo da operação continua sendo O(L).

# Algoritmo guloso escolhido
O algoritmo guloso escolhido foi Huffman, utilizado para fazer a compressão dos dados de um corpo celeste.
O sistema obtém os detalhes de um corpo por uma requisição dinâmica na API (como explicado previamente no documento) e transforma o objeto JSON em uma string. Em seguida, calcula a frequência de cada caractere presente no texto e constrói a árvore de Huffman, combinando sucessivamente os dois nós de menor frequência, e então, é gerado um código binário para cada caractere. Esses códigos são utilizados para produzir a string comprimida.
O sistema imprime a tabela de frequências, a árvore gerada, o dicionário de códigos e a taxa de compressão. 
A escolha do algoritmo foi feita assim porque permite demonstrar uma estratégia gulosa aplicada à redução do tamanho dos dados transmitidos durante uma missão espacial.

# Instruções de uso
Antes de executar o sistema, precisa ser informada a chave da API na environment variable $SOLAIRETOKEN, após isso, executar python sistema.py
