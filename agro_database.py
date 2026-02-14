# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | MASTER DATABASE V4.20
# DESCRIÇÃO: Banco de dados agronômico completo (Nutrição, Pragas, Doenças, Deficiências).

def get_agro_db():
    return {
        # ==============================================================================
        # 1. METODOLOGIAS DE CULTIVO (RECEITAS & PARÂMETROS)
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico (No-Till / Living Soil)": {
                "descricao": "Foco na microbiologia do solo (Soil Food Web). Sabor (Terpenos) superior. Ciclo mais lento, porém mais estável.",
                "substrato_receita": [
                    "BASE: 40% Turfa de Sphagnum + 30% Perlita/Casca de Arroz + 30% Húmus de Minhoca.",
                    "ADITIVOS (p/ 50L): 200g Torta de Neem (Pragas), 200g Farinha de Ostras (Cálcio), 500g Bokashi.",
                    "MINERAIS: 200g Azomite (Micronutrientes), 100g Gesso Agrícola (Enxofre)."
                ],
                "nutricao": "A planta se alimenta da troca catiônica com fungos/bactérias. Use Chás Aerados (Compost Tea) e Fermentados (KNF).",
                "ph_ideal": "6.2 - 6.8 (O solo vivo tampona flutuações. Não use redutores ácidos químicos).",
                "ec_ideal": "N/A (Não se mede EC no runoff em orgânico. Monitore a vida do solo)."
            },
            "Mineral (Coco / High Fertigation)": {
                "descricao": "Alta performance (Crop Steering). Crescimento explosivo. Exige precisão de pH e EC diária.",
                "substrato_receita": [
                    "100% Fibra de Coco (Bufferizada com CalMag previamente).",
                    "OU Mix: 70% Coco + 30% Perlita (Melhor drenagem para regas frequentes)."
                ],
                "nutricao": "Sais Minerais Quelatados. Regas frequentes (Múltiplas vezes ao dia) com Runoff de 10-20% para lavar sais.",
                "ph_ideal": "5.8 - 6.2 (Faixa ácida para absorção de micronutrientes no coco).",
                "ec_ideal": "Veg: 1.2-1.5 mS | Flora: 1.8-2.5 mS (Cuidado com o 'Stacking' de sais no substrato)."
            },
            "Hidroponia (DWC / RDWC)": {
                "descricao": "Raízes submersas em solução oxigenada. Velocidade máxima de crescimento (30% mais rápido). Risco alto de Pythium.",
                "substrato_receita": [
                    "Argila Expandida (Lavada e pH estabilizado em 5.5).",
                    "Cubos de Lã de Rocha (Rockwool) para germinação/clones."
                ],
                "nutricao": "Solução estéril (H2O2) OU Biológica (Beneficiais). Nunca misture os dois. Temperatura da água < 21°C é MANDATÓRIA.",
                "ph_ideal": "5.5 - 6.0 (Flutua rápido. Checar 2x ao dia).",
                "ec_ideal": "Veg: 0.8-1.0 | Flora: 1.2-1.8 (Hidro exige MENOS comida que o coco)."
            },
            "Outdoor (Guerrilha / Quintal)": {
                "descricao": "Energia solar (espectro completo). Plantas gigantes. Risco ambiental alto.",
                "substrato_receita": [
                    "Cova de 40L mínimo.",
                    "Mistura: 50% Solo Nativo + 50% Composto Orgânico + Esterco curtido."
                ],
                "nutricao": "Top Dress (Cobertura) a cada 20 dias com Bokashi ou Torta de Mamona (Veg) / Farinha de Osso (Flora).",
                "ph_ideal": "6.0 - 7.0",
                "ec_ideal": "Depende da análise de solo."
            }
        },

        # ==============================================================================
        # 2. FASES DINÂMICAS (SISTEMA DE DECISÃO DE RISCO)
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula (Semana 1-2)": {
                "foco": "Enraizamento e Umidade",
                "riscos": ["Damping-off (Pythium)", "Desidratação", "Queima por Luz"],
                "obs": "Umidade alta (70%+) é vital. As raízes ainda não bebem, a planta se hidrata pelas folhas. Luz suave (PPFD 150-250)."
            },
            "Vegetativo (Semana 3-6)": {
                "foco": "Estrutura, Poda e Nitrogênio",
                "riscos": ["Tripes", "Ácaros", "Deficiência de Magnésio"],
                "obs": "Hora de treinar (LST/Topping). A planta consome muito Nitrogênio. Ventilação forte para engrossar caules."
            },
            "Pré-Flora / Stretch (Semana 7-8)": {
                "foco": "Controle de Altura e Sexagem",
                "riscos": ["Hermafroditas (Stress)", "Fome de Cálcio"],
                "obs": "A planta pode triplicar de tamanho. Instale a rede SCROG agora. Identifique e remova machos imediatamente."
            },
            "Flora Inicial (Semana 9-11)": {
                "foco": "Formação de Botões (Pistilos)",
                "riscos": ["Oídio (Pó Branco)", "Overfert (Pontas Queimadas)"],
                "obs": "Pare sprays foliares! Aumente o Fósforo (P) e Potássio (K). Reduza a umidade para 50%."
            },
            "Flora Final / Engorda (Semana 12+)": {
                "foco": "Densidade, Resina e Senescência",
                "riscos": ["Botrytis (Bud Rot)", "Bananas (Nanners)"],
                "obs": "Umidade crítica < 45%. Inicie o FLUSH (lavagem) 10 dias antes da colheita se usar mineral. Monitore tricomas."
            }
        },

        # ==============================================================================
        # 3. DOCTOR GROW MASTER (PRAGAS, DOENÇAS E DEFICIÊNCIAS)
        # ==============================================================================
        "DOCTOR_GROW_MASTER": {
            "Pragas": {
                "Spider Mites (Tetranychus urticae)": {
                    "identificacao": "Pontinhos brancos/amarelos nas folhas (picadas). Teias nos buds em casos graves. Vivem na face inferior.",
                    "controle_organico": ["Óleo de Neem (Apenas Veg)", "Beauveria bassiana (Fungo)", "Predadores: Phytoseiulus persimilis"],
                    "controle_quimico": ["Abamectina (Vertimec) - Carência 28 dias.", "Etoxazol (Ovicida)."],
                    "gravidade": "ALTA. Destrói a fotossíntese e cobre a planta de teia."
                },
                "Fungus Gnats (Bradysia)": {
                    "identificacao": "Mosquitinhos pretos voando no solo. Larvas brancas translúcidas na raiz.",
                    "controle_organico": ["BTI (Bacillus thuringiensis israelensis) na rega", "Terra de Diatomáceas (Seco)", "Armadilhas Amarelas"],
                    "controle_quimico": ["Imidacloprido (Apenas se infestação massiva no Veg)."],
                    "gravidade": "MÉDIA. Larvas comem raízes capilares e abrem porta para Fusarium."
                },
                "Tripes (Thrips)": {
                    "identificacao": "Manchas prateadas/bronzeadas que brilham. Inseto palito rápido.",
                    "controle_organico": ["Spinosad (Produto: Tracer/Exalt) - O melhor biológico.", "Sabão Potássico", "Armadilhas Azuis"],
                    "controle_quimico": ["Clorfenapir (Pirate) - Tóxico.", "Acetamiprido."],
                    "gravidade": "MÉDIA. Deforma folhas novas e transmite viroses."
                },
                "Russet Mites (Ácaro-do-Bronzeamento)": {
                    "identificacao": "Invisível a olho nu (precisa de lupa 60x). Folhas ficam 'envernizadas', marrons e encarquilhadas.",
                    "controle_organico": ["Enxofre Micronizado (Pó ou Vapor) - Apenas Veg.", "Ácido Cítrico"],
                    "controle_quimico": ["Abamectina + Espirodiclofeno"],
                    "gravidade": "CRÍTICA. O 'Assassino Invisível'. Quando você vê o dano, já é tarde."
                }
            },
            "Doencas": {
                "Oídio (Powdery Mildew)": {
                    "identificacao": "Pó branco (parece farinha) nas folhas. Começa nas folhas baixas e sombreadas.",
                    "controle_organico": ["Leite Cru 10% + Água 90% (Luz solar ativa a enzima)", "Bicarbonato de Potássio", "Bacillus subtilis"],
                    "controle_quimico": ["Difenoconazol (Score) - Sistêmico.", "Tebuconazol."],
                    "gravidade": "ALTA. Fungo sistêmico. Melhore a ventilação e baixe a umidade."
                },
                "Botrytis (Bud Rot / Mofo Cinza)": {
                    "identificacao": "Buds ficam marrons, moles e úmidos. Ao abrir, sai uma 'fumaça' de esporos.",
                    "controle_organico": ["Prevenção: Trichoderma harzianum desde o início.", "Remoção cirúrgica com saco plástico."],
                    "controle_quimico": ["NÃO USAR FUNGICIDAS EM FLORES. Risco severo à saúde (Pneumonia fúngica)."],
                    "gravidade": "CRÍTICA. Perda total da área afetada. Comum em buds densos (Indicas)."
                },
                "Fusarium (Murcha)": {
                    "identificacao": "Um galho murcha do nada enquanto o resto está bem. Ao cortar o caule, o miolo está marrom.",
                    "controle_organico": ["Trichoderma (Preventivo). Não tem cura pós-infecção."],
                    "controle_quimico": ["Não efetivo. Descarte a planta e esterilize o vaso."],
                    "gravidade": "FATAL. O fungo entope os vasos xilemáticos da planta."
                },
                 "Pythium (Root Rot)": {
                    "identificacao": "Raízes marrons, gosmentas e cheiro de podre (ovo/peixe).",
                    "controle_organico": ["H2O2 (Peróxido) para esterilizar.", "Enzimas (Cannazym)"],
                    "controle_quimico": ["Metalaxil"],
                    "gravidade": "ALTA. Comum em Hidroponia com reservatório quente (>22°C)."
                }
            },
            "Deficiencias (Nutrientes)": {
                "Nitrogênio (N)": {
                    "identificacao": "Folhas velhas (baixeiro) ficam amarelas uniformemente e caem.",
                    "controle_organico": ["Sangue seco", "Humus de Minhoca", "Chá de Urtiga"],
                    "controle_quimico": ["Ureia", "Nitrato de Cálcio"],
                    "gravidade": "BAIXA. Fácil correção no Veg. Normal no final da Flora."
                },
                "Magnésio (Mg)": {
                    "identificacao": "Clorose intervenal (nervuras verdes, meio da folha amarelo). Folhas viram pra cima (rezando).",
                    "controle_organico": ["Sal Amargo (Sulfato de Magnésio) via foliar", "Dolomita"],
                    "controle_quimico": ["CalMag", "Nitrato de Magnésio"],
                    "gravidade": "MÉDIA. Crítico na transição para flora."
                },
                "Cálcio (Ca)": {
                    "identificacao": "Manchas de ferrugem (pontos marrons) nas folhas novas/médias. Crescimento lento.",
                    "controle_organico": ["Farinha de Ostras", "Casca de Ovo moída (Lento)"],
                    "controle_quimico": ["Nitrato de Cálcio (CalMag)"],
                    "gravidade": "ALTA. Cálcio é imóvel. A planta não recupera a folha danificada."
                },
                "Overfert (Excesso/Queima)": {
                    "identificacao": "Pontas das folhas queimadas e viradas para baixo (Garra). Folhas verde escuro excessivo.",
                    "controle_organico": ["Flush (Lavagem) apenas com água.", "Medir Runoff."],
                    "controle_quimico": ["Flush com agente de limpeza (FloraKleen)."],
                    "gravidade": "MÉDIA. Trava o crescimento (Lockout) por excesso de sais."
                }
            }
        }
    }
