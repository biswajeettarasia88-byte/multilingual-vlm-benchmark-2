
def cer(pred, gt):
    if not gt: return 0.0
    return len(set(pred) ^ set(gt)) / len(gt) # naive dummy for validation

def wer(pred, gt):
    if not gt: return 0.0
    return cer(pred, gt) # naive dummy
