# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V8.0 (FINAL)

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS GENÉTICOS (ATUALIZADO: FOTO vs AUTO)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            "Indica Predom. (Fotoperíodo)": {
                "fator_yield": 1.0, 
                "ciclo_dias": 60, # Apenas dias de flora
                "tipo": "Foto",
                "desc": "Arbustiva, compacta, ciclo controlado por 12/12."
            },
            "Sativa Predom. (Fotoperíodo)": {
                "fator_yield": 1.3, 
                "ciclo_dias": 85, 
                "tipo": "Foto",
                "desc": "Alta, esguia, floração longa, maior rendimento."
            },
            "Híbrida 50/50 (Fotoperíodo)": {
                "fator_yield": 1.15, 
                "ciclo_dias": 70, 
                "tipo": "Foto",
                "desc": "Vigor híbrido equilibrado."
            },
            "Indica Predom. (Automática)": {
                "fator_yield": 0.5, 
                "ciclo_dias": 70, # Ciclo total
                "tipo": "Auto",
                "desc": "Rápida, compacta, floresce por idade."
            },
            "Sativa Predom. (Automática)": {
                "fator_yield": 0.7, 
                "ciclo_dias": 90, # Ciclo total
                "tipo": "Auto",
                "desc": "Maior porte que a indica auto."
            },
            "Híbrida 50/50 (Automática)": {
                "fator_yield": 0.6, 
                "ciclo_dias": 80, # Ciclo total
                "tipo": "Auto",
                "desc": "Equilíbrio ideal para ciclos rápidos."
            }
        },

        # ==============================================================================
        # 2. MÉTODOS DE CULTIVO (NOVAS CATEGORIAS)
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico": {
                "descricao": "Solo vivo. Foco total em qualidade e terpenos.",
                "rendimento_base": 50,
                "cor_tema": "#22c55e",
                "ph_ideal": "6.0 - 6.8",
                "ec_ideal": "Solo"
            },
            "Mineral Inerte": {
                "descricao": "Coco ou Turfa. Alta precisão e controle.",
                "rendimento_base": 85,
                "cor_tema": "#38bdf8",
                "ph_ideal": "5.8 - 6.2",
                "ec_ideal": "1.8 - 2.5"
            },
            "Orgânico Mineral": {
                "descricao": "Mix de solo com complementação mineral pontual.",
                "rendimento_base": 70,
                "cor_tema": "#eab308",
                "ph_ideal": "6.0 - 6.5",
                "ec_ideal": "1.2 - 1.8"
            },
            "Hidropônico": {
                "descricao": "DWC/RDWC. Máxima velocidade e rendimento.",
                "rendimento_base": 110,
                "cor_tema": "#a855f7",
                "ph_ideal": "5.5 - 5.8",
                "ec_ideal": "1.2 - 2.0"
            }
        },

        # ==============================================================================
        # 3. NUTRIÇÃO PRECISION (MARCHA DE ABSORÇÃO)
        # ==============================================================================
        "NUTRI_MARCHA_ABSORCAO": {
            "semanas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            # Demanda relativa (0-100%)
            "N": [30, 60, 90, 100, 80, 60, 50, 40, 30, 20, 10, 0], 
            "P": [10, 20, 30, 40, 60, 80, 100, 90, 80, 60, 20, 0], 
            "K": [20, 30, 50, 70, 80, 95, 100, 100, 90, 60, 10, 0], 
            "Ca": [20, 40, 60, 70, 80, 80, 80, 70, 60, 40, 20, 0], 
            "Mg": [20, 30, 50, 60, 70, 70, 60, 50, 40, 30, 10, 0]  
        },
        "DEFICIENCIAS_VISUAIS": {
            "Nitrogênio (N)": {
                "sintoma": "Amarelamento uniforme das folhas velhas (baixeiro).",
                "correcao": "Aumentar Grow/Base ou adicionar Humus/Ureia.",
                "fase_comum": "Vegetativo Tardio / Stretch"
            },
            "Magnésio (Mg)": {
                "sintoma": "Clorose intervenal (nervuras verdes, meio amarelo). Folhas 'rezando'.",
                "correcao": "Sal Amargo (Foliar) ou CalMag (Raiz).",
                "fase_comum": "Pré-Flora (Semana 3-4 Flora)"
            },
            "Cálcio (Ca)": {
                "sintoma": "Pontos de ferrugem marrom e crescimento lento.",
                "correcao": "CalMag ou Nitrato de Cálcio via raiz (Ca é imóvel).",
                "fase_comum": "Pico de crescimento / Stretch"
            },
            "Potássio (K)": {
                "sintoma": "Bordas das folhas queimadas/marrons. Caule fraco.",
                "correcao": "PK Booster ou Cinzas (Orgânico).",
                "fase_comum": "Flora Avançada"
            }
        },

        # ==============================================================================
        # 4. FASES E DOCTOR GROW (FITOSSANIDADE)
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula": {"foco": "Enraizamento", "obs": "Umidade 70%+. Luz fraca.", "ameacas": ["Pythium", "Fungus Gnats"]},
            "Vegetativo": {"foco": "Folhagem", "obs": "Nitrogênio alto. Vento forte.", "ameacas": ["Tripes", "Spider Mites"]},
            "Pré-Flora": {"foco": "Stretch", "obs": "Rede SCROG. Aumentar CalMag.", "ameacas": ["Hermafroditas"]},
            "Flora Inicial": {"foco": "Botões", "obs": "PK Booster. Umidade 50%.", "ameacas": ["Oídio"]},
            "Flora Final": {"foco": "Engorda", "obs": "Flush. Umidade <45%.", "ameacas": ["Botrytis", "Bananas"]}
        },
        "DOCTOR_GROW_FITOSSANIDADE": {
            "Pythium": {
                "tipo": "Doença de Raiz", "gravidade": "ALTA",
                "sintomas": "Raízes marrons, gosmentas, cheiro de podre. Planta murcha.",
                "bio": ["H2O2 (Peróxido)", "Trichoderma harzianum"], "quimico": ["Metalaxil (Ridomil)"],
                "obs": "Comum em hidroponia ou solo encharcado > 22°C."
            },
            "Fungus Gnats": {
                "tipo": "Praga de Solo", "gravidade": "MÉDIA",
                "sintomas": "Mosquitinhos pretos voando. Larvas transparentes na raiz.",
                "bio": ["BTI (Dipel)", "Terra de Diatomáceas"], "quimico": ["Imidacloprido (Veg apenas)"],
                "obs": "Deixe o solo secar bem entre as regas."
            },
            "Tripes": {
                "tipo": "Praga de Folha", "gravidade": "MÉDIA",
                "sintomas": "Manchas prateadas. Inseto palito rápido.",
                "bio": ["Spinosad (Tracer)", "Sabão Potássico"], "quimico": ["Clorfenapir", "Acetamiprido"],
                "obs": "Ataca na fase vegetativa e transmite viroses."
            },
            "Spider Mites": {
                "tipo": "Praga Crítica", "gravidade": "CRÍTICA",
                "sintomas": "Pontos brancos picados. Teias nos buds.",
                "bio": ["Beauveria Bassiana", "Óleo de Neem (Veg)"], "quimico": ["Abamectina", "Etoxazol"],
                "obs": "Reproduz rápido no calor seco."
            },
            "Oídio": {
                "tipo": "Fungo Foliar", "gravidade": "ALTA",
                "sintomas": "Pó branco sobre as folhas.",
                "bio": ["Leite Cru 10%", "Bicarbonato"], "quimico": ["Difenoconazol", "Enxofre"],
                "obs": "Melhore a ventilação interna."
            },
            "Botrytis": {
                "tipo": "Fungo de Flor", "gravidade": "FATAL",
                "sintomas": "Bud podre, marrom/cinza, desmancha ao tocar.",
                "bio": ["Remoção Cirúrgica"], "quimico": ["PROIBIDO EM FLORES"],
                "obs": "Umidade alta na flora final é a causa."
            }
        }
    }
