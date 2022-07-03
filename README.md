# elasticsearch 8.x の環境をdockerで整えるためのファイルを格納するリポジトリ

## 参考URL

- [Elasticsearch 8.0 を docker-compose で起動する][1]
- [(公式) Install Elasticsearch with Docker][2]

## ファイル/ディレクトリ説明

1. [docker-compose\_disable\_security.yaml](docker-compose_disable_security.yaml)

    簡単にセキュリティ無効化で利用したい場合

2. [docker-compose\_full.yaml](docker-compose_full.yaml)

    フル機能で利用したい場合

    |ユーザ名|パスワード|
    |:---|:---|
    |elastic|password|

3. start\_elasticsearch\_docker.txt

    elasticsearch serviceを起動するための手順.

4. [example\_01](./example_01/)

    dense_vectorを使った検索用のマッピング定義、クエリのサンプル.\
    環境設定用、テストクエリ実行用のpythonスクリプトを提供.


[1]: https://zenn.dev/fujimotoshinji/scraps/4fb4616976ee00 "Elasticsearch 8.0 を docker-compose で起動する"
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/8.0/docker.html "(公式) Install Elasticsearch with Docker"
