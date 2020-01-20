from file_operations import read_lines
import sys

ignored_sequences = ['—', "«", '»', '"', '(', ')', '…', '–']

def get_tokens(lines, separator = ' '):
	return list(map(lambda line: line.split(separator)[0], lines))

if __name__ == "__main__":
	first_file = get_tokens(read_lines(sys.argv[1]))
	second_file = get_tokens(read_lines(sys.argv[2]))
	min_length = min(len(first_file), len(second_file))
	for i in range(min_length):
		if first_file[i] != second_file[i] and first_file[i] not in ignored_sequences:
			print(f'{i:4d}\t{first_file[i]:10s}\t{second_file[i]:10s}')
			break
