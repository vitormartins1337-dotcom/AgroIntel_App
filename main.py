# ARQUIVO: main.py
# FUNÇÃO: Interface UI/UX - Visual Blindado (Alto Contraste)
# VERSÃO: 7.0 (Correção Definitiva de Visibilidade)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai
import io
import base64

# --- IMPORTAÇÃO DOS MOTORES ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError as e:
    st.error(f"ERRO DE SISTEMA: {e}")
    st.stop()

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL (CSS BLINDADO)
# ==============================================================================
st.set_page_config(
    page_title="Agro-Intel Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_img_as_base64(file):
    try:
        with open(file, "rb") as f: data = f.read()
        return base64.b64encode(data).decode()
    except: return None

def load_css():
    img_b64 = get_img_as_base64("fundo_agro.jpg")
    img_url = f"data:image/png;base64,{img_b64}" if img_b64 else "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=1740&auto=format&fit=crop"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; }}

    /* FUNDO ESCURO PROFISSIONAL */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0, 0.85), rgba(0,0,0, 0.95)), url("{img_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* HEADER */
    .titan-title {{
        color: #ffffff !important; 
        font-size: 2.5em; 
        font-weight: 900; 
        margin: 0;
        text-shadow: 0px 4px 10px #000000;
        text-transform: uppercase;
    }}
    .titan-sub {{ 
        color: #4fc3f7 !important; /* Azul claro para contraste */
        font-size: 1.1em; 
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* CARTÕES BRANCOS SÓLIDOS (GLOBAL) */
    .pro-card {{
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border-left: 6px solid #0288d1;
        margin-bottom: 20px;
        color: #000000 !important; /* Força texto preto dentro dos cards */
    }}
    
    /* CORREÇÃO DAS METRICAS (KPIs) - FORÇAR VISIBILIDADE */
    div[data-testid="metric-container"] {{
        background-color: #ffffff !important; /* Fundo Branco */
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        color: #000000 !important;
    }}
    
    label[data-testid="stMetricLabel"] {{
        color: #555555 !important; /* Cinza Escuro */
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        color: #000000 !important; /* Preto Absoluto */
        font-size: 1.8rem !important;
        font-weight: 900 !important;
    }}

    /* CORREÇÃO DAS ABAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #ffffff; /* Fundo da barra de abas branco */
        padding: 10px 10px 0 10px;
        border-radius: 10px 10px 0 0;
        gap: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #444 !important; /* Cor do texto da aba não selecionada */
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: #0288d1 !important; /* Azul quando selecionado */
        color: #ffffff !important; /* Texto branco */
    }}

    /* TEXTOS GERAIS */
    h1, h2, h3, p, li {{ color: #000000; }} /* Padrão preto */
    .stMarkdown p {{ color: #000000 !important; }} 
    
    /* TAGS QUÍMICAS */
    .chem-tag {{
        display: inline-block; padding: 4px 10px; border-radius: 15px;
        font-size: 0.75em; font-weight: 700; text-transform: uppercase; margin-top: 5px;
    }}
    .tag-sistemico {{ background: #fff3e0; color: #e65100; border: 1px solid #ffb74d; }}
    .tag-contato {{ background: #e8f5e9; color: #1b5e20; border: 1px solid #81c784; }}
    .tag-bio {{ background: #e1f5fe; color: #01579b; border: 1px solid #4fc3f7; }}

    </style>
    """, unsafe_allow_html=True)

load_css()

# ==============================================================================
# 2. LÓGICA DE DADOS
# ==============================================================================
BANCO_MASTER = get_database()

if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# ==============================================================================
# 3. TELA DE LOGIN
# ==============================================================================
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown("""
        <div class="pro-card" style="text-align:center;">
            <h2 style="margin:0; color:#000;">🔒 LOGIN SEGURO</h2>
            <p style="color:#555;">Gestão Agronômica de Precisão</p>
        </div>
        """, unsafe_allow_html=True)
        kw = st.text_input("API Key OpenWeather", type="password")
        kg = st.text_input("API Key Gemini AI", type="password")
        if st.button("ENTRAR NO SISTEMA", type="primary", use_container_width=True):
            if kw and kg:
                st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# ==============================================================================
# 4. DASHBOARD
# ==============================================================================
st.markdown("""
<div style="text-align:center; padding: 20px 0 30px 0;">
    <h1 class="titan-title">AGRO-INTEL</h1>
    <div class="titan-sub">Gestão Agronômica de Precisão</div>
</div>
""", unsafe_allow_html=True)

# PAINEL DE CONTROLE (BRANCO)
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])

with c1:
    st.markdown("<span style='color:#0277bd; font-weight:900;'>📍 LOCALIZAÇÃO</span>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Busca", "GPS"])
    with t1:
        city = st.text_input("Busca:", label_visibility="collapsed", placeholder="Digite a cidade...")
        if st.button("🔍") and city:
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
    with t2:
        st.write(f"{st.session_state['loc_lat']:.4f}, {st.session_state['loc_lon']:.4f}")

with c2:
    st.markdown("<span style='color:#0277bd; font-weight:900;'>🚜 CULTURA</span>", unsafe_allow_html=True)
    cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
    col_v, col_f = st.columns(2)
    var_sel = col_v.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
    fase_sel = col_f.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))

with c3:
    st.markdown("<span style='color:#0277bd; font-weight:900;'>📆 IDADE</span>", unsafe_allow_html=True)
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<div style='font-size:2.5em; font-weight:900; color:#000; line-height:1;'>{dias} Dias</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPI STRIP (AGORA VISÍVEL)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD", f"{hoje['VPD']} kPa")
    k3.metric("💦 ETc", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    # ==========================================================================
    # CONTEÚDO PRINCIPAL (DENTRO DE ABAS BRANCAS)
    # ==========================================================================
    # Forçamos o conteúdo a ficar dentro de containers brancos para contraste
    
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # 1. TÉCNICO
    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        
        st.markdown(f"**Progresso de Maturação (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)

        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.error("🚨 ALERTA: Umidade Alta. Priorize Sistêmicos.")
        else:
            st.success("✅ CLIMA: Favorável para Preventivos.")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <h3 style="color:#0277bd;">🧬 Fisiologia</h3>
            <p><b>DESCRIÇÃO:</b> {dados_fase['desc']}</p>
            <p><b>DINÂMICA:</b> {dados_fase['fisiologia']}</p>
            <p><b>GENÉTICA:</b> {info['info']}</p>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown('<h3 style="color:#0277bd;">🛡️ Manejo & Químicos</h3>', unsafe_allow_html=True)
            st.write(f"**Cultural:** {dados_fase.get('manejo', '-')}")
            
            st.markdown("**Farmácia Digital:**")
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    # Lógica de cor da etiqueta
                    tipo = q['Tipo'].lower()
                    css_class = "tag-bio"
                    if "sistêmico" in tipo or "curativo" in tipo: css_class = "tag-sistemico"
                    elif "contato" in tipo or "protetor" in tipo: css_class = "tag-contato"
                    
                    st.markdown(f"""
                    <div style="background:#f5f5f5; padding:10px; border-radius:8px; margin-bottom:5px; border-left:4px solid #aaa;">
                        <b>{q['Alvo']}</b>: {q['Ativo']} 
                        <br><span class="chem-tag {css_class}">{q['Grupo']} • {q['Tipo']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(dados_fase['quimica'])
                
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. CLIMA
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#0288d1'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#d32f2f', width=3)))
        fig.update_layout(height=350, paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. RADAR
    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📡 Radar (15km)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""
                <div style="background:{bg}; padding:10px; border-radius:8px; text-align:center; color:black; border:1px solid #ddd;">
                    <b>{r["Direcao"]}</b><br>
                    <h3>{r["Temp"]:.0f}°C</h3>
                    {r["Chuva"]}
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. IA
    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("👁️ Diagnóstico IA")
        img = st.camera_input("Foto")
        if img and url_g:
            genai.configure(api_key=url_g)
            with st.spinner("Analisando..."):
                res = genai.GenerativeModel('gemini-1.5-flash').generate_content([f"Agrônomo. {cult_sel}. Fase {fase_sel}. Diagnóstico.", Image.open(img)]).text
                st.markdown(res)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. CUSTOS
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor")
        if c3.button("Lançar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. MAPA
    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Talhão")
            if st.button("Salvar") and st.session_state.get('last_click'):
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"📍 {p['nome']}")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            for p in st.session_state['pontos_mapa']: folium.Marker([p['lat'], p['lon']], popup=p['nome']).add_to(m)
            out = st_folium(m, height=450, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. LAUDO
    with tabs[6]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📄 Relatório")
        txt = f"LAUDO\nCultura: {cult_sel}\nRecomendação: {dados_fase['manejo']}"
        st.download_button("Baixar", data=txt, file_name="Laudo.txt")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Conectando satélites...")
