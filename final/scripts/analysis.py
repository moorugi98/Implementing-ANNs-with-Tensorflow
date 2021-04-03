import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

from sklearn.manifold import TSNE


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


def plot_tsne(data, labels, save_path, title, fn="tsne_plot.svg"):
    # get and fit data
    tsne_data = TSNE(n_components=2).fit_transform(data)

    # create figure
    plt.figure(figsize=(10, 10))
    tsne_plot = sns.scatterplot(
        x=tsne_data[:, 0],
        y=tsne_data[:, 1],
        hue=labels,
        palette=[
        "purple",
        "lightgreen",
        "red",
        "orange",
        "brown",
        "blue",
        "dodgerblue",
        "green",
        "darkcyan",
        "black",
    ],
        legend="full",
    )

    tsne_plot.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)
    tsne_plot.set_title(
        f"TSNE plot of the {title} Embeddings", fontdict={"fontsize": 25}
    )
    plt.savefig(os.path.join(save_path, fn), bbox_inches="tight")


def plot_tsne_per_genre(data_train, data_test, labels_train, labels_test, save_path, classes):
    # get and fit data
    data = np.concatenate((data_train, data_test))  # (total_num_embeddings, c_dim)
    tsne_data = TSNE(n_components=2).fit_transform(data)
    xmin = np.min(tsne_data[:,0])
    xmax = np.max(tsne_data[:,0])
    ymin = np.min(tsne_data[:, 1])
    ymax = np.max(tsne_data[:,1])
    eps = (ymax - ymin) / 10  # white boundary

    for genre in classes:
        # logical array to select correct indices
        logic_genre_train = labels_train[labels_train == genre]
        logic_genre_test = labels_test[labels_test == genre]
        # take correct points
        selected_train = tsne_data[logic_genre_train]
        selected_test = tsne_data[logic_genre_test]
        selected_ems = np.concatenate((selected_train, selected_test))
        labels_joint = np.concatenate(
            (
                np.repeat(["train"], repeats=selected_train.shape[0]),
                np.repeat(["test"], repeats=selected_test.shape[0]),
            )
        )

        # create figure
        plt.figure(figsize=(10, 10))
        plt.set(xlim=[xmin-eps, xmax+eps], ylim=[ymin-eps, ymax+eps])
        tsne_plot = sns.scatterplot(
            x=tsne_data[:, 0],
            y=tsne_data[:, 1],
            hue=labels_joint,
            palette=[
        'red',
        "black"
    ],
            legend="full",
        )

        tsne_plot.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)
        tsne_plot.set_title(
            f"TSNE plot of the {genre} Embeddings", fontdict={"fontsize": 25}
        )
        plt.savefig(os.path.join(save_path, f"tsne_plot_{genre}.svg"), bbox_inches="tight")