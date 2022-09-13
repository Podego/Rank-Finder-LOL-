import re
import os
from tkinter import *
from riotwatcher import LolWatcher, ApiError

def find_rank(username):
    try:
        api_key = 'KEY_HERE'
        watcher = LolWatcher(api_key)
        region = 'br1'
        me = watcher.summoner.by_name(region, username)
        ranked_stats = watcher.league.by_summoner(region, me['id'])
        for queue in ranked_stats:
            if queue['queueType'] == "RANKED_SOLO_5x5":
                tier = queue['tier']
                rank = queue['rank']
                return tier, rank #tier = elo / rank = divisão
            else:
                return     
    except:
        print(f'Nick {username} não encontrado.')
def pegar_nicks():
    dir = directory.get()
    logs = os.listdir(dir)
    num_logs = 1
    nick_list = []
    for file in logs:
        extensao = os.path.splitext(file)[1]
        if extensao == '.log':
            path = os.path.join(dir, file)
            log = open(path, 'r')
            linhas = log.readlines()
            for linha in linhas:
                if 'CurrentSummoner' in linha:
                    lin = linha
                    nick = re.search(r'\B"displayName":".*","internalName"\B', lin)
                    nick = nick[0]
                    nick = nick[15:-16]
                    if nick in nick_list:
                        continue
                    else:
                        nick_list.append(nick)
                        try:
                            tier, rank = find_rank(nick)
                            elo = tier + ' ' + rank
                            Label(exibir, text=f'Nick {num_logs}: {nick}\nElo: {elo}').grid(row = num_logs + 1)
                        except:
                            Label(exibir, text=f'Nick {num_logs}: {nick}\nElo: Nome de invocador inválido para buscas.').grid(row = num_logs + 1)
                        num_logs += 1            
                    

master = Tk()
master.title('Verificador de Smurfs')
Label(master, text= 'Diretório: ').grid(row=0)
exibir = Label(master)
exibir.grid(row = 2)
directory = Entry(master)
directory.grid(row=0, column = 1)
Button(master, text='Verificar', command=pegar_nicks).grid(row = 3, column = 0)
Button(master, text='Quit', command=master.quit).grid(row=3, column=1, sticky=W, pady=4)
mainloop()
