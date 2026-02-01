# ARQUIVO: main.py
# SISTEMA: AGRO SDI (V18 - Modular Professional Architecture)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# IMPORTAÇÕES DOS MÓDULOS (A MÁGICA ACONTECE AQUI)
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css # Nossa maquiagem profissional
    from agro_utils import AgroBrain # Nosso cérebro agronômico
except ImportError as e:
    st.error(f"🚨 ERRO DE INTEGRIDADE: Módulo {e.name} não encontrado.")
    st.stop()

# 1. CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Agro SDI | Enterprise", page_icon="🌾", layout="wide")
load_css() # Carrega o CSS do arquivo styles.py

# 2. VARIÁVEIS DE SESSÃO
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# 3. LOGIN (Clean)
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="app-card" style="text-align:center;">
            <h1 style="color:#15803d; font-weight:900;">AGRO SDI</h1>
            <p style="text-transform:uppercase; font-size:0.8rem; letter-spacing:2px;">Sistema de Decisão Integrada</p>
        </div>""", unsafe_allow_html=True)
        kw = st.text_input("API Key (OpenWeather)", type="password")
        kg = st.text_input("API Key (Gemini AI)", type="password")
        if st.button("ACESSAR SISTEMA", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw; st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# 4. HEADER (HERO)
st.markdown("""
<div class="brand-container">
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <h1 class="brand-title">AGRO <span class="brand-accent">SDI</span></h1>
            <div class="brand-subtitle">PLATAFORMA ENTERPRISE v18</div>
        </div>
        <div style="text-align:right; font-size:0.8rem; opacity:0.8;">
            Ambiente Seguro<br>Decisão de Alta Precisão
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. BARRA DE CONTROLE (FILTROS)
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade")
    city = st.text_input("Busca GPS", placeholder="Fazenda ou Cidade...", label_visibility="collapsed")
    if st.button("🔄 Sincronizar") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()

with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())), label_visibility="collapsed")
        try:
            vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
            fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
            var_sel = st.selectbox("Genética", vars_disponiveis)
        except: st.warning("Dados incompletos."); st.stop()
    else: st.error("Database vazia."); st.stop()

