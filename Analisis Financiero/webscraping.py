import requests
from bs4 import BeautifulSoup

# URL de la página de Investing.com que deseas scrapear
url = 'https://es.investing.com/equities/nvidia-corp-cash-flow'

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ejemplo: Extraer el precio de las acciones de Apple
    price_element = soup.find('span', {'id': 'last_last'})
    
    if price_element:
        stock_price = price_element.text.strip()
        print(f'Precio de las acciones de Apple: {stock_price}')
    else:
        print('No se pudo encontrar el precio de las acciones.')
else:
    print(f'Error al hacer la solicitud. Código de estado: {response.status_code}')
