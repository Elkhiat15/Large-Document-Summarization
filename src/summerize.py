import Doc

doc = Doc.Document()
doc.load_from_pdf('./Books/Cover Letter.pdf')
cleaned_text = doc.data

print(cleaned_text[:30])

