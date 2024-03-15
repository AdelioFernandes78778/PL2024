import re

def markdown_to_html(md_text):
    # Cabeçalhos
    md_text = re.sub(r'^#\s(.*)', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^##\s(.*)', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^###\s(.*)', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)

    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md_text)

    # Itálico
    md_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', md_text)

    # Lista numerada
    md_text = re.sub(r'^(\d+)\.\s(.*?)$', r'<ol>\n<li>\2</li>\n</ol>', md_text, flags=re.MULTILINE)

    # Lista não numerada
    md_text = re.sub(r'^-\s(.*?)$', r'<ul>\n<li>\1</li>\n</ul>', md_text, flags=re.MULTILINE)

    # Links
    md_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md_text)

    # Imagens
    md_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', md_text)

    return md_text

# Exemplo de uso:
markdown_text = """
# Título
Este é um **exemplo** de conversão de Markdown para HTML.

## Subtítulo
Aqui está um link para [página da UC](http://www.uc.pt).

- Item 1
- Item 2

![Coelho](http://www.coelho.com)
"""
html_output = markdown_to_html(markdown_text)
print(html_output)
