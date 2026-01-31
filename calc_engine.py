# ARQUIVO: calc_engine.py
import math
import requests
import pandas as pd
from datetime import datetime

class AgroPhysics:
    @staticmethod
    def calc_vpd(temp, umid):
        # Pressão de saturação (Tetens)
        es = 0.61078 * math.exp((17.27 * temp) / (temp + 237.3))
        # Pressão atual
        ea = es * (umid / 100.0)
        return round(es - ea, 2)

    @staticmethod
    def calc_delta_t(temp, umid):
        # Aproximação de Bulbo Úmido (Stull)
        atan = math.atan
        rh = umid
        t = temp
        tw = t * atan(0.151977 * (rh + 8.313659)**0.5) + atan(t + rh) - atan(rh - 1.676331) + 0.00391838 * (rh)**1.5 * atan(0.023101 * rh) - 4.686035
        return round(t - tw, 1)

    @staticmethod
    def calc_etc(temp, kc):
        # Hargreaves-Samani adaptado (Radiação fixa ~23MJ)
        et0 = 0.0023 * (temp + 17.8) * (temp ** 0.5) * 0.408 * 23.0
        return round(et0 * kc, 2)

class WeatherConn:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    @staticmethod
    def get_coords(city_name, api_key):
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
            r = requests.get(url, timeout=3).json()
            if r: return r[0]['lat'], r[0]['lon']
            return None, None
        except: return None, None

    @staticmethod
    def get_forecast_dataframe(api_key, lat, lon, kc, t_base):
        try:
            url = f"{WeatherConn.BASE_URL}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
            r = requests.get(url, timeout=3).json()
            
            data = []
            # Pega um ponto a cada 24h (indices 0, 8, 16...) para simplicidade visual no gráfico
            for i in range(0, 40, 8):
                if i < len(r['list']):
                    item = r['list'][i]
                    t = item['main']['temp']
                    h = item['main']['humidity']
                    
                    data.append({
                        'Data': datetime.fromtimestamp(item['dt']).strftime('%d/%m'),
                        'Temp': t,
                        'Umid': h,
                        'VPD': AgroPhysics.calc_vpd(t, h),
                        'Delta T': AgroPhysics.calc_delta_t(t, h),
                        'ETc': AgroPhysics.calc_etc(t, kc),
                        'GDA': max(0, t - t_base),
                        # Soma chuva das próximas 24h (8 blocos de 3h)
                        'Chuva': sum([r['list'][x].get('rain', {}).get('3h', 0) for x in range(i, min(i+8, len(r['list'])))])
                    })
            return pd.DataFrame(data)
        except: return pd.DataFrame()

    @staticmethod
    def get_radar_simulation(api_key, lat, lon):
        try:
            # Simulação de pontos cardeais
            points = {"Norte": (lat+0.1, lon), "Sul": (lat-0.1, lon), "Leste": (lat, lon+0.1), "Oeste": (lat, lon-0.1)}
            res = []
            for d, p in points.items():
                r = requests.get(f"{WeatherConn.BASE_URL}/weather?lat={p[0]}&lon={p[1]}&appid={api_key}&units=metric", timeout=2).json()
                is_raining = "rain" in r or "chuva" in r['weather'][0]['description']
                res.append({"Direcao": d, "Temp": r['main']['temp'], "Chuva": "Sim" if is_raining else "Não"})
            return pd.DataFrame(res)
        except: return pd.DataFrame()
