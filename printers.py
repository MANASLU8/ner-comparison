COMPARATIVE_TABLE_SEPARATOR = '\t'

def print_comparative_table(scores):
    print(COMPARATIVE_TABLE_SEPARATOR.join(['label'] + list(scores.keys())))
    for label in scores[list(scores.keys())[0]]:
        line = [label]
        for model in scores:
            line.append(f'{scores[model][label]:.3f}')
        print(COMPARATIVE_TABLE_SEPARATOR.join(line))


def print_scores(scores):
    for subgroup_by_prefix in scores:
        print(subgroup_by_prefix)
        for metric in scores[subgroup_by_prefix]:
            print(metric)
            print_comparative_table(scores[subgroup_by_prefix][metric])