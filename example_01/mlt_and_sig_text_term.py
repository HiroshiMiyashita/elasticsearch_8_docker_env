import json

from typing import Any
from typing import List
from typing import Mapping

import numpy as np
from elasticsearch import Elasticsearch


def mk_mlt_and_agg_sig_text_query(
        like: str,
        size: int,
        ) -> Mapping[str, Any]:
    '''クエリの結果のドキュメント集合の中でdoc_textフィールドに含まれる重要な単語を取得するクエリを返す.
    
    内部的にsignificant_textアグリゲーションを使用しているためtext型のフィールドのみ対応.
    
    クエリ内に含まれる単語も返ってくるので注意.\
    クエリ内の単語を取り除きたい場合には、別途Analyze APIを使ってlike句として指定した文字列を解析し、このクエリの結果から削除する処理が必要となる.
    
    > 参考)
    > 
    > [Significant text aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-significanttext-aggregation.html)\
    > [Analyze API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html)

    @param like more_like_thisクエリのlike句に与える文字列.
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
      "aggregations" : {
          "sig_keyword": {
              "sampler": {
                "shard_size": 100
              },
              "aggregations": {
                  "keywords": {
                      "significant_text": {
                          "field": "doc_text",
                          "filter_duplicate_text": True
                      }
                  }
              }
          }
      },
      "size": 0
    }


def mk_mlt_and_agg_sig_term_query(
        like: str,
        size: int,
        ) -> Mapping[str, Any]:
    '''クエリの結果のドキュメント集合の中でlabelフィールドに含まれる重要な単語を取得するクエリを返す.
    
    内部的にsignificant_termアグリゲーションを使用している.
    
    クエリ内に含まれるラベルも返ってくる.
    
    > 参考)
    > 
    > [Significant terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-significantterms-aggregation.html)\
    > [Analyze API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html)

    @param like more_like_thisクエリのlike句に与える文字列.
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
      "aggregations" : {
          "sig_label": {
              "significant_terms": {
                "field": "label"
              }
          }
      },
      "size": 0
    }
    

if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # execute query.
    try:
        query = mk_mlt_and_agg_sig_text_query("elasticsearch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
        
        query = mk_mlt_and_agg_sig_term_query("elasticsearch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
    except Exception as e:
        print(e)
