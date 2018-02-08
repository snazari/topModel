from sklearn.manifold import TSNE
import bokeh.plotting as bp
from bokeh.plotting import save
from bokeh import palettes
from matplotlib import pyplot as plt
import numpy as np


def visualization_share_texts_of_topic(matrix, number_topic, file_name):
    """
    :param matrix: The matrix is an 2D array of the size n*m, where n is the number of commits, m is the number of topics
    :param number_topic: Topic number
    :param file_name: Filename to save
    :return: Saves the image
    """
    fig, ax = plt.subplots()
    N, K = matrix.shape
    docnames = ['Commit {}'.format(i+1) for i in range(N)]
    ind = np.arange(N)
    width = 0.5
    ax.bar(ind, matrix[:, number_topic-1], width=width)
    ax.set_xticks(ind)
    ax.set_xticklabels(docnames)
    ax.set_title('Share of Topic #{}'.format(number_topic))
    fig.savefig(file_name)


def visualization_share_texts_of_topics(matrix, file_name):
    """
    :param matrix: The matrix is an 2D array of the size n*m, where n is the number of commits, m is the number of topics
    :param file_name: Filename to save
    :return: Saves the image
    """
    fig, ax = plt.subplots()
    N, K = matrix.shape
    docnames = ['Commit {}'.format(i+1) for i in range(N)]
    ind = np.arange(N)
    width = 0.5
    plots = []
    height_cumulative = np.zeros(N)
    for k in range(K):
        color = plt.cm.coolwarm(k / K, 1)
        if k == 0:
            p = ax.bar(ind, matrix[:, k], width, color=color)
            height_cumulative += matrix[:, k]
            plots.append(p)
        else:
            p = ax.bar(ind, matrix[:, k], width, bottom=height_cumulative, color=color)
            height_cumulative += matrix[:, k]
            plots.append(p)
    ax.set_axis_on()
    ax.set_ylim((-1, 1))
    ax.set_ylabel('Topics')
    ax.set_title('Share of Topics')
    ax.set_xticks(ind)
    ax.set_xticklabels(docnames)
    ax.set_yticks(np.arange(0, 1, 10))
    topic_labels = ['Topic #{}'.format(k + 1) for k in range(K)]
    ax.legend([p[0] for p in plots], topic_labels)
    fig.savefig(file_name)


def visualization_heatmap_topics(matrix, file_name):
    """
    :param matrix: The matrix is an 2D array of the size n*m, where n is the number of commits, m is the number of topics
    :param file_name: Filename to save
    :return: Saves the image
    """
    fig, ax = plt.subplots()
    N, K = matrix.shape
    docnames = ['Commit {}'.format(i + 1) for i in range(N)]
    cax = ax.pcolor(matrix, norm=None, cmap='Blues')
    ax.set_yticks(np.arange(matrix.shape[0]) + 0.5)
    ax.set_yticklabels(docnames)
    topic_labels = ['Topic #{}'.format(k + 1) for k in range(K)]
    ax.set_xticks(np.arange(matrix.shape[1]) + 0.5)
    ax.set_xticklabels(topic_labels)
    ax.invert_yaxis()
    plt.xticks(rotation=90)
    ax.set_title('Heatmap')
    fig.colorbar(cax)
    fig.tight_layout()
    fig.savefig(file_name)


def visualization_TSNE_topics(matrix, number_show_words, file_name, model):
    """
    :param matrix: The matrix is an 2D array of the size n*m, where n is the number of commits, m is the number of topics
    :param number_show_words: Count show words
    :param file_name: Filename to save
    :return: Saves the image
    """
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
    tsne_lda = tsne_model.fit_transform(matrix)
    colors = []
    colors.extend(palettes.Set1[9])
    colors.extend(palettes.Set2[8])
    colors.extend(palettes.Set3[12])

    colormap = np.array(colors)

    topic_keys = []
    for i in range(matrix.shape[0]):
        topic_keys.append(matrix[i].argmax())

    top_words = model.get_top_words_from_topic(number_show_words)
    topic_summaries = []
    for words in top_words:
        topic_summaries.append(' '.join(words))

    topic_coord = np.empty((matrix.shape[1], 2)) * np.nan
    for topic_num in topic_keys:
        if not np.isnan(topic_coord).any():
            break
        topic_coord[topic_num] = tsne_lda[topic_keys.index(topic_num)]

    title = 'TNSE Topics'
    num_example = len(matrix)

    plot_lda = bp.figure(plot_width=1000, plot_height=800,
                         title=title,
                         tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                         x_axis_type=None, y_axis_type=None)

    plot_lda.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], color=colormap[topic_keys][:num_example])

    for i in range(matrix.shape[1]):
        if not np.isnan(topic_coord[i, 0]):
            plot_lda.text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])
    save(plot_lda, file_name)
