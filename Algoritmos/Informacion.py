import MetaTrader5 as mt5
from Inicializar import IniciarMT5
import pandas as pd
import plotly.graph_objects as go
import pytz
from datetime import datetime as dt
import datetime as dat
import numpy as np
IniciarMT5()
timezone = pytz.timezone("Etc/UTC")
def TicketsBol(tcs):
    utc = dt(dt.today().year,dt.today().month,dt.today().day,dt.today().hour,dt.today().minute, dt.today().second) + dat.timedelta(hours=3) - dat.timedelta(microseconds=800)
    Ticket = mt5.copy_ticks_from("US100-DEC23",utc,tcs, mt5.COPY_TICKS_ALL)
    Ticket = pd.DataFrame(Ticket)
    time = []
    time_msc = []
    for t in range(len(Ticket)):
        time.append(dt.fromtimestamp(int(Ticket["time"].iloc[t])))
        time_msc.append(dt.fromtimestamp(Ticket["time_msc"].iloc[t]/1000))
    Ticket["time"] = time
    Ticket["time_msc"] = time_msc


    print(Ticket)



def UltimoTicket(Symbol):
    lasttick=mt5.symbol_info_tick(str(Symbol))
    Dictionary = {
        "fecha" :dt.fromtimestamp(lasttick[5]/1000),
        "bid"   : lasttick[1],
        "ask"   : lasttick[2],
        "flags" : lasttick[6]
    }
    return Dictionary


def Informacion(Symbol, Partidas, Tiempo):
    Dicionario = {"M5": mt5.TIMEFRAME_M5,
              "M10": mt5.TIMEFRAME_M10,
              "H4"  : mt5.TIMEFRAME_H4,
              "M15" : mt5.TIMEFRAME_M15,
              "M1"  : mt5.TIMEFRAME_M1,
              "M30" : mt5.TIMEFRAME_M30,
              "H1"  : mt5.TIMEFRAME_H1,
              "D1"  : mt5.TIMEFRAME_D1,
              "W1"  : mt5.TIMEFRAME_W1,
              }
    rates = pd.DataFrame(mt5.copy_rates_from(Symbol, Dicionario.get(Tiempo) , dt.today() + dat.timedelta(hours= 4), Partidas))
    Tiempo = []
    for T in range(len(rates)):
        Tiempo.append(dt.fromtimestamp(rates['time'].iloc[T]))
    rates['time'] = Tiempo
    rates = rates[~rates['time'].dt.dayofweek.isin([5, 6])]
    rates.set_index('time', inplace=True)
    return rates

#--------------------------------------------------------------
#                      Funciones de Indicadores
#--------------------------------------------------------------
class GeneradorCuotas():
    
    def __init__(self, Capital, Interes, Cuotas):

        self.Interes = Interes/100
        self.Cuotas = Cuotas
        Cuota = np.linspace(1,Cuotas,Cuotas).astype(int)
        Fecha = dat.datetime.now()

        ListaFecha = []
        ListaDias = []
        
        for i in range(0,self.Cuotas):
            Fechas_Siguientes = Fecha + pd.DateOffset(months = i+1)
            if Fechas_Siguientes.weekday() == 6:
                Fechas_Siguientes = Fecha + pd.DateOffset(months = i+1) + pd.DateOffset(days=1)

            ListaFecha.append(Fechas_Siguientes.strftime('%Y-%m-%d'))
            ListaDias.append((Fechas_Siguientes - dat.datetime.now()).days)
        
        self.BaseDatos = pd.DataFrame({"Cuota": Cuota,
                                       "Fecha de Vencimiento": ListaFecha,
                                       "D1" : ListaDias})
        
        self.BaseDatos["Factor de Actualizacion"] = 1/((1+self.Interes)**(self.BaseDatos["D1"]/360))

        FactorActualizacion = self.BaseDatos["Factor de Actualizacion"].sum()

        Valor_Cuota = Capital/FactorActualizacion
        self.valor = Valor_Cuota
        Intereses = []
        Amortizacio = []
        Saldo = []
        Saldo.append(Capital)
        for Filas in range(len(self.BaseDatos)):
            if Filas == 0:
                Interes = Capital * ((1 + self.Interes)**(self.BaseDatos["D1"].iloc[Filas]/360)-1)
            else:
                Interes = Capital * ((1 + self.Interes)**((self.BaseDatos["D1"].iloc[Filas]-self.BaseDatos["D1"].iloc[Filas-1])/360)-1)
            Amortizacion = Valor_Cuota - Interes
            Capital -= Amortizacion
            Saldo.append(Capital)
            Amortizacio.append(Amortizacion)
            Intereses.append(Interes)

        self.BaseDatos["Saldo"] = Saldo[:-1]
        self.BaseDatos["Amortizacion"] = Amortizacio
        self.BaseDatos ["Interes"] = Intereses
        self.BaseDatos["Cuota Total"] = Valor_Cuota

        self.BaseDatos[["Saldo","Amortizacion","Interes","Cuota Total"]] = round(self.BaseDatos[["Saldo","Amortizacion","Interes","Cuota Total"]],2)

    def Para_Excel(self,Nombre):
        self.BaseDatos.to_excel(f"{Nombre}.xlsx", index= False)

    def Seguros_Comisiones(self, Seguros, Comisiones):
        self.BaseDatos["Seguro"] = Seguros
        self.BaseDatos["Comisiones"] = Comisiones
        self.BaseDatos["Cuota Total"] = self.valor + self.BaseDatos[["Seguro","Comisiones"]].sum(axis = 1)
        self.BaseDatos[["Cuota Total","Seguro","Comisiones"]] = round(self.BaseDatos[["Cuota Total","Seguro","Comisiones"]],2)



