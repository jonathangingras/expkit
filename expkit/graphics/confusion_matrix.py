import itertools
import numpy as np
import matplotlib.pyplot as plt


def plot_binary_confusion_matrix(confusion_matrix_array,
                                 classes,
                                 normalize=False,
                                 title='Confusion matrix'):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(confusion_matrix_array, interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        confusion_matrix_array = \
        confusion_matrix_array.astype('float') / confusion_matrix_array.sum(axis=1)[:, np.newaxis]

    thresh = confusion_matrix_array.max() / 2.
    for i, j in itertools.product(range(confusion_matrix_array.shape[0]),
                                  range(confusion_matrix_array.shape[1])):

        plt.text(j, i, confusion_matrix_array[i, j],
                 horizontalalignment="center",
                 color="white" if confusion_matrix_array[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
