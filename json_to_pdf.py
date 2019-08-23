import json
from io import BytesIO

from pdfdocument.document import PDFDocument

if __name__ == "__main__":
    with open('elpais_mvm.json') as json_file:
        articles = json.load(json_file)

    f = BytesIO()
    pdf = PDFDocument(f)
    pdf.init_report()
    for article in articles:
        pdf.h1(article['title'])
        pdf.smaller(article['date'])
        pdf.p(article['content'])
        pdf.h3('Tags')
        pdf.smaller(', '.join(article['tags']))
        pdf.next_frame()
    pdf.generate()

    with open('mvm_articles.pdf', 'w') as file:
        file.write(f.getvalue())
