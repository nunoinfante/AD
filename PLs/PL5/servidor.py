import http.server 
import socketserver 
PORT = 8888 
HOST = "localhost" 

list = []

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler): 
    def _set_headers(self, code): 
        self.send_response(code) 
        self.send_header('Content-type', 'text/html') 
        self.end_headers() 
    
    def do_GET(self): 
        path = [p for p in self.path.split('/') if p != '']

        if path[0] == 'lista':
            if path[1] == 'list':
                self._set_headers(200)
                self.wfile.write(f'{list}'.encode())
            elif path[1] == 'contains':
                if path[2] in list:
                    self._set_headers(200)
                    self.wfile.write(f'{path[2]}'.encode())
                else:
                    self._set_headers(404)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_POST(self):
        path = [p for p in self.path.split('/') if p != '']

        if path[0] == 'lista':
            if path[1] == 'append':
                self._set_headers(200)
                list.append(path[2])
            elif path[1] == 'clear':
                self._set_headers(200)
                list.clear()
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)        

    def do_PUT(self): 
        path = [p for p in self.path.split('/') if p != '']

        if path[0] == 'lista':
            if path[1] == 'update':
                content_length = int(self.headers['Content-Length'])
                new_word = self.rfile.read(content_length).decode()
                
                if path[2] in list:
                    self._set_headers(200)
                    list[list.index(path[2])] = new_word
                else:
                    list.append(new_word)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_DELETE(self): 
        path = [p for p in self.path.split('/') if p != '']

        if path[0] == 'lista':
            if path[1] == 'remove':
                if path[2] not in list:
                    self._set_headers(404)
                else:
                    list.remove(path[2])
                    self._set_headers(200)
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

HTTP_server = socketserver.TCPServer((HOST, PORT), MyHTTPHandler, True) 
HTTP_server.allow_reuse_address = True 
HTTP_server.serve_forever()