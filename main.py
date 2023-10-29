from clasificador.clasificador import SVMClassifier
from scrapper.scrapper import Scraper
import nltk
from clasificador.nube_palabras import generar_nube_palabras

nltk.download('punkt')
nltk.download('stopwords')


output_file = 'data/dataset.csv'
security_url = 'https://blog.segu-info.com.ar/sitemap.xml'
cars_url = 'https://autotest.com.ar/pruebas-sitemap1.xml'
sports_url = 'https://www.espn.com.ar/googlenewssitemap'
food_url = 'https://www.recetasnestle.com.mx/sitemap.xml'

scraper = Scraper(output_file, security_url, cars_url, sports_url, food_url)
scraper.run_scrapers()

svm_classifier = SVMClassifier(output_file, kernel='sigmoid', c=1.0)
svm_classifier.train()

accuracy = svm_classifier.evaluate()
print(f'Precisión del modelo SVM: {accuracy}')

noticia_1 = ' El malware bancario brasileño conocido como "Grandoreiro" o "Mekotio" ha cruzado el charco, con una ' \
             'nueva campaña de TA2725 dirigida a clientes de España, además de Brasil, Argentina y México. ' \
             'La actividad de la Dark Web en América Latina ha aumentado en los últimos dos años y se concentra en ' \
             'gran medida en dos países. Según el reporte de SOCRadar "Brazil Threat Landscape", 360 mil millones de ' \
             'intentos de ciberataques azotaron la región en 2022, de los cuales 187 mil millones y 103 mil millones ' \
             'afectaron a México y Brasil, respectivamente.' \
             'Ahora hay cada vez más evidencia de que el cibercrimen en América Latina se está extendiendo hacia ' \
             'afuera. En lo que va de 2023 se detectaron más de 70 variantes de este troyano bancario. ' \
             'En América Latina, las detecciones de los sistemas de ESET muestran que Argentina (52%) es el país con ' \
             'más actividad de este Mekotio, seguido por México (17%), Perú (12%), Chile (10%) y Brasil (3%). '

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_1])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}')

noticia_2 = 'Preparación: ' \
            'Colocar la última tapa y decorar cubriendo toda la torta con crema chantilly. Cubrirla con merengues ' \
            'triturados y gajos de duraznos en almíbar. Dejar la torta chajà en la heladera para que se enfríe y ' \
            'servir pasada una hora.' \
            'Cortá el bizcochuelo en 3 capas iguales y humedecerlas con el almíbar.' \
            'Untar una de las capas con dulce de leche y cubrirlo con trozos de merengues rotos, reservando algunos ' \
            'merengues para decorar.' \
            'En otra de las capas untar con crema chantilly y agregar merengues y bastantes duraznos cortados en ' \
            'cubos, ' \
            'reservando 4 mitades de duraznos en almíbar para decorar la torta posteriormente. '

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_2])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}')

noticia_3 = 'Las dos incógnitas era el cómo y cuánto. Quién, era una pregunta que tenía una respuesta antes de ' \
            'comenzar ' \
            'el partido. Las chances de que Brasil pudiera perder puntos con Bolivia en Belem eran casi nulas. Es ' \
            'fútbol, por supuesto, pero las diferencias entre ambos equipos son demasiado grandes. Ni siquiera el ' \
            'penal que Viscarra le atajó a Neymar, a los 15’ y cuando el partido todavía estaba 0-0, pudo ser envión ' \
            'para la débil selección que ahora dirige Gustavo Costas. Había que dilucidar, entonces, cómo iba a ser ' \
            'el triunfo loca'

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_3])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}')

noticia_4 = 'El Chevrolet Camaro es un automóvil deportivo de dos puertas, con motor delantero montado ' \
            'longitudinalmente y de tracción trasera, producido por el fabricante estadounidense Chevrolet, ' \
            'división de General Motors (GM) desde 1966.1​ Compartía su plataforma y la mayoría de sus componentes ' \
            'con el Pontiac Firebird, también introducido en 1967.Se clasifica como un pony car y en algunas ' \
            'versiones ' \
            'también como un muscle car. Surgió como la respuesta de GM al creador del segmento de los "pony cars": ' \
            'el Ford Mustang. '
noticia_vectorized = svm_classifier.vectorizer.transform([noticia_4])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}')

generar_nube_palabras('Seguridad Informatica')
generar_nube_palabras('Autos')
generar_nube_palabras('Deportes')
generar_nube_palabras('Recetas')
