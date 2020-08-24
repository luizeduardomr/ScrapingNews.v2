from src.browser import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# with open(os.path.join('src', 'main.js')) as infile:
# 	elimn_assin = infile.read()


def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):
    br = GLOBAL_BR
    query = query.replace(' ', '+')
    # Realiza a busca
    # https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F01%2F2015-03%2F08%2F2020&q=mudanças%20Climáticas // ou mudanças+climáticas
    # https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando={DIAi}%2F{MESi}%2F{ANOi}-{DIAf}%2F{MESf}%2F{ANOf}&q={palavra1}+{palavra2}
    #br.get('https://busca.estadao.com.br/?tipo_conteudo=Notícias&quando=&q={}'.format(query.replace(' ', '+')))
    br.get(
        f'https://busca.estadao.com.br/?tipo_conteudo=&quando={DIAi}%2F{MESi}%2F{ANOi}-{DIAf}%2F{MESf}%2F{ANOf}&q={query}')
    time.sleep(1)

    # Entrar com a conta
    try:
        CLICK('/html/body/header/div/div[2]/a[2]')
        time.sleep(3)
        GET(f'/html/body/section/div/section/div[1]/form[1]/div[4]/div/div/input').send_keys(
            'xxxxxxxxxxxxxxx')
        time.sleep(3)
        GET(f'/html/body/section/div/section/div[1]/form[1]/div[5]/div/div/input').send_keys(
            'xxxxxxxxxxxxxxxxx')
        time.sleep(4)
        CLICK('/html/body/section/div/section/div[1]/form[1]/div[7]/div/input')
    except:
        print_exc()

    time.sleep(2)
    br.get(
        f'https://busca.estadao.com.br/?tipo_conteudo=&quando={DIAi}%2F{MESi}%2F{ANOi}-{DIAf}%2F{MESf}%2F{ANOf}&q={query}')
    # br.execute_script(elimn_assin)

    # Pega a quantidade de resultados da pesquisa
    try:
        secaoqntd = TXT('/html/body/section[3]/div/section/form/section/div/p')
        valor = int(secaoqntd.split(' ')[2])
    except:
        valor = 2

    # ad blocker gambiarra ---------------------
    # try:
    # 	WAIT_ID('botaoFechar').click()
    # except:
    # 	print_exc()

    # Tenta ja expandir a primeira vez os resultados
    # O primeiro botao de "carregar mais" se comporta
    # diferente dos demais
    br.execute_script("window.scrollTo(0, 1080)")
    time.sleep(3)
    try:
        CLICK('/html/body/div[6]/div/div[2]/button')
    except:
        pass
    try:
        CLICK('/html/body/section[4]/div/section[1]/div/section[2]/div/a')
    except:
        print_exc()

    data = []

    i = 0
    c = 0
    isImagem = False
    while c < 5:
        i += 1
        c += 1
        try:
            # Tenta pegar um 'clicavel' novo
            els = WAIT_GET(
                f'/html/body/section[4]/div/section[1]/div/div/section[{i}]')
            isImagem = len(els.find_elements_by_tag_name('img'))
            els = els.find_elements_by_tag_name('a')
        except:
            # Se nao tiver, acabou todas as noticias
            break

        # Filtra o que eh relevante dentre um monte de 'clicaveis'
        #    para compartilhar a noticia
        time.sleep(1)
        el = [x for x in els if len(x.text.strip())][0]
        # Pega o texto que acompanha o 'clicavel'
        descr = el.text.replace('\n', ' ')

        # Checa se o texto eh o do botao
        title = el.get_attribute('title')
        if title == 'Carregar mais':
            el.click()
            continue

        # Pega as informacoes do headline da noticia
        link = el.get_attribute('href')
        title = el.get_attribute('title')
        print(title + '\n')

        # Filtro de conteúdo relevante
        if 'estadao' not in link:
            c -= 1
            continue
        elif 'emais.' in link:
            c -= 1
            continue
        elif 'brpolitico.' in link:
            c -= 1
            continue
        elif 'einvestidor.' in link:
            c -= 1
            continue
        try:
            date = TEXT('data-posts')
        except:
            date = TEXT(
                f'/html/body/section[4]/div/section[1]/div/div/section[{i}]/div/div[2]/section[1]/span[2]')

        if isImagem == True:
            isImagemtxt = 'Tem imagem'
        else:
            isImagemtxt = 'Não tem imagem'
        # Cria o objeto da noticia no json
        data.append({
            'link': link,
            'title': title,
            'descr': descr,
            'date': date,
            'imagem': isImagemtxt
        }
        )
    	## Para cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        link = data[i]['link']
        if 'emais.' in link:
            ##  /html/body/div[1]/div[1]/div[2]/section/div/article/div[1]
            data[i]['content'] = 'Conteúdo irrelevante para a pesquisa.'
            continue

        br.get(link)
        time.sleep(1)
        try:
            content = WAIT_TXT('/html/body/section[3]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
        except:
            try:
                content = WAIT_TXT('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
            except:
                content = 'Conteúdo exclusivo'
		                    
        data[i]['content'] = content
    return data, valor

    # try:
    # 	content = WAIT_TXT('/html/body/section[3]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
    # except:
    # 	try:
    # 		content = WAIT_TXT('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
    # 	except:
    # 		# content = 'Conteúdo para assinantes. O programa não conseguiu capturar o conteúdo. (EM TESTES)'
    # 		print_exc()
