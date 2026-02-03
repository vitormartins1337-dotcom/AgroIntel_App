# ARQUIVO: market_engine.py
# VERSÃO: V-MASTER (Anti-Falha + Conversão Precisa)

import yfinance as yf
import streamlit as st
import pandas as pd

class MarketData:
    @staticmethod
    @st.cache_data(ttl=600) # Atualiza a cada 10 min
    def get_ticker_real():
        tickers = ["BRL=X", "KC=F", "ZS=F", "ZC=F"]
        texto_ticker = " 📊 <b>MERCADO HOJE:</b> "
        
        try:
            # Baixa dados (threads=False evita erros em nuvem)
            df = yf.download(tickers, period="5d", progress=False)['Close']
            
            # TÉCNICA ANTI-NAN: Preenche vazios com o valor do dia anterior
            df = df.ffill().bfill() 

            # 1. DÓLAR (USD)
            usd = float(df['BRL=X'].iloc[-1])
            usd_ant = float(df['BRL=X'].iloc[-2])
            var_usd = ((usd - usd_ant) / usd_ant) * 100
            cor_usd = "#ef4444" if var_usd < 0 else "#10b981"
            
            texto_ticker += f"💵 <b>DÓLAR:</b> R$ {usd:.3f} <span style='color:{cor_usd}'>({var_usd:+.2f}%)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 2. SOJA (CBOT) -> Convertendo para R$/Saca 60kg
            # Fórmula: (Cents/Bushel / 100) * Dólar * 2.20462 (Bushels/Saca)
            soja_cents = float(df['ZS=F'].iloc[-1])
            soja_brl = (soja_cents / 100) * usd * 2.20462
            
            # Variação baseada no contrato original (Cents)
            var_soja = ((soja_cents - float(df['ZS=F'].iloc[-2])) / float(df['ZS=F'].iloc[-2])) * 100
            cor_soja = "#10b981" if var_soja > 0 else "#ef4444"
            icon_soja = "▲" if var_soja > 0 else "▼"

            texto_ticker += f"🌱 <b>SOJA:</b> R$ {soja_brl:.2f} <span style='color:{cor_soja}'>{icon_soja} {var_soja:+.2f}%</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 3. MILHO (CBOT) -> Convertendo para R$/Saca 60kg
            milho_cents = float(df['ZC=F'].iloc[-1])
            milho_brl = (milho_cents / 100) * usd * 2.20462
            var_milho = ((milho_cents - float(df['ZC=F'].iloc[-2])) / float(df['ZC=F'].iloc[-2])) * 100
            cor_milho = "#10b981" if var_milho > 0 else "#ef4444"
            icon_milho = "▲" if var_milho > 0 else "▼"

            texto_ticker += f"🌽 <b>MILHO:</b> R$ {milho_brl:.2f} <span style='color:{cor_milho}'>{icon_milho} {var_milho:+.2f}%</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 4. CAFÉ (NY) -> Convertendo para R$/Saca 60kg
            # Fórmula: (Cents/Lb / 100) * Dólar * 132.277 (Lbs/Saca)
            cafe_cents = float(df['KC=F'].iloc[-1])
            cafe_brl = (cafe_cents / 100) * usd * 132.277
            var_cafe = ((cafe_cents - float(df['KC=F'].iloc[-2])) / float(df['KC=F'].iloc[-2])) * 100
            cor_cafe = "#10b981" if var_cafe > 0 else "#ef4444"
            icon_cafe = "▲" if var_cafe > 0 else "▼"

            texto_ticker += f"☕ <b>CAFÉ:</b> R$ {cafe_brl:.2f} <span style='color:{cor_cafe}'>{icon_cafe} {var_cafe:+.2f}%</span>"

        except Exception as e:
            return f"⚠️ <b>MERCADO:</b> Sincronizando dados globais... (Atualize a página em instantes)"
            
        return texto_ticker
