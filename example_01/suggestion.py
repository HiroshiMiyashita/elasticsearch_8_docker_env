import json

from typing import Any
from typing import List
from typing import Mapping

import numpy as np
from elasticsearch import Elasticsearch


def mk_term_suggestion_query(
        text: str,
        size: int
        ) -> Mapping[str, Any]:
    '''text内のトークンと似ているdoc_textフィールドにあるトークンをサジェストするクエリを返す.
    
    つづりのミスとかを補正したり、その候補を提示したりするためなどで使用する.
    
    > 参考)
    > 
    > [Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    @param text suggest対象となるトークンを含むテキスト.
    @param size トークンごとの最大サジェスト数.
    '''
    return {
      "suggest": {
          "text": text,
          "term_suggestion": {
            "term": {
              "field": "doc_text",
              "analyzer": "japanese_analyzer",
              "sort": "score",
              "size": size
            },
          }
      },
      "size": 0
    }


def mk_phrase_suggestion_query(
        text: str,
        size: int
        ) -> Mapping[str, Any]:
    '''textのフレーズに対してフレーズのサジェストを行うするクエリを返す.
    
    フレーズの中に綴りのミスなどを補正などに使用するクエリ.\
    内部的にはトークンのサジェスチョン機能を使っているが、単純に可能性の高いトークンを出力するだけではなく、共起の情報も利用している.
    
    > 参考)
    > 
    > [Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    @param text suggest対象となる単語を含むテキスト.
    @param size suggestionとして返すフレーズ数（多分）.
    '''
    return {
      "suggest": {
          "text": text,
          "phrase_suggestion": {
            "phrase": {
              "field": "doc_text.shingle",
              "size": size,
              "direct_generator": [
                {
                  "field": "doc_text.shingle",
                  "suggest_mode": "always"
                },
                {
                  "field": "doc_text.reverse",
                  "suggest_mode": "always",
                  "pre_filter": "japanese_reverse_analyzer",
                  "post_filter": "japanese_reverse_analyzer"
                }
              ]
            },
          }
      },
      "size": 0
    }


if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # execute query.
    try:
        # あえてelasticsearchのつづりを間違えてelasticsaerchとしている(aとeを逆転).
        query = mk_term_suggestion_query("elasticsaerch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))

        # あえてopensearchとelasticsearchの綴りを間違えている.
        query = mk_phrase_suggestion_query("opensrch elasticsaerch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
    except Exception as e:
        print(e)
