# ARQUIVO: main.py
# FUNÇÃO: Interface UI/UX - Clean Clinical Enterprise
# VERSÃO: 8.0 (JSON Integration + White Theme)

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

# IMPORTAÇÃO DOS MOTORES
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError as e:
    st.error(f"ERRO DE SISTEMA: {e}")
    st.stop()

# 1. CONFIGURAÇÃO (LIGHT THEME)
st.set_page_config(page_title="Agro-Intel System", page_icon="🌿", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

    /* FUNDO CLEAN (Cinza Claro Profissional) */
    .stApp {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* HEADER */
    .titan-header {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; margin-bottom: 30px;
    }
    .titan-title { color: #1a237e; font-size: 2.5em; font-weight: 900; letter-spacing: -1px; margin: 0; }
    .titan-sub { color: #5c6bc0; font-size: 1.1em; font-weight: 500; text-transform: uppercase; letter-spacing: 2px; }

    /* CARTÕES CLEAN (Branco com Sombra Suave) */
    .pro-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .pro-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px rgba(0,0,0,0.08); }

    /* TIPOGRAFIA DE DADOS */
    .label-tech { color: #7986cb; font-size: 0.8em; font-weight: 700; text-transform: uppercase; margin-top: 15px; }
    .value-tech { color: #283593; font-size: 1.1em; line-height: 1.6; font-weight: 400; text-align: justify; }
    .section-title { color: #1a237e; font-weight: 800; font-size: 1.4em; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; margin-bottom: 15px; }

    /* ETIQUETAS */
    .chem-tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 700; margin-top: 5px; }
    .tag-blue { background: #e3f2fd; color: #1565c0; }
    .tag-green { background: #e8f5e9; color: #2e7d32; }
    .tag-orange { background: #fff3e0; color: #ef6c00; }

    /* KPIs */
    div[data-testid="metric-container"] {
        background: white; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    label[data-testid="stMetricLabel"] { color: #5c6bc0 !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { color: #1a237e !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. DADOS E LOGIN
BANCO_MASTER = get_database() # Agora lê do JSON!
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<div class="pro-card" style="text-align:center;"><h2 style="color:#1a237e;">🔒 Login Enterprise</h2></div>', unsafe_allow_html=True)
        kw = st.text_input("API Key OpenWeather", type="password")
        kg = st.text_input("API Key Gemini AI", type="password")
        if st.button("ENTRAR", type="primary", use_container_width=True):
            if kw and kg: st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# 3. DASHBOARD
st.markdown("""
<div class="titan-header">
    <h1 class="titan-title">AGRO-INTEL SYSTEM</h1>
    <div class="titan-sub">Gestão Agronômica de Precisão</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("**📍 LOCALIZAÇÃO**")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Buscar cidade...")
    if st.button("🔍") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
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
    st.markdown(f"<div style='font-size:2em; font-weight:900; color:#1a237e;'>{dias} Dias</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD", f"{hoje['VPD']} kPa")
    k3.metric("💦 ETc", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown(f"**Progresso GDA:** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="section-title">🧬 Fisiologia</div>
            <div class="label-tech">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
            <div class="label-tech">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
            <div class="label-tech">GENÉTICA</div><div class="value-tech">{info['info']}</div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="section-title">🛡️ Manejo</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='value-tech'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("**Farmácia Digital:**")
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    tag_class = "tag-blue"
                    if "Sistêmico" in q['Tipo']: tag_class = "tag-orange"
                    if "Contato" in q['Tipo']: tag_class = "tag-green"
                    st.markdown(f"""
                    <div style="background:#f8f9fa; padding:12px; border-radius:8px; margin-bottom:8px; border-left:3px solid #ccc;">
                        <b style="color:#333;">{q['Alvo']}</b>: {q['Ativo']}
                        <br><span class="chem-tag {tag_class}">{q['Grupo']} • {q['Tipo']}</span>
                    </div>""", unsafe_allow_html=True)
            else: st.info(dados_fase['quimica'])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#1976d2'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📡 Radar Virtual")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:15px; border-radius:10px; text-align:center;"><b>{r["Direcao"]}</b><br><h3>{r["Temp"]:.0f}°C</h3>{r["Chuva"]}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        img = st.camera_input("Foto")
        if img and url_g:
            genai.configure(api_key=url_g)
            with st.spinner("Analisando..."):
                st.markdown(genai.GenerativeModel('gemini-1.5-flash').generate_content([f"Agrônomo. {cult_sel} {fase_sel}. Diagnóstico.", Image.open(img)]).text)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item"); v = c2.number_input("Valor"); 
        if c3.button("Salvar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Talhão"); 
            if st.button("Salvar") and st.session_state.get('last_click'): st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"📍 {p['nome']}")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            out = st_folium(m, height=450, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[6]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        txt = f"LAUDO\nCultura: {cult_sel}\nRecomendação: {dados_fase['manejo']}"
        st.download_button("Baixar PDF", data=txt, file_name="Laudo.txt")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Conectando satélites...")
