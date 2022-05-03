from flask import Flask,render_template, request, Response, redirect, url_for
app = Flask(__name__)

#import io
import pandas as pd
#import geopandas as gpd
#import contextily
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

lstGioc = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Tutti')
lstPort = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Portieri')
lstDif = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Difensori')
lstCen = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Centrocampisti')
lstAtt = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Attaccanti')


@app.route("/", methods=["GET"])
def home():
  global elSquadre
  elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
  listaGioc = lstGioc.drop('Id', axis = 1)

  return render_template("home.html", listaGioc = listaGioc.to_html(), squadre= elSquadre)

@app.route("/selsquadra", methods=["GET"])
def selsquadra():
  #radio button
  sceltaruolo= request.args["scelta"]
  if sceltaruolo == "AllRoles":
    listaGioc= lstGioc.drop('Id', axis = 1)
  elif sceltaruolo == "P":
    listaGioc= lstPort.drop('Id', axis = 1)
  elif sceltaruolo == "D":
    listaGioc= lstDif.drop('Id', axis = 1)
  elif sceltaruolo == "C":
    listaGioc= lstCen.drop('Id', axis = 1)
  elif sceltaruolo == "A":
    listaGioc= lstAtt.drop('Id', axis = 1)
  return render_template("home.html", listaGioc = listaGioc.to_html(), squadre= elSquadre)
 

  #menù a tendina
  SquadraUtente = request.args['squadra']
  listaGioc = lstGioc[lstGioc.Squadra==SquadraUtente.str.contains(SquadraUtente)]
  return render_template("home.html", listaGioc = listaGioc.to_html(), squadre= elSquadre)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3247, debug=True)