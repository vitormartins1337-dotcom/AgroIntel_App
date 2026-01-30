# ARQUIVO: main.py
# FUNÇÃO: Interface UI/UX - Mobile First & High Contrast
# VERSÃO: 5.0 (Correção Mobile Definitiva)

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
# 1. CONFIGURAÇÃO VISUAL (MOBILE FIRST CSS)
# ==============================================================================
st.set_page_config(
    page_title="Agro-Intel Pro",
    page_icon="🛡️",
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
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; }}

    /* FUNDO FIXO */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0, 0.8), rgba(0,0,0, 0.9)), url("{img_url}");
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
        text-shadow: 2px 2px 4px #000000;
    }}
    .titan-sub {{ color: #e0e0e0 !important; font-size: 1.0em; }}

    /* CARTÕES - FORÇAR BRANCO OPACO */
    .pro-card {{
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        border: 1px solid #d1d5db;
        margin-bottom: 20px;
        opacity: 1 !important; /* Garante que não fique transparente */
    }}

    /* TEXTOS - FORÇAR PRETO (Alto Contraste) */
    .card-title {{
        color: #000000 !important;
        font-size: 1.3em; 
        font-weight: 800; 
        border-bottom: 3px solid #0288d1;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}

    .label-tech {{ 
        color: #0277bd !important; /* Azul Escuro */
        font-size: 0.85em; 
        font-weight: 900; 
        text-transform: uppercase; 
        margin-top: 15px;
    }}
    
    .value-tech {{ 
        color: #111111 !important; /* Preto Quase Absoluto */
        font-size: 1.1em; 
        line-height: 1.5; 
        font-weight: 500;
    }}

    /* ALERTAS */
    .alert-box-red {{ background: #ffcdd2; border-left: 8px solid #b71c1c; padding: 15px; color: #b71c1c; font-weight: bold; border-radius: 5px; }}
    .alert-box-green {{ background: #c8e6c9; border-left: 8px solid #1b5e20; padding: 15px; color: #1b5e20; font-weight: bold; border-radius: 5px; }}

    /* KPIs (Métricas) - Forçar Fundo Branco */
    div[data-testid="metric-container"] {{
        background-color: #ffffff !important;
        border: 2px solid #90caf9;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }}
    label[data-testid="stMetricLabel"] {{ color: #444444 !important; font-weight: 700 !important; }}
    div[data-testid="stMetricValue"] {{ color: #000000 !important; font-weight: 900 !important; }}
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
# 3. TELA DE LOGIN (Simplificada)
# ==============================================================================
if not url_w:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        st.markdown("""
        <div class="pro-card" style="text-align:center;">
            <h2 style="color:#000;">🔒 Agro-Intel Enterprise</h2>
            <p style="color:#333;">Login do Sistema</p>
        </div>
        """, unsafe_allow_html=True)
        kw = st.text_input("API Key OpenWeather", type="password")
        kg = st.text_input("API Key Gemini AI", type="password")
        if st.button("ENTRAR", type="primary", use_container_width=True):
            if kw and kg:
                st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# ==============================================================================
# 4. DASHBOARD
# ==============================================================================
st.markdown("""
<div style="text-align:center; padding: 20px;">
    <h1 class="titan-title">AGRO-INTEL</h1>
    <div class="titan-sub">Enterprise System v5.0</div>
</div>
""", unsafe_allow_html=True)

# PAINEL DE CONTROLE
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])

with c1:
    st.markdown("**📍 LOCALIZAÇÃO**")
    t1, t2 = st.tabs(["Busca", "GPS"])
    with t1:
        city = st.text_input("Cidade:", label_visibility="collapsed", placeholder="Digite a cidade...")
        if st.button("🔍") and city:
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
    with t2:
        st.write(f"{st.session_state['loc_lat']:.4f}, {st.session_state['loc_lon']:.4f}")

with c2:
    st.markdown("**🚜 CULTURA**")
    cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
    col_v, col_f = st.columns(2)
    var_sel = col_v.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
    fase_sel = col_f.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))

with c3:
    st.markdown("**📆 IDADE**")
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h2 style='color:#0277bd; margin:0;'>{dias} Dias</h2>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD", f"{hoje['VPD']} kPa")
    k3.metric("💦 ETc", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    # ABAS
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 PDF"])

    # 1. TÉCNICO
    with tabs[0]:
        st.markdown(f"**Maturação (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)

        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.markdown('<div class="alert-box-red">🚨 ALERTA: Alta Umidade. Risco de Doenças.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box-green">✅ CLIMA: Favorável para Aplicações.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="pro-card">
                <div class="card-title">🧬 Fisiologia</div>
                <div class="label-tech">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
                <div class="label-tech">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
                <div class="label-tech">GENÉTICA</div><div class="value-tech">{info['info']}</div>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            # AQUI ESTÁ A CORREÇÃO PRINCIPAL: SUBSTITUÍMOS HTML PURO POR STREAMLIT NATIVO
            st.markdown('<div class="pro-card"><div class="card-title">🛡️ Protocolo de Manejo</div>', unsafe_allow_html=True)
            
            st.markdown(f"**MANEJO CULTURAL:**\n\n{dados_fase.get('manejo', '-')}")
            st.markdown("---")
            st.markdown("**🧪 FARMÁCIA DIGITAL:**")
            
            # Loop Python para gerar a lista (Nativo = Sem erro no mobile)
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    st.info(f"**{q['Alvo']}**: {q['Ativo']} \n\n *({q['Grupo']} - {q['Tipo']})*")
            else:
                st.info(f"{dados_fase['quimica']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. CLIMA
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#0288d1'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. RADAR
    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📡 Radar Virtual (15km)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""
                <div style="background:{bg}; padding:10px; border-radius:8px; text-align:center; color:black; border:1px solid #ccc;">
                    <b>{r["Direcao"]}</b><br>
                    <span style="font-size:1.5em; font-weight:bold;">{r["Temp"]:.0f}°C</span><br>
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
                res = genai.GenerativeModel('gemini-1.5-flash').generate_content([f"Agrônomo. Cultura {cult_sel}. Fase {fase_sel}. Diagnóstico.", Image.open(img)]).text
                st.markdown(res)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. CUSTOS
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor R$")
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
        txt = f"LAUDO TÉCNICO\nCultura: {cult_sel}\nFase: {fase_sel}\nRecomendação: {dados_fase['manejo']}\nQuímicos: {dados_fase['quimica']}"
        st.download_button("Baixar TXT", data=txt, file_name="Laudo.txt")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Conectando satélites...")
