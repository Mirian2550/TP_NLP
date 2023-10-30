import os
import requests
import zlib
import nltk
from clasificador.clasificador import SVMClassifier
from clasificador.normalizador import title_compare
from scrapper.scrapper import Scraper
from clasificador.nube_palabras import generar_nube_palabras


nltk.download('punkt')
nltk.download('stopwords')


output_file = 'data/dataset.csv'

if os.path.exists(output_file):
    os.remove(output_file)

file_path = 'SBW-vectors-300-min5.bin.gz'
if not os.path.exists(file_path):
    url = "https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.bin.gz"
    local_filename = "SBW-vectors-300-min5.bin.gz"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            file.write(response.content)

        with open(local_filename, 'rb') as file:
            try:
                file_content = file.read()
                
                calculated_crc = zlib.crc32(file_content)
                
                print(f"Calculated CRC: {calculated_crc}")
                stored_crc = zlib.crc32(response.content)
                print(f"Stored CRC: {stored_crc}")
                
                if calculated_crc == stored_crc:
                    print("Descarga exitosa y CRC válido.")
                else:
                    print("Error: CRC no válido. El archivo descargado puede estar corrupto.")
            except Exception as e:
                print(f"Error al verificar CRC: {str(e)}")
else:
    print(f"El archivo {file_path} ya existe localmente.")

security_url = 'https://blog.segu-info.com.ar/sitemap.xml'
baby_url = 'https://blogdelbebe.com/post-sitemap.xml'
sports_url = 'https://www.espn.com.ar/googlenewssitemap'
food_url = 'https://www.recetasnestle.com.mx/sitemap.xml'

scraper = Scraper(output_file, security_url, baby_url, sports_url, food_url)
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

noticia_2 = 'Gemelos dicigóticos (llamados popularmente mellizos)' \
            'Gemelos MellizosEste tipo de gemelos se produce cuando dos óvulos son fecundados por dos espermatozoides. ' \
            'Los espermatozoides pueden ser de dos coitos diferentes y, de hecho, si se diera el caso, incluso de dos ' \
            'padres distintos.Cada óvulo evoluciona por separado con lo que cada embrión tendrá su propio saco amniótico ' \
            'y su propia placenta. Pueden ser del mismo o de diferente sexo y su semejanza física es la misma que se puede ' \
            'dar entre dos hermanos de embarazos distintos. Representa entre el 65% y el 75% de los casos de embarazos ' \
            'gemelares. Son más frecuentes este tipo de gemelos dado que, por un lado, responden a un gen hereditario y, ' \
            'por otro, pueden estar influidos por otros factores como los tratamientos de reproducción asistida, la avanzada ' \
            'edad de la madre o el uso prolongado de pastillas anticonceptivas, entre otros.' \
            'Gemelos monocigóticos Por una razón cuyo origen médico no ha sido aún identificado, en algunos casos, tras la ' \
            'fecundación del óvulo (durante los siguientes 14 días), este sufre una división, dando lugar a dos huevos ' \
            'idénticos. Es decir que de un solo óvulo fecundado por un solo espermatozoide surgen dos embriones. Por esta ' \
            'razón, los gemelos monocigóticos son del mismo sexo y se parecen físicamente e incluso psíquicamente. Sucede ' \
            'esto en el 25% de los embarazos gemelares.' \
            'Dependiendo de en qué momento post fecundación se produzca la división del óvulo, se darán procesos diferentes ' \
            'y, por tanto, los gemelos pueden ser de diferente tipo:' \
            'Tipos de gemelos Gemelos monocigóticos diplacentarios biamnióticos La división del óvulo tuvo lugar a los 3 ' \
            'días de la fecundación. Cada embrión cuenta con su propia placenta y su propio saco amniótico. Como en el caso ' \
            'de los gemelos dicigóticos (mellizos) pero con la diferencia de que estos provienen del mismo óvulo y no de dos ' \
            'óvulos distintos.Suelen darse en un tercio de los casos de embarazos monocigóticos.'

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

noticia_4 = 'Preparación: ' \
            'Colocar la última tapa y decorar cubriendo toda la torta con crema chantilly. Cubrirla con merengues ' \
            'triturados y gajos de duraznos en almíbar. Dejar la torta chajà en la heladera para que se enfríe y ' \
            'servir pasada una hora.' \
            'Cortá el bizcochuelo en 3 capas iguales y humedecerlas con el almíbar.' \
            'Untar una de las capas con dulce de leche y cubrirlo con trozos de merengues rotos, reservando algunos ' \
            'merengues para decorar.' \
            'En otra de las capas untar con crema chantilly y agregar merengues y bastantes duraznos cortados en ' \
            'cubos, ' \
            'reservando 4 mitades de duraznos en almíbar para decorar la torta posteriormente. '

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_4])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}')

generar_nube_palabras('Seguridad Informatica')
generar_nube_palabras('Bebes')
generar_nube_palabras('Deportes')
generar_nube_palabras('Recetas')

title_compare('Seguridad Informatica')