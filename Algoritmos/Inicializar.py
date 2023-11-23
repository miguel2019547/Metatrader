import datetime as dt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

class IniciarMT5():
    def __init__(self):
        mt5.initialize(login = 95570806, server = "XMGlobal-MT5 5", password = "Qlagarty$2023#")
        self.authorized = mt5.login(login = 95570806, server = "XMGlobal-MT5 5", password = "Qlagarty$2023#")
        if not mt5.login(login = 95570806, server = "XMGlobal-MT5 5", password = "Qlagarty$2023#"):
            print("inicializacion falló")
            mt5.shutdown()
        else:
            print("Inicializacion Completa")


    def Informacion(self):
        
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        
        # connect to the trade account specifying a password and a server
        
        if self.authorized:
            account_info=mt5.account_info()
            if account_info!=None:
                account_info_dict = mt5.account_info()._asdict()
                # convert the dictionary into DataFrame and print
                df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
                print(f"Informacion de Cuenta\n{df}")
        else:
            print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
    print('Failed to login')

