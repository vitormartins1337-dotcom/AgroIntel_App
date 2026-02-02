# ARQUIVO: main.py
# SISTEMA: AGRO SDI (Sistema de Decisão Integrada)
# VERSÃO: V19 - INTEGRATED MASTER (VPD + AI + ROBUST DATA)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- 1. IMPORTAÇÃO DOS MOTORES DE INTELIGÊNCIA ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css             # Nossa nova "Roupa" Militar/Tech
    from agro_utils import AgroBrain        # Nosso novo "Cérebro" com VPD
except ImportError as e:
    st.error(f"🚨 FALHA CRÍTICA DE SISTEMA: Módulo {e.name} ausente.")
    st.stop()

# --- 2. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Agro SDI | Enterprise", page_icon="🛰️", layout="wide")
load_css() # Injeta o CSS profissional

# Variáveis de Estado (Memória do App)
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
# Tenta pegar chaves da URL (Query Params)
url_w = st.query_params.get("w_key", None)
url_g = st.query_params.get("g_key", None)

# --- 3. TELA DE LOGIN SEGURA ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="app-card" style="text-align:center; padding:40px;">
            <h1 style="color:#064e3b; font-family:'Montserrat'; font-weight:900; font-size:3rem; margin:0;">AGRO SDI</h1>
            <p style="text-transform:uppercase; color:#6b7280; font-weight:600; letter-spacing:2px; margin-top:5px;">Enterprise Access Portal</p>
        </div>""", unsafe_allow_html=True)
        
        kw = st.text_input("CHAVE DE ACESSO (OpenWeather)", type="password")
        kg = st.text_input("CHAVE DE ACESSO (Gemini AI)", type="password")
        
        if st.button("AUTENTICAR E ACESSAR", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# --- 4. HERO HEADER (CABEÇALHO) ---
st.markdown("""
<div class="brand-container">
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <h1 class="brand-title">AGRO <span class="brand-accent">SDI</span></h1>
            <div class="brand-subtitle">SISTEMA DE DECISÃO INTEGRADA | v19.0</div>
        </div>
        <div style="text-align:right; font-size:0.85rem; opacity:0.9; line-height:1.4;">
            <b>STATUS DO SISTEMA:</b> ONLINE 🟢<br>
            Monitoramento de Alta Precisão
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. BARRA DE CONTROLE (FILTROS) ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade Produtiva")
    city = st.text_input("Busca GPS", placeholder="Ex: Fazenda Santa Maria...", label_visibility="collapsed")
    if st.button("📡 Sincronizar Satélite") and city:
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
        except: st.warning("Estrutura de dados incompleta."); st.stop()
    else: st.error("Banco de dados vazio."); st.stop()

