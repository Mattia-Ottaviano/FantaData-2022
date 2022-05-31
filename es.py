from flask import Flask, render_template, send_file, make_response, url_for, Response, request
from flask import Flask, render_template, request, Response, redirect, url_for 
app = Flask(__name__)


import io
import pandas as pd
from IPython.display import HTML
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily

lstGioc = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Tutti')
lstPort = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Portieri')
lstDif = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Difensori')
lstCen = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Centrocampisti')
lstAtt = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Attaccanti')
comuni = gpd.read_file("/workspace/FantaData-2022/Comuni.zip")

lstGioc = lstGioc.reset_index(drop=True)
lstPort =lstPort.reset_index(drop=True)
lstDif =lstDif.reset_index(drop=True)
lstCen =lstCen.reset_index(drop=True)
lstAtt =lstAtt.reset_index(drop=True)




#caricamento della schermata home 
@app.route("/", methods=["GET"])
def home():
  global elSquadre, criteri
  elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
  listaGioc = lstGioc
  criteri = list(lstGioc.columns.values)
  

  
      
  return render_template("home.html", listaGioc = listaGioc.to_html(border=0, escape=False), squadre= elSquadre, criteri=criteri)

#Passaggio dei dati richiesti per la ricerca ---> home.html
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
  else:
    listaGioc= listaGioc[listaGioc['Nome'].str.startswith(sceltagiocatore.upper())]

  
  def convert(column):
    return '<a href="/workspace/FantaData-2022/{}">{}</a>'.format(column['Nome'],  column.Nome)

  try:
    listaGioc['Nome'] = listaGioc.apply(convert, axis=1)
  except ValueError:
    return render_template('errore.html')

  return render_template("home.html", listaGioc = listaGioc.to_html(border=0, escape=False), squadre= elSquadre, criteri=criteri)


#Passaggio dati del giocatore richiesto ---> player.html 
@app.route("/workspace/FantaData-2022/<giocatore>", methods=["GET"])
def infogioc(giocatore):



  global info_gioc, comune
  info_gioc = listaGioc[listaGioc["Nome"] == f'<a href="/workspace/FantaData-2022/{giocatore}">{giocatore}</a>']
  squadra = info_gioc['Squadra'].values[0].upper()
  ruolo = info_gioc['R'].values[0]
  pres= info_gioc['Pg'].values[0]
  gol = info_gioc['Gf'].values[0]
  assist = info_gioc['Ass'].values[0]
  amm = info_gioc['Amm'].values[0]
  esp = info_gioc['Esp'].values[0]
  media= info_gioc['Mv'].values[0]
  fantamedia= info_gioc['Mf'].values[0]




  if squadra == 'ATALANTA':
    comune='Bergamo'
  elif squadra == 'BOLOGNA':
    comune='Bologna'
  elif squadra == 'CAGLIARI':
    comune='Cagliari'
  elif squadra == 'EMPOLI':
    comune='Empoli'
  elif squadra == 'FIORENTINA':
    comune='Firenze'
  elif squadra == 'GENOA':
    comune='Genova'
  elif squadra == 'INTER':
    comune='Milano'
  elif squadra == 'JUVENTUS':
    comune='Torino'
  elif squadra == 'LAZIO':
    comune='Roma'
  elif squadra == 'MILAN':
    comune='Milano'
  elif squadra == 'NAPOLI':
    comune='Napoli'
  elif squadra == 'SALERNITANA':
    comune='Salerno'
  elif squadra == 'SAMPDORIA':
    comune='Genova'
  elif squadra == 'SASSUOLO':
    comune='Reggio nell\'Emilia'
  elif squadra == 'SPEZIA':
    comune='La Spezia'
  elif squadra == 'TORINO':
    comune='Torino'
  elif squadra == 'UDINESE':
    comune='Udine'
  elif squadra == 'VENEZIA':
    comune='Venezia'
  elif squadra == 'VERONA':
    comune='Verona'
  else:
    comune='Roma'

  


  
  return render_template("player.html", comune=comune, nome=giocatore, info_gioc=info_gioc.to_html(), squadra = squadra, ruolo= ruolo, pres=pres, gol =gol, assist= assist, amm = amm, esp= esp, media= media, fantamedia= fantamedia )





#Grafici e Mappe
@app.route("/grafico.png", methods=["GET"])
def graficopng():

    df= info_gioc[['Pg','Gf','Ass','Amm','Esp','Mv','Mf']]
    
    print(df)

    fig, ax = plt.subplots(figsize = (10,2))

    
    ax.bar(df.columns, df.values[0])


    ax.set_ylim(0,38)
    plt.savefig('/workspace/FantaData-2022/static/styles/fig.png')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

    
    
@app.route("/mappa.png", methods=["GET"])
def mappapng():
    fig, ax = plt.subplots(figsize = (8,4))
    com = comuni[comuni['COMUNE']==comune]
    com.to_crs(epsg=3857).plot(ax=ax, edgecolor="k", facecolor="red", alpha=0.4)
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3247, debug=True)