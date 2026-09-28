from geopy.geocoders import Nominatim

# Inicializa o buscador com o agente obrigatório do OpenStreetMap
geolocator = Nominatim(user_agent="meu_localizador_cg")

# Faz a busca por Campina Grande
localizacao = geolocator.geocode("Campina Grande, Paraiba")

if localizacao:
    print(f"Endereço Oficial: {localizacao.address}")
    print(f"Latitude: {localizacao.latitude}")
    print(f"Longitude: {localizacao.longitude}")
else:
    print("Local não encontrado.")
