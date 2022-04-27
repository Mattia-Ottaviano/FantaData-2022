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

lstGioc = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = ['Tutti'])
lstPort = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = ['Portieri'])
lstDif = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = ['Difensori'])
lstCen = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = ['Centrocampisti'])
lstAtt = pd.read_excel('/workspace/FantaData-2022/Statistiche_Fantacalcio_2021-22.xlsx', sheet_name = ['Attaccanti'])
print(lstDif)

@app.route("/", methods=["GET"])
def home():
  listaGioc = lstGioc
  return render_template("home.html", listaGioc = listaGioc.to_html())




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)