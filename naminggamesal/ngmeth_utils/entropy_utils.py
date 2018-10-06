import numpy as np

def missinginfo(M,W):
	W = max(M,W)
	return sum([np.log2(W-k) for k in range(M)])
