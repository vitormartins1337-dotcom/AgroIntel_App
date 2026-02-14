# ARQUIVO: agro_database.py
# VERSÃO: MASTER CONSULTORIA (Nível Especialista)
# DADOS BASEADOS EM: Embrapa, FRAC, IRAC e Experiência de Campo no Cerrado/Sul.

def get_agro_db():
    return {
        "Soja": {
            "nome_cientifico": "Glycine max",
            "fases_fenologicas": {
                "VE-V2": {
                    "fase": "Emergência e Estabelecimento",
                    "foco": "Raiz e Stand",
                    "visao_pratica": "O potencial produtivo é definido aqui. Não aceite 'perder plantas'. Avalie o vigor: se a soja demorar mais de 7 dias para emergir, o risco de doença de solo (Rhizoctonia/Fusarium) dobra. Verifique a profundidade: semente muito funda gasta energia demais. Momento de avaliar a inoculação.",
                    "alerta": "Lagarta Elasmo em anos secos corta o colo da planta. Coró pode comer a raiz."
                },
                "V3-V6": {
                    "fase": "Desenv. Vegetativo",
                    "foco": "Construção e Sanidade Inicial",
                    "visao_pratica": "Fase crítica para herbicidas (Glifosato/Hormonais). Fitotoxidez aqui custa internódios. É a hora de limpar a lavoura de plantas daninhas (Buva, Capim-amargoso). Se houver histórico de Mancha Alvo, a primeira aplicação de fungicida (Zero) entra no fechamento das linhas.",
                    "alerta": "Ácaros e Tripes podem iniciar aqui em veranicos. Monitorar baixeiro."
                },
                "R1-R2": {
                    "fase": "Florescimento",
                    "foco": "Proteção do Baixeiro",
                    "visao_pratica": "A planta define quantas vagens vai ter. O fungicida aplicado aqui é o mais importante do ciclo: ele protege as folhas de baixo que sustentam o enchimento lá na frente. Proibido entrar com máquina amassando linha (perda direta de 2 sc/ha).",
                    "alerta": "Pressão máxima de Ferrugem e Lagartas do complexo Spodoptera."
                },
                "R3-R5.1": {
                    "fase": "Canivete a Enchimento",
                    "foco": "Peso de Grão (TGW)",
                    "visao_pratica": "O 'dreno' é intenso. A planta puxa tudo da folha para o grão. Se faltou Potássio (K), a folha queima. Percevejo aqui é devastador: 1 percevejo/m² causa dano irreversível (grão picado/abortado). Mantenha o residual de inseticida alto.",
                    "alerta": "Dano de percevejo agora não tem cura. Antracnose pode abortar vagens."
                },
                "R5.5-R7": {
                    "fase": "Maturação",
                    "foco": "Qualidade de Semente",
                    "visao_pratica": "Monitorar doenças de final de ciclo (DFC) e percevejos. Dessecação: não antecipe demais para não colher grão verde (desconto na trading), nem atrase para não ter abertura de vagens. O ponto é a maturidade fisiológica (R7).",
                    "alerta": "Chuva na colheita = Grão ardido e fermentado."
                }
            },
            "problemas": {
                "Pragas": {
                    "Percevejo-marrom": {
                        "tipo": "Praga",
                        "nome_cientifico": "Euschistus heros",
                        "fases_criticas": ["R3", "R4", "R5", "R6"],
                        "nivel_dano": "2/m (Grão) | 0.5/m (Semente)",
                        "identificacao_campo": "Adulto marrom escuro com espinhos laterais. Fica escondido na palhada nas horas quentes.",
                        "sintomas": "Retenção foliar (soja louca), grãos 'chupados', perda de peso e vigor.",
                        "manejo_quimico": [
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Perito", "Orthene"], "mecanismo": "Choque (Acetilcolinesterase)", "observacao": "Obrigatório para baixar população alta. Cheiro forte."},
                            {"ativo": "Tiametoxam + Lambda", "grupo_quimico": "Neonic + Piretroide", "sugestao_produtos": ["Engeo Pleno", "Kaiso"], "mecanismo": "Sistêmico + Contato", "observacao": "Padrão de mercado. Use com óleo para descer no baixeiro."},
                            {"ativo": "Bifentrina + Acetamiprido", "grupo_quimico": "Piretroide + Neonic", "sugestao_produtos": ["Sperto"], "mecanismo": "Modulador de Sódio", "observacao": "Excelente choque. Alternativa para rotacionar ativos."}
                        ]
                    },
                    "Percevejo-verde-pequeno": {
                        "tipo": "Praga",
                        "nome_cientifico": "Piezodorus guildinii",
                        "fases_criticas": ["R4", "R5"],
                        "nivel_dano": "Mais agressivo que o marrom. 1/m já justifica controle.",
                        "identificacao_campo": "Verde claro com listra transversal avermelhada no pronoto.",
                        "sintomas": "Picada profunda. Deforma muito o grão.",
                        "manejo_quimico": [
                            {"ativo": "Imidacloprido + Bifentrina", "grupo_quimico": "Neonic + Piretroide", "sugestao_produtos": ["Galil"], "mecanismo": "Sistêmico", "observacao": "Necessário dose cheia. Difícil controle."}
                        ]
                    },
                    "Lagarta-falsa-medideira": {
                        "tipo": "Praga",
                        "nome_cientifico": "Rachiplusia nu / Chrysodeixis includens",
                        "fases_criticas": ["V4", "R1", "R2"],
                        "nivel_dano": "30% desfolha (Veg) | 15% (Reprod)",
                        "identificacao_campo": "Verde clara, listras brancas, anda medindo palmos. Faz 'renda' na folha.",
                        "sintomas": "Come o parênquima e deixa as nervuras. Ataca de baixo para cima.",
                        "manejo_quimico": [
                            {"ativo": "Clorantraniliprole", "grupo_quimico": "Diamida", "sugestao_produtos": ["Premio", "Coragen"], "mecanismo": "Ingestão (Muscular)", "observacao": "Longo residual. Protege o baixeiro. Não mata adulto."},
                            {"ativo": "Indoxacarbe", "grupo_quimico": "Oxadiazina", "sugestao_produtos": ["Avatar"], "mecanismo": "Bloqueio de Sódio", "observacao": "Excelente ferramenta para manejo de resistência."},
                            {"ativo": "Bacillus thuringiensis", "grupo_quimico": "Biológico", "sugestao_produtos": ["Dipel"], "mecanismo": "Disrupção Intestinal", "observacao": "Apenas lagartas pequenas (<1.5cm)."}
                        ]
                    },
                    "Lagarta-helicoverpa": {
                        "tipo": "Praga",
                        "nome_cientifico": "Helicoverpa armigera",
                        "fases_criticas": ["R1", "R2", "R3"],
                        "nivel_dano": "Baixíssimo. Praga direta de estrutura reprodutiva.",
                        "identificacao_campo": "Corpo com pelos brancos, sela escura no quarto segmento. Come flor e vagem.",
                        "sintomas": "Furos circulares nas vagens. Destruição de botões florais.",
                        "manejo_quimico": [
                            {"ativo": "Clorfenapir", "grupo_quimico": "Pirrol", "sugestao_produtos": ["Pirate"], "mecanismo": "Desacoplador", "observacao": "Ação de choque. Dose dependente. Cuidado com fitotoxidez."},
                            {"ativo": "Espinosade", "grupo_quimico": "Espinosina", "sugestao_produtos": ["Tracer"], "mecanismo": "Ativador Alostérico", "observacao": "Produto nobre, alta eficiência e seletivo."}
                        ]
                    },
                    "Ácaro-rajado": {
                        "tipo": "Praga",
                        "nome_cientifico": "Tetranychus urticae",
                        "fases_criticas": ["R1-R5 (Veranicos)"],
                        "nivel_dano": "Sintomas visuais iniciais.",
                        "identificacao_campo": "Minúsculos pontos na face inferior. Teias visíveis em alta infestação.",
                        "sintomas": "Folhas bronzeadas/amareladas. Queda prematura.",
                        "manejo_quimico": [
                            {"ativo": "Abamectina", "grupo_quimico": "Avermectina", "sugestao_produtos": ["Vertimec"], "mecanismo": "Paralisia", "observacao": "Exige espalhante adesivo de qualidade. Não aplicar nas horas quentes."},
                            {"ativo": "Profpofite", "grupo_quimico": "Sulfito", "sugestao_produtos": ["Omite"], "mecanismo": "Inibidor Mitocondrial", "observacao": "Específico para ácaros. Ação de choque."}
                        ]
                    },
                    "Mosca-branca": {
                        "tipo": "Praga",
                        "nome_cientifico": "Bemisia tabaci",
                        "fases_criticas": ["R1 a R6"],
                        "nivel_dano": "Presença de ninfas e fumagina.",
                        "identificacao_campo": "Nuvens de insetos brancos ao balançar a planta. Ninfas 'escamas' no verso da folha.",
                        "sintomas": "Transmissão de virose (necrose da haste) e fumagina (folha preta).",
                        "manejo_quimico": [
                            {"ativo": "Acetamiprido + Piriproxifen", "grupo_quimico": "Neonic + Juvenóide", "sugestao_produtos": ["Trivor"], "mecanismo": "Sistêmico + Regulador", "observacao": "Mata o adulto e esteriliza os ovos."},
                            {"ativo": "Ciantraniliprole", "grupo_quimico": "Diamida", "sugestao_produtos": ["Benevia"], "mecanismo": "Muscular", "observacao": "Tecnologia de ponta. Alto custo, alta eficiência."}
                        ]
                    }
                },
                "Doencas": {
                    "Ferrugem-asiatica": {
                        "tipo": "Doença",
                        "nome_cientifico": "Phakopsora pachyrhizi",
                        "fases_criticas": ["R1 ao final"],
                        "nivel_dano": "Zero. Preventivo é Lei.",
                        "identificacao_campo": "Urediniosporos na face abaxial. Olhar contra a luz.",
                        "sintomas": "Desfolha rápida. Ciclo encurtado. Grão chocho.",
                        "manejo_quimico": [
                            {"ativo": "Mancozebe (Multissítio)", "grupo_quimico": "Ditiocarbamato", "sugestao_produtos": ["Unizeb Gold", "Manfil"], "mecanismo": "Multissítio", "observacao": "Nunca aplicar triazol/estrobilurina sem ele. Base da resistência."},
                            {"ativo": "Protioconazol + Bixafen", "grupo_quimico": "Triazol + Carboxamida", "sugestao_produtos": ["Fox Xpro"], "mecanismo": "Sistêmico", "observacao": "Padrão ouro atual. Curativo e residual."},
                            {"ativo": "Picoxistrobina + Ciproconazol", "grupo_quimico": "Estrobilurina + Triazol", "sugestao_produtos": ["Aproach Prima"], "mecanismo": "Respiração", "observacao": "Boa sistemicidade. Reforçar com Cobre ou Mancozebe."}
                        ]
                    },
                    "Mancha-alvo": {
                        "tipo": "Doença",
                        "nome_cientifico": "Corynespora cassiicola",
                        "fases_criticas": ["Fechamento das linhas"],
                        "nivel_dano": "Lesões no baixeiro exigem controle.",
                        "identificacao_campo": "Manchas circulares com anéis concêntricos (formato de alvo de tiro).",
                        "sintomas": "Desfolha do baixeiro. Resistente a muitos fungicidas.",
                        "manejo_quimico": [
                            {"ativo": "Fluxapiroxade + Piraclostrobina", "grupo_quimico": "Carboxamida", "sugestao_produtos": ["Orkestra"], "mecanismo": "SDHI", "observacao": "Referência para Mancha Alvo. Alto residual."},
                            {"ativo": "Protioconazol", "grupo_quimico": "Triazolintiona", "sugestao_produtos": ["Fox"], "mecanismo": "Ergosterol", "observacao": "O triazol mais eficiente para Corynespora."}
                        ]
                    },
                    "Mofo-branco": {
                        "tipo": "Doença",
                        "nome_cientifico": "Sclerotinia sclerotiorum",
                        "fases_criticas": ["R1 (Florada)"],
                        "nivel_dano": "Histórico da área + Clima frio/úmido.",
                        "identificacao_campo": "Micélio branco (algodão) na haste. Escleródios (bolinhas pretas) dentro da haste.",
                        "sintomas": "Podridão úmida da haste. Morte da planta acima da lesão.",
                        "manejo_quimico": [
                            {"ativo": "Fluazinam", "grupo_quimico": "Fenilpiridinilamina", "sugestao_produtos": ["Frowncide"], "mecanismo": "Desacoplador", "observacao": "Preventivo na florada (R1). Protege a flor caída."},
                            {"ativo": "Procimidona", "grupo_quimico": "Dicarboximida", "sugestao_produtos": ["Sumilex"], "mecanismo": "Divisão Celular", "observacao": "Antigo, mas muito eficiente. Cuidado com carência."}
                        ]
                    },
                    "Antracnose": {
                        "tipo": "Doença",
                        "nome_cientifico": "Colletotrichum truncatum",
                        "fases_criticas": ["Emergência", "R3-R5"],
                        "nivel_dano": "Monitoramento.",
                        "identificacao_campo": "Manchas negras nas nervuras e vagens. Vagem retorcida em forma de 'C'.",
                        "sintomas": "Abortamento de vagens e queda de folhas.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina + Ciproconazol", "grupo_quimico": "Estrobilurina", "sugestao_produtos": ["Priori Xtra"], "mecanismo": "Respiração", "observacao": "Estrobilurinas controlam bem antracnose."}
                        ]
                    },
                    "Nematoides": {
                        "tipo": "Doença",
                        "nome_cientifico": "Meloidogyne / Heterodera / Pratylenchus",
                        "fases_criticas": ["Todo o ciclo"],
                        "nivel_dano": "Análise de solo e raiz.",
                        "identificacao_campo": "Reboleiras de plantas amareladas/pequenas. Galhas nas raízes (Meloidogyne). Cistos brancos (Heterodera).",
                        "sintomas": "Raiz 'vassoura de bruxa'. Planta não responde a adubo.",
                        "manejo_quimico": [
                            {"ativo": "Abamectina (TS)", "grupo_quimico": "Avermectina", "sugestao_produtos": ["Avicta"], "mecanismo": "Paralisia", "observacao": "Tratamento de sementes é a única via eficiente quimicamente."},
                            {"ativo": "Bacillus subtilis + licheniformis", "grupo_quimico": "Biológico", "sugestao_produtos": ["Quartzo", "Presence"], "mecanismo": "Biofilme/Competição", "observacao": "Fundamental usar biológicos no sulco de plantio."}
                        ]
                    }
                }
            }
        },
        "Milho": {
            "nome_cientifico": "Zea mays",
            "fases_fenologicas": {
                "VE-V3": {
                    "fase": "Estabelecimento",
                    "foco": "Controle de Percevejo e Cigarrinha",
                    "visao_pratica": "O percevejo Barriga-verde injeta toxina aqui que causa o 'perfilhamento' ou planta dominada. A cigarrinha transmite o enfezamento agora, mas o sintoma só aparece na espiga. Tratamento de semente industrial é obrigatório.",
                    "alerta": "Lagarta do cartucho pode cortar planta rente ao solo (hábito de rosca)."
                },
                "V4-V8": {
                    "fase": "Definição Produtiva",
                    "foco": "Nitrogênio e Cartucho",
                    "visao_pratica": "Define-se o nº de fileiras da espiga. A ureia tem que ser aplicada até V5 para máximo aproveitamento. Lagarta do cartucho (Spodoptera) nessa fase é difícil: se entrar no cartucho, o controle cai para menos de 40%. Aplique quando ver 'folha raspada'.",
                    "alerta": "Mancha Branca (Phaeosphaeria) começa no baixeiro."
                },
                "VT-R1": {
                    "fase": "Pendoamento e Polinização",
                    "foco": "Fungicida e Polinização",
                    "visao_pratica": "Momento crítico para aplicação aérea de fungicida. Proteger a folha da espiga é garantir o enchimento. Cuidado com inseticidas que matam abelhas ou inimigos naturais na polinização.",
                    "alerta": "Pulgão do milho pode cobrir o pendão e impedir a liberação de pólen."
                },
                "R2-R6": {
                    "fase": "Enchimento",
                    "foco": "Sanidade de Grão",
                    "visao_pratica": "Se houve enfezamento, as espigas caem ou os grãos ficam frouxos. Podridões de colmo (Gibberella/Fusarium) aparecem agora, causando tombamento pré-colheita.",
                    "alerta": "Colheita com umidade alta favorece micotoxinas."
                }
            },
            "problemas": {
                "Pragas": {
                    "Cigarrinha-do-milho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Dalbulus maidis",
                        "fases_criticas": ["VE até V8"],
                        "nivel_dano": "Presença = Controle Imediato",
                        "identificacao_campo": "Pequena, branca/palha, aloja-se no cartucho. Foge lateralmente.",
                        "sintomas": "Transmite Molicutes (Enfezamento Pálido e Vermelho) e Raio Fino. Planta anã, espiga improdutiva.",
                        "manejo_quimico": [
                            {"ativo": "Imidacloprido", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Confidor", "Gaucho"], "mecanismo": "Sistêmico", "observacao": "Fundamental no TS. Via foliar tem baixo residual."},
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Orthene"], "mecanismo": "Contato", "observacao": "Adulticida de choque. Rotação necessária."},
                            {"ativo": "Isaria fumosorosea", "grupo_quimico": "Biológico", "sugestao_produtos": ["Challenger"], "mecanismo": "Fungo Entomopatogênico", "observacao": "Excelente para controle de ninfas e manejo de resistência."}
                        ]
                    },
                    "Lagarta-do-cartucho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Spodoptera frugiperda",
                        "fases_criticas": ["Todo ciclo (Principalmente V3-VT)"],
                        "nivel_dano": "20% de plantas com folhas raspadas.",
                        "identificacao_campo": "Y invertido na cabeça. 4 pontos no final do abdômen. Fica dentro do cartucho (fezes visíveis).",
                        "sintomas": "Folhas perfuradas, cartucho destruído, espiga comida.",
                        "manejo_quimico": [
                            {"ativo": "Espinetoram", "grupo_quimico": "Espinosina", "sugestao_produtos": ["Exalt"], "mecanismo": "Choque e Ingestão", "observacao": "Produto premium. Aplique antes da lagarta entrar no cartucho."},
                            {"ativo": "Lufenurom", "grupo_quimico": "Fisiológico", "sugestao_produtos": ["Match"], "mecanismo": "Inibidor de Quitina", "observacao": "Preventivo. Impede a lagarta de crescer."},
                            {"ativo": "Metomil", "grupo_quimico": "Carbamato", "sugestao_produtos": ["Lannate"], "mecanismo": "Choque", "observacao": "Para situações de desespero (lagarta grande)."}
                        ]
                    },
                    "Percevejo-barriga-verde": {
                        "tipo": "Praga",
                        "nome_cientifico": "Dichelops melacanthus",
                        "fases_criticas": ["VE a V4"],
                        "nivel_dano": "0.5 a 1 percevejo a cada 2 metros.",
                        "identificacao_campo": "Cinza com abdômen verde. Fica no colo da planta sob a palha.",
                        "sintomas": "Planta 'dominada', folhas transversais rasgadas, perfilhamento excessivo.",
                        "manejo_quimico": [
                            {"ativo": "Tiametoxam + Lambda", "grupo_quimico": "Neonic + Piretroide", "sugestao_produtos": ["Engeo Pleno"], "mecanismo": "Sistêmico", "observacao": "Aplicar no fim da tarde. Jato dirigido na base da planta."},
                            {"ativo": "Clotianidina", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Poncho"], "mecanismo": "TS", "observacao": "O melhor TS para percevejo."}
                        ]
                    },
                     "Pulgão-do-milho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Rhopalosiphum maidis",
                        "fases_criticas": ["VT (Pendoamento)"],
                        "nivel_dano": "Colônias cobrindo o pendão.",
                        "identificacao_campo": "Insetos esverdeados sugadores no pendão ou folhas novas.",
                        "sintomas": "Fumagina, má polinização (pendão estéril).",
                        "manejo_quimico": [
                            {"ativo": "Acetamiprido", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Mospilan"], "mecanismo": "Sistêmico", "observacao": "Específico para sugadores. Seletivo."}
                        ]
                    }
                },
                "Doencas": {
                    "Enfezamentos (Molicutes)": {
                        "tipo": "Doença",
                        "nome_cientifico": "Spiroplasma kunkelii",
                        "fases_criticas": ["Infecção cedo, sintoma tarde"],
                        "nivel_dano": "Preventivo (Controle do Vetor).",
                        "identificacao_campo": "Folhas avermelhadas ou amarelas nas bordas. Multiespigas improdutivas.",
                        "sintomas": "Queda de produção drástica. Encurtamento de internódios.",
                        "manejo_quimico": [
                            {"ativo": "Não existe curativo", "grupo_quimico": "-", "sugestao_produtos": ["Controle a Cigarrinha"], "mecanismo": "-", "observacao": "O foco é controlar a Cigarrinha (Vetor) e usar híbridos tolerantes."}
                        ]
                    },
                    "Mancha-branca": {
                        "tipo": "Doença",
                        "nome_cientifico": "Phaeosphaeria maydis",
                        "fases_criticas": ["V8 a VT"],
                        "nivel_dano": "Lesões no baixeiro.",
                        "identificacao_campo": "Manchas pálidas (brancas/secas) nas folhas inferiores.",
                        "sintomas": "Seca da folha. Perda de área fotossintética.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina + Ciproconazol", "grupo_quimico": "Estrobilurina + Triazol", "sugestao_produtos": ["Priori Xtra"], "mecanismo": "Sistêmico", "observacao": "Aplicação V8 (Pré-pendoamento) é essencial."},
                            {"ativo": "Mancozebe", "grupo_quimico": "Multissítio", "sugestao_produtos": ["Unizeb"], "mecanismo": "Contato", "observacao": "Ajuda no manejo de resistência."}
                        ]
                    },
                    "Cercosporiose": {
                        "tipo": "Doença",
                        "nome_cientifico": "Cercospora zeae-maydis",
                        "fases_criticas": ["VT em diante"],
                        "nivel_dano": "Alta severidade em híbridos suscetíveis.",
                        "identificacao_campo": "Manchas retangulares cinzas, paralelas às nervuras.",
                        "sintomas": "Queima total da folha. Grão leve.",
                        "manejo_quimico": [
                            {"ativo": "Propiconazol", "grupo_quimico": "Triazol", "sugestao_produtos": ["Tilt"], "mecanismo": "Ergosterol", "observacao": "Específico e eficiente para Cercospora."}
                        ]
                    },
                     "Podridoes-de-colmo": {
                        "tipo": "Doença",
                        "nome_cientifico": "Fusarium / Gibberella",
                        "fases_criticas": ["R5-R6 (Pré-colheita)"],
                        "nivel_dano": "Tombamento de plantas.",
                        "identificacao_campo": "Miolo do colmo rosado ou desintegrado. Planta quebra fácil.",
                        "sintomas": "Colheita difícil. Perda total da espiga no chão.",
                        "manejo_quimico": [
                            {"ativo": "Manejo Cultural", "grupo_quimico": "-", "sugestao_produtos": ["Potássio Adequado"], "mecanismo": "-", "observacao": "Não existe fungicida curativo para colmo. Evite alta densidade e excesso de N."}
                        ]
                    }
                }
            }
        }
    "Algodão": {
            "nome_cientifico": "Gossypium hirsutum",
            "fases_fenologicas": {
                "V1-V4": {
                    "fase": "Vegetativo Inicial",
                    "foco": "Raiz, Tripes e Regulador",
                    "visao_pratica": "O jogo do algodão é 'arquitetura'. Se a planta 'disparar' aqui por excesso de chuva ou N, você perde o baixeiro. Tripes nessa fase encarquilha a folha e atrasa o desenvolvimento. Comece o monitoramento do Bicudo nas bordaduras (iscas).",
                    "alerta": "Pulgão na fase inicial transmite viroses que ananicão a planta."
                },
                "B1 (Botão Floral)": {
                    "fase": "Esquadratura",
                    "foco": "Retenção de Botões (Bicudo)",
                    "visao_pratica": "Cada botão que cai é menos peso na colheita. O Bicudo entra agora para ovipositar nos botões. Se encontrar botão furado no chão, inicie a 'Bateria': 3 aplicações sequenciais (intervalo de 3 a 5 dias). O regulador de crescimento deve ser parcelado e contínuo.",
                    "alerta": "Lagarta das maçãs (Heliothis) ataca direto a estrutura reprodutiva."
                },
                "F1 (Florada)": {
                    "fase": "Florescimento",
                    "foco": "Mancha Ramulária e Cut-out",
                    "visao_pratica": "Definição de carga. O alvo principal vira a Ramulária (a 'ferrugem' do algodão). Aplicação de fungicida deve ser preventiva, rotacionando triazóis e estrobilurinas. Monitore o 'Cut-out' (nós acima da última flor branca) para saber quando a planta parou de vegetar.",
                    "alerta": "Mosca-branca na florada = mela na fibra (prejuízo industrial)."
                },
                "C1 (Maçãs)": {
                    "fase": "Enchimento de Maçãs",
                    "foco": "Qualidade de Fibra e Peso",
                    "visao_pratica": "Proteção das maçãs do ponteiro. O Bicudo migra para as maçãs se não houver botão. Percevejo manchador entra para estragar a fibra. O foco aqui é manter a folha sadia para encher a maçã.",
                    "alerta": "Apodrecimento de maçãs em baixadas úmidas."
                }
            },
            "problemas": {
                "Pragas": {
                    "Bicudo-do-algodoeiro": {
                        "tipo": "Praga",
                        "nome_cientifico": "Anthonomus grandis",
                        "fases_criticas": ["B1 (Botão) até Colheita"],
                        "nivel_dano": "Zero Tolerância. Praga Chave.",
                        "identificacao_campo": "Besouro cinza/negro com 'bico' longo. Botões com pontuações de oviposição ou alimentação (amarelam e caem).",
                        "sintomas": "Queda massiva de botões florais (botoeira no chão). Maçãs 'carimã' (não abrem).",
                        "manejo_quimico": [
                            {"ativo": "Malationa", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Malathion"], "mecanismo": "Acetilcolinesterase", "observacao": "Padrão para baterias de choque e final de ciclo."},
                            {"ativo": "Fipronil", "grupo_quimico": "Pirazol", "sugestao_produtos": ["Regent"], "mecanismo": "GABA (Cloro)", "observacao": "Excelente residual. Usar no início (esquadratura)."},
                            {"ativo": "Beta-ciflutrina", "grupo_quimico": "Piretroide", "sugestao_produtos": ["Bulldock"], "mecanismo": "Modulador de Sódio", "observacao": "Efeito de choque rápido ('Knock-down')."}
                        ]
                    },
                    "Pulgão-do-algodoeiro": {
                        "tipo": "Praga",
                        "nome_cientifico": "Aphis gossypii",
                        "fases_criticas": ["V1-V4 (Virose) e Final (Mela)"],
                        "nivel_dano": "Colônias visíveis ou presença de virose.",
                        "identificacao_campo": "Insetos pequenos escuros/verdes na face inferior. Folha encarquilhada 'conchinha'.",
                        "sintomas": "Transmissão do Vírus do Mosaico das Nervuras. Mela da fibra na colheita.",
                        "manejo_quimico": [
                            {"ativo": "Carbosulfano", "grupo_quimico": "Carbamato", "sugestao_produtos": ["Marshal"], "mecanismo": "Sistêmico", "observacao": "Ação rápida. Cuidado com inimigos naturais."},
                            {"ativo": "Flonicamida", "grupo_quimico": "Piridinacarboxamida", "sugestao_produtos": ["Turbine"], "mecanismo": "Bloqueio Alimentar", "observacao": "Específico e seletivo. Ótimo para rotação."}
                        ]
                    },
                    "Ácaro-branco": {
                        "tipo": "Praga",
                        "nome_cientifico": "Polyphagotarsonemus latus",
                        "fases_criticas": ["Todo o ciclo"],
                        "nivel_dano": "Folhas do ponteiro deformadas.",
                        "identificacao_campo": "Invisível a olho nu. Folhas novas ficam 'envernizadas' e rasgadas nas bordas.",
                        "sintomas": "Paralisação do crescimento do ponteiro. Aspecto coriáceo.",
                        "manejo_quimico": [
                            {"ativo": "Abamectina", "grupo_quimico": "Avermectina", "sugestao_produtos": ["Vertimec"], "mecanismo": "Paralisia", "observacao": "Padrão. Exige cobertura perfeita."},
                            {"ativo": "Diafentiurom", "grupo_quimico": "Tioureia", "sugestao_produtos": ["Polo"], "mecanismo": "Respiração", "observacao": "Ação gasosa (fumigante). Funciona bem no calor."}
                        ]
                    }
                },
                "Doencas": {
                    "Ramularia": {
                        "tipo": "Doença",
                        "nome_cientifico": "Ramularia areola",
                        "fases_criticas": ["B1 em diante"],
                        "nivel_dano": "Lesões no baixeiro. Preventivo obrigatório.",
                        "identificacao_campo": "Manchas angulares brancas/azuladas (parece talco) nas duas faces da folha.",
                        "sintomas": "Desfolha total precoce. Abertura forçada de capulhos.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina + Difenoconazol", "grupo_quimico": "Estrobilurina + Triazol", "sugestao_produtos": ["Priori Top"], "mecanismo": "Sistêmico Duplo", "observacao": "Referência de mercado. Alternar com Carboxamidas."},
                            {"ativo": "Clorotalonil", "grupo_quimico": "Multissítio", "sugestao_produtos": ["Bravonil"], "mecanismo": "Contato", "observacao": "Obrigatório adicionar para evitar resistência."}
                        ]
                    },
                    "Mancha-alvo": {
                        "tipo": "Doença",
                        "nome_cientifico": "Corynespora cassiicola",
                        "fases_criticas": ["Fechamento"],
                        "nivel_dano": "Alta severidade em cultivares suscetíveis.",
                        "identificacao_campo": "Manchas circulares com anéis (alvo).",
                        "sintomas": "Desfolha rápida do baixeiro.",
                        "manejo_quimico": [
                            {"ativo": "Fluxapiroxade + Piraclostrobina", "grupo_quimico": "Carboxamida", "sugestao_produtos": ["Orkestra"], "mecanismo": "SDHI", "observacao": "Melhor performance para alvo."}
                        ]
                    }
                }
            }
        },
        "Arroz": {
            "nome_cientifico": "Oryza sativa",
            "fases_fenologicas": {
                "V1-V4": {
                    "fase": "Plântula e Perfilhamento",
                    "foco": "Água e Nitrogênio",
                    "visao_pratica": "A adubação nitrogenada de cobertura deve ser feita em solo seco, imediatamente antes da entrada da água (inundação). Isso garante que o N não volatilize. O número de perfilhos define o número de panículas futuras.",
                    "alerta": "Bicheira-da-raiz reduz drasticamente o stand se não houver tratamento de semente."
                },
                "R1 (Ponto de Algodão)": {
                    "fase": "Diferenciação da Panícula",
                    "foco": "Proteção da Bainha",
                    "visao_pratica": "Ponto crítico! A planta define o tamanho da espiga. Início das aplicações preventivas para Brusone e Queima-da-bainha. Não deixe faltar água na lâmina de irrigação agora.",
                    "alerta": "Lagarta-da-panícula pode cortar a base da espiga."
                },
                "R4 (Florada)": {
                    "fase": "Antese",
                    "foco": "Brusone do Pescoço",
                    "visao_pratica": "Se a Brusone entrar no pescoço da panícula agora, a espiga fica branca e vazia (chocha). A aplicação de Triciclazol deve ser preventiva, antes da panícula emitir totalmente.",
                    "alerta": "Temperaturas abaixo de 17°C na florada causam esterilidade (chochamento por frio)."
                },
                "R8 (Maturação)": {
                    "fase": "Grão",
                    "foco": "Percevejo do Grão",
                    "visao_pratica": "O percevejo (Oebalus) pica o grão leitoso, causando o 'arroz gessado' e manchado, que perde valor comercial no engenho. Drenagem da lavoura deve ser planejada para permitir colheita.",
                    "alerta": "Excesso de N tardio favorece doenças e acamamento."
                }
            },
            "problemas": {
                "Pragas": {
                    "Bicheira-da-raiz": {
                        "tipo": "Praga",
                        "nome_cientifico": "Oryzophagus oryzae",
                        "fases_criticas": ["Logo após inundação"],
                        "nivel_dano": "Larvas nas raízes.",
                        "identificacao_campo": "Plantas amareladas no meio da lâmina d'água. Raízes podadas/comidas.",
                        "sintomas": "Planta solta fácil do solo. Perda de perfilhos.",
                        "manejo_quimico": [
                            {"ativo": "Fipronil", "grupo_quimico": "Pirazol", "sugestao_produtos": ["Standak"], "mecanismo": "GABA", "observacao": "TS é o padrão. Aplicação na água é curativa mas difícil."},
                            {"ativo": "Clorantraniliprole", "grupo_quimico": "Diamida", "sugestao_produtos": ["Dermacor"], "mecanismo": "Muscular", "observacao": "Excelente seletividade e residual no TS."}
                        ]
                    },
                    "Percevejo-do-arroz": {
                        "tipo": "Praga",
                        "nome_cientifico": "Oebalus poecilus",
                        "fases_criticas": ["R4 a R8 (Leitoso)"],
                        "nivel_dano": "1 percevejo a cada 10 batidas de rede.",
                        "identificacao_campo": "Percevejo marrom com manchas amarelas nas 'costas' (escudete).",
                        "sintomas": "Grão picado (mancha preta) e gessado (quebra no benefício).",
                        "manejo_quimico": [
                            {"ativo": "Lambda-cialotrina + Tiametoxam", "grupo_quimico": "Piretroide + Neonic", "sugestao_produtos": ["Engeo Pleno"], "mecanismo": "Choque + Residual", "observacao": "Aplicação aérea comum em pré-colheita."},
                            {"ativo": "Dinotefuran", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Starkle"], "mecanismo": "Sistêmico", "observacao": "Alta solubilidade e eficiência."}
                        ]
                    }
                },
                "Doencas": {
                    "Brusone": {
                        "tipo": "Doença",
                        "nome_cientifico": "Magnaporthe oryzae",
                        "fases_criticas": ["V4 (Folha) e R4 (Pescoço)"],
                        "nivel_dano": "Principal doença. Pode dar 100% de perda.",
                        "identificacao_campo": "Folha: mancha em forma de 'olho' (centro cinza, borda marrom). Pescoço: necrose escura na base da panícula.",
                        "sintomas": "Quebra do pescoço, panícula branca e ereta (sem peso).",
                        "manejo_quimico": [
                            {"ativo": "Triciclazol", "grupo_quimico": "Redutase", "sugestao_produtos": ["Bim", "Sifra"], "mecanismo": "Sistêmico Preventivo", "observacao": "O padrão mundial. Deve ser aplicado ANTES da doença. Não tem ação curativa forte."},
                            {"ativo": "Kasugamicina", "grupo_quimico": "Antibiótico", "sugestao_produtos": ["Kasumin"], "mecanismo": "Síntese Proteica", "observacao": "Curativo e erradicante. Usar se a doença já entrou."}
                        ]
                    },
                    "Queima-da-bainha": {
                        "tipo": "Doença",
                        "nome_cientifico": "Rhizoctonia solani",
                        "fases_criticas": ["Emborrachamento"],
                        "nivel_dano": "Lesões subindo a bainha.",
                        "identificacao_campo": "Manchas ovais branco-acinzentadas com bordas escuras na linha d'água.",
                        "sintomas": "Seca das folhas e acamamento da planta.",
                        "manejo_quimico": [
                            {"ativo": "Azoxistrobina", "grupo_quimico": "Estrobilurina", "sugestao_produtos": ["Priori"], "mecanismo": "Respiração", "observacao": "Melhor grupo para Rhizoctonia."},
                            {"ativo": "Thifluzamida", "grupo_quimico": "Carboxamida", "sugestao_produtos": ["Pulsor"], "mecanismo": "SDHI", "observacao": "Específico e altamente eficaz."}
                        ]
                    }
                }
            }
        }
    }