with c3:
    st.markdown("### 📊 Fase Atual")
    fase_sel = st.selectbox("Estádio", fases_disponiveis, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PROCESSAMENTO & COCKPIT INTELIGENTE ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # CÁLCULOS AVANÇADOS (USANDO AGRO_UTILS)
    temp = hoje['Temp']
    umid = hoje['Umid']
    delta_t = hoje['Delta T']
    
    # 1. Cálculo de VPD (Novo!)
    vpd_atual = AgroBrain.calcular_vpd(temp, umid)
    
    # 2. Definição de Status (Lógica de cores)
    # Temperatura
    t_st, t_cor = ("Ótima ✅", "#16a34a") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc2626")
    
    # Delta T (Janela de Aplicação)
    if 2 <= delta_t <= 8: d_st, d_cor = "APTO ✅", "#16a34a"
    elif 8 < delta_t <= 10: d_st, d_cor = "ATENÇÃO ⚠️", "#ca8a04"
    else: d_st, d_cor = "PARE 🛑", "#dc2626"
    
    # VPD Status
    if 0.5 <= vpd_atual <= 1.5: v_st, v_cor = "Ideal 💧", "#2563eb" # Azul
    elif vpd_atual > 2.0: v_st, v_cor = "Estresse 🌵", "#dc2626" # Vermelho (Seco)
    else: v_st, v_cor = "Baixo ☁️", "#ca8a04" # Amarelo (Muito Úmido/Doença)

    # RENDERIZAÇÃO DO COCKPIT (HTML GERADO PELO AGROBRAIN)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(AgroBrain.gerar_cartao_kpi("🌡️ Temperatura", f"{temp:.1f}", "°C", t_st, t_cor), unsafe_allow_html=True)
    with c2: st.markdown(AgroBrain.gerar_cartao_kpi("🛡️ Delta T", f"{delta_t}", "°C", d_st, d_cor, tooltip="Diferença Psicométrica"), unsafe_allow_html=True)
    with c3: st.markdown(AgroBrain.gerar_cartao_kpi("💨 VPD (Pressão)", f"{vpd_atual:.2f}", "kPa", v_st, v_cor, tooltip="Déficit de Pressão de Vapor"), unsafe_allow_html=True)
    with c4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA Acumulado", f"{gda_acum:.0f}", "°GD", f"Ciclo: {dias} dias", "#1f2937"), unsafe_allow_html=True)

    # --- 7. ABAS DE CONTEÚDO (ENTERPRISE) ---
    tabs = st.tabs(["🧬 TÉCNICO & MANEJO", "☁️ CLIMA & RISCO", "📡 RADAR", "👁️ IA VISION", "💰 GESTÃO", "🗺️ GIS MAP", "📄 LAUDO"])

    # ABA 1: TÉCNICO (AGRONOMIA PURA)
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.caption(f"Evolução do Ciclo Fenológico ({progresso*100:.1f}%)")
        st.progress(progresso)

        # --- INÍCIO DO BLOCO DE IMAGENS INTELIGENTE ---
        # 1. Mapeamento da Cultura para Nome do Arquivo
        nome_arquivo = None
        cultura_lower = str(cult_sel).lower()

        # Dicionário de mapeamento (Nome no App -> Nome do Arquivo)
        if "soja" in cultura_lower: nome_arquivo = "soja"
        elif "milho" in cultura_lower: nome_arquivo = "milho"
        elif "algodão" in cultura_lower or "algodao" in cultura_lower: nome_arquivo = "algodao"
        elif "café" in cultura_lower or "cafe" in cultura_lower: nome_arquivo = "cafe"
        elif "feijão" in cultura_lower or "feijao" in cultura_lower: nome_arquivo = "feijao"
        elif "trigo" in cultura_lower: nome_arquivo = "trigo"
        elif "tomate" in cultura_lower: nome_arquivo = "tomate"
        elif "batata" in cultura_lower: nome_arquivo = "batata"
        elif "alho" in cultura_lower: nome_arquivo = "alho"
        elif "cebola" in cultura_lower: nome_arquivo = "cebola"
        elif "uva" in cultura_lower: nome_arquivo = "uva"
        elif "banana" in cultura_lower: nome_arquivo = "banana"
        elif "citros" in cultura_lower or "laranja" in cultura_lower or "limão" in cultura_lower: nome_arquivo = "citros"
        elif "manga" in cultura_lower: nome_arquivo = "manga"
        elif "morango" in cultura_lower: nome_arquivo = "morango"
        elif "mirtilo" in cultura_lower: nome_arquivo = "mirtilo"
        elif "framboesa" in cultura_lower: nome_arquivo = "framboesa"

        # 2. Busca pelo Arquivo Local (Prioridade Máxima)
        img_local_path = None
        if nome_arquivo:
            # Tenta achar .jpg ou .png na pasta 'images'
            potential_jpg = os.path.join("images", f"(nome_arquivo).jpg")
            potential_png = os.path.join("images", f"(nome_arquivo).png")
            
            if os.path.exists(potential_jpg):
                img_local_path = potential_jpg
            elif os.path.exists(potential_png):
                img_local_path = potential_png

        # 3. Renderização (Local ou Genérica)
        st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
        c_img1, c_img2, c_img3 = st.columns([1, 2, 1]) # Centralizar a imagem
        
        with c_img2:
            if img_local_path:
                # MOSTRA A SUA IMAGEM DA PASTA /IMAGES
                st.image(img_local_path, caption=f"Fenologia: {cult_sel}", use_container_width=True)
            else:
                # FALLBACK: Se não tiver imagem na pasta, mostra uma bonita da internet
                st.image("https://images.unsplash.com/photo-1625246333195-58197bd47d26?q=80&w=1000&auto=format&fit=crop", 
                         caption="Imagem Ilustrativa (Adicione foto na pasta /images)", 
                         use_container_width=True)
        # --- FIM DO BLOCO DE IMAGENS ---

        st.divider()

        # Continuação das Colunas Técnicas (Genética e Fisiologia)
        c_tec1, c_tec2 = st.columns(2)
        with c_tec1:
            st.markdown('<div class="section-title">🧬 CARACTERIZAÇÃO GENÉTICA</div>', unsafe_allow_html=True)
            # AgroBrain busca a informação segura
            info_txt = AgroBrain.get_info_segura(info, ['info', 'desc', 'detalhes'])
            st.markdown(f'<div class="info-text"><b>{var_sel}</b><br>{info_txt}</div>', unsafe_allow_html=True)
        
        with c_tec2:
            st.markdown('<div class="section-title">🌱 FISIOLOGIA DO ESTÁDIO</div>', unsafe_allow_html=True)
            fisio_txt = AgroBrain.get_info_segura(dados_fase, ['fisiologia', 'desenvolvimento'])
            st.markdown(f'<div class="info-text">{fisio_txt}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-title">🛡️ DIRETRIZES TÉCNICAS (MANEJO)</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo', 'recomendacao'])
        st.warning(f"🎯 **Ação Recomendada:** {manejo_txt}")

        st.markdown("### 🧪 Protocolo de Defesa (Químico/Biológico)")
        # Renderiza os cards químicos usando o motor inteligente
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        st.markdown('</div>', unsafe_allow_html=True)

       # --- BLOCO DE IMAGENS DINÂMICAS ENTERPRISE ---
        # Dicionário de imagens de alta resolução para as culturas
        img_map = {
            "Algodão": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Cotton_plant.jpg/800px-Cotton_plant.jpg",
            "Soja": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Soybean.jpg/800px-Soybean.jpg",
            "Milho": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Zea_mays_-_Köhler–s_Medizinal-Pflanzen-283.jpg/800px-Zea_mays_-_Köhler–s_Medizinal-Pflanzen-283.jpg",
            "Café": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Coffea_arabica_002.JPG/800px-Coffea_arabica_002.JPG",
            "Feijão": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Phaseolus_vulgaris_002.JPG/800px-Phaseolus_vulgaris_002.JPG",
            "Trigo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Wheat_close-up.JPG/800px-Wheat_close-up.JPG",
            "Tomate": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bright_red_tomato_and_cross_section02.jpg/800px-Bright_red_tomato_and_cross_section02.jpg",
            "Batata": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Patates.jpg/800px-Patates.jpg",
            "Alho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Garlic_bulbs.jpg/800px-Garlic_bulbs.jpg",
            "Cebola": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Onion_on_White.JPG/800px-Onion_on_White.JPG",
            "Uva": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Abb_grape.jpg/800px-Abb_grape.jpg",
            "Banana": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Banana_and_cross_section.jpg/800px-Banana_and_cross_section.jpg",
            "Citros": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Citrus_sinensis_-_Köhler–s_Medizinal-Pflanzen-186.jpg/800px-Citrus_sinensis_-_Köhler–s_Medizinal-Pflanzen-186.jpg",
            "Manga": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mango_and_cross_section.jpg/800px-Mango_and_cross_section.jpg",
            "Morango": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Strawberry_cross_section.jpg/800px-Strawberry_cross_section.jpg"
        }
        
        # Lógica inteligente para encontrar a imagem certa
        img_url = None
        for key, url in img_map.items():
            if key in str(cult_sel): # Se "Algodão" estiver em "Algodão (Gossypium...)"
                img_url = url
                break
        
        if img_url:
            st.image(img_url, width=400)
        else:
            # Imagem genérica bonita se não achar específica
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Farming_cultivated_field.jpg/800px-Farming_cultivated_field.jpg", width=400)

        c_tec1, c_tec2 = st.columns(2)
        with c_tec1:
            st.markdown('<div class="section-title">🧬 CARACTERIZAÇÃO GENÉTICA</div>', unsafe_allow_html=True)
            # AgroBrain busca a informação segura
            info_txt = AgroBrain.get_info_segura(info, ['info', 'desc', 'detalhes'])
            st.markdown(f'<div class="info-text"><b>{var_sel}</b><br>{info_txt}</div>', unsafe_allow_html=True)
        
        with c_tec2:
            st.markdown('<div class="section-title">🌱 FISIOLOGIA DO ESTÁDIO</div>', unsafe_allow_html=True)
            fisio_txt = AgroBrain.get_info_segura(dados_fase, ['fisiologia', 'desenvolvimento'])
            st.markdown(f'<div class="info-text">{fisio_txt}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-title">🛡️ DIRETRIZES TÉCNICAS (MANEJO)</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo', 'recomendacao'])
        st.warning(f"🎯 **Ação Recomendada:** {manejo_txt}")

        st.markdown("### 🧪 Protocolo de Defesa (Químico/Biológico)")
        # Renderiza os cards químicos usando o motor inteligente
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 2: CLIMA & RISCO
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # Gráfico Interativo
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapo (mm)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(title="Balanço Hídrico (15 Dias)", height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de Risco Automática (AgroBrain)
        st.markdown('<div class="section-title">🚨 ANÁLISE DE RISCO AUTOMÁTICA</div>', unsafe_allow_html=True)
        
        # Simula tipo de produto (padrão sistêmico)
        tipo_prod = "Sistêmico" 
        status_ap, cor_ap, lista_alertas = AgroBrain.analisar_risco_aplicacao(temp, umid, delta_t, tipo_prod)
        
        st.markdown(f"**Condição para {tipo_prod}:** <span style='color:{cor_ap}; font-weight:bold; font-size:1.2rem;'>{status_ap}</span>", unsafe_allow_html=True)
        
        if lista_alertas:
            for tit, desc in lista_alertas:
                st.error(f"**{tit}**: {desc}")
        else:
            st.success("✅ Janela de aplicação favorável.")
            
        st.caption("Nota: Esta análise considera temperatura, umidade, Delta T e VPD (Fisiologia da planta).")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Radar Meteorológico (Simulação)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                with cols[i]:
                    bg = "#fee2e2" if r['Chuva'] == "Sim" else "#ecfdf5"
                    cor = "#b91c1c" if r['Chuva'] == "Sim" else "#047857"
                    st.markdown(f"""
                    <div style="background:{bg}; padding:15px; border-radius:10px; text-align:center; border:1px solid {cor}30;">
                        <div style="font-weight:bold; color:#64748b; font-size:0.8rem;">{r["Direcao"]}</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{cor};">{r["Temp"]:.0f}°</div>
                        <div style="font-weight:700; color:{cor};">{r["Chuva"]}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA VISION (GEMINI)
    with tabs[3]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1: 
            st.markdown("### 📸 Diagnóstico Visual")
            st.info("Tire uma foto da folha, praga ou sintoma.")
            img = st.camera_input("Capturar Imagem")
        with c2:
            st.markdown("### 🧠 Parecer AgroBrain AI")
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("Analisando vetores, sintomas e morfologia..."):
                    try:
                        prompt = f"Atue como um Doutor em Agronomia. Cultura: {cult_sel}, Fase: {fase_sel}. Analise a imagem. 1. Identifique o problema. 2. Explique a causa. 3. Sugira controle químico (ingredientes ativos) e biológico."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content([prompt, Image.open(img)])
                        st.markdown(res.text)
                    except: st.error("Erro na comunicação com a IA.")
            else:
                st.markdown("Aguardo imagem para processamento...")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 💰 Gestão Financeira")
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Descrição")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕ Adicionar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        
        if st.session_state['custos']:
            df = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown(f"<div style='text-align:right; font-size:1.5rem; font-weight:bold; color:#064e3b;'>TOTAL: R$ {df['Valor'].sum():,.2f}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA GIS
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            st.markdown("### 📍 Pontos GPS")
            nm = st.text_input("Nome do Ponto")
            if st.button("Gravar Coordenada") and st.session_state.get('last'): 
                st.session_state['pontos_mapa'].append({"n": nm, "lat": st.session_state['last'][0], "lon": st.session_state['last'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.markdown(f"**📍 {p['n']}**")
        with c2:
            m = folium.Map([st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Sat').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            for p in st.session_state['pontos_mapa']: folium.Marker([p['lat'], p['lon']], popup=p['n']).add_to(m)
            out = st_folium(m, height=500, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7: LAUDO
    with tabs[6]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Emissão de Receituário")
        obs = st.text_area("Observações Técnicas")
        
        if st.button("🖨️ Gerar Documento PDF"):
            # Coleta dados seguros
            diag = AgroBrain.get_info_segura(dados_fase, ['desc', 'diagnostico'])
            man = AgroBrain.get_info_segura(dados_fase, ['manejo'])
            
            st.markdown(f"""
            <div style="border:1px solid #9ca3af; padding:50px; background:white; font-family:'Times New Roman'; color:black;">
                <h1 style="text-align:center; font-size:1.5rem; margin-bottom:5px;">AGRO SDI - RECEITUÁRIO TÉCNICO</h1>
                <p style="text-align:center; font-size:0.9rem; color:#4b5563;">Sistema de Decisão Integrada | Emissão Digital</p>
                <hr style="border-top: 2px solid black;">
                
                <table style="width:100%; margin-top:20px;">
                    <tr><td><b>DATA:</b> {date.today().strftime('%d/%m/%Y')}</td><td style="text-align:right;"><b>LOCAL:</b> {city or 'Não Informado'}</td></tr>
                </table>
                
                <h3 style="background:#f3f4f6; padding:8px; margin-top:20px; border-left:4px solid #10b981;">1. IDENTIFICAÇÃO</h3>
                <p><b>Cultura:</b> {cult_sel} &nbsp;&nbsp; <b>Genética:</b> {var_sel}</p>
                <p><b>Estádio:</b> {fase_sel}</p>
                
                <h3 style="background:#f3f4f6; padding:8px; margin-top:20px; border-left:4px solid #10b981;">2. DIAGNÓSTICO</h3>
                <p>{diag}</p>
                
                <h3 style="background:#f3f4f6; padding:8px; margin-top:20px; border-left:4px solid #10b981;">3. PRESCRIÇÃO</h3>
                <p>{man}</p>
                
                <h3 style="background:#f3f4f6; padding:8px; margin-top:20px; border-left:4px solid #10b981;">4. OBSERVAÇÕES</h3>
                <p>{obs}</p>
                
                <br><br><br><br>
                <div style="text-align:center;">
                    _______________________________________<br>
                    <b>Engenheiro Agrônomo Responsável</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
