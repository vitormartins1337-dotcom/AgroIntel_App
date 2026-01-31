# ARQUIVO: main.py
# FUNÇÃO: Interface Enterprise V11 (Correção de Indentação + Visual FRAC/IRAC)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- TENTATIVA DE IMPORTAÇÃO ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("ERRO CRÍTICO: Motores (data_engine.py ou calc_engine.py) não encontrados.")
    st.stop()

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="Agro-Intel Enterprise", page_icon="🧬", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f0f2f6; }

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
    
    /* TAGS QUÍMICAS AVANÇADAS */
    .chem-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 8px; 
        padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* TEXTO */
    .tech-label { font-size: 0.75em; color: #757575; font-weight: 700; text-transform: uppercase; margin-top: 10px; }
    .tech-val { font-size: 1em; color: #212121; line-height: 1.5; }
    
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. CARREGAMENTO DE DADOS
BANCO_MASTER = get_database()
if not BANCO_MASTER: 
    st.warning("⚠️ O Banco de Dados está vazio ou não foi lido corretamente. Verifique a pasta /database.")

# INICIALIZAÇÃO DE SESSÃO
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

# PEGA CHAVES DA URL
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# 3. TELA DE LOGIN
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<div class="pro-card" style="text-align:center;"><h2>🔒 Enterprise Login</h2></div>', unsafe_allow_html=True)
        kw = st.text_input("OpenWeather Key", type="password")
        kg = st.text_input("Gemini AI Key", type="password")
        if st.button("ACESSAR SISTEMA", type="primary", use_container_width=True, key="login_btn"):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# 4. DASHBOARD PRINCIPAL
st.markdown('<div class="titan-header"><h1>AGRO INTEL ENTERPRISE</h1><p>Sistema de Gestão Fenológica & Fitossanitária</p></div>', unsafe_allow_html=True)

# FILTROS SUPERIORES
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("### 📍 Localização")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Digite a cidade...")
    if st.button("🔍 Buscar Local", key="search_city") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: 
            st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon
            st.rerun()
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Selecione a Cultura", sorted(list(BANCO_MASTER.keys())))
        
        # Garante que as chaves existam antes de acessar
        vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
        fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
        
        col_v, col_f = st.columns(2)
        var_sel = col_v.selectbox("Genética/Variedade", vars_disponiveis)
        fase_sel = col_f.selectbox("Estádio Fenológico", fases_disponiveis)
    else: 
        st.error("Erro: Banco de dados vazio.")
        st.stop()
with c3:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Data de Plantio", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h2 style='text-align:center; color:#1565c0;'>{dias} Dias</h2>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO DE DADOS
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temperatura", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 VPD (Estresse)", f"{hoje['VPD']} kPa")
    k3.metric("💦 Evapotranspiração", f"{hoje['ETc']} mm")
    k4.metric("🛡️ Delta T (Aplicação)", f"{hoje['Delta T']}°C")
    st.write("")

    # ABAS
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # ABA 1: TÉCNICO (AQUI ESTÁ A CORREÇÃO DO CÓDIGO QUÍMICO)
    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.progress(progresso)
        st.caption(f"GDA Acumulado: {gda_acum:.0f} / {info.get('gda_meta', 1500)}")

        if hoje['Umid'] > 85: 
            st.error("🚨 ALERTA: Alta Umidade. Risco severo de doenças fúngicas.")
        else: 
            st.success("✅ CLIMA: Favorável para manejo fitossanitário.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🧬 Fisiologia & Genética")
            st.markdown(f"<div class='tech-label'>DESCRIÇÃO</div><div class='tech-val'>{dados_fase.get('desc', '-')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='tech-label'>DINÂMICA FISIOLÓGICA</div><div class='tech-val'>{dados_fase.get('fisiologia', '-')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='tech-label'>CARACTERÍSTICA VARIETAL</div><div class='tech-val'>{info.get('info', '-')}</div>", unsafe_allow_html=True)
        
        with c2:
            st.markdown("#### 🛡️ Manejo Integrado")
            st.markdown(f"<div class='tech-val'>{dados_fase.get('manejo', '-')}</div>", unsafe_allow_html=True)
            st.write("")
            
            # --- AQUI ESTAVA O ERRO DE INDENTAÇÃO (AGORA CORRIGIDO) ---
            with st.expander("🧪 PROTOCOLO AVANÇADO (FRAC/IRAC)", expanded=True):
                if isinstance(dados_fase.get('quimica'), list):
                    for q in dados_fase['quimica']:
                        # Cores dinâmicas
                        tipo = q.get('Tipo', 'Geral')
                        cor_borda = "#1976d2" # Azul
                        
                        if "Biológico" in tipo: cor_borda = "#2e7d32" # Verde
                        elif "Químico" in tipo: cor_borda = "#d32f2f" # Vermelho
                        elif "Nutrição" in tipo: cor_borda = "#fbc02d" # Amarelo

                        # Exibição do Cartão
                        st.markdown(f"""
                        <div class="chem-card" style="border-left: 5px solid {cor_borda};">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:bold; font-size:1.1em; color:#333;">🎯 {q.get('Alvo', 'Alvo Geral')}</span>
                                <span style="background:{cor_borda}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8em;">{tipo}</span>
                            </div>
                            <div style="margin-top:5px; color:#444;">
                                💊 <b>Ativo:</b> {q.get('Ativo', '-')}
                            </div>
                            <div style="margin-top:5px; font-size:0.9em; color:#666;">
                                🧬 <b>Grupo:</b> <span style="background:#f5f5f5; padding:2px 5px; border-radius:3px; font-weight:bold;">{q.get('Codigos', q.get('Grupo', '-'))}</span>
                            </div>
                            <div style="margin-top:8px; font-style:italic; font-size:0.9em; color:#1565c0;">
                                💡 <b>Estratégia:</b> {q.get('Estrategia', q.get('Obs', ''))}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else: 
                    st.info("Nenhum protocolo cadastrado para esta fase.")
            # -----------------------------------------------------------
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 2: CLIMA
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#1565c0'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc (mm)', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR
    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:10px; border-radius:8px; text-align:center;"><b>{r["Direcao"]}</b><br><h3>{r["Temp"]:.0f}°C</h3>{r["Chuva"]}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA
    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        img = st.camera_input("Tirar Foto do Problema")
        if img and url_g:
            genai.configure(api_key=url_g)
            with st.spinner("A IA está analisando a imagem..."):
                try:
                    prompt = f"Sou Agrônomo. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga/doença na imagem e sugira controle técnico."
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, Image.open(img)])
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Descrição do Item")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("Lançar Custo", key="btn_custos") and i: 
            st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v})
            st.rerun()
        
        if st.session_state['custos']: 
            df_custos = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df_custos, use_container_width=True)
            st.metric("Custo Total", f"R$ {df_custos['Valor'].sum():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA
    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Nome do Talhão")
            if st.button("Salvar Ponto", key="btn_mapa") and st.session_state.get('last_click'): 
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"📍 {p['nome']}")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            out = st_folium(m, height=450, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7: LAUDO
    with tabs[6]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("### Gerador de Laudo Técnico")
        observacoes = st.text_area("Observações Adicionais do Agrônomo")
        
        txt_laudo = f"""
        LAUDO TÉCNICO AGRONÔMICO
        --------------------------------
        Data: {date.today()}
        Cultura: {cult_sel}
        Variedade: {var_sel}
        Estádio: {fase_sel}
        
        DIAGNÓSTICO:
        {dados_fase.get('desc', '')}
        {dados_fase.get('fisiologia', '')}
        
        RECOMENDAÇÃO DE MANEJO:
        {dados_fase.get('manejo', '')}
        
        OBSERVAÇÕES:
        {observacoes}
        """
        st.download_button("📥 Baixar PDF (TXT)", data=txt_laudo, file_name=f"Laudo_{cult_sel}_{date.today()}.txt")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Aguardando conexão com satélites meteorológicos...")
