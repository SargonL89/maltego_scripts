Obtener Bing key: En portal.azure.com, creá recurso "Bing Search v7", copiá la key de "Keys and Endpoint".
IPQualityScore: Registrate en ipqualityscore.com para key gratuita.

Configuración en Maltego: Transforms > New Local Transform Set > Crea set "Digital Presence".

Input: maltego.Person.
Comando: python /ruta/al/script.py %input% %property.email% (para pasar email como propiedad opcional de la entidad Person).

Prueba: En un grafo, creá Person "Elon Musk", agrega propiedad "email" (e.g., un email público ficticio como "elon@tesla.com" para testing), ejecuta la transform. Verás URLs, Aliases y Organizations en el grafo.
Analizá: El grafo mapeará conexiones (e.g., @elonmusk en Twitter a Tesla). Exporta como PDF y guarda como elon_digital.mtz.