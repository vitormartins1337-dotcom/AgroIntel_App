# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | MASTER GENETICS DATABASE
# FONTE: Breeders Oficiais, Leafly, SeedFinder.

def get_agro_db():
    return {
        "📚 BOTÂNICA & SEXAGEM": {
            "tipos": {
                "Fêmea (Sinsemilla)": {
                    "descricao": "O objetivo de todo grower. Produz as flores resinosas ricas em canabinoides (THC/CBD).",
                    "identificacao": "Pistilos (pelinhos brancos) saindo das brácteas nos nós entre o caule e o galho.",
                    "funcao": "Produção de medicina e sementes (se polinizada).",
                    "imagem_ref": "Buscando pistilos em forma de 'V'."
                },
                "Macho": {
                    "descricao": "Produtor de pólen. Essencial para breeding (criação de novas seeds), mas inimigo do cultivo de flores.",
                    "identificacao": "Sacos de pólen (bolinhas) agrupados nos nós. Parecem cachos de uva minúsculos.",
                    "funcao": "Polinizar fêmeas.",
                    "alerta": "Se abrir o saco de pólen, uma única planta macho pode estragar (semear) a colheita de uma estufa inteira."
                },
                "Hermafrodita (Hermie)": {
                    "descricao": "Pesadelo do grower. Planta que desenvolve ambos os sexos, geralmente por estresse (luz, calor).",
                    "identificacao": "Estruturas amarelas em forma de 'banana' (nanners) saindo de dentro da flor fêmea.",
                    "acao": "Corte imediato ou remoção cirúrgica das 'bananas' com pinça e água.",
                    "causa": "Vazamento de luz no período noturno ou genética instável."
                }
            }
        },
        "🧬 GENÉTICAS REAIS (CATÁLOGO MASTER)": {
            "Indica Dominante": {
                "Granddaddy Purple": {
                    "banco": "Ken Estes",
                    "thc": "20-27%", "cbd": "<1%",
                    "terpenos": ["Mirceno", "Pineno", "Cariofileno"],
                    "sabor": "Uva, Frutas Vermelhas, Doce.",
                    "efeito": "Sedação pesada, relaxamento muscular, sono.",
                    "medicinal": "Insônia, Dor Crônica, Espasmos.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "8-10 semanas",
                        "rendimento_indoor": "450-500g/m²",
                        "clima": "Gosta de umidade moderada. Tende a ficar roxa com frio noturno."
                    }
                },
                "Northern Lights": {
                    "banco": "Sensi Seeds",
                    "thc": "18-22%", "cbd": "<1%",
                    "terpenos": ["Mirceno", "Cariofileno", "Limoneno"],
                    "sabor": "Terroso, Pinho, Picante.",
                    "efeito": "Euforia suave seguida de relaxamento profundo (Couch-lock).",
                    "medicinal": "Stress, Ansiedade, Falta de Apetite.",
                    "cultivo": {
                        "dificuldade": "Fácil (Lendária pela resistência)",
                        "tempo_flora": "7-8 semanas",
                        "rendimento_indoor": "500-550g/m²",
                        "clima": "Resistente a mofo e pragas. Ideal para iniciantes."
                    }
                },
                "Bubba Kush": {
                    "banco": "Green House Seeds",
                    "thc": "15-22%", "cbd": "0-1%",
                    "terpenos": ["Cariofileno", "Limoneno", "Mirceno"],
                    "sabor": "Café, Chocolate, Terra.",
                    "efeito": "Narcótico, tranquilizante físico.",
                    "medicinal": "Dor aguda, Insônia severa.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "8-9 semanas",
                        "rendimento_indoor": "400-450g/m²",
                        "clima": "Planta compacta e arbustiva. Exige poda de limpeza (lollipopping)."
                    }
                }
            },
            "Sativa Dominante": {
                "Sour Diesel": {
                    "banco": "Genética Americana (Clone only orig)",
                    "thc": "20-25%", "cbd": "<1%",
                    "terpenos": ["Cariofileno", "Limoneno", "Mirceno"],
                    "sabor": "Diesel, Combustível, Cítrico.",
                    "efeito": "Energético, Cerebral, Criativo.",
                    "medicinal": "Depressão, Fadiga, Stress.",
                    "cultivo": {
                        "dificuldade": "Difícil",
                        "tempo_flora": "10-12 semanas",
                        "rendimento_indoor": "450-600g/m²",
                        "clima": "Estica muito (Stretch 200%). Precisa de teto alto e SCROG."
                    }
                },
                "Super Lemon Haze": {
                    "banco": "Green House Seeds",
                    "thc": "19-25%", "cbd": "<1%",
                    "terpenos": ["Terpinoleno", "Cariofileno", "Mirceno"],
                    "sabor": "Limão siciliano, Doce, Zest.",
                    "efeito": "Eufórico, Vivo, Social.",
                    "medicinal": "Melhora de humor, Dores de cabeça.",
                    "cultivo": {
                        "dificuldade": "Média/Alta",
                        "tempo_flora": "10 semanas",
                        "rendimento_indoor": "600-800g/m² (Monstra produtiva)",
                        "clima": "Gosta de EC alto. Suporta bem nutrientes."
                    }
                },
                "Jack Herer": {
                    "banco": "Sensi Seeds",
                    "thc": "18-24%", "cbd": "<1%",
                    "terpenos": ["Terpinoleno", "Cariofileno", "Pineno"],
                    "sabor": "Pinho, Madeira, Especiarias.",
                    "efeito": "Foco mental, clareza, energia limpa.",
                    "medicinal": "TDAH, Fadiga Mental.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "8-10 semanas",
                        "rendimento_indoor": "500g/m²",
                        "clima": "Fenótipos variam. Produz muita resina."
                    }
                }
            },
            "Híbridas (50/50 ou Balanceadas)": {
                "Gorilla Glue #4 (GG4)": {
                    "banco": "GG Strains",
                    "thc": "25-32% (Extrema)", "cbd": "<1%",
                    "terpenos": ["Cariofileno", "Mirceno", "Limoneno"],
                    "sabor": "Pungente, Terra, Azedo.",
                    "efeito": "Colada no sofá (Glue), Euforia pesada.",
                    "medicinal": "Dor Crônica, TOC, Insônia.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "8-9 semanas",
                        "rendimento_indoor": "500-600g/m²",
                        "clima": "Hermafrodita se estressada. Sensível a luz."
                    }
                },
                "Girl Scout Cookies (GSC)": {
                    "banco": "Cookie Fam",
                    "thc": "22-28%", "cbd": "1%",
                    "terpenos": ["Cariofileno", "Limoneno", "Humuleno"],
                    "sabor": "Doce, Menta, Terroso.",
                    "efeito": "Relaxamento total com felicidade mental.",
                    "medicinal": "Náusea, Perda de Apetite, Dor.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "9-10 semanas",
                        "rendimento_indoor": "450g/m²",
                        "clima": "Produz buds muito densos e duros."
                    }
                },
                "Wedding Cake": {
                    "banco": "Seed Junky Genetics",
                    "thc": "22-27%", "cbd": "<1%",
                    "terpenos": ["Limoneno", "Cariofileno", "Mirceno"],
                    "sabor": "Baunilha, Pimenta, Doce.",
                    "efeito": "Relaxante, mas não sedativo imediato.",
                    "medicinal": "Ansiedade, Depressão.",
                    "cultivo": {
                        "dificuldade": "Média",
                        "tempo_flora": "8-9 semanas",
                        "rendimento_indoor": "500g/m²",
                        "clima": "Muito resistente. Ótima para extração."
                    }
                }
            },
            "Automáticas (Ruderalis)": {
                "Gorilla Cookies Auto": {
                    "banco": "FastBuds",
                    "thc": "Até 27%", "cbd": "<1%",
                    "terpenos": ["Cariofileno", "Limoneno"],
                    "sabor": "Cookie, Diesel, Cítrico.",
                    "efeito": "Riso frouxo, relaxamento corporal.",
                    "medicinal": "Stress, Dor.",
                    "cultivo": {
                        "dificuldade": "Fácil",
                        "tempo_flora": "10 semanas (Ciclo Total)",
                        "rendimento_indoor": "500-600g/m²",
                        "clima": "Aguenta muita comida e luz 20/4."
                    }
                },
                "Purple Punch Auto": {
                    "banco": "Barney's Farm",
                    "thc": "18-20%", "cbd": "1%",
                    "terpenos": ["Cariofileno", "Limoneno"],
                    "sabor": "Torta de maçã, Cravo, Blueberry.",
                    "efeito": "Desestressante, calmante.",
                    "medicinal": "Ansiedade, Relaxamento.",
                    "cultivo": {
                        "dificuldade": "Muito Fácil",
                        "tempo_flora": "8-9 semanas (Ciclo Total)",
                        "rendimento_indoor": "350-400g/m²",
                        "clima": "Fica pequena e robusta. Ideal para espaços curtos."
                    }
                }
            }
        },
        "💡 SETUP & MANEJO": {
            "luz": "VEG: 18/6h (PPFD 400-600) | FLORA: 12/12h (PPFD 800-1000). Automáticas: 20/4h sempre.",
            "clima_ideal": "Temp: 22-26°C (Dia) / 18-22°C (Noite). Umidade: Veg 60-70% / Flora 40-50%.",
            "nutricao": "EC Veg: 0.8-1.2 | EC Flora: 1.4-2.2. pH Solo: 6.0-6.8 | pH Inerte: 5.5-6.2.",
            "treinamento": "LST (Amarras), Topping (Poda Apical), SCROG (Tela), Lollipopping (Limpeza Baixeiro).",
            "colheita": "Observar Tricomas com lupa 60x: Transparente (Verde) -> Leitoso (Ponto Máximo THC) -> Âmbar (CBN/Sedativo)."
        },
        "🛡️ DOCTOR GROW (PROBLEMAS)": {
            "Pragas": {
                "Spider Mites": {"tipo": "Praga", "identificacao": "Pontos brancos na folha, teias nos buds.", "dano": "Suga a vida da planta.", "solucao": ["Óleo de Neem (Veg)", "Beauveria bassiana", "Predadores"], "obs": "Aumentar umidade ajuda a frear."},
                "Fungus Gnats": {"tipo": "Praga", "identificacao": "Mosquitinhos pretos no solo.", "dano": "Larvas comem raiz.", "solucao": ["BTI (Dipel/Dimy)", "Armadilhas Amarelas", "Terra Diatomácea"], "obs": "Deixe o solo secar bem."}
            },
            "Doencas": {
                "Oídio (Powdery Mildew)": {"tipo": "Fungo", "identificacao": "Pó branco nas folhas.", "dano": "Bloqueia luz.", "solucao": ["Leite cru 10%", "Bicarbonato de K", "Vaporizador de Enxofre"], "obs": "Melhore a ventilação imediatamente."},
                "Botrytis (Bud Rot)": {"tipo": "Fungo", "identificacao": "Bud podre, cinza/marrom.", "dano": "Perda total do bud.", "solucao": ["Remover área afetada com saco", "Reduzir umidade para 40%"], "obs": "Comum em buds gordos."}
            }
        }
    }
