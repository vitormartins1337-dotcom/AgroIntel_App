# ARQUIVO: main.py
# FUNÇÃO: Interface UI/UX - Visual Pro Dinâmico
# VERSÃO: 6.0 (Layout Atrativo & Subtítulo Original)

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
# 1. CONFIGURAÇÃO VISUAL (VISUAL PRO CSS)
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

    /* FUNDO AGRO-DARK (IMERSIVO) */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0, 0.85), rgba(0,0,0, 0.92)), url("{img_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* HEADER COM SUBTÍTULO ORIGINAL */
    .titan-title {{
        color: #ffffff !important; 
        font-size: 2.8em; 
        font-weight: 900; 
        margin: 0;
        text-transform: uppercase;
        letter-spacing: -1px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.8);
    }}
    .titan-sub {{ 
        color: #4fc3f7 !important; /* Azul Neon Suave */
        font-size: 1.2em; 
        font-weight: 500;
        letter-spacing: 1px;
        margin-top: 5px;
        text-transform: uppercase;
    }}

    /* CARTÕES DINÂMICOS (HOVER EFFECT) */
    .pro-card {{
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #0288d1; /* Borda lateral azul */
        margin-bottom: 20px;
        opacity: 1 !important;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s;
    }}
    .pro-card:hover {{
        transform: translateY(-3px); /* Levanta levemente ao passar o mouse */
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }}

    /* TIPOGRAFIA DE DADOS (VISIBILIDADE TOTAL) */
    .data-label {{
        color: #546e7a !important;
        font-size: 0.8em;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 3px;
    }}
    .data-value {{
        color: #102027 !important;
        font-size: 1.1em;
        font-weight: 500;
        line-height: 1.4;
    }}
    .section-header {{
        color: #01579b !important;
        font-size: 1.3em;
        font-weight: 900;
        border-bottom: 2px solid #e1f5fe;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}

    /* ETIQUETAS QUÍMICAS */
    .chem-tag {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 5px;
    }}
    .tag-sistemico {{ background: #fff3e0; color: #e65100; border: 1px solid #ffb74d; }} /* Laranja */
    .tag-contato {{ background: #e8f5e9; color: #1b5e20; border: 1px solid #81c784; }} /* Verde */
    .tag-bio {{ background: #e1f5fe; color: #01579b; border: 1px solid #4fc3f7; }} /* Azul */

    /* AJUSTES KPI DO STREAMLIT */
    div[data-testid="metric-container"] {{
        background-color: #ffffff !important;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #cfd8dc;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    label[data-testid="stMetricLabel"] {{ color: #455a64 !important; font-weight: 700 !important; }}
    div[data-testid="stMetricValue"] {{ color: #000000 !important; font-weight: 900 !important; font-size: 1.8em !important; }}
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
            <h2 style="color:#000; margin:0;">🔒 ACESSO SEGURO</h2>
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
# 4. DASHBOARD (CABEÇALHO)
# ==============================================================================
st.markdown("""
<div style="text-align:center; padding: 25px 0 40px 0;">
    <h1 class="titan-title">AGRO-INTEL</h1>
    <div class="titan-sub">Gestão Agronômica de Precisão</div>
</div>
""", unsafe_allow_html=True)

# PAINEL DE CONTROLE
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])

with c1:
    st.markdown("<div class='data-label'>📍 LOCALIZAÇÃO</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Cidade", "GPS"])
    with t1:
        city = st.text_input("Busca:", label_visibility="collapsed", placeholder="Digite a cidade...")
        if st.button("🔍") and city:
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
    with t2:
        st.write(f"Coord: {st.session_state['loc_lat']:.4f}, {st.session_state['loc_lon']:.4f}")

with c2:
    st.markdown("<div class='data-label'>🚜 PRODUÇÃO</div>", unsafe_allow_html=True)
    cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
    col_v, col_f = st.columns(2)
    var_sel = col_v.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
    fase_sel = col_f.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))

with c3:
    st.markdown("<div class='data-label'>📆 CICLO</div>", unsafe_allow_html=True)
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<div style='font-size:2.2em; font-weight:900; color:#0277bd; line-height:1;'>{dias} Dias</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPI STRIP
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD", f"{hoje['VPD']} kPa")
    k3.metric("💦 ETc", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    # ==========================================================================
    # ABAS DE CONTEÚDO (LAYOUT DINÂMICO)
    # ==========================================================================
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # 1. TÉCNICO (RECEITUÁRIO COLORIDO)
    with tabs[0]:
        st.markdown(f"**Progresso de Maturação (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)

        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.error("🚨 ALERTA: Alta Umidade. Risco de Doenças. Priorize Sistêmicos.")
        else:
            st.success("✅ CLIMA: Favorável para Preventivos e Manejo.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="pro-card">
                <div class="section-header">🧬 Fisiologia</div>
                <div class="data-label">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
                <div style="margin-top:10px;"></div>
                <div class="data-label">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
                <div style="margin-top:10px;"></div>
                <div class="data-label">GENÉTICA</div><div class="value-tech">{info['info']}</div>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div class="pro-card"><div class="section-header">🛡️ Protocolo de Manejo</div>', unsafe_allow_html=True)
            
            st.markdown(f"<div class='data-label'>MANEJO CULTURAL</div><div class='value-tech'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.divider()
            st.markdown("<div class='data-label'>🧪 FARMÁCIA DIGITAL</div>", unsafe_allow_html=True)
            
            # LÓGICA DE CORES PARA QUÍMICOS
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    # Define a cor baseada no tipo
                    tipo_str = q['Tipo'].lower()
                    classe_css = "tag-bio" # Default azul
                    if "sistêmico" in tipo_str or "curativo" in tipo_str:
                        classe_css = "tag-sistemico" # Laranja
                    elif "contato" in tipo_str or "protetor" in tipo_str:
                        classe_css = "tag-contato" # Verde
                    
                    st.markdown(f"""
                    <div style="background:#f9f9f9; padding:10px; border-radius:8px; border:1px solid #eee; margin-bottom:8px;">
                        <div style="font-weight:bold; color:#000;">{q['Alvo']}</div>
                        <div style="color:#333;">{q['Ativo']}</div>
                        <div class="{classe_css} chem-tag">{q['Grupo']} • {q['Tipo']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"{dados_fase['quimica']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. CLIMA
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#0288d1'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#d32f2f', width=3)))
        fig.update_layout(title="Balanço Hídrico (5 Dias)", height=350)
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
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#f1f8e9"
                with cols[i]: st.markdown(f"""
                <div style="background:{bg}; padding:15px; border-radius:8px; text-align:center; border:1px solid #ccc; color:black;">
                    <b>{r["Direcao"]}</b><br>
                    <span style="font-size:1.5em; font-weight:900;">{r["Temp"]:.0f}°C</span><br>
                    {r["Chuva"]}
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. IA
    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("👁️ Diagnóstico IA")
        img = st.camera_input("Foto da Lavoura")
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
        txt = f"LAUDO TÉCNICO - AGRO INTEL\n\nCultura: {cult_sel}\nFase: {fase_sel}\n\nRecomendação: {dados_fase['manejo']}\n\nQuímicos: {dados_fase['quimica']}"
        st.download_button("Baixar TXT", data=txt, file_name="Laudo.txt")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Conectando satélites...")
