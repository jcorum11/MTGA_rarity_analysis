def url_stripper(data, old_column, new_column_name, replacement): 
    data[old_column] = data[old_column].astype('str')
    data[new_column_name] = data[old_column].str.extract(replacement)
    data[new_column_name] = data[new_column_name].str.replace('>', '')
    data[new_column_name] = data[new_column_name].str.replace('<', '')
    data[new_column_name] = data[new_column_name].str.strip()


