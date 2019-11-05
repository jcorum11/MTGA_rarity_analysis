def url_stripper(first_column, second_column, replacement): 
    first_column = first_column.astype('str')
    second_column = deck_type_urls.url.str.extract(replacement)
    second_column = second_column.str.replace('>', '')
    second_column = second_column.str.replace('<', '')
    second_column = second_column.str.strip()