import fitz  # PyMuPDF
import io
from PIL import Image
import os

# --- Configuração ---
# Crie uma pasta para salvar as imagens extraídas
OUTPUT_IMAGE_DIR = "extracted_images"
if not os.path.exists(OUTPUT_IMAGE_DIR):
    os.makedirs(OUTPUT_IMAGE_DIR)


def get_image_description(image_bytes: bytes) -> str:
    """
    Esta é a função que se comunicará com um modelo de visão.
    Por enquanto, ela apenas retorna um placeholder.
    """
    # TODO: Implementar a chamada para a API de visão (ex: OpenAI GPT-4o)
    # from openai import OpenAI
    # client = OpenAI(api_key="SUA_CHAVE_API")
    # ... chamada da API ...
    return "[Descrição da imagem pendente]"

def process_pdf(pdf_path: str) -> str:
    """
    Processa um único arquivo PDF, extraindo texto e descrevendo imagens.

    Args:
        pdf_path: O caminho para o arquivo PDF.

    Returns:
        Uma string contendo todo o texto consolidado do PDF.
    """
    print(f"Processando PDF: {pdf_path}...")
    doc = fitz.open(pdf_path)
    consolidated_text = ""

    for page_num, page in enumerate(doc):
        # 1. Extrair texto da página
        consolidated_text += f"--- Página {page_num + 1} ---\n"
        consolidated_text += page.get_text()
        consolidated_text += "\n"

        # 2. Extrair imagens da página
        image_list = page.get_images(full=True)
        if image_list:
            consolidated_text += f"\n[IMAGENS ENCONTRADAS NA PÁGINA {page_num + 1}]\n"

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Obter descrição da imagem (atualmente um placeholder)
            description = get_image_description(image_bytes)
            
            consolidated_text += f"- Imagem {img_index + 1}: {description}\n"

            # Opcional: Salvar a imagem em disco para verificação
            image_ext = base_image["ext"]
            image_filename = f"{os.path.basename(pdf_path)}_p{page_num+1}_img{img_index+1}.{image_ext}"
            image_path = os.path.join(OUTPUT_IMAGE_DIR, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            # print(f"  - Imagem salva em: {image_path}")

    doc.close()
    print("Processamento concluído.")
    return consolidated_text

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Encontre um PDF no seu workspace para testar
    # Vou usar um que vi na sua estrutura de arquivos.
    # Adapte o caminho se necessário.
    test_pdf_path = "DH.pdf"
    
    if os.path.exists(test_pdf_path):
        full_text_content = process_pdf(test_pdf_path)
        
        # Salva o resultado em um arquivo de texto para análise
        output_txt_filename = f"{os.path.basename(test_pdf_path)}.txt"
        with open(output_txt_filename, "w", encoding="utf-8") as f:
            f.write(full_text_content)
            
        print(f"\nConteúdo extraído e salvo em '{output_txt_filename}'")
        # print("\n--- CONTEÚDO EXTRAÍDO ---")
        # print(full_text_content)
    else:
        print(f"Arquivo de teste não encontrado em: {test_pdf_path}")
        print("Por favor, ajuste a variável 'test_pdf_path' no final do script para um PDF existente.")

