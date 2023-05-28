from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import pyautogui as pag

hostName = "localhost"
serverPort = 3000

pag.FAILSAFE = False

class MyServer(BaseHTTPRequestHandler):
    def updateScreenshot(self):
        screenshot = pag.screenshot()
        screenshot.save("./screen.png")

    def configureHeaders(self, isHTML=True):
        self.send_response(200)

        if isHTML:
            self.send_header("Content-Type", "text/html")
        else:
            self.send_header("Content-Type", "text/plain")

        self.end_headers()

    def addResponseData(self, data):
        self.wfile.write(bytes(data, "utf-8"))

    def do_GET(self):
        if (self.path.startswith("/screen.png")):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            with open("./screen.png", "rb") as f:
                self.wfile.write(f.read())
                f.close()

            return

        self.configureHeaders()
        self.updateScreenshot()

        print("Request:", self.path)

        if (self.path == "/"):
            with open("./input.html", "r") as f:
                self.addResponseData(f.read())
                f.close()

    def do_POST(self):
        print("Post request recieved")
        print(self.path)

        self.updateScreenshot()
        
        if (self.path.startswith("/type")):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            params = urllib.parse.parse_qs(post_data)

            toWrite = params.get(bytes("totype", "utf-8"))[0].decode()
            print(toWrite)

            pag.typewrite(toWrite)

            self.configureHeaders()
            self.addResponseData("<script>window.location.href = document.referrer;</script>")

        if (self.path.startswith("/movemouse")):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            params = urllib.parse.parse_qs(post_data)

            x = params.get(bytes("x", "utf-8"))[0].decode()
            y = params.get(bytes("y", "utf-8"))[0].decode()

            print(x, y)

            pag.moveTo(int(x), int(y), 0.2)

            self.configureHeaders()
            self.addResponseData("<script>window.location.href = document.referrer;</script>")

        if self.path.startswith("/click"):
            print("Click request detected")

            if "left" in self.path:
                pag.leftClick()

            elif "right" in self.path:
                pag.rightClick()

            elif "middle" in self.path:
                pag.middleClick()

            self.configureHeaders()
            self.addResponseData("<script>window.location.href = document.referrer;</script>")

        if self.path.startswith("/press"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            params = urllib.parse.parse_qs(post_data)

            toPress = params.get(bytes("topress", "utf-8"))[0].decode()

            pag.press(toPress) 

            self.configureHeaders()
            self.addResponseData("<script>window.location.href = document.referrer;</script>")

        if self.path.startswith("/hotkey"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            params = urllib.parse.parse_qs(post_data)

            tohotkey = params.get(bytes("tohotkey", "utf-8"))[0].decode()

            pag.hotkey(tohotkey.split(","))

            self.configureHeaders()
            self.addResponseData("<script>window.location.href = document.referrer;</script>")
            



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")