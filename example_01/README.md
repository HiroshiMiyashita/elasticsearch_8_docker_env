# サンプルの説明

## サンプル実行方法

### 環境設定方法

1. pythonのパッケージをインストール

    `python -m pip install -r requirements.txt`

2. elasticsearchサーバにテンプレート登録、インデックスの作成、データの投入を行う.

    `python setup_index.py`

### サンプルの実行

1. 検索結果を検索対象ドキュメント内のベクトルフィールドとクエリで与えるベクトルの類似度で補正するクエリを実行する.

    `python mlt_and_rescore_by_vec_sim.py`

2. 検索結果を日付フィールドでソートするクエリを実行する.

    `python mlt_and_sort_by_date.py`

3. 検索結果のドキュメント内の重要単語を取得するクエリを実行する.

    `python mlt_and_sig_text_term.py`

4. ちょっとしたつづりのミスなどを補正するための補正候補を出力するクエリ、オートコンプリート用クエリを実行する.

    `python suggestion.py`

## ファイル説明

1. [requirements.txt](./requirements.txt)

    サンプル実行に必要となるpythonパッケージ.

2. [setup\_index.py](./setup_index.py)

    サンプルクエリを字っこするためのAnalyzer定義、インデックス作成、データを投入するためのスクリプト.

3. [mlt\_and\_rescore\_by\_vec\_sim.py](./mlt_and_rescore_by_vec_sim.py)

    検索結果を検索対象ドキュメント内のベクトルフィールドとクエリで与えるベクトルの類似度で補正するクエリを実行する.

4. [mlt\_and\_sort\_by\_date.py](./mlt_and_sort_by_date.py)

    検索結果を日付フィールドでソートするクエリを実行する.

5. [mlt\_and\_sig\_text\_term.py](./mlt_and_sig_text_term.py)

    検索結果のドキュメント内の重要単語を取得するクエリを実行する.\
    関連する単語を出力するのに利用することを想定したaggregationを実行する.
    
6. [suggestion.py](./suggestion.py)

    ちょっとしたつづりのミスなどを補正するための補正候補を出力するクエリ、オートコンプリート用クエリを実行する.

7. [analysis\_template.json](./analysis_template.json)

    文をトークンに分解するアナライザー、文字列を正規化するためのノーマライザーのテンプレートの定義.
    
8. [mapping.json](./mapping.json)

    インデックスを作成するためのマッピング定義.

9. [mapping\_autocomplete.json](./mapping_autocomplete.json)

    オートコンプリート用のインデックスのマッピング定義.

10. [mapping\_autocomplete\_with\_context.json](./mapping_autocomplete_with_context.json)

    コンテキスト付きオートコンプリート用のインデックスのマッピング定義.

11. [corpus.txt](./corpus.txt)

    投入するデータ.

12. [location\_name.txt](./location_name.txt)

    オートコンプリートに使用するデータ.
