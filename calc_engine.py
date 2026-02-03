# ARQUIVO: calc_engine.py
# VERSÃO: V-24H (Com suporte a previsão horária detalhada)

import requests
import pandas as pd
import math
from datetime import datetime

class AgroPhysics:
    @staticmethod
    def calc_eto(temp_media, lat):
        # Fórmula simplificada de Hargreaves-Samani para estimativa rápida
        # Ra: Radiação extraterrestre (estimada pela latitude e dia do ano)
        # Na prática, usamos temperatura como proxy de energia
        try:
            eto = 0.0023 * (temp_media + 17.8) * (temp_media ** 0.5) * 0.408 * 23 # Fator de ajuste
            return max(0.0, round(eto, 2))
        except:
            return 3.5 # Valor médio de fallback

    @staticmethod
    def calc_delta_t(temp, umid):
        # Delta T = Temperatura Seca - Temperatura Úmida
        # Aproximação prática para decisões de campo
        try:
            bulb_umido = temp * math.atan(0.151977 * (umid + 8.313659)**0.5) + math.atan(temp + umid) - math.atan(umid - 1.676331) + 0.00391838 * (umid)**1.5 * math.atan(0.023101 * umid) - 4.686035
            return round(temp - bulb_umido, 1)
        except:
            return 0.0

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
        # Previsão Diária (Resumo)
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
                        "Temp": t_avg,
                        "Umid": umid,
                        "Chuva": chuva,
                        "ETc": round(etc, 2),
                        "GDA": round(gda, 1),
                        "Delta T": delta_t
                    }
            
            return pd.DataFrame(list(lista_dias.values()))
        except:
            return pd.DataFrame()

    @staticmethod
    def get_hourly_forecast(api_key, lat, lon):
        """
        NOVA FUNÇÃO: Pega a previsão detalhada das próximas 24 horas (blocos de 3h).
        Fundamental para ver a variação ao longo do dia.
        """
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
            r = requests.get(url).json()
            
            hourly_data = []
            
            # Pegamos os primeiros 8 itens (8 * 3h = 24 horas)
            for item in r['list'][:9]:
                hora = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                dia = datetime.fromtimestamp(item['dt']).strftime('%d/%m')
                temp = item['main']['temp']
                umid = item['main']['humidity']
                chuva = item.get('rain', {}).get('3h', 0)
                vento = item['wind']['speed'] * 3.6 # Convertendo m/s para km/h
                desc = item['weather'][0]['description']
                
                # Cálculo Agro
                delta_t = AgroPhysics.calc_delta_t(temp, umid)
                
                hourly_data.append({
                    "Hora": f"{dia} {hora}",
                    "HoraSimples": hora,
                    "Temp": temp,
                    "Chuva": chuva,
                    "Umid": umid,
                    "Delta T": delta_t,
                    "Vento": round(vento, 1),
                    "Desc": desc.title()
                })
                
            return pd.DataFrame(hourly_data)
        except Exception as e:
            return pd.DataFrame() # Retorna vazio se der erro
