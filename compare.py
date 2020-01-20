from average_precision import get_average_precision, get_weighted_average
import argparse, os
from file_operations import read_lines
from converters import get_labels, delete_prefixes
from printers import print_scores

def compare(reference, hypotheses):
    hypotheses_precision_scores = {}
    for key in hypotheses:
        hypothese_scores = {}
        labels = list(set(reference))   
        scores = get_average_precision(y_true=reference, y_pred=hypotheses[key], labels=labels, average=None)
        for label, score in zip(labels, scores):
            hypothese_scores[label] = score

        weighted_average = get_weighted_average(hypothese_scores, {label: hypotheses[key].count(label) for label in labels})

        hypothese_scores['weighted-average'] = weighted_average
        hypothese_scores['unweighted-average'] = get_average_precision(y_true=reference, y_pred=hypotheses[key], labels=labels, average='macro')
        hypothese_scores['micro-average'] = get_average_precision(y_true=reference, y_pred=hypotheses[key], labels=labels, average='micro')

        hypotheses_precision_scores[key] = hypothese_scores
    return {'precision': hypotheses_precision_scores}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--reference_file', type=str, default='eval.tagged.txt')
    parser.add_argument('--hypotheses_dir', type=str, default='.')

    args = parser.parse_args()

    reference_labels = get_labels(args.reference_file)

    prefix_sensitive_hypotheses = {}
    prefix_agnostic_hypotheses = {}
    reference_path_splitted = args.reference_file.split('/')[-1].split('.')
    for path in os.listdir(args.hypotheses_dir):
        hypothesis_path_splitted = path.split('.')
        flagged_path = [1 if item in reference_path_splitted else 0 for item in hypothesis_path_splitted]
        if (sum(flagged_path) == len(flagged_path) - 1) and (sum(flagged_path) == len(reference_path_splitted)):
            hypothese_labels = get_labels(path)
            prefix_sensitive_hypotheses[hypothesis_path_splitted[flagged_path.index(0)]] = hypothese_labels
            prefix_agnostic_hypotheses[hypothesis_path_splitted[flagged_path.index(0)]] = delete_prefixes(hypothese_labels)

    scores = {'prefix-sensitive': compare(reference_labels, prefix_sensitive_hypotheses), 'prefix-agnostic': compare(delete_prefixes(reference_labels), prefix_agnostic_hypotheses)}
    print_scores(scores)
