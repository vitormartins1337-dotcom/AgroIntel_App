# ARQUIVO: market_engine.py
# VERSÃO: V-BRL (Conversão Automática para Reais/Saca)

import yfinance as yf
import streamlit as st

class MarketData:
    @staticmethod
    @st.cache_data(ttl=900) # Atualiza a cada 15 min
    def get_ticker_real():
        """
        Busca dados em Dólar e converte para o Padrão Brasileiro (Reais por Saca).
        """
        # TICKERS
        # BRL=X: Dólar
        # KC=F: Café Arábica (NY) - Cents/lb
        # ZS=F: Soja (Chicago) - Cents/Bushel
        # ZC=F: Milho (Chicago) - Cents/Bushel
        
        tickers = ["BRL=X", "KC=F", "ZS=F", "ZC=F"]
        
        texto_ticker = " 📊 <b>MERCADO AGRO (REF. EXPORTAÇÃO):</b> "
        
        try:
            # Baixa tudo de uma vez
            dados = yf.download(tickers, period="2d", progress=False)
            
            # 1. DÓLAR (USD)
            # Pega o fechamento mais recente
            usd_price = float(dados['Close']['BRL=X'].iloc[-1])
            usd_delta = (usd_price - float(dados['Close']['BRL=X'].iloc[-2])) / float(dados['Close']['BRL=X'].iloc[-2]) * 100
            cor_usd = "#ef4444" if usd_delta < 0 else "#10b981" # Dólar caindo é vermelho (bom pra insumo, ruim pra venda)
            
            texto_ticker += f"💵 <b>DÓLAR:</b> R$ {usd_price:.2f} <span style='color:{cor_usd}'>({usd_delta:+.2f}%)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 2. CAFÉ ARÁBICA (NY -> BRL/SACA)
            # Fator: Preço (Cents) / 100 * 132.276 (Libras na saca) * Dólar
            cafe_cents = float(dados['Close']['KC=F'].iloc[-1])
            cafe_brl = (cafe_cents / 100) * 132.276 * usd_price
            cafe_delta = (cafe_cents - float(dados['Close']['KC=F'].iloc[-2])) / float(dados['Close']['KC=F'].iloc[-2]) * 100
            cor_cafe = "#10b981" if cafe_delta > 0 else "#ef4444"
            
            texto_ticker += f"☕ <b>CAFÉ (Saca 60kg):</b> R$ {cafe_brl:.2f} <span style='color:{cor_cafe}'>({cafe_delta:+.2f}%)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 3. SOJA (CBOT -> BRL/SACA)
            # Fator: Preço (Cents) / 100 * 2.20462 (Bushels na saca de 60kg) * Dólar
            soja_cents = float(dados['Close']['ZS=F'].iloc[-1])
            soja_brl = (soja_cents / 100) * 2.20462 * usd_price
            soja_delta = (soja_cents - float(dados['Close']['ZS=F'].iloc[-2])) / float(dados['Close']['ZS=F'].iloc[-2]) * 100
            cor_soja = "#10b981" if soja_delta > 0 else "#ef4444"

            texto_ticker += f"🌱 <b>SOJA (Saca 60kg):</b> R$ {soja_brl:.2f} <span style='color:{cor_soja}'>({soja_delta:+.2f}%)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "

            # 4. MILHO (CBOT -> BRL/SACA)
            milho_cents = float(dados['Close']['ZC=F'].iloc[-1])
            milho_brl = (milho_cents / 100) * 2.20462 * usd_price
            milho_delta = (milho_cents - float(dados['Close']['ZC=F'].iloc[-2])) / float(dados['Close']['ZC=F'].iloc[-2]) * 100
            cor_milho = "#10b981" if milho_delta > 0 else "#ef4444"

            texto_ticker += f"🌽 <b>MILHO (Saca 60kg):</b> R$ {milho_brl:.2f} <span style='color:{cor_milho}'>({milho_delta:+.2f}%)</span>"

        except Exception as e:
            return f"⚠️ <b>SISTEMA DE MERCADO:</b> Conectando à Bolsa (B3/CBOT)... Aguarde. ({str(e)})"
            
        return texto_ticker
