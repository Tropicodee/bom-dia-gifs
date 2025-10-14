import os
import json
import unicodedata
import re

def padronizar_nome(nome):
    """Remove acentos, espaços e caracteres especiais de nomes"""
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome = nome.replace(" ", "_").replace("-", "_")
    nome = re.sub(r'[^\w_.]', '', nome)  # mantém apenas letras, números, underscore e ponto
    return nome.lower()

def gerar_nome_unico(nome_base, nomes_existentes):
    """Gera um nome único adicionando sufixo incremental (_1, _2, etc)"""
    if nome_base not in nomes_existentes:
        return nome_base
    contador = 1
    nome_sem_ext, ext = os.path.splitext(nome_base)
    novo_nome = f"{nome_sem_ext}_{contador}{ext}"
    while novo_nome in nomes_existentes:
        contador += 1
        novo_nome = f"{nome_sem_ext}_{contador}{ext}"
    return novo_nome

# Caminho raiz onde estão as pastas gif/ e imagens/
ROOT_PATH = "C:\\Users\\91mar\\Downloads\\bom-dia-gifs"  # ALTERE para seu caminho local

# 🔧 Configurações principais
GITHUB_USER = "Tropicodee"
REPO_NAME = "bom-dia-gifs"
BRANCH = "master"

BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"

FOLDERS = ["gif", "imagens"]

manifest = {
    "version": "2",
    "gif": {},
    "imagens": {}
}

for folder in FOLDERS:
    folder_path = os.path.join(ROOT_PATH, folder)
    if not os.path.exists(folder_path):
        print(f"Pasta não encontrada: {folder_path}")
        continue

    for category in os.listdir(folder_path):
        category_path = os.path.join(folder_path, category)
        if os.path.isdir(category_path):
            files = []
            nome_categoria = padronizar_nome(category)

            nomes_existentes = set()

            for file in os.listdir(category_path):
                if file.startswith("."):
                    continue

                arquivo_padronizado = padronizar_nome(file)
                nome_unico = gerar_nome_unico(arquivo_padronizado, nomes_existentes)
                nomes_existentes.add(nome_unico)

                antigo = os.path.join(category_path, file)
                novo = os.path.join(category_path, nome_unico)

                # Renomeia localmente se necessário
                if antigo != novo:
                    if not os.path.exists(novo):
                        print(f"Renomeando {file} → {os.path.basename(novo)}")
                        os.rename(antigo, novo)
                    else:
                        print(f"Arquivo já existe, mantendo nome único: {os.path.basename(novo)}")

                # Gera URL para o JSON
                url = f"{BASE_URL}/{folder}/{nome_categoria}/{nome_unico}"
                files.append(url)

            manifest[folder][nome_categoria] = files

# Salva o JSON final
output_path = os.path.join(ROOT_PATH, "conteudo.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"\n✅ conteudo.json gerado com sucesso em {output_path}")
