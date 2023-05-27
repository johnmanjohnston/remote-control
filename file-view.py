from http.server import HTTPServer, SimpleHTTPRequestHandler

host = "localhost"
port = 8000
print(f"http://{host}:{port}")
httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
httpd.serve_forever()
