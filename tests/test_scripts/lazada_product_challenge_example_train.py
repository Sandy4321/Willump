from sklearn.feature_extraction.text import CountVectorizer
import time
import pandas as pd
import numpy
import pickle
import willump.evaluation.willump_executor
import scipy.sparse.csr
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import mean_squared_error


def rmse_score(y, pred):
    return numpy.sqrt(mean_squared_error(y, pred))

# @willump.evaluation.willump_executor.willump_execute()
def vectorizer_transform(input_vect, input_df):
    np_input = list(input_df.values)
    transformed_result = input_vect.transform(np_input)
    return transformed_result


df = pd.read_csv("tests/test_resources/lazada_challenge_features/lazada_data_train.csv", header=None,
                 names=['country', 'sku_id', 'title', 'category_lvl_1', 'category_lvl_2', 'category_lvl_3',
                        'short_description', 'price', 'product_type'])

vect = CountVectorizer(analyzer='char', ngram_range=(2, 6), min_df=0.005, max_df=1.0,
                       lowercase=False, stop_words=None, binary=False, decode_error='replace')
vect.fit(df["title"].tolist())
print("Vocabulary has length %d" % len(vect.vocabulary_))

set_size = len(df)
mini_df = df.head(2).copy()["title"]
vectorizer_transform(vect, mini_df)
vectorizer_transform(vect, mini_df)
vectorizer_transform(vect, mini_df)
t0 = time.time()
X_title = vectorizer_transform(vect, df["title"])
time_elapsed = time.time() - t0
print("Title Processing Time %fs Num Rows %d Throughput %f rows/sec" %
      (time_elapsed, set_size, set_size / time_elapsed))

model = SGDClassifier(loss='log', penalty='l1', max_iter=1000, verbose=0, tol=0.0001)
y = numpy.loadtxt("tests/test_resources/lazada_challenge_features/conciseness_train.labels", dtype=int)

model.fit(X_title, y)

preds = model.predict(X_title)

print("RMSE Score: %f" % rmse_score(preds, y))

pickle.dump(model, open("tests/test_resources/lazada_challenge_features/lazada_model.pk", "wb"))