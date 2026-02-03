# ARQUIVO: styles.py
# VERSÃO: V-RESTORATION (Abas Originais + Ticker Animado)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. ANIMAÇÃO DO TICKER (LETREIRO CORRENDO) */
            @keyframes ticker {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            
            .ticker-wrap {
                width: 100%;
                overflow: hidden;
                background-color: #0f172a; /* Fundo Escuro Profissional */
                color: #e2e8f0;
                padding: 10px 0;
                margin-bottom: 20px;
                border-top: 2px solid #10b981;
                border-bottom: 2px solid #10b981;
                white-space: nowrap;
                box-sizing: border-box;
            }
            
            .ticker-move {
                display: inline-block;
                white-space: nowrap;
                padding-right: 100%;
                animation: ticker 30s linear infinite; /* Velocidade da animação */
            }
            
            .ticker-item {
                display: inline-block;
                padding: 0 2rem;
                font-family: 'Courier New', monospace; /* Fonte tipo Bolsa de Valores */
                font-size: 1rem;
            }

            /* 2. ESTILO DOS CARDS (Mantém o visual limpo) */
            .app-card {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border: 1px solid #e5e7eb;
                margin-bottom: 20px;
            }

            /* 3. BRANDING */
            .brand-container { padding: 10px 0; }
            .brand-title {
                font-family: sans-serif;
                font-weight: 800;
                font-size: 2.5rem;
                color: #064e3b;
                margin: 0;
            }
            .brand-accent { color: #10b981; }
            .brand-subtitle {
                font-size: 0.9rem;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 3px;
            }

            /* 4. KPI BOX (Indicadores Coloridos) */
            .kpi-box {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                text-align: center;
                overflow: hidden;
            }
            .kpi-header { background: #f8fafc; padding: 5px; font-size: 0.8rem; font-weight: bold; color: #64748b; }
            .kpi-value { padding: 10px; font-size: 1.5rem; font-weight: bold; color: #1e293b; }
            .kpi-footer { color: white; padding: 5px; font-size: 0.8rem; font-weight: bold; }

            /* CORREÇÃO: NÃO MEXER NAS ABAS (TABS) PARA NÃO DEFORMAR */
            /* O Streamlit padrão já é bonito, vamos deixar ele quieto */

        </style>
    """, unsafe_allow_html=True)
