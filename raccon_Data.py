import requests
import re
import json

def id_produto(e):
  return e["product_id"]

'''
a) IDs dos produtos que contém "promoção" no título e seus respectivos preços para todas as mídias. O
resultado deve estar ordenado por preço e depois ID, de forma CRESCENTE. OBS: Não pode conter IDs de
produtos repetidos.
'''
def parte_A(raw_json):
    # Lista que conterá os produtos do item A
    lista_A = []

    # Percorrendo todos os posts em busca da string "promocao" no titlo
    for produtos in raw_json["posts"]:

        if re.search('promocao', produtos["title"], re.IGNORECASE):
            # Se encontrou coloca o post na lista
            lista_A.append(produtos)

    # Ordena a lista com o primeiro critério sendo o preço e depois o ID do produto
    lista_A = sorted(lista_A, key=lambda k: (k["price"],k["product_id"]))

    # Remove produtos com ids repetidos
    lista_A_product_id = []
    new_lista_A = []

    for produto in lista_A: 
        if produto["product_id"] not in lista_A_product_id:
            lista_A_product_id.append(produto["product_id"])
            new_lista_A.append(produto) 

    lista_A = new_lista_A

    '''
    # Visualização
    cont = 0
    for prod in lista_A:
        cont += 1
        print(str(cont) + "  - " + str(prod))
        print(" ")
    '''

    return lista_A


'''
b) IDs dos posts e preços dos produtos para as postagens com mais de 700 likes na mídia
"instagram_cpc". O resultado deve estar ordenado por preço e depois ID de forma CRESCENTE.
'''
def parte_B(raw_json):
    # Lista que conterá os produtos do item B
    lista_B = []

    # Percorrendo todos os posts em busca da string "promocao" no titlo
    for produtos in raw_json["posts"]:

        if re.search('instagram_cpc', produtos["media"], re.IGNORECASE):
            if produtos["likes"] > 700:
                # Se encontrou e for maior coloca o post na lista
                lista_B.append(produtos)

    # Ordena a lista com o primeiro critério sendo o preço e depois o ID do post
    lista_B = sorted(lista_B, key=lambda k: (k["price"],k["post_id"]))

    '''
    # Visualização
    cont = 0
    for prod in lista_B:
        cont += 1
        print(str(cont) + "  - " + str(prod))
        print(" ")
    '''

    return lista_B


'''
c) Somatório de likes no mês de maio de 2019 para todas as mídias pagas (google_cpc, facebook_cpc,
instagram_cpc).
'''
def parte_C(raw_json):
    # Variável com todos os posts
    lengh_json = len(raw_json["posts"])

    # Somatório de likes do mês de maio
    likes_maio = 0

    # Percorrendo todos os posts em busca da string "promocao" no titlo
    for produtos in raw_json["posts"]:

        if re.search('/05/', produtos["date"], re.IGNORECASE):
            if re.search('google_cpc', produtos["media"], re.IGNORECASE) or re.search('facebook_cpc', produtos["media"], re.IGNORECASE) or re.search('instagram_cpc', produtos["media"], re.IGNORECASE):
                # Adiciona o número de likes ao somatório de likes de maio
                likes_maio += produtos["likes"]

    #print("Quantidade de likes no mês de maio: " + str(likes_maio))
 
    return likes_maio



'''
d) Todos os IDs de produtos devem ter o mesmo preço nas postagens. Eventualmente poderá ocorrer
postagens com o mesmo produto e diferentes preços, causando problemas para o cliente.

Sua tarefa é verificar se existe alguma inconsistência nos produtos que a API retorna pela rota 
https://uscentral1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error

Caso seja encontrado algum erro, envie em uma lista todos os IDs de produtos com erro de forma ordenada
e crescente.
'''
def parte_D(raw_json):
    # Lista que conterá os produtos do item D
    lista_D = []
    lista_D_product_id = []
    lista_D_errados = []

    # Variável com todos os posts
    lengh_json = len(raw_json["posts"])

    # Verifica se existem ID's repetidos, se estiver só irá colocar a primeira ocorrência em uma lista
    for produto in raw_json["posts"]:
        if produto["product_id"] not in lista_D_product_id:
            lista_D_product_id.append(produto["product_id"])
            lista_D.append(produto)

    # Irá verificar se com as ocorrência da lista montada anteriormente, existe duplicada de ID's com preços diferentes
    for produto in raw_json["posts"]:
        for prod2 in lista_D:
            if produto["product_id"] == prod2["product_id"]:
                if produto["price"] != prod2["price"]:
                    lista_D_errados.append(produto)

    # Ordena a lista com o ID do produto
    lista_D_errados = sorted(lista_D_errados, key=id_produto)

    '''
    #Visualização
    for produto in lista_D_errados:
        print(produto)
    '''

    return lista_D_errados


def enviar_resposta(resposta_A, resposta_B, resposta_C, resposta_D):
    final_response = {
        'full_name': "Gustavo de Souza",
        'email': "gustavo.dcomp@gmail.com",
        'code_link': "www.github.com/gusstavo/raccon_ps",
        'response_a': [
        ],
        'response_b': [

        ],
        'response_c': 0,
        'response_d': [
        ]
    }

    for elemento in resposta_A:
        final_response["response_a"].append({"product_id":elemento["product_id"],"price_field":elemento["price"]})
    
    for elemento in resposta_B:
        final_response["response_b"].append({"post_id":elemento["post_id"],"price_field":elemento["price"]})

    final_response["response_c"] = resposta_C

    for elemento in resposta_D:
        final_response["response_d"].append(elemento["product_id"])


    return final_response


def main():
    url = "https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get"
    response = requests.get(url)
    # Variável com todos os posts
    raw_json = response.json()

    resposta_A = []
    resposta_B = []
    resposta_C = 0
    resposta_D = []

    # Executa a solução de cada parte
    resposta_A = parte_A(raw_json)
    resposta_B = parte_B(raw_json)
    resposta_C = parte_C(raw_json)

    # Caminho alterado para a última parte
    url = "https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error"
    response = requests.get(url)
    raw_json = response.json()

    resposta_D = parte_D(raw_json)

    # Recebe o json com as respostas
    resultado = enviar_resposta(resposta_A, resposta_B, resposta_C, resposta_D)

    #print(json.dumps(resultado, indent=4))
    
    # Apenas gerar um arquivo com a resposta
    with open('resposta.json', 'w') as json_file:
        json.dump(resultado, json_file)

    # Prepara para realizar o request
    headers = {
        'Content-Type': 'application/json',
    }
    url = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post'

    response = requests.post(url, headers=headers, data=resultado)

    print("Response:" + str(response))


if __name__ == '__main__':
    main()
