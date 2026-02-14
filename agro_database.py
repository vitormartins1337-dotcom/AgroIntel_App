# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI (Database Especializada em Cannabis)
# FONTES: Jorge Cervantes, Ed Rosenthal, High Times, Leafly.

def get_agro_db():
    return {
        "Cannabis Indica (Fotoperíodo)": {
            "descricao": "Plantas baixas, arbustivas, folhas largas e escuras. Ciclo de floração rápido. Efeito corporal (Body High).",
            "geneticas_famosas": ["OG Kush", "Northern Lights", "Granddaddy Purple", "Afghan Kush"],
            "manejo_grow": {
                "luz": "Vegetativo: 18/6h. Floração: 12/12h (Estrito). Vazamento de luz causa hermafroditismo.",
                "clima_ideal": "Temp: 20-25°C. Umidade: 40-50% na Floração (Evitar Botrytis em buds densos).",
                "nutricao": "Exige mais Magnésio (Mg) e Fósforo (P) na floração. Aguenta EC mais alto (1.8 - 2.2).",
                "treinamento": "Aceita bem podas (Topping/FIM) e LST para abrir a estrutura compacta.",
                "colheita": "7 a 9 semanas de floração. Tricomas: 20% Âmbar / 80% Leitoso para efeito sedativo."
            },
            "ciclo_vida": {
                "Germinação (1-2 semanas)": {
                    "foco": "Raiz e Umidade",
                    "detalhe": "Escuro total e úmido. Domo de umidade a 70-80%. Luz fraca (PPFD < 200).",
                    "alerta": "Damping-off (tombamento) é fatal aqui. Não encharque o substrato."
                },
                "Vegetativo (4-8 semanas)": {
                    "foco": "Estrutura e Nitrogênio",
                    "detalhe": "Crescimento explosivo. Foco em N. PPFD: 400-600. Hora de fazer transplante e podas.",
                    "alerta": "Deficiência de Cal-Mag aparece como manchas de ferrugem."
                },
                "Floração (7-9 semanas)": {
                    "foco": "Engorda e Terpenos",
                    "detalhe": "Stretch (estirão) nas primeiras 2 semanas. Foco em P e K. Reduzir umidade para <50%.",
                    "alerta": "Mofo (Botrytis) nos buds centrais. Monitorar ventilação."
                },
                "Flush & Cura": {
                    "foco": "Limpeza de Sais",
                    "detalhe": "Regar apenas com água pH ajustado nas últimas 2 semanas. Secagem no escuro (18°C/60% UR).",
                    "alerta": "Secagem muito rápida deixa gosto de clorofila (feno)."
                }
            },
            "problemas": {
                "Pragas": {
                    "Spider Mites (Ácaro-rajado)": {
                        "tipo": "Praga",
                        "identificacao": "Pontinhos brancos nas folhas. Teias nos buds em casos graves.",
                        "dano": "Suga a seiva, trava o crescimento e inutiliza a flor (teia).",
                        "solucao": ["Óleo de Neem (Veg)", "Abamectina (Apenas Veg Inicial)", "Predadores (Phytoseiulus)"],
                        "obs": "Nunca aplicar óleo nas flores."
                    },
                    "Fungus Gnats": {
                        "tipo": "Praga",
                        "identificacao": "Mosquitinhos pretos voando no solo. Larvas brancas na terra.",
                        "dano": "Larvas comem a raiz capilar. Porta de entrada para Fusarium.",
                        "solucao": ["Terra de Diatomáceas", "BTI (Bacillus thuringiensis israelensis)", "Armadilhas Amarelas"],
                        "obs": "Deixar o solo secar entre regas."
                    }
                },
                "Doencas": {
                    "Powdery Mildew (Oídio)": {
                        "tipo": "Fungo",
                        "identificacao": "Pó branco (parece farinha) nas folhas.",
                        "dano": "Bloqueia fotossíntese. Impróprio para consumo.",
                        "solucao": ["Bicarbonato de Potássio", "Peróxido de Hidrogênio", "Controle de Umidade"],
                        "obs": "VPD desajustado favorece o Oídio."
                    },
                    "Botrytis (Bud Rot)": {
                        "tipo": "Fungo",
                        "identificacao": "Bud fica marrom/cinza, mole e se desfaz.",
                        "dano": "Perda total da flor atingida.",
                        "solucao": ["Remover o bud com saco plástico", "Melhorar ventilação", "Desumidificador"],
                        "obs": "Ocorre muito em Indicas densas com umidade alta."
                    }
                }
            }
        },
        "Cannabis Sativa (Fotoperíodo)": {
            "descricao": "Plantas altas, esguias, folhas finas. Floração longa (10-14 semanas). Efeito cerebral e energético.",
            "geneticas_famosas": ["Sour Diesel", "Jack Herer", "Amnesia Haze", "Durban Poison"],
            "manejo_grow": {
                "luz": "Exige muita luz (PPFD 800-1000 na flora). Cuidado com altura da lâmpada (queima de topo).",
                "clima_ideal": "Aguenta mais calor (24-28°C) e umidade tropical, mas prefere ar circulante.",
                "nutricao": "Menos exigente em EC que a Indica (cuidado com overfert de Nitrogênio na flora).",
                "treinamento": "SCROG (Tela) é obrigatório indoor para controlar a altura.",
                "colheita": "Paciência. Colher cedo perde a potência e o perfil de terpenos."
            },
            "ciclo_vida": {
                "Germinação": {"foco": "Raiz", "detalhe": "Igual à Indica.", "alerta": "Cuidado com excesso de água."},
                "Vegetativo": {"foco": "Controle de Altura", "detalhe": "Cresce muito rápido. Podar cedo.", "alerta": "Espaço vertical acaba rápido."},
                "Floração (Longa)": {"foco": "Paciência", "detalhe": "Pode triplicar de tamanho no stretch. Flores são mais aeradas (Fox tails).", "alerta": "Hermafroditismo por stress de luz."},
                "Flush": {"foco": "Sabor", "detalhe": "Flush longo (2 semanas) essencial para Hazes.", "alerta": "-"}
            },
            "problemas": {
                 "Pragas": {
                    "Thrips (Tripes)": {
                        "tipo": "Praga",
                        "identificacao": "Manchas prateadas na folha. Inseto palito minúsculo.",
                        "dano": "Deforma folhas novas. Vetor de vírus.",
                        "solucao": ["Spinosad", "Sabão Potássico", "Armadilhas Azuis"],
                        "obs": "Resistente a muitos químicos."
                    }
                 },
                 "Doencas": {
                     "Fusarium": {
                         "tipo": "Fungo",
                         "identificacao": "Murcha súbita de um galho ou da planta toda. Haste marrom por dentro.",
                         "dano": "Morte da planta.",
                         "solucao": ["Trichoderma (Preventivo)", "Eliminar planta doente"],
                         "obs": "Não tem cura. Higienizar tudo."
                     }
                 }
            }
        },
        "Cannabis Ruderalis (Automática)": {
            "descricao": "Cruza com genética siberiana. Floresce por idade, não por luz. Ciclo total curtíssimo (60-80 dias).",
            "geneticas_famosas": ["Gorilla Glue Auto", "Girl Scout Cookies Auto", "Magnum Auto"],
            "manejo_grow": {
                "luz": "Ciclo contínuo de 20/4h ou 18/6h do início ao fim. Mais luz = Mais peso.",
                "clima_ideal": "Estável. Qualquer stress trava a planta e ela fica anã.",
                "nutricao": "Come pouco! Use 1/2 ou 1/4 da dose recomendada para fotoperíodos.",
                "treinamento": "NÃO FAZER PODAS DE ALTO ESTRESS (Topping). Apenas LST (amarras).",
                "colheita": "Rápida. Ciclo total de 2 a 3 meses."
            },
            "ciclo_vida": {
                "Ciclo Único": {
                    "foco": "Não travar",
                    "detalhe": "Você tem 3 semanas de vegetativo. Se errar aqui, a planta floresce com 10cm de altura.",
                    "alerta": "Transplantes não recomendados. Plantar no vaso final."
                }
            },
            "problemas": {
                "Pragas": {
                    "Minadora (Leaf Miner)": {
                        "tipo": "Praga",
                        "identificacao": "Caminhos (minas) brancos nas folhas.",
                        "dano": "Estético e fotossintético.",
                        "solucao": ["Apertar a larva na folha", "Óleo de Neem"],
                        "obs": "Em autos, perder folha é perder energia."
                    }
                },
                "Doencas": {
                     "Overfert (Excesso de Nutrientes)": {
                         "tipo": "Fisiológico",
                         "identificacao": "Pontas das folhas queimadas (Garra de águia). Folhas verde escuro brilhante.",
                         "dano": "Bloqueio de nutrientes (Lockout).",
                         "solucao": ["Flush imediato", "Reduzir EC"],
                         "obs": "Erro número 1 em automáticas."
                     }
                }
            }
        }
    }
