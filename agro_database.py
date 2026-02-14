# ARQUIVO: agro_database.py
# VERSÃO: V-NATIVE-DB-1.0
# DESCRIÇÃO: Banco de dados local para operação OFFLINE.

def get_agro_db():
    """
    Retorna a estrutura completa de dados do aplicativo.
    Em um app nativo (Flutter/React Native), isso seria um arquivo JSON ou SQLite local.
    """
    return {
        "Soja": {
            "nome_cientifico": "Glycine max",
            "fases_fenologicas": {
                "VE-V2": "Emergência e Estabelecimento",
                "V3-V6": "Desenvolvimento Vegetativo",
                "R1-R2": "Florescimento",
                "R3-R5": "Formação de Vagens e Enchimento",
                "R6-R8": "Maturação Plena"
            },
            # AQUI ESTÁ O OURO: A ENCICLOPÉDIA DE MANEJO
            "problemas": {
                "Pragas": {
                    "Percevejo-marrom": {
                        "nome_cientifico": "Euschistus heros",
                        "fases_criticas": ["R3-R5", "R6-R8"],
                        "nivel_dano": "2 percevejos/metro (Grão) | 1 percevejo/metro (Semente)",
                        "identificacao_campo": "Adulto de cor marrom-escuro, com dois espinhos laterais no pronoto. Ovos amarelos em pequenas massas.",
                        "sintomas": "Picada nas vagens causando grãos 'chupados', retenção foliar (soja louca) e perda de vigor da semente.",
                        "manejo_quimico": [
                            {
                                "grupo_quimico": "Neonicotinoide + Piretroide",
                                "ativo": "Tiametoxam + Lambda-cialotrina",
                                "mecanismo": "Moduladores de canais de sódio e Agonistas de acetilcolina.",
                                "sugestao_produtos": ["Engeo Pleno", "Kaiso", "Zeus"],
                                "observacao": "Alta eficiência de choque. Cuidado com populações resistentes."
                            },
                            {
                                "grupo_quimico": "Organofosforado",
                                "ativo": "Acefato",
                                "mecanismo": "Inibidores da Acetilcolinesterase.",
                                "sugestao_produtos": ["Orthene", "Perito"],
                                "observacao": "Uso estratégico para rotação. Cheiro forte. Evitar em horários quentes."
                            }
                        ]
                    },
                    "Lagarta-falsa-medideira": {
                        "nome_cientifico": "Rachiplusia nu",
                        "fases_criticas": ["V3-V6", "R1-R2"],
                        "nivel_dano": "30% desfolha (Veg) | 15% desfolha (Reprod)",
                        "identificacao_campo": "Desloca-se medindo palmos. Coloração verde-claro com listras longitudinais brancas.",
                        "sintomas": "Desfolha preservando as nervuras. Começa do baixeiro para o topo.",
                        "manejo_quimico": [
                            {
                                "grupo_quimico": "Diamidas",
                                "ativo": "Clorantraniliprole",
                                "mecanismo": "Moduladores dos receptores de Rianodina.",
                                "sugestao_produtos": ["Premio", "Coragen"],
                                "observacao": "Longo residual. Excelente para proteção do baixeiro."
                            },
                            {
                                "grupo_quimico": "Benzoilureias (Fisiológico)",
                                "ativo": "Diflubenzuron",
                                "mecanismo": "Inibidores da síntese de quitina.",
                                "sugestao_produtos": ["Dimilin", "Diflusect"],
                                "observacao": "Aplicar em lagartas pequenas (<1.5cm). Não tem efeito de choque."
                            }
                        ]
                    }
                },
                "Doencas": {
                    "Ferrugem-asiatica": {
                        "nome_cientifico": "Phakopsora pachyrhizi",
                        "fases_criticas": ["R1-R2", "R3-R5", "R6-R8"],
                        "nivel_dano": "Monitoramento constante. Aplicação preventiva é mandatória.",
                        "identificacao_campo": "Pequenos pontos escuros (urédias) na face inferior da folha. Contra a luz, vê-se saliências.",
                        "sintomas": "Clorose e queda prematura das folhas. Ciclo encurtado.",
                        "manejo_quimico": [
                            {
                                "grupo_quimico": "Triazol + Estrobilurina",
                                "ativo": "Ciproconazol + Azoxistrobina",
                                "mecanismo": "Inibidores da desmetilação e respiração mitocondrial.",
                                "sugestao_produtos": ["Priori Xtra"],
                                "observacao": "Padrão preventivo. Sempre adicionar multissítio (Mancozebe/Clorotalonil)."
                            },
                            {
                                "grupo_quimico": "Carboxamida + Protioconazol",
                                "ativo": "Bixafen + Protioconazol",
                                "mecanismo": "Inibidores da succinato desidrogenase.",
                                "sugestao_produtos": ["Fox Xpro"],
                                "observacao": "Alta eficácia curativa e residual. Tecnologia premium."
                            }
                        ]
                    }
                }
            }
        },
        "Milho": {
            "nome_cientifico": "Zea mays",
            "fases_fenologicas": {
                "VE-V3": "Estabelecimento",
                "V4-V8": "Definição de Produção",
                "VT-R1": "Pendoamento e Polinização",
                "R2-R6": "Enchimento de Grãos"
            },
            "problemas": {
                "Pragas": {
                    "Cigarrinha-do-milho": {
                        "nome_cientifico": "Dalbulus maidis",
                        "fases_criticas": ["VE-V3", "V4-V8"],
                        "nivel_dano": "Presença da praga exige controle (Vetor de Enfezamentos).",
                        "identificacao_campo": "Pequeno inseto branco-palha (3-4mm), aloja-se no cartucho ou base da folha. Foge rápido.",
                        "sintomas": "Transmissão de molicutes (Enfezamento Pálido e Vermelho). Plantas anãs e espigas improdutivas.",
                        "manejo_quimico": [
                            {
                                "grupo_quimico": "Neonicotinoide",
                                "ativo": "Imidacloprido",
                                "mecanismo": "Agonista de acetilcolina.",
                                "sugestao_produtos": ["Confidor", "ImidaGold"],
                                "observacao": "Tratamento de sementes é fundamental. Aplicação foliar em V2 e V4."
                            },
                            {
                                "grupo_quimico": "Carbamato",
                                "ativo": "Metomil",
                                "mecanismo": "Inibidor de acetilcolinesterase.",
                                "sugestao_produtos": ["Lannate"],
                                "observacao": "Apenas para choque em altas infestações (adulticidas)."
                            }
                        ]
                    }
                }
            }
        }
    }
