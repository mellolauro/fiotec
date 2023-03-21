#Programa02.v1
#Programa destinado para avaliação da Fiotec

import mysql.connector
db_connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="msg_email")
cursor = db_connection.cursor()
cursor.execute("select remetente, destinatario, dt_hora, conteudo from arquivo_email")

palavras = []
palavras_nome = []
bodys=[]

for (remetente, destinatario, dt_hora, conteudo) in cursor:
    body= remetente+" "+destinatario+" "+dt_hora+" "+conteudo
    body=body.replace(' - ', '-')
    bodys.append(body)
    body = body.replace('/', ' ')
    body = body.replace('.', ' ')
    body_array=body.split(' ')
    for pv in body_array:
        pv = pv.replace(',', '')
        pv = pv.replace(' ', '')
        pv = pv.replace('<', '')
        pv = pv.replace('>', '')
        pv = pv.replace("\t", '')
        pv = pv.replace("\n", '')
        pv = pv.replace(':', '')
        pv = pv.replace('#', '')
        pv = pv.replace('?', '')
        pv = pv.replace('"', '')
        if pv != "" and pv!='-' and pv!='/':
            if len(pv)>=2 and (pv[0].isupper() and pv[1].islower()) and pv in destinatario and pv not in remetente and 'Equinix' not in pv:
                if pv not in palavras_nome :
                        palavras_nome.append(pv)
            else:
                if pv.lower() not in pvavras:
                    palavras.append(pv.lower())

palavras_nome_filter=[]
palavras_filter=[]
exibe_db=cursor.rowcount*0.05
for pv in palavras_nome:
    exibe=0
    for body in bodys:
        body=body.replace("\t", '')
        body = body.replace("\n", '')
        if(pv in body):
            exibe+=1
        if(exibe>=exibe_db):
            palavras_nome_filter.append(pv)
            break

for pv in palavras:
    exibe=0
    for body in bodys:
        body=body.replace("\t", '')
        body = body.replace("\n", '')
        if(pv in body.lower()):
            exibe+=1
        if(exibe>=exibe_db):
            palavras_filter.append(pv)
            break

bodys=None
cursor.execute("delete from palavra_chave;")
db_connection.commit()
dicionario='';
with open('dicionario.txt') as arquivo:
    dicionario= arquivo.read()

for pv in palavras_filter:
    type='Outros'
    if(pv in dicionario):
        type='Dicionário'
    cursor.execute("INSERT INTO palavra_chave (chave, tipo) VALUES (%s, %s);", (pv, type))

for pv in palavras_nome_filter:
    type='Nome Próprio'
    cursor.execute("INSERT INTO palavra_chave (chave, tipo) VALUES (%s, %s);", (pv, type))

db_connection.commit()
db_connection.close()