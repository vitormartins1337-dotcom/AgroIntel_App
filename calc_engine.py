# ARQUIVO: calc_engine.py
# VERSÃO: V-COMPLETE (Radar Restaurado + 24h + Física)

import requests
import pandas as pd
import math
import random
from datetime import datetime

class AgroPhysics:
    @staticmethod
    def calc_eto(temp_media, lat):
        try:
            eto = 0.0023 * (temp_media + 17.8) * (temp_media ** 0.5) * 0.408 * 23
            return max(0.0, round(eto, 2))
        except: return 3.5

    @staticmethod
    def calc_delta_t(temp, umid):
        try:
            bulb_umido = temp * math.atan(0.151977 * (umid + 8.313659)**0.5) + math.atan(temp + umid) - math.atan(umid - 1.676331) + 0.00391838 * (umid)**1.5 * math.atan(0.023101 * umid) - 4.686035
            return round(temp - bulb_umido, 1)
        except: return 0.0

class WeatherConn:
    @staticmethod
    def get_coords(city_name, api_key):
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
            r = requests.get(url).json()
            if r: return r[0]['lat'], r[0]['lon']
            return None, None
        except: return None, None

    @staticmethod
    def get_forecast_dataframe(api_key, lat, lon, kc=1.0, t_base=10):
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
            data = requests.get(url).json()
            lista_dias = {}
            for item in data['list']:
                dt = datetime.fromtimestamp(item['dt']).date()
                if dt not in lista_dias:
                    t_avg = item['main']['temp']
                    chuva = item.get('rain', {}).get('3h', 0)
                    umid = item['main']['humidity']
                    eto = AgroPhysics.calc_eto(t_avg, lat)
                    etc = eto * kc
                    gda = max(0, t_avg - t_base)
                    delta_t = AgroPhysics.calc_delta_t(t_avg, umid)
                    lista_dias[dt] = {
                        "Data": dt.strftime('%d/%m'),
                        "Temp": t_avg, "Umid": umid, "Chuva": chuva,
                        "ETc": round(etc, 2), "GDA": round(gda, 1), "Delta T": delta_t
                    }
            return pd.DataFrame(list(lista_dias.values()))
        except: return pd.DataFrame()

    @staticmethod
    def get_hourly_forecast(api_key, lat, lon):
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
            r = requests.get(url).json()
            hourly_data = []
            for item in r['list'][:9]: # Próximas 24h (blocos de 3h)
                hora = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                temp = item['main']['temp']
                umid = item['main']['humidity']
                chuva = item.get('rain', {}).get('3h', 0)
                delta_t = AgroPhysics.calc_delta_t(temp, umid)
                hourly_data.append({
                    "HoraSimples": hora, "Temp": temp, "Chuva": chuva, 
                    "Umid": umid, "Delta T": delta_t
                })
            return pd.DataFrame(hourly_data)
        except: return pd.DataFrame()

    @staticmethod
    def get_radar_simulation(api_key, lat, lon):
        """
        Simula dados de estações vizinhas (Norte, Sul, Leste, Oeste)
        para criar o efeito de Radar Meteorológico.
        """
        try:
            # Deslocamentos para simular cidades vizinhas (~20km)
            offsets = [
                ("Norte (Sede)", lat + 0.1, lon),
                ("Sul (Distrito)", lat - 0.1, lon),
                ("Leste (Serra)", lat, lon + 0.1),
                ("Oeste (Baixada)", lat, lon - 0.1)
            ]
            radar_data = []
            
            # Pega dados reais dessas coordenadas deslocadas
            for nome, n_lat, n_lon in offsets:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={n_lat}&lon={n_lon}&appid={api_key}&units=metric"
                r = requests.get(url).json()
                
                # Simula chuva baseado na nuvem/descrição real
                is_raining = "rain" in str(r.get('weather', [{'main':''}])[0]['main']).lower()
                
                radar_data.append({
                    "Direcao": nome,
                    "Temp": r['main']['temp'],
                    "Chuva": "Sim" if is_raining else "Não"
                })
                
            return pd.DataFrame(radar_data)
        except:
            return pd.DataFrame()
