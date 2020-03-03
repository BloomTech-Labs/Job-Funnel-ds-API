import pickle
import time
import gensim

from os.path import join
from urllib.request import urlopen, urlretrieve

from sklearn.neighbors import KNeighborsClassifier


class ModelManager:
	FRESHNESS_THRESHOLD = 3600  # Number of seconds before the model is out-of-date


class LDA17Manager(ModelManager):
	BASE_URL = 'http://quickhire-data-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/'
	NN_MODEL_URL = BASE_URL + 'models/lda17-nn'
	LDA_MODEL_URL = BASE_URL + 'models/lda17-m'
	LDA_ID2WORD_URL = BASE_URL + 'models/lda17-id'
	LDA_EXTRA_URLS = [
		BASE_URL + 'models/lda17-m.expElogbeta.npy',
		BASE_URL + 'models/lda17-m.id2word',
		BASE_URL + 'models/lda17-m.state',
	]
	MODEL_FILES_PATH = 'models/lda17/files/'

	def __init__(self):
		self.load_model()

	def load_model(self):
		with urlopen(self.NN_MODEL_URL) as f:
			self.nn_model = pickle.load(f)
		extra_files = []
		for lda_url in self.LDA_EXTRA_URLS:
			urlretrieve(
				lda_url,
				join(self.MODEL_FILES_PATH, lda_url.split('/')[-1])
			)
		filename, _ = urlretrieve(self.LDA_MODEL_URL, self.LDA_MODEL_URL.split('/')[-1])
		self.lda_model = gensim.models.LdaModel.load(filename)
		filename, _ = urlretrieve(self.LDA_ID2WORD_URL)
		self.id2word = gensim.corpora.Dictionary.load(filename)

		self.last_loaded = time.time()

	def refresh(self):
		if time.time() - self.last_loaded > self.FRESHNESS_THRESHOLD:
			self.load_model()

	def get_scores(self, description):
		processed = self.sentence_to_words(description)
		bow = self.id2word.doc2bow(processed)

		topic_scores = [0 for _ in range(17)]
		topics = self.lda_model.get_document_topics(
			bow,
			minimum_probability=0,
			minimum_phi_value=0
		)
		for topic_tuple in topics:
			# Note that topic numbers are 1-indexed by gensim
			# Hence why we assign to topic_tuple[0]-1
			topic_scores[topic_tuple[0] - 1] = float(topic_tuple[1])
		return topic_scores

	def predict(self, description, count=50):
		scores = self.get_scores(description)
		distances, indices = self.nn_model.kneighbors([scores])
		job_ids = self.nn_model._y[indices]
		return job_ids

	@staticmethod
	def sentence_to_words(sentence):
		return gensim.utils.simple_preprocess(str(sentence), deacc=True)

