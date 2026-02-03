# ARQUIVO: styles.py
# VERSÃO: V-MASTER-GOLD (Trava de Quebra de Linha + Animação Pulse)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. CONFIGURAÇÃO GERAL (Remove espaços desnecessários) */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 3rem !important;
                max-width: 100% !important;
            }
            header[data-testid="stHeader"] { display: none; }

            /* 2. O HEADER PREMIUM (CAPA) */
            .header-wrapper {
                background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
                padding: 20px 15px;
                color: white;
                border-radius: 0px; /* Reto embaixo para colar no ticker */
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                position: relative;
                z-index: 10; /* Fica acima do ticker */
            }

            .brand-main {
                font-family: 'Helvetica Neue', sans-serif;
                font-weight: 900;
                font-size: 1.8rem;
                line-height: 1;
                letter-spacing: -1px;
                margin: 0;
            }

            .brand-sub {
                font-family: 'Segoe UI', sans-serif;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 2px;
                opacity: 0.85;
                margin-top: 4px;
                font-weight: 600;
            }

            /* 3. O STATUS "ONLINE" (CORREÇÃO DA QUEBRA DE LINHA) */
            .status-badge {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 6px 12px;
                border-radius: 30px;
                font-size: 0.7rem;
                font-weight: 800;
                color: #d1fae5;
                
                /* O SEGREDO DO PADRÃO OURO: */
                white-space: nowrap; /* Proíbe quebrar linha */
                display: flex;
                align-items: center;
                gap: 6px;
            }

            /* Animação da Bolinha (Pulso) */
            @keyframes pulse-green {
                0% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }
                70% { box-shadow: 0 0 0 6px rgba(74, 222, 128, 0); }
                100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: #4ade80; /* Verde neon */
                border-radius: 50%;
                display: inline-block;
                animation: pulse-green 2s infinite;
            }

            /* 4. O TICKER (LETREIRO) INTEGRADO */
            .ticker-container {
                background-color: #0f172a; /* Preto azulado premium */
                width: 100%;
                overflow: hidden;
                white-space: nowrap;
                height: 40px;
                display: flex;
                align-items: center;
                margin-bottom: 25px; /* Espaço para o conteúdo de baixo */
                border-bottom: 4px solid #10b981; /* Linha de acabamento */
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }
            
            .ticker-text {
                display: inline-block;
                color: #e2e8f0;
                font-family: 'Consolas', 'Monaco', monospace; /* Fonte técnica */
                font-size: 0.85rem;
                animation: marquee 45s linear infinite; /* Mais lento e suave */
                padding-left: 100%; /* Começa fora da tela */
            }

            @keyframes marquee {
                0% { transform: translateX(0); }
                100% { transform: translateX(-100%); }
            }

            /* 5. CARTÕES E INTERFACE GERAL */
            .app-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #f1f5f9;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                margin-bottom: 15px;
                transition: transform 0.2s;
            }
            .app-card:active { transform: scale(0.99); } /* Efeito de toque no celular */

            /* Abas Limpas */
            .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #e2e8f0; gap: 5px; }
            .stTabs [data-baseweb="tab"] { border-radius: 6px; border: none; background: #f8fafc; font-size: 0.8rem; }
            .stTabs [aria-selected="true"] { background-color: #064e3b !important; color: white !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
