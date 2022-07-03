import json

from typing import Any
from typing import List
from typing import Mapping

import numpy as np
from elasticsearch import Elasticsearch


def mk_suggestion_query(
        text: str,
        size: int
        ) -> Mapping[str, Any]:
    '''text内の単語で似ているdoc_textフィールドにある単語をサジェストするクエリを返す.
    
    追加意味地としては、つづりのミスとかを補正したり、その候補を提示したりする.
    
    > 参考)
    > 
    > [Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    @param text suggest対象となる単語を含むテキスト.
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

if __name__ == '__main__':
    index = "resource_test"

    els_clt: Elasticsearch = Elasticsearch(hosts='http://localhost:9200')

    # execute query.
    try:
        # あえてelasticsearchのつづりを間違えてelasticsaerchとしている(aとeを逆転).
        query = mk_suggestion_query("elasticsaerch lucene fork", 5)
        res = els_clt.search(index=index, **query)
        print(json.dumps(res.body, ensure_ascii=False))
    except Exception as e:
        print(e)
