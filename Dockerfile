FROM docker.elastic.co/elasticsearch/elasticsearch:8.2.3

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-icu
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-kuromoji
