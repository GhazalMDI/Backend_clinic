import requests

url = 'https://api.neshan.org/v5/reverse'

def map(lat,lng):
    params = {
        'lat':lat,
        'lng':lng
    }
    
    headers = {
        'Api-Key': 'service.5e4ab9dec08a4aba81dfc0c44cb78027'
    }
    response = requests.get(url,params=params,headers=headers)
    if response.status_code == 200:
        return response.json()
    return response.status_code