with c3:
    st.markdown("### 📊 Fase")
    fase_sel = st.selectbox("Estádio", fases_disponiveis, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days

st.markdown('</div>', unsafe_allow_html=True)

# 6. PROCESSAMENTO E KPIs
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # Semáforo Inteligente (Calculado via AgroBrain ou Inline)
    temp = hoje['Temp']
    t_status, t_color = ("Ótima ✅", "#16a34a") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc2626")
    
    delta_t = hoje['Delta T']
    if 2 <= delta_t <= 8: d_status, d_color = "APTO ✅", "#16a34a"
    elif 8 < delta_t <= 10: d_status, d_color = "ATENÇÃO ⚠️", "#ca8a04"
    else: d_status, d_color = "PARE 🛑", "#dc2626"

    # Geração dos Cards via AgroBrain (HTML limpo)
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1: st.markdown(AgroBrain.gerar_cartao_kpi("🌡️ Temperatura", f"{temp:.1f}", "°C", t_status, t_color), unsafe_allow_html=True)
    with col_k2: st.markdown(AgroBrain.gerar_cartao_kpi("💧 Umidade", f"{hoje['Umid']}", "%", "Relativa", "#2563eb"), unsafe_allow_html=True)
    with col_k3: st.markdown(AgroBrain.gerar_cartao_kpi("🛡️ Delta T", f"{delta_t}", "°C", d_status, d_color), unsafe_allow_html=True)
    with col_k4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA Acumulado", f"{gda_acum:.0f}", "°GD", f"Dias: {dias}", "#334155"), unsafe_allow_html=True)

    # 7. CONTEÚDO PRINCIPAL (ABAS)
    tabs = st.tabs(["🧬 TÉCNICO", "☁️ CLIMA", "📡 RADAR", "👁️ IA VISION", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # --- ABA TÉCNICA (AGRO MASTER) ---
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.caption(f"Progresso Estimado da Cultura ({progresso*100:.1f}%)")
        st.progress(progresso)

        # Imagem Blindada
        if "Soja" in str(cult_sel):
            try: st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Soybean.jpg/800px-Soybean.jpg", width=400)
            except: pass

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="agro-title">🧬 CARACTERIZAÇÃO VARIETAL</div>', unsafe_allow_html=True)
            # Usa o AgroBrain para buscar info segura
            info_txt = AgroBrain.get_info_segura(info, ['info', 'desc', 'detalhes'])
            st.markdown(f'<div class="agro-text">{info_txt}</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div class="agro-title">🌱 FISIOLOGIA E DESENVOLVIMENTO</div>', unsafe_allow_html=True)
            fisio_txt = AgroBrain.get_info_segura(dados_fase, ['fisiologia', 'desenvolvimento'])
            st.markdown(f'<div class="agro-text">{fisio_txt}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="agro-title">🛡️ DIRETRIZES DE MANEJO</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo', 'recomendacao'])
        st.warning(f"🎯 **Foco do Agrônomo:** {manejo_txt}")

        st.markdown("### 🧪 Protocolo Avançado")
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) # Renderiza os cards sem erro
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA CLIMA ---
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapo (mm)', line=dict(color='#ef4444', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        
        # Alertas Automáticos do AgroBrain
        st.markdown("#### 🚨 Alertas Climáticos Automáticos")
        alertas = AgroBrain.analisar_risco_climatico(temp, delta_t, hoje['Umid'])
        if alertas:
            for tit, desc in alertas:
                st.error(f"**{tit}**: {desc}")
        else:
            st.success("✅ Nenhuma condição climática adversa detectada no momento.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA RADAR ---
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                with cols[i]:
                    bg = "#fee2e2" if r['Chuva'] == "Sim" else "#dcfce7"
                    cor = "#991b1b" if r['Chuva'] == "Sim" else "#166534"
                    st.markdown(f"""
                    <div style="background:{bg}; padding:15px; border-radius:10px; text-align:center; border:1px solid {cor}30;">
                        <div style="font-weight:bold; color:#64748b;">{r["Direcao"]}</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{cor};">{r["Temp"]:.0f}°</div>
                        <div style="font-weight:700; color:{cor};">{r["Chuva"]}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA IA ---
    with tabs[3]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,1])
        with c1: img = st.camera_input("📸 Foto Diagnóstico")
        with c2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("🤖 AgroBrain Analisando..."):
                    try:
                        prompt = f"Agrônomo Expert. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique problemas visuais e sugira manejo."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content([prompt, Image.open(img)])
                        st.markdown(res.text)
                    except: st.error("Erro IA.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA CUSTOS ---
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']:
            df = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown(f"<h3 style='text-align:right; color:#dc2626;'>Total: R$ {df['Valor'].sum():,.2f}</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA MAPA ---
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Ponto GPS")
            if st.button("📍 Gravar") and st.session_state.get('last'): 
                st.session_state['pontos_mapa'].append({"n": nm, "lat": st.session_state['last'][0], "lon": st.session_state['last'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"🚩 {p['n']}")
        with c2:
            m = folium.Map([st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Sat').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            
            for p in st.session_state['pontos_mapa']:
                folium.Marker([p['lat'], p['lon']], popup=p['n']).add_to(m)
                
            out = st_folium(m, height=450, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA LAUDO ---
    with tabs[6]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("📝 Emissão de Receituário")
        obs = st.text_area("Observações Técnicas")
        if st.button("🖨️ Gerar PDF"):
            # O AgroBrain ajuda a formatar o texto se estiver faltando
            diag = AgroBrain.get_info_segura(dados_fase, ['desc', 'diagnostico'])
            man = AgroBrain.get_info_segura(dados_fase, ['manejo'])
            
            st.markdown(f"""
            <div style="border:2px solid black; padding:40px; background:white; font-family:'Times New Roman';">
                <h2 style="text-align:center;">AGRO SDI - RECEITUÁRIO AGRONÔMICO</h2>
                <hr>
                <p><b>Data:</b> {date.today()} | <b>Local:</b> {city}</p>
                <h4>1. IDENTIFICAÇÃO</h4>
                <p>Cultura: {cult_sel} ({var_sel}) | Fase: {fase_sel}</p>
                <h4>2. DIAGNÓSTICO</h4>
                <p>{diag}</p>
                <h4>3. PRESCRIÇÃO</h4>
                <p>{man}</p>
                <h4>4. OBSERVAÇÕES</h4>
                <p>{obs}</p>
                <br><br><br>
                <center>__________________________<br>Engenheiro Agrônomo</center>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
