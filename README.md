Realtime web test
=================

Exploring websockets and messaging. This test project combines code samples found on the web.

Requirements:

* rabbitmq-server >= 3.0.0
* tornado >= 2.3
* pika >= 0.9.8


Running:

* Open 2 terminal windows and 2 browser tabs
* on one terminal window run the server:

    python server.py

* Go to http://localhost:8888 on both browser tabs
* on the second terminal window run the producer and watch the messages load on the browser

    python producer.py

