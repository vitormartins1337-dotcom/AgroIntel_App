# ARQUIVO: main.py
# FUNÇÃO: Interface Enterprise V12 (Full Expanders - Cockpit Agronômico)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- IMPORTAÇÃO DOS MOTORES ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("ERRO CRÍTICO: Motores (data_engine.py ou calc_engine.py) não encontrados.")
    st.stop()

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="Agro-Intel Enterprise", page_icon="🚜", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f4f6f9; }

    /* HEADER */
    .titan-header {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); /* Verde Agro Profissional */
        padding: 20px; border-radius: 10px; text-align: center; color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15); margin-bottom: 20px;
    }
    
    /* CARDS GERAIS */
    .pro-card {
        background: white; border-radius: 8px; padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }

    /* TAGS QUÍMICAS (VISUAL NOVO) */
    .chem-card {
        background: #fafafa; border: 1px solid #ddd; border-radius: 6px; 
        padding: 10px; margin-bottom: 8px; 
    }
    </style>
    """, unsafe_allow_html=True)
load_css()

# 2. CARREGAMENTO DE DADOS
BANCO_MASTER = get_database()
if not BANCO_MASTER: 
    # Fallback silencioso para não travar o app se o JSON estiver com erro
    st.warning("⚠️ Aviso: Banco de dados instável ou vazio. Verifique os arquivos JSON.")
    BANCO_MASTER = {}

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
        st.markdown('<div class="pro-card" style="text-align:center;"><h2>🔒 Acesso Restrito</h2><p>Agro-Intel Enterprise System</p></div>', unsafe_allow_html=True)
        kw = st.text_input("🔑 OpenWeather Key", type="password")
        kg = st.text_input("🧠 Gemini AI Key", type="password")
        if st.button("ENTRAR NO SISTEMA", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# 4. DASHBOARD
st.markdown('<div class="titan-header"><h1>AGRO INTEL ENTERPRISE</h1><p>Gestão de Safra de Alta Precisão</p></div>', unsafe_allow_html=True)

# FILTROS
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("### 📍 Localização")
    city = st.text_input("Cidade", label_visibility="collapsed", placeholder="Ex: Lucas do Rio Verde...")
    if st.button("🔍 Buscar Local") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: 
            st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon
            st.rerun()
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Selecione a Cultura", sorted(list(BANCO_MASTER.keys())))
        try:
            vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
            fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
            
            col_v, col_f = st.columns(2)
            var_sel = col_v.selectbox("Genética", vars_disponiveis)
            fase_sel = col_f.selectbox("Fase Atual", fases_disponiveis)
        except:
            st.error("Erro na estrutura da cultura selecionada.")
            st.stop()
    else: 
        st.error("Banco de dados vazio.")
        st.stop()
with c3:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Data Plantio", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h3 style='text-align:center; color:#2e7d32; margin:0;'>{dias} DAE</h3>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # KPIs CLIMÁTICOS
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temperatura", f"{hoje['Temp']:.1f}°C")
    k2.metric("💧 Umidade Relativa", f"{hoje['Umid']}%")
    k3.metric("💦 Evapotranspiração", f"{hoje['ETc']} mm/dia")
    k4.metric("🛡️ Delta T (Pulverização)", f"{hoje['Delta T']}°C", delta_color="inverse")
    
    # ABAS
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # --- ABA 1: TÉCNICO (MODELO NOVO EXPANDER) ---
    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.progress(progresso)
        st.caption(f"Ciclo Acumulado (GDA): {gda_acum:.0f} / {info.get('gda_meta', 1500)}")

        # 1. EXPANDER: GENÉTICA
        with st.expander("🧬 GENÉTICA & CARACTERÍSTICAS VARIETAIS", expanded=True):
            st.info(f"**{var_sel}**")
            st.markdown(f"**Características:** {info.get('info', 'Sem dados.')}")
            st.markdown(f"**Kc (Coeficiente de Cultura):** {info.get('kc', '1.0')}")

        # 2. EXPANDER: FISIOLOGIA
        with st.expander("🌱 FISIOLOGIA DO ESTÁDIO (FÊNOLÓGICO)", expanded=True):
            col_f1, col_f2 = st.columns([1, 2])
            with col_f1:
                st.markdown(f"**Descrição Visual:**\n{dados_fase.get('desc', '-')}")
            with col_f2:
                st.markdown(f"**Dinâmica Interna (Fisiologia):**\n{dados_fase.get('fisiologia', '-')}")

        # 3. EXPANDER: MANEJO
        with st.expander("🛡️ ESTRATÉGIAS DE MANEJO TÉCNICO", expanded=True):
            st.warning(f"**Recomendação:** {dados_fase.get('manejo', '-')}")

        # 4. EXPANDER: QUÍMICA (PROTOCOLOS)
        with st.expander("🧪 PROTOCOLO AVANÇADO (FRAC/IRAC/BIO)", expanded=False):
            if isinstance(dados_fase.get('quimica'), list):
                for q in dados_fase['quimica']:
                    # Cores dinâmicas
                    tipo = q.get('Tipo', 'Geral')
                    cor_borda = "#1976d2" # Azul Padrão
                    icone = "💊"
                    
                    if "Biológico" in tipo: 
                        cor_borda = "#2e7d32"; icone = "🦠" # Verde Bio
                    elif "Químico" in tipo: 
                        cor_borda = "#d32f2f"; icone = "☠️" # Vermelho Quimico
                    elif "Nutrição" in tipo: 
                        cor_borda = "#fbc02d"; icone = "⚡" # Amarelo Nutri

                    # Layout do Card
                    st.markdown(f"""
                    <div class="chem-card" style="border-left: 5px solid {cor_borda};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:bold; font-size:1.05em; color:#333;">{icone} {q.get('Alvo', 'Alvo Geral')}</span>
                            <span style="background:{cor_borda}; color:white; padding:2px 8px; border-radius:4px; font-size:0.75em; font-weight:bold;">{tipo}</span>
                        </div>
                        <div style="margin-top:8px; color:#444; font-size:0.95em;">
                            <b>Ativo:</b> {q.get('Ativo', '-')}
                        </div>
                        <div style="margin-top:4px; font-size:0.9em; color:#666;">
                            🧬 <b>Grupo:</b> <span style="background:#eee; padding:2px 6px; border-radius:4px;">{q.get('Codigos', q.get('Grupo', '-'))}</span>
                        </div>
                        <div style="margin-top:8px; font-style:italic; font-size:0.9em; color:#0277bd;">
                            💡 <b>Estratégia:</b> {q.get('Estrategia', q.get('Obs', ''))}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else: 
                st.info("Nenhum protocolo cadastrado para esta fase.")
        
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
        c_ia1, c_ia2 = st.columns([1, 1])
        with c_ia1:
            img = st.camera_input("📸 Identificar Praga/Doença")
        with c_ia2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("Analisando imagem..."):
                    try:
                        prompt = f"Sou Agrônomo. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga/doença e sugira controle técnico (químico e biológico)."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([prompt, Image.open(img)])
                        st.markdown(response.text)
                    except Exception as e: st.error(f"Erro IA: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item / Insumo")
        v = c2.number_input("Valor Total (R$)", min_value=0.0)
        if c3.button("➕ Lançar") and i: 
            st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v})
            st.rerun()
        if st.session_state['custos']: 
            df_custos = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df_custos, use_container_width=True)
            st.metric("Total Acumulado", f"R$ {df_custos['Valor'].sum():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA
    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Nome do Ponto")
            if st.button("📍 Marcar Ponto") and st.session_state.get('last_click'): 
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"🚩 {p['nome']}")
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
        st.markdown("### 📝 Emitir Receituário/Laudo")
        obs = st.text_area("Parecer Técnico")
        if st.button("🖨️ Gerar PDF"):
            st.success("Laudo gerado com sucesso!")
            st.write(f"""
            **LAUDO TÉCNICO - {date.today()}**
            Cultura: {cult_sel} | Variedade: {var_sel}
            Fase: {fase_sel}
            
            Diagnóstico: {dados_fase.get('desc','')}
            Recomendação: {dados_fase.get('manejo','')}
            
            Observações: {obs}
            """)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Aguardando dados meteorológicos...")
