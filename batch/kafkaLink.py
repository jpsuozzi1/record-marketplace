# Script to pull messages from Kafka and indexs them in ES
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

import json
import time

es = Elasticsearch(['es'])
time.sleep(20) # Wait a while until Kafka is up and running
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    new_listing = json.loads((message.value).decode('utf-8')) # Load listing from consumer
    es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing) # Add listing to ES
    es.indices.refresh(index="listing_index") # Refresh elastic search
