import fitz
import re
import pandas as pd
import configparser

# Carregar as configurações do arquivo config.ini
config = configparser.ConfigParser()
config.read('config.ini')

pdf_document = config.get('PDF', 'pdf_document')

# Resto do seu código permanece o mesmo
pdf = fitz.open(pdf_document)

stop_text = "Próxima fatura"

# Expressão regular para encontrar padrões de data, movimentação e valor
pattern = r'(\d{1,2} \w{3} \d{4})\n((?!VALOR TOTAL CARTÃO).+)\n(R\$ [\d.,]+)'  # Padrão para data, movimentação e valor

# Lista para armazenar os dados
table = []

for page_num in range(pdf.page_count):
    page = pdf.load_page(page_num)
    text = page.get_text("text")
    
    # Verificar se o texto de parada foi encontrado
    if stop_text in text:
        print(f"'{stop_text}' encontrado. Interrompendo a leitura.")
        break
    
    # Procurar padrões de dados da tabela na página
    matches = re.findall(pattern, text)
    
    # Verificar se os padrões foram encontrados e criar as entradas da tabela
    if matches:
        for match in matches:
            # Remover o "R$" do valor
            valor_sem_r = match[2].replace("R$ ", "")
            valor_sem_r = valor_sem_r.replace(",",".")
            
            row = {
                "Data": match[0],
                "Movimentação": match[1],
                "Valor": valor_sem_r
            }
            table.append(row)

# Criar um DataFrame pandas a partir da lista
df = pd.DataFrame(table)

# Exportar para um arquivo Excel
excel_file = "output.xlsx"  # Nome do arquivo Excel de saída
df.to_excel(excel_file, index=False)

# Mostrar a tabela no console (opcional)
print(df)

pdf.close()
