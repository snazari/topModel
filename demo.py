import csv

from modeling import Model
from visualizing_topic_models import *

# # create model, available models are listed in the file "config.py"
model_name = 'HDP'
model = Model(model_name)
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
contributor = 'Harshil Darji'
texts = model.data_for_user(contributor)

# get transforming vector for data
vectors = model.transforming(texts)
print(vectors)

# visualization topics
# visualization is only available for models LSI, LDA, RP

model_visualization = ['LSI', 'LDA', 'RP']
if not model_name in model_visualization:
     exit('ERROR: Visualization is only available for models LSI, LDA, RP')
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
#
# # get all data from save model for repository
texts = model.corpus_words
# # get matrix for repository
matrix = model.get_matrix(texts)
# visualization TSNE topics for all corpus, save plot to html file
visualization_TSNE_topics(matrix, 5, 'TSNE_topics_all.html', model)

# save topics to file
model.print_topics(10, 'topics.log')
model.print_topics(30, 'topics.log')
model.print_topics(50, 'topics.log')


#In order to avoid training model comment all the code above
#Below is the code to load model from file and make plots

# example create model from save model, path for load model to config.py file
model_name = 'RP'
model = Model(model_name)
model.load()

# get data for user from save model for repository
contributor = 'Harshil Darji'
texts = model.data_for_user(contributor)

model_visualization = ['LSI', 'LDA', 'RP']
if not model_name in model_visualization:
    exit('ERROR: Visualization is only available for models LSI, LDA, RP')

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

# get all data from save model for repository
texts = model.corpus_words
# get matrix for repository
matrix = model.get_matrix(texts)
# visualization TSNE topics for all corpus, save plot to html file
visualization_TSNE_topics(matrix, 5, 'TSNE_topics_all.html', model)

model.print_topics(10, 'topics.log')
model.print_topics(30, 'topics.log')
model.print_topics(50, 'topics.log')

