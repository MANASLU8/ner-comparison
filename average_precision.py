from sklearn.metrics import precision_score, recall_score, f1_score

def get_weighted_average(scores, weights):
    result = 0
    for metric in scores:
        result += scores[metric] * weights[metric]
    return result / sum(weights.values())

def get_average_precision(y_true, y_pred, labels, average='micro'):
	return precision_score(y_true, y_pred, labels=labels, average=average)

def get_average_recall(y_true, y_pred, labels, average='micro'):
	return recall_score(y_true, y_pred, labels=labels, average=average)

def get_average_f1(y_true, y_pred, labels, average='micro'):
	return f1_score(y_true, y_pred, labels=labels, average=average)