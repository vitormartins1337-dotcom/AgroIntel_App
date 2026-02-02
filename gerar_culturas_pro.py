import os
import json

# Função para salvar no padrão Dual-File (2 arquivos por pasta)
def criar_cultura(pasta_nome, nome_display, biologia, manejo):
    # Pode criar dentro de categorias se quiser, ou direto na raiz da database
    # Aqui vou colocar direto ou organizado, o Data Engine novo lê de qualquer jeito.
    # Vamos organizar por categorias para ficar limpo para você.
    
    base_path = os.path.join("database", pasta_nome) 
    os.makedirs(base_path, exist_ok=True)

    # 1. BIOLOGIA.JSON
    with open(os.path.join(base_path, "biologia.json"), "w", encoding="utf-8") as f:
        json.dump({nome_display: biologia}, f, indent=2, ensure_ascii=False)

    # 2. MANEJO_AVANCADO.JSON
    with open(os.path.join(base_path, "manejo_avancado.json"), "w", encoding="utf-8") as f:
        json.dump({nome_display: manejo}, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Cultura Gerada: {nome_display} em {base_path}")

# ==============================================================================
# 1. ALGODÃO (FIBRA) - Nível Consultoria
# ==============================================================================
bio_algodao = {
    "t_base": 15,
    "vars": {
        "FiberMax 985 GLTP": {"kc": 1.2, "gda_meta": 1650, "info": "Tecnologia TwinLink Plus. Ciclo Médio. Alta exigência de regulador (Pix)."},
        "TMG 44 B2RF": {"kc": 1.15, "gda_meta": 1580, "info": "Precoce. Ideal para fechamento. Monitorar Ramulária."}
    },
    "fases": {
        "B1 - Botão Floral": {
            "desc": "Primeiros botões (Pinhead square).",
            "fisiologia": "Início da fase reprodutiva. Planta sensível a abortamento.",
            "manejo": "Monitoramento de Bicudo (Bordadura) e Início do Regulador."
        },
        "F1 - Primeira Flor": {
            "desc": "Abertura da primeira flor branca.",
            "fisiologia": "Pico de demanda de Potássio e Água.",
            "manejo": "Controle preventivo de Ramulária e Lagartas."
        }
    }
}
man_algodao = {
    "fases": {
        "B1 - Botão Floral": {
            "quimica": [
                {"Alvo": "Bicudo (Bordadura)", "Ativo": "Malationa", "Tipo": "Químico Choque", "Estrategia": "Bateria 3x (3-5 dias) SOMENTE na borda. Foco em fêmeas migrantes."},
                {"Alvo": "Regulador", "Ativo": "Cloreto de Mepiquat", "Tipo": "Fisiológico", "Estrategia": "Dose baixa (50ml/ha) sequencial para travar internódio."}
            ]
        },
        "F1 - Primeira Flor": {
            "quimica": [
                {"Alvo": "Ramulária", "Ativo": "Azoxistrobina + Difenoconazol", "Tipo": "Sistêmico", "Estrategia": "Obrigatório uso de multissítio (Mancozebe) junto. Intervalo max 14 dias."},
                {"Alvo": "Lagarta das Maçãs", "Ativo": "Clorantraniliprole", "Tipo": "Seletivo", "Estrategia": "Proteção de longo residual."}
            ]
        }
    }
}

# ==============================================================================
# 2. MILHO (CEREAL)
# ==============================================================================
bio_milho = {
    "t_base": 10,
    "vars": {
        "Pioneer P3016 VYHR": {"kc": 1.2, "gda_meta": 1600, "info": "Híbrido Leptra. Defensivo. Responsivo a Fungicida."},
        "Agroceres AG 8780": {"kc": 1.18, "gda_meta": 1550, "info": "Precoce. Boa sanidade de colmo."}
    },
    "fases": {
        "V4 - Definição": {
            "desc": "4 folhas abertas (Colar visível).",
            "fisiologia": "Definição do nº de fileiras da espiga.",
            "manejo": "Controle de Cigarrinha e Percevejo Barriga-Verde."
        },
        "VT - Pendoamento": {
            "desc": "Pendão totalmente exposto.",
            "fisiologia": "Polinização. Fase crítica para estresse hídrico.",
            "manejo": "Aplicação de Fungicida (Terço Médio)."
        }
    }
}
man_milho = {
    "fases": {
        "V4 - Definição": {
            "quimica": [
                {"Alvo": "Cigarrinha (D. maidis)", "Ativo": "Acefato + Imidacloprido", "Tipo": "Químico Choque", "Estrategia": "Controle do vetor do Enfezamento. Rotação de ativos."},
                {"Alvo": "Percevejo", "Ativo": "Tiametoxam + Lambda", "Tipo": "Sistêmico", "Estrategia": "Evitar dominância e perfilhamento."}
            ]
        },
        "VT - Pendoamento": {
            "quimica": [
                {"Alvo": "Mancha Branca", "Ativo": "Trifloxistrobina + Protioconazol", "Tipo": "Sistêmico Premium", "Estrategia": "Aplicação aérea ou autopropelido. Foco em sanidade foliar."}
            ]
        }
    }
}

# ==============================================================================
# 3. CAFÉ (PERENE)
# ==============================================================================
bio_cafe = {
    "t_base": 18,
    "vars": {
        "Catuaí 144": {"kc": 1.0, "gda_meta": 2500, "info": "Porte baixo. Alta carga pendente. Exige nutrição."},
        "Mundo Novo": {"kc": 1.1, "gda_meta": 2600, "info": "Vigoroso. Rústico."}
    },
    "fases": {
        "Florada": {
            "desc": "Abertura das flores (Véu de noiva).",
            "fisiologia": "Fecundação e pegamento.",
            "manejo": "Controle de Phoma e Rosellinia."
        },
        "Chumbinho": {
            "desc": "Expansão dos frutos.",
            "fisiologia": "Enchimento de grão (Dreno).",
            "manejo": "Broca do Café e Ferrugem."
        }
    }
}
man_cafe = {
    "fases": {
        "Florada": {
            "quimica": [
                {"Alvo": "Phoma/Ascochyta", "Ativo": "Boscalida", "Tipo": "Sistêmico", "Estrategia": "Proteger botões florais em períodos frios e úmidos."}
            ]
        },
        "Chumbinho": {
            "quimica": [
                {"Alvo": "Broca do Café", "Ativo": "Clorantraniliprole", "Tipo": "Ingestão", "Estrategia": "Monitorar trânsito da broca. Aplicar se >3% de frutos broqueados."},
                {"Alvo": "Ferrugem", "Ativo": "Epoxiconazol + Piraclostrobina", "Tipo": "Sistêmico", "Estrategia": "Via foliar. Essencial para manter enfolhamento."}
            ]
        }
    }
}

# ==============================================================================
# 4. FEIJÃO (LEGUMINOSA)
# ==============================================================================
bio_feijao = {
    "t_base": 12,
    "vars": {
        "BRS Estilo": {"kc": 1.1, "gda_meta": 1100, "info": "Carioca. Porte ereto. Ciclo normal."},
        "BRS Pérola": {"kc": 1.15, "gda_meta": 1150, "info": "Tradicional. Grão grande. Sensível a doenças."}
    },
    "fases": {
        "V4 - Vegetativo": {
            "desc": "Terceira folha trifoliada aberta.",
            "fisiologia": "Rápido crescimento vegetativo.",
            "manejo": "Controle de Mosca Branca (Mosaico Dourado)."
        },
        "R6 - Floração": {
            "desc": "Abertura das primeiras flores.",
            "fisiologia": "Definição de vagens.",
            "manejo": "Antracnose e Mancha Angular."
        }
    }
}
man_feijao = {
    "fases": {
        "V4 - Vegetativo": {
            "quimica": [
                {"Alvo": "Mosca Branca", "Ativo": "Ciantraniliprole", "Tipo": "Sistêmico", "Estrategia": "Vetor de virose. Controle deve ser rigoroso na fase inicial."}
            ]
        },
        "R6 - Floração": {
            "quimica": [
                {"Alvo": "Antracnose", "Ativo": "Piraclostrobina", "Tipo": "Sistêmico", "Estrategia": "Proteger flores e vagens jovens. Doença que mancha o grão."}
            ]
        }
    }
}

# --- EXECUÇÃO ---
# Criando estrutura limpa e profissional
if __name__ == "__main__":
    print("🚜 Gerando Database Pro...")
    
    # Organizando por Categorias (O Data Engine acha tudo, mas fica organizado para você)
    criar_cultura("01_Graos/01_Soja", "Soja (Glycine max)", 
                  {"t_base":10, "vars":{"Intacta":{"kc":1},"Brasmax":{"kc":1}}, "fases":{"V3":{"desc":"Veg","fisiologia":"FBN","manejo":"Lagarta"},"R1":{"desc":"Flor","fisiologia":"Reprod","manejo":"Ferrugem"}}},
                  {"fases":{"V3":{"quimica":[{"Alvo":"Lagarta","Ativo":"Benzoato","Estrategia":"Bater Pano"}]},"R1":{"quimica":[{"Alvo":"Ferrugem","Ativo":"Protioconazol","Estrategia":"Preventivo"}]}}})
                  
    criar_cultura("01_Graos/02_Algodao", "Algodão (Gossypium hirsutum)", bio_algodao, man_algodao)
    criar_cultura("01_Graos/03_Milho", "Milho (Zea mays)", bio_milho, man_milho)
    criar_cultura("01_Graos/04_Feijao", "Feijão (Phaseolus vulgaris)", bio_feijao, man_feijao)
    criar_cultura("02_Perenes/01_Cafe", "Café (Coffea arabica)", bio_cafe, man_cafe)
    
    print("\n✅ Script Finalizado! 5 Culturas Base criadas.")
    print("👉 Próximo passo: Limpe o Cache (C) e Recarregue (R).")
