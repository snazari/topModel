import csv
from modeling import Model
from visualizing_topic_models import *

model_name = 'LSI'
model = Model(model_name)

with open('message.csv', encoding='utf-8') as f:
    reader_file = csv.reader(f)
    for row in reader_file:
        model(row[1], row[0])

model.train_model()
model.save()

contributor = 'Takashi Iwai'

texts = model.data_for_user(contributor)
vectors = model.transforming(texts)
matrix  = model.get_matrix(texts)
print(vectors)

visualization_share_texts_of_topic(matrix, 1, 'takashi Share of topic 1.png')
visualization_share_texts_of_topic(matrix, 2, 'takashi Share of topic 2.png')
visualization_share_texts_of_topic(matrix, 3, 'takashi Share of topic 3.png')
visualization_share_texts_of_topic(matrix, 4, 'takashi Share of topic 4.png')
visualization_share_texts_of_topic(matrix, 5, 'takashi Share of topic 5.png')

visualization_TSNE_topics(matrix, 5, 'takashi TSNE topics (FreeCodeCamp).html', model)

# get all data from save model for repository
texts = model.corpus_words
# get matrix for repository
matrix = model.get_matrix(texts)

visualization_TSNE_topics(matrix, 5, 'FreeCodeCamp TSNE_topics_all.html', model)

