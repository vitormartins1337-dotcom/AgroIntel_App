
# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V9.0 (MASTER AGRONOMY)
# DESCRIÇÃO: Banco de dados completo com Marcha de Absorção e Fitopatologia Avançada.

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS GENÉTICOS (NOMENCLATURA TÉCNICA PRECISA)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            "Indica Dominante (Fotoperíodo)": {
                "fator_yield": 1.0, 
                "ciclo_dias": 60, 
                "tipo": "Foto",
                "desc": "Arbustiva, internódios curtos, buds densos. Alta necessidade de Magnésio."
            },
            "Sativa Predominante (Fotoperíodo)": {
                "fator_yield": 1.3, 
                "ciclo_dias": 85, 
                "tipo": "Foto",
                "desc": "Alta, esguia, floração longa. Sensível a altos níveis de Nitrogênio na flora."
            },
            "Híbrida 50/50 (Fotoperíodo)": {
                "fator_yield": 1.15, 
                "ciclo_dias": 70, 
                "tipo": "Foto",
                "desc": "Vigor híbrido equilibrado. Adapta-se bem a podas e treinos."
            },
            "Indica Dominante (Automática)": {
                "fator_yield": 0.5, 
                "ciclo_dias": 70, 
                "tipo": "Auto",
                "desc": "Ciclo rápido. Raiz sensível (evitar transplantes)."
            },
            "Sativa Predominante (Automática)": {
                "fator_yield": 0.7, 
                "ciclo_dias": 90, 
                "tipo": "Auto",
                "desc": "Maior porte para uma automática. Requer mais luz (DLI alto)."
            },
            "Híbrida 50/50 (Automática)": {
                "fator_yield": 0.6, 
                "ciclo_dias": 80, 
                "tipo": "Auto",
                "desc": "Equilíbrio ideal entre tempo e produção."
            }
        },

        # ==============================================================================
        # 2. MÉTODOS DE CULTIVO (PARÂMETROS FÍSICO-QUÍMICOS)
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico (Solo Vivo)": {
                "descricao": "Ciclo do Nitrogênio natural. Foco em fungos/bactérias.",
                "rendimento_base": 55, "ph_ideal": "6.0-6.8", "ec_ideal": "Solo (Não medir Runoff)"
            },
            "Mineral (Inerte/Coco)": {
                "descricao": "Fertirrigação de alta frequência (Crop Steering).",
                "rendimento_base": 85, "ph_ideal": "5.8-6.2", "ec_ideal": "1.8-2.5 (Alta EC)"
            },
            "Orgânico-Mineral (Mix)": {
                "descricao": "Solo base com complementação mineral na engorda.",
                "rendimento_base": 70, "ph_ideal": "6.0-6.5", "ec_ideal": "1.2-1.8"
            },
            "Hidroponia (DWC/RDWC)": {
                "descricao": "Raízes em solução oxigenada. Absorção iônica imediata.",
                "rendimento_base": 110, "ph_ideal": "5.5-5.8", "ec_ideal": "1.2-2.0"
            }
        },

        # ==============================================================================
        # 3. MARCHA DE ABSORÇÃO (CURVAS MATEMÁTICAS DE DEMANDA %)
        # ==============================================================================
        "NUTRI_MARCHA_ABSORCAO": {
            "semanas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            # Nitrogênio: Alto na vega, cai drasticamente na flora
            "N": [90, 100, 100, 80, 60, 40, 30, 20, 10, 5, 0, 0], 
            # Fósforo: Baixo na vega, explode na pré-flora e flora média
            "P": [20, 30, 40, 60, 80, 100, 100, 90, 70, 40, 10, 0], 
            # Potássio: Crescente constante, pico na engorda (semana 6-8)
            "K": [30, 40, 50, 70, 85, 95, 100, 100, 95, 60, 20, 0], 
            # Cálcio: Necessidade constante para parede celular, pico no stretch
            "Ca": [40, 50, 70, 90, 100, 90, 80, 70, 50, 30, 10, 0], 
            # Magnésio: Segue o cálcio, essencial para clorofila
            "Mg": [40, 50, 60, 80, 90, 80, 70, 60, 40, 20, 10, 0],
            # Enxofre: Essencial para terpenos na flora
            "S": [20, 30, 40, 50, 60, 80, 90, 90, 80, 50, 20, 0]
        },

        # ==============================================================================
        # 4. ENCICLOPÉDIA DE DEFICIÊNCIAS (MACRO & MICRO)
        # ==============================================================================
        "DEFICIENCIAS_VISUAIS": {
            # --- MACRONUTRIENTES PRIMÁRIOS ---
            "Nitrogênio (N)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Amarelamento geral começando pelas folhas mais velhas (base). A planta 'canibaliza' as folhas de baixo.",
                "correcao_bio": "Sangue seco, Farinha de penas, Humus de minhoca, Chá de urtiga.",
                "correcao_quim": "Ureia, Nitrato de Amônio, Fertilizante 'Grow' base.",
                "gravidade": "BAIXA (Se corrigido rápido)",
                "cor_card": "#fbbf24" # Amarelo
            },
            "Fósforo (P)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Crescimento lento. Caules/pecíolos roxos. Folhas verde-azuladas escuras com manchas necróticas.",
                "correcao_bio": "Farinha de osso, Guano de morcego (rico em P), Rocha fosfática.",
                "correcao_quim": "Superfosfato, MAP, Fertilizante 'Bloom' base.",
                "gravidade": "MÉDIA (Afeta rendimento)",
                "cor_card": "#3b82f6" # Azul Escuro
            },
            "Potássio (K)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Queima das bordas das folhas (parece queimadura solar). Caules fracos. Flores pequenas.",
                "correcao_bio": "Cinzas de madeira, Kelp (Algas), Sulfato de Potássio orgânico.",
                "correcao_quim": "Nitrato de Potássio, PK Booster (13-14).",
                "gravidade": "ALTA (Afeta peso e qualidade)",
                "cor_card": "#ef4444" # Vermelho
            },
            
            # --- MACRONUTRIENTES SECUNDÁRIOS ---
            "Cálcio (Ca)": {
                "tipo": "Macro Secundário (Imóvel)",
                "sintoma": "Pontos marrons/ferrugem nas folhas novas e médias. Folhas novas nascem distorcidas ou em gancho.",
                "correcao_bio": "Farinha de ostras, Calcário dolomítico, Casca de ovo moída (lento).",
                "correcao_quim": "Nitrato de Cálcio, CalMag.",
                "gravidade": "ALTA (Trava a planta)",
                "cor_card": "#f97316" # Laranja
            },
            "Magnésio (Mg)": {
                "tipo": "Macro Secundário (Móvel)",
                "sintoma": "Clorose intervenal (nervuras ficam verdes, o meio fica amarelo). As bordas se curvam para cima ('rezando').",
                "correcao_bio": "Sal Amargo (Sulfato de Magnésio) foliar, Dolomita.",
                "correcao_quim": "Nitrato de Magnésio, CalMag.",
                "gravidade": "MÉDIA",
                "cor_card": "#eab308" # Amarelo Ouro
            },
            "Enxofre (S)": {
                "tipo": "Macro Secundário (Imóvel)",
                "sintoma": "Parecido com Nitrogênio (amarelo), mas começa nas folhas NOVAS (topo), não nas velhas.",
                "correcao_bio": "Gesso agrícola, Esterco bem curtido.",
                "correcao_quim": "Sulfato de Magnésio (Epsom) também fornece S.",
                "gravidade": "BAIXA",
                "cor_card": "#facc15" # Amarelo Claro
            },

            # --- MICRONUTRIENTES ---
            "Ferro (Fe)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Folhas novas nascem amarelo-limão brilhante, mas as nervuras permanecem verdes estritas.",
                "correcao_bio": "Quelatos naturais, Algas.",
                "correcao_quim": "Ferro Quelatado (EDTA/DTPA).",
                "gravidade": "MÉDIA (Geralmente pH incorreto)",
                "cor_card": "#a3e635" # Verde Lima
            },
            "Zinco (Zn)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Folhas novas com pontas queimadas e rotação 90º. 'Rosetting' (internódios muito curtos no topo).",
                "correcao_bio": "Kelp, Extrato de sementes.",
                "correcao_quim": "Sulfato de Zinco, Mix de Micro.",
                "gravidade": "BAIXA",
                "cor_card": "#9ca3af" # Cinza
            },
            "Boro (B)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Pontos de crescimento (meristemas) morrem ou ficam marrons. Caules ocos.",
                "correcao_bio": "Bórax (Cuidado, tóxico em excesso).",
                "correcao_quim": "Ácido bórico.",
                "gravidade": "RARA",
                "cor_card": "#9ca3af"
            }
        },

        # ==============================================================================
        # 5. FASES FENOLÓGICAS (DETALHAMENTO PROFISSIONAL)
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula (Seedling)": {
                "foco": "Estabelecimento Radicular",
                "obs": "Sistema radicular frágil. Manter VPD baixo (0.4-0.8 kPa). Evitar luz intensa direta.",
                "ameacas": ["Pythium (Damping-off)", "Fungus Gnats"],
                "clima_ideal": "Temp: 24-26°C | Umidade: 70-80%"
            },
            "Vegetativo Inicial": {
                "foco": "Desenvolvimento Foliar",
                "obs": "Início da demanda de Nitrogênio. Folhas de 3 a 5 pontas surgindo. Pode iniciar ventilação leve.",
                "ameacas": ["Tripes", "Mosca Branca"],
                "clima_ideal": "Temp: 22-28°C | Umidade: 60-70%"
            },
            "Vegetativo Tardio": {
                "foco": "Estrutura e Ramificação",
                "obs": "Planta robusta. Hora de podas (Top/Fim) e LST. Demanda máxima de Nitrogênio.",
                "ameacas": ["Spider Mites", "Deficiência de N"],
                "clima_ideal": "Temp: 22-28°C | Umidade: 55-65%"
            },
            "Pré-Flora (Stretch)": {
                "foco": "Transição Hormonal",
                "obs": "Alongamento do caule (2x a 3x). Sexagem visível. Alto consumo de Cálcio e Magnésio.",
                "ameacas": ["Hermafroditas", "Deficiência de Mg"],
                "clima_ideal": "Temp: 20-26°C | Umidade: 50-60%"
            },
            "Flora Inicial (Early Bloom)": {
                "foco": "Formação de Coroas",
                "obs": "Pistilos brancos abundantes ('Pompons'). Parar Nitrogênio, aumentar P e K.",
                "ameacas": ["Oídio", "Overfert"],
                "clima_ideal": "Temp: 20-26°C | Umidade: 45-55%"
            },
            "Flora Média (Bulking)": {
                "foco": "Engorda e Densidade",
                "obs": "Pico de produção de óleo. Buds inchando. Consumo máximo de Potássio e Fósforo.",
                "ameacas": ["Queima de luz", "Deficiência de K"],
                "clima_ideal": "Temp: 18-24°C | Umidade: 40-50%"
            },
            "Flora Final (Ripening)": {
                "foco": "Maturação e Senescência",
                "obs": "Pistilos marrons. Tricomas leitosos/âmbar. Iniciar Flush (lavagem) se usar mineral.",
                "ameacas": ["Botrytis (Mofo)", "Bananas (Stress)"],
                "clima_ideal": "Temp: 18-22°C | Umidade: 35-45%"
            }
        },

        # ==============================================================================
        # 6. FITOSSANIDADE (PRAGAS E DOENÇAS)
        # ==============================================================================
        "DOCTOR_GROW_FITOSSANIDADE": {
            "Spider Mites (Ácaros)": {
                "gravidade": "CRÍTICA",
                "sintomas": "Pontos brancos minúsculos na face superior (estippling). Teias finas nos buds em casos avançados.",
                "bio": ["Beauveria Bassiana", "Óleo de Neem (Apenas Veg)", "Predadores (Phytoseiulus)"],
                "quimico": ["Abamectina (Vertimec)", "Etoxazol"],
                "obs": "Reproduzem-se exponencialmente no calor e seca."
            },
            "Tripes": {
                "gravidade": "MÉDIA",
                "sintomas": "Manchas prateadas/bronzeadas que brilham. Insetos finos como agulhas na parte inferior.",
                "bio": ["Spinosad (Tracer)", "Sabão Potássico", "Armadilhas Azuis"],
                "quimico": ["Clorfenapir", "Acetamiprido"],
                "obs": "Vetores de vírus. Atacam folhas novas."
            },
            "Fungus Gnats": {
                "gravidade": "BAIXA/MÉDIA",
                "sintomas": "Mosquitos pretos voando no solo. Larvas transparentes comendo pelos radiculares.",
                "bio": ["BTI (Bacillus thuringiensis israelensis)", "Terra de Diatomáceas"],
                "quimico": ["Imidacloprido (Apenas Veg)"],
                "obs": "Sinal de excesso de rega (Solo muito úmido)."
            },
            "Oídio (Powdery Mildew)": {
                "gravidade": "ALTA",
                "sintomas": "Manchas de pó branco (parece farinha) sobre as folhas. Não sai passando o dedo facilmente.",
                "bio": ["Leite Cru 10% no Sol", "Bicarbonato de Potássio", "Bacillus subtilis"],
                "quimico": ["Difenoconazol", "Enxofre (Vaporizador)"],
                "obs": "Sistêmico. Requer baixa umidade e alta ventilação."
            },
            "Botrytis (Bud Rot)": {
                "gravidade": "FATAL",
                "sintomas": "Folha de açúcar seca repentinamente no meio do bud. Bud fica marrom/cinza e mole. Esporos voam.",
                "bio": ["Remoção cirúrgica com saco plástico", "Trichoderma (Prevenção)"],
                "quimico": ["NENHUM (Descarte a parte afetada)"],
                "obs": "Causado por umidade alta na floração (>50%) ou lagartas."
            },
            "Pythium (Root Rot)": {
                "gravidade": "ALTA",
                "sintomas": "Raízes marrons, gosmentas, cheiro de ovo podre/peixe. Planta murcha mesmo com água.",
                "bio": ["H2O2 (Peróxido de Hidrogênio)", "Enzimas", "Trichoderma"],
                "quimico": ["Metalaxil"],
                "obs": "Comum em hidroponia com reservatório quente (>22°C)."
            }
        }
    }
