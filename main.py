# ARQUIVO: main.py
# SISTEMA: AGRO SDI | ENTERPRISE EDITION
# VERSÃO: V-GESTÃO-360 (Estimativa de Safra + Financeiro Real)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
import os
import json

# --- 1. SETUP & SEGURANÇA ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css
    from agro_utils import AgroBrain
    from notification_engine import NotificationSystem
    import market_engine 
except ImportError as e:
    st.error(f"⚠️ Erro Crítico de Sistema: {e.name} não encontrado.")
    st.stop()

st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")
load_css() 

# --- 2. VARIÁVEIS DE SESSÃO (PERSISTÊNCIA) ---
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = [] # MIP
if 'custos_safra' not in st.session_state: st.session_state['custos_safra'] = [] # Gestão
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w = st.query_params.get("w_key", None)
url_g = st.query_params.get("g_key", None)

# --- 3. LOGIN ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="app-card" style="text-align:center; padding:40px;">
            <h1 style="color:#064e3b; margin:0; font-size:2.5rem;">AGRO SDI</h1>
            <p style="color:#6b7280; font-weight:bold; margin-top:10px; letter-spacing:1px;">PLATAFORMA INTEGRADA DE GESTÃO</p>
        </div>""", unsafe_allow_html=True)
        kw = st.text_input("CHAVE OPENWEATHER", type="password")
        kg = st.text_input("CHAVE GEMINI (Opcional)", type="password") # Deixei opcional pois tiramos a aba IA
        if st.button("ACESSAR PAINEL", type="primary", use_container_width=True):
            if kw: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# ==============================================================================
# 💎 HEADER & TICKER
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
# 💎 FILTROS GLOBAIS (SISTEMA DE MEMÓRIA PERSISTENTE & GPS)
# ==============================================================================
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

# --- 1. MÓDULO GPS (MEMÓRIA DE LOCALIZAÇÃO) ---
with c1:
    st.markdown("### 📍 Unidade")
    # Tenta recuperar o último local digitado, senão usa vazio
    default_gps = st.session_state.get('last_city', '')
    city = st.text_input("GPS", value=default_gps, placeholder="Digitar Cidade ou Fazenda...", label_visibility="collapsed")
    
    # Botão de Sincronia com Feedback
    if st.button("📡 Sincronizar Local", use_container_width=True):
        if city:
            # Busca Coordenadas
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: 
                st.session_state['loc_lat'] = lat
                st.session_state['loc_lon'] = lon
                st.session_state['last_city'] = city # Salva na memória para não sumir
                st.toast(f"✅ GPS Calibrado: {city.upper()}", icon="🛰️")
                # Não usamos st.rerun() aqui desnecessariamente para evitar piscar, 
                # o fluxo segue e atualiza os dados abaixo naturalmente.
            else:
                st.toast("⚠️ Local não encontrado. Tente cidade próxima.", icon="❌")
        else:
            st.toast("⚠️ Digite o nome da fazenda ou cidade.", icon="⌨️")

# --- 2. SELETOR DE CULTURA (COM MEMÓRIA KEY) ---
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        # AQUI ESTÁ O SEGREDO: key="sessao_cultura"
        # Isso impede que o valor volte para 'Algodão' quando o GPS roda.
        cult_sel = st.selectbox(
            "Cultura", 
            sorted(list(BANCO_MASTER.keys())), 
            label_visibility="collapsed",
            key="sessao_cultura" 
        )
        
        # Atualiza as listas baseadas na cultura selecionada
        vars_disp = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
        fases_disp = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
        
        var_sel = st.selectbox(
            "Genética", 
            vars_disp,
            key="sessao_genetica" # Memória para a Genética
        )
    else: 
        st.error("Banco de Dados Offline")
        st.stop()

# --- 3. SELETOR DE FASE (COM MEMÓRIA KEY) ---
with c3:
    st.markdown("### 📊 Fase")
    fase_sel = st.selectbox(
        "Estádio", 
        fases_disp, 
        label_visibility="collapsed",
        key="sessao_fase" # Memória para a Fase
    )

# --- 4. DATA DE PLANTIO (COM MEMÓRIA KEY) ---
with c4:
    st.markdown("### 📆 Safra")
    # Se não tiver data na sessão, define hoje
    if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date.today()
    
    st.session_state['d_plantio'] = st.date_input(
        "Plantio", 
        st.session_state['d_plantio'], 
        label_visibility="collapsed",
        key="sessao_data"
    )
    dias = (date.today() - st.session_state['d_plantio']).days

st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSAMENTO PRINCIPAL ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))
    temp, umid, delta_t = hoje['Temp'], hoje['Umid'], hoje['Delta T']
    vpd = AgroBrain.calcular_vpd(temp, umid)
    
    # Cores KPI
    t_st, t_cor = ("Ótima ✅", "#16a34a") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc2626")
    d_st, d_cor = ("APTO ✅", "#16a34a") if 2 <= delta_t <= 8 else ("PARE 🛑", "#dc2626")
    v_st, v_cor = ("Ideal 💧", "#2563eb") if 0.5 <= vpd <= 1.5 else ("Estresse 🌵", "#dc2626")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(AgroBrain.gerar_cartao_kpi("🌡️ Temperatura", f"{temp:.1f}", "°C", t_st, t_cor), unsafe_allow_html=True)
    with c2: st.markdown(AgroBrain.gerar_cartao_kpi("🛡️ Delta T", f"{delta_t}", "°C", d_st, d_cor), unsafe_allow_html=True)
    with c3: st.markdown(AgroBrain.gerar_cartao_kpi("💨 VPD (Pressão)", f"{vpd:.2f}", "kPa", v_st, v_cor), unsafe_allow_html=True)
    with c4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA Acumulado", f"{gda_acum:.0f}", "°GD", f"Ciclo: {dias}d", "#1e293b"), unsafe_allow_html=True)

    # ==============================================================================
    # 💎 ABAS DE NAVEGAÇÃO (NOVA ORDEM)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    # Removemos IA e Laudo, adicionamos Gestão em destaque
    tabs = st.tabs(["🧬 TÉCNICO", "🧪 NUTRIÇÃO", "☁️ CLIMA", "📡 RADAR", "🗺️ MAPA", "💰 GESTÃO", "🔔 ALERTAS"])

    # 1. TÉCNICO
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.caption(f"Evolução do Ciclo: {progresso*100:.1f}%")
        st.progress(progresso)

        # Imagem da Cultura
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
            if img_path: st.image(img_path, caption=f"Fase: {fase_sel}", use_container_width=True)
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
        st.warning(f"🎯 **Recomendação:** {manejo_txt}")
        
        st.markdown("### 🧪 Defensivos Sugeridos")
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        st.markdown('</div>', unsafe_allow_html=True)


                                                       # 2. NUTRIÇÃO (MARCHA DE ABSORÇÃO & MANEJO - CALIBRADO TOTAL HIGH-YIELD)
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        

      # --- 2. BANCO DE DADOS MASTER (COM META DE PRODUTIVIDADE EXPLÍCITA) ---
        DB_NUTRI_MASTER = {
            "Soja": {
                "meta": "75 a 90 sacas/ha", # <--- ADICIONEI ISSO AQUI EM TODAS
                "fases": ["V1", "V4", "R1 (Flor)", "R5.1 (Ench)", "R8 (Mat)"],
                "macros": {"N": [10, 40, 110, 280, 380], "P": [2, 8, 20, 35, 40], "K": [10, 40, 100, 180, 200], "Ca": [5, 25, 60, 90, 110], "Mg": [2, 10, 25, 40, 50], "S": [2, 8, 20, 35, 45]},
                "micros": {"Mn": [20, 100, 300, 500, 600], "Zn": [10, 50, 150, 300, 350], "B": [5, 20, 60, 100, 120]},
                "totais_display": {"N": "300 – 400", "P": "30 – 50", "K": "180 – 230", "Ca": "90 – 120", "Mg": "40 – 60", "S": "30 – 50"},
                "manejo_tatico": {
                    "N": "<b>ALTA PERFORMANCE (FBN):</b> Proibido aplicar N mineral (ureia/sulfato) na base ou cobertura, pois inibe a nodulação. O segredo de 85+ sacas é: Inoculação Turbo (Turfa + Líquido) + Co-inoculação (Azospirillum) + Cobalto/Molibdênio foliar em V3.",
                    "P": "<b>ENERGIA (ATP):</b> Aplicar 100% no sulco ou pré-plantio incorporado. Níveis de P no solo devem ser > 15-20 mg/dm³. Se usar MAP, cuidado com a salinidade junto à semente.",
                    "K": "<b>ENCHIMENTO DE GRÃO:</b> A extração é violenta no final do ciclo (R5). Se o solo for arenoso (CTC baixa), parcele o K: 50% pré-plantio e 50% em V4 (a lanço). Isso evita lixiviação e queima de raiz."
                }
            },
            "Milho": {
                "meta": "180 a 220 sacas/ha",
                "fases": ["V2", "V6", "VT (Pendão)", "R3 (Leitoso)", "R6 (Matur)"],
                "macros": {"N": [10, 60, 160, 240, 280], "P": [2, 15, 40, 55, 60], "K": [15, 90, 200, 240, 260], "Ca": [5, 25, 50, 65, 75], "Mg": [3, 15, 35, 50, 60], "S": [2, 10, 25, 35, 40]},
                "micros": {"Zn": [20, 150, 400, 550, 600], "Mn": [15, 100, 300, 400, 450], "B": [10, 30, 80, 120, 140]},
                "totais_display": {"N": "240 – 300", "P": "50 – 80", "K": "220 – 280", "Ca": "60 – 90", "Mg": "40 – 70", "S": "35 – 50"},
                "manejo_tatico": {
                    "N": "<b>DEFINIÇÃO DE TETO (V4-V6):</b> O número de fileiras da espiga é definido agora. A planta não pode passar fome de N aqui. Aplique 70% da dose de cobertura até V6 impreterivelmente. Atrasar cobertura reduz teto produtivo.",
                    "Zn": "<b>ELEMENTO CHAVE:</b> O milho é extremamente exigente em Zinco. Se o solo for pobre, usar Zn no sulco ou tratamento de semente robusto. Deficiência de Zn encurta os entrenós e reduz área foliar.",
                    "K": "<b>RESISTÊNCIA:</b> Equilíbrio N:K é vital. Excesso de N sem K proporcional gera plantas com colmo fraco, suscetíveis a tombamento (acamamento) e quebramento."
                }
            },
            "Café": { 
                "meta": "60 a 90 sacas/ha",
                "fases": ["Veg/Flor", "Chumbinho", "Expansão", "Granação", "Maturação"],
                "macros": {"N": [40, 100, 180, 260, 300], "P": [5, 15, 25, 35, 40], "K": [30, 90, 180, 280, 330], "Ca": [30, 60, 100, 140, 160], "Mg": [10, 25, 45, 60, 70], "S": [10, 20, 35, 50, 60]},
                "micros": {"Fe": [200, 1000, 2000, 2500, 3000], "B": [50, 250, 500, 700, 800], "Zn": [40, 200, 400, 550, 600]},
                "totais_display": {"N": "280 – 350", "P": "35 – 50", "K": "300 – 400", "Ca": "140 – 180", "Mg": "50 – 80", "S": "40 – 60"},
                "manejo_tatico": {
                    "N": "<b>VEGETAÇÃO E CARGA:</b> Parcelar em 3 ou 4x (Set a Mar). Para altas cargas (>80sc), a demanda na fase de expansão (Dez/Jan) é crítica. Use Nitrato de Amônio se não houver previsão de chuva imediata (menor volatilização).",
                    "K": "<b>DIE-BACK (SECA DE PONTEIROS):</b> Na fase de Granação (Jan-Mar), o fruto drena todo o K das folhas. Se faltar K no solo, a planta sacrifica as folhas e os ramos secam, prejudicando a safra seguinte.",
                    "B": "<b>PEGAMENTO DE FLOR:</b> Boro foliar na pré-florada e chumbinho é obrigatório. O Boro é imóvel no floema do café, precisa de aplicações localizadas nas rosetas."
                }
            },
            "Batata": {
                "meta": "45 a 60 ton/ha",
                "fases": ["Emerg", "Estolon", "Tuber", "Enchimento", "Maturação"],
                "macros": {"N": [20, 70, 140, 190, 220], "P": [5, 20, 40, 55, 60], "K": [30, 100, 220, 320, 360], "Ca": [10, 40, 80, 100, 120], "Mg": [5, 20, 40, 55, 65], "S": [5, 15, 30, 45, 55]},
                "micros": {"Mn": [30, 120, 280, 450, 500], "B": [8, 30, 70, 100, 120], "Zn": [15, 50, 120, 180, 220]},
                "totais_display": {"N": "220 – 300", "P": "80 – 120", "K": "350 – 500", "Ca": "80 – 150", "Mg": "30 – 60", "S": "25 – 50"},
                "manejo_tatico": {
                    "P": "<b>TUBERIZAÇÃO:</b> Fósforo no sulco define o NÚMERO de tubérculos por planta. Use fontes solúveis. P deficiente = poucos tubérculos grandes.",
                    "K": "<b>FONTE NOBRE:</b> Para batata indústria (chips/frita), use Sulfato de Potássio (SOP). O Cloreto (KCl) reduz o teor de amido e aumenta a absorção de água, piorando a fritura.",
                    "Ca": "<b>SARNA E PELE:</b> Cálcio reforça a parede celular da casca, reduzindo incidência de Sarna e danos mecânicos na colheita."
                }
            },
            "Algodão": {
                "meta": "350 a 450 @/ha",
                "fases": ["Emerg", "Botão", "Flor", "Maçã", "Abertura"],
                "macros": {"N": [10, 50, 120, 180, 200], "P": [2, 15, 35, 50, 60], "K": [10, 60, 140, 200, 220], "Ca": [5, 30, 80, 120, 140], "Mg": [2, 10, 25, 40, 45], "S": [2, 10, 25, 40, 50]},
                "micros": {"B": [20, 100, 250, 350, 400], "Zn": [15, 80, 180, 250, 300]},
                "totais_display": {"N": "180 – 220", "P": "50 – 70", "K": "200 – 250", "Ca": "120 – 160", "Mg": "40 – 60", "S": "40 – 60"},
                "manejo_tatico": {
                    "N": "<b>VIGOR CONTROLADO:</b> Algodão não pode 'disparar'. O N deve ser acompanhado de Regulador de Crescimento (Mepiquat). Planta muito vegetativa aborta as maçãs do baixeiro.",
                    "K": "<b>QUALIDADE DE FIBRA:</b> A 'Fome de Potássio' (Oulakh) ocorre no pico de carga. K baixo resulta em fibra com Micronaire (finura) baixo, desvalorizando o produto final.",
                    "B": "<b>RETENÇÃO:</b> A demanda de Boro na florada é altíssima. O solo sozinho não supre. Fazer de 3 a 5 aplicações foliares sequenciais para segurar as estruturas reprodutivas."
                }
            },
            "Citros": {
                "meta": "1200 a 1800 cx/ha",
                "fases": ["Brotação", "Flor", "Fruto I", "Fruto II", "Colheita"],
                "macros": {"N": [30, 80, 150, 220, 250], "P": [5, 12, 20, 30, 35], "K": [20, 70, 150, 220, 260], "Ca": [40, 100, 180, 220, 240], "Mg": [10, 25, 45, 60, 70], "S": [10, 25, 40, 55, 65]},
                "micros": {"Mn": [50, 250, 500, 700, 800], "Zn": [50, 250, 500, 700, 800], "B": [30, 100, 200, 300, 350]},
                "totais_display": {"N": "200 – 280", "P": "30 – 50", "K": "220 – 300", "Ca": "200 – 280", "Mg": "60 – 80", "S": "50 – 70"},
                "manejo_tatico": {
                    "N": "<b>FLUXOS VEGETATIVOS:</b> Sincronizar adubação nitrogenada com os fluxos de brotação (Primavera/Verão). Árvore bem enfolhada suporta carga e protege frutos do sol.",
                    "Ca": "<b>CREASING (RACHADURA):</b> O Ca é o 'cimento' da casca (albedo). Deficiência causa rachadura (Creasing) e colapso da casca pós-colheita. Usar Nitrato de Cálcio via solo.",
                    "Mg": "<b>CLOROSE V:</b> Deficiência de Mg causa o 'V amarelo' nas folhas velhas, reduzindo fotossíntese e tamanho de fruto."
                }
            },
            "Banana": {
                "meta": "80 a 100 ton/ha",
                "fases": ["Cresc", "Flor", "Cacho", "Enchimento", "Colheita"],
                "macros": {"N": [50, 150, 300, 450, 550], "P": [10, 30, 50, 70, 80], "K": [100, 400, 900, 1300, 1600], "Ca": [30, 80, 180, 250, 300], "Mg": [15, 40, 90, 130, 150], "S": [15, 40, 80, 100, 120]},
                "micros": {"Mn": [150, 600, 1800, 2800, 3500], "Zn": [30, 150, 400, 600, 700], "B": [15, 60, 180, 280, 350]},
                "totais_display": {"N": "400 – 600", "P": "60 – 90", "K": "1400 – 1800", "Ca": "250 – 350", "Mg": "120 – 160", "S": "80 – 120"},
                "manejo_tatico": {
                    "K": "<b>BOMBA DE POTÁSSIO:</b> A banana exporta 1600kg de K/ha. É impossível aplicar tudo de uma vez. Parcelar em 10 a 12 aplicações anuais. Sem K, o cacho não enche e o 'pescoço' quebra.",
                    "N": "<b>RITMO CONSTANTE:</b> A planta emite uma folha nova a cada 7-10 dias. Se faltar N, a emissão para. Aplicação mensal ou quinzenal obrigatória.",
                    "Ca": "<b>EQUILÍBRIO IÔNICO:</b> Com tanto Potássio aplicado, ocorre inibição competitiva de Cálcio e Magnésio ('Azul da Banana'). Obrigatório aplicar Ca e Mg via calcário ou gesso regularmente."
                }
            },
            "Tomate": {
                "meta": "120 a 140 ton/ha",
                "fases": ["Veg", "Flor 1", "Fruto 1", "Fruto Total", "Colheita"],
                "macros": {"N": [20, 60, 150, 250, 300], "P": [5, 20, 40, 50, 60], "K": [30, 100, 250, 400, 480], "Ca": [20, 70, 160, 220, 250], "Mg": [10, 30, 60, 80, 90], "S": [10, 30, 60, 80, 90]},
                "micros": {"Mn": [25, 180, 450, 650, 750], "B": [15, 60, 140, 220, 280], "Zn": [15, 70, 180, 280, 350]},
                "totais_display": {"N": "250 – 350", "P": "60 – 90", "K": "450 – 600", "Ca": "200 – 280", "Mg": "70 – 100", "S": "70 – 100"},
                "manejo_tatico": {
                    "Ca": "<b>FUNDO PRETO (PODRIDÃO APICAL):</b> O cálcio é imóvel e não chega na ponta do fruto rápido o suficiente. Pulverizações semanais de Cloreto de Cálcio ou quelatos direcionadas aos frutos são mandatórias.",
                    "N": "<b>VÍCIO:</b> Excesso de N na fase inicial cria plantas com entrenós longos e pouca flor. Segurar o N até o pegamento do primeiro cacho.",
                    "K": "<b>BRIX E COR:</b> O Potássio é responsável pela translocação de açúcares. K baixo resulta em tomate manchado (blotchy ripening) e sem sabor."
                }
            },
            "Feijão": {
                "meta": "50 a 65 sacas/ha",
                "fases": ["V2", "V4", "R5", "R7", "R9"],
                "macros": {"N": [10, 40, 90, 130, 150], "P": [3, 10, 20, 30, 35], "K": [10, 35, 80, 110, 130], "Ca": [5, 25, 60, 80, 90], "Mg": [3, 12, 25, 35, 40], "S": [2, 8, 15, 20, 25]},
                "micros": {"Fe": [60, 250, 700, 1100, 1300], "Mn": [25, 100, 250, 350, 400], "Zn": [15, 50, 120, 180, 220]},
                "totais_display": {"N": "120 – 160", "P": "30 – 45", "K": "100 – 140", "Ca": "70 – 90", "Mg": "30 – 45", "S": "20 – 30"},
                "manejo_tatico": {
                    "N": "<b>TIMING PERFEITO:</b> O ciclo é muito rápido. Aplique 1/3 no plantio e 2/3 em cobertura V3/V4. Passou de V4, o N não recupera mais o potencial produtivo.",
                    "Mo": "<b>MOLIBDÊNIO:</b> Essencial para a enzima Nitrato Redutase. Aplicação foliar em V3/V4 melhora drasticamente o aproveitamento do Nitrogênio aplicado.",
                    "Micros": "<b>FERRO E MANGANÊS:</b> Feijão é muito sensível a clorose férrica em solos de pH alto. Atenção aos micronutrientes foliares."
                }
            },
            "Trigo": {
                "meta": "90 a 110 sacas/ha",
                "fases": ["Emerg", "Perfilho", "Along", "Espiga", "Grão"],
                "macros": {"N": [15, 50, 110, 150, 170], "P": [5, 15, 30, 40, 45], "K": [10, 40, 100, 130, 150], "Ca": [5, 20, 45, 60, 70], "Mg": [3, 10, 20, 30, 35], "S": [5, 15, 30, 45, 50]},
                "micros": {"Mn": [30, 150, 350, 450, 500], "Cu": [5, 15, 35, 50, 60], "Zn": [10, 30, 70, 100, 120]},
                "totais_display": {"N": "150 – 180", "P": "40 – 55", "K": "130 – 160", "Ca": "50 – 80", "Mg": "25 – 40", "S": "30 – 50"},
                "manejo_tatico": {
                    "N": "<b>TRÍPLICE ESTRATÉGIA:</b> 1. Base (Arranque). 2. Perfilhamento (Define nº de espigas). 3. Emborrachamento (Define teor de proteína/glúten). Fracionar é a chave.",
                    "Cu": "<b>SANIDADE E PÓLEN:</b> Cobre é vital no trigo. Deficiência causa esterilidade masculina (espigas chochas) e menor resistência a doenças fúngicas.",
                    "K": "<b>ACAMAMENTO:</b> Trigo de alta produtividade (espiga pesada) tomba fácil. Potássio reforça a parede celular do colmo, funcionando como o 'esqueleto' da planta."
                }
            },
            "Uva": {
                "meta": "Alta qualidade (Mesa/Vinho)",
                "fases": ["Brota", "Flor", "Varaison", "Maturação", "Colheita"],
                "macros": {"N": [20, 60, 100, 120, 130], "P": [5, 12, 20, 30, 35], "K": [15, 50, 120, 180, 220], "Ca": [15, 50, 100, 130, 150], "Mg": [5, 20, 40, 55, 65], "S": [5, 15, 30, 40, 50]},
                "micros": {"Fe": [60, 250, 600, 800, 900], "B": [15, 60, 120, 180, 220], "Zn": [15, 50, 120, 180, 250]},
                "totais_display": {"N": "100 – 140", "P": "30 – 40", "K": "180 – 240", "Ca": "120 – 160", "Mg": "50 – 70", "S": "40 – 60"},
                "manejo_tatico": {
                    "K": "<b>AÇÚCAR (BRIX):</b> O Potássio é o motor da translocação de açúcar para a baga. Aumentar a dose a partir da mudança de cor (Varaison) para garantir doçura.",
                    "Mg": "<b>DESSECAÇÃO DA RÁQUIS:</b> Distúrbio fisiológico grave (Palo Negro) causado por falta de Mg/Ca. As bagas murcham e caem. Aplicações preventivas de Magnésio no cacho são necessárias.",
                    "N": "<b>SUSPENSÃO:</b> Cortar o Nitrogênio na fase de maturação. N tardio deixa a baga aguada, com pele fina e propensa a podridão."
                }
            },
            "Manga": {
                "meta": "30 a 45 ton/ha",
                "fases": ["Veg", "Flor", "Chumbinho", "Expansão", "Colheita"],
                "macros": {"N": [30, 80, 140, 180, 200], "P": [5, 20, 35, 50, 60], "K": [20, 70, 160, 240, 280], "Ca": [20, 70, 140, 180, 220], "Mg": [10, 30, 60, 80, 95], "S": [10, 25, 50, 70, 80]},
                "micros": {"B": [15, 80, 160, 240, 280], "Fe": [60, 250, 700, 900, 1100], "Zn": [25, 100, 200, 280, 350]},
                "totais_display": {"N": "180 – 220", "P": "50 – 70", "K": "250 – 300", "Ca": "200 – 240", "Mg": "80 – 100", "S": "60 – 80"},
                "manejo_tatico": {
                    "N": "<b>INDUÇÃO FLORAL:</b> O N estimula vegetação. Deve ser suspenso 60 dias antes da indução (Paclobutrazol) para causar o estresse necessário para a planta florir.",
                    "Ca": "<b>COLAPSO INTERNO:</b> Distúrbio fisiológico (Soft Nose) que apodrece a manga de dentro para fora na prateleira. Cálcio via solo e foliar na fase de chumbinho é a única prevenção.",
                    "B": "<b>PEGAMENTO:</b> Manga tem taxa de abortamento alta natural. Boro e Zinco na pré-florada aumentam a viabilidade do pólen e a fixação dos frutinhos."
                }
            },
            "Morango": {
                "meta": "Alta performance (Estufa)",
                "fases": ["Plantio", "Flor", "Fruto Inic", "Pico", "Final"],
                "macros": {"N": [10, 40, 90, 150, 180], "P": [5, 15, 25, 40, 50], "K": [10, 50, 120, 220, 280], "Ca": [10, 40, 90, 140, 170], "Mg": [5, 15, 40, 60, 75], "S": [5, 15, 30, 50, 60]},
                "micros": {"Fe": [30, 120, 350, 550, 650], "Mn": [15, 70, 200, 300, 350], "B": [8, 30, 70, 100, 120]},
                "totais_display": {"N": "150 – 200", "P": "40 – 60", "K": "250 – 300", "Ca": "150 – 180", "Mg": "60 – 80", "S": "50 – 70"},
                "manejo_tatico": {
                    "N:K": "<b>EQUILÍBRIO:</b> Na fase vegetativa use 1:1. Na frutificação mude para 1:1.5 ou 1:2. Excesso de N gera fruto mole e Botrytis.",
                    "Ca": "<b>FIRMEZA:</b> Morango é pura água e parede celular. Sem Cálcio constante na fertirrigação, a fruta perde 'shelf-life' (tempo de prateleira) e vaza líquido.",
                    "Fe": "<b>CLOROSE:</b> Morango em substrato inerte tende a ter deficiência de Ferro (folhas novas amarelas). Usar Ferro EDDHA (quelato) na solução nutritiva."
                }
            },
            "Mirtilo": {
                "meta": "15 a 20 ton/ha",
                "fases": ["Brota", "Flor", "Verde", "Matur", "Dorm"],
                "macros": {"N": [10, 30, 60, 90, 100], "P": [2, 8, 15, 20, 25], "K": [10, 30, 60, 90, 110], "Ca": [5, 20, 40, 60, 70], "Mg": [2, 10, 20, 30, 35], "S": [5, 15, 30, 45, 55]},
                "micros": {"Fe": [20, 80, 150, 220, 250], "Mn": [10, 40, 80, 120, 150]},
                "totais_display": {"N": "80 – 120", "P": "20 – 30", "K": "100 – 130", "Ca": "60 – 80", "Mg": "30 – 40", "S": "40 – 60"},
                "manejo_tatico": {
                    "N": "<b>FORMA AMONIACAL:</b> O Mirtilo evoluiu em solos ácidos e não metaboliza bem Nitratos. Use Sulfato de Amônio ou Ureia. Evite Nitrato de Cálcio/Potássio em excesso.",
                    "pH": "<b>ACIDIFICAÇÃO:</b> O pH da rizosfera deve estar entre 4.5 e 5.5. Se subir, o Ferro fica indisponível. Injete ácido (fosfórico/sulfúrico) na irrigação se necessário.",
                    "K": "<b>SENSIBILIDADE:</b> Mirtilo é sensível a Cloro e Salinidade. Jamais use Cloreto de Potássio (KCl). Use apenas Sulfato de Potássio (SOP)."
                }
            },
            "Cebola": {
                "meta": "70 a 90 ton/ha",
                "fases": ["Mudas", "Cresc", "Bulbo", "Mat", "Estalo"],
                "macros": {"N": [10, 50, 120, 160, 180], "P": [5, 20, 40, 50, 60], "K": [10, 60, 150, 200, 240], "Ca": [5, 30, 80, 110, 130], "Mg": [3, 12, 30, 45, 55], "S": [10, 30, 60, 80, 100]},
                "micros": {"Mn": [20, 80, 200, 350, 400], "Zn": [10, 50, 120, 180, 220], "B": [5, 20, 50, 80, 100]},
                "totais_display": {"N": "160 – 200", "P": "50 – 70", "K": "220 – 280", "Ca": "100 – 140", "Mg": "40 – 60", "S": "60 – 90"},
                "manejo_tatico": {
                    "N": "<b>ESTALO:</b> O Nitrogênio deve ser suspenso assim que os bulbos começarem a formar ou no início do 'estalo' (tombamento). N tardio causa 'pescoço grosso', rebrota e podridão no armazém.",
                    "S": "<b>PUNGÊNCIA:</b> O Enxofre é responsável pelo cheiro e sabor (ácido pirúvico) da cebola. Em solos pobres em S, a cebola fica 'fraca' e suscetível a ácaros.",
                    "K": "<b>PELE:</b> Potássio abundante garante número de cera nas folhas (proteção) e catáfilos (casca) resistentes, melhorando a cura pós-colheita."
                }
            },
            "Alho": {
                "meta": "15 a 18 ton/ha",
                "fases": ["Emerg", "Veg", "Bulbo", "Mat", "Colheita"],
                "macros": {"N": [10, 60, 140, 160, 170], "P": [5, 20, 40, 50, 55], "K": [10, 70, 160, 200, 220], "Ca": [5, 35, 80, 100, 110], "Mg": [3, 15, 35, 50, 60], "S": [10, 30, 60, 80, 90]},
                "micros": {"Zn": [10, 60, 140, 180, 220], "B": [5, 25, 60, 90, 100]},
                "totais_display": {"N": "150 – 180", "P": "45 – 60", "K": "200 – 240", "Ca": "100 – 120", "Mg": "50 – 70", "S": "80 – 100"},
                "manejo_tatico": {
                    "N": "<b>DENTE DE CACHORRO:</b> O alho precisa de N no início para formar folhas. Porém, na fase de diferenciação (formação dos dentes), o excesso de N causa o superbrotamento (anomalia fisiológica). Corte o N no momento certo.",
                    "P": "<b>ENRAIZAMENTO:</b> O sistema radicular do alho é fasciculado e pouco eficiente. Fósforo disponível no sulco é vital para arranque.",
                    "K": "<b>PESO:</b> O Potássio é o principal responsável pelo enchimento e peso final da cabeça. Deficiência gera bulbos 'ocos' ou leves."
                }
            },
            "Pastagens": {
                "meta": "Intensiva (Corte/Rotacionado)",
                "fases": ["D0", "D10", "D20", "D30", "D45"],
                "macros": {"N": [10, 60, 150, 250, 300], "P": [5, 15, 30, 40, 45], "K": [10, 50, 140, 220, 280], "Ca": [5, 20, 50, 70, 80], "Mg": [2, 10, 25, 40, 50], "S": [5, 15, 30, 50, 60]},
                "micros": {"Mn": [20, 80, 200, 350, 400], "Zn": [10, 50, 120, 180, 220]},
                "totais_display": {"N": "250 – 350", "P": "40 – 60", "K": "250 – 350", "Ca": "70 – 100", "Mg": "40 – 60", "S": "50 – 70"},
                "manejo_tatico": {
                    "N": "<b>MOTOR DE PRODUÇÃO:</b> O N deve ser aplicado IMEDIATAMENTE após a saída dos animais (rotacionado), desde que haja umidade. É ele que empurra a rebrota rápida.",
                    "P": "<b>RESPOSTA:</b> Não adianta jogar N se o P estiver baixo. O Fósforo é o combustível energético. Reposição anual de P (superfosfato) é necessária em sistemas intensivos.",
                    "K": "<b>RECICLAGEM vs CORTE:</b> Em pastejo, 80% do K volta na urina. Em sistemas de corte (Feno/Silagem), a planta leva o K embora. A reposição deve ser muito maior em capineiras de corte."
                }
            },
            "Framboesa": {
                "meta": "Alta Produtividade",
                "fases": ["Veg", "Flor", "Verde", "Colheita", "Senesc"],
                "macros": {"N": [10, 30, 60, 80, 90], "P": [2, 8, 15, 20, 25], "K": [10, 35, 70, 100, 110], "Ca": [5, 20, 40, 60, 70], "Mg": [2, 8, 15, 25, 30], "S": [2, 8, 15, 20, 25]},
                "micros": {"Fe": [20, 80, 150, 200, 250], "B": [5, 15, 30, 45, 50]},
                "totais_display": {"N": "80 – 100", "P": "20 – 30", "K": "100 – 120", "Ca": "60 – 80", "Mg": "25 – 35", "S": "20 – 30"},
                "manejo_tatico": {
                    "N": "<b>EQUILÍBRIO:</b> Parcelar a oferta de nitrogênio principalmente na primavera e início do verão. Excesso tardio gera ramos moles e suscetíveis a doenças.",
                    "P": "<b>MANUTENÇÃO:</b> Aplicar anualmente no início da primavera para suportar o novo fluxo de raízes e brotos.",
                    "K": "<b>DOÇURA:</b> Vital para a translocação de açúcares. Aplique potássio consistentemente durante a formação do fruto para garantir sabor e qualidade."
                }
            }
        }

        dados_nutri = None
        nome_cultura_exibicao = str(cult_sel)
        
        # Lógica de Busca Inteligente
        for chave in DB_NUTRI_MASTER:
            if chave.lower() in str(cult_sel).lower() or str(cult_sel).lower() in chave.lower():
                dados_nutri = DB_NUTRI_MASTER[chave]
                nome_cultura_exibicao = chave
                break
        
        # Fallbacks (Cítricos e Frutas Vermelhas)
        if not dados_nutri and ("citrus" in str(cult_sel).lower() or "limão" in str(cult_sel).lower() or "laranja" in str(cult_sel).lower()):
            dados_nutri = DB_NUTRI_MASTER["Citros"]
            nome_cultura_exibicao = "Citros"
        
        if not dados_nutri and ("berry" in str(cult_sel).lower() or "framboesa" in str(cult_sel).lower()):
             dados_nutri = DB_NUTRI_MASTER["Framboesa"]
             nome_cultura_exibicao = "Framboesa"


        if dados_nutri:
            
            # Recupera a meta do banco de dados (COM SEGURANÇA)
            meta_produtividade = dados_nutri.get("meta", "Consulte Agrônomo")

            # Layout do Cabeçalho com KPI
            c_head_n1, c_head_n2 = st.columns([2.5, 1.5])
            
            with c_head_n1:
                st.markdown(f"### 🧪 Nutrição High-Yield: **{nome_cultura_exibicao}**")
                st.caption("Curvas de Absorção para Tetos Produtivos (Fisiologia de Alta Performance)")
                
            with c_head_n2:
                # CARD DE META (KPI VISUAL)
                st.markdown(f"""
                <div style="
                    background-color: #fef2f2; 
                    border: 1px solid #ef4444; 
                    border-radius: 8px; 
                    padding: 8px 12px; 
                    text-align: right; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="color: #ef4444; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
                        🎯 META ALVO
                    </div>
                    <div style="color: #991b1b; font-size: 1.1rem; font-weight: 800;">
                        {meta_produtividade}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # --- 3. SELEÇÃO DA CULTURA ---
        dados_nutri = None
        nome_cultura_exibicao = str(cult_sel)
        
        for chave in DB_NUTRI_MASTER:
            if chave.lower() in str(cult_sel).lower() or str(cult_sel).lower() in chave.lower():
                dados_nutri = DB_NUTRI_MASTER[chave]
                nome_cultura_exibicao = chave
                break
        
        if not dados_nutri and ("citrus" in str(cult_sel).lower() or "limão" in str(cult_sel).lower() or "laranja" in str(cult_sel).lower()):
            dados_nutri = DB_NUTRI_MASTER["Citros"]
            nome_cultura_exibicao = "Citros"
        
        # Fallback genérico para Framboesa ou outras frutas vermelhas se não achar
        if not dados_nutri and ("berry" in str(cult_sel).lower() or "framboesa" in str(cult_sel).lower()):
             dados_nutri = DB_NUTRI_MASTER["Framboesa"]
             nome_cultura_exibicao = "Framboesa"

        if dados_nutri:
            
           # --- 4. PAINEL QUÍMICO (ATUALIZADO PARA RANGES/FAIXAS) ---
            st.markdown(f"#### ⚛️ Demanda Total (Extração High-Yield: {nome_cultura_exibicao})")
            st.caption("Quantidade total extraída (Kg/ha) para atingir o teto produtivo.")

            # Função auxiliar para pegar a faixa ou o último valor do gráfico
            def get_range(nutriente, default_list):
                # Tenta pegar a string "220 - 300" do dicionário novo
                range_str = dados_nutri.get('totais_display', {}).get(nutriente)
                if range_str:
                    return range_str
                # Se não existir, pega o último número da lista (ex: 200) e formata
                return f"{default_list[-1]}"

            # Busca os valores (agora são Faixas Strings ou Números)
            n_val = get_range('N', dados_nutri['macros'].get('N', [0]))
            p_val = get_range('P', dados_nutri['macros'].get('P', [0]))
            k_val = get_range('K', dados_nutri['macros'].get('K', [0]))
            ca_val = get_range('Ca', dados_nutri['macros'].get('Ca', [0]))
            mg_val = get_range('Mg', dados_nutri['macros'].get('Mg', [0]))
            s_val = get_range('S', dados_nutri['macros'].get('S', [0]))

            # CSS CORRIGIDO (LETRA ESCURA E VISUAL LIMPO)
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin-bottom: 25px;">
                <div style="background:#f0fdf4; border:1px solid #16a34a; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#16a34a; font-size:1.3rem;">N</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{n_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
                <div style="background:#eff6ff; border:1px solid #2563eb; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#2563eb; font-size:1.3rem;">P</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{p_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
                <div style="background:#fef2f2; border:1px solid #dc2626; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#dc2626; font-size:1.3rem;">K</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{k_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
                <div style="background:#fffbeb; border:1px solid #d97706; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#d97706; font-size:1.3rem;">Ca</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{ca_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
                <div style="background:#faf5ff; border:1px solid #9333ea; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#9333ea; font-size:1.3rem;">Mg</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{mg_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
                <div style="background:#fff7ed; border:1px solid #ea580c; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#ea580c; font-size:1.3rem;">S</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{s_val}</div>
                    <div style="font-size:0.7rem;">kg/ha</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- 5. GRÁFICOS ---
            st.markdown("#### 1. Macronutrientes Primários (N, K)")
            fig_big = go.Figure()
            colors_big = {'N': '#16a34a', 'K': '#dc2626'}
            for nutri in ['N', 'K']:
                fig_big.add_trace(go.Scatter(x=dados_nutri['fases'], y=dados_nutri['macros'][nutri], mode='lines+markers', name=nutri, line=dict(width=4, color=colors_big[nutri]), fill='tozeroy'))
            fig_big.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="kg/ha"))
            st.plotly_chart(fig_big, use_container_width=True)

            st.markdown("#### 2. Fósforo e Secundários (P, Ca, Mg, S)")
            fig_mid = go.Figure()
            colors_mid = {'P': '#2563eb', 'Ca': '#eab308', 'Mg': '#9333ea', 'S': '#f97316'}
            for nutri in ['P', 'Ca', 'Mg', 'S']:
                width_l = 5 if nutri == 'P' else 3
                fig_mid.add_trace(go.Scatter(x=dados_nutri['fases'], y=dados_nutri['macros'][nutri], mode='lines+markers', name=nutri, line=dict(width=width_l, color=colors_mid[nutri])))
            fig_mid.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="kg/ha"))
            st.plotly_chart(fig_mid, use_container_width=True)

            st.markdown("#### 3. Micronutrientes (g/ha)")
            fig_mic = go.Figure()
            colors_mic = {'B': '#ec4899', 'Zn': '#06b6d4', 'Mn': '#8b5cf6', 'Cu': '#f59e0b', 'Fe': '#64748b'}
            for nutri, vals in dados_nutri['micros'].items():
                fig_mic.add_trace(go.Scatter(x=dados_nutri['fases'], y=vals, mode='lines+markers', name=nutri, line=dict(width=2, dash='dot', color=colors_mic.get(nutri, '#555'))))
            fig_mic.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="g/ha"))
            st.plotly_chart(fig_mic, use_container_width=True)

            st.divider()

            # --- 6. MANEJO ESPECÍFICO (DINÂMICO E BLINDADO) ---
            st.markdown("### 🚜 Estratégia de Manejo Específica")
            st.caption(f"Recomendações técnicas para atingir o potencial genético do(a) **{nome_cultura_exibicao}**.")
            
            # Recupera o dicionário de manejo
            manejo = dados_nutri.get('manejo_tatico', {"Geral": "Consulte um Engenheiro Agrônomo para recomendações locais."})
            
            # Transforma o dicionário em lista para podermos acessar por índice (0, 1, 2)
            # Isso resolve o erro: não buscamos mais por chave fixa ['P'], pegamos o que tiver.
            itens_manejo = list(manejo.items())
            
            # Garante que a lista tenha pelo menos 3 itens para não quebrar o layout de 3 colunas
            # Se a cultura tiver só 2 dicas, ele completa com vazio para não dar erro de índice
            while len(itens_manejo) < 3:
                itens_manejo.append((" - ", "Sem recomendação específica adicional."))

            c_ad1, c_ad2, c_ad3 = st.columns(3)
            
            # Definição de estilos visuais para os cards (Azul, Verde, Vermelho)
            # O sistema vai aplicar essas cores na ordem dos itens
            estilos = [
                {"bg": "#eff6ff", "border": "#2563eb", "text": "#1e3a8a"}, # Estilo 1 (Azul)
                {"bg": "#f0fdf4", "border": "#16a34a", "text": "#14532d"}, # Estilo 2 (Verde)
                {"bg": "#fef2f2", "border": "#dc2626", "text": "#7f1d1d"}  # Estilo 3 (Vermelho)
            ]

            # Loop para criar os 3 cards dinamicamente
            colunas_cards = [c_ad1, c_ad2, c_ad3]
            
            for i in range(3):
                chave_nutri, texto_nutri = itens_manejo[i]
                style = estilos[i]
                
                with colunas_cards[i]:
                    st.markdown(f"""
                    <div style="background:{style['bg']}; border-top: 4px solid {style['border']}; padding:15px; border-radius:8px; color:#0f172a; height:100%;">
                        <b style="color:{style['text']};">{chave_nutri}</b><hr style="margin:8px 0;">
                        <div style="font-size:0.85rem;">{texto_nutri}</div>
                    </div>""", unsafe_allow_html=True)

            # --- 7. AVISO LEGAL E FONTE (MANDATÓRIO) ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: #fff7ed; border-left: 5px solid #f97316; padding: 20px; border-radius: 5px;">
                <h4 style="color: #9a3412; margin-top: 0;">⚠️ ALERTA AGRONÔMICO (LEIA COM ATENÇÃO)</h4>
                <p style="color: #7c2d12; font-size: 0.9rem; margin-bottom: 10px;">
                    <b>1. Demanda vs. Recomendação:</b> Estes gráficos mostram a <i>Marcha de Absorção</i> (o que a planta consome), 
                    NÃO a recomendação de adubação (o que você deve aplicar).
                </p>
                <p style="color: #7c2d12; font-size: 0.9rem; margin-bottom: 10px;">
                    <b>2. Lei do Mínimo:</b> O solo já possui reservas de nutrientes. Aplicar a quantidade total absorvida sem descontar 
                    o que já existe no solo pode causar toxicidade, salinidade e prejuízo financeiro.
                </p>
                <p style="color: #7c2d12; font-weight: bold; font-size: 0.95rem;">
                    🧪 RECOMENDAÇÃO OFICIAL: Faça sempre a ANÁLISE DE SOLO antes do plantio. Consulte um Engenheiro Agrônomo 
                    para calcular a dose exata baseada na "Lei de Restituição".
                </p>
                <hr style="border-color: #fdba74;">
                <p style="color: #9a3412; font-size: 0.7rem; margin-top: 5px;">
                    <i>Fontes de Dados: Malavolta (2006), Embrapa Soja/Milho/Café, IPNI Brasil. Dados baseados em média para alta produtividade.</i>
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("Dados em compilação.")

        st.markdown('</div>', unsafe_allow_html=True)
    
    
    # 3. CLIMA (CORRIGIDO E BLINDADO)
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        c_clim1, c_clim2 = st.columns([3, 1])
        with c_clim1:
            st.markdown("### 📅 Planejamento Climático")
        with c_clim2:
            hora_att = datetime.now().strftime("%H:%M")
            st.markdown(f"<div style='text-align:right; font-size:0.7rem; color:#64748b; margin-top:5px;'>🔄 Atualizado às: <b>{hora_att}</b></div>", unsafe_allow_html=True)

        # Gráfico Semanal (Mantido)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Consumo (ETc)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=20), legend=dict(orientation="h", y=1.1), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # --- TABELA DE DETALHE HORÁRIO (CORREÇÃO DO ERRO) ---
        df_hora = WeatherConn.get_hourly_forecast(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        
        if not df_hora.empty:
            st.markdown("### 🕒 Detalhe Operacional (Próximas 24h)")
            st.caption("Analise as janelas de aplicação baseadas no Delta T.")

            # 1. Cria a coluna de Condição (Semáforo)
            def get_status_deltat(dt):
                if 2 <= dt <= 8: return "✅ IDEAL"
                elif 8 < dt <= 10: return "⚠️ ATENÇÃO"
                else: return "🚫 PARE"

            # Garante que a coluna Delta T existe antes de aplicar
            if 'Delta T' in df_hora.columns:
                df_hora['Condição'] = df_hora['Delta T'].apply(get_status_deltat)
            else:
                df_hora['Condição'] = "---"

            # 2. Seleção de Colunas Segura (Evita o KeyError)
            # Lista de colunas que QUEREMOS mostrar
            cols_desejadas = ['HoraSimples', 'Temp', 'Chuva', 'Umid', 'Vento', 'Delta T', 'Condição']
            
            # Filtra apenas as que REALMENTE EXISTEM no dataframe
            cols_finais = [c for c in cols_desejadas if c in df_hora.columns]
            
            # Cria a tabela de visualização apenas com o que existe
            df_view = df_hora[cols_finais].copy()
            
            # Renomeia para ficar bonito (se a coluna existir)
            mapa_nomes = {
                'HoraSimples': 'Horário',
                'Temp': 'Temp (°C)',
                'Chuva': 'Chuva (mm)',
                'Umid': 'Umid (%)',
                'Vento': 'Vento (km/h)',
                'Delta T': 'Delta T',
                'Condição': 'Status'
            }
            df_view.rename(columns=mapa_nomes, inplace=True)

            # 3. Exibição da Tabela
            st.dataframe(
                df_view,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Horário": st.column_config.TextColumn("Horário"),
                    "Temp (°C)": st.column_config.ProgressColumn(
                        "Temperatura", format="%.1f°", min_value=0, max_value=45
                    ),
                    "Chuva (mm)": st.column_config.NumberColumn("Chuva", format="%.1f mm"),
                    "Umid (%)": st.column_config.NumberColumn("Umidade", format="%d%%"),
                    "Delta T": st.column_config.NumberColumn("Delta T", format="%.1f", help="Ideal: 2 a 8"),
                    "Status": st.column_config.TextColumn("Janela Aplicação")
                }
            )
            
            # Legenda
            c_leg1, c_leg2 = st.columns(2)
            with c_leg1: st.info("💧 **Chuva:** Acumulado previsto na hora.")
            with c_leg2: st.warning("🛡️ **Delta T:** Ideal entre 2 e 8.")

        else:
            st.error("⚠️ Previsão horária indisponível no momento.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. RADAR (VISUAL MASTER)
    with tabs[3]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Monitoramento Regional")
        st.caption("Dados em tempo real das estações meteorológicas vizinhas.")
        
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                # Lógica Visual
                if r['Chuva'] == "Sim":
                    cor_fundo, cor_borda, icon, txt, cor_txt = "#fef2f2", "#fca5a5", "🌧️", "Chuva", "#991b1b"
                else:
                    cor_fundo, cor_borda, icon, txt, cor_txt = "#f0fdf4", "#86efac", "☀️", "Limpo", "#166534"

                html_radar = f"""
                <div style="background-color:{cor_fundo}; border:1px solid {cor_borda}; border-radius:12px; padding:15px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; color:#64748b; margin-bottom:5px;">📍 {r['Direcao']}</div>
                    <div style="font-size:2rem; font-weight:800; color:#0f172a; line-height:1;">{r['Temp']:.0f}°</div>
                    <div style="margin-top:8px; font-size:0.8rem; font-weight:700; color:{cor_txt}; background:rgba(255,255,255,0.5); padding:4px; border-radius:6px;">{icon} {txt}</div>
                </div>"""
                with cols[i]: st.markdown(html_radar, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. MAPA (MIP SYNGENTA STYLE - COM MODAL FLUTUANTE)
    with tabs[4]:
        import json
        import base64
        from io import BytesIO

        # --- 1. CONFIGURAÇÃO E BANCO DE DADOS ---
        DB_FILE = "monitoramento_campo.json"
        
        # Banco de Imagens (Simulando App Nativo)
        DB_IMAGENS_MIP = {
            "Soja": {
                "Lagarta-do-cartucho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Spodoptera_frugiperda_back.jpg/320px-Spodoptera_frugiperda_back.jpg",
                "Percevejo-marrom": "https://live.staticflickr.com/65535/49086326938_5f470375e8_w.jpg",
                "Ferrugem Asiática": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Phakopsora_pachyrhizi_on_Soybean_02.jpg/320px-Phakopsora_pachyrhizi_on_Soybean_02.jpg",
                "Antracnose": "https://content.eol.org/data/media/7f/32/a6/542.1465431668.jpg",
                "Mofo-branco": "https://www.agrolink.com.br/upload/problemas/Sclerotinia_sclerotiorum81.jpg"
            },
            "Milho": {
                "Cigarrinha": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Dalbulus_maidis.jpg/320px-Dalbulus_maidis.jpg",
                "Lagarta-do-cartucho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Spodoptera_frugiperda_back.jpg/320px-Spodoptera_frugiperda_back.jpg",
                "Pulgão": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Rhopalosiphum_maidis.jpg/320px-Rhopalosiphum_maidis.jpg"
            },
            # Fallback para outras culturas
            "Geral": {
                "Praga Genérica": "https://via.placeholder.com/300x200.png?text=Praga+Detectada",
                "Doença Genérica": "https://via.placeholder.com/300x200.png?text=Doen%C3%A7a+Detectada"
            }
        }

        # Funções de Banco de Dados
        def carregar_dados():
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f: return json.load(f)
            return []

        def salvar_dado(novo):
            d = carregar_dados()
            d.append(novo)
            with open(DB_FILE, "w") as f: json.dump(d, f)
            return d

        # Carrega dados
        historico = carregar_dados()
        cultura_atual = str(cult_sel)
        imgs_cultura = DB_IMAGENS_MIP.get(cultura_atual, DB_IMAGENS_MIP["Geral"])

        # --- 2. MODAL FLUTUANTE (A MÁGICA VISUAL) ---
        # Esta função cria a janela "Pop-up" bonita
        @st.dialog(f"🛡️ Registrar Ocorrência: {cultura_atual}")
        def popup_monitoramento(lat, lon):
            st.markdown(f"<div style='font-size:0.8rem; color:#64748b; margin-bottom:10px;'>📍 Localização Exata: {lat:.5f}, {lon:.5f}</div>", unsafe_allow_html=True)
            
            # Abas dentro do Modal (Praga vs Doença)
            tab_p, tab_d = st.tabs(["🐛 PRAGAS", "🍄 DOENÇAS"])
            
            sel_nome = None
            sel_img = None
            sel_tipo = None

            # Conteúdo Visual (Cards Selecionáveis)
            with tab_p:
                st.caption("Toque na imagem para selecionar")
                cols = st.columns(3)
                idx = 0
                for nome, url in imgs_cultura.items():
                    # Filtro simples (num app real seria mais robusto)
                    if "Ferrugem" not in nome and "Antracnose" not in nome and "Mofo" not in nome: 
                        with cols[idx % 3]:
                            st.image(url, use_container_width=True)
                            if st.button(nome, key=f"btn_p_{nome}", use_container_width=True):
                                st.session_state['temp_sel'] = (nome, url, "Praga")
                        idx += 1
            
            with tab_d:
                st.caption("Toque na imagem para selecionar")
                cols_d = st.columns(3)
                idx_d = 0
                for nome, url in imgs_cultura.items():
                    if "Ferrugem" in nome or "Antracnose" in nome or "Mofo" in nome:
                        with cols_d[idx_d % 3]:
                            st.image(url, use_container_width=True)
                            if st.button(nome, key=f"btn_d_{nome}", use_container_width=True):
                                st.session_state['temp_sel'] = (nome, url, "Doença")
                        idx_d += 1

            st.divider()

            # Área de Confirmação (Só aparece se selecionou algo)
            if 'temp_sel' in st.session_state:
                s_nome, s_url, s_tipo = st.session_state['temp_sel']
                
                st.markdown(f"""
                <div style="background:#f0fdf4; padding:10px; border-radius:8px; border:1px solid #bbf7d0; display:flex; align-items:center; gap:10px;">
                    <img src="{s_url}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">
                    <div>
                        <div style="font-weight:bold; color:#166534;">{s_nome}</div>
                        <div style="font-size:0.8rem; color:#166534;">{s_tipo} Identificada</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_qtd, c_sev = st.columns(2)
                with c_qtd:
                    focos = st.number_input("Número de Focos", min_value=1, value=1)
                with c_sev:
                    severidade = st.select_slider("Severidade", ["Leve", "Média", "Alta"], value="Média")
                
                obs = st.text_input("Observação de Campo", placeholder="Ex: Próximo à bordadura...")

                if st.button("✅ CONFIRMAR REGISTRO", type="primary", use_container_width=True):
                    novo = {
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Cultura": cultura_atual,
                        "Tipo": s_tipo,
                        "Nome": s_nome,
                        "Focos": focos,
                        "Severidade": severidade,
                        "Obs": obs,
                        "lat": lat,
                        "lon": lon
                    }
                    salvar_dado(novo)
                    st.toast("💾 Ocorrência Salva com Sucesso!")
                    del st.session_state['temp_sel'] # Limpa seleção
                    st.rerun()

        # --- 3. TELA PRINCIPAL (MAPA FULL) ---
        st.markdown('<div class="app-card" style="padding:0px; overflow:hidden;">', unsafe_allow_html=True)
        
        # Header Flutuante
        c_act1, c_act2 = st.columns([2, 1])
        with c_act1:
            st.markdown(f"### 🛰️ Monitoramento Ativo")
            st.caption(f"Pontos na Sessão: **{len(historico)}**")
        with c_act2:
            # Botão de Exportar
            if st.button("📂 Fechar & Exportar", type="secondary", use_container_width=True):
                 st.session_state['modo_relatorio'] = True
                 st.rerun()

        # O MAPA (GOOGLE EARTH STYLE)
        m = folium.Map(
            location=[st.session_state['loc_lat'], st.session_state['loc_lon']], 
            zoom_start=18,
            tiles=None,
            control_scale=True
        )
        
        # Satélite HD
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri', name='Satélite HD', overlay=False
        ).add_to(m)

        # Pontos Salvos (Ícones Profissionais)
        for p in historico:
            cor = "red" if p['Severidade'] == "Alta" else "orange" if p['Severidade'] == "Média" else "#4ade80"
            folium.Marker(
                [p['lat'], p['lon']],
                popup=f"<b>{p['Nome']}</b><br>{p['Focos']} focos ({p['Severidade']})",
                icon=folium.Icon(color="black", icon_color=cor, icon="bug", prefix="fa")
            ).add_to(m)

        # GPS DO USUÁRIO (BOLINHA AZUL PULSANTE)
        LocateControl(auto_start=True, strings={"title": "Minha Posição"}).add_to(m)
        
        # Captura de Clique
        map_data = st_folium(m, height=500, returned_objects=["last_clicked"])

        # --- GATILHO DO MODAL ---
        # Se clicar no mapa, ABRE O MODAL (Não abre formulário embaixo!)
        if map_data and map_data["last_clicked"]:
            lat_clique = map_data["last_clicked"]["lat"]
            lon_clique = map_data["last_clicked"]["lng"]
            popup_monitoramento(lat_clique, lon_clique)

        st.markdown('</div>', unsafe_allow_html=True)

        # --- 4. ÁREA DE RELATÓRIO / EXPORTAÇÃO (PASTA DIGITAL) ---
        if st.session_state.get('modo_relatorio'):
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📂 RELATÓRIO DE MONITORAMENTO (EXPORTAR)", expanded=True):
                st.markdown("### 📋 Resumo da Inspeção")
                
                if not historico:
                    st.warning("Nenhum dado coletado nesta sessão.")
                else:
                    df = pd.DataFrame(historico)
                    
                    # Métricas
                    c_m1, c_m2, c_m3 = st.columns(3)
                    c_m1.metric("Total de Pontos", len(df))
                    c_m2.metric("Pragas Críticas", len(df[df['Severidade']=='Alta']))
                    c_m3.metric("Focos Totais", df['Focos'].sum())
                    
                    st.dataframe(df[['Data', 'Nome', 'Severidade', 'Focos', 'Obs']], use_container_width=True)
                    
                    # Botão Download Excel
                    c_d1, c_d2 = st.columns(2)
                    with c_d1:
                        # Converte para Excel na memória
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            df.to_excel(writer, index=False, sheet_name='Monitoramento')
                        excel_data = output.getvalue()
                        
                        st.download_button(
                            label="📥 Baixar Planilha (.xlsx)",
                            data=excel_data,
                            file_name=f"Monitoramento_{cultura_atual}_{date.today()}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    with c_d2:
                        if st.button("🔙 Voltar ao Mapa", use_container_width=True):
                            st.session_state['modo_relatorio'] = False
                            st.rerun()

                                
    # 6. GESTÃO (SIMULADOR DE NEGÓCIO - CORRIGIDO E PRÁTICO)
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # --- 1. BANCO DE DADOS INTELIGENTE (CORRIGIDO) ---
        # input_type: 'area' (Hectares) ou 'planta' (Pés/Unidades)
        # prod_factors: [Baixa Tec, Média Tec, Alta Tec] -> Quanto rende por unidade de entrada
        
        AGRO_PLAN = {
            # GRÃOS (Extensivos -> Hectares)
            "Soja":      {"input": "area", "label": "Hectares", "prod": [50, 65, 85],   "medida_final": "Sacas", "preco": 128.00},
            "Milho":     {"input": "area", "label": "Hectares", "prod": [100, 140, 180], "medida_final": "Sacas", "preco": 58.00},
            "Algodão":   {"input": "area", "label": "Hectares", "prod": [250, 320, 400], "medida_final": "@",     "preco": 145.00},
            "Trigo":     {"input": "area", "label": "Hectares", "prod": [40, 60, 80],    "medida_final": "Sacas", "preco": 85.00},
            
            # PERENES E FRUTAS (Intensivos -> Pés/Plantas)
            # Café: Pede PÉS -> Entrega SACAS (Conversão automática: ~0.01 a 0.02 sacas/pé)
            "Café":      {"input": "planta", "label": "Pés/Plantas", "prod": [0.010, 0.015, 0.025], "medida_final": "Sacas (60kg)", "preco": 1150.00},
            
            # Frutas Pequenas: Pede PÉS -> Entrega KG
            "Framboesa": {"input": "planta", "label": "Pés/Mudas",   "prod": [0.5, 1.2, 2.5],    "medida_final": "Kg",      "preco": 60.00}, # Alto valor
            "Mirtilo":   {"input": "planta", "label": "Pés/Mudas",   "prod": [1.0, 2.5, 4.0],    "medida_final": "Kg",      "preco": 45.00},
            "Uva":       {"input": "planta", "label": "Pés/Videiras","prod": [8.0, 15.0, 25.0],  "medida_final": "Kg",      "preco": 9.50},
            
            # Frutas Grandes: Pede PÉS -> Entrega CAIXAS/KG
            "Citros":    {"input": "planta", "label": "Árvores",     "prod": [2.0, 3.5, 5.0],    "medida_final": "Cx 40.8kg", "preco": 45.00},
            "Tomate":    {"input": "planta", "label": "Pés",         "prod": [4.0, 7.0, 10.0],   "medida_final": "Cx 20kg",   "preco": 70.00},
            "Banana":    {"input": "planta", "label": "Touceiras",   "prod": [15.0, 30.0, 50.0], "medida_final": "Kg",        "preco": 3.00},
        }

        # Carrega dados ou usa genérico se a cultura não estiver na lista
        dados = AGRO_PLAN.get(cult_sel, {"input": "area", "label": "Unidades", "prod": [1, 1, 1], "medida_final": "Unid", "preco": 1.0})

        st.markdown(f"### 📊 Calculadora de Potencial: **{cult_sel}**")
        st.caption("Estimativa de colheita baseada no seu volume de plantio.")

        # --- 2. INPUT INTUITIVO (Pergunta o que faz sentido) ---
        
        c_i1, c_i2, c_i3 = st.columns([1.2, 1.5, 1])
        
        with c_i1:
            # Pergunta Dinâmica: "Quantos Pés?" ou "Quantos Hectares?"
            qtd_input = st.number_input(
                f"Quantos {dados['label']} você tem?", 
                min_value=1.0, 
                value=1000.0 if dados['input'] == 'planta' else 50.0, 
                step=1.0 if dados['input'] == 'planta' else 0.5,
                help="Quantidade total plantada."
            )

        with c_i2:
            # Nível Tecnológico (Define a produtividade unitária)
            tec = st.select_slider(
                "Nível Tecnológico", 
                options=["Baixo (Simples)", "Médio (Padrão)", "Alto (Intensivo)"],
                value="Médio (Padrão)"
            )
            # Pega o índice 0, 1 ou 2
            idx = 0 if "Baixo" in tec else 1 if "Médio" in tec else 2
            fator_prod = dados['prod'][idx]

        with c_i3:
            # Mostra o fator usado para educação do usuário
            st.metric(f"Rendimento Esp.", f"{fator_prod:.3f}", f"{dados['medida_final']}/{dados['label'][:-1]}")

        st.divider()

        # --- 3. RESULTADO DIRETO (POTENCIAL BRUTO) ---
        # O usuário pediu "Dado bruto aproximado"
        
        producao_potencial = qtd_input * fator_prod
        receita_bruta = producao_potencial * dados['preco']

        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            # BALÃO DE PRODUÇÃO (O que importa pro produtor)
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                border: 1px solid #bae6fd; 
                border-radius: 12px; 
                padding: 20px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            ">
                <div style="color:#0284c7; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">POTENCIAL PRODUTIVO</div>
                <div style="color:#0369a1; font-size:2.2rem; font-weight:900; line-height:1.2;">
                    {producao_potencial:,.1f}
                </div>
                <div style="background:#0ea5e9; color:white; font-size:0.8rem; font-weight:bold; padding:4px 10px; border-radius:15px; display:inline-block; margin-top:5px;">
                    {dados['medida_final'].upper()} TOTAIS
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            # BALÃO FINANCEIRO (Estimativa Bruta)
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                border: 1px solid #86efac; 
                border-radius: 12px; 
                padding: 20px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            ">
                <div style="color:#16a34a; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">VALOR BRUTO ESTIMADO</div>
                <div style="color:#15803d; font-size:2.2rem; font-weight:900; line-height:1.2;">
                    R$ {receita_bruta/1000:,.1f} k
                </div>
                <div style="color:#166534; font-size:0.8rem; margin-top:10px;">
                    Baseado em R$ {dados['preco']:.2f} / {dados['medida_final']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Nota: Este cálculo considera o **Potencial Produtivo** da planta. Fatores climáticos, pragas e manejo podem alterar o resultado real.")

        # --- 4. LINKS DE AÇÃO RÁPIDA (GOOGLE) ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🌍 Inteligência de Mercado")
        
        c_btn1, c_btn2 = st.columns(2)
        local_user = city if city else "na minha região"
        
        with c_btn1:
            # Botão 1: Buscar Compradores
            termos_busca = f"compradores de {cult_sel} {local_user} atacado"
            st.link_button(f"🤝 Quem compra {cult_sel}?", f"https://www.google.com/search?q={termos_busca}", use_container_width=True)
            
        with c_btn2:
            # Botão 2: Buscar Preço
            termos_preco = f"preço kg {cult_sel} hoje {local_user} ceasa"
            st.link_button(f"💰 Cotação Hoje no Google", f"https://www.google.com/search?q={termos_preco}", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. ALERTAS (CENTRAL DE CONFIGURAÇÃO)
    with tabs[6]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Central de Automação")
        st.info("Configure aqui os alertas automáticos. No App Mobile, estas notificações chegarão como Push Notification.")
        
        with st.form("form_notificacao_pro"):
            st.markdown("#### 👤 Perfil do Assinante")
            col_n1, col_n2 = st.columns(2)
            nome_user = col_n1.text_input("Nome Responsável", value="Produtor")
            email_user = col_n2.text_input("E-mail Principal")
            
            st.markdown("#### ⚙️ Regras de Disparo")
            c_chk1, c_chk2 = st.columns(2)
            chk_chuva = c_chk1.checkbox("Alertar Chuva (>10mm)", value=True)
            chk_praga = c_chk1.checkbox("Alertar Risco de Pragas", value=True)
            chk_temp = c_chk2.checkbox("Alertar Alta Temperatura (>35°C)")
            chk_mercado = c_chk2.checkbox("Alertar Variação de Preço (>2%)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 SALVAR CONFIGURAÇÃO", type="primary"):
                NotificationSystem.salvar_assinatura(nome_user, email_user, [cult_sel])
                st.success("✅ Configurações salvas no servidor!")
        
        st.divider()
        st.markdown("#### 🧪 Teste de Workflow")
        c_t1, c_t2 = st.columns([3,1])
        with c_t1: st.markdown("Disparar relatório imediato para validar o servidor de e-mail.")
        with c_t2:
            if st.button("📧 Enviar Agora"):
                if email_user:
                    dados_simulados = {str(cult_sel): f"Estimativa: {prod_liquida:.0f} sc | Preço: R$ {preco_venda}"}
                    ok, msg = NotificationSystem.enviar_email_agora(nome_user, email_user, [cult_sel], dados_simulados)
                    if ok: st.toast("E-mail enviado com sucesso!")
                    else: st.error(msg)
                else: st.warning("Preencha o e-mail acima.")
        st.markdown('</div>', unsafe_allow_html=True)
