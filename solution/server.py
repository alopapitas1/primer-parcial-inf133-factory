from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse
pedidos=[
    {
        1:{
            "tipo":"fisico",
            "client":"juan Perez",
            "status":"pendiente",
            "payment":"tarjeta de credito",
            "shipings":"10",
            "products":"camisa",
        },
    }
]

class Producto:
    def __init__(self,tipo,client,status,payment,shipings,products):
        self.tipo=tipo
        self.client=client
        self.status=status
        self.payments=payment
        self.shipings=shipings
        self.products=products

class Fisico(Producto):
    def __init__(self,tipo,client,status,payment,shipings,products,code,expiration):
        super().__init__("fisico",tipo,client,status,payment,shipings,products)

class digital(Producto):
    def __init__(self,tipo,client,status,payment,code,expiration):
        super().__init__("fisico",tipo,client,status,payment,code,expiration)


class ProductFactory:
    @staticmethod
    def crear_producto(tipo,client,status,payment,shipings,products,code,expiration):
        if tipo == "fisico":
            return Fisico(tipo,client,status,payment,shipings,products)
        elif tipo == "digital":
            return digital(tipo,client,status,payment,code,expiration)
        else:
            raise ValueError("Tipo de producto no valido")
        
class PedidoService:
    def __init__(self):
        self.factory=ProductFactory()

    def create_pedido(self,data):
        tipo=data.get('tipo',None)
        client=data.get('client',None)
        status=data.get('status',None)
        payment=data.get('payment',None)
        shipings=data.get('shipings',None)
        products=data.get('products',None)
        
        pedido=self.factory.crear_producto(
            tipo,client,status,payment,shipings,products
        )
        id=max(pedidos[0].keys())+1
        pedidos[0][id]=(pedido.__dict__)
        return pedido.__dict__
    
    
    def buscar_status(self,status):
        n=[{}]
        lista=pedidos[0].values()
        for i, animal in enumerate(lista):
            if animal['status']==status:
                n[0][i+1]=animal
        return n
    
    def actualizar_pedido(self,id,data):
        lista=pedidos[0].keys()
        for i in lista:
            if i==id:
                pedidos[0][i].update(data)
                return pedidos
        return None
    
    def borrar_pedido(self,id):
        lista=pedidos[0].keys()
        for i in lista:
            if i==id:
                del pedidos[0][i]
                return pedidos
        return None

class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class PedidoHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=PedidoService()
        super().__init__(*args,**kwargs)
    
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path == "/pedidos":
            if 'status' in query_params:
                status=query_params['status'][0]
                filtrados_esta=self.controller.buscar_status(status)
                if filtrados_esta[0]:
                    HTTPResponseHandler.response_handler(self,200,filtrados_esta)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Pedido no encontrada"})
            else:
                HTTPResponseHandler.response_handler(self,200,pedidos)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/pedidos":
            data=HTTPResponseHandler.read_data(self)
            animal_c=self.controller.create_pedido(data)
            HTTPResponseHandler.response_handler(self,201,animal_c)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/pedidos/"):
            id=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            pedido=self.controller.actualizar_pedido(id,data)
            if pedido:
                HTTPResponseHandler.response_handler(self,200,pedido)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrada"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/pedidos/"):
            id=int(self.path.split("/")[-1])
            pedido=self.controller.borrar_pedido(id)
            if pedido:
                HTTPResponseHandler.response_handler(self,200,pedido)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})


def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,PedidoHandler)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
            
    
    
    
    
        
