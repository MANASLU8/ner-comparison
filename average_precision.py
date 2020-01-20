from sklearn.metrics import precision_score

def get_weighted_average(scores, weights):
    result = 0
    for metric in scores:
        result += scores[metric] * weights[metric]
    return result / sum(weights.values())

def get_average_precision(y_true, y_pred, labels, average='micro'):
	return precision_score(y_true, y_pred, labels=labels, average=average)
