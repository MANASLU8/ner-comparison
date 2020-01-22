from average_precision import get_average_precision, get_weighted_average, get_average_recall, get_average_f1
import argparse, os
from file_operations import read_lines
from converters import get_labels, delete_prefixes
from printers import print_scores

NO_ENTITY_MARK = 'O'

def get_scores(compute_score, hypotheses, reference):
    hypotheses_precision_scores = {}
    for key in hypotheses:
        hypothese_scores = {}
        labels = list(set(reference))   
        scores = compute_score(y_true=reference, y_pred=hypotheses[key], labels=labels, average=None)
        for label, score in zip(labels, scores):
            hypothese_scores[label] = score

        weighted_average = get_weighted_average({score: hypothese_scores[score] for score in hypothese_scores if score != NO_ENTITY_MARK}, {label: hypotheses[key].count(label) for label in labels if label != NO_ENTITY_MARK})

        hypothese_scores['weighted-average (without O)'] = weighted_average
        hypothese_scores['unweighted-average (without O)'] = compute_score(y_true=reference, y_pred=hypotheses[key], labels=[label for label in labels if label != NO_ENTITY_MARK], average='macro')
        hypothese_scores['micro-average'] = compute_score(y_true=reference, y_pred=hypotheses[key], labels=labels, average='micro')

        hypotheses_precision_scores[key] = hypothese_scores
    return hypotheses_precision_scores

def add_to_result(result, subgroup_by_prefix, metric, engine, tag, value):
    if subgroup_by_prefix not in result:
        result[subgroup_by_prefix] = {}
    if metric not in result[subgroup_by_prefix]:
        result[subgroup_by_prefix][metric] = {}
    if engine not in result[subgroup_by_prefix][metric]:
        result[subgroup_by_prefix][metric][engine] = {}
    if tag not in result[subgroup_by_prefix][metric][engine]:
        result[subgroup_by_prefix][metric][engine][tag] = 0
    result[subgroup_by_prefix][metric][engine][tag] += value

def get_average_score(scores):
    result = {}
    for score_set in scores:
        for subgroup_by_prefix in score_set:
            for metric in score_set[subgroup_by_prefix]:
                for engine in score_set[subgroup_by_prefix][metric]:
                    for tag in score_set[subgroup_by_prefix][metric][engine]:
                        add_to_result(result, subgroup_by_prefix, metric, engine, tag, score_set[subgroup_by_prefix][metric][engine][tag])

    for subgroup_by_prefix in result:
            for metric in result[subgroup_by_prefix]:
                for engine in result[subgroup_by_prefix][metric]:
                    for tag in result[subgroup_by_prefix][metric][engine]:
                        result[subgroup_by_prefix][metric][engine][tag] /= len(scores)

    return result

def merge_scores(scores):
    result = {}
    #print(scores)
    for score_set in scores:
        for subgroup_by_prefix in score_set:
            #print(subgroup_by_prefix)
            if subgroup_by_prefix not in result:
                result[subgroup_by_prefix] = {}
            for metric in score_set[subgroup_by_prefix]:
                if metric not in result[subgroup_by_prefix]:
                    result[subgroup_by_prefix][metric] = {}
                for engine in score_set[subgroup_by_prefix][metric]:
                    result[subgroup_by_prefix][metric][engine] = score_set[subgroup_by_prefix][metric][engine]
    return result

def compare(reference, hypotheses):
    return {'precision': get_scores(get_average_precision, hypotheses, reference), 'recall': get_scores(get_average_recall, hypotheses, reference), 'f1': get_scores(get_average_f1, hypotheses, reference)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--reference_file', type=str, default='eval.tagged.txt')
    parser.add_argument('--hypotheses_dir', type=str, default='.')
    parser.add_argument("--cv_dir", type=str, default='cv')
    parser.add_argument("--cv_reference_dir", type=str, default='reference')
    parser.add_argument("--cv", action="store_true")

    args = parser.parse_args()

    if not args.cv:
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
    else:
        prefix_sensitive_hypotheses = {}
        prefix_agnostic_hypotheses = {}
        average_scores = []
        for dir_path in os.listdir(args.cv_dir):
            scores_to_average = []
            if dir_path != args.cv_reference_dir:
                for path in os.listdir(f'{args.cv_dir}/{dir_path}'):
                    #print(path)
                    hypothesis_path = f'{args.cv_dir}/{dir_path}/{path}'
                    reference_path = f'{args.cv_dir}/{args.cv_reference_dir}/{path}'
                    
                    reference_labels = get_labels(reference_path)
                    hypothesis_labels = get_labels(hypothesis_path)
                    prefix_sensitive_hypotheses[dir_path] = hypothesis_labels
                    prefix_agnostic_hypotheses[dir_path] = delete_prefixes(hypothesis_labels)

                    scores_to_average.append({'prefix-sensitive': compare(reference_labels, prefix_sensitive_hypotheses), 'prefix-agnostic': compare(delete_prefixes(reference_labels), prefix_agnostic_hypotheses)})
            average_scores.append(get_average_score(scores_to_average))
        print_scores(merge_scores(average_scores))