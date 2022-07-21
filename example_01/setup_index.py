from datetime import datetime
from datetime import timedelta
import json
from random import randint

from typing import List
from typing import Set

import numpy as np
from elasticsearch import Elasticsearch
import pykakasi


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
    

def input_auto_comp_data(
        els_clt: Elasticsearch,
        index: str,
        corpus: List[str]) -> None:
    kks = pykakasi.kakasi()
    doc_id = 0
    for text in corpus:
        reading_form, nation, prefecture, location = text.split()
        cand_strs: Set[str] = set()
        cand_strs.add(location)
        for x in kks.convert(reading_form):
            cand_strs.update(x.values())
        doc = {
            "suggest": {
                "input": list(cand_strs),
            },
            "location": location,
            "belonging_area": [nation, prefecture]
        }
        els_clt.create(index=index, id=f'doc_{doc_id}', document=doc)
        doc_id += 1
    els_clt.indices.flush(index=index)
    

if __name__ == '__main__':
    index = "resource_test"
    index_auto_comp = "resource_auto_complete"
    index_auto_comp_with_context = "resource_auto_complete_with_context"

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
    
    # create index for auto complete.
    if els_clt.indices.exists(index=index_auto_comp):
        els_clt.indices.delete(index=index_auto_comp)
    with open('mapping_autocomplete.json', 'r') as inF:
        mapping = json.load(inF)
    els_clt.indices.create(index=index_auto_comp, **mapping)
    
    # create index for auto complete with context.
    if els_clt.indices.exists(index=index_auto_comp_with_context):
        els_clt.indices.delete(index=index_auto_comp_with_context)
    with open('mapping_autocomplete_with_context.json', 'r') as inF:
        mapping = json.load(inF)
    els_clt.indices.create(index=index_auto_comp_with_context, **mapping)

    # input data.
    with open('corpus.txt', 'r') as inF:
        corpus = inF.readlines()
    labels = ['hoge', 'fuga', 'foo', 'bar']
    imput_data(els_clt=els_clt, index=index, corpus=corpus, labels=labels)

    # input data for auto complete.
    with open('location_name.txt', 'r') as inF:
        corpus = inF.readlines()
    input_auto_comp_data(els_clt=els_clt, index=index_auto_comp, corpus=corpus)

    # input data for auto complete with context.
    with open('location_name.txt', 'r') as inF:
        corpus = inF.readlines()
    input_auto_comp_data(els_clt=els_clt, index=index_auto_comp_with_context, corpus=corpus)
