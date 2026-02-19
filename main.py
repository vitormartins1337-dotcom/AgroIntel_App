# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | TITANIUM EDITION V19.0 (MASTER STABLE)
# DESCRIÇÃO: Sistema Agronômico Completo com Volumetria, HVAC e Fitopatologia Avançada.

import streamlit as st
import datetime
import plotly.graph_objects as go
import textwrap

# ==============================================================================
# 1. CORE ENGINE & DATABASE (MONOLITHIC BLOCK)
# ==============================================================================
class AgroEngine:
    def __init__(self):
        self.db = self._get_agro_db()

    def _get_agro_db(self):
        return {
            # --- 1.1 GENÉTICAS DETALHADAS ---
            "GENETICAS_PARAMETROS": {
                "Indica Predom. THC (Fotoperíodo)": {
                    "fator_yield": 1.0, "ciclo_dias": 60, "tipo": "Foto",
                    "desc": "Arbustiva, compacta. Alta demanda de Magnésio na flora. Resistente a frio.",
                    "terpenos": "Mirceno, Cariofileno (Sedativo)"
                },
                "Sativa Predom. THC (Fotoperíodo)": {
                    "fator_yield": 1.4, "ciclo_dias": 90, "tipo": "Foto",
                    "desc": "Alta estatura (pode triplicar na flora). Sensível a Nitrogênio alto. Requer LST.",
                    "terpenos": "Limoneno, Pineno (Euforico)"
                },
                "Híbrida 50/50 THC (Fotoperíodo)": {
                    "fator_yield": 1.2, "ciclo_dias": 70, "tipo": "Foto",
                    "desc": "Vigor híbrido. Estrutura forte, aceita bem podas (Topping/FIM).",
                    "terpenos": "Balanceado"
                },
                "Indica Predom. CBD (Fotoperíodo)": {
                    "fator_yield": 1.1, "ciclo_dias": 65, "tipo": "Foto",
                    "desc": "Medicinal. Foco em biomassa. Geralmente mais resistente a mofo.",
                    "terpenos": "Linalol (Relaxante)"
                },
                "Landrace Pura (Sativa Foto)": {
                    "fator_yield": 1.5, "ciclo_dias": 110, "tipo": "Foto",
                    "desc": "Genética selvagem. Floração extremamente longa. Requer pouca comida.",
                    "terpenos": "Terpinoleno (Exótico)"
                },
                "Indica Predom. THC (Automática)": {
                    "fator_yield": 0.5, "ciclo_dias": 65, "tipo": "Auto",
                    "desc": "Ciclo rápido. Raiz sensível. Não aceita transplantes.",
                    "terpenos": "Variável"
                },
                "Sativa Predom. THC (Automática)": {
                    "fator_yield": 0.8, "ciclo_dias": 90, "tipo": "Auto",
                    "desc": "Genética XXL. Requer DLI alto (20/4) para expressar potencial.",
                    "terpenos": "Cítricos"
                },
                "Medicinal CBD (Automática)": {
                    "fator_yield": 0.6, "ciclo_dias": 75, "tipo": "Auto",
                    "desc": "Foco terapêutico. Baixo THC. Ideal para extração.",
                    "terpenos": "Mirceno"
                }
            },

            # --- 1.2 MÉTODOS DE CULTIVO ---
            "METODOS_CULTIVO": {
                "Orgânico (Solo Vivo/Notill)": {
                    "descricao": "Ciclo biológico. Foco na vida do solo. Não mede pH de saída.",
                    "rendimento_base": 55, "ph_ideal": "6.0-6.8", "ec_ideal": "N/A"
                },
                "Mineral (Coco/Perlita)": {
                    "descricao": "Alta performance (Crop Steering). Exige rega frequente.",
                    "rendimento_base": 90, "ph_ideal": "5.8-6.2", "ec_ideal": "2.0-3.0"
                },
                "Orgânico-Mineral (Mix)": {
                    "descricao": "Solo base com reforço de sais na floração.",
                    "rendimento_base": 75, "ph_ideal": "6.0-6.5", "ec_ideal": "1.2-1.8"
                },
                "Hidroponia (DWC/RDWC)": {
                    "descricao": "Máxima oxigenação. Crescimento explosivo.",
                    "rendimento_base": 110, "ph_ideal": "5.5-5.8", "ec_ideal": "1.5-2.2"
                },
                "KNF (Korean Natural Farming)": {
                    "descricao": "Insumos fermentados naturais (FPJ, FFJ).",
                    "rendimento_base": 60, "ph_ideal": "6.0-6.5", "ec_ideal": "N/A"
                }
            },

            # --- 1.3 NUTRIÇÃO (MARCHA DE ABSORÇÃO - 12 SEMANAS) ---
            "NUTRI_MARCHA_ABSORCAO": {
                "semanas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "N": [90, 100, 100, 80, 60, 40, 30, 20, 10, 5, 0, 0], 
                "P": [20, 30, 40, 60, 80, 100, 100, 90, 70, 40, 10, 0], 
                "K": [30, 40, 50, 70, 85, 95, 100, 100, 95, 60, 20, 0], 
                "Ca": [40, 50, 70, 90, 100, 90, 80, 70, 50, 30, 10, 0], 
                "Mg": [40, 50, 60, 80, 90, 80, 70, 60, 40, 20, 10, 0],
                "S": [20, 30, 40, 50, 60, 80, 90, 90, 80, 50, 20, 0]
            },

            # --- 1.4 FITOSSANIDADE (DATABASE EXPANDIDO) ---
            "DOCTOR_GROW_FITOSSANIDADE": {
                "Spider Mites (Ácaros)": {
                    "gravidade": "CRÍTICA",
                    "sintomas": "Pontos brancos (estippling) na face superior. Teias. Folhas opacas.",
                    "bio": ["Beauveria Bassiana", "Óleo de Neem (Veg)", "Phytoseiulus (Predador)"],
                    "quimico": ["Abamectina", "Etoxazol"],
                    "obs": "Explodem no calor >28°C e umidade baixa."
                },
                "Russet Mites (Ácaro do Bronzeamento)": {
                    "gravidade": "FATAL",
                    "sintomas": "Invisíveis a olho nu. Folhas 'enrolam' pra cima (Taco). Caule bronzeado/ferrugem.",
                    "bio": ["Enxofre Micronizado (Pó)", "Amblyseius swirskii"],
                    "quimico": ["Abamectina", "Spiromesifen"],
                    "obs": "Frequentemente confundido com deficiência de Magnésio ou estresse de calor."
                },
                "Tripes": {
                    "gravidade": "MÉDIA",
                    "sintomas": "Manchas prateadas irregulares. Pontos pretos (fezes). Insetos finos.",
                    "bio": ["Spinosad", "Sabão Potássico", "Armadilhas Azuis"],
                    "quimico": ["Imidacloprido (Veg)", "Acetamiprido"],
                    "obs": "Vetores de vírus."
                },
                "Fungus Gnats": {
                    "gravidade": "BAIXA",
                    "sintomas": "Mosquitos no solo. Larvas comem raízes.",
                    "bio": ["BTI (Bacillus)", "Terra de Diatomáceas"],
                    "quimico": ["Peróxido de Hidrogênio"],
                    "obs": "Sinal de excesso de rega."
                },
                "Oídio (White Mold)": {
                    "gravidade": "ALTA",
                    "sintomas": "Pó branco nas folhas (parece farinha).",
                    "bio": ["Bicarbonato de Potássio", "Leite Cru 10%", "Bacillus Subtilis"],
                    "quimico": ["Difenoconazol", "Tebuconazol"],
                    "obs": "Requer pH da folha alcalino para morrer."
                },
                "Botrytis (Bud Rot)": {
                    "gravidade": "FATAL",
                    "sintomas": "Bud apodrece de dentro para fora (marrom/cinza). Folha de açúcar solta fácil.",
                    "bio": ["Trichoderma (Prevenção)", "Ventilação Extrema"],
                    "quimico": ["NENHUM (Cortar e descartar)"],
                    "obs": "Causado por umidade alta na floração."
                },
                "Fusarium": {
                    "gravidade": "FATAL",
                    "sintomas": "Um galho murcha repentinamente. O resto da planta parece bem.",
                    "bio": ["Trichoderma", "Micorrizas"],
                    "quimico": ["NENHUM (Solo contaminado)"],
                    "obs": "Fungo de solo. Descarte tudo."
                },
                "Mosca Branca": {
                    "gravidade": "MÉDIA",
                    "sintomas": "Nuvem branca ao tocar na planta. Melada nas folhas.",
                    "bio": ["Beauveria Bassiana", "Armadilha Amarela"],
                    "quimico": ["Acetamiprido"],
                    "obs": "Resistente a muitos venenos."
                }
            },
            
            # --- 1.5 DEFICIÊNCIAS VISUAIS ---
            "DEFICIENCIAS_VISUAIS": {
                "Nitrogênio (N)": {"tipo": "Macro Móvel", "sintoma": "Amarelamento folhas velhas (base).", "correcao_bio": "Sangue seco, Humus.", "correcao_quim": "Ureia.", "cor_card": "#22c55e"},
                "Fósforo (P)": {"tipo": "Macro Móvel", "sintoma": "Caules roxos, manchas escuras, necrose.", "correcao_bio": "Guano, Farinha Osso.", "correcao_quim": "MAP, MKP.", "cor_card": "#3b82f6"},
                "Potássio (K)": {"tipo": "Macro Móvel", "sintoma": "Bordas queimadas, flores magras.", "correcao_bio": "Cinzas, Kelp.", "correcao_quim": "Nitrato de K.", "cor_card": "#a855f7"},
                "Cálcio (Ca)": {"tipo": "Macro Imóvel", "sintoma": "Ferrugem em folhas novas/médias.", "correcao_bio": "Calcário, Ostras.", "correcao_quim": "Nitrato de Ca.", "cor_card": "#f97316"},
                "Magnésio (Mg)": {"tipo": "Macro Móvel", "sintoma": "Clorose intervenal (nervura verde).", "correcao_bio": "Dolomita, Epsom.", "correcao_quim": "Sulfato de Mg.", "cor_card": "#eab308"},
                "Enxofre (S)": {"tipo": "Macro Imóvel", "sintoma": "Amarelo em folhas NOVAS (topo).", "correcao_bio": "Gesso.", "correcao_quim": "Sulfato de Mg.", "cor_card": "#facc15"},
                "Ferro (Fe)": {"tipo": "Micro Imóvel", "sintoma": "Folha nova nasce amarelo limão.", "correcao_bio": "Quelatos.", "correcao_quim": "Fe-EDTA.", "cor_card": "#a3e635"},
                "Zinco (Zn)": {"tipo": "Micro Imóvel", "sintoma": "Rosetting (topo amassado), pontas queimadas.", "correcao_bio": "Extrato sementes.", "correcao_quim": "Sulfato Zn.", "cor_card": "#9ca3af"}
            },
            
            # --- 1.6 FASES DINÂMICAS (ATUALIZADO V19: COM METAS DE CLIMA & LUZ) ---
            "FASES_DINAMICAS": {
                "Plântula": {
                    "foco": "Raízes/Sobrevivência", 
                    "luz_h": "18/6", "meta_ppfd": "200-300", "meta_vpd": "0.4-0.8",
                    "obs": "Umidade alta (70%+). Luz fraca. Não adube forte.", 
                    "ameacas": ["Pythium", "Damping-off"]
                },
                "Vegetativo": {
                    "foco": "Estrutura/Folhagem", 
                    "luz_h": "18/6", "meta_ppfd": "400-600", "meta_vpd": "0.8-1.1",
                    "obs": "Nitrogênio alto. Poda Top/FIM. Ventilação constante.", 
                    "ameacas": ["Tripes", "Minadores"]
                },
                "Pré-Flora": {
                    "foco": "Stretch/Sexagem", 
                    "luz_h": "12/12", "meta_ppfd": "600-750", "meta_vpd": "1.0-1.2",
                    "obs": "Planta dobra de tamanho. Demanda alta de Ca/Mg.", 
                    "ameacas": ["Hermafroditismo", "Carência de Mg"]
                },
                "Flora Inicial": {
                    "foco": "Formação de Pistilos", 
                    "luz_h": "12/12", "meta_ppfd": "750-900", "meta_vpd": "1.1-1.3",
                    "obs": "Botões florais aparecendo. Parar Nitrogênio gradualmente.", 
                    "ameacas": ["Oídio", "Estresse de Calor"]
                },
                "Flora Média": {
                    "foco": "Engorda/Densidade", 
                    "luz_h": "12/12", "meta_ppfd": "900-1000", "meta_vpd": "1.2-1.5",
                    "obs": "PK Booster. Máxima exigência de luz e ventilação.", 
                    "ameacas": ["Queima de Luz", "Ácaros"]
                },
                "Flora Final": {
                    "foco": "Maturação/Resina", 
                    "luz_h": "12/12", "meta_ppfd": "800-600", "meta_vpd": "1.3-1.6",
                    "obs": "Senescência natural. Flush (lavagem). Reduzir temperatura.", 
                    "ameacas": ["Botrytis (Mofo)", "Bananas"]
                }
            }
        }

