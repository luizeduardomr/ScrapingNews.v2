import os  # importa o sistema
import json
import csv  # importa o CSV para gerar arquivos
import src.verify  # Baixa os arquivos para o selenium
import re
import traceback
import json
from src.interface import Iniciar

nomearquivo, palavrachave, opcao, datainicial, datafinal, quantidade = Iniciar()

# Atribui as datas para as variáveis
DIAi = datainicial.split("/")[0]
MESi = datainicial.split("/")[1]
ANOi = datainicial.split("/")[2]

DIAf = datafinal.split("/")[0]
MESf = datafinal.split("/")[1]
ANOf = datafinal.split("/")[2]

qntdresult = 0

# Começa as pesquisas
results = []

if opcao == 'folha':
    import src.folhasp as site_atual
elif opcao == 'estadao':
    import src.estadao2 as site_atual
elif opcao == 'uol':
    import src.uol as site_atual
else:
    raise ValueError('Site Invalido')

# Realiza a pesquisa
if(opcao == 'uol' or opcao == 'estadao'):   
    pesquisa, valor = site_atual.search(
        query=palavrachave, DIAi=DIAi, MESi=MESi, ANOi=ANOi, DIAf=DIAf, MESf=MESf, ANOf=ANOf)

elif(opcao == 'folha'):
    pesquisa, valor = site_atual.search(query=palavrachave)

site_atual.END()

for search_result in pesquisa:
    results.append(search_result)

# Faz a criação da pasta resultados
dir_path = os.path.join('./resultados2', nomearquivo)
if not os.path.exists('./resultados2'):
    os.makedirs('./resultados2')

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Faz o preenchimento de arquivos (todos)
    #Preenche um CSV com os resultados obtidos (Título, Data, descrição e link)
with open('{}.csv'.format(os.path.join(dir_path, "_Resultados_da_coleta")), 'w',  encoding='utf-8') as csv_file:
    for res in results:
        csv_file.write((res['title'] + '||\t' + res['date'] + '||\t' + res['imagem'] + '||\t' + res['link']).replace('\n', ' '))
        csv_file.write('\n')
        qntdresult+=1
        arquivotxt = re.sub('\W', '_', res['title'])
        with open('{}.txt'.format(os.path.join(dir_path, arquivotxt[:40])), 'w', encoding='utf-8') as text:
            try:
                content = res['content']
            except KeyError:
                content = "Algo deu errado"
            re.sub('\n+', '\n', content)
            # for i in range(len(content)//100):
            #     pos = 100*(i+1)+i
            #     content = content[:pos]+'\n'+content[pos:]
            text.write(content)
with open('{}.txt'.format(os.path.join(dir_path, "_Parâmetros_da_coleta")), 'w', encoding='utf-8') as text:
    if(opcao =='uol' or opcao == 'estadao'):
        text.write(f'Palavra chave: {palavrachave}\nNome da pasta: {nomearquivo}\nSite: {opcao}\nData inicial: {datainicial}\nData final: {datafinal}\nNotícias encontradas (no site): {valor}\nResultados obtidos: {qntdresult}')
    elif (opcao == 'folha'):
        text.write(
            f"Palavra Chave: {palavrachave}\nNome da pasta: {nomearquivo}\nSite: {opcao}\nPeríodo: Último ano\nNotícias encontradas: {valor}\nResultados obtidos: {qntdresult}")



# n = conteudo.index('As desvastadas')
# conteudo = conteudo[n+400:n+300]
# conteudo = conteudo[:n+100]
# pega da posição n+400 até n+100
