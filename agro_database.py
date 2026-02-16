# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V FINAL (CORRIGIDO)

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS GENÉTICOS (CORREÇÃO DO ERRO KEYERROR)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            "Indica Dominante": {
                "fator_yield": 1.0, 
                "ciclo_dias": 60, # Dias de flora
                "desc": "Estrutura arbustiva, buds densos e pesados."
            },
            "Sativa Dominante": {
                "fator_yield": 1.2, 
                "ciclo_dias": 80, 
                "desc": "Planta alta, floração longa, buds aerados."
            },
            "Híbrida (50/50)": {
                "fator_yield": 1.1, 
                "ciclo_dias": 70, 
                "desc": "Vigor híbrido, equilíbrio entre peso e tempo."
            },
            "Automática (Ruderalis)": {
                "fator_yield": 0.6, 
                "ciclo_dias": 75, # Ciclo total
                "desc": "Ciclo rápido, não depende de fotoperíodo."
            }
        },

        # ==============================================================================
        # 2. METODOLOGIAS
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico (Solo Vivo)": {
                "descricao": "Foco em terpenos e qualidade. Ciclo natural.",
                "rendimento_base": 50, # g por planta
                "cor_tema": "#22c55e",
                "ph_ideal": "6.2 - 6.8",
                "ec_ideal": "Solo"
            },
            "Mineral (Coco/Inerte)": {
                "descricao": "Alta performance e controle. Rendimento alto.",
                "rendimento_base": 80,
                "cor_tema": "#38bdf8",
                "ph_ideal": "5.8 - 6.2",
                "ec_ideal": "1.8 - 2.2"
            },
            "Hidroponia (DWC)": {
                "descricao": "Crescimento explosivo. Rendimento máximo.",
                "rendimento_base": 110,
                "cor_tema": "#a855f7",
                "ph_ideal": "5.5 - 5.8",
                "ec_ideal": "1.2 - 1.8"
            },
            "Outdoor (Sol)": {
                "descricao": "Energia solar total. Plantas de grande porte.",
                "rendimento_base": 150,
                "cor_tema": "#facc15",
                "ph_ideal": "6.0 - 7.0",
                "ec_ideal": "Solo"
            }
        },

        # ==============================================================================
        # 3. FASES DINÂMICAS & AMEAÇAS
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula (Semana 1-2)": {
                "foco": "Enraizamento",
                "obs": "Umidade 70%+. Luz fraca. Não adubar.",
                "ameacas": ["Pythium (Root Rot)", "Fungus Gnats"]
            },
            "Vegetativo (Semana 3-6)": {
                "foco": "Estrutura/Poda",
                "obs": "Topping/LST. Nitrogênio alto. Vento forte.",
                "ameacas": ["Tripes", "Spider Mites", "Deficiência N"]
            },
            "Pré-Flora (Semana 7-8)": {
                "foco": "Stretch/Sexagem",
                "obs": "Rede SCROG. Remover machos. Aumentar CalMag.",
                "ameacas": ["Deficiência Mg", "Deficiência Ca", "Hermafroditas"]
            },
            "Flora Inicial (Semana 9-11)": {
                "foco": "Formação de Botões",
                "obs": "PK Booster. Baixar umidade para 50%.",
                "ameacas": ["Oídio", "Overfert"]
            },
            "Flora Final (Semana 12+)": {
                "foco": "Engorda/Resina",
                "obs": "Flush (Lavagem). Umidade <45%. Monitorar Tricomas.",
                "ameacas": ["Botrytis (Bud Rot)", "Bananas"]
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
            },
            "Hermafroditas": {
                "tipo": "Estresse",
                "identificacao": "Sacos de pólen em plantas fêmeas.",
                "controle": "Remover a planta ou os sacos com cuidado extremo.",
                "produtos": ["Água (para matar pólen)"]
            }
        }
    }
