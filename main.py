# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | TITANIUM EDITION V18.0 (MONSTER LOGIC)
# DESCRIÇÃO: Sistema Completo: Database Integrado, Volumetria HVAC, Consultoria Blindada.

import streamlit as st
import datetime
import plotly.graph_objects as go

# ==============================================================================
# 1. CORE ENGINE & DATABASE (BLOCO MONOLÍTICO INTEGRADO)
# ==============================================================================
# Incorporamos o banco de dados aqui para garantir que todas as novas informações
# (Russet Mites, Landraces, Volumetria) estejam disponíveis sem erros de importação.

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
# Aqui garantimos que todos os inputs fiquem na lateral para não poluir a tela.
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
# 4. SDI INTELLIGENCE CORE V18 (CÁLCULOS & LÓGICA)
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

# --- B. ENGENHARIA CLIMÁTICA & HVAC (V18 NOVO!) ---
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

# CÁLCULO DE ESTIMATIVA DE TÉRMINO
ciclo_total_dias = info_genetica.get('ciclo_dias', 90) + 30 # +30 de margem para vega
dias_restantes = max(0, ciclo_total_dias - dias_vida)

 with col_a:   
    # Cores dinâmicas para as metas
    meta_vpd = fase_dados.get('meta_vpd', '-')
    meta_ppfd = fase_dados.get('meta_ppfd', '-')
    regime_luz = fase_dados.get('luz_h', '-')
    
    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:15px;">
            <div>
                <div class="card-label" style="color:#a855f7;">FASE ATUAL ({info_genetica.get('tipo', 'Foto').upper()})</div>
                <div class="big-val" style="font-size:1.8rem;">{fase_nome.upper()}</div>
                <div style="background:#3b0764; color:#d8b4fe; padding:2px 8px; border-radius:4px; font-size:0.7rem; display:inline-block; font-weight:bold;">
                    💡 LUZ: {regime_luz}H
                </div>
            </div>
            <div style="text-align:right;">
                <div class="card-label">CRONOGRAMA</div>
                <div style="font-size:1.4rem; font-weight:bold; color:#fff;">{dias_vida} <span style="font-size:0.8rem; color:#888;">DIAS</span></div>
                <div style="font-size:0.75rem; color:#a855f7;">SEMANA {semanas}</div>
                <div style="font-size:0.7rem; color:#666; margin-top:2px;">Restam ~{dias_restantes} dias</div>
            </div>
        </div>

        <div style="height:1px; background:#333; margin:10px 0;"></div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px;">
            <div>
                <div class="card-label" style="margin-bottom:8px;">ALVOS DE REGA</div>
                <div style="display:flex; gap:5px; flex-wrap:wrap;">
                    <span class="meta-badge bg-ph" title="pH Ideal">💧 PH {info_metodo['ph_ideal']}</span>
                    <span class="meta-badge bg-ec" title="Eletrocondutividade">⚡ EC {info_metodo['ec_ideal']}</span>
                </div>
            </div>
            <div>
                <div class="card-label" style="margin-bottom:8px;">ALVOS DE CLIMA</div>
                <div style="display:flex; gap:5px; flex-wrap:wrap;">
                    <span class="meta-badge" style="background:rgba(234, 179, 8, 0.15); color:#facc15; border:1px solid #854d0e;">
                        ☀️ {meta_ppfd} PPFD
                    </span>
                    <span class="meta-badge" style="background:rgba(236, 72, 153, 0.15); color:#f472b6; border:1px solid #831843;">
                        🌫️ VPD {meta_vpd}
                    </span>
                </div>
            </div>
        </div>
        
        <div style="margin-top:15px; background:rgba(255,255,255,0.05); padding:8px; border-radius:6px; display:flex; align-items:center; gap:10px;">
            <div style="font-size:1.2rem;">🎯</div>
            <div style="line-height:1.2;">
                <div class="card-label" style="margin:0; color:#aaa;">FOCO ESTRATÉGICO</div>
                <div style="color:#fff; font-size:0.85rem; font-weight:600;">{fase_dados.get('foco', '-')}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="yield-card">
        <div class="card-label" style="color:#fcd34d;">ESTIMATIVA DE COLHEITA</div><div class="big-val" style="color:#fef08a;">{yield_total:.0f}g</div><div class="sub-info" style="color:#fde047;">~ {yield_kg:.2f} kg (Seco)</div>
        <div style="height:1px; background:#422006; margin:15px 0;"></div>
        <div style="font-size:0.75rem; color:#ca8a04;">BASE: <b>{n_plantas} plantas</b> ({info_genetica['tipo']})</div>
    </div>""", unsafe_allow_html=True)

# CARD DE CONSULTORIA V18 (HTML BLINDADO - SEM INDENTAÇÃO INTERNA)
if show_consultoria:
    titulo_card = f"CONSULTORIA: {ambiente_sel.split('(')[0].upper()}"
    
    html_content = f"""
