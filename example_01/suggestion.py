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
              "gram_size": 3,
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


def mk_auto_complete_suggestion_query(
        prefix: str,
        size: int
        ) -> Mapping[str, Any]:
    '''prefixに対応する単語をサジェストするクエリを返す.
    
    > 参考)
    > 
    > [Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    @param prefix 単語のプレフィックス.
    @param size suggestionとして返すドキュメント数.
    '''
    return {
      "suggest": {
        "location_suggest": {
          "prefix": prefix,
          "completion": {         
            "field": "suggest",
            "skip_duplicates": True,
            "size": size
          }
        }
      }
    }


def mk_auto_complete_suggestion_with_context_query(
        prefix: str,
        natin: str,
        prefecture: str,
        size: int
        ) -> Mapping[str, Any]:
    '''prefixに対応する単語をコンテキスト(nation, prefectureで指定)を指定してサジェストするクエリを返す.
    
    > 参考)
    > 
    > [Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    @param prefix 単語のプレフィックス.
    @param nation 所属する国(これがコンテキストの役割を持つ).
    @param prefecture 所属する県(これがコンテキストの役割を持つ).
    @param size suggestionとして返すドキュメント数.
    '''
    return {
      "suggest": {
        "location_suggest": {
          "prefix": prefix,
          "completion": {         
            "field": "suggest",
            "skip_duplicates": True,
            "contexts": {
              "area": [
                {
                  "context": nation,
                  "boost": 1
                },
                {
                  "context": prefecture,
                  "boost": 3
                }
              ]
            },
            "size": size
          }
        }
      }
    }


if __name__ == '__main__':
    index = "resource_test"
    index_auto_complete = "resource_auto_complete"
    index_auto_complete_with_context = "resource_auto_complete_with_context"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # execute query.
    try:
        # あえてelasticsearchのつづりを間違えてelasticsaerchとしている(aとeを逆転).
        query = mk_term_suggestion_query("elasticsaerch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
        print('----------')

        # あえてopensearchとelasticsearchの綴りを間違えている.
        query = mk_phrase_suggestion_query("opensrch elasticsaerch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
        print('----------')

        # プレフィックス(get auto complete candidates)
        for prefix, nation, prefecture in [("os", "日本", "北海道"), ("mi", "日本", "熊本県"), ("sh", "日本", "長野県")]:
            query = mk_auto_complete_suggestion_query(prefix, 5)
            res = els_clt.search(index=index_auto_complete, **query)
            print(json.dumps(res.body, ensure_ascii=False))
            print('----------')

            query = mk_auto_complete_suggestion_with_context_query(prefix, nation, prefecture, 10)
            res = els_clt.search(index=index_auto_complete_with_context, **query)
            print(json.dumps(res.body, ensure_ascii=False))
            print('----------')
    except Exception as e:
        print(e)
