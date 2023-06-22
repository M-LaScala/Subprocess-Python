# Enconding
# https://docs.python.org/3/library/codecs.html

# Biblioteca para conseguir usar o prompt no python
from datetime import datetime
import subprocess


# Comandos a serem digitados no prompt de comando (CMD)
# netsh wlan show profiles
listar_redes = ["netsh", "wlan", "show", "profiles"]
listar_inf_sistema = ["systeminfo"]
listar_armazenamento = ["wmic", "logicaldisk", "get", "Caption,", "Size"]
listar_processador = ["wmic", "cpu", "get", "Name"]
listar_memoria = ["wmic", "memorychip", "get", "Capacity,", "Speed"]

# Variáveis de lista
lista_redes = []
lista_senhas = []

# Início do programa, obtendo resultados dos acessos ao prompt de comando (CMD)
info_redes = subprocess.check_output(listar_redes, encoding='cp858')
info_inf_sistema = subprocess.check_output(listar_inf_sistema, encoding='cp858')
info_armazenamento = subprocess.check_output(listar_armazenamento, encoding='cp858')
info_processador = subprocess.check_output(listar_processador, encoding='cp858')
info_memoria = subprocess.check_output(listar_memoria, encoding='cp858')

# Pegar os nomes das redes que estão na info_redes
for linhas in info_redes.split('\n'):
    if "Usuários:" in linhas:
        posi = linhas.find(":")
        logins = linhas[posi+2:]
        lista_redes.append(logins)

# Pegar o nome do proprietário registrado
for linhas in info_inf_sistema.split('\n'):
    if "Proprietário registrado:" in linhas:
        posi = linhas.find(":")
        proprietario = linhas[posi+2:] # Fazer um trinn é melhor

# Pegar a senha de cada uma das redes encontradas
for nome in lista_redes:
    info_senha = subprocess.check_output(["netsh", "wlan", "show", "profile", nome, "key", "=", "clear"], encoding='cp858')
    for linhas in info_senha.split('\n'):
        if "Conteúdo da Chave" in linhas:
            posi = linhas.find(":")
            senhas = linhas[posi+2:]
            lista_senhas.append(senhas)

nome_arquivo = "MinhasRedes.txt"

# Salve as informações no arquivo especificado
with open(nome_arquivo, 'a') as arquivo:
    cont = len(lista_redes)
    arquivo.write(f"Informacoes retiradas: {datetime.today().strftime('%d-%m-%Y %H:%M:%S')}\n")
    for i in range(cont):
        arquivo.write(f"Rede: {lista_redes[i]} Senha: {lista_senhas[i]}\n")

# systeminfo
# Proprietário registrado:

# wmic logicaldisk get Caption, Size
# fazer um round no valor de armazenamento

# wmic cpu get Name
# Pega no nome do processador / modelo

# wmic memorychip get Capacity, Speed
# Pega a quantidade de pentes de memoria e a velocidade que estão trabalhando