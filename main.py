# Enconding
# https://docs.python.org/3/library/codecs.html

# Biblioteca para conseguir usar o prompt no python
import subprocess
from datetime import datetime

# Definindo nome do arquivo
nome_arquivo = "MinhasRedes.txt"

# Comandos a serem digitados no prompt de comando (CMD)
comando_redes = ["netsh", "wlan", "show", "profiles"]
comando_sistema = ["systeminfo"]
comando_armazenamento = ["wmic", "logicaldisk", "get", "Caption,", "Size"]
comando_processador = ["wmic", "cpu", "get", "Name"]
comando_memoria = ["wmic", "memorychip", "get", "Capacity,", "Speed"]

# Variáveis de lista
lista_redes = []
lista_senhas = []
lista_armazenamento = []
lista_memorias = []

# Início do programa, obtendo resultados dos acessos ao prompt de comando (CMD)
info_redes = subprocess.check_output(comando_redes, encoding='cp858')
info_sistema = subprocess.check_output(comando_sistema, encoding='cp858')
info_armazenamento = subprocess.check_output(comando_armazenamento, encoding='cp858')
info_processador = subprocess.check_output(comando_processador, encoding='cp858')
info_memoria = subprocess.check_output(comando_memoria, encoding='cp858')

# Obter o nome do proprietário registrado
for linhas in info_sistema.split('\n'):
    if "Proprietário registrado:" in linhas:
        posi = linhas.find(":")
        proprietario = linhas[posi+1:].strip()

# Obter as informações de armazenamento
for linhas in info_armazenamento.split('\n'):
    if ":" in linhas:
        posi = linhas.find(":")
        valor = linhas[posi+1:].strip()
        nome = linhas[:posi+1].strip()
        nome_valor = f"{nome} {valor}"
        lista_armazenamento.append(nome_valor)

# Obter o nome do processador
cont_linhas = 0
for linhas in info_processador.split('\n'):
    cont_linhas += 1
    if cont_linhas == 3:
        processador = linhas.strip()

# Obter as informações da memoria
count_memorias = 0
lista_numerica = ['0','1','2','3', '4', '5', '6', '7', '8', '9']
for linhas in info_memoria.split('\n'):
    for numero in lista_numerica:
        if linhas.startswith(numero):
            count_memorias += 1
            valores = linhas.strip().split()
            valores_definidos = f"Memoria {count_memorias} tamanho: {valores[0]} velocidade {valores[1]}"
            lista_memorias.append(valores_definidos)

# Obter os nomes das redes
for linhas in info_redes.split('\n'):
    if "Usuários:" in linhas:
        posi = linhas.find(":")
        logins = linhas[posi+1:].strip()
        lista_redes.append(logins)

# Pegar a senha de cada uma das redes encontradas
for nome in lista_redes:
    info_senha = subprocess.check_output(["netsh", "wlan", "show", "profile", nome, "key", "=", "clear"], encoding='cp858')
    for linhas in info_senha.split('\n'):
        if "Conteúdo da Chave" in linhas:
            posi = linhas.find(":")
            senhas = linhas[posi+1:].strip()
            lista_senhas.append(senhas)

# Salve as informações no arquivo especificado
with open(nome_arquivo, 'a') as arquivo:
    
    arquivo.write(f"Informacoes retiradas: {datetime.today().strftime('%d-%m-%Y %H:%M:%S')}\n")
    arquivo.write(f"Usuario: {proprietario}\n")
    arquivo.write(f"Modelo do processador: {processador}\n")
    cont = len(lista_armazenamento)
    arquivo.write(f"Unidades de armazenamento: {cont}\n")
    for i in range(cont):
        arquivo.write(f"{lista_armazenamento[i]}\n")
    
    cont = len(lista_memorias)
    arquivo.write(f"Unidades de memoria: {cont}\n")
    for i in range(cont):
        arquivo.write(f"{lista_memorias[i]}\n")

    cont = len(lista_redes)
    arquivo.write(f"Redes encontradas: {cont}\n")
    for i in range(cont):
        arquivo.write(f"Rede: {lista_redes[i]} Senha: {lista_senhas[i]}\n")

    arquivo.close()
