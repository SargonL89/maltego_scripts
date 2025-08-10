import sys
import requests
import json
import os
from MaltegoTransform import *

def digital_presence(person_name, email=None):
    mt = MaltegoTransform()
    
    # Cargar keys desde config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            bing_key = config.get('bing_api_key')
            ipqs_key = config.get('ipqs_api_key') if email else None
            if not bing_key:
                raise ValueError("Bing API key no encontrada en config.json")
    except Exception as e:
        mt.addUIMessage(f"Error al cargar config.json: {str(e)}")
        mt.returnOutput()
        return
    
    # Paso 1: Bing Search para URLs relacionadas con la persona
    bing_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": f"{person_name} social profiles site:x.com OR site:linkedin.com OR site:instagram.com", "count": 10}
    try:
        response = requests.get(bing_url, headers=headers, params=params)
        data = response.json()
        
        if 'webPages' in data:
            for result in data['webPages']['value']:
                url = result['url']
                # Crear entidad URL
                url_entity = mt.addEntity("maltego.URL", url)
                
                # Extraer alias social si aplica (simple parsing)
                if 'x.com' in url:
                    alias = url.split('/')[-1]
                    alias_entity = mt.addEntity("maltego.Alias", alias)
                    alias_entity.addProperty("description", "X Profile", "loose", "Posible perfil en X")
                elif 'linkedin.com' in url:
                    alias = url.split('/')[-1]
                    alias_entity = mt.addEntity("maltego.Alias", alias)
                    alias_entity.addProperty("description", "LinkedIn Profile", "loose", "Posible perfil en LinkedIn")
                
                # Análisis simple: Si menciona Tesla/SpaceX, agregar Organization
                if 'tesla' in result['snippet'].lower():
                    mt.addEntity("maltego.Organization", "Tesla")
                elif 'spacex' in result['snippet'].lower():
                    mt.addEntity("maltego.Organization", "SpaceX")
        else:
            mt.addUIMessage("No se encontraron resultados en Bing Search.")
    
    except Exception as e:
        mt.addUIMessage(f"Error en Bing Search: {str(e)}")
    
    # Paso opcional: Si hay email, verificar con IPQualityScore y encadenar Bing Search
    if email and ipqs_key:
        ipqs_url = f"https://www.ipqualityscore.com/api/json/email/{ipqs_key}/{email}"
        try:
            response = requests.get(ipqs_url)
            data = response.json()
            if data.get('valid', False):
                mt.addUIMessage(f"Email válido: {data.get('domain')}")
                # Encadenar Bing Search con el domain del email
                params['q'] = f"site:{data['domain']} {person_name}"
                response = requests.get(bing_url, headers=headers, params=params)
                data = response.json()
                if 'webPages' in data:
                    for result in data['webPages']['value']:
                        mt.addEntity("maltego.URL", result['url'])
            else:
                mt.addUIMessage("Email inválido o fraudulento.")
        except Exception as e:
            mt.addUIMessage(f"Error en IPQualityScore: {str(e)}")
    
    mt.returnOutput()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        person_name = sys.argv[1]
        email = sys.argv[2] if len(sys.argv) > 2 else None
        digital_presence(person_name, email)
    else:
        print("Uso: python person_digital_presence.py <nombre_persona> [email_opcional]")