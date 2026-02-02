import os
import json

# Define o caminho específico para GRÃOS -> SOJA
# Mantemos a estrutura organizada por categorias
PATH_DIR = os.path.join("database", "01_Graos")
FILE_NAME = "soja.json"

def gerar_soja_master():
    print("🚜 Gerando Módulo de Inteligência: SOJA MASTER...")

    dados_soja = {
      "Soja (Glycine max)": {
        "t_base": 10,
        "vars": {
          "Intacta 2 Xtend (I2X)": { 
              "kc": 1.15, 
              "gda_meta": 1380, 
              "info": "Plataforma Biotecnológica tolerante a Dicamba e Glifosato. Alta produtividade. Exige manejo de refúgio estruturado. Atenção a lagartas não-alvo (Spodoptera)." 
          },
          "Brasmax Zeus": { 
              "kc": 1.20, 
              "gda_meta": 1400, 
              "info": "Material de ciclo precoce/médio com alto PMG (Peso de Mil Grãos). Exige fertilidade de solo alta e proteção fungicida robusta." 
          },
          "FT Sementes (Convencional)": {
              "kc": 1.15,
              "gda_meta": 1350,
              "info": "Soja não-transgênica. Exige manejo de lagartas à moda antiga (Monitoramento constante). Prêmio financeiro na venda (Bônus)."
          }
        },
        "fases": {
          
          # --- FASE 1: ESTABELECIMENTO ---
          "VE - Emergência (TS)": {
            "desc": "Cotilédones acima do solo.",
            "fisiologia": "Absorção de reservas da semente. Fase crítica para estande.",
            "manejo": "Tratamento de Sementes Industrial (TSI) é mandatório para alto teto.",
            "quimica": [
              {
                "Alvo": "Damping-off (Tombamento)",
                "Ativo": "Carboxina + Tiram",
                "Grupo": "Carboxamida",
                "Tipo": "Tratamento de Sementes (TS)",
                "Estrategia": "Blindagem contra Rhizoctonia e Pythium. O Tiram age por contato (solo) e Carboxina penetra na plântula."
              },
              {
                "Alvo": "Fixação Biológica (FBN)",
                "Ativo": "Bradyrhizobium japonicum",
                "Grupo": "Bactéria",
                "Tipo": "Biológico",
                "Estrategia": "Inoculação TURBO (Líquida no sulco + Turfa na semente). NÃO aplicar fungicida ou micronutrientes direto sobre a bactéria."
              },
              {
                "Alvo": "Nematoides/Pragas Iniciais",
                "Ativo": "Abamectina + Tiodicarbe",
                "Grupo": "Avermectina",
                "Tipo": "TS Nematicida",
                "Estrategia": "Proteção do sistema radicular jovem contra nematoides de galha e cisto nos primeiros 20 dias."
              }
            ]
          },

          # --- FASE 2: VEGETATIVO ---
          "V3 - Terceiro Trifólio": {
            "desc": "Três folhas trifoliadas abertas.",
            "fisiologia": "Início da nodulação ativa (FBN). Planta define potencial de ramificação.",
            "manejo": "Limpeza da lavoura (Herbicida) e Proteção contra Lagartas.",
            "quimica": [
              {
                "Alvo": "Ervas (Amargoso/Buva)",
                "Ativo": "Glifosato + Cletodim",
                "Grupo": "EPSPS + ACCase",
                "Tipo": "Herbicida Sistêmico",
                "Estrategia": "Aplicação sequencial se a touceira for grande. Cuidado com o efeito 'falso-controle' em dias nublados."
              },
              {
                "Alvo": "Lagartas (Spodoptera/Helicoverpa)",
                "Ativo": "Benzoato de Emamectina",
                "Grupo": "Avermectina",
                "Tipo": "Químico Ingestão",
                "Estrategia": "Entrar apenas se desfolha > 20% ou corte de plantas. Rotacionar com Clorfenapir para manejo de resistência."
              },
              {
                "Alvo": "Reforço FBN",
                "Ativo": "Cobalto (Co) + Molibdênio (Mo)",
                "Grupo": "Micronutrientes",
                "Tipo": "Nutricional",
                "Estrategia": "O Molibdênio é cofator da enzima Nitrogenase. Essencial para transformar N2 em NH3."
              }
            ]
          },

          # --- FASE 3: REPRODUTIVO INICIAL ---
          "R1 - Início Floração": {
            "desc": "Uma flor aberta em qualquer nó.",
            "fisiologia": "Parada do crescimento radicular. Alta demanda de Boro para viabilidade do pólen.",
            "manejo": "Aplicação ZERO (Fungicida Preventivo). O Baixeiro é salvo aqui.",
            "quimica": [
              {
                "Alvo": "Ferrugem Asiática / Mancha Alvo",
                "Ativo": "Protioconazol + Trifloxistrobina",
                "Grupo": "Triazolinthiona + Estrobirulina",
                "Tipo": "Sistêmico Premium",
                "Estrategia": "Aplicação MANDATÓRIA independente de sintomas. É a aplicação mais importante da safra para proteger o baixeiro."
              },
              {
                "Alvo": "Reforço (Protetor)",
                "Ativo": "Mancozebe ou Clorotalonil",
                "Grupo": "Ditiocarbamato",
                "Tipo": "Multissítio",
                "Estrategia": "Parceiro obrigatório dos sistêmicos para evitar resistência do fungo. Cria uma capa protetora na folha."
              }
            ]
          },

          # --- FASE 4: ENCHIMENTO DE GRÃOS ---
          "R5.1 - Início Enchimento": {
            "desc": "Grãos perceptíveis ao tato (3mm).",
            "fisiologia": "Translocação total de fotoassimilados das folhas para o grão. Dreno forte.",
            "manejo": "Controle de Percevejos (Dano Direto) e Antracnose.",
            "quimica": [
              {
                "Alvo": "Percevejo Marrom (Euschistus)",
                "Ativo": "Acefato + Imidacloprido",
                "Grupo": "Organofosforado + Neonicotinoide",
                "Tipo": "Choque + Residual",
                "Estrategia": "O Acefato derruba a população adulta, o Imidacloprido segura a reinfestação. Nível de dano: 1 percevejo/m."
              },
              {
                "Alvo": "Doenças de Final de Ciclo",
                "Ativo": "Picoxistrobina + Ciproconazol",
                "Grupo": "Estrob + Triazol",
                "Tipo": "Sistêmico",
                "Estrategia": "Manter a folha verde pelo maior tempo possível (Stay Green) para aumentar peso de grão."
              }
            ]
          },

          # --- FASE 5: MATURAÇÃO ---
          "R7.1 - Início Maturação": {
            "desc": "Inicio do amarelecimento de folhas e vagens.",
            "fisiologia": "Desligamento vascular. Grão atinge peso máximo fisiológico.",
            "manejo": "Dessecação para colheita (Uniformização).",
            "quimica": [
              {
                "Alvo": "Dessecação (Pré-Colheita)",
                "Ativo": "Diquat",
                "Grupo": "Fotossistema I",
                "Tipo": "Herbicida Contato",
                "Estrategia": "Aplicar quando a umidade do grão estiver próxima a 18-20% para antecipar colheita. Exige boa cobertura (gotas)."
              }
            ]
          }
        }
      }
    }

    # Criar pasta se não existir
    os.makedirs(PATH_DIR, exist_ok=True)
    
    # Caminho completo
    full_path = os.path.join(PATH_DIR, FILE_NAME)

    # Gravação UTF-8
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(dados_soja, f, indent=2, ensure_ascii=False)
    
    print(f"✅ SUCESSO! Soja Enterprise gerada em: {full_path}")
    print("👉 Agora no App: Limpe Cache (C) e Recarregue (R).")

if __name__ == "__main__":
    gerar_soja_master()
