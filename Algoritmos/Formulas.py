import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

def Stocastic_Hesston(dt, paths = 30, Ventana = 8, T = 1.0):
    lastYear = np.log(dt['close'].iloc[-252:])
    sigma = lastYear.pct_change().std()*(len(lastYear)**0.5)
    mu = (lastYear[-1:].values[0]/lastYear[:1].values[0])-1

    last_price = dt["close"].iloc[-1]

    dt = T/Ventana
    S = sp.zeros([Ventana], dtype = float)
    x = range(0,int(Ventana))

    df = pd.DataFrame()
    
    plt.figure(figsize=(10,15))
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
    plt.hist(df.iloc[-1],bins = 40, edgecolor='black')

    minimo = 0
    maximo = 0
    n, bins, _ = plt.hist(df.iloc[-1], bins=30, edgecolor='black', alpha=0)
    percentages = (n / sum(n)) * 100
    for lns in df.iloc[-1]:
        if lns > last_price:
            maximo += 1
        else:
            minimo += 1

    print("Alza: ",maximo/len(df.iloc[-1]))
    print('Baja: ',minimo/len(df.iloc[-1]))

    for percentage, bin_edge in zip(percentages, bins[:-1]):
        plt.text(bin_edge + 0.5, percentage, f'{percentage:.1f}%', ha='center', va='bottom', fontsize = 6)


    plt.grid(axis = "y", linestyle = "--")
    plt.show()
