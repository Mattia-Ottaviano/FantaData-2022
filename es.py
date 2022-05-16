from flask import Flask,render_template, request, Response, redirect, url_for, session
app = Flask(__name__)

import pandas as pd
from IPython.display import HTML

lstGioc = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = 'Tutti')
lstPort = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = 'Portieri')
lstDif = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = 'Difensori')
lstCen = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = 'Centrocampisti')
lstAtt = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = 'Attaccanti')




@app.route("/", methods=["GET"])
def home():
  global elSquadre, criteri
  elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
  listaGioc = lstGioc
  criteri = list(lstGioc.columns.values)
  

  
      
  return render_template("home.html", listaGioc = listaGioc.to_html(border=0, escape=False), squadre= elSquadre, criteri=criteri)


@app.route("/selruolo", methods=["GET"])
def selruolo():

  global listaGioc
   
  sceltaruolo = request.args["scelta"]
  sceltasquadra= request.args["squadra"]
  sceltacriterio= request.args["criterio"]
  sceltagiocatore= request.args["calciatore"]

  if sceltaruolo == "AllRoles":
    listaGioc = lstGioc 
  elif sceltaruolo == "P":
    listaGioc = lstPort 
  elif sceltaruolo == "D":
    listaGioc = lstDif 
  elif sceltaruolo == "C":
    listaGioc = lstCen  
  elif sceltaruolo == "A":
    listaGioc = lstAtt
    

  if sceltasquadra== "-":
      listaGioc = listaGioc[listaGioc['Squadra']==listaGioc['Squadra']]
  elif sceltasquadra in listaGioc['Squadra'].values:
      listaGioc = listaGioc[listaGioc['Squadra']==sceltasquadra]




  if sceltacriterio== "-":
      listaGioc = listaGioc
  elif sceltacriterio in criteri:
    if sceltacriterio == 'Nome'or sceltacriterio == 'Squadra':
      listaGioc = listaGioc.sort_values(by=sceltacriterio, ascending= True)
    else:
      listaGioc = listaGioc.sort_values(by=sceltacriterio, ascending= False)


  if sceltagiocatore == "":
    listaGioc = listaGioc
  #elif sceltagiocatore not in listaGioc['Nome'].to_list():

    #return render_template("errore.html", gioc=sceltagiocatore)
  
  else:
    listaGioc= listaGioc[listaGioc['Nome'].str.startswith(sceltagiocatore.upper())]

  
  #if sceltagiocatore not in listaGioc['Nome'].to_list():
    #return render_template("errore.html", gioc = sceltagiocatore)


  def convert(column):
    return '<a href="/workspace/FantaData-2022/{}">{}</a>'.format(column['Nome'],  column.Nome)

  listaGioc['Nome'] = listaGioc.apply(convert, axis=1)

  #listaGioc['Nome'] = listaGioc['Nome'].apply(lambda x: f'<a href="/workspace/FantaData-2022/templates/player.html/{x}">{x}</a>')
  #HTML(listaGioc.to_html(escape=False))

  return render_template("home.html", listaGioc = listaGioc.to_html(border=0, escape=False), squadre= elSquadre, criteri=criteri)


@app.route("/workspace/FantaData-2022/<giocatore>", methods=["GET"])
def infogioc(giocatore):
  info_gioc = listaGioc[listaGioc["Nome"] == f'<a href="/workspace/FantaData-2022/{giocatore}">{giocatore}</a>']
  squadra = info_gioc['Squadra'].values[0]
  gol = info_gioc['Gf'].values[0]
  assist = info_gioc['Ass'].values[0]
  amm = info_gioc['Amm'].values[0]
  esp = info_gioc['Esp'].values[0]
  media= info_gioc['Mv'].values[0]
  fantamedia= info_gioc['Mf'].values[0]
  print(squadra)
  return render_template("player.html", nome=giocatore, info_gioc=info_gioc.to_html(), squadra = squadra, gol =gol, assist= assist, amm = amm, esp= esp, media= media, fantamedia= fantamedia )





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3247, debug=True)