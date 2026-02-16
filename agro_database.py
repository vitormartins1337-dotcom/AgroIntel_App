# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V5.0 (INTEGRAÇÃO TOTAL)

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS DE GENÉTICA & PRODUTIVIDADE (NOVO)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            "Indica (Fotoperíodo)": {
                "fator_yield": 1.0, # Padrão
                "ciclo_total_dias": 100,
                "desc": "Arbustiva, densa, ciclo rápido.",
                "risco_fase": "Botrytis (Mofo) na Flora Final devido à densidade."
            },
            "Sativa (Fotoperíodo)": {
                "fator_yield": 1.2, # Rende mais, mas demora mais
                "ciclo_total_dias": 120,
                "desc": "Alta, esguia, flores aeradas.",
                "risco_fase": "Queima por luz (cresce muito) e Hermafroditismo."
            },
            "Híbrida (50/50)": {
                "fator_yield": 1.1,
                "ciclo_total_dias": 110,
                "desc": "Vigor híbrido, equilíbrio ideal.",
                "risco_fase": "Variável conforme fenótipo."
            },
            "Automática (Ruderalis)": {
                "fator_yield": 0.6, # Menor rendimento por planta
                "ciclo_total_dias": 75,
                "desc": "Ciclo curtíssimo, floresce por idade.",
                "risco_fase": "Travamento no veg (estresse reduz colheita drasticamente)."
            }
        },

        # ==============================================================================
        # 2. METODOLOGIAS (COM ESTIMATIVA DE RENDIMENTO BASE)
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico (Solo Vivo)": {
                "descricao": "Qualidade máxima de terpenos. Rendimento médio.",
                "rendimento_base_g_planta": 60, # g secas por planta (média conservadora)
                "cor_tema": "#22c55e",
                "ph_ideal": "6.2-6.8",
                "ec_ideal": "Solo"
            },
            "Mineral (Coco/Inerte)": {
                "descricao": "Alta performance. Rendimento alto.",
                "rendimento_base_g_planta": 85,
                "cor_tema": "#38bdf8",
                "ph_ideal": "5.8-6.0",
                "ec_ideal": "1.8-2.2"
            },
            "Hidroponia (DWC)": {
                "descricao": "Crescimento explosivo. Rendimento máximo.",
                "rendimento_base_g_planta": 110,
                "cor_tema": "#a855f7",
                "ph_ideal": "5.5-5.8",
                "ec_ideal": "1.2-1.8"
            },
            "Outdoor (Sol)": {
                "descricao": "Plantas gigantes se plantadas na época certa.",
                "rendimento_base_g_planta": 150, # Pode ser muito mais, mas média Brasil
                "cor_tema": "#facc15",
                "ph_ideal": "6.0-6.5",
                "ec_ideal": "Solo"
            }
        },

        # ==============================================================================
        # 3. FASES DINÂMICAS (COM AMEAÇAS VINCULADAS AO DOCTOR GROW)
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula (Semana 1-2)": {
                "foco": "Enraizamento",
                "obs": "Umidade 70%+. Luz fraca. Não adubar.",
                "ameacas_chave": ["Pythium (Root Rot)", "Fungus Gnats"]
            },
            "Vegetativo (Semana 3-6)": {
                "foco": "Estrutura/Poda",
                "obs": "Topping/LST. Nitrogênio alto. Vento forte.",
                "ameacas_chave": ["Tripes", "Spider Mites", "Deficiência N"]
            },
            "Pré-Flora (Semana 7-8)": {
                "foco": "Stretch/Sexagem",
                "obs": "Instalar rede SCROG. Remover machos.",
                "ameacas_chave": ["Deficiência Mg", "Deficiência Ca"]
            },
            "Flora Inicial (Semana 9-11)": {
                "foco": "Formação de Botões",
                "obs": "PK Booster. Baixar umidade para 50%.",
                "ameacas_chave": ["Oídio", "Overfert"]
            },
            "Flora Final (Semana 12+)": {
                "foco": "Densidade/Resina",
                "obs": "Flush (Lavagem). Umidade <45%. Escuridão 48h antes da faca.",
                "ameacas_chave": ["Botrytis (Bud Rot)", "Bananas"]
            }
        },

        # ==============================================================================
        # 4. DOCTOR GROW (DATABASE DE SOLUÇÕES)
        # ==============================================================================
        "DOCTOR_GROW_MASTER": {
            "Pythium (Root Rot)": {
                "tipo": "Doença",
                "identificacao": "Raízes marrons gosmentas, cheiro de podre. Planta murcha.",
                "controle": "H2O2 (Peróxido) na rega. Enzimas (Cannazym). Manter água fria (<21°C).",
                "produtos": ["Peróxido 10 vol", "Trichoderma", "Metalaxil (Químico)"]
            },
            "Fungus Gnats": {
                "tipo": "Praga",
                "identificacao": "Mosquitinhos pretos voando. Larvas na raiz.",
                "controle": "Deixar solo secar. BTI na rega. Armadilhas amarelas.",
                "produtos": ["Dipel (BTI)", "Terra Diatomácea", "Dimy Pel"]
            },
            "Tripes": {
                "tipo": "Praga",
                "identificacao": "Folhas prateadas/brilhantes. Inseto palito.",
                "controle": "Spinosad é o rei. Sabão potássico ajuda.",
                "produtos": ["Tracer (Spinosad)", "Óleo de Neem (Só Veg)", "Mospilan (Químico)"]
            },
            "Spider Mites": {
                "tipo": "Praga",
                "identificacao": "Pontos brancos na folha. Teias.",
                "controle": "Alta umidade freia eles. Abamectina no veg.",
                "produtos": ["Vertimec", "Beauveria Bassiana", "Enxofre"]
            },
            "Deficiência N": {
                "tipo": "Nutrição",
                "identificacao": "Folhas velhas amarelam por inteiro.",
                "controle": "Aumentar Nitrogênio na rega.",
                "produtos": ["Flowermind", "Ureia", "Humus"]
            },
            "Deficiência Mg": {
                "tipo": "Nutrição",
                "identificacao": "Amarelo entre as nervuras (esqueleto verde).",
                "controle": "Sal Amargo foliar ou CalMag.",
                "produtos": ["Sulfato de Magnésio", "CalMag"]
            },
            "Deficiência Ca": {
                "tipo": "Nutrição",
                "identificacao": "Pontos de ferrugem marrom nas folhas.",
                "controle": "Cálcio é imóvel. Aplicar CalMag na raiz.",
                "produtos": ["Nitrato de Cálcio", "Farinha de Ostras"]
            },
            "Oídio": {
                "tipo": "Fungo",
                "identificacao": "Pó branco nas folhas (farinha).",
                "controle": "Leite 10% no sol. Bicarbonato.",
                "produtos": ["Score (Químico)", "Enxofre", "Bicarbonato de Potássio"]
            },
            "Overfert": {
                "tipo": "Nutrição",
                "identificacao": "Pontas queimadas e viradas p/ baixo (Garra).",
                "controle": "Flush (Lavagem do solo).",
                "produtos": ["Água pura", "FloraKleen"]
            },
            "Botrytis (Bud Rot)": {
                "tipo": "Fungo",
                "identificacao": "Bud podre, cinza/marrom, soltando esporos.",
                "controle": "Remoção cirúrgica. Baixar umidade urgente.",
                "produtos": ["NADA (Cortar fora)", "Desumidificador"]
            },
            "Bananas": {
                "tipo": "Estresse",
                "identificacao": "Estruturas macho amarelas na flor fêmea.",
                "controle": "Pinça molhada para remover.",
                "produtos": ["Reduzir calor/luz"]
            }
        }
    }
