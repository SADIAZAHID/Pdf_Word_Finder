import fitz


def search_word(pdf_path, search_term):

    results = []
    total_matches = 0

    pdf = fitz.open(pdf_path)

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text()

        count = text.lower().count(search_term.lower())

        if count > 0:

            total_matches += count

            results.append({
                "page": page_number,
                "count": count,
                "text": text
            })

    pdf.close()

    return total_matches, results