def extract_handwriting_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)
        if pdf_reader.numPages < 2:
            return ''
        page = pdf_reader.getPage(1)
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                image = Image.frombytes('L', size, data)
                text = extract_handwriting(image)
                if handwriting_pattern.match(text):
                    return text
    return ''
