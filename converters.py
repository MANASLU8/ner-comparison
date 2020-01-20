from file_operations import read_lines

def get_labels(input_file):
    return list(map(lambda line: line.split(' ')[1], [i for i in read_lines(input_file) if i != '']))

def delete_prefixes(labels):
    return list(map(lambda label: label.split('-')[-1], labels))