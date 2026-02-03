# ARQUIVO: styles.py
# VERSÃO: V-MASTER (Zero Gap + Layout Fluido)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. REMOÇÃO CIRÚRGICA DA BARRA BRANCA SUPERIOR */
            .block-container {
                padding-top: 0rem !important; /* Zera o topo */
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                max-width: 100% !important;
            }
            
            /* Remove o Header padrão do Streamlit (Hambúrguer) para limpar a vista */
            header[data-testid="stHeader"] {
                display: none;
            }

            /* 2. HEADER PERSONALIZADO (CAPA) */
            .custom-header {
                background: linear-gradient(90deg, #064e3b 0%, #065f46 100%);
                padding: 20px 15px;
                color: white;
                border-bottom: 4px solid #047857;
            }
            
            .brand-main {
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 2rem;
                font-weight: 900;
                margin: 0;
                line-height: 1;
                letter-spacing: -1px;
            }
            
            .brand-sub {
                font-family: monospace;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 2px;
                opacity: 0.8;
                margin-top: 5px;
            }

            /* 3. TICKER (Letreiro) - Cola no Header sem espaço */
            .ticker-container {
                background-color: #0f172a;
                width: 100%;
                overflow: hidden;
                white-space: nowrap;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
                margin-bottom: 20px; /* Espaço só DEPOIS do ticker */
            }
            
            .ticker-text {
                display: inline-block;
                padding: 8px 0;
                color: #e2e8f0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 0.9rem;
                animation: marquee 35s linear infinite;
            }
            
            @keyframes marquee {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }

            /* 4. CARDS E CONTEÚDO */
            .app-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                margin-bottom: 15px;
            }
            
            /* Ajuste fino para Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: white;
                border-bottom: 1px solid #e2e8f0;
            }
            .stTabs [aria-selected="true"] {
                background-color: #064e3b !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
