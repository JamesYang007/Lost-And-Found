from app import db
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
nltk.download('genesis')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
genesis_ic = wn.ic(genesis, False, 0.0)

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from sklearn.metrics import roc_auc_score

# make an engine to interact with SQL
engine = db.create_engine('sqlite:///database/post.db', {})
connection = engine.connect()
metadata = db.MetaData()

# make our database table
entries = db.Table('entries', metadata,
                   db.Column('title', db.String(100), primary_key=True),
                   db.Column('imagepath', db.String(100), nullable=False),
                   #db.Column('latitude', db.Float, nullable=False),
                   #db.Column('longitude', float, nullable=False),
                   db.Column('phone', db.String(15), nullable=False),
                   db.Column('keywords', db.String(100), nullable=False),
                   db.Column('desc', db.String(1000), nullable=False),
                   db.Column('lost', db.Boolean, nullable=False)
                   )

# test: make sure labels are working ok
"""for ent in metadata.sorted_tables:
    print(ent.name)"""

# test: column access
"""for c in entries.c:
    print(c)"""
    
# test: make a query
query = db.select([entries.c.title])
result = connection.execute(query).fetchall()
df = pd.DataFrame(result)
df.columns = result[0].keys()
df.head(5)

# knn sorting algorithm to come up with suggestions for closest data points
class KNN_NLC_Classifer():
    def __init__(self, k=1, distance_type = 'path'):
        self.k = k
        self.distance_type = distance_type

    # This function is used for training
    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    # This function runs the K(1) nearest neighbour algorithm and
    # returns the label with closest match. 
    def predict(self, x_test):
        self.x_test = x_test
        y_predict = []

        for i in range(len(x_test)):
            max_sim = 0
            max_index = 0
            for j in range(self.x_train.shape[0]):
                temp = self.document_similarity(x_test[i], self.x_train[j])
                if temp > max_sim:
                    max_sim = temp
                    max_index = j
            y_predict.append(self.y_train[max_index])
        return y_predict
    
"""TODO: change from document-based kNN to utilizing databasae entries"""
def convert_tag(self, tag):
    """Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets"""
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
    try:
        return tag_dict[tag[0]]
    except KeyError:
        return None


def doc_to_synsets(self, doc):
    """
    Returns a list of synsets in document.
    Tokenizes and tags the words in the document doc.
    Then finds the first synset for each word/tag combination.
    If a synset is not found for that combination it is skipped.

    Args:
    doc: string to be converted

    Returns:
        list of synsets
    """
    tokens = word_tokenize(doc+' ')
        
    l = []
    tags = nltk.pos_tag([tokens[0] + ' ']) if len(tokens) == 1 else nltk.pos_tag(tokens)
        
    for token, tag in zip(tokens, tags):
        syntag = self.convert_tag(tag[1])
        syns = wn.synsets(token, syntag)
        if (len(syns) > 0):
            l.append(syns[0])
    return l

def similarity_score(self, s1, s2, distance_type = 'path'):
    """
    Calculate the normalized similarity score of s1 onto s2
    For each synset in s1, finds the synset in s2 with the largest similarity value.
    Sum of all of the largest similarity values and normalize this value by dividing it by the
    number of largest similarity values found.

    Args:
        s1, s2: list of synsets from doc_to_synsets

    Returns:
        normalized similarity score of s1 onto s2
    """
    s1_largest_scores = []

    for i, s1_synset in enumerate(s1, 0):
        max_score = 0
        for s2_synset in s2:
            if distance_type == 'path':
                score = s1_synset.path_similarity(s2_synset, simulate_root = False)
            else:
                score = s1_synset.wup_similarity(s2_synset)                  
        if score != None:
            if score > max_score:
                max_score = score
              
        if max_score != 0:
            s1_largest_scores.append(max_score)
          
    mean_score = np.mean(s1_largest_scores)
                 
    return mean_score

"""TODO: finish

architecture drawn from 
https://towardsdatascience.com/text-classification-using-k-nearest-neighbors-46fa8a77acc5

"""
