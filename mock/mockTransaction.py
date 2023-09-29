import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Gera uma resposta aleatória: 90% de chance de autorizado, 10% de chance de não autorizado
        authorized = random.choice([True]*9 + [False])

        msg = "Autorizado" if authorized else "Desautorizado"

        response = {
            "message": msg
        }

        self.wfile.write(json.dumps(response).encode('utf-8'))
        print(msg)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        

        # Gera uma resposta aleatória: 90% de chance de retornar status 200, 10% de chance de retornar outro status
        status_code = 200 if random.choice([True]*9 + [False]) else random.choice([400, 401, 403, 404])

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        print(f'\nstatus code: {status_code}')
        print(f'data: {data}\n')

        response = {
            "status_code": status_code,
            "message": "OK" if status_code == 200 else "Erro na solicitação"
        }

        self.wfile.write(json.dumps(response).encode('utf-8'))

# Define a porta do servidor
port = 3000

# Inicia o servidor mock
httpd = HTTPServer(('localhost', port), MockRequestHandler)
print(f'Servidor mock em execução na porta {port}')

# Mantém o servidor em execução
httpd.serve_forever()
