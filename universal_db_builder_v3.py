import os
import json
import shutil

# --- CONFIGURAÇÃO ---
NOVA_DB = "database"
DB_ANTIGA = "database_BKP_OLD"

def montar_dados_cultura(nome_cultura, t_base, variedades, fases_protocolos):
    """Construtor padronizado de módulos agronômicos."""
    genetica = {"cultura": nome_cultura, "t_base": t_base, "variedades": variedades}
    fenologia = {"fases": {}}
    protocolos = {}
    
    for cod, dados in fases_protocolos.items():
        fenologia["fases"][cod] = {
            "nome": dados["nome"], "desc": dados["desc"],
            "fisiologia": dados["fisiologia"], "manejo": dados["manejo"]
        }
        if "quimica" in dados: protocolos[cod] = dados["quimica"]
            
    return genetica, fenologia, protocolos

# ==============================================================================
# BASE DE DADOS AGRONÔMICA MASSIVA (16 CULTURAS)
# ==============================================================================
CULTURAS_DATA = {
    
    # ------------------------------------------------------------------
    # GRUPO 1: GRÃOS E CEREAIS
    # ------------------------------------------------------------------
    "01_Graos": {
        "01_Algodao": montar_dados_cultura(
            "Algodão (Gossypium hirsutum)", 15,
            {"FiberMax GLTP": {"kc": 1.2, "info": "Tecnologia TwinLink. Exige regulador."}, "TMG 44 B2RF": {"kc": 1.15, "info": "Precoce."}},
            {
                "B1": {"nome": "B1 - Botão Floral", "desc": "Pinhead (Cabeça de alfinete).", "fisiologia": "Início reprodutivo.", "manejo": "Monitorar Bicudo (Borda).",
                       "quimica": [{"Alvo": "Bicudo", "Ativo": "Malationa", "Tipo": "Químico", "Estrategia": "Bateria 3x (3-5 dias) na bordadura."},
                                   {"Alvo": "Regulador", "Ativo": "Mepiquat", "Tipo": "Fisio", "Estrategia": "Dose baixa (50ml) sequencial."}]},
                "F1": {"nome": "F1 - Primeira Flor", "desc": "Flor branca.", "fisiologia": "Pico hídrico.", "manejo": "Ramulária (Preventivo).",
                       "quimica": [{"Alvo": "Ramulária", "Ativo": "Azoxistrobina + Ciproconazol", "Tipo": "Sistêmico", "Estrategia": "Preventivo obrigatório + Protetor."}]}
            }
        ),
        "02_Feijao": montar_dados_cultura(
            "Feijão (Phaseolus vulgaris)", 12,
            {"BRS Estilo": {"kc": 1.1, "info": "Carioca. Ereto."}, "Pérola": {"kc": 1.15, "info": "Tradicional."}},
            {
                "V4": {"nome": "V4 - Terceira Folha", "desc": "Vegetativo pleno.", "fisiologia": "Ramificação.", "manejo": "Mosca Branca (Mosaico).",
                       "quimica": [{"Alvo": "Mosca Branca", "Ativo": "Ciantraniliprole", "Tipo": "Sistêmico", "Estrategia": "Evitar transmissão de virose (Mosaico Dourado)."}]},
                "R6": {"nome": "R6 - Floração", "desc": "Primeiras flores.", "fisiologia": "Abortamento se stress.", "manejo": "Antracnose/Mancha Angular.",
                       "quimica": [{"Alvo": "Antracnose", "Ativo": "Piraclostrobina", "Tipo": "Sistêmico", "Estrategia": "Proteção de flores e vagens jovens."}]}
            }
        ),
        "03_Milho": montar_dados_cultura(
            "Milho (Zea mays)", 10,
            {"Pioneer P3016": {"kc": 1.2, "info": "Leptra. Defensivo."}, "Agroceres 8780": {"kc": 1.18, "info": "Rústico."}},
            {
                "V4": {"nome": "V4 - Definição", "desc": "4 folhas.", "fisiologia": "Define nº fileiras.", "manejo": "Cigarrinha (Enfezamento).",
                       "quimica": [{"Alvo": "Cigarrinha", "Ativo": "Metomil / Acefato", "Tipo": "Choque", "Estrategia": "Rotação de ativos. Controle vetor."}]},
                "VT": {"nome": "VT - Pendoamento", "desc": "Pendão.", "fisiologia": "Polinização.", "manejo": "Fungicida foliar.",
                       "quimica": [{"Alvo": "Mancha Branca", "Ativo": "Trifloxistrobina", "Tipo": "Sistêmico", "Estrategia": "Proteger terço médio superior."}]}
            }
        ),
        "04_Trigo": montar_dados_cultura(
            "Trigo (Triticum aestivum)", 8,
            {"TBIO Toruk": {"kc": 1.1, "info": "Branqueador."}, "ORS Vigor": {"kc": 1.05, "info": "Precoce."}},
            {
                "Perfilhamento": {"nome": "Perfilhamento", "desc": "Emissão afilhos.", "fisiologia": "Define espigas/m².", "manejo": "Pulgão.",
                                  "quimica": [{"Alvo": "Pulgão", "Ativo": "Imidacloprido", "Tipo": "Sistêmico", "Estrategia": "Evitar Nanismo Amarelo (Virose)."}]},
                "Espigamento": {"nome": "Espigamento", "desc": "Espiga exposta.", "fisiologia": "Antese.", "manejo": "Giberela (Fusarium).",
                                "quimica": [{"Alvo": "Giberela", "Ativo": "Tebuconazol", "Tipo": "Sistêmico", "Estrategia": "Aplicar se houver previsão de chuva na flor."}]}
            }
        ),
    },

    # ------------------------------------------------------------------
    # GRUPO 2: HORTIFRUTI (HF) & VEGETAIS
    # ------------------------------------------------------------------
    "02_Hortifruti": {
        "01_Alho": montar_dados_cultura(
            "Alho (Allium sativum)", 7,
            {"Ito": {"kc": 1.05, "info": "Roxo nobre."}, "Caçador": {"kc": 1.0, "info": "Virus Free."}},
            {
                "Vegetativo": {"nome": "Desenv. Vegetativo", "desc": "Emissão de folhas.", "fisiologia": "Acúmulo reservas.", "manejo": "Tripes e Ácaro.",
                               "quimica": [{"Alvo": "Tripes", "Ativo": "Spinetoram", "Tipo": "Seletivo", "Estrategia": "Atingir bainha das folhas."}]},
                "Bulbificacao": {"nome": "Bulbificação", "desc": "Estalo.", "fisiologia": "Translocação.", "manejo": "Mancha Púrpura/Ferrugem.",
                                 "quimica": [{"Alvo": "Mancha Púrpura", "Ativo": "Iprodiona", "Tipo": "Contato", "Estrategia": "Alternar com Tebuconazol."}]}
            }
        ),
        "02_Batata": montar_dados_cultura(
            "Batata (Solanum tuberosum)", 12,
            {"Agata": {"kc": 1.15, "info": "Pele lisa."}, "Asterix": {"kc": 1.1, "info": "Indústria (Frita)."}},
            {
                "Tuberizacao": {"nome": "Início Tuberização", "desc": "Gancho nos estolões.", "fisiologia": "Dreno forte.", "manejo": "Requeima (Phytophthora).",
                                "quimica": [{"Alvo": "Requeima", "Ativo": "Fluazinam", "Tipo": "Protetor", "Estrategia": "Blindagem total antes de chuvas."},
                                            {"Alvo": "Requeima (Curativo)", "Ativo": "Metalaxil-M", "Tipo": "Sistêmico", "Estrategia": "Apenas se houver sintoma ativo."}]}
            }
        ),
        "03_Cebola": montar_dados_cultura(
            "Cebola (Allium cepa)", 10,
            {"Bella Dura": {"kc": 1.05, "info": "Ciclo médio."}, "Crioula": {"kc": 1.0, "info": "Armazenamento."}},
            {
                "Crescimento": {"nome": "Fase 5-7 Folhas", "desc": "Planta ereta.", "fisiologia": "Expansão foliar.", "manejo": "Tripes e Míldio.",
                                "quimica": [{"Alvo": "Tripes", "Ativo": "Clorfenapir", "Tipo": "Contato", "Estrategia": "Alta pressão, rotacionar mecanismo."},
                                            {"Alvo": "Míldio", "Ativo": "Mancozebe + Metalaxil", "Tipo": "Sistêmico", "Estrategia": "Preventivo em noites frias/úmidas."}]}
            }
        ),
        "04_Tomate": montar_dados_cultura(
            "Tomate (Solanum lycopersicum)", 15,
            {"Italiano": {"kc": 1.15, "info": "Mesa."}, "Saladete": {"kc": 1.1, "info": "Rústico."}},
            {
                "Vegetativo": {"nome": "Desenv. Vegetativo", "desc": "Crescimento haste.", "fisiologia": "Vigor.", "manejo": "Traça (Tuta) e Mosca.",
                               "quimica": [{"Alvo": "Traça (Tuta absoluta)", "Ativo": "Clorantraniliprole", "Tipo": "Sistêmico", "Estrategia": "Monitorar galerias. Rotacionar com Bt."}]},
                "Floracao": {"nome": "Floração/Pegamento", "desc": "Cachos florais.", "fisiologia": "Cálcio exigente.", "manejo": "Requeima e Pinta Preta.",
                             "quimica": [{"Alvo": "Requeima", "Ativo": "Mandipropamida", "Tipo": "Sistêmico", "Estrategia": "Alta especificidade para Oomicetos."}]}
            }
        ),
    },

    # ------------------------------------------------------------------
    # GRUPO 3: FRUTAS (PREMIUM)
    # ------------------------------------------------------------------
    "03_Frutas": {
        "01_Banana": montar_dados_cultura(
            "Banana (Musa spp.)", 22,
            {"Prata": {"kc": 1.1, "info": "Mercado interno."}, "Nanica": {"kc": 1.2, "info": "Exportação."}},
            {
                "Cacho": {"nome": "Emissão do Cacho", "desc": "Coração visível.", "fisiologia": "Definição pencas.", "manejo": "Sigatoka Negra e Tripes.",
                          "quimica": [{"Alvo": "Sigatoka Negra", "Ativo": "Mancozeb + Tebuconazol", "Tipo": "Sistêmico", "Estrategia": "Manejo de resistência com óleo mineral."},
                                      {"Alvo": "Tripes da Flor", "Ativo": "Spinosad", "Tipo": "Biológico/Seletivo", "Estrategia": "Injeção no coração ou pulverização do cacho."}]}
            }
        ),
        "02_Citros": montar_dados_cultura(
            "Citros (Limão/Laranja)", 13,
            {"Tahiti": {"kc": 0.9, "info": "Limão."}, "Pera Rio": {"kc": 0.95, "info": "Laranja."}},
            {
                "Brotacao": {"nome": "Fluxo Vegetativo", "desc": "Folhas novas (Tenras).", "fisiologia": "Atrativo para vetores.", "manejo": "Psilídeo (Greening) e Minadora.",
                             "quimica": [{"Alvo": "Psilídeo (Diaphorina)", "Ativo": "Imidacloprido + Bifentrina", "Tipo": "Sistêmico+Contato", "Estrategia": "TOLERÂNCIA ZERO. Monitorar brotações."},
                                         {"Alvo": "Minadora", "Ativo": "Abamectina", "Tipo": "Translaminar", "Estrategia": "Aplicar ao notar galerias iniciais."}]}
            }
        ),
        "03_Framboesa": montar_dados_cultura(
            "Framboesa (Rubus idaeus)", 10,
            {"Heritage": {"kc": 1.0, "info": "Reflorescente."}, "Autumn Bliss": {"kc": 1.0, "info": "Tardia."}},
            {
                "Floracao": {"nome": "Floração", "desc": "Botões brancos.", "fisiologia": "Polinização (Abelhas).", "manejo": "Botrytis e Ácaro.",
                             "quimica": [{"Alvo": "Mofo Cinzento (Botrytis)", "Ativo": "Fenhexamida", "Tipo": "Específico", "Estrategia": "Aplicação preventiva. Cuidado com carência."},
                                         {"Alvo": "Ácaro Rajado", "Ativo": "Bifenazato", "Tipo": "Contato", "Estrategia": "Evitar piretroides para não matar predadores."}]}
            }
        ),
        "04_Manga": montar_dados_cultura(
            "Manga (Mangifera indica)", 20,
            {"Palmer": {"kc": 1.0, "info": "Exportação."}, "Tommy": {"kc": 1.1, "info": "Resistente."}},
            {
                "Inducao": {"nome": "Indução Floral", "desc": "Aplicação PBZ.", "fisiologia": "Parada vegetativa.", "manejo": "Antracnose.",
                            "quimica": [{"Alvo": "Indutor Floral", "Ativo": "Paclobutrazol (PBZ)", "Tipo": "Fisiológico", "Estrategia": "Aplicação via solo (Drench) conforme copa."},
                                        {"Alvo": "Antracnose", "Ativo": "Difenoconazol", "Tipo": "Sistêmico", "Estrategia": "Proteger panícula floral."}]}
            }
        ),
        "05_Mirtilo": montar_dados_cultura(
            "Mirtilo (Vaccinium spp.)", 12,
            {"Biloxi": {"kc": 0.9, "info": "Baixo frio."}, "Emerald": {"kc": 1.0, "info": "Vigorosa."}},
            {
                "Brotacao": {"nome": "Brotação/Floração", "desc": "Novos ramos.", "fisiologia": "Sensível pH.", "manejo": "Ferrugem e Botrytis.",
                             "quimica": [{"Alvo": "Ferrugem", "Ativo": "Azoxistrobina", "Tipo": "Sistêmico", "Estrategia": "Preventivo em folhas novas."}]}
            }
        ),
        "06_Morango": montar_dados_cultura(
            "Morango (Fragaria x ananassa)", 12,
            {"Albion": {"kc": 0.95, "info": "Dia neutro."}, "Camarosa": {"kc": 1.0, "info": "Dia curto."}},
            {
                "Producao": {"nome": "Frutificação Plena", "desc": "Flores e frutos.", "fisiologia": "Dreno contínuo.", "manejo": "Ácaro e Botrytis.",
                             "quimica": [{"Alvo": "Ácaro Rajado", "Ativo": "Abamectina ou Neoseiulus (Bio)", "Tipo": "Acaricida", "Estrategia": "Alta pressão. Rotacionar mecanismo."},
                                         {"Alvo": "Mofo Cinzento", "Ativo": "Iprodiona", "Tipo": "Contato", "Estrategia": "Evitar molhamento foliar excessivo."}]}
            }
        ),
        "07_Uva": montar_dados_cultura(
            "Uva (Vitis vinifera)", 12,
            {"Niágara": {"kc": 0.9, "info": "Mesa Rústica."}, "Chardonnay": {"kc": 1.0, "info": "Vinho Fino."}},
            {
                "Brotacao": {"nome": "Brotação", "desc": "Ponta verde.", "fisiologia": "Ativação.", "manejo": "Antracnose (Pérola).",
                             "quimica": [{"Alvo": "Antracnose", "Ativo": "Mancozebe", "Tipo": "Contato", "Estrategia": "Protetor essencial nos brotos novos."}]},
                "Compactacao": {"nome": "Compactação Cacho", "desc": "Grão ervilha.", "fisiologia": "Enchimento.", "manejo": "Míldio e Oídio.",
                                "quimica": [{"Alvo": "Míldio", "Ativo": "Metalaxil-M + Mancozebe", "Tipo": "Sistêmico", "Estrategia": "Preventivo em clima úmido."},
                                            {"Alvo": "Podridão da Uva", "Ativo": "Pirimetanil", "Tipo": "Específico", "Estrategia": "Preventivo antes do fechamento do cacho."}]}
            }
        ),
    },

    # ------------------------------------------------------------------
    # GRUPO 4: PERENES
    # ------------------------------------------------------------------
    "04_Perenes": {
        "01_Cafe": montar_dados_cultura(
            "Café (Coffea arabica)", 18,
            {"Catuaí 144": {"kc": 1.0, "info": "Produtivo."}, "Mundo Novo": {"kc": 1.1, "info": "Vigoroso."}},
            {
                "Florada": {"nome": "Florada Principal", "desc": "Véu de noiva.", "fisiologia": "Fecundação.", "manejo": "Phoma e Rosellinia.",
                            "quimica": [{"Alvo": "Phoma/Ascochyta", "Ativo": "Boscalida", "Tipo": "Sistêmico", "Estrategia": "Proteger botões florais e chumbinhos."}]},
                "Granacao": {"nome": "Granação/Maturação", "desc": "Fruto verde/cereja.", "fisiologia": "Enchimento.", "manejo": "Broca e Ferrugem.",
                             "quimica": [{"Alvo": "Broca do Café", "Ativo": "Clorantraniliprole", "Tipo": "Ingestão", "Estrategia": "Monitorar trânsito da broca (fruto verde)."},
                                         {"Alvo": "Ferrugem", "Ativo": "Epoxiconazol + Piraclostrobina", "Tipo": "Sistêmico", "Estrategia": "Via foliar preventiva."}]}
            }
        ),
    }
}

