# ARQUIVO: styles.py
# VERSÃO: V-GOLD-RESTORATION (Design Premium + Hover Effects)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. AJUSTE FINO DO TOPO (Remove excesso de branco sem quebrar) */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 2rem !important;
                max-width: 100% !important;
            }
            
            /* Remove o Header padrão do Streamlit */
            header[data-testid="stHeader"] { display: none; }

            /* 2. O DESIGN DOS CARTÕES (ESTILO "APPLE") */
            /* Isso traz de volta o efeito de elevação e sombra bonita */
            .app-card {
                background-color: #ffffff;
                padding: 25px;
                border-radius: 12px; /* Cantos mais arredondados */
                border: 1px solid #f1f5f9;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Animação suave */
                margin-bottom: 20px;
            }
            
            /* O Efeito Mágico: Eleva quando passa o mouse/dedo */
            .app-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                border-color: #10b981; /* Borda verde suave ao focar */
            }

            /* 3. CABEÇALHO E TICKER (Integrados) */
            .header-wrapper {
                margin-bottom: 20px;
                border-radius: 0 0 15px 15px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            /* 4. ABAS (TABS) - VOLTANDO AO ORIGINAL BONITO */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 5px;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 45px;
                border-radius: 8px;
                background-color: white;
                border: 1px solid #e2e8f0;
                padding: 0 20px;
                font-weight: 600;
                color: #64748b;
                transition: all 0.2s;
            }

            .stTabs [aria-selected="true"] {
                background-color: #064e3b !important; /* Verde Agro Escuro */
                color: white !important;
                border: none;
                box-shadow: 0 4px 6px rgba(6, 78, 59, 0.2);
            }

            /* 5. KPI BOXES (Indicadores Coloridos) */
            .kpi-box {
                background: linear-gradient(to bottom right, #ffffff, #f8fafc);
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                text-align: center;
                padding: 0;
                overflow: hidden;
                transition: transform 0.2s;
            }
            .kpi-box:hover { transform: scale(1.03); } /* Leve zoom */
            
            .kpi-header { 
                background: #f1f5f9; 
                padding: 8px; 
                font-size: 0.75rem; 
                font-weight: 700; 
                color: #475569; 
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            .kpi-value { 
                padding: 15px 0; 
                font-size: 1.6rem; 
                font-weight: 800; 
                color: #0f172a; 
            }
            .kpi-footer { 
                color: white; 
                padding: 6px; 
                font-size: 0.7rem; 
                font-weight: 700; 
                letter-spacing: 0.5px;
            }

            /* 6. TICKER ANIMATION */
            .ticker-wrap {
                width: 100%;
                overflow: hidden;
                background-color: #1e293b; /* Azul noturno elegante */
                color: #f1f5f9;
                height: 40px;
                display: flex;
                align-items: center;
            }
            .ticker-move {
                display: inline-block;
                white-space: nowrap;
                padding-right: 100%;
                animation: ticker 40s linear infinite;
            }
            .ticker-item {
                display: inline-block;
                padding: 0 2rem;
                font-family: 'Segoe UI', sans-serif;
                font-size: 0.9rem;
            }
            @keyframes ticker {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }

        </style>
    """, unsafe_allow_html=True)
