# ARQUIVO: data_engine.py
# FUNÇÃO: Banco de Dados Agronômico Enterprise
# VERSÃO: 1.0 (Database Core)

def get_database():
    """
    Retorna o dicionário mestre de culturas, variedades, pragas e defensivos.
    Estrutura otimizada para consulta rápida.
    """
    return {
        # ==============================================================================
        # GRUPO A: GRANDES CULTURAS (COMMODITIES)
        # ==============================================================================
        "Soja (Glycine max)": {
            "t_base": 10,
            "vars": {
                "Intacta 2 Xtend": {"kc": 1.15, "gda_meta": 1400, "info": "Tecnologia I2X. Resistência a lagartas (Helicoverpa/Spodoptera) e herbicida Dicamba. Refúgio estruturado obrigatório (20%)."},
                "Brasmax": {"kc": 1.15, "gda_meta": 1350, "info": "Alto teto produtivo. Exige perfil de solo corrigido (Sat. Bases > 60%) e manejo fino de fungicidas."},
                "Conkesta Enlist": {"kc": 1.15, "gda_meta": 1450, "info": "Sistema Enlist (Tolerância a 2,4-D Colina, Glifosato e Glufosinato). Excelente para áreas com Buva resistente."}
            },
            "fases": {
                "Emergência (VE)": {
                    "desc": "Cotilédones acima do solo.",
                    "fisiologia": "Início da autotrofia. Radícula pivotante em descida rápida. Fase crítica para stand final.",
                    "manejo": "Monitorar Damping-off (Rhizoctonia/Pythium) e Lagarta Elasmo em solos arenosos ou sob stress hídrico.",
                    "quimica": [
                        {"Alvo": "Damping-off", "Ativo": "Carboxina + Tiram", "Grupo": "Carboxamida", "Tipo": "Tratamento Sementes"},
                        {"Alvo": "Elasmo", "Ativo": "Fipronil", "Grupo": "Pirazol", "Tipo": "TS / Sulco"},
                        {"Alvo": "Nematoides", "Ativo": "Abamectina", "Grupo": "Avermectina", "Tipo": "TS"}
                    ]
                },
                "Vegetativo (V3-V6)": {
                    "desc": "Desenvolvimento de nós e folhas trifolioladas.",
                    "fisiologia": "Estabelecimento da FBN (Fixação Biológica de Nitrogênio). Alta demanda de P e K. Definição do potencial produtivo.",
                    "manejo": "Manejo de daninhas (Glifosato/Dicamba). Monitorar Lagartas (Helicoverpa/Spodoptera) e Ácaros.",
                    "quimica": [
                        {"Alvo": "Lagartas", "Ativo": "Benzoato de Emamectina", "Grupo": "Avermectina", "Tipo": "Ingestão/Contato"},
                        {"Alvo": "Lagartas", "Ativo": "Clorantraniliprole", "Grupo": "Diamida", "Tipo": "Sistêmico Longa Duração"},
                        {"Alvo": "Buva/Amargoso", "Ativo": "Diclosulam", "Grupo": "ALS", "Tipo": "Herbicida Seletivo"}
                    ]
                },
                "Reprodutivo (R1-R2)": {
                    "desc": "Florescimento pleno.",
                    "fisiologia": "Definição do número de vagens. Estresse hídrico causa abortamento severo de flores.",
                    "manejo": "Entrada de Fungicidas para Ferrugem Asiática (Phakopsora) e Mancha Alvo (Corynespora).",
                    "quimica": [
                        {"Alvo": "Ferrugem Asiática", "Ativo": "Protioconazol + Trifloxistrobina", "Grupo": "Triazol + Estrobilurina", "Tipo": "Sistêmico/Mesostêmico"},
                        {"Alvo": "Mancha Alvo", "Ativo": "Fluxapiroxade", "Grupo": "Carboxamida", "Tipo": "Sistêmico"},
                        {"Alvo": "Multissítio", "Ativo": "Mancozebe", "Grupo": "Ditiocarbamato", "Tipo": "Protetor Obrigatório"}
                    ]
                },
                "Enchimento (R5)": {
                    "desc": "Formação de grãos.",
                    "fisiologia": "Máxima translocação de fotoassimilados. Peso de Mil Grãos (PMG) sendo definido.",
                    "manejo": "Controle de Percevejos (Marrom/Verde/Barriga-Verde) para evitar grão picado e retenção foliar.",
                    "quimica": [
                        {"Alvo": "Percevejo", "Ativo": "Acefato", "Grupo": "Organofosforado", "Tipo": "Choque"},
                        {"Alvo": "Percevejo", "Ativo": "Tiametoxam + Lambda-Cialotrina", "Grupo": "Neo + Piretroide", "Tipo": "Sistêmico + Choque"}
                    ]
                }
            }
        },
        "Milho (Zea mays)": {
            "t_base": 10,
            "vars": {
                "Pioneer Bt": {"kc": 1.2, "gda_meta": 1600, "info": "Híbrido Precoce de alto investimento. Exige N parcelado."},
                "Dekalb": {"kc": 1.2, "gda_meta": 1650, "info": "Rústico. Boa tolerância a estresse hídrico e sanidade de colmo."}
            },
            "fases": {
                "Vegetativo (V4-V8)": {
                    "desc": "Definição do número de fileiras da espiga.",
                    "fisiologia": "Ponto de crescimento sai do solo. Alta absorção de Nitrogênio.",
                    "manejo": "Controle rigoroso de Cigarrinha (Dalbulus maidis) para evitar Enfezamentos (Spiroplasma).",
                    "quimica": [
                        {"Alvo": "Cigarrinha", "Ativo": "Clotianidina", "Grupo": "Neonicotinoide", "Tipo": "Sistêmico"},
                        {"Alvo": "Percevejo Barriga-Verde", "Ativo": "Metomil", "Grupo": "Carbamato", "Tipo": "Choque"},
                        {"Alvo": "Lagarta do Cartucho", "Ativo": "Espinetoram", "Grupo": "Espinocina", "Tipo": "Ingestão"}
                    ]
                },
                "Pendoamento (VT)": {
                    "desc": "Emissão do pendão (inflorescência masculina).",
                    "fisiologia": "Polinização. Fase mais crítica para falta de água.",
                    "manejo": "Aplicação de Fungicida preventivo (Mancha Branca/Cercospora).",
                    "quimica": [
                        {"Alvo": "Mancha Branca", "Ativo": "Azoxistrobina + Ciproconazol", "Grupo": "Estrobilurina + Triazol", "Tipo": "Sistêmico"},
                        {"Alvo": "Pulgão", "Ativo": "Acetamiprido", "Grupo": "Neonicotinoide", "Tipo": "Sistêmico"}
                    ]
                }
            }
        },

        # ==============================================================================
        # GRUPO B: HORTIFRUTI (HF) & TUBÉRCULOS
        # ==============================================================================
        "Batata (Solanum tuberosum)": {
            "t_base": 7,
            "vars": {
                "Orchestra": {"kc": 1.15, "gda_meta": 1600, "info": "Pele lisa premium. Exige K e Ca para acabamento. Sensível a Pinta Preta."},
                "Cupido": {"kc": 1.10, "gda_meta": 1400, "info": "Ciclo curto. Extrema sensibilidade à Requeima (Phytophthora). Colheita rápida."},
                "Atlantic": {"kc": 1.15, "gda_meta": 1650, "info": "Indústria (Chips). Monitorar Matéria Seca e Coração Oco."}
            },
            "fases": {
                "Emergência": {
                    "desc": "Brotamento e Enraizamento.",
                    "fisiologia": "Dreno de reservas da batata-mãe. Raízes frágeis.",
                    "manejo": "Solo friável. Evitar encharcamento (Pectobacterium/Canela Preta).",
                    "quimica": [
                        {"Alvo": "Rizoctonia (Cancro)", "Ativo": "Azoxistrobina", "Grupo": "Estrobilurina", "Tipo": "Sulco de Plantio"},
                        {"Alvo": "Larva Minadora", "Ativo": "Ciromazina", "Grupo": "Regulador de Crescimento", "Tipo": "Foliar"},
                        {"Alvo": "Pragas de Solo", "Ativo": "Fipronil", "Grupo": "Fenilpirazol", "Tipo": "Sulco"}
                    ]
                },
                "Estolonização": {
                    "desc": "Crescimento vegetativo e início dos estolões.",
                    "fisiologia": "Alta demanda de N para índice de área foliar (IAF).",
                    "manejo": "Realizar a Amontoa. Monitorar Vaquinha (Diabrotica) e Pulgão (Viroses).",
                    "quimica": [
                        {"Alvo": "Requeima (Preventivo)", "Ativo": "Mancozeb", "Grupo": "Ditiocarbamato", "Tipo": "Protetor"},
                        {"Alvo": "Vaquinha", "Ativo": "Tiametoxam", "Grupo": "Neonicotinoide", "Tipo": "Sistêmico"},
                        {"Alvo": "Pulgão", "Ativo": "Pimetrozina", "Grupo": "Piridina", "Tipo": "Seletivo"}
                    ]
                },
                "Tuberização": {
                    "desc": "Início do Gancho (Fase Crítica).",
                    "fisiologia": "Inversão hormonal (Giberelina cai). Estresse hídrico causa Sarna e abortamento.",
                    "manejo": "Irrigação frequente e leve. Controle 'militar' de Requeima.",
                    "quimica": [
                        {"Alvo": "Requeima", "Ativo": "Metalaxil-M + Mancozeb", "Grupo": "Fenilamida + Protetor", "Tipo": "Curativo/Sistêmico"},
                        {"Alvo": "Requeima", "Ativo": "Mandipropamida", "Grupo": "CAA", "Tipo": "Translaminar (Forte fixação na cera)"},
                        {"Alvo": "Alternaria", "Ativo": "Metiram", "Grupo": "Ditiocarbamato", "Tipo": "Protetor"}
                    ]
                },
                "Enchimento": {
                    "desc": "Engorda dos tubérculos.",
                    "fisiologia": "Dreno forte de Potássio e Magnésio. Translocação Folha -> Tubérculo.",
                    "manejo": "Monitorar Traça (Phthorimaea), Mosca Branca e Larva Alfinete.",
                    "quimica": [
                        {"Alvo": "Traça", "Ativo": "Clorfenapir", "Grupo": "Pirrol", "Tipo": "Ingestão/Contato"},
                        {"Alvo": "Mosca Branca", "Ativo": "Ciantraniliprole", "Grupo": "Diamida", "Tipo": "Sistêmico"},
                        {"Alvo": "Mosca Branca (Ninfa)", "Ativo": "Espirotesifeno", "Grupo": "Cetoenol", "Tipo": "Inibidor de Lipídeos"},
                        {"Alvo": "Alternaria", "Ativo": "Boscalida", "Grupo": "Carboxamida", "Tipo": "Sistêmico"}
                    ]
                }
            }
        },
        "Tomate (Solanum lycopersicum)": {
            "t_base": 10,
            "vars": {
                "Italiano": {"kc": 1.2, "gda_meta": 1600, "info": "Determinado (Rasteiro/Vara). Sensível a Fundo Preto (Deficiência de Ca)."},
                "Grape": {"kc": 1.1, "gda_meta": 1450, "info": "Indeterminado. Alto teor de brix. Sensível a Rachadura."}
            },
            "fases": {
                "Vegetativo": {
                    "desc": "Crescimento de hastes.",
                    "fisiologia": "Formação estrutural.",
                    "manejo": "Desbrota lateral. Controle de Tripes (Vetor de Vira-Cabeça/TSWV).",
                    "quimica": [
                        {"Alvo": "Tripes", "Ativo": "Espinetoram", "Grupo": "Espinocina", "Tipo": "Choque/Residual"},
                        {"Alvo": "Bacteriose", "Ativo": "Cobre + Kasugamicina", "Grupo": "Antibiótico", "Tipo": "Protetor"},
                        {"Alvo": "Mosca Branca", "Ativo": "Acetamiprido", "Grupo": "Neonicotinoide", "Tipo": "Sistêmico"}
                    ]
                },
                "Frutificação": {
                    "desc": "Formação e engorda de frutos.",
                    "fisiologia": "Alta demanda de Cálcio para parede celular.",
                    "manejo": "Monitorar Traça (Tuta absoluta) e Requeima.",
                    "quimica": [
                        {"Alvo": "Tuta absoluta", "Ativo": "Indoxacarbe", "Grupo": "Oxadiazina", "Tipo": "Ingestão"},
                        {"Alvo": "Tuta absoluta", "Ativo": "Clorantraniliprole", "Grupo": "Diamida", "Tipo": "Sistêmico"},
                        {"Alvo": "Requeima", "Ativo": "Zoxamida", "Grupo": "Benzamida", "Tipo": "Protetor de Alta Adesão"}
                    ]
                }
            }
        },

        # ==============================================================================
        # GRUPO C: FRUTAS FINAS (BERRIES)
        # ==============================================================================
        "Amora Preta (Blackberry)": {
            "t_base": 7,
            "vars": {
                "Tupy": {"kc": 1.0, "gda_meta": 1500, "info": "Exige horas de frio. Alta produtividade. Presença de espinhos."},
                "BRS Xingu": {"kc": 1.05, "gda_meta": 1400, "info": "Cultivar sem espinhos. Facilita manejo e colheita. Boa conservação pós-colheita."}
            },
            "fases": {
                "Brotação": {
                    "desc": "Emissão de novas hastes produtivas.",
                    "fisiologia": "Alta demanda de Nitrogênio para vigor vegetativo.",
                    "manejo": "Seleção de hastes. Monitoramento de Ferrugem.",
                    "quimica": [
                        {"Alvo": "Ferrugem", "Ativo": "Tebuconazol", "Grupo": "Triazol", "Tipo": "Curativo"},
                        {"Alvo": "Cochonilha", "Ativo": "Óleo Mineral", "Grupo": "Físico", "Tipo": "Contato (Sufocamento)"}
                    ]
                },
                "Frutificação": {
                    "desc": "Formação e maturação de bagas.",
                    "fisiologia": "Acúmulo de sólidos solúveis (Brix). Fruto não climatérico.",
                    "manejo": "Controle de Drosophila suzukii (SWD) e Botrytis.",
                    "quimica": [
                        {"Alvo": "SWD (Mosca)", "Ativo": "Espinosade", "Grupo": "Espinocina", "Tipo": "Isca Biológica/Tóxica"},
                        {"Alvo": "Botrytis", "Ativo": "Iprodiona", "Grupo": "Dicarboximida", "Tipo": "Contato"},
                        {"Alvo": "Antracnose", "Ativo": "Piraclostrobina", "Grupo": "Estrobilurina", "Tipo": "Preventivo"}
                    ]
                }
            }
        },
        "Framboesa (Raspberry)": {
            "t_base": 7,
            "vars": {
                "Heritage": {"kc": 1.1, "gda_meta": 1300, "info": "Remontante (Produz na haste do ano e do ano anterior). Rústica."}
            },
            "fases": {
                "Vegetativo": {
                    "desc": "Crescimento de canas.",
                    "fisiologia": "Estruturação.",
                    "manejo": "Ácaro Vermelho (Tetranychus urticae).",
                    "quimica": [
                        {"Alvo": "Ácaro", "Ativo": "Abamectina", "Grupo": "Avermectina", "Tipo": "Translaminar"},
                        {"Alvo": "Ácaro", "Ativo": "Propargito", "Grupo": "Sulfito", "Tipo": "Contato"}
                    ]
                },
                "Produção": {
                    "desc": "Flores e Frutos.",
                    "fisiologia": "Sensível a chuva na flor (abortamento).",
                    "manejo": "Podridão Cinzenta (Botrytis).",
                    "quimica": [
                        {"Alvo": "Botrytis", "Ativo": "Ciprodinil + Fludioxonil", "Grupo": "Anilinopirimidina + Fenilpirrol", "Tipo": "Sistêmico Local (Switch)"}
                    ]
                }
            }
        },
        "Mirtilo (Blueberry)": {
            "t_base": 7, 
            "vars": {
                "Emerald": {"kc": 0.95, "gda_meta": 1800, "info": "Exige pH ácido (4.5). Alta exigência de matéria orgânica."},
                "Biloxi": {"kc": 0.90, "gda_meta": 1900, "info": "Ereta. Poda de limpeza central necessária. Baixa exigência de frio."}
            },
            "fases": {
                "Florada": {
                    "desc": "Polinização.",
                    "fisiologia": "Dependência de Abelhas (Bombus/Mamangavas). Polinização cruzada aumenta calibre.",
                    "manejo": "Controle de Botrytis sem afetar abelhas.",
                    "quimica": [
                        {"Alvo": "Botrytis", "Ativo": "Fludioxonil", "Grupo": "Fenilpirrol", "Tipo": "Contato (Seguro p/ abelhas à noite)"},
                        {"Alvo": "Ferrugem", "Ativo": "Difenoconazol", "Grupo": "Triazol", "Tipo": "Curativo"}
                    ]
                },
                "Fruto Verde": {
                    "desc": "Crescimento de bagas.",
                    "fisiologia": "Evitar Nitrato (Usar Amônio).",
                    "manejo": "Antracnose.",
                    "quimica": [
                        {"Alvo": "Antracnose", "Ativo": "Azoxistrobina", "Grupo": "Estrobilurina", "Tipo": "Sistêmico"}
                    ]
                }
            }
        },
        "Morango": {
            "t_base": 7, 
            "vars": {
                "Albion": {"kc": 0.85, "gda_meta": 1250, "info": "Dia neutro. Sabor excelente. Sensível a Colletotrichum."},
                "San Andreas": {"kc": 0.85, "gda_meta": 1200, "info": "Dia neutro. Mais rústica. Sensível a ácaros."}
            },
            "fases": {
                "Produção": {
                    "desc": "Colheita contínua.",
                    "fisiologia": "Alta extração K e Ca.",
                    "manejo": "Ácaro Rajado e Mofo Cinzento. Limpeza sanitária.",
                    "quimica": [
                        {"Alvo": "Ácaro", "Ativo": "Etoxazol", "Grupo": "Inibidor de Crescimento", "Tipo": "Contato (Ovos/Ninfas)"},
                        {"Alvo": "Ácaro (Adulto)", "Ativo": "Fenpiroximato", "Grupo": "METI", "Tipo": "Choque"},
                        {"Alvo": "Oídio", "Ativo": "Enxofre", "Grupo": "Inorgânico", "Tipo": "Protetor/Vapor"},
                        {"Alvo": "Botrytis", "Ativo": "Procimidona", "Grupo": "Dicarboximida", "Tipo": "Contato"}
                    ]
                }
            }
        },

        # ==============================================================================
        # GRUPO D: CULTURAS PERENES TROPICAIS
        # ==============================================================================
        "Café (Coffea arabica)": {
            "t_base": 10, 
            "vars": {
                "Catuaí": {"kc": 1.1, "gda_meta": 3000, "info": "Padrão de qualidade de bebida. Suscetível a ferrugem e nematoides."},
                "Arara": {"kc": 1.2, "gda_meta": 2900, "info": "Alta produtividade. Resistente a ferrugem (imune). Fruto amarelo."}
            },
            "fases": {
                "Chumbinho": {
                    "desc": "Expansão rápida do fruto.",
                    "fisiologia": "Intensa divisão celular. Déficit hídrico causa queda de chumbinhos.",
                    "manejo": "Controle preventivo de Ferrugem (Hemileia) e Cercospora.",
                    "quimica": [
                        {"Alvo": "Ferrugem", "Ativo": "Ciproconazol + Azoxistrobina", "Grupo": "Triazol+Estrob", "Tipo": "Sistêmico (Via Solo ou Foliar)"},
                        {"Alvo": "Cercospora", "Ativo": "Tebuconazol", "Grupo": "Triazol", "Tipo": "Curativo"}
                    ]
                },
                "Granação": {
                    "desc": "Enchimento de grão (Sólidos).",
                    "fisiologia": "Dreno de Nitrogênio e Potássio. Risco de escaldadura.",
                    "manejo": "Monitorar Broca do Café e Bicho Mineiro.",
                    "quimica": [
                        {"Alvo": "Broca", "Ativo": "Ciantraniliprole", "Grupo": "Diamida", "Tipo": "Sistêmico"},
                        {"Alvo": "Bicho Mineiro", "Ativo": "Clorpirifós", "Grupo": "Organofosforado", "Tipo": "Contato/Vapor"},
                        {"Alvo": "Bicho Mineiro", "Ativo": "Cartape", "Grupo": "Análogo de Nereistoxina", "Tipo": "Sistêmico"}
                    ]
                }
            }
        },
        "Citros (Limão/Laranja)": {
            "t_base": 13, 
            "vars": {
                "Tahiti": {"kc": 0.75, "gda_meta": 2000, "info": "Limão Ácido. Produção contínua."}
            },
            "fases": {
                "Fluxo Vegetativo": {
                    "desc": "Brotação de folhas novas.",
                    "fisiologia": "Tecido tenro atrativo para vetores.",
                    "manejo": "Controle de Psilídeo (Diaphorina citri - Vetor do Greening/HLB) e Minadora.",
                    "quimica": [
                        {"Alvo": "Psilídeo", "Ativo": "Imidacloprido + Bifentrina", "Grupo": "Neo+Piretroide", "Tipo": "Choque e Residual"},
                        {"Alvo": "Minadora", "Ativo": "Abamectina", "Grupo": "Avermectina", "Tipo": "Translaminar"}
                    ]
                }
            }
        },
        "Uva (Vitis vinifera)": {
            "t_base": 10, 
            "vars": {
                "Vitoria": {"kc": 0.85, "gda_meta": 1500, "info": "Uva preta sem semente. Sabor Fox (framboesa)."},
                "Nubia": {"kc": 0.85, "gda_meta": 1600, "info": "Uva preta com semente. Baga grande."}
            },
            "fases": {
                "Brotação": {
                    "desc": "Gema algodonosa/Ponta verde.",
                    "fisiologia": "Mobilização de reservas.",
                    "manejo": "Míldio (Plasmopara) e Antracnose (Elsinoe).",
                    "quimica": [
                        {"Alvo": "Míldio", "Ativo": "Metalaxil-M", "Grupo": "Fenilamida", "Tipo": "Sistêmico"},
                        {"Alvo": "Antracnose", "Ativo": "Tiofanato-Metílico", "Grupo": "Benzimidazol", "Tipo": "Sistêmico"}
                    ]
                },
                "Maturação": {
                    "desc": "Véraison (Mudança de cor).",
                    "fisiologia": "Acúmulo de açúcar. Amolecimento da baga.",
                    "manejo": "Podridão do Cacho e Moscas.",
                    "quimica": [
                        {"Alvo": "Podridão", "Ativo": "Iprodiona", "Grupo": "Dicarboximida", "Tipo": "Contato"},
                        {"Alvo": "Moscas", "Ativo": "Deltametrina", "Grupo": "Piretroide", "Tipo": "Contato (Carencia curta)"}
                    ]
                }
            }
        }
    }
