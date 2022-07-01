import json

from typing import List

import numpy as np
from elasticsearch import Elasticsearch


def imput_data(
        els_clt: Elasticsearch,
        index: str,
        src_text: str, 
        labels: List[str]) -> None:
    doc_id = 0
    for text in src_text.split('。'):
        vec = np.random.randn(3)
        vec = (vec / np.linalg.norm(vec)).tolist()
        doc = {
            'doc_text': text,
            'doc_vector': vec,
            'label': labels[np.random.choice(len(labels))]
        }
        print(doc)
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
    els_clt.indices.delete(index=index)
    with open('mapping.json', 'r') as inF:
        mapping = json.load(inF)
    els_clt.indices.create(index=index, **mapping)

    # input data
    src_text = '''Elasticsearch（エラスティックサーチ）はLucene基盤の分散処理マルチテナント対応検索エンジンである。かつてはオープンソースソフトウェア（OSS）だったが、現在はプロプライエタリソフトウェアである。[要出典] 現在はオランダ・アムステルダムに本社を置くElastic社が中心になって開発が進められている[2]。なお「Elastic Search」といったように間に空白を入れる・「search」の頭を大文字にするといった表記は誤り（ただしVer.1.0.0リリース前にはそのような表記も混在していた）[3]。
    全文検索に特化しており、他のソリューションと比較しても圧倒的な全文検索スピードと利便性を誇る[4]。Elasticsearchの内部ではApache Luceneが提供する超高速全文検索をフル活用しており、スケーラブル、スキーマレス、マルチテナントを特長とする。
    Javaで組まれたソフトウェアであり、商用を含めた検索エンジン業界では一番人気（2016年9月現在）[5]とされている。著名な導入例としてWikimedia[6]、Facebook[7]、StumbleUpon[8]、Mozilla[9][10]、アマデウスITグループ、Quora[11]、Foursquare[12]、Etsy[13]、SoundCloud[14]、GitHub[15]、FDA[16]、欧州原子核研究機構[17]、Stack Exchange[18]、Netflix[19]、Pixabay[20]、Sophosなどがある。
    Amazon.comは、Amazon Web Services（AWS）においてElasticsearchをベースとした「Amazon Elasticsearch Service」を提供していたが、Elastic社はかねてより「AWSはOSSにタダ乗りする形で大きな利益を得ている」と主張していた。2021年にElastic社はElasticsearchのライセンスを変更し、商用マネージドサービスでのElasticsearchの利用を制限する行為に踏み切った。これに対しAmazonは、ライセンス変更前のElasticsearchをforkする形で新たに「OpenSearch」を立ち上げており、同年9月に今後はOpenSearchベースのサービスを提供していくことを発表している[21]。
    '''
    labels = ['hoge', 'fuga', 'foo', 'bar']
    imput_data(els_clt=els_clt, index=index, src_text=src_text, labels=labels)
