from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import pyautogui as pag
import cv2 as cv

hostName = "localhost"
serverPort = 3000
webServer = None # We'll assign later.

def init():
    pag.FAILSAFE = False


class MyServer(BaseHTTPRequestHandler):
    def updateScreenshot(self):
        screenshot = pag.screenshot()
        screenshot.save("./screen.png")


    def redirectToReferer(self): 
        self.addResponseData("<script>window.location.href = document.referrer;</script>")


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
        print(f"GET request from {self.client_address}; Path: {self.path}")

        if self.path.startswith("/killserver"):
            webServer.server_close()
            print(f"Stopping web server from {self.client_address}...")

        if (self.path.startswith("/screen.png")):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            with open("./screen.png", "rb") as f:
                self.wfile.write(f.read())
                f.close()

            return
        
        if self.path.startswith("/webcam.png"):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
    
            # Screenshot webcam and save as ./webcam.png
            cam = cv.VideoCapture(0)
            frame, img = cam.read()

            if frame:   
                cv.imwrite("webcam.png", img)

            cam.release()

            # Read and deliver
            with open("./webcam.png", "rb") as f:
                self.wfile.write(f.read())
                f.close()

            return

        self.configureHeaders()
        self.updateScreenshot()

        if (self.path == "/"):
            with open("./input.html", "r") as f:
                self.addResponseData(f.read())
                f.close()

    def do_POST(self):
        print(f"Post request recieved from {self.client_address}")
        print(self.path)

        self.updateScreenshot()
        
        contentLengt = int(self.headers["Content-Length"])
        postData = self.rfile.read(contentLengt)

        if (self.path.startswith("/type")):
            params = urllib.parse.parse_qs(postData)

            toWrite = params.get(bytes("totype", "utf-8"))[0].decode()
            print(toWrite)

            pag.typewrite(toWrite)

            self.configureHeaders()
            self.redirectToReferer()

        if (self.path.startswith("/movemouse")):
            params = urllib.parse.parse_qs(postData)

            x = params.get(bytes("x", "utf-8"))[0].decode()
            y = params.get(bytes("y", "utf-8"))[0].decode()

            print(x, y)

            pag.moveTo(int(x), int(y), 0.2)

            self.configureHeaders()
            self.redirectToReferer()

        if self.path.startswith("/click"):
            print("Click request detected")

            if "left" in self.path:
                pag.leftClick()

            elif "right" in self.path:
                pag.rightClick()

            elif "middle" in self.path:
                pag.middleClick()

            self.configureHeaders()
            self.redirectToReferer()

        if self.path.startswith("/press"):
            params = urllib.parse.parse_qs(postData)

            toPress = params.get(bytes("topress", "utf-8"))[0].decode()

            pag.press(toPress) 

            self.configureHeaders()
            self.redirectToReferer()

        if self.path.startswith("/hotkey"):
            params = urllib.parse.parse_qs(postData)

            tohotkey = params.get(bytes("tohotkey", "utf-8"))[0].decode()

            pag.hotkey(tohotkey.split(","))

            self.configureHeaders()
            self.redirectToReferer()


def main(): 
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started on {hostName, serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":       
    main()