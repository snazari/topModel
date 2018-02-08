import csv

from big_query import GhtorrentBq, RepositoryGhtorrentBq, GitHubRepos, RepositoryGitHubRepos
from modeling import Model
from visualizing_topic_models import *

# get data from repository ghtorrent_bq
client = GhtorrentBq()
client.get_list_repository('linux')
repository = RepositoryGhtorrentBq("torvalds", "linux")
repository.contributors(100)
repository.get_commit_comments()
repository.get_pull_request_comments()

# get data from repository public_github


# create model
model = Model('LSI')
# add data to model
with open('message.csv', encoding='utf-8') as f:
    reader_file = csv.reader(f)
    for row in reader_file:
        model(row[1], row[0])

# train model
model.train_model()
# save model, path for save to config.py file
model.save()

# get data for user from save model for repository
texts = model.data_for_user('Harshil Darji')

# get transforming vector for data
vectors = model.transforming(texts)
print(vectors)

# save topics to file
model.print_topics(10, 'topics.log')

# visualization topics

# get matrix for commits user
matrix = model.get_matrix(texts)
# the matrix is an 2D array of the size n*m, where n is the number of commits, m is the number of topics

# visualization share of topic, save plot to png file
visualization_share_texts_of_topic(matrix, 1, 'Share of topic.png')
# visualization share of topics, save plot to png file
visualization_share_texts_of_topics(matrix, 'Share of topics.png')
# visualization heat map topics, save plot to png file
visualization_heatmap_topics(matrix, 'Heat Map.png')
# visualization TSNE topics, save plot to html file
visualization_TSNE_topics(matrix, 5, 'TSNE_topics.html', model)


# example create model from save model, path for load model to config.py file
model_1 = Model('LSI')
model_1.load()
# print topics to console
model_1.print_topics()


