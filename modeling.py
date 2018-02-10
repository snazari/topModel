import csv
import logging
import os
import pickle

import numpy as np
from gensim import corpora, models
from gensim.utils import SaveLoad

from config import config_processing, config_models
from processing import Processing
from utils import make_dirs


class Model(object):

    def __init__(self, model_name):
        self.model_name = model_name
        self._dictionary = corpora.Dictionary()
        self.corpus = []
        self.users = []
        self.corpus_words = []
        self._processing = Processing(**config_processing)
        self.model = SaveLoad()
        # self.model = models.LsiModel()

    def __iter__(self):
        pass

    def __call__(self, texts, user):
        document = self._processing(texts)
        self.corpus_words.append(document)
        self.users.append(user)
        self._dictionary.add_documents([document])
        self.corpus.append(self._dictionary.doc2bow(document))

    def get_topic_words(self):
        return [self._dictionary.get(key) for key in self._dictionary.keys()]

    def TfIdf(self, **config):
        normalize = config['normalize']
        self.model = models.TfidfModel(self.corpus, normalize=normalize)

    def LSI(self, **config):
        num_topics = config['num_topics']
        power_iters = config['power_iters']
        extra_samples = config['extra_samples']
        tfidf = models.TfidfModel(self.corpus)
        corpus_tfidf = tfidf[self.corpus]
        self.model = models.LsiModel(corpus_tfidf, id2word=self._dictionary, num_topics=num_topics,
                                     power_iters=power_iters, extra_samples=extra_samples)

    def RP(self, **config):
        num_topics = config['num_topics']
        self.model = models.RpModel(self.corpus, num_topics=num_topics)

    def LDA(self, **config):
        num_topics = config['num_topics']
        distributed = config['distributed']
        alpha = config['alpha']
        eta = config['eta']
        self.model = models.LdaModel(self.corpus, num_topics=num_topics, distributed=distributed, alpha=alpha, eta=eta)

    def HDP(self, **config):
        gamma = config['gamma']
        kappa = config['kappa']
        tau = config['tau']
        K = config['K']
        T = config['T']
        eta = config['eta']
        self.model = models.HdpModel(self.corpus, id2word=self._dictionary, gamma=gamma, kappa=kappa, tau=tau, K=K,
                                     T=T, eta=eta)

    def train_model(self):
        train_fun = getattr(self, self.model_name)
        train_fun(**config_models[self.model_name])

    def save_model(self):
        model_path = make_dirs('model', self.model_name)
        self.model.save(os.path.join(model_path, 'model.pickle'))

    def load_model(self):
        model_path = make_dirs('model', self.model_name)
        if self.model_name == 'TfIdf':
            self.model = models.TfidfModel.load(os.path.join(model_path, 'model.pickle'))
        elif self.model_name == 'LSI':
            self.model = models.LsiModel.load(os.path.join(model_path, 'model.pickle'))
        elif self.model_name == 'RP':
            self.model = models.RpModel.load(os.path.join(model_path, 'model.pickle'))
        elif self.model_name == 'LDA':
            self.model = models.LdaModel.load(os.path.join(model_path, 'model.pickle'))
        elif self.model_name == 'HDP':
            self.model = models.HdpModel.load(os.path.join(model_path, 'model.pickle'))

    def save_corpus(self):
        corpus_path = make_dirs('corpus', self.model_name)
        corpora.MmCorpus.serialize(os.path.join(corpus_path, 'corpus.mm'), self.corpus)

    def load_corpus(self):
        corpus_path = make_dirs('corpus', self.model_name)
        self.corpus = corpora.MmCorpus(os.path.join(corpus_path, 'corpus.mm'))

    def save_corpus_words(self):
        corpus_words_path = make_dirs('corpus_words', self.model_name)
        with open(os.path.join(corpus_words_path, 'corpus_words.pickle'), 'wb') as f:
            pickle.dump([self.corpus_words, self.users], f)

    def load_corpus_words(self):
        corpus_words_path = make_dirs('corpus_words', self.model_name)
        with open(os.path.join(corpus_words_path, 'corpus_words.pickle'), 'rb') as f:
            self.corpus_words, self.users = pickle.load(f)

    def save_dictionary(self):
        dictionary_path = make_dirs('dictionary', self.model_name)
        self._dictionary.save(os.path.join(dictionary_path, 'dictionary.dict'))

    def load_dictionary(self):
        dictionary_path = make_dirs('dictionary', self.model_name)
        self._dictionary = corpora.Dictionary.load(os.path.join(dictionary_path, 'dictionary.dict'))

    def save(self):
        self.save_model()
        self.save_corpus()
        self.save_corpus_words()
        self.save_dictionary()

    def load(self):
        self.load_model()
        self.load_corpus()
        self.load_corpus_words()
        self.load_dictionary()

    def data_for_user(self, user):
        ind = np.array(self.users) == user
        texts = np.array(self.corpus_words)[ind].tolist()
        return texts

    def transforming(self, data):
        if isinstance(data[0], list):
            corpus = [self._dictionary.doc2bow(token) for token in data]
        else:
            corpus = self._dictionary.doc2bow(data)
        if self.model_name in ['TfIdf', 'LDA', 'HDP']:
            model = self.model[corpus]
            if not isinstance(model, list):
                vectors = [vector for vector in model]
                return vectors
            else:
                return model
        elif self.model_name in ['LSI', 'RP']:
            model = models.TfidfModel(self.corpus, normalize=True)
            corpus_tfidf = model[corpus]
            if not isinstance(corpus_tfidf, list):
                corpus = [token for token in corpus_tfidf]
            else:
                corpus = corpus_tfidf
            predict = self.model[corpus]
            if not isinstance(predict, list):
                vectors = [vector for vector in predict]
                return vectors
            else:
                return predict

    def print_topics(self, num_words=10, file_name=None):
        if self.model_name in ['LSI', 'LDA', 'HDP']:
            if file_name is not None:
                logging.basicConfig(filename=file_name, filemode='w', format='%(levelname)s : %(message)s',
                                    level=logging.INFO)

                logging.root.level = logging.INFO
                logging.info('Number of words {}'.format(num_words))
                self.model.print_topics(num_topics=config_models[self.model_name]['num_topics'], num_words=num_words)
            else:
                return self.model.show_topics(num_topics=config_models[self.model_name]['num_topics'],
                                              num_words=num_words)
        else:
            pass

    def get_topics(self):
        if self.model_name in ['LSI', 'LDA', 'HDP']:
            return self.model.get_topics()
        else:
            exit('ERROR: TNSE visualization is only for methods LSI, LDA')

    def get_matrix(self, texts):
        vectors = self.transforming(texts)
        matrix = []
        for vector in vectors:
            if vector:
                # vec = np.zeros(self.model.num_topics)
                vec = np.zeros(config_models[self.model_name]['num_topics'])
                for id, topic in vector:
                    vec[id] = topic
                matrix.append(vec)
        return np.array(matrix)

    def get_top_words_from_topic(self, number_words):
        self._dictionary.get(0)
        id2token = self._dictionary.id2token
        topics = self.get_topics()
        id_top_words = np.argsort(-topics)
        top_words = []
        for i in range(topics.shape[0]):
            line = []
            for j in range(number_words):
                line.append(id2token[id_top_words[i, j]])
            top_words.append(line)
        return top_words
