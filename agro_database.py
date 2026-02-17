# ARQUIVO: agro_database.py
# SISTEMA: AGROWER SDI | DATABASE V10.0 (TITANIUM EDITION)
# DESCRIÇÃO: Banco de Dados Agronômico Completo (Genética, Nutrição, Fitossanidade e Clima)

def get_agro_db():
    return {
        # ==============================================================================
        # 1. PARÂMETROS GENÉTICOS (EXPANDIDO: THC / CBD / TIPO)
        # ==============================================================================
        "GENETICAS_PARAMETROS": {
            # --- FOTOPERÍODO THC (ALTO RENDIMENTO) ---
            "Indica Predom. THC (Fotoperíodo)": {
                "fator_yield": 1.0, 
                "ciclo_dias": 60, 
                "tipo": "Foto",
                "desc": "Arbustiva, internódios curtos. Efeito narcótico. Alta demanda de Magnésio na flora."
            },
            "Sativa Predom. THC (Fotoperíodo)": {
                "fator_yield": 1.3, 
                "ciclo_dias": 85, 
                "tipo": "Foto",
                "desc": "Alta estatura, floração longa. Sensível a excesso de Nitrogênio na flora."
            },
            "Híbrida 50/50 THC (Fotoperíodo)": {
                "fator_yield": 1.15, 
                "ciclo_dias": 70, 
                "tipo": "Foto",
                "desc": "Vigor híbrido. Equilibra produção e tempo. Adapta-se bem a podas."
            },

            # --- FOTOPERÍODO MEDICINAL (CBD / 1:1) ---
            "Indica Predom. CBD (Fotoperíodo)": {
                "fator_yield": 1.1, 
                "ciclo_dias": 65, 
                "tipo": "Foto",
                "desc": "Foco medicinal relaxante. Estrutura robusta e resistente a estresse."
            },
            "Sativa Predom. CBD (Fotoperíodo)": {
                "fator_yield": 1.25, 
                "ciclo_dias": 80, 
                "tipo": "Foto",
                "desc": "Medicinal diurno. Planta alta, requer amarras (LST) para controle de altura."
            },
            "Híbrida 1:1 THC:CBD (Fotoperíodo)": {
                "fator_yield": 1.1, 
                "ciclo_dias": 70, 
                "tipo": "Foto",
                "desc": "Efeito entourage balanceado. Ótima para extrações medicinais full spectrum."
            },

            # --- AUTOMÁTICAS (CICLO RÁPIDO) ---
            "Indica Predom. THC (Automática)": {
                "fator_yield": 0.5, 
                "ciclo_dias": 65, 
                "tipo": "Auto",
                "desc": "Ciclo ultra rápido. Raiz sensível. Não aceita podas agressivas ou transplantes."
            },
            "Sativa Predom. THC (Automática)": {
                "fator_yield": 0.7, 
                "ciclo_dias": 85, 
                "tipo": "Auto",
                "desc": "Genética XXL. Requer DLI (Luz) alto (20/4) para expressar potencial."
            },
            "Híbrida 50/50 THC (Automática)": {
                "fator_yield": 0.6, 
                "ciclo_dias": 75, 
                "tipo": "Auto",
                "desc": "Equilíbrio ideal entre rapidez e sabor."
            },
            "Medicinal CBD (Automática)": {
                "fator_yield": 0.55, 
                "ciclo_dias": 75, 
                "tipo": "Auto",
                "desc": "Terapêutico rápido. Baixo teor de THC. Ideal para óleo medicinal caseiro."
            }
        },

        # ==============================================================================
        # 2. MÉTODOS DE CULTIVO (PARÂMETROS FÍSICO-QUÍMICOS)
        # ==============================================================================
        "METODOS_CULTIVO": {
            "Orgânico (Solo Vivo)": {
                "descricao": "Ciclo biológico. Foco na vida do solo (Food Web).",
                "rendimento_base": 55, "ph_ideal": "6.0-6.8", "ec_ideal": "Solo (Não medir Runoff)"
            },
            "Mineral (Inerte/Coco)": {
                "descricao": "Alta performance via fertirrigação precisa.",
                "rendimento_base": 85, "ph_ideal": "5.8-6.2", "ec_ideal": "1.8-2.6 (Alta EC)"
            },
            "Orgânico-Mineral (Mix)": {
                "descricao": "Híbrido: Solo base com reforço mineral na floração.",
                "rendimento_base": 70, "ph_ideal": "6.0-6.5", "ec_ideal": "1.2-1.8"
            },
            "Hidroponia (DWC/RDWC)": {
                "descricao": "Máxima oxigenação e absorção iônica direta.",
                "rendimento_base": 110, "ph_ideal": "5.5-5.8", "ec_ideal": "1.2-2.0"
            },
            "Semi-Inerte (Turfa/Perlita)": {
                "descricao": "Substrato leve com retenção média. Exige rega controlada.",
                "rendimento_base": 75, "ph_ideal": "5.9-6.3", "ec_ideal": "1.4-2.0"
            }
        },

        # ==============================================================================
        # 3. MARCHA DE ABSORÇÃO (CURVAS MATEMÁTICAS - 12 SEMANAS)
        # ==============================================================================
        "NUTRI_MARCHA_ABSORCAO": {
            "semanas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            # Nitrogênio: Alto na vega, cai drasticamente na flora
            "N": [90, 100, 100, 80, 60, 40, 30, 20, 10, 5, 0, 0], 
            # Fósforo: Baixo na vega, explode na pré-flora e flora média
            "P": [20, 30, 40, 60, 80, 100, 100, 90, 70, 40, 10, 0], 
            # Potássio: Crescente constante, pico na engorda (semana 6-8)
            "K": [30, 40, 50, 70, 85, 95, 100, 100, 95, 60, 20, 0], 
            # Cálcio: Necessidade constante (parede celular), pico no stretch
            "Ca": [40, 50, 70, 90, 100, 90, 80, 70, 50, 30, 10, 0], 
            # Magnésio: Essencial para clorofila, pico no meio da flora
            "Mg": [40, 50, 60, 80, 90, 80, 70, 60, 40, 20, 10, 0],
            # Enxofre: Essencial para terpenos e proteínas
            "S": [20, 30, 40, 50, 60, 80, 90, 90, 80, 50, 20, 0]
        },

        # ==============================================================================
        # 4. ENCICLOPÉDIA DE DEFICIÊNCIAS (MACRO & MICRO COMPLETO)
        # ==============================================================================
        "DEFICIENCIAS_VISUAIS": {
            # --- MACRONUTRIENTES PRIMÁRIOS ---
            "Nitrogênio (N)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Amarelamento uniforme das folhas mais VELHAS (base). Planta com aspecto pálido e crescimento lento.",
                "correcao_bio": "Sangue seco, Farinha de penas, Humus de minhoca, Chorume de urtiga.",
                "correcao_quim": "Ureia, Nitrato de Amônio, Base 'Grow' (NPK 10-5-5).",
                "cor_card": "#22c55e" # Verde Nitrogênio
            },
            "Fósforo (P)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Pecíolos (cabinhos) roxos. Manchas marrons/necróticas. Folhas verde-azulado escuro e brilho reduzido.",
                "correcao_bio": "Farinha de osso, Guano de morcego (alto P), Rocha fosfática.",
                "correcao_quim": "Superfosfato, MAP, Base 'Bloom', MKP.",
                "cor_card": "#3b82f6" # Azul Fósforo
            },
            "Potássio (K)": {
                "tipo": "Macro Primário (Móvel)",
                "sintoma": "Bordas das folhas queimadas/secas (parece queimadura). Caules fracos. Flores pequenas e sem densidade.",
                "correcao_bio": "Cinzas de madeira (cuidado pH), Kelp (Algas), Sulfato de Potássio Orgânico.",
                "correcao_quim": "Nitrato de Potássio, PK Booster (13-14), Silicato de Potássio.",
                "cor_card": "#a855f7" # Roxo Potássio
            },
            
            # --- MACRONUTRIENTES SECUNDÁRIOS ---
            "Cálcio (Ca)": {
                "tipo": "Macro Secundário (Imóvel)",
                "sintoma": "Pontos de ferrugem marrom em folhas NOVAS ou médias. Folhas novas nascem distorcidas ou em gancho.",
                "correcao_bio": "Farinha de ostras, Calcário dolomítico, Casca de ovo moída (ação lenta).",
                "correcao_quim": "Nitrato de Cálcio, CalMag (fundamental em LED).",
                "cor_card": "#f97316" # Laranja Cálcio
            },
            "Magnésio (Mg)": {
                "tipo": "Macro Secundário (Móvel)",
                "sintoma": "Clorose intervenal (nervuras verdes, meio amarelo). Folhas curvam para cima ('rezando').",
                "correcao_bio": "Sal Amargo (Sulfato de Magnésio) via foliar, Dolomita.",
                "correcao_quim": "Nitrato de Magnésio, CalMag, Sal de Epsom.",
                "cor_card": "#eab308" # Dourado Magnésio
            },
            "Enxofre (S)": {
                "tipo": "Macro Secundário (Imóvel)",
                "sintoma": "Amarelamento (clorose) começando nas folhas NOVAS (topo), diferente do N que começa nas velhas.",
                "correcao_bio": "Gesso agrícola, Esterco curtido.",
                "correcao_quim": "Sulfato de Magnésio (Epsom) já corrige S também.",
                "cor_card": "#facc15" # Amarelo Enxofre
            },

            # --- MICRONUTRIENTES (COMPLETO) ---
            "Ferro (Fe)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Folhas novas nascem amarelo-limão brilhante, nervuras permanecem verdes estritas. Comum em pH alto.",
                "correcao_bio": "Quelatos naturais, Algas marinhas.",
                "correcao_quim": "Ferro Quelatado (EDTA/DTPA) via foliar.",
                "cor_card": "#a3e635"
            },
            "Zinco (Zn)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Folhas novas com pontas queimadas e rotação 90º. 'Rosetting' (internódios muito curtos no topo).",
                "correcao_bio": "Kelp, Extrato de sementes de abóbora.",
                "correcao_quim": "Sulfato de Zinco, Mix de Micro.",
                "cor_card": "#9ca3af"
            },
            "Manganês (Mn)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Manchas necróticas marrons espalhadas em folhas novas. Parece deficiência de Mg mas os pontos são menores.",
                "correcao_bio": "Farinha de Algas, Bokashi.",
                "correcao_quim": "Sulfato de Manganês, Quelato Mn.",
                "cor_card": "#64748b"
            },
            "Boro (B)": {
                "tipo": "Micro (Imóvel)",
                "sintoma": "Morte do meristema apical (topo queima). Caules ocos e quebradiços.",
                "correcao_bio": "Bórax (diluído), Cinzas.",
                "correcao_quim": "Ácido bórico.",
                "cor_card": "#94a3b8"
            }
        },

        # ==============================================================================
        # 5. FASES FENOLÓGICAS (DETALHAMENTO PROFISSIONAL)
        # ==============================================================================
        "FASES_DINAMICAS": {
            "Plântula (Seedling)": {
                "foco": "Estabelecimento Radicular",
                "obs": "Raiz pivotante descendo. Manter VPD baixo (0.4-0.8 kPa). Evitar luz intensa direta. Regar apenas ao redor do caule.",
                "ameacas": ["Pythium (Damping-off)", "Fungus Gnats"],
                "clima_ideal": "Temp: 24-26°C | Umidade: 70-80%"
            },
            "Vegetativo Inicial": {
                "foco": "Desenvolvimento Foliar",
                "obs": "Folhas de 3 a 5 pontas. Início da demanda de N. Pode iniciar ventilação leve para fortalecer o caule.",
                "ameacas": ["Tripes", "Mosca Branca", "Minadores"],
                "clima_ideal": "Temp: 22-28°C | Umidade: 60-70%"
            },
            "Vegetativo Tardio": {
                "foco": "Estrutura e Ramificação",
                "obs": "Planta robusta. Hora de podas (Top/Fim), LST e Supercropping. Demanda máxima de Nitrogênio.",
                "ameacas": ["Spider Mites", "Deficiência de N", "Cochonilhas"],
                "clima_ideal": "Temp: 22-28°C | Umidade: 55-65%"
            },
            "Pré-Flora (Stretch)": {
                "foco": "Transição Hormonal",
                "obs": "Alongamento do caule (2x a 3x). Sexagem visível. Alto consumo de Cálcio/Magnésio. Instalar rede SCROG se usar.",
                "ameacas": ["Hermafroditas", "Deficiência de Mg", "Estresse de luz"],
                "clima_ideal": "Temp: 20-26°C | Umidade: 50-60%"
            },
            "Flora Inicial (Early Bloom)": {
                "foco": "Formação de Coroas",
                "obs": "Pistilos brancos abundantes ('Pompons'). Parar Nitrogênio gradualmente, aumentar P e K. Desfoliação leve.",
                "ameacas": ["Oídio", "Overfert de N"],
                "clima_ideal": "Temp: 20-26°C | Umidade: 45-55%"
            },
            "Flora Média (Bulking)": {
                "foco": "Engorda e Densidade",
                "obs": "Pico de produção de óleo. Buds inchando e unindo. Consumo máximo de Potássio (K) e Fósforo (P).",
                "ameacas": ["Queima de luz", "Deficiência de K", "Calor excessivo"],
                "clima_ideal": "Temp: 18-24°C | Umidade: 40-50%"
            },
            "Flora Final (Ripening)": {
                "foco": "Maturação e Senescência",
                "obs": "Pistilos marrons. Tricomas leitosos/âmbar. Iniciar Flush (lavagem) se usar mineral. Reduzir temperatura noturna favorece cor (antocianina).",
                "ameacas": ["Botrytis (Mofo)", "Bananas (Stress)", "Sementes"],
                "clima_ideal": "Temp: 18-22°C | Umidade: 35-45%"
            }
        },

        # ==============================================================================
        # 6. FITOSSANIDADE (PRAGAS E DOENÇAS - EXPANDIDO)
        # ==============================================================================
        "DOCTOR_GROW_FITOSSANIDADE": {
            "Spider Mites (Ácaros)": {
                "gravidade": "CRÍTICA",
                "sintomas": "Pontos brancos minúsculos na face superior (estippling). Teias finas nos buds em casos avançados. Gostam de calor e seca.",
                "bio": ["Beauveria Bassiana", "Óleo de Neem (Apenas Veg)", "Predadores (Phytoseiulus)"],
                "quimico": ["Abamectina (Vertimec)", "Etoxazol", "Espirodiclofeno"],
                "obs": "Reproduzem-se a cada 3 dias no calor."
            },
            "Tripes": {
                "gravidade": "MÉDIA",
                "sintomas": "Manchas prateadas/bronzeadas que brilham. Insetos finos e rápidos. Deixam fezes pretas nas folhas.",
                "bio": ["Spinosad (Tracer)", "Sabão Potássico", "Armadilhas Azuis", "Óleo de Laranja"],
                "quimico": ["Clorfenapir", "Acetamiprido", "Imidacloprido (Veg)"],
                "obs": "Vetores de vírus. Atacam folhas novas."
            },
            "Fungus Gnats": {
                "gravidade": "BAIXA/MÉDIA",
                "sintomas": "Mosquitos pretos voando no solo. Larvas transparentes comendo pelos radiculares. Solo muito úmido.",
                "bio": ["BTI (Bacillus thuringiensis israelensis)", "Terra de Diatomáceas", "Nematóides SF"],
                "quimico": ["Imidacloprido (Apenas Veg)", "Peróxido de Hidrogênio (Solo)"],
                "obs": "Indicador de erro na rega."
            },
            "Pulgões (Aphids)": {
                "gravidade": "MÉDIA",
                "sintomas": "Colônias de insetos (verdes/pretos) sugando seiva nos caules e embaixo das folhas. Produzem 'melada' que atrai formigas.",
                "bio": ["Joaninhas (Predador)", "Sabão de Potássio", "Óleo de Neem"],
                "quimico": ["Acetamiprido", "Piretróides"],
                "obs": "Formigas protegem pulgões. Elimine as formigas também."
            },
            "Mosca Branca": {
                "gravidade": "MÉDIA/ALTA",
                "sintomas": "Nuvem de mosquitos brancos ao balançar a planta. Folhas amareladas e pegajosas.",
                "bio": ["Armadilhas Amarelas", "Beauveria Bassiana", "Sabão Potássico"],
                "quimico": ["Acetamiprido", "Piretróides"],
                "obs": "Muito resistentes. Requer aplicações a cada 3 dias."
            },
            "Cochonilha": {
                "gravidade": "MÉDIA",
                "sintomas": "Lapas brancas (parece algodão) ou marrons grudadas no caule. Sugam seiva.",
                "bio": ["Álcool Isopropílico (cotonete)", "Óleo Mineral", "Sabão"],
                "quimico": ["Acefato", "Imidacloprido"],
                "obs": "Remover manualmente antes de aplicar produto."
            },
            "Lagartas": {
                "gravidade": "ALTA (Outdoor)",
                "sintomas": "Buracos grandes nas folhas. Fezes pretas grandes nos buds. Apodrecimento rápido do bud (Botrytis).",
                "bio": ["Bacillus thuringiensis kurstaki (BTk)", "Catação manual"],
                "quimico": ["Espinosade"],
                "obs": "Principal causa de perda total em outdoor."
            },
            "Oídio (Powdery Mildew)": {
                "gravidade": "ALTA",
                "sintomas": "Manchas de pó branco (parece farinha) sobre as folhas. Não sai passando o dedo facilmente.",
                "bio": ["Leite Cru 10% no Sol", "Bicarbonato de Potássio", "Bacillus subtilis"],
                "quimico": ["Difenoconazol", "Enxofre (Vaporizador - Veg)", "Tebuconazol"],
                "obs": "Fungo sistêmico. Requer baixa umidade e alta ventilação."
            },
            "Botrytis (Bud Rot)": {
                "gravidade": "FATAL",
                "sintomas": "Folha de açúcar seca repentinamente no meio do bud. Bud fica marrom/cinza e mole. Esporos voam.",
                "bio": ["Remoção cirúrgica com saco plástico", "Trichoderma (Prevenção)"],
                "quimico": ["NENHUM (Descarte a parte afetada)"],
                "obs": "Causado por umidade alta na floração (>50%) ou lagartas. Nunca fume mofo."
            },
            "Pythium (Root Rot)": {
                "gravidade": "ALTA",
                "sintomas": "Raízes marrons, gosmentas, cheiro de ovo podre/peixe. Planta murcha mesmo com água.",
                "bio": ["H2O2 (Peróxido de Hidrogênio)", "Enzimas", "Trichoderma"],
                "quimico": ["Metalaxil"],
                "obs": "Comum em hidroponia com reservatório quente (>22°C)."
            },
            "Fusarium": {
                "gravidade": "FATAL",
                "sintomas": "Um galho inteiro murcha e morre enquanto o resto está bem. Caule marrom por dentro.",
                "bio": ["Trichoderma (Prevenção)", "Micorrizas"],
                "quimico": ["NENHUM EFICAZ (Descarte)"],
                "obs": "Fungo de solo persistente. Não reutilize o solo."
            }
        }
    }
