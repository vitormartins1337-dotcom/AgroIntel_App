# ARQUIVO: styles.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* 1. TIPOGRAFIA PREMIUM (Inter & Montserrat) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Montserrat:wght@700;800;900&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: #1e293b; /* Cinza Escuro Profissional */
        background-color: #f1f5f9; /* Fundo Suave */
    }

    /* 2. LOGOMARCA AGRO SDI */
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 40px; border-radius: 16px; margin-bottom: 30px;
        color: white; border-bottom: 4px solid #22c55e;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .brand-title {
        font-family: 'Montserrat', sans-serif; font-size: 3rem; font-weight: 900;
        letter-spacing: -1px; margin: 0; line-height: 1;
    }
    .brand-accent { color: #22c55e; } /* Verde Neon Agro */
    .brand-subtitle {
        font-family: 'Montserrat', sans-serif; font-size: 0.9rem; letter-spacing: 3px;
        text-transform: uppercase; color: #94a3b8; margin-top: 5px;
    }

    /* 3. CARTÕES DE CONTEÚDO (CARDS) */
    .app-card {
        background: white; border-radius: 12px; padding: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }

    /* 4. KPI / COCKPIT (Painel de Decisão) */
    .kpi-box {
        background: white; border-radius: 12px; padding: 0;
        border: 1px solid #e2e8f0; overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .kpi-box:hover { transform: translateY(-3px); border-color: #cbd5e1; }
    
    .kpi-header {
        background: #f8fafc; padding: 12px 15px; font-size: 0.75rem;
        font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;
        border-bottom: 1px solid #e2e8f0;
    }
    .kpi-value {
        padding: 15px 20px 5px 20px; font-family: 'Montserrat', sans-serif;
        font-size: 2.2rem; font-weight: 800; color: #0f172a;
    }
    .kpi-unit { font-size: 1rem; color: #94a3b8; font-weight: 500; }
    .kpi-footer {
        padding: 8px 15px; font-size: 0.8rem; font-weight: 600; color: white;
    }

    /* 5. ABAS (TABS) MAIS LEGÍVEIS */
    button[data-baseweb="tab"] {
        font-size: 16px !important; font-weight: 600 !important;
        padding: 15px 25px !important; color: #64748b !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #166534 !important; border-bottom: 3px solid #166534 !important;
        background: #f0fdf4 !important;
    }

    /* 6. TEXTOS AGRONÔMICOS */
    .agro-title { font-weight: 700; color: #15803d; font-size: 1.1rem; margin-bottom: 8px; }
    .agro-text { font-size: 1rem; line-height: 1.6; color: #334155; text-align: justify; }
    
    /* Tags Químicas */
    .tag-chem {
        display: inline-block; padding: 3px 8px; border-radius: 4px; 
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: white; margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
