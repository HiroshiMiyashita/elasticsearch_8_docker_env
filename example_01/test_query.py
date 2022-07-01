import json

from typing import Any
from typing import List
from typing import Mapping

import numpy as np
from elasticsearch import Elasticsearch


def mk_query(
        text: str,
        doc_vec: Any,
        doc_vec_weight: float,
        user_vec: Any,
        user_vec_weight: float,
        size: int,
        ) -> Mapping[str, Any]:
    return {
      "query": {
        "bool" : {
          "must" : [],
          "filter": [],
          "must_not" : [],
          "should" : [
            {
              "more_like_this" : {
                "fields" : ["doc_text"],
                "like" : text,
                "min_term_freq" : 1,
                "min_doc_freq": 1,
                "minimum_should_match": "30%"
              }
            }
          ],
          "minimum_should_match" : 1
        }
      },
      "size": size,
      "rescore" : {
        "window_size" : 50,
        "query" : {
          "score_mode": "multiply",
          "rescore_query" : {
            "function_score" : {
              "functions": [
                {
                  "script_score": {
                    "script": {
                      "source": "return 1.0 + params.weight * (doc['doc_vector'].size() == 0 ? 0.0 : (cosineSimilarity(params.docVec, 'doc_vector') + 1));",
                      "params": {
                        "docVec": doc_vec.tolist(),
                        "weight": doc_vec_weight
                      }
                    }
                  }
                },
                {
                  "script_score": {
                    "script": {
                      "source": "return 1.0 + params.weight * (doc['doc_vector'].size() == 0 ? 0.0 : (cosineSimilarity(params.userVec, 'doc_vector') + 1));",
                      "params": {
                        "userVec": user_vec.tolist(),
                        "weight": user_vec_weight
                      }
                    }
                  }
                }
              ],
              "score_mode": "avg"
            }
          }
        }
      } 
    }
    

def test_query(els_clt: Elasticsearch, index: str, query: Mapping[str, Any]) -> None:
    try:
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # create analysis template.
    doc_vec = np.array(np.random.randn(3), dtype=float)
    doc_vec = doc_vec / np.linalg.norm(doc_vec)
    user_vec = np.array(np.random.randn(3), dtype=float)
    user_doc = user_vec / np.linalg.norm(user_vec)
    query = mk_query("elasticsearch lucene fork", doc_vec, 5, user_vec, 2, 1)
    test_query(els_clt, index, query)
