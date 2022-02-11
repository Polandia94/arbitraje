
################************************* EDITAR CON LOS DATOS PROPIOS *************##########

# Definir un rpc endpoint:
httpEndPoint = "https://bsc.getblock.io/mainnet/?api_key="

# Definir el listado de tokens que se desea intercambiar
tokens = ["0x0eb3a705fc54725037cc9e008bdede697f62f335", "0x2170ed0880ac9a755fd29b2688956bd959f933f8", "0x55d398326f99059ff775485246999027b3197955", "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d", "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe", "0x3ee2200efb3400fabb9aacf31297cbdd1d435d47", "0x7083609fce4d1d8dc0c979aab8c869ea2c873402", "0xba2ae424d960c26247dd6c32edc70b295c744c43", "0x1ce0c2827e2ef14d5c4f29a091d735a204794041", "0x2859e4544c4bb03966803b044a93563bd2d0dd4d", "0xe9e7cea3dedca5984780bafc599bd69add087d56", "0x23396cf899ca06c4472205fc903bdb4de249d6fc", "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3", "0x4338665cbb7b2485a8855a139b75d5e34ab0db94",
"0x1fc9004ec7e5722891f5f38bae7678efcb11d34d", "0xc748673057861a797275CD8A068AbB95A902e8de", "0x9ac983826058b8a9c7aa1c9171441191232e8404", "0xfd7b3a77848f1c2d67e05e54d78d174a0c850335", "0xf68c9df95a18b2a5a5fa1124d79eeeffbad0b6fa", "0x8e17ed70334c87ece574c9d537bc153d8609e2a3", "0xea998d307aca04d4f0a3b3036aba84ae2e409c0a", "0x7950865a9140cb519342433146ed5b40c6f210f7", "0xaec945e04baf28b135fa7c640f624f8d90f1c3a6", "0xb6c53431608e626ac81a9776ac3e999c5556717c", "0x1f9f6a696c6fd109cd3956f45dc709d2b3902163", "0x47bead2563dcbf3bf2c9407fea4dc236faba485a", "0x8da443f84fea710266c8eb6bc34b71702d033ef2", "0xadbaf88b39d37dc68775ed1541f1bf83a5a45feb", "0xf21768ccbc73ea5b6fd3c687208a7c2def2d966e", "0x4b0f1812e5df2a09796481ff14017e6005508003", "0xa3f020a5c92e15be13caf0ee5c95cf79585eecc9"]

# Definir dos Dex. En Este caso use Pancake y Bakery
factoryAddressPancake = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
factoryAddressBakery = "0x01bF7C66c6BD861915CdaaE475042d3c4BaE16A7"
pancakeRouter="0x10ED43C718714eb63d5aA57B78B54704E256024E"
bakeryRoute= "0xCDe540d7eAFE93aC5fE6233Bee57E1270D3E330F"

# Seleccionar el contrato deployado para el intercambio
contratoAddress = "0x"

# PrivateKey y address de la cuenta

privateKey = ""
cuenta = "0x"

################************************* A PARTIR DE ACA NO EDITAR *************##########


import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from abi import abiPar, abiFactory, abiContrato
w3 = Web3(Web3.HTTPProvider(httpEndPoint))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Se contruyen los contratos
contractFactoryPancake = w3.eth.contract(address=Web3.toChecksumAddress(factoryAddressPancake), abi=abiFactory)
contractFactoryBakery = w3.eth.contract(address=Web3.toChecksumAddress(factoryAddressBakery), abi=abiFactory)
contrato = w3.eth.contract(address=contratoAddress, abi=abiContrato)

# Se define el address de WBNB
wbnb = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

# Se crean los listados vacios de pares
paresPancake = []
paresBakery = []
n = 0
while n < len(tokens):
    par = contractFactoryPancake.functions.getPair(w3.toChecksumAddress(tokens[n]),wbnb).call()
    paresPancake.append(par)
    par = contractFactoryBakery.functions.getPair(w3.toChecksumAddress(tokens[n]),wbnb).call()
    paresBakery.append(par)
    n = n+1

#Se define el minimo y maximo de diferencia a partir del cual se realiza la transaccion
maximo = 0.991
minimo = 1.009

# Se crea el listado de contratosDex con los pares y los tokens
contratosDex = []
n = 0
while n < len(paresPancake):
    contractPancake = w3.eth.contract(address=Web3.toChecksumAddress(paresPancake[n]), abi=abiPar)
    contractBakery = w3.eth.contract(address=Web3.toChecksumAddress(paresBakery[n]), abi=abiPar)
    if paresPancake[n] != "0x0000000000000000000000000000000000000000" and paresBakery[n] != "0x0000000000000000000000000000000000000000":
        token0 = contractPancake.functions.token0().call()
        token1 = contractPancake.functions.token1().call()
        contratosDex.append({"addressPancake":paresPancake[n], "addressBakery":paresBakery[n], "token0":token0, "token1":token1})
    n = n +1

# Funcion para obtener precio para un token en un dex
def obtenerPrecio(par, dex):
    if par[dex] != "0x0000000000000000000000000000000000000000":
        contractPAR = w3.eth.contract(address=Web3.toChecksumAddress(par[dex]), abi=abiPar)
        token0, token1, bloque = contractPAR.functions.getReserves().call()
        if par["token0"] == wbnb:
            if token0 > 1*10**18:
                return (token0/token1, 1)
        elif par["token1"] == wbnb:
            if token1 > 1*10**18:
                return (token1/token0, 0)

# Funcion para enviar na transaccion
def enviarTransaccion(funcion):
    transaccion = funcion.buildTransaction(dict(
        nonce=w3.eth.get_transaction_count(cuenta),
        gasPrice=Web3.toWei(6, 'gwei'),
        value=0
        ))
    signed_txn = w3.eth.account.sign_transaction(transaccion, privateKey)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
# Funcion central. Obtiene el precio para un par, si la diferencia es sustancial realiza el cambio
def cambiarTokens(par):
    precioPancake = obtenerPrecio(par, "addressPancake")
    precioBakery = obtenerPrecio(par, "addressBakery")
    if precioPancake is not None and precioBakery is not None:
        diferencia = precioPancake[0]/precioBakery[0]
        if diferencia > minimo:
            if precioPancake[1] == 0:
                enviarTransaccion(contrato.functions.cambiarSeguro(par["token0"], pancakeRouter, bakeryRoute))
            else:
                enviarTransaccion(contrato.functions.cambiarSeguro(par["token1"], pancakeRouter, bakeryRoute))
        elif diferencia < maximo:
            if precioPancake[1] == 0:
                enviarTransaccion(contrato.functions.cambiarSeguro(par["token0"], bakeryRoute, pancakeRouter))
            else:
                enviarTransaccion(contrato.functions.cambiarSeguro(par["token1"], bakeryRoute, pancakeRouter))
        return diferencia
    

# loop permanente de funcionamiento
while True:
    for par in contratosDex:    
        resultado = cambiarTokens(par)
    print("loop")
    time.sleep(20)
    




