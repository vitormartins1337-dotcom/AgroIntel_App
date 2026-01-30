# ARQUIVO: calc_engine.py
# FUNÇÃO: Motor de Cálculos Físicos e Conectividade API
# VERSÃO: 2.0 (Physics & Network Core)

import math
import requests
import pandas as pd
from datetime import datetime

class AgroPhysics:
    """
    Motor de Física Ambiental.
    Realiza cálculos termodinâmicos para agricultura de precisão.
    """
    
    @staticmethod
    def calc_saturation_vapor_pressure(temp_c: float) -> float:
        """Calcula Es (Pressão de Saturação de Vapor) em kPa (Tetens)."""
        return 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

    @staticmethod
    def calc_vpd(temp_c: float, humidity: float) -> float:
        """
        Calcula o VPD (Déficit de Pressão de Vapor) em kPa.
        Vital para entender a taxa de transpiração da planta.
        """
        es = AgroPhysics.calc_saturation_vapor_pressure(temp_c)
        ea = es * (humidity / 100.0) # Pressão atual
        return round(es - ea, 2)

    @staticmethod
    def calc_delta_t(temp_c: float, humidity: float) -> float:
        """
        Calcula o Delta T (Diferença entre Bulbo Seco e Úmido).
        Crucial para pulverização agrícola.
        """
        # Fórmula de Stull (aproximação robusta para Bulbo Úmido)
        atan = math.atan
        rh = humidity
        t = temp_c
        
        tw = t * atan(0.151977 * (rh + 8.313659)**0.5) + \
             atan(t + rh) - atan(rh - 1.676331) + \
             0.00391838 * (rh)**1.5 * atan(0.023101 * rh) - 4.686035
             
        return round(t - tw, 1)

    @staticmethod
    def calc_etc(temp_c: float, kc: float) -> float:
        """
        Estima a Evapotranspiração da Cultura (ETc) em mm/dia.
        Usa método simplificado para trópicos (baseado em temperatura e radiação média).
        """
        # Estimativa de Radiação (Ra) média para zonas tropicais ~ 25 MJ/m2/dia
        # Adaptação do método Hargreaves-Samani
        et0 = 0.0023 * (temp_c + 17.8) * (temp_c ** 0.5) * 0.408 * 23.0 
        return round(et0 * kc, 2)

    @staticmethod
    def calc_gda(temp_avg: float, t_base: float) -> float:
        """Calcula Graus-Dia Acumulados (GDA) diário."""
        return max(0, temp_avg - t_base)


class WeatherConn:
    """
    Gerenciador de Conexões Externas (APIs).
    Trata erros de rede e formata dados brutos.
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

    @staticmethod
    def get_coords(city_name: str, api_key: str):
        """Converte Nome da Cidade -> Latitude/Longitude."""
        try:
            url = f"{WeatherConn.GEO_URL}?q={city_name}&limit=1&appid={api_key}"
            response = requests.get(url, timeout=5)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            return None, None
        except Exception as e:
            print(f"Erro Geocoding: {e}")
            return None, None

    @staticmethod
    def get_forecast_dataframe(api_key: str, lat: float, lon: float, kc: float, t_base: float):
        """
        Busca previsão de 5 dias (3h/3h) e processa todos os cálculos agronômicos.
        Retorna: Pandas DataFrame pronto para gráficos.
        """
        try:
            url = f"{WeatherConn.BASE_URL}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
            response = requests.get(url, timeout=5)
            raw_data = response.json()
            
            processed_data = []
            
            # A API retorna 40 pontos (5 dias * 8 blocos de 3h)
            # Vamos pegar um ponto a cada 24h (aprox índice 0, 8, 16...) para simplificar o gráfico diário
            # Ou pegar todos e fazer média. Aqui pegaremos os pontos do meio-dia para representar o pico.
            
            for i in range(0, 40, 8):
                # Tenta pegar o bloco mais próximo do meio dia ou apenas o índice sequencial
                item = raw_data['list'][i]
                
                t_mean = item['main']['temp']
                humid = item['main']['humidity']
                
                # Cálculos Físicos
                vpd = AgroPhysics.calc_vpd(t_mean, humid)
                delta_t = AgroPhysics.calc_delta_t(t_mean, humid)
                etc = AgroPhysics.calc_etc(t_mean, kc)
                gda = AgroPhysics.calc_gda(t_mean, t_base)
                
                # Chuva acumulada nas próximas 24h (somando 8 blocos)
                chuva_acc = 0
                for j in range(8):
                    if i + j < len(raw_data['list']):
                        chuva_part = raw_data['list'][i+j].get('rain', {}).get('3h', 0)
                        chuva_acc += chuva_part

                processed_data.append({
                    'Data': datetime.fromtimestamp(item['dt']).strftime('%d/%m'),
                    'Temp': t_mean,
                    'Umid': humid,
                    'VPD': vpd,
                    'Delta T': delta_t,
                    'ETc': etc,
                    'GDA': gda,
                    'Chuva': round(chuva_acc, 1)
                })
                
            return pd.DataFrame(processed_data)
            
        except Exception as e:
            print(f"Erro Forecast: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_radar_simulation(api_key: str, lat: float, lon: float):
        """
        Simula um Radar Meteorológico buscando dados reais de 4 pontos cardeais
        a 15km de distância do ponto central.
        """
        # Deslocamento aproximado de 15km em graus lat/lon
        offset = 0.15 
        
        points = {
            "Norte (15km)": (lat + offset, lon),
            "Sul (15km)": (lat - offset, lon),
            "Leste (15km)": (lat, lon + offset),
            "Oeste (15km)": (lat, lon - offset)
        }
        
        radar_results = []
        
        for direction, (p_lat, p_lon) in points.items():
            try:
                url = f"{WeatherConn.BASE_URL}/weather?lat={p_lat}&lon={p_lon}&appid={api_key}&units=metric&lang=pt_br"
                r = requests.get(url, timeout=3).json()
                
                # Detecção de chuva na string de descrição ou volume
                is_raining = "rain" in r or "chuva" in r['weather'][0]['description'].lower()
                
                radar_results.append({
                    "Direcao": direction,
                    "Temp": r['main']['temp'],
                    "Condicao": r['weather'][0]['description'].title(),
                    "Chuva": "Sim" if is_raining else "Não"
                })
            except:
                continue
                
        return pd.DataFrame(radar_results)
