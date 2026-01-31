# ARQUIVO: main.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai
import base64

# --- IMPORTAÇÃO SEGURA ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("ERRO: Motores (data_engine.py / calc_engine.py) não encontrados.")
    st.stop()

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Agro-Intel Pro", page_icon="🛡️", layout="wide")

def load_css():
    st.markdown("""
    <style>
    /* FUNDO CLEAN (CINZA CLARO) PARA CONTRASTE PERFEITO */
    .stApp { background-color: #f0f2f6; }
    
    /* HEADER */
    .titan-header { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; }
    .titan-title { color: #1565c0; font-size: 2.2em; font-weight: 900; margin: 0; }
    
    /* CARTÕES BRANCOS */
    .pro-card { background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e0e0e0; margin-bottom: 20px; color: #333; }
    
    /* TIPOGRAFIA */
    h1, h2, h3, h4, p, li { color: #212121; }
    .label-tech { color: #546e7a; font-size: 0.8em; font-weight: 700; text-transform: uppercase; margin-top: 10px; }
    .value-tech { color: #1a237e; font-size: 1.05em; font-weight: 500; text-align: justify; }
    
    /* TAGS */
    .chem-tag { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.7em; font-weight: 700; margin-top: 5px; }
    .tag-blue { background: #e3f2fd; color: #1565c0; }
    .tag-orange { background: #fff3e0; color: #e65100; }
    
    /* METRICS */
    div[data-testid="metric-container"] { background: #fff; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. DADOS E ESTADO
BANCO_MASTER = get_database() # Lê do JSON via data_engine
if not BANCO_MASTER: st.warning("Banco de dados vazio ou não encontrado.")

if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# 3. LOGIN
if not url_w:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<div class="pro-card" style="text-align:center;"><h2>🔒 Login Enterprise</h2></div>', unsafe_allow_html=True)
        kw = st.text_input("API Key OpenWeather", type="password")
        kg = st.text_input("API Key Gemini AI", type="password")
        if st.button("ENTRAR", type="primary", use_container_width=True):
            if kw and kg: st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# 4. APP
st.markdown('<div class="titan-header"><h1 class="titan-title">AGRO-INTEL</h1><p>Gestão Agronômica de Precisão</p></div>', unsafe_allow_html=True)

st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("**📍 LOCALIZAÇÃO**")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Buscar...")
    if st.button("🔍") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
with c2:
    st.markdown("**🚜 CULTURA**")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
        cv, cf = st.columns(2)
        var_sel = cv.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
        fase_sel = cf.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))
    else:
        st.error("Erro no DB")
        st.stop()
with c3:
    st.markdown("**📆 SAFRA**")
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
    k1.metric("Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("VPD", f"{hoje['VPD']} kPa")
    k3.metric("ETc", f"{hoje['ETc']} mm")
    k4.metric("Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown(f"**Progresso GDA:** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <h4 style="color:#1565c0;">🧬 Fisiologia</h4>
            <div class="label-tech">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
            <div class="label-tech">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
            <div class="label-tech">GENÉTICA</div><div class="value-tech">{info['info']}</div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f'<h4 style="color:#1565c0;">🛡️ Manejo</h4>', unsafe_allow_html=True)
            st.markdown(f"<div class='value-tech'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("**Químicos:**")
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    tag = "tag-orange" if "Sistêmico" in q['Tipo'] else "tag-blue"
                    st.markdown(f"""
                    <div style="background:#f5f5f5; padding:8px; border-radius:5px; margin-bottom:5px; border-left:3px solid #bbb;">
                        <b>{q['Alvo']}</b>: {q['Ativo']}
                        <br><span class="chem-tag {tag}">{q['Grupo']}</span>
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
        st.subheader("📡 Radar (15km)")
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
        if c3.button("Lançar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
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
