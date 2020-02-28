
import logging
import gensim
import pickle

from typing import List
from os.path import join, dirname


LDA_LOG = logging.getLogger(__name__)


class LDA17:
	def __init__(self):
		LDA_LOG.info('Loading lda17 model...')
		self.model = gensim.models.LdaModel.load(
			join(dirname(__file__), 'files', 'model')
		)
		self.id2word = gensim.corpora.Dictionary.load(
			join(dirname(__file__), 'files', 'id2word')
		)
		with open(
				join(dirname(__file__), 'files', 'nearest_neighbors'),
				'rb',
		) as f:
			self.nearest_neighbors = pickle.load(f)
		LDA_LOG.info('Done loading model.')

	def get_topic_scores(self, text: str) -> List[float]:
		words = self.sentence_to_words(text)
		bow = self.id2word.doc2bow(words)
		topic_scores = [0 for _ in range(17)]
		topics = self.model.get_document_topics(
			bow,
			minimum_probability=0,
			minimum_phi_value=0,
		)
		for topic_tuple in topics:
			# Note that topic numbers are 1-indexed by gensim
			# Hence why we assign to topic_tuple[0]-1
			topic_scores[topic_tuple[0] - 1] = float(topic_tuple[1])
			# We have to convert our numpy.float32 to Python floats
			# Since psycopg2 doesn't understand numpy.
		return topic_scores

	def get_nearest(self, topic_scores, count=50, return_distance=False):
		dist, indices = self.nearest_neighbors.kneighbors(
			topic_scores,
			n_neighbors=count,
			return_distance=False,
		)
		if return_distance is True:
			return indices, dist
		else:
			return indices

	@staticmethod
	def sentence_to_words(sentence: str):
		return gensim.utils.simple_preprocess(str(sentence), deacc=True)

	def __enter__(self):
		return (self)

	def __exit__(self, exc_type, exc_value, tb):
		LDA_LOG.info(f'__exit__ called, cleaning up...')
		LDA_LOG.info(f'exc_type: {exc_type}')
		del self.model
		del self.id2word
		del self.nearest_neighbors

