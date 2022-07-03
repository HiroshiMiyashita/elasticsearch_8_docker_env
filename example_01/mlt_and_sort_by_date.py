import json

from typing import Any
from typing import List
from typing import Mapping

import numpy as np
from elasticsearch import Elasticsearch


def mk_mlt_and_order_by_date_query(
        like: str,
        size: int,
        ) -> Mapping[str, Any]:
    '''クエリの結果をベクトルの類似度でさらにリランキングするクエリ.
    
    more_like_thisで検索した結果を、ドキュメント内のdoc_vecフィールド(dense_vector型)
    と引数で指定したdoc_vec,user_vecの類似度でリランキングするクエリを作成する.
    引数で指定するdoc_vecはlikeで句の文をベクトル化したものというイメージ.
    (必ずしもそうでなくてはならないというわけではない)
    引数で指定するuser_vecはユーザをベクトル化したものというイメージ.

    @param like more_like_thisクエリのlike句に与える文字列.
    @param size 何件の結果を取得するか.
    '''
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
                "like" : like,
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
      "sort" : [
          {"date_random": {"order": "desc"}}
      ] 
    }
    

if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # execute query.
    try:
        query = mk_mlt_and_order_by_date_query("elasticsearch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
    except Exception as e:
        print(e)
