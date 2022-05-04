from flask import Flask,render_template, request, Response, redirect, url_for
app = Flask(__name__)

import pandas as pd


lstGioc = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Tutti')
lstPort = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Portieri')
lstDif = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Difensori')
lstCen = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Centrocampisti')
lstAtt = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22 .xlsx', sheet_name = 'Attaccanti')


@app.route("/", methods=["GET"])
def home():
  global elSquadre
  elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
  listaGioc = lstGioc

  return render_template("home.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)

@app.route("/selsquadra", methods=["GET"])
def selsquadra():
  #radio button
  sceltaruolo= request.args["scelta"]
  if sceltaruolo == "AllRoles":
    listaGioc= lstGioc
  elif sceltaruolo == "P":
    listaGioc= lstPort
  elif sceltaruolo == "D":
    listaGioc= lstDif
  elif sceltaruolo == "C":
    listaGioc= lstCen
  elif sceltaruolo == "A":
    listaGioc= lstAtt


  return render_template("home.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3247, debug=True)