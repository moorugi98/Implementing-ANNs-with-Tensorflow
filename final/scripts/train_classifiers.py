import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import os

from params import *
from classifier_model import get_classifier
from train import configure_gpu_options

if set_memory_growth_tf:
    configure_gpu_options()

### from a folder with embedding npy files, create a tf dataset with labels
def create_classifier_dataset(embedding_path):
    """
    Works only when the contained string doesn't have multiple class names
    """
    em_files = os.listdir(embedding_path)
    em_filepaths = [
        os.path.join(embedding_path, f) for f in em_files
    ]  # train files was created for training

    embedding_data = [np.reshape(np.load(x), (1, c_dim)) for x in em_filepaths]

    classes = [
        "blues",
        "reggae",
        "metal",
        "rock",
        "pop",
        "classical",
        "country",
        "disco",
        "jazz",
        "hiphop",
    ]

    em_onehot_labels = [
        tf.reshape(tf.eye(len(classes))[l], (1, len(classes)))
        for l in [
            [i for i, label in enumerate(classes) if label in p][0]
            for p in em_filepaths
        ]
    ]

    ds = tf.data.Dataset.from_tensor_slices((embedding_data, em_onehot_labels))

    return ds


def plot_classifier_training(history, epochs, save_path):
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, epochs), history.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), history.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs), history.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs), history.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt_fn = "loss.png"
    plt.savefig(os.path.join(save_path, plt_fn), bbox_inches="tight")


def plot_confusion_matrix(test_ds, model, save_path):
    test_em = []
    test_labels = []
    classes = [
        "blues",
        "reggae",
        "metal",
        "rock",
        "pop",
        "classical",
        "country",
        "disco",
        "jazz",
        "hiphop",
    ]

    for em, label in test_ds:
        test_em.append(np.reshape(em.numpy(), (c_dim)))
        test_labels.append(np.reshape(label.numpy(), (1, len(classes))))
    test_em = np.array(test_em)
    test_labels = np.reshape(np.array(test_labels), (len(test_labels), len(classes)))
    y_pred = np.argmax(model.predict(test_em), axis=1)
    y_true = np.argmax(test_labels, axis=1)
    confusion_mtx = tf.math.confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        confusion_mtx, xticklabels=classes, yticklabels=classes, annot=True, fmt="g"
    )
    plt.xlabel("Prediction")
    plt.ylabel("Label")
    plt_fn = "confusion.png"
    plt.savefig(os.path.join(save_path, plt_fn), bbox_inches="tight")


# 3 design principles
model = get_classifier(c_dim, 10)
optimizer = tf.keras.optimizers.Adam(learning_rate_class)
cce = tf.keras.losses.CategoricalCrossentropy()

# generate dataset from saved embeddings
train_ds = create_classifier_dataset(path_load_embeddings_train)
test_ds = create_classifier_dataset(path_load_embeddings_test)

# train and test the model
model.compile(optimizer=optimizer, loss=cce, metrics=["accuracy"])
history = model.fit(
    train_ds,
    epochs=epochs_class,
    batch_size=batch_size_classifier,
    validation_data=test_ds,
)  # add additional arguments


# analysis of the model
# 1. Loss
plot_classifier_training(history, epochs_class, path_save_classifier_plots)
exp_data_fn = "train_results.npy"
np.save(os.path.join(path_save_classifier_plots, exp_data_fn), history.history)

# 2. Confusion matrix
plot_confusion_matrix(test_ds, model, path_save_classifier_plots)