# ==============================================================================
# EXECUÇÃO: BUILDER
# ==============================================================================
def construir_database_v3():
    print("="*60)
    print("🚜 CONSTRUINDO BASE DE DADOS ENTERPRISE V3 (16 CULTURAS)")
    print("="*60)

    # 1. Backup e Limpeza
    if os.path.exists(NOVA_DB):
        if os.path.exists(DB_ANTIGA): shutil.rmtree(DB_ANTIGA)
        shutil.move(NOVA_DB, DB_ANTIGA)
        print(f"📦 Backup realizado: {DB_ANTIGA}")
    
    os.makedirs(NOVA_DB)

    # 2. Criação Modular
    for categoria, culturas in CULTURAS_DATA.items():
        path_cat = os.path.join(NOVA_DB, categoria)
        os.makedirs(path_cat, exist_ok=True)
        
        for codigo_cultura, (gen, fen, prot) in culturas.items():
            path_cultura = os.path.join(path_cat, codigo_cultura)
            os.makedirs(path_cultura, exist_ok=True)
            
            # Escreve os 3 arquivos JSON
            with open(os.path.join(path_cultura, "1_genetica.json"), "w", encoding='utf-8') as f:
                json.dump(gen, f, indent=2, ensure_ascii=False)
            with open(os.path.join(path_cultura, "2_fenologia.json"), "w", encoding='utf-8') as f:
                json.dump(fen, f, indent=2, ensure_ascii=False)
            with open(os.path.join(path_cultura, "3_protocolos.json"), "w", encoding='utf-8') as f:
                json.dump(prot, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Gerado: {gen['cultura']}")

    print("="*60)
    print("🎉 ENCICLOPÉDIA AGRONÔMICA CRIADA COM SUCESSO!")
    print("👉 Passo final: Limpe o Cache (Tecla C) e Recarregue (Tecla R).")

if __name__ == "__main__":
    construir_database_v3()
