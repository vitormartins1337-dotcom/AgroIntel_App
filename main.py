# ARQUIVO: main.py
# SISTEMA: AGRO SDI
# VERSÃO: V-REPAIR (Visual Original Restaurado + Ticker)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai
import os

# --- SETUP ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css
    from agro_utils import AgroBrain
    from notification_engine import NotificationSystem
    import market_engine 
except ImportError as e:
    st.error(f"Erro Crítico: {e.name}")
    st.stop()

st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")
load_css() # Carrega o visual restaurado

# --- DADOS ---
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w = st.query_params.get("w_key", None)
url_g = st.query_params.get("g_key", None)

# --- LOGIN ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="app-card" style="text-align:center; padding:40px;">
            <h1 style="color:#064e3b; margin:0; font-size:2.5rem;">AGRO SDI</h1>
            <p style="color:#6b7280; font-weight:bold; margin-top:10px;">ENTERPRISE PORTAL</p>
        </div>""", unsafe_allow_html=True)
        kw = st.text_input("CHAVE OPENWEATHER", type="password")
        kg = st.text_input("CHAVE GEMINI AI", type="password")
        if st.button("ACESSAR SISTEMA", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# ==============================================================================
# 💎 HEADER BLINDADO (Sem erro de quebra)
# ==============================================================================
ticker_html = market_engine.MarketData.get_ticker_real()

st.markdown(f"""
<div class="header-wrapper">
    <div>
        <h1 style="margin:0; font-family:sans-serif; font-weight:900; font-size:1.8rem; letter-spacing:-1px;">
            AGRO <span style="color:#34d399;">SDI</span>
        </h1>
        <div style="font-size:0.7rem; letter-spacing:2px; opacity:0.9; margin-top:5px; font-weight:bold;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        ONLINE
    </div>
</div>

<div class="ticker-container">
    <div class="ticker-text">{ticker_html}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 💎 FILTROS (Visual Limpo)
# ==============================================================================
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade")
    city = st.text_input("GPS", placeholder="Fazenda...", label_visibility="collapsed")
    if st.button("📡 Sincronizar", use_container_width=True) and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()

with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())), label_visibility="collapsed")
        vars_disp = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
        fases_disp = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
        var_sel = st.selectbox("Genética", vars_disp)
    else: st.error("Banco Offline"); st.stop()

