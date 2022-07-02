# Start Elaticsearch Docker Envrionment.

1. 以下のコマンドを実行してdockerサービスを起動する(起動していたら必要ない).

    sudo service docker start

2. ElasticsearchとKibanaのコンテナを起動する.

    docker-compose up -d
    
3. ElasticsearchとKibanaのコンテナを停止する.

    docker-compose down
