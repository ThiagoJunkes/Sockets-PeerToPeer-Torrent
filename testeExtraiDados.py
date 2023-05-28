import re
import ast

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

    return dados_conexao

# Exemplo de utilização
strings = []
strings.append("('192.168.100.131', 63128)(['a.txt', 'b.txt', 'c.txt'])")
strings.append("('192.168.100.131', 63242)(['a.txt', 'b.txt', 'c.txt'])")

todos_dados = []
for string in strings:
    dados = extrair_dados(string)
    todos_dados.extend(dados)

print(todos_dados)
