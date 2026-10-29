import numpy as np
import matplotlib.pyplot as plt
from sklearn import (svm, tree, metrics, naive_bayes, clone)
from matplotlib.lines import Line2D # For the custom legend
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedKFold


def load_wdbc_data(filename):
    class WDBCData:
        data          = [] # Shape: (569, 30)
        target        = [] # Shape: (569, )
        target_names  = ['malignant', 'benign']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
    wdbc = WDBCData()
    with open(filename) as f:
        for line in f.readlines():
            items = line.split(',')
            wdbc.target.append(0 if items[1] == "M" else 1) # Add the true label (0 for M / 1 for others)
            wdbc.data.append([float(x) for x in items[2:]]) # Add 30 attributes (as floating-point numbers)
        wdbc.data = np.array(wdbc.data)
        wdbc.target = np.array(wdbc.target)
    return wdbc

# Reusable function to clone and train fresh models since training/validating on the entire set makes no sense
def cross_validate(model, X, y, cv):
    predict = np.zeros_like(y)
    fold_scores = []
    for train_idx, test_idx in cv.split(X, y):
        fold_model = clone(model)
        fold_model.fit(X[train_idx], y[train_idx])
        predict[test_idx] = fold_model.predict(X[test_idx])
        fold_scores.append(metrics.balanced_accuracy_score(y[test_idx], predict[test_idx]))
    return np.array(fold_scores), predict


if __name__ == '__main__':
    # Load a dataset
    wdbc = load_wdbc_data('data/wdbc.data')

    # Models
    models = {
        'SVM': svm.SVC(),
        'Decision Tree': tree.DecisionTreeClassifier(max_depth=5, random_state=0),
        'Naive Bayes': naive_bayes.GaussianNB(),
    }

    # Use K-Fold Cross Validation to get more accurate results and avoid overfitting
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    results = {}
    for name, model in models.items():
        fold_scores, predict = cross_validate(model, wdbc.data, wdbc.target, cv)
        overall = metrics.balanced_accuracy_score(wdbc.target, predict)
        results[name] = {'folds': fold_scores, 'predict': predict, 'overall': overall}

    print('5-fold stratified cross-validation (balanced accuracy)')
    print(f'{"Model":<16}{"Mean":>8}{"Std":>8}{"Overall":>10}')
    for name, r in results.items():
        print(f'{name:<16}{r["folds"].mean():>8.3f}{r["folds"].std():>8.3f}{r["overall"]:>10.3f}')
    print()
    for name, r in results.items():
        print(f'{name} per-fold: ' + ', '.join(f'{s:.3f}' for s in r['folds']))
    print()

    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]

    # Confusion matrix for each model
    for name, r in results.items():
        ConfusionMatrixDisplay.from_predictions(wdbc.target, r['predict'], display_labels=wdbc.target_names)
        plt.title(f'Confusion matrix {name}')
        plt.savefig(f'wdbc_classification_matrix_{name.lower().replace(" ", "_")}.png')
        plt.show()

        plt.figure()
        plt.title(f'{name} Classifier (Accuracy: {results[name]["overall"]:.3f})')
        plt.scatter(wdbc.data[:, 0], wdbc.data[:, 1], c=cmap[wdbc.target], edgecolors=cmap[results[name]['predict']])
        plt.xlabel(wdbc.feature_names[0])
        plt.ylabel(wdbc.feature_names[1])
        plt.legend(handles=clabel, framealpha=0.5)
        plt.savefig(f'wdbc_classification_scatter_{name.lower().replace(" ", "_")}.png')
        plt.show()

    # Visualize testing results
    for (x, y) in [(0, 1)]: # Not mandatory, but try [(i, i+1) for i in range(0, 30, 2)]
        plt.figure()
        plt.title(f'My Classifier (Accuracy: {results["SVM"]["overall"]:.3f})')
        plt.scatter(wdbc.data[:, x], wdbc.data[:, y], c=cmap[wdbc.target], edgecolors=cmap[results['SVM']['predict']])
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
    # plt.show()