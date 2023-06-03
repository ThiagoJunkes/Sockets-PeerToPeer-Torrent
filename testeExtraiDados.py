import re
import ast

IP = "192.168.100.131"

def extrair_dados(string):
    # Extrai o IP e a porta usando uma expressão regular
    ip_porta = re.findall(r"\('([\d.]+)',\s(\d+)\)", string)
    # Extrai a lista de arquivos como uma string
    lista_arquivos = re.findall(r"\((\[.*?\])\)", string)

    # Cria uma lista de dicionários com os dados extraídos
    dados_conexao = []
    for i in range(len(ip_porta)):
        ip, porta = ip_porta[i]
        arquivos = ast.literal_eval(lista_arquivos[i])
        dados_conexao.append({
            'ip': ip,
            'porta': int(porta),
            'arquivos': arquivos
        })

    dados_conexao = [dado for dado in dados_conexao if dado['ip'] != IP]

    return dados_conexao

# Exemplo de utilização
strings = []
strings.append("('192.168.100.131', 63128)(['teste.txt', 'excluir.txt', 'mostrar.txt'])")
strings.append("('192.168.100.132', 63242)(['a.txt', 'b.txt', 'c.txt'])")
strings.append("('192.168.100.133', 63242)(['d.txt', 'e.txt', 'f.txt'])")

todos_dados = []
for string in strings:
    dados = extrair_dados(string)
    todos_dados.extend(dados)

# Imprimir apenas o IP
for dados in todos_dados:
    print(dados['ip'])

# Imprimir apenas os nomes de arquivo
for dados in todos_dados:
    for arquivo in dados['arquivos']:
        print(arquivo)