<div class="diag-card" style="border-left: 4px solid {cor_card};">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
<div style="font-weight:900; color:{cor_card}; letter-spacing:1px; font-size:1.2rem;">{titulo_card}</div>
<div style="background:{cor_card}20; color:{cor_card}; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">SDI TITANIUM V18</div>
</div>
<div style="font-family:sans-serif; color:#e4e4e7;">
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">1. Fotônica & Climatologia</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_luz_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_luz_desc}</div>
<div style="font-size:0.85rem; color:#888; margin-top:4px; font-style:italic;">{txt_clima_desc}</div>
</div>
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">2. Ocupação Física</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_espaco_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_espaco_desc}</div>
</div>
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">3. Raízes & Substrato</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_raiz_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_raiz_desc}</div>
</div>
<div style="margin-top:25px; padding:15px; background:linear-gradient(90deg, {cor_card}15 0%, rgba(0,0,0,0) 100%); border-radius:8px; border-left:4px solid {cor_card};">
<span style="color:{cor_card}; font-weight:bold; font-size:0.9rem;">PLANO DE AÇÃO:</span><br>
<span style="color:#fff; font-size:1rem; line-height:1.6; display:block; margin-top:6px;">
{recomendacao_premium if recomendacao_premium else "Seu ecossistema está produtivo. Mantenha o VPD na faixa de 1.0 kPa."}
</span>
</div>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

# ABAS INFERIORES
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor = st.tabs(["🧪 NUTRIÇÃO & ABSORÇÃO", "🚑 DOCTOR GROW"])

with tab_nutri:
    st.markdown("#### 🔍 Diagnóstico Visual")
    cols_def = st.columns(4)
    defs_items = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (k, v) in enumerate(defs_items):
        with cols_def[i % 4]:
            cor_c = v.get('cor_card', '#333')
            # Imagem de placeholder contextual
            
            with st.expander(f"👁️ {k}"):
                st.markdown(f"""
                <div style="border-left: 3px solid {cor_c}; padding-left: 10px;">
                    <div style="font-size: 0.85rem; color: #eee; margin-bottom: 10px;">{v['sintoma']}</div>
                    <div style="background: rgba(34, 197, 94, 0.1); padding: 5px; margin-bottom: 5px;">BIO: {v.get('correcao_bio', '-')}</div>
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 5px;">MINERAL: {v.get('correcao_quim', '-')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"#### 📊 Marcha de Absorção (Semana {semanas})")
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    s_idx = min(semanas - 1, 11) if semanas > 0 else 0
    
    macros_config = {
        "N":  {"nome": "Nitrogênio", "cor": "#22c55e", "val": nutri['N'][s_idx]},
        "P":  {"nome": "Fósforo",    "cor": "#3b82f6", "val": nutri['P'][s_idx]},
        "K":  {"nome": "Potássio",   "cor": "#a855f7", "val": nutri['K'][s_idx]},
        "Ca": {"nome": "Cálcio",     "cor": "#f97316", "val": nutri['Ca'][s_idx]},
        "Mg": {"nome": "Magnésio",   "cor": "#eab308", "val": nutri['Mg'][s_idx]},
        "S":  {"nome": "Enxofre",    "cor": "#facc15", "val": nutri['S'][s_idx]}
    }
    
    fig = go.Figure()
    for symbol, d in macros_config.items():
        fig.add_trace(go.Bar(
            name=symbol, x=nutri['semanas'], y=nutri[symbol],
            marker_color=d['cor'], opacity=0.9, text=symbol, textposition='inside'
        ))
    fig.add_vline(x=semanas, line_width=4, line_color="rgba(255,255,255,0.5)")
    fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#ccc"), height=500, showlegend=False)
    
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
