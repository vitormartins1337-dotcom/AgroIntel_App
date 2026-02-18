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
# CARD CONSULTORIA: OPERAÇÕES TÁTICAS V35 (MANEJO, PODAS & KNF)
# ==============================================================================
if show_consultoria:
    titulo_card = f"OPERAÇÕES TÁTICAS: SEMANA {semanas}"
    cor_brand = "#a855f7" 
    
    # 1. CÉREBRO DE MANEJO AVANÇADO (O "MASTER GROWER")
    # Dicionário contendo: Manejo Físico, Insumos (KNF/Bio), Previsão Futura e Correção de Erros Passados
    manejos = {
        0: {
            "fase": "Enraizamento",
            "tecnica": "Nenhuma poda. Foco total em umidade (Domo).",
            "insumo": "🌱 <b>Bio:</b> Trichoderma e Micorrizas (No buraco de plantio).<br>🧪 <b>KNF:</b> LAB (Bactérias Ácido Láticas) diluído 1:1000.",
            "futuro": "Prepare-se para transplantar semana que vem.",
            "esqueceu": "Se não usou micorrizas, aplique via rega agora.",
            "icone": "🌱"
        },
        1: {
            "fase": "Vegetativo Inicial",
            "tecnica": "Vento Indireto (Fortalecer caule). Leve LST se for Auto.",
            "insumo": "🌿 <b>Bio:</b> Extrato de Algas (Ascophyllum nodosum).<br>🧪 <b>KNF:</b> FPJ (Suco Fermentado de Planta) - Brotos verdes.",
            "futuro": "Semana que vem faremos a Poda Top (Se for Fotoperíodo).",
            "esqueceu": "Caule fraco? Adicione Silício na rega urgente.",
            "icone": "🌿"
        },
        2: {
            "fase": "Estruturação",
            "tecnica": "✂️ <b>Poda Top/FIM:</b> Cortar o topo para dividir em 2 galhos principais.<br>🪢 <b>LST:</b> Começar a amarrar galhos laterais para abrir a planta.",
            "insumo": "💪 <b>Bio:</b> Bokashi (Cobertura de solo).<br>🧪 <b>KNF:</b> FAA (Aminoácido de Peixe) para explosão de nitrogênio.",
            "futuro": "Instalação de Rede (Scrog) ou Estacas.",
            "esqueceu": "Não podou ainda? Faça HOJE. Se esperar mais, vai atrasar a vega.",
            "icone": "✂️"
        },
        3: {
            "fase": "Pré-Flora / Stretch",
            "tecnica": "🕸️ <b>SCROG:</b> Passe os galhos pela rede. Preencha os quadrados.<br>🧹 <b>Limpeza:</b> Remova folhas grandes que tapam brotos novos.",
            "insumo": "🦴 <b>Bio:</b> CalMag e Ácidos Húmicos.<br>🧪 <b>KNF:</b> WCA (Cálcio Solúvel em Água) - Casca de ovo e vinagre.",
            "futuro": "A planta vai dobrar de tamanho. Suba as luzes.",
            "esqueceu": "<b>Perdeu o time da Poda Top?</b> NÃO corte mais. Use Supercropping (esmagar o caule) para controlar altura.",
            "icone": "🕸️"
        },
        4: {
            "fase": "Transição Floral",
            "tecnica": "🦵 <b>Canelas Nuas (Lollipopping):</b> Limpe os 30% inferiores da planta. Remova tudo que não recebe luz direta.",
            "insumo": "🌸 <b>Bio:</b> Melado de Cana (Carboidratos).<br>🧪 <b>KNF:</b> FFJ (Suco Fermentado de Fruta) - Banana/Manga.",
            "futuro": "Fim do crescimento vertical. Foco em engorda.",
            "esqueceu": "Não fez LST? A planta está muito alta? Dobre os galhos mais altos agressivamente (High Stress Training) antes que os buds formem.",
            "icone": "🦵"
        },
        5: {
            "fase": "Formação de Buds",
            "tecnica": "🛑 <b>PARAR PODAS:</b> Não estresse mais a planta. Apenas remova folhas que estejam fazendo sombra direta em buds principais (Defoliação Estratégica).",
            "insumo": "🔥 <b>Bio:</b> Guano de Morcego (Rico em Fósforo).<br>🧪 <b>KNF:</b> FFJ + WCA (Cálcio para estrutura floral).",
            "futuro": "Os buds vão começar a engordar e pedir Potássio.",
            "esqueceu": "Esqueceu o Lollipopping? Faça uma limpeza leve apenas nas folhas amarelas de baixo. Não tire folhas saudáveis agora.",
            "icone": "🛑"
        },
        6: {
            "fase": "Engorda (Bulking)",
            "tecnica": "🏋️ <b>Suporte:</b> Os galhos vão pesar. Use yoyos ou amarre os colas principais no teto para não quebrar.",
            "insumo": "💎 <b>Bio:</b> Chá de Banana ou Cinzas de Madeira.<br>🧪 <b>KNF:</b> WCAP (Cálcio-Fosfato) - Ossos queimados + Vinagre.",
            "futuro": "Monitorar Mofo (Botrytis) nos buds densos.",
            "esqueceu": "Buds pequenos? Aumente a intensidade da luz (DLI) e garanta que o VPD esteja alto (1.4+).",
            "icone": "🏋️"
        },
        7: {
            "fase": "Maturação",
            "tecnica": "❄️ <b>Estresse Térmico (Opcional):</b> Reduzir temperatura noturna para 18°C para estimular resina e cor roxa.",
            "insumo": "🍬 <b>Bio:</b> Finalizador (Terpenos) ou água de coco.<br>🧪 <b>KNF:</b> Apenas água ou LAB leve para limpar solo.",
            "futuro": "Prepare-se para o corte (Colheita).",
            "esqueceu": "Mofo no bud? CORTE o pedaço afetado imediatamente e coloque um saco plástico antes de tirar para não espalhar esporos.",
            "icone": "❄️"
        },
        8: {
            "fase": "Flush / Colheita",
            "tecnica": "✂️ <b>Manicure:</b> Comece a remover folhas grandes (Fan leaves) para facilitar a secagem pós-colheita.",
            "insumo": "🚿 <b>Flush:</b> Apenas Água pH 6.0. Sem cloro.",
            "futuro": "Secagem e Cura.",
            "esqueceu": "Não fez Flush? Se estiver no orgânico, tudo bem. Se for mineral, tente dar 2 dias de água pura pelo menos.",
            "icone": "🚿"
        }
    }
    
    # Seleção da semana (Trava na última se passar)
    idx_m = min(semanas, 8)
    dado_m = manejos.get(idx_m, manejos[8])

    # HTML BLINDADO (SEM INDENTAÇÃO INTERNA)
    html_consultoria = f"""
<div class="diag-card" style="border-left: 4px solid {cor_brand}; background: linear-gradient(170deg, #18181b 0%, #09090b 100%); padding:20px; border-radius:15px; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
<div style="display:flex; align-items:center; gap:10px;">
<div style="background:{cor_brand}; width:45px; height:45px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.5rem; box-shadow: 0 0 10px {cor_brand}40;">{dado_m['icone']}</div>
<div>
<div style="font-weight:900; color:{cor_brand}; font-size:1.1rem; letter-spacing:0.5px;">{titulo_card}</div>
<div style="font-size:0.75rem; color:#888;">PROTOCOLO: <b style="color:#fff;">{dado_m['fase'].upper()}</b></div>
</div>
</div>
</div>
<div style="display:grid; grid-template-columns: 1fr; gap:15px;">
<div style="background:rgba(255,255,255,0.03); border:1px solid #333; border-radius:10px; padding:15px; position:relative; overflow:hidden;">
<div style="position:absolute; top:0; left:0; width:4px; height:100%; background:#22c55e;"></div>
<div style="margin-left:10px;">
<div style="color:#22c55e; font-size:0.8rem; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">✂️ MANEJO FÍSICO (PODAS & TREINOS)</div>
<div style="color:#e4e4e7; font-size:0.95rem; line-height:1.4;">{dado_m['tecnica']}</div>
</div>
</div>
<div style="background:rgba(255,255,255,0.03); border:1px solid #333; border-radius:10px; padding:15px; position:relative; overflow:hidden;">
<div style="position:absolute; top:0; left:0; width:4px; height:100%; background:#3b82f6;"></div>
<div style="margin-left:10px;">
<div style="color:#3b82f6; font-size:0.8rem; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">🧪 BIO-INSUMOS & KNF (RECEITA)</div>
<div style="color:#ccc; font-size:0.9rem; line-height:1.4;">{dado_m['insumo']}</div>
</div>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
<div style="background:rgba(234, 179, 8, 0.05); border:1px solid rgba(234, 179, 8, 0.2); padding:10px; border-radius:8px;">
<div style="color:#facc15; font-size:0.7rem; font-weight:bold; margin-bottom:3px;">🔮 RADAR FUTURO</div>
<div style="color:#ddd; font-size:0.8rem; line-height:1.3;">{dado_m['futuro']}</div>
</div>
<div style="background:rgba(239, 68, 68, 0.05); border:1px solid rgba(239, 68, 68, 0.2); padding:10px; border-radius:8px;">
<div style="color:#f87171; font-size:0.7rem; font-weight:bold; margin-bottom:3px;">⚠️ ESQUECEU O ANTERIOR?</div>
<div style="color:#ddd; font-size:0.8rem; line-height:1.3;">{dado_m['esqueceu']}</div>
</div>
</div>
</div>
<div style="margin-top:15px; text-align:center; font-size:0.7rem; color:#555;">
<i>Sugestões baseadas no método {metodo_sel.split(' ')[0]} para plantas com {semanas} semanas.</i>
</div>
</div>
"""
    st.markdown(html_consultoria, unsafe_allow_html=True)

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
