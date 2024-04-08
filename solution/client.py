import requests

url="http://localhost:8000/"

("print listas------------")
get_response=requests.get(url+"/pedidos")
print(get_response.text)
("agregas pedido------------")

nuevo_pedido=[
    {
        2:{
            "tipo":"fisico",
            "client":"juan Perez",
            "status":"pendiente",
            "payment":"tarjeta de credito",
            "shipings":"10",
            "products":"camisa",
        }
    }
]

post_response=requests.request(method="POST",url=url+"/pedidos", json=nuevo_pedido)
print(post_response.text)
("print listas------------")
get_response=requests.get(url+"/pedidos")
print(get_response.text)