# ==============================================================================
# 2. SETUP VISUAL & CONFIGURAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="Agrower SDI Pro", 
    page_icon="🍁", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa Classes
engine = AgroEngine()
db = engine.db

# CSS MASTER "MONSTRUOSO"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* GERAL */
    .stApp { background-color: #050505; color: #e4e4e7; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }
    
    /* HERO */
    .hero-card {
        background: linear-gradient(135deg, #1a0b2e 0%, #000000 100%);
        border: 1px solid #a855f7;
        box-shadow: 0 0 60px rgba(168, 85, 247, 0.25);
        border-radius: 20px; padding: 40px 20px; margin-bottom: 20px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        position: relative;
    }
    .main-title { font-size: 3.5rem; font-weight: 900; color: #fff; line-height: 1; text-align: center; text-shadow: 0 0 30px rgba(168, 85, 247, 0.6); }
    .sub-title { font-family: 'Courier New', monospace; font-size: 0.9rem; color: #d8b4fe; letter-spacing: 4px; text-transform: uppercase; margin-top: 10px; font-weight: 600; }
    .status-pill { position: absolute; bottom: 15px; right: 20px; background: rgba(16, 185, 129, 0.1); border: 1px solid #059669; color: #4ade80; padding: 4px 12px; border-radius: 99px; font-size: 0.7rem; font-weight: 700; }
    
    /* CARDS */
    .status-card { background: linear-gradient(145deg, #120520 0%, #050505 100%); border: 1px solid #3b0764; border-left: 5px solid #a855f7; border-radius: 12px; padding: 20px; height: 100%; }
    .yield-card { background: linear-gradient(135deg, #1e1b10 0%, #000000 100%); border: 1px solid #854d0e; border-right: 5px solid #eab308; border-radius: 12px; padding: 20px; text-align: center; height: 100%; }
    .diag-card { background: #0f0f0f; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-top: 25px; margin-bottom: 25px; }
    .doc-card { background: #0f0f0f; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #333; }
    
    /* TEXTO E VALORES */
    .card-label { font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 5px; }
    .big-val { font-size: 2.2rem; font-weight: 900; color: #fff; line-height: 1; margin-bottom: 5px; }
    .meta-badge { display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; margin-right: 5px; margin-top: 5px; }
    .bg-ph { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid #1e3a8a; }
    .bg-ec { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #064e3b; }
    
    /* TICKER ANIMATION */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-top: 1px solid #333; border-bottom: 1px solid #333; height: 30px; display: flex; align-items: center; margin-bottom: 20px; }
    .tick-item { margin-right: 40px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #a855f7; }
    .tick-val { color: #fff; margin-left: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR (PAINEL DE COMANDO BLINDADO)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ COMANDO SDI")
    st.caption("Central de Controle Agronômico")
    st.markdown("---")

    # A. GENÉTICA E AMBIENTE
    st.markdown("#### 🧬 Genética")
    genetica_sel = st.selectbox("Cepa / Strain", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
    
    st.markdown("#### 🏠 Ambiente")
    ambiente_sel = st.selectbox("Tipo de Local", [
        "Indoor (Luz Artificial)", 
        "Estufa (Luz Complementar)", 
        "Estufa (Somente Sol)", 
        "Outdoor (Sol Pleno)"
    ])
    
    # B. CRONOGRAMA
    st.markdown("#### 📅 Cronograma")
    data_inicio = st.date_input("Início do Ciclo", datetime.date.today() - datetime.timedelta(days=1))
    n_plantas = st.number_input("Nº de Plantas", 1, 500, 4)

    # C. SISTEMA RADICULAR
    st.markdown("#### 🌱 Raízes")
    metodo_sel = st.selectbox("Método/Substrato", list(db.get("METODOS_CULTIVO", {}).keys()))
    tipo_plantio = st.radio("Instalação", ["Vasos", "Canteiro/Chão"], horizontal=True)
    
    vol_vaso = 999
    if tipo_plantio == "Vasos":
        vol_vaso = st.select_slider("Volume do Vaso (L)", options=[4, 7, 11, 15, 20, 25, 30, 40, 50, 100], value=11)
    
    horas_luz = st.slider("Fotoperíodo (Horas/Dia)", 10, 24, 18)

    st.markdown("---")
    
    # D. ENGENHARIA (COM ALTURA E VOLUMETRIA V18)
    st.markdown("#### 💡 Engenharia & Dimensões")
    
    watts_painel = 0; area_m2 = 0; altura = 0
    largura = 0; profundidade = 0

    if "Indoor" in ambiente_sel:
        watts_painel = st.number_input("Potência LED (Watts Reais)", 50, 5000, 240)
        largura = st.number_input("Largura (cm)", 40, 1000, 80)
        profundidade = st.number_input("Profundidade (cm)", 40, 1000, 80)
        altura = st.number_input("Altura/Pé Direito (cm)", 60, 500, 160, help="Necessário para calcular exaustão (m³/h).")
        area_m2 = (largura * profundidade) / 10000
        
    elif "Complementar" in ambiente_sel: # Estufa com Luz
        watts_painel = st.number_input("Luz Extra (Watts)", 10, 5000, 100)
        largura = st.number_input("Largura Estufa (cm)", 100, 5000, 200)
        profundidade = st.number_input("Comprimento (cm)", 100, 5000, 200)
        altura = st.number_input("Altura Máxima (cm)", 100, 1000, 250)
        area_m2 = (largura * profundidade) / 10000

    elif "Somente Sol" in ambiente_sel:
        largura = st.number_input("Largura Estufa (cm)", 100, 5000, 200)
        profundidade = st.number_input("Comprimento (cm)", 100, 5000, 200)
        altura = st.number_input("Altura Máxima (cm)", 100, 1000, 250)
        area_m2 = (largura * profundidade) / 10000
    
    else: # Outdoor
        area_m2 = 999
        st.info("Cultivo em área aberta.")

    if area_m2 != 999:
        st.caption(f"Área: {area_m2:.2f} m² | Vol: {(area_m2*(altura/100)):.1f} m³")

# ==============================================================================
# 4. SDI INTELLIGENCE CORE V19 (CÁLCULOS & LÓGICA)
# ==============================================================================
# Bloco de inicialização para evitar NameError
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
mapa_ocupacao = {4: 0.04, 7: 0.06, 11: 0.09, 15: 0.11, 20: 0.14, 25: 0.16, 30: 0.20, 40: 0.25, 50: 0.30, 100: 0.50}

show_consultoria = False
titulo_consultoria = "ANÁLISE SDI"
txt_luz_titulo = "Dados insuficientes"; txt_luz_desc = "Configure a engenharia na barra lateral."
txt_espaco_titulo = "N/A"; txt_espaco_desc = ""
txt_raiz_titulo = "N/A"; txt_raiz_desc = ""
txt_clima_titulo = "N/A"; txt_clima_desc = ""
recomendacao_premium = ""
cor_card = "#a855f7" # Roxo Profissional

# Processamento Cronológico
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7
fase_atual = "Plântula"
if dias_vida > 14: fase_atual = "Vegetativo"
if dias_vida > 42: fase_atual = "Flora"

# --- A. ENGENHARIA DE ILUMINAÇÃO (PPFD/DLI) ---
dli = 0; ppfd = 0
if area_m2 > 0 and area_m2 != 999:
    show_consultoria = True
    
    if "Indoor" in ambiente_sel:
        # Cálculo Reverso de PPFD baseado na eficiência média de LEDs modernos (2.3 umol/J)
        ppfd = (watts_painel * 2.3) / area_m2
        dli = ppfd * horas_luz * 0.0036
        
        # Análise Contextual (Idade da Planta x Intensidade)
        if fase_atual == "Plântula":
            if ppfd > 400:
                txt_luz_titulo = f"⚠️ LUZ EXCESSIVA ({ppfd:.0f} PPFD)"
                txt_luz_desc = "Mudas e clones não suportam essa intensidade. As folhas vão curvar e travar. Reduza para 40% ou afaste o painel."
                cor_card = "#eab308"
            else:
                txt_luz_titulo = "✅ INTENSIDADE SEGURA"
                txt_luz_desc = "Nível ideal para enraizamento sem estresse térmico."
                cor_card = "#22c55e"
        
        elif fase_atual == "Vegetativo":
            if ppfd < 400:
                txt_luz_titulo = "⚠️ CRESCIMENTO LENTO"
                txt_luz_desc = "Energia insuficiente para ramificação lateral robusta."
                cor_card = "#eab308"
            elif ppfd > 850:
                 txt_luz_titulo = "🔥 LIMITE METABÓLICO"
                 txt_luz_desc = "Você está no limite máximo sem injeção de CO2."
            else:
                 txt_luz_titulo = "✅ VEGETATIVO VIGOROSO"
                 txt_luz_desc = "PPFD ideal para estrutura forte antes da flora."
                 cor_card = "#22c55e"

        elif fase_atual == "Flora":
            if dli < 30:
                txt_luz_titulo = f"⚠️ BAIXA ENERGIA (DLI {dli:.1f})"
                txt_luz_desc = "Insuficiente para buds densos. Espere flores 'aeradas' (pipoca)."
                recomendacao_premium = "Aumente a potência do LED ou reduza a área do grow."
                cor_card = "#eab308"
            elif dli > 45:
                txt_luz_titulo = f"🔥 SATURAÇÃO (DLI {dli:.1f})"
                txt_luz_desc = "Risco de queima (Bleaching). Obrigatório CO2 (1200ppm) e CalMag extra."
            else:
                txt_luz_titulo = f"🚀 FLORAÇÃO IDEAL (DLI {dli:.1f})"
                txt_luz_desc = "Sweet Spot para produção máxima de resina e peso."
                cor_card = "#22c55e"
            
    elif "Complementar" in ambiente_sel:
        ppfd_art = (watts_painel * 2.3) / area_m2
        txt_luz_titulo = f"SUPLEMENTAÇÃO: {ppfd_art:.0f} PPFD"
        txt_luz_desc = "Luz artificial auxiliando o Sol. Garante o fotoperíodo constante e aumenta o DLI em dias nublados."

    else:
        txt_luz_titulo = "☀️ LUZ SOLAR"
        txt_luz_desc = "Dependência do clima. Monitore a temperatura das raízes em dias muito quentes."
        cor_card = "#facc15"

# --- B. ENGENHARIA CLIMÁTICA & HVAC (V18) ---
if area_m2 > 0 and area_m2 != 999 and altura > 0:
    volume_m3 = area_m2 * (altura / 100)
    # Troca de ar recomendada: 60 vezes por hora (1x por minuto)
    trocas_hora = volume_m3 * 60
    
    txt_clima_titulo = f"VOLUMETRIA: {volume_m3:.1f} m³"
    
    if "Indoor" in ambiente_sel:
        if altura < 160:
            txt_clima_desc = f"⚠️ TETO BAIXO ({altura}cm). Calor acumula rápido. Sua exaustão real deve ser > <b>{trocas_hora:.0f} m³/h</b>."
            if not recomendacao_premium: recomendacao_premium = "Monitore a temperatura do topo das plantas (Canopy) diariamente."
        else:
            txt_clima_desc = f"Para renovar o ar (CO2) 60x por hora, seu exaustor deve ter vazão real > <b>{trocas_hora:.0f} m³/h</b>."
    else:
        txt_clima_desc = f"Volume de ar na estufa: {volume_m3:.1f} m³. Garanta janelas laterais ou exaustores para remover umidade."

# --- C. FÍSICA E ESPAÇO ---
if area_m2 != 999 and show_consultoria:
    if tipo_plantio == "Vasos":
        area_uni = mapa_ocupacao.get(vol_vaso, 0.15)
        area_req = n_plantas * area_uni
        ocupacao = (area_req / area_m2) * 100
        
        if ocupacao > 110:
            txt_espaco_titulo = f"🚫 ERRO FÍSICO ({ocupacao:.0f}%)"
            txt_espaco_desc = "Impossível caber fisicamente. Plantas vão crescer umas sobre as outras."
            cor_card = "#ef4444"
            recomendacao_premium = "Remova plantas fracas (Culling) imediatamente."
        elif ocupacao > 85:
            txt_espaco_titulo = "⚠️ ALTA DENSIDADE"
            txt_espaco_desc = "Risco de mofo (Botrytis). Poda 'canela nua' obrigatória."
            if cor_card != "#ef4444": cor_card = "#eab308"
        else:
            txt_espaco_titulo = "✅ ESPAÇO OTIMIZADO"
            txt_espaco_desc = "Boa circulação de ar e penetração de luz."
    else:
        txt_espaco_titulo = "🌿 SOLO LIVRE"
        txt_espaco_desc = "Sem restrição de área."

# --- D. RAÍZES E SUBSTRATO ---
if tipo_plantio == "Vasos":
    if info_genetica['tipo'] == "Auto":
        if vol_vaso < 7:
            txt_raiz_titulo = "⚠️ VASO PEQUENO"
            txt_raiz_desc = "Limita crescimento da automática. Resultará em planta pequena."
        elif vol_vaso > 25:
            txt_raiz_titulo = "ℹ️ SUBSTRATO EXTRA"
            txt_raiz_desc = "Planta não colonizará tudo antes de morrer. Desperdício."
        else:
            txt_raiz_titulo = "✅ VOLUME IDEAL"
            txt_raiz_desc = "Perfeito para o ciclo rápido."
    else: # Foto
        if vol_vaso < 11 and dias_vida > 30:
            txt_raiz_titulo = "⚠️ ROOT BOUND (Raiz Presa)"
            txt_raiz_desc = "Raiz sufocada. Transplante para vaso maior é necessário."
            if not recomendacao_premium: recomendacao_premium = "Transplante antes de virar para floração."
        else:
            txt_raiz_titulo = "✅ VOLUME OK"
            txt_raiz_desc = "Sustenta bem o desenvolvimento."
else:
    txt_raiz_titulo = "🌍 SOLO"
    txt_raiz_desc = "Atenção à compactação."

# --- CÁLCULOS FINAIS ---
fator_luz = 1.0
if "Indoor" in ambiente_sel and dli > 0:
    if dli < 20: fator_luz = 0.6
    elif dli > 40: fator_luz = 1.1

yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas * fator_luz
yield_kg = yield_total / 1000 

fase_nome = "Indefinida"; fase_dados = {}
range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
fator_ciclo = 0.75 if info_genetica.get("tipo") == "Auto" else 1.0

for k, v in db.get("FASES_DINAMICAS", {}).items():
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: fase_nome = k; fase_dados = v; break

# ==============================================================================
# 5. DASHBOARD VISUAL (PÁGINA PRINCIPAL)
# ==============================================================================

# HERO
st.markdown("""
<div class="hero-card">
    <div class="status-pill">🍁 SISTEMA ONLINE</div>
    <div class="main-title">AGROWER <span style="color:#a855f7">SDI</span></div>
    <div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
</div>
""", unsafe_allow_html=True)

# TICKER
st.markdown("""
<div class="ticker-wrap">
    <div style="display:inline-block; white-space:nowrap; animation:ticker 45s linear infinite;">
        <span class="tick-item">VPD <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">TEMP <span class="tick-val">22-26°C</span></span>
        <span class="tick-item">UMIDADE <span class="tick-val">45-50%</span></span>
        <span class="tick-item">CO2 <span class="tick-val">400-800 ppm</span></span>
        <span class="tick-item">DLI <span class="tick-val">35-45 mol</span></span>
    </div>
</div>
<style>@keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }</style>
""", unsafe_allow_html=True)

# CÁLCULO DE ESTIMATIVA & PROGRESSO
# 2. CÁLCULOS DE PROGRESSO E ESTRATÉGIA
ciclo_total_dias = info_genetica.get('ciclo_dias', 90) + 30
dias_restantes = max(0, ciclo_total_dias - dias_vida)
progresso_pct = min(100, max(0, int((dias_vida / ciclo_total_dias) * 100)))

# ==============================================================================
# CARDS SUPERIORES (STATUS V21 + YIELD) - COM TEMP E UMIDADE
# ==============================================================================

# 1. CRIAÇÃO DAS COLUNAS
col_a, col_b = st.columns([1.8, 1.2]) 

# 2. CÁLCULOS DE PROGRESSO E ESTRATÉGIA
ciclo_total_dias = info_genetica.get('ciclo_dias', 90) + 30 
dias_restantes = max(0, ciclo_total_dias - dias_vida)
progresso_pct = min(100, max(0, int((dias_vida / ciclo_total_dias) * 100)))

# 3. BASE DE CONHECIMENTO CLIMÁTICO (TEMP & UMIDADE POR FASE)
# Define os alvos ideais dependendo da fase atual
mapa_clima_ideal = {
    "Plântula":    {"temp": "20-25°C", "rh": "65-80%"},
    "Vegetativo":  {"temp": "22-28°C", "rh": "55-70%"},
    "Pré-Flora":   {"temp": "21-26°C", "rh": "50-60%"},
    "Flora Inicial": {"temp": "21-26°C", "rh": "45-55%"},
    "Flora Média":   {"temp": "20-25°C", "rh": "40-50%"},
    "Flora Final":   {"temp": "18-23°C", "rh": "35-45%"} # Mais frio para terpenos
}
# Pega os dados da fase atual (ou usa um padrão seguro se não encontrar)
alvos_clima = mapa_clima_ideal.get(fase_nome, {"temp": "22-26°C", "rh": "50-60%"})

# Dicionário de Conselhos (Estratégia)
conselhos_fase = {
    "Plântula": "🌱 <b>Foco:</b> Sobrevivência. Mantenha a umidade alta (cúpula) e não exagere na água.",
    "Vegetativo": "🌿 <b>Foco:</b> Estrutura. A planta precisa crescer folhas e galhos fortes. Hora de podas e amarras (LST).",
    "Pré-Flora": "🚀 <b>Foco:</b> Estirão. A planta vai dobrar de tamanho. Ajuste a altura da luz diariamente.",
    "Flora Inicial": "🌸 <b>Foco:</b> Formação. Os pistilos apareceram. Pare o Nitrogênio e aumente Fósforo/Potássio.",
    "Flora Média": "💪 <b>Foco:</b> Engorda. Os buds estão inchando. Garanta ventilação máxima para evitar mofo.",
    "Flora Final": "💎 <b>Foco:</b> Resina e Sabor. Reduza a temperatura e umidade para destacar os terpenos e evitar Botrytis."
}
texto_estrategico = conselhos_fase.get(fase_nome, "Mantenha os parâmetros estáveis e monitore o clima.")

# --- COLUNA A: STATUS CARD V21 (AGORA COM 4 MÉTRICAS DE CLIMA) ---
with col_a:
    meta_vpd = fase_dados.get('meta_vpd', '-')
    meta_ppfd = fase_dados.get('meta_ppfd', '-')
    regime_luz = fase_dados.get('luz_h', '-')
    
    # HTML SEM INDENTAÇÃO (BLINDADO)
    html_status = f"""
<div class="status-card">
<div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;">
<div>
<div class="card-label" style="color:#a855f7;">FASE ATUAL ({info_genetica.get('tipo', 'Foto').upper()})</div>
<div class="big-val" style="font-size:1.8rem; margin-bottom:0;">{fase_nome.upper()}</div>
<div style="font-size:0.75rem; color:#888; font-style:italic; margin-bottom:5px;">Semanas de vida: {semanas}</div>
<div style="background:#3b0764; color:#d8b4fe; padding:2px 8px; border-radius:4px; font-size:0.7rem; display:inline-block; font-weight:bold;">
💡 LUZ: {regime_luz}H/DIA
</div>
</div>
<div style="text-align:right; width:45%;">
<div class="card-label">PROGRESSO DO CICLO</div>
<div style="font-size:1.4rem; font-weight:bold; color:#fff;">{progresso_pct}% <span style="font-size:0.8rem; color:#888;">CONCLUÍDO</span></div>
<div style="width:100%; background:#333; height:8px; border-radius:10px; margin-top:5px; overflow:hidden;">
<div style="width:{progresso_pct}%; background:linear-gradient(90deg, #a855f7, #d8b4fe); height:100%; border-radius:10px;"></div>
</div>
<div style="font-size:0.7rem; color:#666; margin-top:4px;">Faltam aprox. {dias_restantes} dias</div>
</div>
</div>
<div style="height:1px; background:#333; margin:15px 0;"></div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-top:10px;">
<div>
<div class="card-label" style="margin-bottom:8px;">🎯 ALVOS DE NUTRIÇÃO</div>
<div style="display:flex; flex-direction:column; gap:6px;">
<div style="display:flex; align-items:center; gap:6px;">
<span class="meta-badge bg-ph">💧 PH {info_metodo['ph_ideal']}</span>
<span style="font-size:0.65rem; color:#666;">(Acidez)</span>
</div>
<div style="display:flex; align-items:center; gap:6px;">
<span class="meta-badge bg-ec">⚡ EC {info_metodo['ec_ideal']}</span>
<span style="font-size:0.65rem; color:#666;">(Nutrientes)</span>
</div>
</div>
</div>
<div>
<div class="card-label" style="margin-bottom:8px;">🌤️ ALVOS DE CLIMA</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
<div title="Força da Luz Ideal">
<span class="meta-badge" style="background:rgba(234, 179, 8, 0.15); color:#facc15; border:1px solid #854d0e; width:100%; text-align:center; display:block;">☀️ {meta_ppfd}</span>
<div style="font-size:0.6rem; color:#666; text-align:center; margin-top:2px;">PPFD</div>
</div>
<div title="Déficit de Pressão de Vapor">
<span class="meta-badge" style="background:rgba(236, 72, 153, 0.15); color:#f472b6; border:1px solid #831843; width:100%; text-align:center; display:block;">🌫️ {meta_vpd}</span>
<div style="font-size:0.6rem; color:#666; text-align:center; margin-top:2px;">VPD (kPa)</div>
</div>
<div title="Temperatura Ambiente Ideal">
<span class="meta-badge" style="background:rgba(249, 115, 22, 0.15); color:#fdba74; border:1px solid #9a3412; width:100%; text-align:center; display:block;">🌡️ {alvos_clima['temp']}</span>
<div style="font-size:0.6rem; color:#666; text-align:center; margin-top:2px;">TEMP</div>
</div>
<div title="Umidade Relativa Ideal">
<span class="meta-badge" style="background:rgba(6, 182, 212, 0.15); color:#67e8f9; border:1px solid #155e75; width:100%; text-align:center; display:block;">☁️ {alvos_clima['rh']}</span>
<div style="font-size:0.6rem; color:#666; text-align:center; margin-top:2px;">UMIDADE</div>
</div>
</div>
</div>
</div>
<div style="margin-top:20px; background:rgba(255,255,255,0.03); padding:12px; border-radius:8px; border-left:3px solid #a855f7;">
<div class="card-label" style="margin:0; color:#a855f7; margin-bottom:4px;">ESTRATÉGIA DA SEMANA:</div>
<div style="color:#e4e4e7; font-size:0.85rem; line-height:1.4;">
{texto_estrategico}
</div>
</div>
</div>
"""
    st.markdown(html_status, unsafe_allow_html=True)

# ==============================================================================
# CARD: PREDIÇÃO DE SAFRA INTELIGENTE (ALGORITMO V40)
# ==============================================================================
with col_b:
    
    # --- 1. MOTOR DE CÁLCULO DE BIOMASSA (O CÉREBRO) ---
    
    # A. Base de Produtividade por Genética (g/planta em condições médias)
    base_yield = 40 # Média padrão konservadora
    tipo_gen = info_genetica.get('tipo', 'Foto')
    if "Sativa" in ambiente_sel: base_yield = 55
    if "Indica" in ambiente_sel: base_yield = 45
    if "Auto" in tipo_gen: base_yield = 30 # Autos produzem menos em média
    
    # B. Fator Vaso (Volume de Raiz)
    # Vaso de 7L é o padrão (fator 1.0). 
    # Vaso 20L -> fator 1.5 | Vaso 50L -> fator 2.2
    # Usamos uma lógica simplificada de curva:
    vol_ref = 7.0
    if vol_vaso == 999: # Chão
        fator_vaso = 3.5 # Planta no chão cresce muito
        txt_vaso = "Cultivo em Solo (Raízes Livres)"
    else:
        # Fórmula: Cada dobra de tamanho adiciona 50% de yield, até um limite
        import math
        fator_vaso = 1 + (math.log(vol_vaso / vol_ref) * 0.6) if vol_vaso > vol_ref else (vol_vaso / vol_ref)
        fator_vaso = max(0.5, min(fator_vaso, 4.0)) # Trava entre 0.5x e 4x
        txt_vaso = f"Vaso de {vol_vaso}L"

    # C. Fator Ambiente & Luz
    fator_luz = 1.0
    txt_luz_yield = "Luz Padrão"
    
    if "Indoor" in ambiente_sel:
        # Indoor depende dos Watts
        fator_luz = 1.2 + (watts_painel / (n_plantas * 100)) # Mais watts por planta = mais yield
        txt_luz_yield = "Indoor Controlado"
    elif "Outdoor" in ambiente_sel and "Luz Comp" in ambiente_sel: # Outdoor Misto
        fator_luz = 1.5 # Sol + LED é o cenário mais produtivo
        txt_luz_yield = "Sol Pleno + Complemento"
    elif "Outdoor" in ambiente_sel:
        fator_luz = 1.0 # Sol apenas (depende do clima, média)
        txt_luz_yield = "Outdoor (Sol)"
    elif "Estufa" in ambiente_sel:
        fator_luz = 1.3
        txt_luz_yield = "Estufa Agrícola"

    # D. Fator Método (Nutrição)
    fator_metodo = 1.0
    if "Hidro" in metodo_sel or "Coco" in metodo_sel or "DWC" in metodo_sel:
        fator_metodo = 1.3 # Hidro cresce 30% mais rápido/maior
        txt_metodo_yield = "Alta Performance (Hidro/Coco)"
    elif "Orgânico" in metodo_sel:
        fator_metodo = 1.0 # Foco em qualidade, volume normal
        txt_metodo_yield = "Orgânico (Solo Vivo)"
    else:
        txt_metodo_yield = "Convencional"

    # --- CÁLCULO FINAL ---
    estimativa_g_planta = base_yield * fator_vaso * fator_luz * fator_metodo
    estimativa_total_g = estimativa_g_planta * n_plantas
    estimativa_total_kg = estimativa_total_g / 1000

    # Definição de Cores da Safra
    cor_yield = "#facc15" # Amarelo Ouro
    if estimativa_total_g > 500: cor_yield = "#22c55e" # Verde (Alta produção)
    
    # HTML DO CARD DE PRODUÇÃO (COM EXPLICAÇÃO DOS PARÂMETROS)
    html_yield = f"""
<div class="yield-card" style="height:100%; display:flex; flex-direction:column; justify-content:space-between;">
        
<div>
<div class="card-label" style="color:#fcd34d; margin-bottom:5px;">ESTIMATIVA DE SAFRA (SECO)</div>
<div class="big-val" style="color:{cor_yield}; font-size:2.2rem; line-height:1;">{estimativa_total_g:.0f}g</div>
<div class="sub-info" style="color:#fef08a; font-size:0.9rem;">~ {estimativa_total_kg:.2f} kg Totais</div>
<div style="font-size:0.75rem; color:#888; margin-top:2px;">Média: <b>{estimativa_g_planta:.0f}g / planta</b></div>
</div>

<div style="height:1px; background:#422006; margin:10px 0;"></div>

<div style="background:rgba(0,0,0,0.2); padding:8px; border-radius:6px; border:1px solid #422006;">
<div style="font-size:0.65rem; color:#ca8a04; font-weight:bold; margin-bottom:4px;">PARÂMETROS DO CÁLCULO:</div>
            
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
<span style="font-size:0.7rem; color:#ccc;">🪴 {txt_vaso}</span>
<span style="font-size:0.7rem; color:{'#4ade80' if fator_vaso > 1.2 else '#888'}; font-weight:bold;">x{fator_vaso:.1f}</span>
</div>
            
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
<span style="font-size:0.7rem; color:#ccc;">☀️ {txt_luz_yield}</span>
<span style="font-size:0.7rem; color:{'#4ade80' if fator_luz > 1.1 else '#888'}; font-weight:bold;">x{fator_luz:.1f}</span>
</div>
            
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="font-size:0.7rem; color:#ccc;">💧 {txt_metodo_yield}</span>
<span style="font-size:0.7rem; color:{'#4ade80' if fator_metodo > 1.0 else '#888'}; font-weight:bold;">x{fator_metodo:.1f}</span>
</div>
</div>
        
<div style="margin-top:8px; font-size:0.65rem; color:#666; font-style:italic; line-height:1.2;">
            *Estimativa baseada em genética {info_genetica['tipo']} com manejo ideal. Variações climáticas afetam o resultado.
</div>
</div>
    """
    st.markdown(html_yield, unsafe_allow_html=True)

# ==============================================================================
# CARD CONSULTORIA: PRESCRIÇÃO AGRONÔMICA & CROP STEERING (V43 - MASTER)
# ==============================================================================
if show_consultoria:
    titulo_card = f"OPERAÇÕES TÁTICAS: SEMANA {semanas}"
    cor_brand = "#a855f7" 
    
    # 1. LÓGICA DE IDADE FISIOLÓGICA DINÂMICA
    ciclo_total_dias = info_genetica.get('ciclo_dias', 90) + 30 
    progresso_ciclo = min(1.0, dias_vida / ciclo_total_dias)
    idx_tatico = min(8, int(progresso_ciclo * 8.99))
    
    # 2. VERIFICAÇÃO DO SISTEMA DE CULTIVO
    is_organic = "Orgânico" in metodo_sel or "KNF" in metodo_sel or "Solo Vivo" in metodo_sel
    tipo_txt = "ORGÂNICO/BIOLÓGICO" if is_organic else "MINERAL/HIDRO"
    
    # 3. CÉREBRO DE MANEJO INTEGRADO (DATABASE PREMIUM V43)
    # Informações aprofundadas sobre metabolismo, crop steering e MIP (Manejo Integrado de Pragas)
    manejos = {
        0: {
            "fase": "Enraizamento & Aclimatação", "icone": "🌱", 
            "foco_nutri": "Desenvolvimento do Meristema Radicular (Fósforo e Auxinas).", 
            "manejo": "<b>Steering Vegetativo:</b> Mantenha VPD baixo (0.4-0.8 kPa) e umidade >70% (Domo). A pressão de turgor é mantida por absorção foliar enquanto o sistema radicular pivotante se estabelece. Evite saturação do substrato (água em excesso asfixia as raízes e atrai <i>Pythium</i>).", 
            "org_prod": "Endomicorrizas + Trichoderma harzianum + Ácido Húmico", "org_dose": 2.0, "org_modo": "g/L inoculado direto no berço/raiz", 
            "min_prod": "Ácido Indolbutírico (Clonex) ou Enraizador Base Kelp", "min_dose": 1.0, "min_modo": "ml/L via rega leve (Runoff 0%)", 
            "futuro": "Preparação para a fase de crescimento exponencial (Vigor Híbrido). Introduza ventilação indireta nos próximos dias.", 
            "esqueceu": "<b>MIP:</b> Não inoculou biológicos no solo? Faça uma rega (Drench) com Beauveria bassiana preventivamente contra Fungus Gnats."
        },
        1: {
            "fase": "Vegetativo Inicial (Crescimento Exponencial)", "icone": "🌿", 
            "foco_nutri": "Síntese de Clorofila e Aminoácidos (Nitrogênio Alto).", 
            "manejo": "<b>Steering Vegetativo:</b> Aumente a intensidade luminosa (DLI) gradativamente. Permita 'Drybacks' (secas) de 15-20% entre as regas para forçar as raízes a explorarem o fundo do vaso. O vento deve balançar levemente a planta para causar microfissuras no caule, engrossando-o via lignificação.", 
            "org_prod": "Rega com Chá de Húmus Aerado ou FPJ (Suco Fermentado de Planta rica em N)", "org_dose": 5.0, "org_modo": "ml/L via rega lenta", 
            "min_prod": "Nutrição Base Grow (N-P-K Focado em N) + Silício (Silicato de Potássio)", "min_dose": 1.5, "min_modo": "ml/L na água de rega (Ajuste pH 5.8-6.2)", 
            "futuro": "Formação dos primeiros nós fortes. O relógio biológico está pronto para o primeiro treinamento de alto estresse (HST).", 
            "esqueceu": "Caule fino ou tombando? A deficiência de vento ou luz fraca causa estiolamento. Abaixe a luz e aplique Silício foliar."
        },
        2: {
            "fase": "Estruturação & Quebra de Dominância", "icone": "✂️", 
            "foco_nutri": "Redistribuição Hormonal (Citocininas vs Auxinas). Cálcio para paredes celulares.", 
            "manejo": "<b>Manejo Físico:</b> Execute Poda Apical (Topping) ou FIM. Isso corta a produção de auxina no topo, forçando a planta a enviar energia (citocininas) para os galhos laterais. Inicie o LST (Low Stress Training) amarrando os galhos em 90° para quebrar a dominância apical e criar um dossel plano e uniforme.", 
            "org_prod": "Top Dressing: Torta de Mamona (N) + Bokashi (Microbiologia ativa)", "org_dose": 4.0, "org_modo": "g/L espalhado na superfície do solo", 
            "min_prod": "Nutrição Base Grow (Pico de EC: 1.5 a 1.8) + Suplemento CalMag", "min_dose": 2.0, "min_modo": "ml/L via rega com 10% de Runoff", 
            "futuro": "Transição de fotoperíodo iminente. A planta precisará de suporte físico estrutural para aguentar o peso futuro.", 
            "esqueceu": "<b>MIP Prevencionista:</b> Pulverize Óleo de Neem + Sabão Potássico antes de mudar para flora. Após o surgimento das flores, foliares são proibidos."
        },
        3: {
            "fase": "Pré-Flora / Estirão (Stretch)", "icone": "🕸️", 
            "foco_nutri": "Pico de Fósforo (ATP/Energia) e transição metabólica rápida.", 
            "manejo": "<b>Steering Transicional:</b> A mudança de fotoperíodo causa uma explosão de ácido giberélico, alongando os internódios (Stretch). A planta pode dobrar ou triplicar de tamanho em 14 dias. Instale a malha SCROG agora. Direcione os galhos através dos quadrados diariamente. Mantenha o VPD em 1.0-1.2 kPa.", 
            "org_prod": "Transição: Farinha de Osso (Fósforo Lento) + WCA (Cálcio Solúvel KNF)", "org_dose": 3.0, "org_modo": "g/L no solo + 2ml/L WCA na água", 
            "min_prod": "Mistura 50% Grow / 50% Bloom (Evite cortar o Nitrogênio abruptamente)", "min_dose": 2.0, "min_modo": "ml/L (Manter EC alto: 1.8 - 2.0)", 
            "futuro": "Formação das coroas florais. O crescimento vertical vai parar bruscamente na semana 3 de flora.", 
            "esqueceu": "Dossel irregular? Faça 'Supercropping' estalando os galhos mais altos para nivela-los com os menores, evitando queimadura por luz (Light Burn)."
        },
        4: {
            "fase": "Formação de Botão Floral (Lollipopping)", "icone": "🦵", 
            "foco_nutri": "Formação de Cálices. Alta demanda de Fósforo (P).", 
            "manejo": "<b>Operação Cirúrgica:</b> Execute o 'Lollipopping'. Remova implacavelmente toda a folhagem, brotos e galhos finos no terço inferior da planta (onde a luz não bate >200 PPFD). Isso redireciona fotossintatos apenas para os colas superiores, evitando 'buds pipoca' (larf). Mantenha as 'Fan Leaves' superiores como painéis solares.", 
            "org_prod": "Top Dressing: Guano de Morcego (Bloom) + Rega com FFJ (Fermentado de Fruta)", "org_dose": 4.0, "org_modo": "g/L solo + 2ml/L FFJ via rega", 
            "min_prod": "Fertilizante Bloom Base Puro (Cortar Grow) + Estimulador de Floração", "min_dose": 2.5, "min_modo": "ml/L (EC 2.0 a 2.2)", 
            "futuro": "Os cálices começarão a inchar e empilhar (stacking). O metabolismo muda para síntese de terpenos e canabinoides.", 
            "esqueceu": "A planta está uma selva muito densa? Faça uma defoliação estrutural no meio (ventilação), ou você terá sérios problemas com microclimas úmidos."
        },
        5: {
            "fase": "Engorda Inicial (Bulking)", "icone": "🛑", 
            "foco_nutri": "Início do Pico de Potássio (K) para transporte de carboidratos.", 
            "manejo": "<b>Steering Generativo:</b> Proibido podas e estresses de alto impacto (HST). Induza a planta à reprodução aumentando os 'Drybacks' (deixe secar 30-40% antes de regar novamente). Regas pontuais com grande volume (Shot Size alto). Isso força a planta a produzir resina como mecanismo de defesa e a inchar os cálices buscando reter água.", 
            "org_prod": "Cinzas de Madeira (K) + Extrato de Algas (Citoquininas naturais)", "org_dose": 3.0, "org_modo": "g/L diluído em água morna", 
            "min_prod": "Bloom Base + Introdução de PK Booster (PK 13/14)", "min_dose": 2.0, "min_modo": "ml/L + 1ml/L PK (Atenção a pontas queimadas)", 
            "futuro": "O peso das flores testará a integridade dos galhos. O odor ficará forte (ative filtros de carvão).", 
            "esqueceu": "As pontas das folhas amarelaram (Nutrient Burn)? O EC do solo subiu demais com os drybacks. Faça uma rega apenas com água e enzimas para equilibrar a osmose."
        },
        6: {
            "fase": "Engorda Pesada & Empilhamento", "icone": "🏋️", 
            "foco_nutri": "Pico Crítico de Potássio (K). Absorção massiva de água (Transpiração).", 
            "manejo": "<b>Controle Ambiental Crítico:</b> O VPD deve estar cravado em 1.4 a 1.6 kPa para a planta transpirar o máximo possível, puxando o Potássio da raiz para as flores. Monitore a Umidade Relativa: se passar de 55% à noite com temperaturas caindo, o ponto de orvalho causará condensação dentro do bud, gerando <i>Botrytis cinerea</i> (Bud Rot/Mofo Cinzento).", 
            "org_prod": "Chá de Banana Aerado por 24h + Melaço de Cana (Carboidratos para o solo)", "org_dose": 5.0, "org_modo": "ml/L via rega profunda", 
            "min_prod": "Heavy PK Booster / Finalizador de Engorda (Pico Máximo de EC: 2.4 - 2.6)", "min_dose": 3.0, "min_modo": "ml/L via rega programada", 
            "futuro": "Os pistilos brancos vão retrair e oxidar (ficar laranjas/marrons). Os cálices vão inchar, engolindo as folhinhas de açúcar.", 
            "esqueceu": "Galhos caindo com o peso? Amarre-os urgentemente. Se o galho tombar, a planta restringe o fluxo de seiva para aquela flor, paralisando a engorda."
        },
        7: {
            "fase": "Maturação (Senescência & Terpenos)", "icone": "❄️", 
            "foco_nutri": "Esgotamento Nutricional (Fade). Síntese extrema de Óleos Essenciais.", 
            "manejo": "<b>Steering de Finalização:</b> Zere o Nitrogênio. O amarelecimento (Fade) e aparecimento de cores roxas/pretas (Antocianinas) é o objetivo botânico agora. Para maximizar tricomas, baixe a temperatura noturna (18°C) e reduza a intensidade da luz gradativamente (simulando a chegada do inverno). Inicie a observação diária com microscópio: 70% leitoso / 30% âmbar é o ponto comercial padrão.", 
            "org_prod": "Zero N-P-K. Apenas LAB (Bactérias Ácido Láticas) diluído levemente para limpar microbiota.", "org_dose": 1.0, "org_modo": "ml/L de água purificada", 
            "min_prod": "Sweetener / Cleanser (Ácidos húmicos/fúlvicos para quebrar sais residuais)", "min_dose": 2.0, "min_modo": "ml/L via rega", 
            "futuro": "Semana de Lavagem final (Flush). Preparação do ambiente de secagem.", 
            "esqueceu": "A flor ainda está lançando pistilos brancos novos sem parar (Foxtailing)? Estresse térmico ou luminoso excessivo. Afaste a luz e baixe a temperatura do grow."
        },
        8: {
            "fase": "Colheita & Preparo Pós-Colheita", "icone": "🚿", 
            "foco_nutri": "Absorção Zero. Forçando o consumo das reservas internas.", 
            "manejo": "<b>Estresse Osmótico (Flush):</b> Regue com volume de 20 a 30% a mais para gerar escoamento limpo. Isso retira os sais da zona de raiz, forçando a planta a devorar suas próprias folhas (melhorando muito o sabor e queima final). Antes do corte, faça 48h de escuridão total para degradar a clorofila restante e estressar a planta a produzir uma última camada defensiva de resina.", 
            "org_prod": "Apenas Água com pH Neutro (6.0 a 6.5). Deixe a água descansar 24h para evaporar cloro.", "org_dose": 0, "org_modo": "Rega de Lavagem (Flush)", 
            "min_prod": "Solução de Flush (Flawless Finish / Clearex) para quelatar sais minerais pesados.", "min_dose": 2.0, "min_modo": "ml/L via rega de lavagem profunda", 
            "futuro": "Corte as plantas pela base. Seque a 16-18°C com 60% de Umidade Constante por 10 a 14 dias.", 
            "esqueceu": "Tem pragas microscópicas na colheita? Faça um 'Bud Washing' (banho suave de água com peróxido de hidrogênio e bicarbonato) logo após cortar os galhos."
        }
    }
    
    d = manejos.get(idx_tatico, manejos[8])

    # 4. PRESCRIÇÃO CALCULADA PARA O TAMANHO DO VASO
    receita_txt = ""
    produto_sugerido = d['org_prod'] if is_organic else d['min_prod']
    modo_aplicacao = d['org_modo'] if is_organic else d['min_modo']
    
    if d['org_dose'] == 0:
        receita_txt = "Apenas água. Protocolo de restrição nutricional ativo."
    elif is_organic and "g/L" in d['org_modo']:
        vaso_calc = 20 if vol_vaso == 999 else vol_vaso
        dose_total = d['org_dose'] * vaso_calc
        receita_txt = f"Calibrado para vaso de {vaso_calc}L: Aplicar <b>{dose_total:.1f}g</b> de produto total."
    elif is_organic:
        receita_txt = f"Diluir <b>{d['org_dose']} {modo_aplicacao.split(' ')[0]}</b> por Litro de água limpa."
    else:
        receita_txt = f"Diluir <b>{d['min_dose']} {modo_aplicacao.split(' ')[0]}</b> por Litro de água com pH ajustado."

    # HTML BLINDADO (ZERO INDENTAÇÃO INTERNA)
    html_consultoria = f"""
<div class="diag-card" style="border-left: 4px solid {cor_brand}; background: linear-gradient(170deg, #18181b 0%, #09090b 100%); padding:20px; border-radius:15px; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
<div style="display:flex; align-items:center; gap:12px;">
<div style="background:{cor_brand}; width:45px; height:45px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.5rem; box-shadow: 0 0 10px {cor_brand}40;">{d['icone']}</div>
<div>
<div style="font-weight:900; color:{cor_brand}; font-size:1.1rem; letter-spacing:0.5px;">CONSULTORIA MASTER GROWER</div>
<div style="font-size:0.75rem; color:#888;">ESTÁGIO FENOLÓGICO: <b style="color:#fff;">{d['fase'].upper()}</b></div>
</div>
</div>
</div>
<div style="display:grid; grid-template-columns: 1fr; gap:15px;">
<div style="background:rgba(255,255,255,0.03); border:1px solid #333; border-radius:10px; padding:15px; position:relative; overflow:hidden;">
<div style="position:absolute; top:0; left:0; width:4px; height:100%; background:#22c55e;"></div>
<div style="margin-left:10px;">
<div style="color:#22c55e; font-size:0.8rem; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">🎯 METABOLISMO & CROP STEERING</div>
<div style="color:#a8a29e; font-size:0.8rem; font-weight:bold; margin-bottom:6px; border-bottom:1px dashed #444; padding-bottom:4px;">📈 {d['foco_nutri']}</div>
<div style="color:#e4e4e7; font-size:0.95rem; line-height:1.6; text-align:justify;">{d['manejo']}</div>
</div>
</div>
<div style="background:rgba(255,255,255,0.03); border:1px solid #333; border-radius:10px; padding:15px; position:relative; overflow:hidden;">
<div style="position:absolute; top:0; left:0; width:4px; height:100%; background:#3b82f6;"></div>
<div style="margin-left:10px;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
<div style="color:#3b82f6; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">💊 PROTOCOLO NUTRICIONAL & BIOTECNOLÓGICO ({tipo_txt})</div>
</div>
<div style="background:rgba(59, 130, 246, 0.1); border:1px solid rgba(59, 130, 246, 0.3); padding:10px; border-radius:6px;">
<div style="color:#fff; font-size:0.9rem; font-weight:bold; margin-bottom:4px;">🧪 Insumo Sugerido: <span style="color:#93c5fd;">{produto_sugerido}</span></div>
<div style="color:#e4e4e7; font-size:0.9rem;">⚖️ Cálculo de Aplicação: <span style="color:#60a5fa; font-weight:bold;">{receita_txt}</span></div>
<div style="color:#888; font-size:0.75rem; margin-top:4px;"><i>Via: {modo_aplicacao}</i></div>
</div>
</div>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
<div style="background:rgba(234, 179, 8, 0.05); border:1px solid rgba(234, 179, 8, 0.2); padding:12px; border-radius:8px;">
<div style="color:#facc15; font-size:0.75rem; font-weight:bold; margin-bottom:5px;">🔮 RADAR AGRONÔMICO (FUTURO)</div>
<div style="color:#ddd; font-size:0.85rem; line-height:1.4;">{d['futuro']}</div>
</div>
<div style="background:rgba(239, 68, 68, 0.05); border:1px solid rgba(239, 68, 68, 0.2); padding:12px; border-radius:8px;">
<div style="color:#f87171; font-size:0.75rem; font-weight:bold; margin-bottom:5px;">⚠️ MITIGAÇÃO DE DANOS (ESQUECEU?)</div>
<div style="color:#ddd; font-size:0.85rem; line-height:1.4;">{d['esqueceu']}</div>
</div>
</div>
</div>
<div style="margin-top:15px; text-align:center; font-size:0.7rem; color:#555;">
<i>Motor de Predição Ativo: Progresso Cronológico ajustado em {int(progresso_ciclo*100)}% base Genética {info_genetica['tipo']}.</i>
</div>
</div>
"""
    st.markdown(html_consultoria, unsafe_allow_html=True)

# ==============================================================================
# PAINEL DE TELEMETRIA E CRONOGRAMA VISUAL (V46 - DIF TÉRMICO)
# ==============================================================================
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True) 

# 1. LÓGICA DO CRONOGRAMA (TIMELINE)
pct = progresso_ciclo * 100
step = 1
if pct > 15: step = 2 # Vega
if pct > 45: step = 3 # Pré-Flora
if pct > 65: step = 4 # Engorda
if pct > 90: step = 5 # Colheita

def cor_step(s): return "#a855f7" if step >= s else "#333"
def cor_texto(s): return "#fff" if step >= s else "#666"

# 2. DIRETRIZES DE REGA (DRYBACK RÁPIDO)
rega_estrategia = "Manter Úmido (Sem Encharcar)"
if step == 2: rega_estrategia = "Seca de 20% (Dryback Leve) entre regas"
elif step == 3: rega_estrategia = "Rega de Alto Volume (Sem secar muito)"
elif step == 4: rega_estrategia = "Seca de 40% (Dryback Severo) para estresse generativo"
elif step == 5: rega_estrategia = "Lavagem (Flush) com bastante escoamento"

# 3. LÓGICA DO DELTA TÉRMICO (DIF - Diferença de Temp. Dia/Noite)
# Essa é a nova inteligência que substitui o pH/EC
dif_alvo = "DIF Baixo (Queda de 2°C a 4°C)"
dif_motivo = "Mantém os internódios curtos e a planta compacta."
if step == 3: # Pré-Flora (Stretch)
    dif_alvo = "DIF Zero (Queda de 0°C a 2°C)"
    dif_motivo = "Trava o estirão vertical da planta."
elif step == 4: # Engorda
    dif_alvo = "DIF Médio (Queda de 4°C a 6°C)"
    dif_motivo = "Otimiza a respiração celular noturna."
elif step == 5: # Colheita/Maturação
    dif_alvo = "DIF Alto (Queda de 8°C a 12°C)"
    dif_motivo = "Simula outono: força resina e cores roxas."

# 4. HTML BLINDADO (FLEXBOX)
html_telemetria = f"""
<div style="background:#0a0a0a; border:1px solid #222; border-radius:12px; padding:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
<div style="color:#aaa; font-size:0.75rem; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">⏱️ CRONOGRAMA FENOLÓGICO: {info_genetica['tipo'].upper()}</div>
<div style="display:flex; align-items:center; justify-content:space-between; position:relative; margin-bottom:25px; padding:0 10px;">
<div style="position:absolute; top:15px; left:10%; right:10%; height:3px; background:#333; z-index:1;"></div>
<div style="position:absolute; top:15px; left:10%; width:{min(100, (step-1)*25)}%; height:3px; background:#a855f7; z-index:2; transition: width 0.5s;"></div>
<div style="display:flex; flex-direction:column; align-items:center; z-index:3; width:20%;">
<div style="width:30px; height:30px; border-radius:50%; background:{cor_step(1)}; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; border:3px solid #0a0a0a; box-shadow: 0 0 8px {cor_step(1)}80;">1</div>
<div style="font-size:0.65rem; color:{cor_texto(1)}; margin-top:5px; font-weight:bold; text-align:center;">RAÍZES</div>
</div>
<div style="display:flex; flex-direction:column; align-items:center; z-index:3; width:20%;">
<div style="width:30px; height:30px; border-radius:50%; background:{cor_step(2)}; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; border:3px solid #0a0a0a; box-shadow: 0 0 8px {cor_step(2)}80;">2</div>
<div style="font-size:0.65rem; color:{cor_texto(2)}; margin-top:5px; font-weight:bold; text-align:center;">VEGETATIVO</div>
</div>
<div style="display:flex; flex-direction:column; align-items:center; z-index:3; width:20%;">
<div style="width:30px; height:30px; border-radius:50%; background:{cor_step(3)}; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; border:3px solid #0a0a0a; box-shadow: 0 0 8px {cor_step(3)}80;">3</div>
<div style="font-size:0.65rem; color:{cor_texto(3)}; margin-top:5px; font-weight:bold; text-align:center;">PRÉ-FLORA</div>
</div>
<div style="display:flex; flex-direction:column; align-items:center; z-index:3; width:20%;">
<div style="width:30px; height:30px; border-radius:50%; background:{cor_step(4)}; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; border:3px solid #0a0a0a; box-shadow: 0 0 8px {cor_step(4)}80;">4</div>
<div style="font-size:0.65rem; color:{cor_texto(4)}; margin-top:5px; font-weight:bold; text-align:center;">ENGORDA</div>
</div>
<div style="display:flex; flex-direction:column; align-items:center; z-index:3; width:20%;">
<div style="width:30px; height:30px; border-radius:50%; background:{cor_step(5)}; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; border:3px solid #0a0a0a; box-shadow: 0 0 8px {cor_step(5)}80;">5</div>
<div style="font-size:0.65rem; color:{cor_texto(5)}; margin-top:5px; font-weight:bold; text-align:center;">COLHEITA</div>
</div>
</div>
<div style="display:grid; grid-template-columns: 1.2fr 1fr; gap:10px;">
<div style="background:rgba(59, 130, 246, 0.05); border:1px solid rgba(59, 130, 246, 0.2); padding:12px; border-radius:8px;">
<div style="display:flex; align-items:center; gap:5px; color:#60a5fa; font-size:0.75rem; font-weight:bold; margin-bottom:5px;">💧 MODO DE IRRIGAÇÃO</div>
<div style="color:#fff; font-size:0.85rem; line-height:1.4;">{rega_estrategia}</div>
<div style="font-size:0.65rem; color:#888; margin-top:5px; border-top:1px dashed #333; padding-top:3px;"><i>Baseado no estágio fenológico atual.</i></div>
</div>
<div style="background:rgba(249, 115, 22, 0.05); border:1px solid rgba(249, 115, 22, 0.2); padding:12px; border-radius:8px;">
<div style="display:flex; align-items:center; gap:5px; color:#fb923c; font-size:0.75rem; font-weight:bold; margin-bottom:5px;">🌡️ DELTA TÉRMICO (DIF)</div>
<div style="color:#fff; font-size:0.85rem; font-weight:bold; margin-bottom:2px;">{dif_alvo}</div>
<div style="font-size:0.7rem; color:#ccc; line-height:1.3;">{dif_motivo}</div>
</div>
</div>
</div>
<div style="height:20px;"></div>
"""
st.markdown(html_telemetria, unsafe_allow_html=True)

# ABAS INFERIORES
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor, tab_tools = st.tabs(["🧪 NUTRIÇÃO & ABSORÇÃO", "🚑 DOCTOR GROW", "🧮 LABORATÓRIO & TOOLS"])


# ==============================================================================
# ABA: DIAGNÓSTICO VISUAL MASTER (V25 - BANCO DE DADOS EXPANDIDO & CALCULADORA)
# ==============================================================================
with tab_nutri:
    
    # --- 1. CONFIGURAÇÃO & BANCO DE DADOS LOCAL (EXPANDIDO) ---
    is_organic = "Orgânico" in metodo_sel or "KNF" in metodo_sel
    tipo_cultivo_txt = "ORGÂNICO/SOLO VIVO" if is_organic else "MINERAL/HIDRO"
    
    # 1.1 DATABASE DE SINTOMAS (3x MAIOR QUE O ANTERIOR)
    # Agora inclui Micros, Excessos e Problemas Fisiológicos
    db_visual_master = {
        "MACRO NUTRIENTES": {
            "Nitrogênio (Carência)": {"cor": "#22c55e", "sintoma": "Folhas velhas (base) ficam amarelo pálido uniformemente. Planta para de crescer.", "elem": "N"},
            "Nitrogênio (Toxidez)":  {"cor": "#14532d", "sintoma": "Folhas verde-escuro quase preto. Pontas em 'garra' viradas para baixo.", "elem": "Flush"},
            "Fósforo (Carência)":    {"cor": "#3b82f6", "sintoma": "Manchas roxas/azuladas nas folhas. Caules vermelhos. Crescimento travado.", "elem": "P"},
            "Potássio (Carência)":   {"cor": "#a855f7", "sintoma": "Bordas das folhas queimadas (marrom) e enrolando para cima. Parece queimadura.", "elem": "K"},
            "Magnésio (Carência)":   {"cor": "#eab308", "sintoma": "Clorose intervenal (amarelo entre as veias, veias continuam verdes). Folhas médias.", "elem": "Mg"},
            "Cálcio (Carência)":     {"cor": "#f97316", "sintoma": "Manchas marrons/ferrugem (spots) no meio da folha. Folhas novas nascem deformadas.", "elem": "Ca"},
            "Enxofre (Carência)":    {"cor": "#facc15", "sintoma": "Parecido com Nitrogênio, mas começa nas folhas NOVAS (topo) ficando amarelas.", "elem": "S"},
        },
        "MICRO NUTRIENTES": {
            "Ferro (Carência)":      {"cor": "#a3e635", "sintoma": "Folhas novas nascem amarelo-limão brilhante. Veias ficam verdes no início.", "elem": "Fe"},
            "Zinco (Carência)":      {"cor": "#9ca3af", "sintoma": "Rosetting (topo amassado/compacto). Pontas das folhas queimadas (90 graus).", "elem": "Zn"},
            "Boro (Carência)":       {"cor": "#be123c", "sintoma": "Pontos de crescimento (meristemas) morrem ou ficam marrons. Caules ocos.", "elem": "B"},
            "Manganês (Carência)":   {"cor": "#0d9488", "sintoma": "Manchas necróticas (marrons) espalhadas entre as veias. Folhas jovens.", "elem": "Mn"},
            "Cobre (Carência)":      {"cor": "#b45309", "sintoma": "Folhas ficam escuras com tons azulados/metálicos e bordas viram para baixo.", "elem": "Cu"},
        },
        "AMBIENTE & REGA": {
            "Excesso de Rega":       {"cor": "#38bdf8", "sintoma": "Folhas pesadas, caídas e curvadas para baixo (Garrra de Água). Solo encharcado.", "elem": "Seca"},
            "Falta de Rega":         {"cor": "#d97706", "sintoma": "Folhas murchas e moles, parecem papel fino. Solo seco e separado do vaso.", "elem": "Agua"},
            "Light Burn (Luz)":      {"cor": "#ffffff", "sintoma": "Branqueamento (Bleaching) apenas no topo mais alto. Bud fica branco/albino.", "elem": "Luz"},
            "Wind Burn (Vento)":     {"cor": "#94a3b8", "sintoma": "Folhas em formato de 'garra' ou torcidas, parecem secas pelo vento constante.", "elem": "Vento"},
            "PH Flutuante":          {"cor": "#ec4899", "sintoma": "Manchas marrons irregulares, folhas retorcidas. Parece várias deficiências juntas.", "elem": "PH"}
        }
    }

    # 1.2 PROTOCOLOS DE TRATAMENTO (O CÉREBRO)
    protocolos = {
        "N": {"bio": ["Farinha de Sangue", "Fish Mix"], "quim": ["Ureia", "Nitrato de Cálcio"], "dose_s": 3.0, "dose_a": 0.8},
        "P": {"bio": ["Farinha de Osso", "Guano"], "quim": ["MAP", "MKP 0-52-34"], "dose_s": 4.0, "dose_a": 0.6},
        "K": {"bio": ["Cinzas", "Kelp Meal"], "quim": ["Sulfato de Potássio"], "dose_s": 5.0, "dose_a": 0.8},
        "Ca": {"bio": ["Calcário Ostras"], "quim": ["CalMag", "Nitrato de Cálcio"], "dose_s": 2.0, "dose_a": 1.0},
        "Mg": {"bio": ["Dolomita"], "quim": ["Sal Amargo (Epsom)"], "dose_s": 1.5, "dose_a": 1.0},
        "S": {"bio": ["Gesso Agrícola"], "quim": ["Sulfato de Magnésio"], "dose_s": 1.0, "dose_a": 0.5},
        "Fe": {"bio": ["Quelato de Ferro Nat.", "Algas"], "quim": ["Ferro EDTA"], "dose_s": 0.5, "dose_a": 0.2},
        "Zn": {"bio": ["Quelato Zinco", "Sementes"], "quim": ["Sulfato de Zinco"], "dose_s": 0.3, "dose_a": 0.1},
        "B":  {"bio": ["Ácido Bórico Nat."], "quim": ["Ácido Bórico"], "dose_s": 0.1, "dose_a": 0.05},
        "Mn": {"bio": ["Sulfato Manganês"], "quim": ["Sulfato Manganês"], "dose_s": 0.2, "dose_a": 0.1},
        "Cu": {"bio": ["Fungicida Cobre"], "quim": ["Sulfato de Cobre"], "dose_s": 0.1, "dose_a": 0.05},
        "Flush": {"bio": ["Água Pura", "Enzimas"], "quim": ["Flush Finish", "Água pH 6.0"], "dose_s": 0, "dose_a": 0, "txt": "Faça uma rega com 3x o volume do vaso para lavar o solo."},
        "Seca": {"bio": ["Ventilação"], "quim": ["Ventilação"], "dose_s": 0, "dose_a": 0, "txt": "Pare de regar por 3-5 dias. Aumente a circulação de ar no chão."},
        "Agua": {"bio": ["Água + Algas"], "quim": ["Água + Wetting Agent"], "dose_s": 0, "dose_a": 0, "txt": "Regue lentamente com borrifador para reidratar o solo compactado."},
        "Luz": {"bio": ["Afaste o LED"], "quim": ["Afaste o LED"], "dose_s": 0, "dose_a": 0, "txt": "Suba o painel 15-30cm imediatamente. Diminua a potência em 20%."},
        "Vento": {"bio": ["Reposicionar"], "quim": ["Reposicionar"], "dose_s": 0, "dose_a": 0, "txt": "Não aponte ventiladores direto para a planta. Use o vento rebatido na parede."},
        "PH": {"bio": ["Calcário/Vinagre"], "quim": ["PH Up/Down"], "dose_s": 0, "dose_a": 0, "txt": "Meça o runoff. Se < 5.5 use Calcário. Se > 7.5 use Enxofre/Turfa."}
    }

    # --- 2. RENDERIZAÇÃO DA INTERFACE ---
    st.markdown(f"#### 🩺 Central de Diagnóstico ({len(db_visual_master['MACRO NUTRIENTES']) + len(db_visual_master['MICRO NUTRIENTES']) + len(db_visual_master['AMBIENTE & REGA'])} Sintomas)")
    
    # Cria abas para organizar o banco de dados gigante
    tab_macro, tab_micro, tab_amb = st.tabs(["MACRO NUTRIENTES", "MICRO NUTRIENTES", "FISIOLÓGICO & AMBIENTE"])
    
    # Função Auxiliar de Renderização (Para não repetir código e EVITAR ERRO DE HTML)
    def render_cards(categoria_dict):
        cols = st.columns(3)
        idx = 0
        for k, v in categoria_dict.items():
            elem_key = v['elem']
            proto = protocolos.get(elem_key, {})
            
            # Cálculo de Dose
            receita = ""
            if "txt" in proto:
                receita = proto['txt'] # Instrução direta (ex: Flush)
            elif is_organic and vol_vaso != 999 and proto:
                total = proto['dose_s'] * vol_vaso
                receita = f"Aplicar <b>{total:.1f}g</b> no vaso de {vol_vaso}L."
            elif proto:
                receita = f"Diluir <b>{proto['dose_a']}g</b> por Litro d'água."
            
            # Produtos
            prods = proto.get('bio' if is_organic else 'quim', [])
            prods_html = ", ".join(prods) if prods else "Ajuste Ambiental"

            with cols[idx % 3]:
                # CARD SEGURO (HTML SEM INDENTAÇÃO)
                with st.expander(f"👁️ {k}"):
                    # Imagem Placeholder
                    
                    
                    html_card = f"""
<div style="border-left:3px solid {v['cor']}; padding-left:10px; margin-bottom:10px;">
<div style="font-size:0.85rem; color:#ccc; margin-bottom:5px;"><b>Sintoma:</b> {v['sintoma']}</div>
</div>
<div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:6px; border:1px solid #333;">
<div style="color:{v['cor']}; font-weight:bold; font-size:0.75rem; letter-spacing:1px; margin-bottom:5px;">SOLUÇÃO {tipo_cultivo_txt}</div>
<div style="font-size:0.85rem; margin-bottom:5px;"><b>🛠️ Usar:</b> {prods_html}</div>
<div style="background:{v['cor']}15; padding:6px; border-radius:4px; font-size:0.85rem; border:1px dashed {v['cor']}; color:#fff;">
<b>⚖️ DOSE:</b> {receita}
</div>
</div>
"""
                    st.markdown(html_card, unsafe_allow_html=True)
            idx += 1

    with tab_macro: render_cards(db_visual_master["MACRO NUTRIENTES"])
    with tab_micro: render_cards(db_visual_master["MICRO NUTRIENTES"])
    with tab_amb:   render_cards(db_visual_master["AMBIENTE & REGA"])

    st.markdown("---")
    
    # --- 3. GRÁFICO DE MARCHA DE ABSORÇÃO (MANTIDO ZOOM V22) ---
    st.markdown(f"#### 📊 Demanda Nutricional: Semana {semanas}")
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    
    macros_config = {
        "N":  {"nome": "Nitrogênio", "cor": "#22c55e", "val": nutri['N'][min(semanas-1,11)]},
        "P":  {"nome": "Fósforo",    "cor": "#3b82f6", "val": nutri['P'][min(semanas-1,11)]},
        "K":  {"nome": "Potássio",   "cor": "#a855f7", "val": nutri['K'][min(semanas-1,11)]},
        "Ca": {"nome": "Cálcio",     "cor": "#f97316", "val": nutri['Ca'][min(semanas-1,11)]},
        "Mg": {"nome": "Magnésio",   "cor": "#eab308", "val": nutri['Mg'][min(semanas-1,11)]},
        "S":  {"nome": "Enxofre",    "cor": "#facc15", "val": nutri['S'][min(semanas-1,11)]}
    }
    
    fig = go.Figure()
    for symbol, d in macros_config.items():
        opacity_list = [1.0 if x == semanas else 0.3 for x in nutri['semanas']]
        fig.add_trace(go.Bar(
            name=symbol, x=nutri['semanas'], y=nutri[symbol],
            marker_color=d['cor'], marker_opacity=opacity_list,
            text=nutri[symbol], textposition='auto'
        ))
    
    zoom_start = max(0.5, semanas - 2.5)
    zoom_end = min(12.5, semanas + 2.5)
    fig.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="#ccc"), height=400, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(tickmode='linear', tick0=1, dtick=1, showgrid=False, range=[zoom_start, zoom_end]),
        yaxis=dict(showgrid=True, gridcolor='#333', range=[0, 110])
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab_doctor:
    st.markdown("### 🚑 Doctor Grow")
    busca = st.text_input("🔍 Buscar Praga:", placeholder="Ex: Ácaros...")
    
    for nome, info in db["DOCTOR_GROW_FITOSSANIDADE"].items():
        if busca and busca.lower() not in nome.lower() and busca.lower() not in info['sintomas'].lower(): continue
        cor_g = "#ef4444" if info['gravidade'] in ["ALTA", "CRÍTICA", "FATAL"] else "#eab308"
        
        st.markdown(f"""
        <div class="doc-card" style="border-left-color: {cor_g};">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div style="font-weight:bold; color:#fff;">{nome}</div>
                <div style="color:{cor_g}; font-size:0.7rem; font-weight:bold;">{info['gravidade']}</div>
            </div>
            <div style="color:#ccc; font-size:0.9rem; margin-bottom:10px;"><i>{info['sintomas']}</i></div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div style="color:#4ade80; font-size:0.8rem;"><b>BIO:</b> {', '.join(info['bio'])}</div>
                <div style="color:#f87171; font-size:0.8rem;"><b>SOS:</b> {', '.join(info['quimico'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==============================================================================
# ABA: LABORATÓRIO & FERRAMENTAS (V34 - SUÍTE DE CÁLCULO MASTER)
# ==============================================================================
with tab_tools:
    
    # Cabeçalho da Seção
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="font-size:2rem;">🧮</div>
        <div>
            <div style="font-weight:900; font-size:1.5rem; color:#fff;">LABORATÓRIO SDI</div>
            <div style="color:#888; font-size:0.9rem;">FERRAMENTAS DE PRECISÃO PARA CULTIVADORES</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sub-abas para organizar as ferramentas
    t_clima, t_solo, t_custo, t_visual = st.tabs(["☁️ CLIMA & VPD", "🌍 SOLO & MIX", "⚡ ENERGIA (R$)", "📸 BENCHMARK"])

    # --- 1. CALCULADORA CLIMÁTICA (VPD + CO2) ---
    with t_clima:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("##### 🌫️ Calculadora de VPD (Real Time)")
            t_ar = st.number_input("Temperatura do Ar (°C):", 10.0, 45.0, 26.0, step=0.5)
            rh_ar = st.number_input("Umidade Relativa (%):", 10, 100, 60, step=1)
            offset = st.slider("Temp. da Folha (Offset):", -5.0, 2.0, -2.0, help="Diferença entre a temperatura do ar e da folha (Use termômetro infravermelho).")
            
            # Cálculo VPD
            svp = 0.61078 * 2.71828 ** ((17.27 * t_ar) / (t_ar + 237.3))
            avp = svp * (rh_ar / 100)
            t_folha = t_ar + offset
            svp_folha = 0.61078 * 2.71828 ** ((17.27 * t_folha) / (t_folha + 237.3))
            vpd = max(0.01, svp_folha - avp)
            
            # Diagnóstico VPD
            cor_vpd = "#ccc"; msg_vpd = "Neutro"
            if vpd < 0.4: cor_vpd = "#ef4444"; msg_vpd = "PERIGO: MOFO (Baixa Transpiração)"
            elif 0.4 <= vpd < 0.8: cor_vpd = "#4ade80"; msg_vpd = "FASE: CLONES / VEGA INICIAL"
            elif 0.8 <= vpd < 1.2: cor_vpd = "#22c55e"; msg_vpd = "FASE: VEGETATIVO / PRÉ-FLORA"
            elif 1.2 <= vpd < 1.6: cor_vpd = "#facc15"; msg_vpd = "FASE: FLORAÇÃO (Alta Demanda)"
            else: cor_vpd = "#ef4444"; msg_vpd = "PERIGO: ESTRESSE HÍDRICO (Seca)"

            st.markdown(f"""
            <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; text-align:center;">
                <div style="font-size:2.2rem; font-weight:900; color:{cor_vpd};">{vpd:.2f} kPa</div>
                <div style="font-size:0.8rem; font-weight:bold; color:{cor_vpd}; margin-top:5px;">{msg_vpd}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown("##### 💨 Calculadora de CO2 (PPM Alvo)")
            ppfd_input = st.number_input("PPFD Médio (umol/m²/s):", 100, 2000, 800, step=50, help="Medido no topo das plantas.")
            
            # Lógica simples de CO2: Até 700 PPFD, CO2 ambiente (400ppm) serve. Acima disso, precisa injetar.
            co2_alvo = 400
            if ppfd_input > 1000: co2_alvo = 1200 + ((ppfd_input - 1000) * 0.5)
            elif ppfd_input > 700: co2_alvo = 800 + ((ppfd_input - 700) * 1.3)
            
            cor_co2 = "#3b82f6" if co2_alvo > 500 else "#94a3b8"
            
            st.markdown(f"""
            <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; text-align:center; height:130px; display:flex; flex-direction:column; justify-content:center;">
                <div style="font-size:0.8rem; color:#aaa;">META DE CO2 SUGERIDA</div>
                <div style="font-size:2.2rem; font-weight:900; color:{cor_co2};">{co2_alvo:.0f} <span style="font-size:1rem;">PPM</span></div>
            </div>
            """, unsafe_allow_html=True)

    # --- 2. CALCULADORA DE SOLO (V34 NOVO) ---
    with t_solo:
        st.markdown("##### 🧪 Misturador de Substrato (Receita Clássica)")
        st.caption("Calcula a quantidade de insumos para preencher seus vasos.")
        
        c_s1, c_s2 = st.columns([1, 2])
        with c_s1:
            vasos_qtd = st.number_input("Quantidade de Vasos:", 1, 100, int(n_plantas))
            litragem = st.number_input("Tamanho do Vaso (L):", 1, 500, int(vol_vaso) if vol_vaso != 999 else 20)
            total_litros = vasos_qtd * litragem
        
        with c_s2:
            # Receita Padrão: 40% Turfa, 40% Perlita, 20% Húmus
            turfa = total_litros * 0.40
            perlita = total_litros * 0.40
            humus = total_litros * 0.20
            
            st.markdown(f"""
            <div style="background:#1c1917; border-radius:10px; padding:15px; border:1px solid #444;">
                <div style="font-weight:bold; color:#fff; margin-bottom:10px;">PARA PREENCHER {total_litros} LITROS TOTAIS:</div>
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #333; padding:5px 0;">
                    <span style="color:#a8a29e;">🟫 Turfa/Coco (40%):</span> <b style="color:#fff;">{turfa:.1f} L</b>
                </div>
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #333; padding:5px 0;">
                    <span style="color:#e5e5e5;">⬜ Perlita (40%):</span> <b style="color:#fff;">{perlita:.1f} L</b>
                </div>
                <div style="display:flex; justify-content:space-between; padding:5px 0;">
                    <span style="color:#57534e;">⬛ Húmus/Composto (20%):</span> <b style="color:#fff;">{humus:.1f} L</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 3. CALCULADORA DE CUSTO (V34) ---
    with t_custo:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            potencia_real = st.number_input("Watts Totais (LED + Equipamentos):", 0, 10000, int(watts_painel + 50))
            horas_uso = st.number_input("Horas Ligado/Dia:", 0, 24, int(horas_luz))
        with col_e2:
            preco_kwh = st.number_input("Preço do kWh (R$):", 0.1, 5.0, 0.92)
            dias_mes = 30
        
        # Cálculo
        kwh_mes = (potencia_real * horas_uso * dias_mes) / 1000
        reais_mes = kwh_mes * preco_kwh
        reais_ciclo = reais_mes * 4 # Estimativa 4 meses
        
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:15px;">
            <div style="background:rgba(234, 179, 8, 0.1); border:1px solid #ca8a04; padding:15px; border-radius:10px; text-align:center;">
                <div style="font-size:0.8rem; color:#eab308; font-weight:bold;">CUSTO MENSAL</div>
                <div style="font-size:1.5rem; color:#fff; font-weight:900;">R$ {reais_mes:.2f}</div>
            </div>
            <div style="background:rgba(255, 255, 255, 0.05); border:1px solid #333; padding:15px; border-radius:10px; text-align:center;">
                <div style="font-size:0.8rem; color:#888; font-weight:bold;">CUSTO CICLO (4 MÊS)</div>
                <div style="font-size:1.5rem; color:#fff; font-weight:900;">R$ {reais_ciclo:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 4. BENCHMARK VISUAL (CORRIGIDO SEM ERRO DE SINTAXE) ---
    with t_visual:
        st.markdown(f"##### 📸 Referência Visual: {fase_nome}")
        
        # Define características baseadas na fase (Sem Erro de Indentação)
        # Usamos CSS para simular o "Wireframe" da planta
        cor_planta = "#4ade80" # Verde Vegetativo
        if "Flora" in fase_nome: cor_planta = "#a855f7" # Roxo Flora
        if "Maturação" in fase_nome: cor_planta = "#f59e0b" # Laranja
        
        col_v1, col_v2 = st.columns([1, 2])
        
        with col_v1:
            # Placeholder Gráfico Seguro (Substituindo a imagem que dava erro)
            st.markdown(f"""
            <div style="width:100%; height:180px; background:#111; border:2px dashed {cor_planta}; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-direction:column;">
                <div style="font-size:3rem; margin-bottom:10px;">🌿</div>
                <div style="color:{cor_planta}; font-weight:bold; font-size:0.8rem;">VISUAL {fase_nome.upper()}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_v2:
            st.markdown(f"""
            <div style="background:#18181b; padding:15px; border-radius:10px; border-left:4px solid {cor_planta};">
                <div style="font-weight:bold; color:#fff; margin-bottom:8px;">CHECKLIST VISUAL:</div>
                <ul style="color:#ccc; font-size:0.9rem; margin-left:20px; line-height:1.6;">
                    <li><b>Vigor:</b> Planta deve estar com folhas "rezando" (apontando p/ luz).</li>
                    <li><b>Cor:</b> { "Verde escuro uniforme." if "Vega" in fase_nome else "Verde claro, pistilos brancos aparecendo." if "Flora" in fase_nome else "Folhas amarelando (Outono natural)." }</li>
                    <li><b>Caule:</b> Espesso e rígido. Se estiver fino, aumente o vento.</li>
                    <li><b>Problemas Comuns:</b> Verifique embaixo das folhas por ácaros.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
