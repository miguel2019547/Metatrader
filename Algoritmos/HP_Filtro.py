import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from Informacion import Informacion
import plotly.graph_objects as go
from plotly.subplots import make_subplots

datos = Informacion("Nvidia", 5000 , "M1")
CambioTend = 0
datos["ciclo"], datos["tendencia"] = sm.tsa.filters.hpfilter(datos["close"], lamb=150000)
DifData = 480
datos['return'] = datos["tendencia"] - datos["tendencia"].shift(1)
Bajo = np.percentile(datos['ciclo'][-DifData:],0.02)
Alto = np.percentile(datos['ciclo'][-DifData:],0.98)
Rest  = np.abs(Alto - Bajo)

Total_Valores = []
for a in range(100000):
    Nuevos_Valores = []
    Fecha = []
    x = datos["close"].iloc[-1]
    Tendencia = datos['return'][int(-DifData*2.5):].mean()
    Tiempo = datos['time'].iloc[-1]
    for i in range(DifData):
        x = x+Tendencia + np.random.normal(0,Rest/1.15) - CambioTend
        Tiempo = Tiempo + pd.Timedelta(days = 1)
        Fecha.append(Tiempo)
        Nuevos_Valores.append(x)
    Total_Valores.append(Nuevos_Valores)


Total_Valores = np.array(Total_Valores)
Final_Valores = Total_Valores[:,-1:]


plt.axvline(x = np.mean(Final_Valores), color = 'grey', linestyle = '--', label = f'{np.mean(Final_Valores)}')
plt.hist(Final_Valores, bins = 40, alpha = 0.6)
plt.title(f"El valor Minimo es {round(np.min(Total_Valores),2)}")
plt.xlabel(f'El valor Actual es: {round(datos["close"].iloc[-1],2)}')
plt.grid(axis='y', linestyle = '--')
plt.legend()
plt.show()

abc = np.array([[1,2,3],[3,4,5],[5,6,7]])
abc[:,-1:]

np.mean(Final_Valores)-datos["close"].iloc[-1]





fig = make_subplots(rows=2, cols=1, subplot_titles=[f'GBPUSD'])



fig.add_trace(go.Candlestick(x=datos["time"],
                              open = datos['open'],
                              close = datos["close"],
                              high = datos["high"],
                              low = datos["low"],
                                name="GBPUSD"), row = 1, col = 1)

fig.add_trace(go.Scatter(x = datos["time"], y = datos["tendencia"], mode = "lines", name = "Tendencia"), row=1, col = 1)

fig.add_trace(go.Scatter(x = datos["time"], y = datos["ciclo"], mode = "lines", name = "ciclo"), row = 2 , col = 1)


fig.update_layout(
    title='Gráfico de Velas',
    xaxis_title='Fecha',
    yaxis_title='Precio',
    xaxis_rangeslider_visible=False  # Si no deseas mostrar el control deslizante de rango en el eje x
)
fig.update_xaxes(type = "category")

fig.show()


datos["ciclo"].std()

datos["ciclo"].mean()

import numpy as np

# Obtener la señal desde el DataFrame
señal = datos["tendencia"].values

# Calcular la DFT de la señal
dft = np.fft.fft(señal)
frecuencias = np.fft.fftfreq(len(señal), d=1)  # Frecuencias en Hz

# Encontrar las componentes senoidales
amplitudes = np.abs(dft) / len(señal)
fases = np.angle(dft)

# Filtrar las componentes significativas (puedes ajustar este umbral según tus necesidades)
umbral_amplitud = 0.000528  # Por ejemplo, considerar solo las amplitudes mayores que 10

# Filtrar las componentes significativas
componentes_significativas = [(frecuencias[i], amplitudes[i], fases[i]) for i in range(len(señal)) if amplitudes[i] > umbral_amplitud]

# Imprimir las componentes significativas encontradas
print("Componentes senoidales significativas:")
for frecuencia, amplitud, fase in componentes_significativas:
    print(f"Frecuencia: {frecuencia} Hz, Amplitud: {amplitud}, Fase: {fase} rad")

g =np.linspace(1,len(datos), len(datos))

# Graficar la señal original y las componentes senoidales encontradas
plt.figure(figsize=(12, 6))
plt.subplot(2,1,1)
plt.plot(g, señal, label='Señal original')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.legend()
plt.title('Señal Original y Componentes Senoidales Significativas')

plt.subplot(2,1,2)
# Graficar cada componente senoidal significativa
for i, (frecuencia, amplitud, fase) in enumerate(componentes_significativas):
    if frecuencia > 0:
        componente = amplitud * np.cos(2 * np.pi * frecuencia * np.arange(len(señal)) + fase)
        plt.plot(g, componente, label=f'Frecuencia: {frecuencia} Hz')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid()
plt.show()

#---------------------------------------------------------------------------------------------

#                       Modelo Browniano

#---------------------------------------------------------------------------------------------

import scipy as sp
import numpy as np
from Inicializar import IniciarMT5
IniciarMT5()
from datetime import datetime as dt
import datetime as dat
db = Informacion("US100-DEC23", 500 , "D1")


lastYear = np.log(db['close'].iloc[-252:])
sigma = lastYear.pct_change().std()*(len(lastYear)**0.5)

mu = (lastYear[-1:].values[0]/lastYear[:1].values[0])-1

Ventana = 8
T = 1.0
last_price = db["close"].iloc[-1]

sp.random.seed(10)
paths = 30
dt = T/Ventana
S = sp.zeros([Ventana], dtype = float)
x = range(0,int(Ventana))

df = pd.DataFrame()

#-------------------- La Grafica ---------------------------------------------------------------------------

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
for a in range(paths):
    S[0] = last_price
    for b in x[:-1]:
        e = np.random.normal()
        S[b+1] = S[b]+S[b]*(mu - 0.5*pow(sigma,2))*dt+sigma*S[b]*np.sqrt(dt)*e
        df[a] = S
    plt.plot(x,S, linestyle = "--")
plt.title("Caminos de Movimiento Browniano")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.grid()
plt.subplot(2,1,2)
plt.hist(df.iloc[-1],bins = 10)
plt.grid(axis = "y", linestyle = "--")
plt.show()

Ultima_Fecha = db['time'].iloc[-1]
Fechas = []
for i in x:
    Fechas.append(Ultima_Fecha)
    Ultima_Fecha = Ultima_Fecha + pd.Timedelta(days=1)

df["Fechas"] = Fechas
plt.figure(figsize=(16,8))
plt.plot(db["time"].iloc[-100:],db["close"].iloc[-100:])
plt.plot(df['Fechas'],df.drop('Fechas',axis =1))
plt.grid(axis = "y", linestyle = "--")
plt.show()