# ARQUIVO: styles.py
# VERSÃO: V-RESTORATION (Cards Flutuantes + Abas Originais + Ticker Seguro)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. AJUSTES GERAIS (Para o Header colar no topo) */
            .block-container {
                padding-top: 0rem !important; /* Cola no teto */
                padding-bottom: 3rem !important;
                max-width: 100% !important;
            }
            header[data-testid="stHeader"] { display: none; }

            /* 2. O HEADER VERDE (CAPA) */
            .header-wrapper {
                background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
                padding: 20px 20px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                position: relative;
                z-index: 99;
            }

            /* 3. O STATUS ONLINE (CORRIGIDO) */
            .status-badge {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(167, 243, 208, 0.3);
                color: #d1fae5;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 800;
                letter-spacing: 1px;
                display: flex;
                align-items: center;
                gap: 8px;
                white-space: nowrap; /* Trava a quebra de linha */
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: #34d399;
                border-radius: 50%;
                box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
                animation: pulse-green 2s infinite;
            }
            
            @keyframes pulse-green {
                0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
                70% { box-shadow: 0 0 0 6px rgba(52, 211, 153, 0); }
                100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
            }

            /* 4. O TICKER (LETREIRO) - AGORA EMBAIXO DO HEADER */
            .ticker-container {
                background-color: #0f172a;
                width: 100%;
                height: 40px;
                overflow: hidden;
                white-space: nowrap;
                display: flex;
                align-items: center;
                border-bottom: 4px solid #10b981;
                margin-bottom: 25px;
            }
            
            .ticker-text {
                display: inline-block;
                color: #e2e8f0;
                font-family: 'Consolas', monospace;
                font-size: 0.9rem;
                padding-left: 100%;
                animation: marquee 40s linear infinite;
            }
            
            @keyframes marquee {
                0% { transform: translateX(0); }
                100% { transform: translateX(-100%); }
            }

            /* 5. OS CARDS (ESTILO PADRÃO OURO RESTAURADO) */
            /* Esse é o código que faz o efeito "Balãozinho" e Sombra */
            .app-card {
                background-color: white;
                padding: 25px;
                border-radius: 15px;
                border: 1px solid #f1f5f9;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .app-card:hover {
                transform: translateY(-5px); /* O efeito de elevar */
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                border-color: #34d399;
            }

            /* 6. KPI BOXES (OS DADOS COLORIDOS) */
            /* Restaurei o visual robusto dos números */
            .kpi-box {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                text-align: center;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                transition: transform 0.2s;
            }
            .kpi-box:hover {
                transform: scale(1.02);
                border-color: #cbd5e1;
            }
            .kpi-header {
                background: #f8fafc;
                color: #64748b;
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            .kpi-value {
                font-size: 1.8rem;
                font-weight: 800;
                color: #1e293b;
                padding: 15px 0;
            }
            .kpi-unit { font-size: 0.9rem; color: #94a3b8; font-weight: 500; }
            .kpi-footer {
                color: white;
                font-size: 0.7rem;
                font-weight: 700;
                padding: 5px;
                letter-spacing: 0.5px;
            }

            /* 7. ABAS (TABS) - VOLTANDO AO ORIGINAL BONITO DO STREAMLIT */
            /* Removi o código que deformava. Agora vai ficar o padrão bonito + ajustes finos */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                border-bottom: 1px solid #e2e8f0;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                border-radius: 8px 8px 0 0;
                padding: 0 20px;
                font-weight: 600;
                color: #475569;
            }
            .stTabs [aria-selected="true"] {
                background-color: white !important;
                color: #064e3b !important;
                border-bottom: 3px solid #064e3b;
            }
        </style>
    """, unsafe_allow_html=True)
