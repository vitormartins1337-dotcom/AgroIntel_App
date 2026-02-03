# ARQUIVO: market_engine.py
# FUNÇÃO: Buscar cotações reais (B3/Chicago) via Yahoo Finance

import yfinance as yf
import streamlit as st

class MarketData:
    @staticmethod
    @st.cache_data(ttl=1800) # Atualiza a cada 30 min (Cache)
    def get_ticker_real():
        """
        Busca dados reais de Commodities e Moedas.
        """
        # TICKERS (Símbolos de Mercado):
        # BRL=X: Dólar vs Real
        # ZS=F: Soja Futuro (Chicago) - Convertido para Bushel
        # KC=F: Café Arábica (Nova York)
        # ZC=F: Milho Futuro (Chicago)
        
        tickers = {
            "💵 USD": "BRL=X",
            "🌱 SOJA (CBOT)": "ZS=F",
            "🌽 MILHO (CBOT)": "ZC=F",
            "☕ CAFÉ (NY)": "KC=F"
        }
        
        texto_ticker = ""
        
        try:
            dados = yf.download(list(tickers.values()), period="1d", progress=False)['Close']
            
            # Pega o último preço disponível (iloc[-1])
            for nome, simbolo in tickers.items():
                try:
                    # Tenta pegar o valor. Se for DataFrame com multiplas colunas ou Series
                    valor = dados[simbolo].iloc[-1]
                    
                    # Formatação específica
                    if "USD" in nome:
                        formatado = f"R$ {valor:.2f}"
                    else:
                        # Commodities internacionais geralmente são em US cents/bushel ou lb
                        # Aqui mostramos o valor bruto do contrato futuro
                        formatado = f"US$ {valor:.2f}"
                        
                    texto_ticker += f"&nbsp;&nbsp;&nbsp;&nbsp; <b>{nome}:</b> {formatado} &nbsp;&nbsp; |"
                except:
                    continue
                    
        except Exception as e:
            return "⚠️ Mercado Offline ou Erro de Conexão API."
            
        return texto_ticker + "&nbsp;&nbsp;&nbsp;&nbsp; 📍 <b>FONTE:</b> Yahoo Finance (Delay 15min)"
