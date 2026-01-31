# ARQUIVO: main.py
# FUNÇÃO: Interface Vibrant Pro V9.1 (Correção de Botões Duplicados)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- IMPORTAÇÃO ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("ERRO: Motores não encontrados.")
    st.stop()

# 1. CONFIGURAÇÃO (VIBRANT THEME)
st.set_page_config(page_title="Agro-Intel Pro", page_icon="🚀", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    /* FUNDO MODERNO */
    .stApp {
        background-color: #f4f7f6;
        background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* HEADER COM DEGRADÊ */
    .titan-header {
        background: linear-gradient(90deg, #1CB5E0 0%, #000851 100%);
        padding: 30px; border-radius: 15px; text-align: center; color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2); margin-bottom: 30px;
    }
    .titan-title { color: white; font-size: 3em; font-weight: 800; margin: 0; text-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .titan-sub { color: #a8edea; font-size: 1.2em; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }

    /* CARTÕES VIBRANTES */
    .pro-card {
        background: white; border-radius: 15px; padding: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); border: 1px solid #eee;
        transition: transform 0.3s ease; margin-bottom: 20px;
    }
    .pro-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }

    /* TEXTOS E ETIQUETAS */
    .label-tech { color: #888; font-size: 0.8em; font-weight: 700; text-transform: uppercase; margin-top: 10px; }
    .value-tech { color: #222; font-size: 1.1em; font-weight: 500; }
    
    .chem-tag { display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 700; color: white; margin-top: 5px; }
    .tag-sys { background: linear-gradient(45deg, #FF512F, #DD2476); } /* Laranja/Rosa */
    .tag-con { background: linear-gradient(45deg, #11998e, #38ef7d); } /* Verde */
    .tag-bio { background: linear-gradient(45deg, #2193b0, #6dd5ed); } /* Azul */

    /* METRICS COLORIDAS */
    div[data-testid="metric-container"] {
        background: white; border-radius: 12px; border-left: 5px solid #1CB5E0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    label[data-testid="stMetricLabel"] { color: #555 !important; font-weight: 600 !important; }
    div[data-testid="stMetricValue"] { font-size: 2em !important; font-weight: 800 !important; }
    
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. DADOS
BANCO_MASTER = get_database()
if not BANCO_MASTER: st.warning("⚠️ Banco de dados vazio. Adicione arquivos .json na pasta database.")

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
        st.markdown('<div class="pro-card" style="text-align:center;"><h2 style="color:#000851;">🔒 Login Seguro</h2></div>', unsafe_allow_html=True)
        kw = st.text_input("API Key OpenWeather", type="password")
        kg = st.text_input("API Key Gemini AI", type="password")
        if st.button("ACESSAR PAINEL", type="primary", use_container_width=True, key="btn_login"):
            if kw and kg: st.query_params["w_key"] = kw; st.query_params["g_key"] = kg; st.rerun()
    st.stop()

# 4. APP DASHBOARD
st.markdown("""
<div class="titan-header">
    <h1 class="titan-title">AGRO INTEL</h1>
    <div class="titan-sub">Inteligência Agronômica Avançada</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("### 📍 Localização")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Buscar cidade...")
    if st.button("🔍 Buscar", key="btn_buscar_cidade") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Selecione:", sorted(list(BANCO_MASTER.keys())))
        col_v, col_f = st.columns(2)
        var_sel = col_v.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
        fase_sel = col_f.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))
    else: st.error("Database Error"); st.stop()
with c3:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h1 style='color:#1CB5E0;'>{dias} Dias</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPIS VIBRANTES
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temp", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD", f"{hoje['VPD']} kPa")
    k3.metric("💦 ETc", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C")
    st.write("")

    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.write(f"**Maturação (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)

        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.markdown('<div style="background:#ffcdd2; color:#c62828; padding:15px; border-radius:10px; font-weight:bold;">🚨 ALERTA: Umidade Alta. Use Sistêmicos.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#c8e6c9; color:#2e7d32; padding:15px; border-radius:10px; font-weight:bold;">✅ CLIMA: Ideal para Preventivos.</div>', unsafe_allow_html=True)
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <h3 style="color:#000851;">🧬 Fisiologia</h3>
            <div class="label-tech">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
            <div class="label-tech">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
            <div class="label-tech">GENÉTICA</div><div class="value-tech">{info['info']}</div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f'<h3 style="color:#000851;">🛡️ Manejo</h3>', unsafe_allow_html=True)
            st.markdown(f"<div class='value-tech'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.markdown("<br><b>Farmácia Digital:</b>", unsafe_allow_html=True)
            
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    tag = "tag-bio"
                    if "Sistêmico" in q['Tipo'] or "Curativo" in q['Tipo']: tag = "tag-sys"
                    if "Contato" in q['Tipo'] or "Protetor" in q['Tipo']: tag = "tag-con"
                    
                    st.markdown(f"""
                    <div style="background:#f9f9f9; padding:10px; border-radius:8px; margin-bottom:8px; border-left:4px solid #1CB5E0;">
                        <b>{q['Alvo']}</b>: {q['Ativo']}
                        <br><span class="chem-tag {tag}">{q['Grupo']} • {q['Tipo']}</span>
                    </div>""", unsafe_allow_html=True)
            else: st.info(dados_fase['quimica'])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#1CB5E0'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc', line=dict(color='#DD2476', width=4)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📡 Radar (15km)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#fff" 
                border = "#eee"
                if r['Chuva'] == "Sim": bg = "#ffebee"; border = "#ffcdd2"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:15px; border-radius:10px; text-align:center; border:2px solid {border};"><b>{r["Direcao"]}</b><br><h2>{r["Temp"]:.0f}°C</h2>{r["Chuva"]}</div>""", unsafe_allow_html=True)
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
        # AQUI FOI CORRIGIDO: key="btn_save_custo"
        if c3.button("Salvar", key="btn_save_custo") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Talhão"); 
            # AQUI FOI CORRIGIDO: key="btn_save_mapa"
            if st.button("Salvar", key="btn_save_mapa") and st.session_state.get('last_click'): st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]}); st.rerun()
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
