# サンプルの説明

## ファイル説明

1. [setup_index.py](./setup_index.py)

    サンプルクエリを字っこするためのAnalyzer定義、インデックス作成、データを投入するためのスクリプト.

2. [analysis_template.json](./analysis_template.json)

    文をトークンに分解するアナライザー、文字列を正規化するためのノーマライザーのテンプレートの定義.
    
3. [mapping.json](./mapping.json)

    インデックスを作成するためのマッピング定義.

4. [corpus.txt](./corpus.txt)

    投入するデータ.
    
5. [mlt_and_rescore_by_vec_sim.py](./mlt_and_rescore_by_vec_sim.py)

    検索結果を検索対象ドキュメント内のベクトルフィールドとクエリで与えるベクトルの類似度で補正するクエリを実行する.

6. [mlt_and_sort_by_date.py](./mlt_and_sort_by_date.py)

    検索結果を日付フィールドでソートするクエリを実行する.

7. [mlt_and_sig_text_term.py](./mlt_and_sig_text_term.py)

    検索結果のドキュメント内の重要単語を取得するクエリを実行する.\
    関連する単語を出力するのに利用することを想定したaggregationを実行する.
    
8. [suggestion.py](./suggestion.py)

    ちょっとしたつづりのミスなどを補正するための補正候補を出力するクエリを実行する.\
