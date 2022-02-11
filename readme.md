Bot para arbitraje entre dos exchanges
El bot está pensado para la red bsc(aunque adaptando wbnb por weth puede utilizarse en Ethereum)

Requiere en primer lugar compilar y deployar el contrato(Probado con remix y solidity 0.8.7)

En segundo lugar instalar las dependencias con:
pip3 install -r requeriments.txt

Luego modificar el comienzo del archivo compareSimple.py para colocar los valores adecuados

por ultimo ejecutar compareSimple para de manera permanente buscar las oportunidades y realizar los intercambios.
Es posible adaptar las condiciones a las cuales un intercambio se considerará rentable

El sistema es muy sencillo y no se encuentra optimizado, por lo que es poco probable que pueda resultar rentable