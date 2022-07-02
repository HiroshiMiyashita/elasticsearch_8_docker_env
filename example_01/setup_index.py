from datetime import datetime
from datetime import timedelta
import json
from random import randint

from typing import List
from xmlrpc.client import DateTime

import numpy as np
from elasticsearch import Elasticsearch


def imput_data(
        els_clt: Elasticsearch,
        index: str,
        corpus: List[str], 
        labels: List[str]) -> None:
    doc_id = 0
    for text in corpus:
        vec = np.random.randn(3)
        vec = (vec / np.linalg.norm(vec)).tolist()
        date = datetime.now() - timedelta(days=randint(0, 100))
        doc = {
            'doc_text': text,
            'doc_vector': vec,
            'label': labels[np.random.choice(len(labels))],
            'date_random': date.isoformat()
        }
        els_clt.create(index=index, id=f'doc_{doc_id}', document=doc)
        doc_id += 1
    els_clt.indices.flush(index=index)
    

if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # create analysis template.
    with open('analysis_template.json', 'r') as inF:
        template = json.load(inF)
    els_clt.indices.put_index_template(name="default_analysis", **template)

    # create index.
    if els_clt.indices.exists(index=index):
        els_clt.indices.delete(index=index)
    with open('mapping.json', 'r') as inF:
        mapping = json.load(inF)
    els_clt.indices.create(index=index, **mapping)

    # input data
    with open('corpus.txt', 'r') as inF:
        corpus = inF.readlines()
    labels = ['hoge', 'fuga', 'foo', 'bar']
    imput_data(els_clt=els_clt, index=index, corpus=corpus, labels=labels)