with c3:
    st.markdown("### 📊 Estádio")
    fase_sel = st.selectbox("Fase", fases_disp, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days

st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSAMENTO ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))
    temp, umid, delta_t = hoje['Temp'], hoje['Umid'], hoje['Delta T']
    vpd = AgroBrain.calcular_vpd(temp, umid)
    
    # Cores
    t_st, t_cor = ("Ótima ✅", "#16a34a") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc2626")
    d_st, d_cor = ("APTO ✅", "#16a34a") if 2 <= delta_t <= 8 else ("PARE 🛑", "#dc2626")
    v_st, v_cor = ("Ideal 💧", "#2563eb") if 0.5 <= vpd <= 1.5 else ("Estresse 🌵", "#dc2626")

    # KPI CARDS (COM VISUAL RESTAURADO)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(AgroBrain.gerar_cartao_kpi("🌡️ Temperatura", f"{temp:.1f}", "°C", t_st, t_cor), unsafe_allow_html=True)
    with c2: st.markdown(AgroBrain.gerar_cartao_kpi("🛡️ Delta T", f"{delta_t}", "°C", d_st, d_cor), unsafe_allow_html=True)
    with c3: st.markdown(AgroBrain.gerar_cartao_kpi("💨 VPD (Pressão)", f"{vpd:.2f}", "kPa", v_st, v_cor), unsafe_allow_html=True)
    with c4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA Acumulado", f"{gda_acum:.0f}", "°GD", f"Ciclo: {dias}d", "#1e293b"), unsafe_allow_html=True)

    # --- ABAS (VISUAL ORIGINAL RESTAURADO) ---
    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["🧬 TÉCNICO", "☁️ CLIMA", "📡 RADAR", "👁️ IA", "💰 GESTÃO", "🗺️ MAPA", "📄 LAUDO", "🔔 ALERTAS"])

    # ABA 1
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.caption(f"Evolução: {progresso*100:.1f}%")
        st.progress(progresso)

        nome_cultura = str(cult_sel).lower()
        mapa_img = {"soja": "soja", "milho": "milho", "algodão": "algodao", "algodao": "algodao", "café": "cafe", "cafe": "cafe", "feijão": "feijao", "feijao": "feijao", "trigo": "trigo", "tomate": "tomate", "batata": "batata", "uva": "uva", "banana": "banana", "citros": "citros", "manga": "manga"}
        arquivo_base = next((v for k, v in mapa_img.items() if k in nome_cultura), None)
        img_path = None
        if arquivo_base:
            p_jpg = os.path.join("images", f"{arquivo_base}.jpg")
            p_png = os.path.join("images", f"{arquivo_base}.png")
            if os.path.exists(p_jpg): img_path = p_jpg
            elif os.path.exists(p_png): img_path = p_png

        st.markdown("<br>", unsafe_allow_html=True)
        c_i1, c_i2, c_i3 = st.columns([1,2,1])
        with c_i2:
            if img_path: st.image(img_path, caption=f"Fenologia: {fase_sel}", use_container_width=True)
            else: st.image("https://images.unsplash.com/photo-1625246333195-58197bd47d26?q=80&w=1000&auto=format&fit=crop", caption="Imagem Ilustrativa", use_container_width=True)

        st.divider()
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            st.markdown('<div class="section-title">🧬 GENÉTICA</div>', unsafe_allow_html=True)
            info_txt = AgroBrain.get_info_segura(info, ['info', 'desc'])
            st.markdown(f'<div class="info-text"><b>{var_sel}</b><br>{info_txt}</div>', unsafe_allow_html=True)
        with c_t2:
            st.markdown('<div class="section-title">🌱 FISIOLOGIA</div>', unsafe_allow_html=True)
            fisio_txt = AgroBrain.get_info_segura(dados_fase, ['fisiologia'])
            st.markdown(f'<div class="info-text">{fisio_txt}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-title">🛡️ MANEJO</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo'])
        st.warning(f"🎯 **Ação:** {manejo_txt}")

        st.markdown("### 🧪 Protocolo de Defesa")
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 2
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📅 Tendência Semanal")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Consumo (ETc)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        df_hora = WeatherConn.get_hourly_forecast(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_hora.empty:
            st.markdown("### 🕒 Detalhe 24 Horas")
            fig_h = go.Figure()
            fig_h.add_trace(go.Scatter(x=df_hora['HoraSimples'], y=df_hora['Temp'], name='Temp', mode='lines+markers+text', text=[f"{t:.0f}°" for t in df_hora['Temp']], textposition="top center", line=dict(color='#f97316', width=3), fill='tozeroy', fillcolor='rgba(249, 115, 22, 0.1)'))
            fig_h.update_layout(title="Variação Térmica", height=250, margin=dict(l=20, r=20, t=40, b=20), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_h, use_container_width=True)

            st.markdown("#### 🚜 Janela Delta T")
            cores_dt = ["#16a34a" if 2 <= dt <= 8 else "#ca8a04" if 8 < dt <= 10 else "#dc2626" for dt in df_hora['Delta T']]
            fig_dt = go.Figure()
            fig_dt.add_trace(go.Bar(x=df_hora['HoraSimples'], y=df_hora['Delta T'], marker_color=cores_dt, text=df_hora['Delta T'], textposition='auto'))
            fig_dt.add_hrect(y0=2, y1=8, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Ideal")
            fig_dt.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_dt, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR (VISUAL MASTER - CARDS FLUTUANTES)
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Monitoramento Regional (Satélite)")
        st.caption("Dados em tempo real das estações meteorológicas vizinhas.")
        
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                # Lógica de Cores Profissionais
                if r['Chuva'] == "Sim":
                    cor_fundo = "#fef2f2" # Vermelho bem claro
                    cor_borda = "#fca5a5" # Vermelho suave
                    icon = "🌧️"
                    texto_chuva = "Chuva"
                    cor_texto = "#991b1b" # Vermelho escuro (para leitura)
                else:
                    cor_fundo = "#f0fdf4" # Verde bem claro
                    cor_borda = "#86efac" # Verde suave
                    icon = "☀️"
                    texto_chuva = "Limpo"
                    cor_texto = "#166534" # Verde escuro (para leitura)

                # HTML DO CARD FLUTUANTE
                html_radar = f"""
                <div style="
                    background-color: {cor_fundo};
                    border: 1px solid {cor_borda};
                    border-radius: 12px;
                    padding: 15px;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                    transition: transform 0.2s;
                    height: 100%;
                ">
                    <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 5px;">
                        📍 {r['Direcao']}
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #0f172a; line-height: 1;">
                        {r['Temp']:.0f}°
                    </div>
                    <div style="margin-top: 8px; font-size: 0.9rem; font-weight: 700; color: {cor_texto}; background: rgba(255,255,255,0.5); padding: 4px; border-radius: 6px;">
                        {icon} {texto_chuva}
                    </div>
                </div>
                """
                
                with cols[i]:
                    st.markdown(html_radar, unsafe_allow_html=True)
        else:
            st.info("📡 Sincronizando satélites vizinhos... Aguarde um momento.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4
    with tabs[3]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: img = st.camera_input("Foto")
        with c2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("Analisando..."):
                    try: st.markdown(genai.GenerativeModel('gemini-1.5-flash').generate_content(["Diagnóstico técnico", Image.open(img)]).text)
                    except: st.error("Erro AI")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor", min_value=0.0)
        if c3.button("➕ Adicionar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA MIP (SISTEMA DE PRECISÃO COM BANCO DE DADOS TÉCNICO)
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # --- 1. CONFIGURAÇÃO E BANCO DE DADOS MIP ---
        # Este catálogo define as pragas específicas por cultura
        CATALOGO_MIP = {
            "Soja": {
                "Pragas": ["Lagarta-do-cartucho (S. frugiperda)", "Percevejo-marrom (E. heros)", "Lagarta-falsa-medideira", "Ácaro-rajado", "Mosca-branca"],
                "Doencas": ["Ferrugem Asiática (P. pachyrhizi)", "Antracnose", "Mofo-branco", "Mancha-alvo", "Damping-off"]
            },
            "Milho": {
                "Pragas": ["Cigarrinha-do-milho (D. maidis)", "Lagarta-do-cartucho", "Percevejo-barriga-verde", "Pulgão-do-milho"],
                "Doencas": ["Enfezamento Pálido/Vermelho", "Ferrugem Polissora", "Mancha-branca", "Cercosporiose"]
            },
            "Café": {
                "Pragas": ["Broca-do-café (H. hampei)", "Bicho-mineiro (L. coffeella)", "Ácaro-vermelho", "Cigarra-do-café"],
                "Doencas": ["Ferrugem-do-cafeeiro (H. vastatrix)", "Cercosporiose", "Mancha-de-Phoma", "Rosellinia"]
            },
            "Algodão": {
                "Pragas": ["Bicudo-do-algodoeiro", "Lagarta-das-maçãs", "Pulgão-do-algodoeiro", "Ácaro-rajado"],
                "Doencas": ["Ramulária", "Mancha-angular", "Murcha-de-Fusarium", "Nematoides"]
            }
        }

        # Identifica a cultura selecionada no filtro principal (cult_sel)
        # Se não achar, usa uma lista genérica
        cultura_atual = str(cult_sel).capitalize()
        dados_mip = CATALOGO_MIP.get(cultura_atual, {
            "Pragas": ["Lagarta não identificada", "Percevejo não identificado", "Ácaros", "Tripes"],
            "Doencas": ["Fungo foliar", "Bacteriose", "Vírus", "Murcha"]
        })

        st.markdown(f"### 🛰️ Monitoramento de Precisão: <span style='color:#166534'>{cultura_atual}</span>", unsafe_allow_html=True)
        st.caption("Toque no mapa na localização exata da ocorrência para abrir o diagnóstico.")

        # Layout Otimizado para Mobile (Mapa em Cima, Form em Baixo)
        # MAPA OCUPA 100% DA LARGURA AGORA
        
        m = folium.Map(
            location=[st.session_state['loc_lat'], st.session_state['loc_lon']], 
            zoom_start=18, # Zoom bem próximo para ver o talhão
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satélite HD'
        )
        folium.TileLayer('cartodbpositron', name='Mapa Vetorial').add_to(m)

        # Renderiza os pontos já salvos
        for p in st.session_state['pontos_mapa']:
            # Cores baseadas na severidade
            cor = '#ef4444' if p['Severidade'] == 'Crítico' else '#f97316' if p['Severidade'] == 'Alerta' else '#eab308'
            raio = 40 if p['Severidade'] == 'Crítico' else 25
            
            # Círculo de calor
            folium.Circle(
                location=[p['lat'], p['lon']], radius=raio,
                color=cor, fill=True, fill_color=cor, fill_opacity=0.3, stroke=False
            ).add_to(m)
            
            # Ícone técnico
            icone = "🐛" if "Praga" in p['Categoria'] else "🍄" if "Doença" in p['Categoria'] else "🌿"
            folium.Marker(
                [p['lat'], p['lon']],
                popup=f"<b>{p['Nome']}</b><br>{p['Severidade']}",
                icon=folium.DivIcon(html=f"<div style='font-size:20px;'>{icone}</div>")
            ).add_to(m)

        # Botão de GPS Ativo (Rastreio)
        LocateControl(auto_start=True, strings={"title": "Minha Posição"}).add_to(m)
        out = st_folium(m, height=450, returned_objects=["last_clicked"])

        st.divider()

        # --- LÓGICA DE CADASTRO (SÓ APARECE SE CLICAR OU TIVER POSIÇÃO) ---
        # Se clicou no mapa, usa a coordenada do clique. Se não, usa a última conhecida.
        lat_f = out["last_clicked"]["lat"] if out["last_clicked"] else st.session_state['loc_lat']
        lon_f = out["last_clicked"]["lng"] if out["last_clicked"] else st.session_state['loc_lon']

        if out["last_clicked"]:
            st.markdown(f"#### 📍 Novo Apontamento em: {lat_f:.5f}, {lon_f:.5f}")
            
            with st.form("form_mip_profissional"):
                c_form1, c_form2 = st.columns(2)
                
                with c_form1:
                    categoria = st.radio("Categoria", ["🐛 Praga", "🍄 Doença", "🌿 Daninha"], horizontal=True)
                    
                    # LISTA DINÂMICA: Mostra as pragas REAIS da cultura selecionada
                    if "Praga" in categoria:
                        opcoes = dados_mip["Pragas"] + ["Outra..."]
                    elif "Doença" in categoria:
                        opcoes = dados_mip["Doencas"] + ["Outra..."]
                    else:
                        opcoes = ["Buva", "Amargoso", "Trapoeraba", "Outra..."]
                        
                    agente = st.selectbox("Agente Causal (Identificação)", options=opcoes)

                with c_form2:
                    nivel = st.select_slider("Nível de Dano Econômico (NDE)", 
                                           options=["Monitorar", "Alerta", "Crítico"], 
                                           value="Alerta")
                    
                    contagem = st.number_input("Contagem (nº por metro/planta)", min_value=0.0, step=0.1)

                obs = st.text_input("Nota de Campo", placeholder="Ex: Foco inicial na bordadura...")
                
                # Botão de Salvar Grande
                if st.form_submit_button("✅ CONFIRMAR OCORRÊNCIA", type="primary", use_container_width=True):
                    novo_ponto = {
                        "Data": date.today().strftime("%d/%m/%Y"),
                        "Cultura": cultura_atual,
                        "Categoria": categoria,
                        "Nome": agente,
                        "Severidade": nivel,
                        "Contagem": contagem,
                        "Obs": obs,
                        "lat": lat_f,
                        "lon": lon_f
                    }
                    st.session_state['pontos_mapa'].append(novo_ponto)
                    st.success(f"Ocorrência de {agente} registrada com sucesso!")
                    st.rerun()

        # --- TABELA RESUMO ---
        if st.session_state['pontos_mapa']:
            with st.expander("📋 Ver Caderno de Campo Digital"):
                st.dataframe(pd.DataFrame(st.session_state['pontos_mapa']).drop(columns=['lat', 'lon']), use_container_width=True)
                if st.button("Limpar Histórico"):
                    st.session_state['pontos_mapa'] = []
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7
    with tabs[6]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        obs = st.text_area("Notas")
        if st.button("Gerar PDF"):
            diag = AgroBrain.get_info_segura(dados_fase, ['desc', 'diagnostico'])
            man = AgroBrain.get_info_segura(dados_fase, ['manejo'])
            st.markdown(f"<div style='background:white; color:black; padding:20px; border:1px solid #ccc;'><h1>LAUDO</h1><p><b>{cult_sel}</b></p><p>DIAGNÓSTICO: {diag}</p><p>PRESCRIÇÃO: {man}</p><p>NOTAS: {obs}</p></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 8
    with tabs[7]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Configurar Alertas")
        with st.form("form_notificacao"):
            col_n1, col_n2 = st.columns(2)
            nome_user = col_n1.text_input("Seu Nome")
            email_user = col_n2.text_input("Seu E-mail")
            opcoes_culturas = sorted(list(BANCO_MASTER.keys())) if BANCO_MASTER else []
            culturas_subs = st.multiselect("Culturas", options=opcoes_culturas, default=[cult_sel] if cult_sel in opcoes_culturas else None)
            if st.form_submit_button("Salvar"):
                NotificationSystem.salvar_assinatura(nome_user, email_user, culturas_subs)
                st.success("Salvo!")
        
        st.divider()
        if st.button("📧 Testar Envio"):
            if not email_user: st.warning("Preencha o e-mail.")
            else:
                with st.spinner("Enviando..."):
                    dados_simulados = {}
                    for c in culturas_subs:
                        dados_simulados[c] = f"Temp: {temp:.1f}°C | Chuva: {hoje['Chuva']}mm | Delta T: {delta_t:.1f}°C."
                    sucesso, msg = NotificationSystem.enviar_email_agora(nome_user, email_user, culturas_subs, dados_simulados)
                    if sucesso: st.success(msg)
                    else: st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
