# ARQUIVO: styles.py
# VERSÃO: V-NO-GAPS (Zero Espaços Brancos + Visual Compacto)

import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* 1. REMOVE A BARRA BRANCA DO TOPO (Padding do Container Principal) */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
                max-width: 100% !important;
            }

            /* 2. ESCONDE O CABEÇALHO PADRÃO DO STREAMLIT (Aquele menu no canto) */
            header[data-testid="stHeader"] {
                background-color: transparent !important;
                display: none !important;
            }

            /* 3. REMOVE ESPAÇO ENTRE AS ABAS E O CONTEÚDO */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: white;
                padding-bottom: 0px;
                margin-bottom: 0px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: #f8fafc;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding-top: 10px;
                padding-bottom: 10px;
                border: 1px solid #e2e8f0;
                border-bottom: none;
            }
            .stTabs [aria-selected="true"] {
                background-color: #064e3b !important;
                color: white !important;
                font-weight: bold;
            }

            /* 4. AJUSTA OS CARDS PARA COLAR NAS ABAS */
            div[data-testid="stVerticalBlock"] > div {
                gap: 0.5rem !important; 
            }
            
            /* ESTILO DOS CARDS (Sombra Suave e Bordas) */
            .app-card {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid #e5e7eb;
                margin-bottom: 15px;
                margin-top: 0px; /* Garante que cola em cima */
            }

            /* ESTILOS DE TEXTO ENTERPRISE */
            .brand-title {
                font-family: 'Helvetica Neue', sans-serif;
                font-weight: 900;
                font-size: 2.2rem;
                color: #064e3b;
                margin: 0;
                line-height: 1.1;
            }
            .brand-accent { color: #10b981; }
            .brand-subtitle {
                font-size: 0.9rem;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 600;
            }
            .section-title {
                font-size: 1.1rem;
                font-weight: 800;
                color: #1e293b;
                margin-bottom: 15px;
                border-left: 4px solid #10b981;
                padding-left: 10px;
                text-transform: uppercase;
            }
            
            /* KPI BOX (Quadrados Coloridos) */
            .kpi-box {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0;
                overflow: hidden;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .kpi-header {
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                padding: 8px;
                background: #f8fafc;
                border-bottom: 1px solid #f1f5f9;
            }
            .kpi-value {
                font-size: 1.8rem;
                font-weight: 900;
                color: #0f172a;
                padding: 10px 0;
            }
            .kpi-unit { font-size: 0.9rem; color: #94a3b8; font-weight: 400; margin-left: 2px; }
            .kpi-footer {
                color: white;
                font-size: 0.75rem;
                font-weight: 700;
                padding: 4px;
                text-transform: uppercase;
            }
        </style>
    """, unsafe_allow_html=True)
