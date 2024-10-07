def partition_train_val(X, y, r=0.2):
    K = round(1 / r)
    X_val = [x[1] for x in enumerate(X) if x[0] % K == 0]
    y_val = [x[1] for x in enumerate(y) if x[0] % K == 0]
    X_train = [x[1] for x in enumerate(X) if x[0] % K > 0]
    y_train = [x[1] for x in enumerate(y) if x[0] % K > 0]
    return X_train, y_train, X_val, y_val

def partition_val_croisee(X, y, K=5):
    X_K, y_K = [], []
    for k in range(K):
        X_K.append([x[1] for x in enumerate(X) if x[0] % K == k])
        y_K.append([x[1] for x in enumerate(y) if x[0] % K == k])
    return X_K, y_K
