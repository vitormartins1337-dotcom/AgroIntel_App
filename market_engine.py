# ARQUIVO: market_engine.py
# VERSÃO: V-FINAL-FIX (Correção Anti-NaN para Café)

import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

class MarketData:
    @staticmethod
    @st.cache_data(ttl=600) # Cache de 10 minutos
    def get_ticker_real():
        # TICKERS:
        # BRL=X: Dólar
        # KC=F: Café Arábica (NY)
        # ZS=F: Soja (Chicago)
        # ZC=F: Milho (Chicago)
        tickers = ["BRL=X", "KC=F", "ZS=F", "ZC=F"]
        
        texto_ticker = " 📊 <b>MERCADO HOJE:</b> "
        
        try:
            # Baixa 1 mês de dados para garantir que não falte histórico (evita NaN)
            df = yf.download(tickers, period="1mo", progress=False)['Close']
            
            # TÉCNICA DE CURA DE DADOS (Preenche buracos com dia anterior)
            df = df.ffill().bfill()
            
            # --- 1. DÓLAR ---
            try:
                usd = float(df['BRL=X'].iloc[-1])
                usd_ant = float(df['BRL=X'].iloc[-2])
                var_usd = ((usd - usd_ant) / usd_ant) * 100
                cor_usd = "#ef4444" if var_usd < 0 else "#10b981"
                texto_ticker += f"💵 <b>DÓLAR:</b> R$ {usd:.3f} <span style='color:{cor_usd}'>({var_usd:+.2f}%)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
            except:
                usd = 5.80 # Fallback de segurança
                texto_ticker += f"💵 <b>DÓLAR:</b> R$ {usd:.3f} &nbsp;&nbsp;|&nbsp;&nbsp; "

            # --- 2. SOJA (Chicago -> Saca 60kg) ---
            try:
                soja_cents = float(df['ZS=F'].iloc[-1])
                if np.isnan(soja_cents): raise ValueError("NaN")
                
                soja_brl = (soja_cents / 100) * usd * 2.20462
                var_soja = ((soja_cents - float(df['ZS=F'].iloc[-2])) / float(df['ZS=F'].iloc[-2])) * 100
                cor_soja = "#10b981" if var_soja > 0 else "#ef4444"
                icon_soja = "▲" if var_soja > 0 else "▼"
                texto_ticker += f"🌱 <b>SOJA:</b> R$ {soja_brl:.2f} <span style='color:{cor_soja}'>{icon_soja} {var_soja:+.2f}%</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
            except:
                texto_ticker += "🌱 <b>SOJA:</b> -- &nbsp;&nbsp;|&nbsp;&nbsp; "

            # --- 3. MILHO (Chicago -> Saca 60kg) ---
            try:
                milho_cents = float(df['ZC=F'].iloc[-1])
                if np.isnan(milho_cents): raise ValueError("NaN")
                
                milho_brl = (milho_cents / 100) * usd * 2.20462
                var_milho = ((milho_cents - float(df['ZC=F'].iloc[-2])) / float(df['ZC=F'].iloc[-2])) * 100
                cor_milho = "#10b981" if var_milho > 0 else "#ef4444"
                icon_milho = "▲" if var_milho > 0 else "▼"
                texto_ticker += f"🌽 <b>MILHO:</b> R$ {milho_brl:.2f} <span style='color:{cor_milho}'>{icon_milho} {var_milho:+.2f}%</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
            except:
                texto_ticker += "🌽 <b>MILHO:</b> -- &nbsp;&nbsp;|&nbsp;&nbsp; "

            # --- 4. CAFÉ ARÁBICA (NY -> Saca 60kg) ---
            # Aqui estava o problema: KC=F às vezes falha.
            try:
                cafe_cents = float(df['KC=F'].iloc[-1])
                
                # SE O CAFÉ FOR NaN (Inválido), forçamos um erro para ir pro 'except'
                if np.isnan(cafe_cents): raise ValueError("Dados de Café Inválidos")

                # Cálculo: (Cents/Lb / 100) * Dólar * 132.277 (Lbs/Saca)
                cafe_brl = (cafe_cents / 100) * usd * 132.277
                
                var_cafe = ((cafe_cents - float(df['KC=F'].iloc[-2])) / float(df['KC=F'].iloc[-2])) * 100
                cor_cafe = "#10b981" if var_cafe > 0 else "#ef4444"
                icon_cafe = "▲" if var_cafe > 0 else "▼"
                texto_ticker += f"☕ <b>CAFÉ:</b> R$ {cafe_brl:.2f} <span style='color:{cor_cafe}'>{icon_cafe} {var_cafe:+.2f}%</span>"
            
            except:
                # FALLBACK INTELIGENTE: Se der erro, mostra o último valor conhecido ou aviso
                # Tenta pegar o penúltimo valor se o último for NaN
                try:
                    cafe_safe = float(df['KC=F'].iloc[-2])
                    cafe_brl = (cafe_safe / 100) * usd * 132.277
                    texto_ticker += f"☕ <b>CAFÉ:</b> R$ {cafe_brl:.2f} (Est.)"
                except:
                     texto_ticker += f"☕ <b>CAFÉ:</b> R$ -- (Mercado Fechado)"

        except Exception as e:
            return "⚠️ <b>SISTEMA FINANCEIRO:</b> Sincronizando dados... Aguarde."
            
        return texto_ticker
