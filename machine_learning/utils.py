import matplotlib.pyplot as plt
import random
import numpy as np
from sklearn import cross_validation

def file_to_dataset(fname,start_col,end_col,target_col,skip_lines=3,sparse=False):
    with open(fname) as file:
        attributes = list()
        target = list()

        #we need these for sparse matrix
        col_i = list()
        row_i = list()

        # skip lines
        for i in range(skip_lines):
            file.readline()

        for i, line in enumerate(file):
            split_line = line.split('\t')
            atrs = list()
            for j, value in enumerate(split_line[start_col:end_col]):
                try:
                    f_val = int(value.strip())
                except ValueError:
                    f_val = float(value.strip())
                if sparse and f_val > 0:
                    attributes.append(float(f_val))
                    row_i.append(i)
                    col_i.append(j)
                elif not sparse:
                    atrs.append(float(f_val))
            if not sparse:
                attributes.append(atrs)

            target.append(split_line[target_col].strip())

    return attributes,target, row_i, col_i

def plot_learning_curve(clf, X_train, y_train, X_test, y_test, step=100, use_loo=False):
    n_train = y_train.size
    available_indexes = [i for i in range(n_train)]
    indexes = []
    test_plot = []
    train_plot = []
    x_plot = []
    while len(available_indexes)>step:
        indexes += [available_indexes.pop(random.randrange(len(available_indexes))) for _ in range(step)]
        x_plot.append(len(indexes))

        clf.fit(X_train[indexes, ], y_train[indexes, ])
        train_plot.append(clf.score(X_train[indexes,], y_train[indexes,]))
        if not use_loo:
            test_plot.append(clf.score(X_test,y_test))

        else:
            ca = list()
            loo = cross_validation.LeaveOneOut(n=n_train)
            for train_index, test_index in loo:
                X_tr, X_ts = X_train[train_index], X_train[test_index]
                y_tr, y_ts = y_train[train_index], y_train[test_index]
                clf.fit(X_tr, y_tr)
                ca.append(clf.score(X_ts,y_ts))
            test_plot.append(sum(ca)/len(ca))


    test_label = 'test CA' if not use_loo else 'LOO CA'
    plt.plot(x_plot, test_plot, '-b', label=test_label)
    plt.plot(x_plot, train_plot, '-g', label='learn CA')

    plt.xlabel('Training size')
    plt.ylabel('CA')
    plt.title('Learning curve')
    plt.grid(True)
    plt.legend()
    #plt.savefig("test.png")
    plt.show()

def CA(y_test, y_pred):
    return np.sum(y_test == y_pred)/y_test.size