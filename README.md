# TP_NLP

Categorías:
- Seguridad Informática
- Tecnología
- Deportes
- Comida

# Deploy del Bot
Luego de pasar unas horas luchando porque se pudiera 
ejecutar tanto en windows como en linux optamos 
por crear un contenedor de docker simplifica 
el desarrollo, la colaboración y el despliegue, 
garantizando una mayor consistencia y reduciendo las diferencias en las versiones del sistema operativo. Esto ahorra tiempo y reduce la posibilidad de errores 
relacionados con las dependencias del sistema
## creacion de la imagen
`sudo docker build -t tp_nlp .`
## Ejcución del bot de telegram 
`sudo docker run -it tp_nlp`

# Proyecto

`pip install -r requirements`
`python main.py`