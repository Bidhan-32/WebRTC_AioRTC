First install the required packages:

    $ cd server

    $ pip install -r requirements.txt 

When you start the example, it will create an HTTP server which you
can connect to from your browser:
    
    $ cd server

    $ python main.py

You can then browse to the following page with your browser:

http://localhost:8080

Once you click `Start` the browser will send the audio and video from its
webcam to the server.

The server will play a pre-recorded audio clip and send the received video back
to the browser, optionally applying a transform to it.

In parallel to media streams, the browser sends a 'ping' message over the data
channel, and the server replies with 'pong'.


Additional options
------------------

If you want to enable verbose logging, run:

    $ cd server

    $ python server.py -v

Running the server in docker
----------------------------

If you have docker setup, run:

    $ cd server

    $ docker build -t aiortc_server .

    $ docker run -p 8080:8080 -it --rm aiortc_server

You can then browse to the following page with your browser:

http://localhost:8080


Setting up flutter
------------------

First install the required packages.
- flutter pub get

Then run the app
- flutter run
