import json

from typing import Any
from typing import List
from typing import Mapping
from typing import Optional

import numpy as np
from elasticsearch import Elasticsearch


def mk_mlt_and_vec_sim_query(
        like: str,
        doc_vec: Any,
        doc_vec_weight: float,
        user_vec: Any,
        user_vec_weight: float,
        size: int,
        analyzer: Optional[str]=None,
        ) -> Mapping[str, Any]:
    '''クエリの結果をベクトルの類似度でさらにリランキングするクエリ.
    
    more_like_thisで検索した結果を、ドキュメント内のdoc_vecフィールド(dense_vector型)
    と引数で指定したdoc_vec,user_vecの類似度でリランキングするクエリを作成する.
    引数で指定するdoc_vecはlikeで句の文をベクトル化したものというイメージ.
    (必ずしもそうでなくてはならないというわけではない)
    引数で指定するuser_vecはユーザをベクトル化したものというイメージ.

    @param like more_like_thisクエリのlike句に与える文字列.
    @param doc_vec ドキュメントベクトル.
    @param doc_vec_weight ドキュメントベクトルの類似度のスコアへの寄与の重み.
    @param user_vec ユーザベクトル.
    @param user_vec_weight ユーザベクトルの類似度のスコアへの寄与度の重み.
    @param size 何件の結果を取得するか.
    @param analyzer 使用するanalyzer.
    '''

    more_like_this_clouse = {
      "fields" : ["doc_text"],
      "like" : like,
      "min_term_freq" : 1,
      "min_doc_freq": 1,
      "minimum_should_match": "30%",
    }
    if analyzer is not None:
        more_like_this_clouse["analyzer"] = analyzer

    return {
      "query": {
        "bool" : {
          "must" : [],
          "filter": [],
          "must_not" : [],
          "should" : [
            {
              "more_like_this" : more_like_this_clouse
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
    

if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # create random vector.
    doc_vec = np.array(np.random.randn(3), dtype=float)
    doc_vec = doc_vec / np.linalg.norm(doc_vec)
    user_vec = np.array(np.random.randn(3), dtype=float)
    user_doc = user_vec / np.linalg.norm(user_vec)
    
    # execute query.
    try:
        query = mk_mlt_and_vec_sim_query(
            "エラスティック lucene fork", doc_vec, 5, user_vec, 2, 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
        print("----------")

        query = mk_mlt_and_vec_sim_query(
            "エラスティック lucene fork", doc_vec, 5, user_vec, 2, 5,
            analyzer="japanese_search_analyzer")
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
    except Exception as e:
        print(e)
