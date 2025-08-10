#################################################
# Transform personalizada para Maltego en Python.
# Enriquece una entidad tipo "Domain" en Maltego con datos WHOIS obtenidos de la API de WhoisXML.
#################################################

import sys
import requests
import json
import os
from MaltegoTransform import *

def whois_lookup(domain):
    mt = MaltegoTransform()
    
    # Cargar API key desde config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')  # Ruta relativa al script
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            api_key = config.get('api_key')
            if not api_key:
                raise ValueError("API key no encontrada en config.json")
    except Exception as e:
        mt.addUIMessage(f"Error al cargar config.json: {str(e)}")
        mt.returnOutput()
        return  # Salir temprano si falla la config
    
    url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'WhoisRecord' in data:
            whois = data['WhoisRecord']
            # Entidad para registrante
            person = mt.addEntity("maltego.Person", whois.get('registrant', {}).get('name', "Desconocido"))
            person.addProperty("organization", "Organización", "loose", whois.get('registrant', {}).get('organization', ""))
            
            # Entidad para email
            email = mt.addEntity("maltego.EmailAddress", whois.get('registrant', {}).get('email', "Desconocido"))
            
            # Entidades para servidores de nombres
            for ns in whois.get('nameServers', {}).get('hostNames', []):
                mt.addEntity("maltego.NSRecord", ns)
                
        else:
            mt.addUIMessage("No se encontraron datos WHOIS para el dominio.")
            
    except Exception as e:
        mt.addUIMessage(f"Error: {str(e)}")
        
    mt.returnOutput()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        domain = sys.argv[1]
        whois_lookup(domain)
    else:
        print("Uso: python whois_transform.py <dominio>")