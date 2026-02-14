# ARQUIVO: agro_database.py
# BANCO DE DADOS COM VISÃO DE CAMPO (20 ANOS DE EXPERIÊNCIA)

def get_agro_db():
    return {
        "Soja": {
            "nome_cientifico": "Glycine max",
            "fases_fenologicas": {
                "VE-V2": {
                    "fase": "Emergência e Estabelecimento",
                    "foco": "Stand de Plantas e Raiz",
                    "visao_pratica": "O jogo começa aqui. O foco não é parte aérea, é raiz. Verifique a profundidade da semente. Se houver tombamento (Damping-off), o tratamento de semente falhou. Não aplique glifosato com a planta estressada ou 'melada'.",
                    "alerta": "Lagarta Elasmo em solo seco corta o colo da planta."
                },
                "V3-V6": {
                    "fase": "Desenvolvimento Vegetativo",
                    "foco": "Construção Produtiva e Nodulação",
                    "visao_pratica": "Fase crítica para fitotoxidez. Herbicida mal posicionado aqui 'trava' a soja e encurta os nós. Arranque uma planta: se tiver menos de 10 nódulos rosados no interior, a FBN falhou e precisa de reforço de N ou cobalto/molibdênio via folha.",
                    "alerta": "Entrada preventiva de fungicida multissítio junto com o glifosato."
                },
                "R1-R2": {
                    "fase": "Florescimento Pleno",
                    "foco": "Definição de Vagens",
                    "visao_pratica": "A planta muda a chave metabólica. Proibido entrar com trator se não for estritamente necessário (amassamento causa perda direta). O abortamento de flores é normal, mas seca excessiva exige bioestimulante anti-estresse.",
                    "alerta": "Start do programa pesado de fungicidas. O que perder de folha agora, não recupera."
                },
                "R3-R5": {
                    "fase": "Formação e Enchimento",
                    "foco": "Peso de Grão (T.G.W)",
                    "visao_pratica": "O dreno de potássio é violento. Se faltou K na base, a folha 'queima' a borda agora. Monitoramento de percevejo tem que ser diário: 1 percevejo aqui faz estrago irreversível (grão picado/chupado).",
                    "alerta": "Ferrugem Asiática costuma explodir no baixeiro nesta fase."
                },
                 "R6-R8": {
                    "fase": "Maturação",
                    "foco": "Qualidade de Semente/Grão",
                    "visao_pratica": "Dessecação antecipada gera grão verde e desconto no armazém. O ponto ideal é quando 95% das vagens estão marrons. Cuidado com chuva na colheita (grão ardido).",
                    "alerta": "Percevejo nessa fase ataca direto o grão, reduzindo peso e vigor."
                }
            },
            "problemas": {
                "Pragas": {
                    "Percevejo-marrom": {
                        "tipo": "Praga",
                        "nome_cientifico": "Euschistus heros",
                        "fases_criticas": ["R3", "R4", "R5"],
                        "nivel_dano": "2/metro (Grão) | 0.5/metro (Semente)",
                        "identificacao_campo": "O mais difícil de controlar. Esconde-se na palhada nas horas quentes.",
                        "sintomas": "Retenção foliar (haste verde/soja louca) e grãos deformados.",
                        "manejo_quimico": [
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Perito", "Orthene"], "mecanismo": "Choque", "observacao": "Cheiro forte. Ideal para baixar população rápido."},
                            {"ativo": "Tiametoxam + Lambda", "grupo_quimico": "Neonic + Piretroide", "sugestao_produtos": ["Engeo Pleno", "Kaiso"], "mecanismo": "Sistêmico + Contato", "observacao": "Padrão de mercado. Cuidado com resistência."}
                        ]
                    },
                    "Lagarta-falsa-medideira": {
                        "tipo": "Praga",
                        "nome_cientifico": "Rachiplusia nu",
                        "fases_criticas": ["V3-R2"],
                        "nivel_dano": "30% desfolha (Veg)",
                        "identificacao_campo": "Verde clara com listras brancas. Anda 'medindo palmo'.",
                        "sintomas": "Raspa as folhas deixando as nervuras. Começa de baixo para cima.",
                        "manejo_quimico": [
                            {"ativo": "Clorantraniliprole", "grupo_quimico": "Diamida", "sugestao_produtos": ["Premio", "Coragen"], "mecanismo": "Ingestão", "observacao": "O melhor residual do mercado. Protege o baixeiro."},
                            {"ativo": "Metomil", "grupo_quimico": "Carbamato", "sugestao_produtos": ["Lannate"], "mecanismo": "Choque", "observacao": "Apenas para 'apagar incêndio'. Baixo residual."}
                        ]
                    }
                },
                "Doencas": {
                    "Ferrugem-asiatica": {
                        "tipo": "Doença",
                        "nome_cientifico": "Phakopsora pachyrhizi",
                        "fases_criticas": ["R1 em diante"],
                        "nivel_dano": "Zero tolerância. Preventivo obrigatório.",
                        "identificacao_campo": "Pontos escuros na face inferior. Olhando contra o sol, vê-se saliências.",
                        "sintomas": "Queda prematura das folhas. A lavoura 'acelera' e morre antes da hora.",
                        "manejo_quimico": [
                            {"ativo": "Mancozebe (Multissítio)", "grupo_quimico": "Ditiocarbamato", "sugestao_produtos": ["Unizeb Gold"], "mecanismo": "Multissítio", "observacao": "Obrigatório em todas as aplicações para evitar resistência."},
                            {"ativo": "Protioconazol + Bixafen", "grupo_quimico": "Triazolintiona + Carboxamida", "sugestao_produtos": ["Fox Xpro"], "mecanismo": "Sistêmico", "observacao": "Tecnologia premium com força curativa e residual."}
                        ]
                    }
                }
            }
        },
        "Milho": {
            "nome_cientifico": "Zea mays",
            "fases_fenologicas": {
                "V4-V6": {
                    "fase": "Definição Produtiva",
                    "foco": "Número de Fileiras na Espiga",
                    "visao_pratica": "É aqui que se define se a espiga vai ter 14, 16 ou 18 fileiras. O Nitrogênio de cobertura tem que estar disponível na boca da planta AGORA. Atrasar a ureia aqui é jogar dinheiro fora.",
                    "alerta": "Percevejo Barriga-verde pode 'charutar' o milho nesta fase."
                },
                "VT-R1": {
                    "fase": "Pendoamento",
                    "foco": "Polinização",
                    "visao_pratica": "Fase mais sensível à seca. Se faltar água 1 semana aqui, perde 50% da produção. Aplicação de fungicida com avião é recomendada para proteger as folhas do terço superior.",
                    "alerta": "Pulgão do milho pode sugar a vitalidade do pendão."
                }
            },
            "problemas": {
                 "Pragas": {
                    "Cigarrinha-do-milho": {
                        "tipo": "Praga",
                        "nome_cientifico": "Dalbulus maidis",
                        "fases_criticas": ["VE-V8"],
                        "nivel_dano": "Presença = Controle",
                        "identificacao_campo": "Branquinha, foge rápido. Fica no cartucho.",
                        "sintomas": "Enfezamentos (Vermelho/Pálido). Planta não cresce e espiga cai.",
                        "manejo_quimico": [
                            {"ativo": "Imidacloprido", "grupo_quimico": "Neonicotinoide", "sugestao_produtos": ["Confidor", "Gaucho"], "mecanismo": "Sistêmico", "observacao": "Tratamento de sementes é a base de tudo."},
                            {"ativo": "Acefato", "grupo_quimico": "Organofosforado", "sugestao_produtos": ["Orthene"], "mecanismo": "Contato", "observacao": "Rotação para matar adultos."}
                        ]
                    }
                 },
                 "Doencas": {}
            }
        }
    }
