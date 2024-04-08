from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse , parse_qs


pedidos=[
    {
        "tipo":"fisico",
        "id":"1",
        "client":"juan",
        "status":"pendiente",
        "payment":"paypal",
        "shipings":"200",
        "products":"camisa",
    },
]










class Pedido:
    def __init__(self,tipo, id,client,status,payment,shiping,products,code,expiration):
        self.tipo=tipo
        self.id=id
        self.client=client
        self.status=status
        self.payment=payment
        self.shiping=shiping
        self.products=products
        self.code=code
        self.expiration=expiration
        

class Fisico:
    def __init__(self,id,client,status,payment,shipings,products,code,expiration):
        super().__init__("fisico", id,client,status,payment,shipings,products,code,expiration)
        
class digital:
    def __init__(self,id,client,status,payment,shipings,products,code,expiration):
        super().__init__("digital", id,client,status,payment,shipings,products,code,expiration)
        

class FabricPedido:
    @staticmethod
    def crear_pedido(tipo,id,client,status,payment,shipings,products,code,expiration):
        if tipo=="fisico":
            return Fisico(id,client,status,payment,shipings,products,None,None)
        elif tipo=="digital":
            return Fisico(id,client,status,payment,None,None,code,expiration)
        
        else:
            raise ValueError("tipo de pedido no valido")

class PedidoService:
    def __init__(self):
        self.fafabrica=FabricPedido()
        
    def crear_pedido(self, data):
        tipo=data.get("tipo",None)
        id=data.get("id",None)
        client=data.get("client",None)
        status=data.get("status",None)
        payment=data.get("payment",None)
        shipings=data.get("shipings",None)
        products=data.get("products",None)
        code=data.get("code",None)
        expiration=data.get("expiration",None)
        pedido=self.fafabrica.crear_pedido(tipo,id,client,status,payment,shipings,products,code,expiration)
        
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
    
    def borrar_animal(self,id):
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
    
class AnimalHandler(BaseHTTPRequestHandler):
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
