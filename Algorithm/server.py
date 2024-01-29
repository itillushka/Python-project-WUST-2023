"""
This module provides a simple HTTP server for handling Spotify's OAuth2 callback.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    """
        A simple HTTP request handler that responds to all GET requests with a 200 status code.
    """

    def do_GET(self):
        """
            Handles all GET requests by sending a 200 status code and a simple message.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'You can close this window')


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    """
        Starts the HTTP server.

        Args:
            server_class (HTTPServer, optional): The class to use for the server. Defaults to HTTPServer.
            handler_class (BaseHTTPRequestHandler, optional): The class to use for handling requests. Defaults to RequestHandler.
            port (int, optional): The port to listen on. Defaults to 8000.
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    """
        If this module is run as a script, start the server.
    """
    run()
