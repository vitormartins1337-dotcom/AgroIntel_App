# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | MASTER DATABASE
# DESCRIÇÃO: Dados técnicos para Orgânico, Mineral, Hidro e IPM (Manejo Integrado de Pragas).

def get_agro_db():
    return {
        "METODOS_CULTIVO": {
            "Orgânico (Living Soil)": {
                "descricao": "Cultivo baseado na vida do solo. Foco em terroirs e qualidade final.",
                "substrato_receita": [
                    "40% Turfa de Sphagnum ou Coco (Lavado)",
                    "30% Perlita ou Casca de Arroz Carbonizada (Aeração)",
                    "30% Húmus de Minhoca ou Composto (Vida)",
                    "Aditivos (p/ 100L): 1kg Torta de Neem, 2kg Farinha de Osso, 200g Azomite, 500g Gesso Agrícola."
                ],
                "nutricao": "A planta come o solo. Use chás de compostagem (Aerados), Bokashi e KNF (Fermentados).",
                "ph_ideal": "6.2 - 6.8 (O solo tampona variações leves).",
                "ec_ideal": "Não se mede EC no runoff em orgânico puro."
            },
            "Mineral (Inerte)": {
                "descricao": "Alta performance e controle total. Foco em rendimento (g/watt).",
                "substrato_receita": [
                    "50% Turfa de Sphagnum",
                    "50% Perlita Expandida",
                    "Ou 100% Coco (Bufferizado com CalMag)"
                ],
                "nutricao": "Fertilizantes minerais quelatados (Salt based). Obrigatório medir pH e EC na entrada e saída (Runoff).",
                "ph_ideal": "5.8 - 6.2 (Mais ácido para absorção de micronutrientes).",
                "ec_ideal": "Veg: 1.2-1.5 | Flora: 1.8-2.4 mS/cm."
            },
            "Hidroponia (DWC/RDWC)": {
                "descricao": "Máxima oxigenação radicular. Crescimento explosivo (30-50% mais rápido).",
                "substrato_receita": [
                    "Argila Expandida (Lavada e pH regulado)",
                    "Lã de Rocha (Rockwool)"
                ],
                "nutricao": "Solução nutritiva estéril ou com biofiltro. Temperatura da água é crítica.",
                "ph_ideal": "5.5 - 6.0 (Flutuação é normal, corrigir se passar disso).",
                "ec_ideal": "Veg: 0.8-1.2 | Flora: 1.5-2.0 (Menos é mais em hidro)."
            }
        },
        "FASES_DINAMICAS": {
            "Plântula (Semana 1-2)": {
                "foco": "Enraizamento",
                "riscos": ["Damping-off (Pythium)", "Fungus Gnats", "Seca por luz forte"],
                "obs": "Manter domo de umidade (70-80%). Luz fraca (PPFD 200). Não adubar se o solo tiver carga."
            },
            "Vegetativo (Semana 3-6)": {
                "foco": "Estrutura e Nitrogênio",
                "riscos": ["Tripes", "Ácaros", "Deficiência de CalMag"],
                "obs": "Hora das podas (Topping/LST). Ventilação forte para fortalecer o caule."
            },
            "Pré-Flora (Semana 7-8)": {
                "foco": "Stretch (Estirão)",
                "riscos": ["Hermafroditismo", "Fome de Magnésio"],
                "obs": "A planta pode dobrar de tamanho. Instalar rede SCROG. Identificar sexagem final."
            },
            "Flora Inicial (Semana 9-11)": {
                "foco": "Formação de Botões",
                "riscos": ["Oídio (Powdery Mildew)", "Overfert (Queima)"],
                "obs": "Parar Foliares! A partir daqui nada de neem ou químicos nas folhas."
            },
            "Flora Final/Engorda (Semana 12+)": {
                "foco": "Densidade e Terpenos",
                "riscos": ["Botrytis (Bud Rot)", "Bananas (Stress final)"],
                "obs": "Baixar umidade para <45%. Monitorar tricomas."
            }
        },
        "DOCTOR_GROW_MASTER": {
            "Pragas": {
                "Spider Mites (Ácaro-rajado)": {
                    "identificacao": "Pontos brancos nas folhas (picadas). Teias nos buds em casos graves. Vivem embaixo da folha.",
                    "controle_organico": ["Óleo de Neem (Apenas Veg)", "Beauveria bassiana (Fungo)", "Predadores: Phytoseiulus persimilis"],
                    "controle_quimico": ["Abamectina (Vertimec) - Período de carência 28 dias.", "Etoxazol (Barricade) - Ovicida."],
                    "gravidade": "ALTA. Pode destruir a colheita em 3 dias."
                },
                "Fungus Gnats": {
                    "identificacao": "Mosquitinhos pretos voando no solo. Larvas brancas com cabeça preta na raiz.",
                    "controle_organico": ["BTI (Bacillus thuringiensis israelensis) na rega", "Terra de Diatomáceas na superfície", "Armadilhas Amarelas (Sticky Traps)"],
                    "controle_quimico": ["Imidacloprido (Apenas se infestação massiva no Veg)."],
                    "gravidade": "MÉDIA. Abre porta para doenças de raiz."
                },
                "Tripes (Thrips)": {
                    "identificacao": "Manchas prateadas/bronzeadas nas folhas. Inseto palito rápido.",
                    "controle_organico": ["Spinosad (O melhor orgânico)", "Sabão Potássico + Álcool Isopropílico", "Armadilhas Azuis"],
                    "controle_quimico": ["Clorfenapir (Pirate) - Tóxico, cuidado.", "Acetamiprido."],
                    "gravidade": "MÉDIA. Vetor de viroses."
                },
                "Cochonilha (Mealybugs)": {
                    "identificacao": "Massas brancas algodoadas no caule ou folhas.",
                    "controle_organico": ["Álcool 70% direto no inseto (Cotonete)", "Óleo Mineral"],
                    "controle_quimico": ["Acetamiprido (Mospilan)"],
                    "gravidade": "BAIXA/MÉDIA. Sugadores de seiva."
                }
            },
            "Doencas": {
                "Oídio (Powdery Mildew)": {
                    "identificacao": "Pó branco (parece farinha) nas folhas. Começa nas folhas baixas e sombreadas.",
                    "controle_organico": ["Leite Cru 10% + Água 90% (Solar)", "Bicarbonato de Potássio", "Bacillus subtilis"],
                    "controle_quimico": ["Difenoconazol (Score) - Sistêmico.", "Enxofre (Vaporização) - Apenas Veg."],
                    "gravidade": "ALTA. Inutiliza a flor para consumo."
                },
                "Botrytis (Bud Rot)": {
                    "identificacao": "Buds ficam marrons, moles e úmidos. Mofo cinza visível dentro da flor.",
                    "controle_organico": ["Prevenção apenas: Trichoderma harzianum", "Remoção cirúrgica com saco plástico"],
                    "controle_quimico": ["NÃO USAR EM FLORES. Risco à saúde humana."],
                    "gravidade": "CRÍTICA. Perda total da área afetada."
                },
                "Pythium (Root Rot)": {
                    "identificacao": "Raízes marrons, Gosmentas e com cheiro de podre. Planta murcha mesmo regada.",
                    "controle_organico": ["Peróxido de Hidrogênio (H2O2) para limpar", "Enzimas", "Trichoderma"],
                    "controle_quimico": ["Metalaxil (Ridomil) - Apenas em clones/mães."],
                    "gravidade": "ALTA. Comum em hidroponia com água quente (>22°C)."
                }
            }
        }
    }
