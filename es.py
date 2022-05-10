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

@app.route("/selruolo", methods=["GET"])
def selsquadra():
  #radio button
  sceltaruolo= request.args["scelta"]

  if sceltaruolo == ""
    if sceltaruolo == "AllRoles":
      listaGioc = lstGioc
      return render_template("home.html", listaGioc = listaGioc.to_html(border=0))
    elif sceltaruolo == "P":
      listaGioc = lstPort
      return render_template("portieri.html", listaGioc = listaGioc.to_html(border=0))
    elif sceltaruolo == "D":
      listaGioc = lstDif
      return render_template("difensori.html", listaGioc = listaGioc.to_html(border=0))
    elif sceltaruolo == "C":
      listaGioc = lstcen
      return render_template("centrocampisti.html", listaGioc = listaGioc.to_html(border=0))
    elif sceltaruolo == "A":
      listaGioc = lstAtt
      return render_template("attaccanti.html", listaGioc = listaGioc.to_html(border=0))
  else:

   
  
  
  return render_template("home.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


@app.route("/allroles", methods=["GET"])
def allroles():
    elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
    listaGioc = lstGioc
    return render_template("allroles.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


@app.route("/por", methods=["GET"])
def por():
    elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
    listaGioc = lstPort
    return render_template("por.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


@app.route("/dif", methods=["GET"])
def dif():
    elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
    listaGioc = lstDif
    return render_template("por.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


@app.route("/cen", methods=["GET"])
def cen():
    elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
    listaGioc = lstCen
    return render_template("por.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)


@app.route("/att", methods=["GET"])
def att():
    elSquadre = lstGioc['Squadra'].drop_duplicates().sort_values(ascending=True)
    listaGioc = lstAtt
    return render_template("por.html", listaGioc = listaGioc.to_html(border=0), squadre= elSquadre)





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3247, debug=True)