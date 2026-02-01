# ARQUIVO: styles.py
# VERSÃO: AGRO SDI ENTERPRISE SKIN (Visual Militar/Tech)

import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* 1. IMPORTAÇÃO DE FONTES (ROBUSTAS E LEGÍVEIS) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&family=Montserrat:wght@800;900&display=swap');
    
    /* Configuração Base */
    html, body, [class*="css"] { 
        font-family: 'Roboto', sans-serif; 
        color: #1f2937; /* Cinza Chumbo */
        background-color: #f3f4f6; /* Cinza Névoa */
    }

    /* 2. HEADER DA MARCA (AGRO SDI) */
    .brand-container {
        background: linear-gradient(120deg, #064e3b 0%, #111827 100%); /* Verde Floresta -> Preto Noturno */
        padding: 45px 40px; 
        border-radius: 12px; 
        margin-bottom: 30px;
        color: white; 
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border-bottom: 4px solid #10b981; /* Linha Verde Neon */
    }
    
    /* Título da Marca */
    .brand-title {
        font-family: 'Montserrat', sans-serif; 
        font-size: 3.5rem; 
        font-weight: 900;
        letter-spacing: -2px; 
        margin: 0; 
        line-height: 1;
        text-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    .brand-accent { color: #34d399; } /* Verde Esmeralda Claro */
    
    .brand-subtitle {
        font-family: 'Roboto', sans-serif; 
        font-size: 0.95rem; 
        letter-spacing: 4px;
        text-transform: uppercase; 
        color: #d1fae5; 
        margin-top: 8px;
        font-weight: 500;
        border-left: 3px solid #34d399;
        padding-left: 15px;
    }

    /* 3. CONTAINER PADRÃO (CARD BRANCO) */
    .app-card {
        background: white; 
        border-radius: 10px; 
        padding: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb; 
        margin-bottom: 25px;
    }

    /* 4. KPI COCKPIT (Geração via AgroBrain) */
    .kpi-box {
        background: white; 
        border-radius: 12px; 
        padding: 0;
        border: 1px solid #e2e8f0; 
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: transform 0.2s ease-in-out;
        height: 100%; /* Garante altura igual */
    }
    .kpi-box:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        border-color: #94a3b8;
    }
    
    .kpi-header {
        background: #f8fafc; 
        padding: 14px 16px; 
        font-size: 0.8rem;
        font-weight: 700; 
        color: #64748b; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .kpi-value {
        padding: 15px 20px 5px 20px; 
        font-family: 'Montserrat', sans-serif;
        font-size: 2.6rem; 
        font-weight: 800; 
        color: #111827;
        line-height: 1.1;
    }
    
    .kpi-unit { 
        font-size: 1.1rem; 
        color: #9ca3af; 
        font-weight: 500; 
        margin-left: 4px;
    }
    
    .kpi-footer {
        padding: 10px 16px; 
        font-size: 0.85rem; 
        font-weight: 700; 
        color: white; 
        letter-spacing: 0.5px;
    }

    /* 5. ABAS (TABS) ENTERPRISE */
    /* Remove o estilo padrão e aplica um estilo de botão tátil */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding-bottom: 5px;
    }
    
    button[data-baseweb="tab"] {
        font-family: 'Roboto', sans-serif;
        font-size: 16px !important; 
        font-weight: 600 !important;
        padding: 12px 24px !important;
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #6b7280 !important;
        margin-right: 5px !important;
        transition: all 0.2s;
    }
    
    button[data-baseweb="tab"]:hover {
        border-color: #10b981 !important;
        color: #065f46 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #064e3b !important; /* Verde Escuro Fundo */
        color: white !important; /* Texto Branco */
        border-color: #064e3b !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    /* 6. ELEMENTOS AGRONÔMICOS */
    .section-title {
        font-size: 1.1rem; 
        font-weight: 700; 
        color: #065f46; 
        border-left: 4px solid #10b981; 
        padding-left: 10px; 
        margin-bottom: 15px;
        margin-top: 10px;
    }
    
    .info-text {
        font-size: 1rem; 
        line-height: 1.6; 
        color: #374151; 
        text-align: justify;
    }

    /* Estilo para tabelas e dataframes */
    [data-testid="stDataFrame"] { 
        border: 1px solid #e5e7eb; 
        border-radius: 8px; 
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)
