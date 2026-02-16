# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V7.0 (NUTRIÇÃO PRECISION)

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS GENÉTICOS & MÉTODOS (MANTIDOS)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            "Indica Dominante": {"fator_yield": 1.0, "ciclo_dias": 60, "desc": "Arbustiva, compacta."},
            "Sativa Dominante": {"fator_yield": 1.2, "ciclo_dias": 80, "desc": "Alta, esguia, flora longa."},
            "Híbrida 50/50": {"fator_yield": 1.1, "ciclo_dias": 70, "desc": "Vigor híbrido equilibrado."},
            "Automática": {"fator_yield": 0.6, "ciclo_dias": 75, "desc": "Ciclo rápido, não fotoperiódica."}
        },
        "METODOS_CULTIVO": {
            "Orgânico Vivo": {"descricao": "Foco em terpenos.", "rendimento_base": 55, "cor_tema": "#22c55e", "ph_ideal": "6.2-6.8", "ec_ideal": "Solo"},
            "Mineral Inerte": {"descricao": "Alta performance.", "rendimento_base": 85, "cor_tema": "#38bdf8", "ph_ideal": "5.8-6.2", "ec_ideal": "1.8-2.2"},
            "Hidroponia": {"descricao": "Velocidade máxima.", "rendimento_base": 110, "cor_tema": "#a855f7", "ph_ideal": "5.5-5.8", "ec_ideal": "1.2-1.8"},
            "Outdoor Sol": {"descricao": "Plantas gigantes.", "rendimento_base": 150, "cor_tema": "#facc15", "ph_ideal": "6.0-7.0", "ec_ideal": "Solo"}
        },
        "FASES_DINAMICAS": {
            "Plântula": {"foco": "Enraizamento", "obs": "Umidade 70%+. Luz fraca.", "ameacas": ["Pythium", "Fungus Gnats"]},
            "Vegetativo": {"foco": "Folhagem", "obs": "Nitrogênio alto. Vento forte.", "ameacas": ["Tripes", "Spider Mites"]},
            "Pré-Flora": {"foco": "Stretch", "obs": "Rede SCROG. Aumentar CalMag.", "ameacas": ["Hermafroditas"]},
            "Flora Inicial": {"foco": "Botões", "obs": "PK Booster. Umidade 50%.", "ameacas": ["Oídio"]},
            "Flora Final": {"foco": "Engorda", "obs": "Flush. Umidade <45%.", "ameacas": ["Botrytis", "Bananas"]}
        },

        # ==============================================================================
        # 2. NUTRIÇÃO PRECISION (NOVO: DADOS PARA GRÁFICOS)
        # ==============================================================================
        "NUTRI_MARCHA_ABSORCAO": {
            # Semanas do ciclo padrão (1-12)
            "semanas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            # Demanda relativa (0-100%)
            "N": [30, 60, 90, 100, 80, 60, 50, 40, 30, 20, 10, 0], # Nitrogênio cai na flora
            "P": [10, 20, 30, 40, 60, 80, 100, 90, 80, 60, 20, 0], # Fósforo explode na flora
            "K": [20, 30, 50, 70, 80, 95, 100, 100, 90, 60, 10, 0], # Potássio alto na flora
            "Ca": [20, 40, 60, 70, 80, 80, 80, 70, 60, 40, 20, 0], # Cálcio constante
            "Mg": [20, 30, 50, 60, 70, 70, 60, 50, 40, 30, 10, 0]  # Magnésio segue o Cálcio
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
        # 3. DOCTOR GROW (APENAS PRAGAS E DOENÇAS AGORA)
        # ==============================================================================
        "DOCTOR_GROW_FITOSSANIDADE": {
            "Pythium": {
                "tipo": "Doença de Raiz",
                "gravidade": "ALTA",
                "sintomas": "Raízes marrons, gosmentas, cheiro de podre. Planta murcha mesmo regada.",
                "bio": ["H2O2 (Peróxido)", "Trichoderma harzianum"],
                "quimico": ["Metalaxil (Ridomil)"],
                "obs": "Comum em hidroponia ou solo encharcado > 22°C."
            },
            "Fungus Gnats": {
                "tipo": "Praga de Solo",
                "gravidade": "MÉDIA",
                "sintomas": "Mosquitinhos pretos voando. Larvas transparentes na raiz.",
                "bio": ["BTI (Dipel/Dimy)", "Terra de Diatomáceas", "Armadilha Amarela"],
                "quimico": ["Imidacloprido (Veg apenas)"],
                "obs": "Deixe o solo secar bem entre as regas."
            },
            "Tripes": {
                "tipo": "Praga de Folha",
                "gravidade": "MÉDIA",
                "sintomas": "Manchas prateadas/bronzeadas. Inseto palito rápido.",
                "bio": ["Spinosad (Tracer)", "Sabão Potássico", "Armadilha Azul"],
                "quimico": ["Clorfenapir", "Acetamiprido"],
                "obs": "Ataca na fase vegetativa e transmite viroses."
            },
            "Spider Mites": {
                "tipo": "Praga Crítica",
                "gravidade": "CRÍTICA",
                "sintomas": "Pontos brancos picados (estippling). Teias nos buds.",
                "bio": ["Beauveria Bassiana", "Óleo de Neem (Veg)", "Ácaro Predador"],
                "quimico": ["Abamectina", "Etoxazol"],
                "obs": "Reproduz rápido no calor seco. Aumente a umidade."
            },
            "Oídio": {
                "tipo": "Fungo Foliar",
                "gravidade": "ALTA",
                "sintomas": "Pó branco (parece farinha) sobre as folhas.",
                "bio": ["Leite Cru 10% (Sol)", "Bicarbonato de Potássio"],
                "quimico": ["Difenoconazol", "Enxofre (Vapor)"],
                "obs": "Melhore a ventilação interna da planta."
            },
            "Botrytis": {
                "tipo": "Fungo de Flor",
                "gravidade": "FATAL",
                "sintomas": "Bud podre, marrom/cinza, desmancha ao tocar.",
                "bio": ["Remoção Cirúrgica", "Trichoderma (Preventivo)"],
                "quimico": ["PROIBIDO EM FLORES"],
                "obs": "Umidade alta na flora final é a causa."
            }
        }
    }
