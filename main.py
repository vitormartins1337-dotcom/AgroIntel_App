# ARQUIVO: main.py
# FUNÇÃO: Interface Enterprise V10 (Expanders & Deep Data)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("ERRO CRÍTICO: Motores não encontrados.")
    st.stop()

# 1. VISUAL SETTINGS
st.set_page_config(page_title="Agro-Intel Enterprise", page_icon="🧬", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f8f9fa; }

    /* HEADER */
    .titan-header {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
        padding: 25px; border-radius: 12px; text-align: center; color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    
    /* CARDS */
    .pro-card {
        background: white; border-radius: 10px; padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
        margin-bottom: 15px; border-left: 5px solid #1565c0;
    }
    
    /* TAGS QUÍMICAS */
    .chem-pill { display: inline-block; padding: 4px 10px; border-radius: 15px; font-size: 0.75em; font-weight: 700; color: white; margin-right: 5px; }
    .sys { background: #ff9800; } /* Laranja */
    .con { background: #4caf50; } /* Verde */
    .bio { background: #03a9f4; } /* Azul */
    .hor { background: #9c27b0; } /* Roxo */
    
    /* TEXTO */
    .tech-label { font-size: 0.75em; color: #757575; font-weight: 700; text-transform: uppercase; margin-top: 10px; }
    .tech-val { font-size: 1em; color: #212121; line-height: 1.5; }
    
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. DATA LOADING
BANCO_MASTER = get_database()
if not BANCO_MASTER: st.warning("⚠️ Adicione arquivos .json nas pastas em database/")

if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# 3. LOGIN
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<div class="pro-card" style="text-align:center;"><h2>🔒 Enterprise Login</h2></div>', unsafe_allow_html=True)
        kw = st.text_input("OpenWeather Key", type="password")
        kg = st.text_input("Gemini AI Key", type="password")
        if st.button("ACESSAR", type="primary", use_container_width=True, key="login_btn"):
            if kw and kg: st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# 4. DASHBOARD
st.markdown('<div class="titan-header"><h1>AGRO INTEL ENTERPRISE</h1><p>Sistema de Gestão Fenológica & Fitossanitária</p></div>', unsafe_allow_html=True)

st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("### 📍 Localização")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Buscar...")
    if st.button("🔍 Buscar", key="search_city") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
        col_v, col_f = st.columns(2)
        var_sel = col_v.selectbox("Genética", list(BANCO_MASTER[cult_sel]['vars'].keys()))
        fase_sel = col_f.selectbox("Fenologia", list(BANCO_MASTER[cult_sel]['fases'].keys()))
    else: st.error("Database vazio"); st.stop()
with c3:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h2>{dias} Dias</h2>", unsafe_allow_html=True)
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
        st.progress(progresso)
        st.caption(f"GDA Acumulado: {gda_acum:.0f} / {info.get('gda_meta', 1500)}")

        if hoje['Umid'] > 85: st.error("🚨 ALERTA: Alta Umidade. Risco de doenças fúngicas.")
        else: st.success("✅ CLIMA: Favorável para manejo.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🧬 Fisiologia & Genética")
            st.markdown(f"<div class='tech-label'>DESCRIÇÃO</div><div class='tech-val'>{dados_fase['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='tech-label'>DINÂMICA</div><div class='tech-val'>{dados_fase['fisiologia']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='tech-label'>CARACTERÍSTICA VARIETAL</div><div class='tech-val'>{info['info']}</div>", unsafe_allow_html=True)
        
        with c2:
            st.markdown("#### 🛡️ Manejo Integrado")
            st.markdown(f"<div class='tech-val'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.write("")
            
            with st.expander("🧪 PROTOCOLO AVANÇADO DE MANEJO (FRAC/IRAC)", expanded=True):
                if isinstance(dados_fase.get('quimica'), list):
                    for q in dados_fase['quimica']:
                        # Cores dinâmicas para as etiquetas
                        tipo = q.get('Tipo', 'Geral')
                        cor_tipo = "#1976d2" # Azul padrão
                        if "Biológico" in tipo: cor_tipo = "#2e7d32" # Verde Bio
                        elif "Químico" in tipo: cor_tipo = "#d32f2f" # Vermelho Quimico
                        
                        # Layout do Card Químico
                        st.markdown(f"""
                        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid {cor_tipo};">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:bold; font-size:1.1em; color:#333;">🎯 {q['Alvo']}</span>
                                <span style="background:{cor_tipo}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8em;">{tipo}</span>
                            </div>
                            <div style="margin-top:5px; color:#555;">
                                💊 <b>Ativo:</b> {q['Ativo']}
                            </div>
                            <div style="margin-top:5px; font-size:0.9em; color:#666;">
                                🧬 <b>Grupo (Resistência):</b> <span style="background:#eee; padding:2px 5px; border-radius:3px; font-weight:bold;">{q.get('Codigos', '-')}</span>
                            </div>
                            <div style="margin-top:8px; font-style:italic; font-size:0.9em; color:#1565c0;">
                                💡 <b>Estratégia:</b> {q.get('Estrategia', '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else: 
                    st.info("Nenhum protocolo cadastrado para esta fase.")

                        st.markdown(f"""
                        <div style="border-bottom:1px solid #eee; padding:10px 0;">
                            <span class="chem-pill {tag_cls}">{q['Grupo']}</span>
                            <b>{q['Alvo']}</b>
                            <br><span style="color:#555; font-size:0.9em;">{q['Ativo']} • <i>{q['Tipo']}</i></span>
                        </div>""", unsafe_allow_html=True)
                else: st.info(dados_fase['quimica'])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#1565c0'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:10px; border-radius:8px; text-align:center;"><b>{r["Direcao"]}</b><br><h3>{r["Temp"]:.0f}°C</h3>{r["Chuva"]}</div>""", unsafe_allow_html=True)
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
        if c3.button("Lançar", key="btn_custos") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Talhão"); 
            if st.button("Salvar", key="btn_mapa") and st.session_state.get('last_click'): st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]}); st.rerun()
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
        txt = f"LAUDO TÉCNICO\n\nCultura: {cult_sel}\nFase: {fase_sel}\n\nRecomendação: {dados_fase['manejo']}"
        st.download_button("Baixar PDF", data=txt, file_name="Laudo.txt")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Conectando satélites...")
