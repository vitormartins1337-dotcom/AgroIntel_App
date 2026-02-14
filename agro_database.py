# ARQUIVO: agro_database.py
# VERSÃO: MASTER CONSULTORIA + PLANTIO DE PRECISÃO

def get_agro_db():
    return {
        "Soja": {
            "nome_cientifico": "Glycine max",
            "manejo_plantio": {
                "solo_ideal": "Argiloso a Franco-Arenoso. pH 5.5 a 6.5. Saturação (V%) ideal: 60-70%.",
                "populacao": "240.000 a 350.000 plantas/ha (depende do Grupo de Maturação).",
                "espacamento": "45cm ou 50cm entre linhas. Média de 10 a 14 sementes/metro.",
                "profundidade": "3 a 5 cm. (Solo arenoso pede mais profundidade que argiloso).",
                "maquinario": {
                    "sistema": "Disco Duplo Desencontrado ou Facão (em solos compactados).",
                    "velocidade": "Máximo 6 km/h. Acima disso, o coeficiente de variação (CV) explode e perde stand.",
                    "pressao_linha": "Regular molas para garantir contato semente-solo, mas sem compactar a parede do sulco.",
                    "tecnologia": "Obrigatório uso de Inoculante (Bradyrhizobium) no sulco ou TS. Grafite na caixa para fluidez."
                },
                "alerta_tecnico": "Cuidado com o 'Espelhamento do Sulco' em plantio com solo muito úmido. A raiz não rompe a parede compactada e a planta fica 'bonsai'."
            },
            "fases_fenologicas": {
                "VE-V2": {
                    "fase": "Emergência e Estabelecimento",
                    "foco": "Raiz e Stand",
                    "visao_pratica": "O potencial produtivo é definido aqui. Não aceite 'perder plantas'. Avalie o vigor: se a soja demorar mais de 7 dias para emergir, o risco de doença de solo (Rhizoctonia/Fusarium) dobra.",
                    "alerta": "Lagarta Elasmo em anos secos corta o colo da planta."
                },
                "V3-V6": {
                    "fase": "Desenv. Vegetativo",
                    "foco": "Construção e Sanidade Inicial",
                    "visao_pratica": "Fase crítica para herbicidas. Fitotoxidez aqui custa internódios. É a hora de limpar a lavoura de plantas daninhas. Mancha Alvo: primeira aplicação no fechamento.",
                    "alerta": "Ácaros e Tripes podem iniciar aqui em veranicos."
                },
                "R1-R2": {
                    "fase": "Florescimento",
                    "foco": "Proteção do Baixeiro",
                    "visao_pratica": "A planta define quantas vagens vai ter. O fungicida aplicado aqui é o mais importante do ciclo: ele protege as folhas de baixo.",
                    "alerta": "Pressão máxima de Ferrugem e Lagartas."
                },
                "R3-R5.1": {
                    "fase": "Canivete a Enchimento",
                    "foco": "Peso de Grão (TGW)",
                    "visao_pratica": "O 'dreno' é intenso. Se faltou Potássio (K), a folha queima. Percevejo aqui é devastador: 1 percevejo/m² causa dano irreversível.",
                    "alerta": "Dano de percevejo agora não tem cura."
                },
                "R5.5-R7": {
                    "fase": "Maturação",
                    "foco": "Qualidade de Semente",
                    "visao_pratica": "Monitorar DFC e percevejos. Dessecação: não antecipe demais para não colher grão verde.",
                    "alerta": "Chuva na colheita = Grão ardido e fermentado."
                }
            },
            "problemas": {
                "Pragas": {
                    "Percevejo-marrom": {
                        "tipo": "Praga",
                        "nome_cientifico": "Euschistus heros",
                        "fases_criticas": ["R3", "R4", "R5"],
                        "nivel_dano": "2/m (Grão) | 0.5/m (Semente)",
                        "identificacao_campo": "Adulto marrom escuro com espinhos laterais. Fica escondido na palhada.",
                        "sintomas": "Retenção foliar (soja louca), grãos 'chupados'.",
                        "manejo_quimico": [
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Perito", "Orthene"], "mecanismo": "Choque", "observacao": "Obrigatório para baixar população alta."},
                            {"ativo": "Tiametoxam + Lambda", "grupo_quimico": "Neonic + Piretroide", "sugestao_produtos": ["Engeo Pleno"], "mecanismo": "Sistêmico + Contato", "observacao": "Padrão de mercado."}
                        ]
                    }
                },
                "Doencas": {
                    "Ferrugem-asiatica": {
                        "tipo": "Doença",
                        "nome_cientifico": "Phakopsora pachyrhizi",
                        "fases_criticas": ["R1 ao final"],
                        "nivel_dano": "Zero. Preventivo é Lei.",
                        "identificacao_campo": "Urediniosporos na face abaxial (contra a luz).",
                        "sintomas": "Desfolha rápida. Ciclo encurtado.",
                        "manejo_quimico": [
                            {"ativo": "Mancozebe", "grupo_quimico": "Ditiocarbamato", "sugestao_produtos": ["Unizeb Gold"], "mecanismo": "Multissítio", "observacao": "Base da resistência. Sempre misturar."},
                            {"ativo": "Protioconazol + Bixafen", "grupo_quimico": "Triazol + Carboxamida", "sugestao_produtos": ["Fox Xpro"], "mecanismo": "Sistêmico", "observacao": "Padrão ouro atual."}
                        ]
                    }
                }
            }
        },
        "Milho": {
            "nome_cientifico": "Zea mays",
            "manejo_plantio": {
                "solo_ideal": "Alta fertilidade, bem drenado. Exigente em Nitrogênio e Zinco. V% ideal: 70%.",
                "populacao": "60.000 a 80.000 plantas/ha (Híbridos modernos aguentam mais população).",
                "espacamento": "45cm a 50cm (Tendência de reduzir para fechar linha rápido).",
                "profundidade": "4 a 6 cm. Uniformidade é tudo: Planta 'dominada' (atrasada) vira erva daninha.",
                "maquinario": {
                    "sistema": "Distribuição Pneumática (Vácuo) é superior ao disco mecânico para evitar duplas/falhas.",
                    "velocidade": "Rigidamente 5.5 km/h. Milho não aceita desaforo de velocidade.",
                    "pressao_linha": "Rodas compactadoras em 'V' para fechar o sulco sem deixar bolsão de ar.",
                    "tecnologia": "Singulação (Discos Selenium/Precision Planting) deve estar acima de 98%."
                },
                "alerta_tecnico": "A 'Planta Dominada' produz 50% menos. Se a semente ficar na superfície ou muito funda, ela nasce atrasada e vira prejuízo."
            },
            "fases_fenologicas": {
                "VE-V3": {
                    "fase": "Estabelecimento",
                    "foco": "Percevejo e Cigarrinha",
                    "visao_pratica": "O percevejo Barriga-verde injeta toxina aqui. A cigarrinha transmite o enfezamento agora.",
                    "alerta": "Lagarta do cartucho pode cortar planta rente ao solo."
                },
                "V4-V8": {
                    "fase": "Definição Produtiva",
                    "foco": "Nitrogênio e Cartucho",
                    "visao_pratica": "Define-se o nº de fileiras da espiga. A ureia tem que ser aplicada até V5.",
                    "alerta": "Mancha Branca começa no baixeiro."
                },
                "VT-R1": {
                    "fase": "Pendoamento",
                    "foco": "Polinização",
                    "visao_pratica": "Momento crítico para aplicação aérea. Proteger a folha da espiga.",
                    "alerta": "Pulgão do milho pode cobrir o pendão."
                }
            },
            "problemas": {
                "Pragas": {
                    "Cigarrinha-do-milho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Dalbulus maidis",
                        "fases_criticas": ["VE até V8"],
                        "nivel_dano": "Presença = Controle",
                        "identificacao_campo": "Pequena, branca/palha, aloja-se no cartucho.",
                        "sintomas": "Transmite Enfezamentos. Planta anã.",
                        "manejo_quimico": [
                            {"ativo": "Imidacloprido", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Confidor"], "mecanismo": "Sistêmico", "observacao": "Fundamental no TS."},
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Orthene"], "mecanismo": "Contato", "observacao": "Adulticida de choque."}
                        ]
                    },
                    "Lagarta-do-cartucho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Spodoptera frugiperda",
                        "fases_criticas": ["V3-VT"],
                        "nivel_dano": "20% plantas raspadas.",
                        "identificacao_campo": "Y invertido na cabeça. Cartucho.",
                        "sintomas": "Cartucho destruído.",
                        "manejo_quimico": [
                            {"ativo": "Espinetoram", "grupo_quimico": "Espinosina", "sugestao_produtos": ["Exalt"], "mecanismo": "Choque/Ingestão", "observacao": "Produto premium."},
                            {"ativo": "Lufenurom", "grupo_quimico": "Fisiológico", "sugestao_produtos": ["Match"], "mecanismo": "Inibidor de Quitina", "observacao": "Preventivo."}
                        ]
                    }
                },
                "Doencas": {
                     "Mancha-branca": {
                        "tipo": "Doença",
                        "nome_cientifico": "Phaeosphaeria maydis",
                        "fases_criticas": ["V8 a VT"],
                        "nivel_dano": "Lesões no baixeiro.",
                        "identificacao_campo": "Manchas pálidas (brancas/secas).",
                        "sintomas": "Seca da folha.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina + Ciproconazol", "grupo_quimico": "Estrobilurina + Triazol", "sugestao_produtos": ["Priori Xtra"], "mecanismo": "Sistêmico", "observacao": "Aplicação V8 é essencial."}
                        ]
                    }
                }
            }
        },
        "Algodão": {
            "nome_cientifico": "Gossypium hirsutum",
            "manejo_plantio": {
                "solo_ideal": "Solos profundos (raiz pivotante), sem compactação (pé-de-grade) e corrigidos (V% 60-70%).",
                "populacao": "80.000 a 110.000 plantas/ha. (Adensado sobe para 200k).",
                "espacamento": "76cm a 90cm. O fechamento da entrelinha é crucial para controle de mato.",
                "profundidade": "2 a 4 cm (Raso). Semente com pouca reserva, exige emergência rápida.",
                "maquinario": {
                    "sistema": "Disco de corte turbo. Plantio direto na palha é desafio devido ao 'Hairpinning' (dobra da palha).",
                    "velocidade": "4 a 6 km/h. Algodão exige precisão cirúrgica.",
                    "pressao_linha": "Baixa. Solo muito compactado sobre a semente causa 'encrostamento' e a plântula não rompe.",
                    "tecnologia": "Tratamento de Sementes Industrial (TSI) é mandatório para pragas iniciais e doenças (Tombamento)."
                },
                "alerta_tecnico": "Temperatura do solo abaixo de 20°C inibe a germinação. Não plante com previsão de frio/chuva intensa nos próximos 3 dias."
            },
            "fases_fenologicas": {
                "V1-V4": {
                    "fase": "Vegetativo Inicial",
                    "foco": "Raiz, Tripes e Regulador",
                    "visao_pratica": "Se a planta 'disparar' aqui, você perde o baixeiro. Tripes encarquilha a folha.",
                    "alerta": "Pulgão transmite viroses."
                },
                "B1 (Botão Floral)": {
                    "fase": "Esquadratura",
                    "foco": "Bicudo e Retenção",
                    "visao_pratica": "Cada botão que cai é menos peso. Bicudo entra agora. Regulador deve ser contínuo.",
                    "alerta": "Lagarta das maçãs ataca estrutura reprodutiva."
                },
                "F1 (Florada)": {
                    "fase": "Florescimento",
                    "foco": "Ramulária e Cut-out",
                    "visao_pratica": "O alvo vira a Ramulária. Monitore o 'Cut-out' para saber quando a planta parou de vegetar.",
                    "alerta": "Mosca-branca na florada = mela na fibra."
                }
            },
            "problemas": {
                "Pragas": {
                    "Bicudo-do-algodoeiro": {
                        "tipo": "Praga",
                        "nome_cientifico": "Anthonomus grandis",
                        "fases_criticas": ["B1 até Colheita"],
                        "nivel_dano": "Zero Tolerância.",
                        "identificacao_campo": "Besouro cinza/negro com 'bico' longo.",
                        "sintomas": "Queda massiva de botões.",
                        "manejo_quimico": [
                            {"ativo": "Malationa", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Malathion"], "mecanismo": "Acetilcolinesterase", "observacao": "Padrão para baterias."},
                            {"ativo": "Fipronil", "grupo_quimico": "Pirazol", "sugestao_produtos": ["Regent"], "mecanismo": "GABA", "observacao": "Excelente residual."}
                        ]
                    }
                },
                "Doencas": {
                     "Ramularia": {
                        "tipo": "Doença",
                        "nome_cientifico": "Ramularia areola",
                        "fases_criticas": ["B1 em diante"],
                        "nivel_dano": "Preventivo obrigatório.",
                        "identificacao_campo": "Manchas angulares brancas (talco).",
                        "sintomas": "Desfolha total precoce.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina + Difenoconazol", "grupo_quimico": "Estrobilurina + Triazol", "sugestao_produtos": ["Priori Top"], "mecanismo": "Sistêmico", "observacao": "Referência."},
                            {"ativo": "Clorotalonil", "grupo_quimico": "Multissítio", "sugestao_produtos": ["Bravonil"], "mecanismo": "Contato", "observacao": "Obrigatório adicionar."}
                        ]
                    }
                }
            }
        },
        "Arroz": {
            "nome_cientifico": "Oryza sativa",
            "manejo_plantio": {
                "solo_ideal": "Planos e sistematizados (Laser). Solos de várzea com camada impermeável para segurar água.",
                "populacao": "80 a 120 kg de semente/ha (Sistema convencional/Cultivo Mínimo).",
                "espacamento": "17cm a 20cm entre linhas.",
                "profundidade": "1 a 3 cm. Arroz tem pouca força de emergência se enterrado demais.",
                "maquinario": {
                    "sistema": "Semeadura em linha (Plantio Direto ou Convencional) ou Pré-germinado (Lanço na lama).",
                    "velocidade": "Lenta. O nivelamento do solo é mais importante que a velocidade.",
                    "pressao_linha": "Mínima em solos úmidos para não compactar.",
                    "tecnologia": "Taipa (lombada) deve ser construída antes ou logo após o plantio com precisão de nível."
                },
                "alerta_tecnico": "O segredo do arroz é a entrada da água. O plantio deve ser planejado para coincidir com a capacidade de bombeamento de água na fase V3/V4."
            },
            "fases_fenologicas": {
                "V1-V4": {
                    "fase": "Plântula e Perfilhamento",
                    "foco": "Água e Nitrogênio",
                    "visao_pratica": "Adubação nitrogenada em solo seco, antes da água. Perfilhos definem panículas.",
                    "alerta": "Bicheira-da-raiz reduz o stand."
                },
                "R1": {
                    "fase": "Ponto de Algodão",
                    "foco": "Proteção da Bainha",
                    "visao_pratica": "Início das aplicações preventivas para Brusone. Não deixe faltar água.",
                    "alerta": "Lagarta-da-panícula pode cortar a base."
                },
                "R4": {
                    "fase": "Florada",
                    "foco": "Brusone do Pescoço",
                    "visao_pratica": "Se a Brusone entrar no pescoço agora, a espiga fica branca. Triciclazol preventivo.",
                    "alerta": "Frio na florada causa esterilidade."
                }
            },
            "problemas": {
                "Pragas": {
                    "Bicheira-da-raiz": {
                        "tipo": "Praga",
                        "nome_cientifico": "Oryzophagus oryzae",
                        "fases_criticas": ["Pós inundação"],
                        "nivel_dano": "Larvas nas raízes.",
                        "identificacao_campo": "Plantas amareladas. Raízes podadas.",
                        "sintomas": "Planta solta fácil.",
                        "manejo_quimico": [
                            {"ativo": "Fipronil", "grupo_quimico": "Pirazol", "sugestao_produtos": ["Standak"], "mecanismo": "GABA", "observacao": "TS é o padrão."},
                            {"ativo": "Clorantraniliprole", "grupo_quimico": "Diamida", "sugestao_produtos": ["Dermacor"], "mecanismo": "Muscular", "observacao": "Excelente seletividade."}
                        ]
                    }
                },
                "Doencas": {
                     "Brusone": {
                        "tipo": "Doença",
                        "nome_cientifico": "Magnaporthe oryzae",
                        "fases_criticas": ["V4 e R4"],
                        "nivel_dano": "Pode dar 100% de perda.",
                        "identificacao_campo": "Folha: mancha 'olho'. Pescoço: necrose escura.",
                        "sintomas": "Quebra do pescoço, panícula branca.",
                        "manejo_quimico": [
                            {"ativo": "Triciclazol", "grupo_quimico": "Redutase", "sugestao_produtos": ["Bim"], "mecanismo": "Preventivo", "observacao": "Padrão mundial. Aplicar ANTES."},
                            {"ativo": "Kasugamicina", "grupo_quimico": "Antibiótico", "sugestao_produtos": ["Kasumin"], "mecanismo": "Síntese Proteica", "observacao": "Curativo."}
                        ]
                    }
                }
            }
        }
    }
