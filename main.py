import os
import time

import requests
import zlib

from clasificador.clasificador import SVMClassifier

from clasificador.normalizador import title_compare
from scrapper.scrapper import Scraper
from clasificador.nube_palabras import generar_nube_palabras

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

security_url = 'http://blog.segu-info.com.ar/sitemap.xml?page=2'
baby_url = 'https://blogdelbebe.com/post-sitemap.xml'
sports_url = 'https://www.espn.com.ar/googlenewssitemap'
food_url = 'https://www.recetasnestle.com.mx/sitemap.xml'
start_time = time.time()
print('Hora de inicio scrapper:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
scraper = Scraper(output_file, security_url, baby_url, sports_url, food_url)
scraper.run_scrapers()
end_time = time.time()
execution_time = end_time - start_time
print('Hora de fin scrapper:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))

svm_classifier = SVMClassifier(output_file, kernel='linear', c=1.0)
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
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}', ' esperada:Seguridad')

noticia_2 = 'Gemelos dicigóticos (llamados popularmente mellizos)' \
            'Gemelos MellizosEste tipo de gemelos se produce cuando dos óvulos son fecundados por dos ' \
            'espermatozoides. ' \
            'Los espermatozoides pueden ser de dos coitos diferentes y, de hecho, si se diera el caso, incluso de ' \
            'dos ' \
            'padres distintos.Cada óvulo evoluciona por separado con lo que cada embrión tendrá su propio saco ' \
            'amniótico ' \
            'y su propia placenta. Pueden ser del mismo o de diferente sexo y su semejanza física es la misma que se ' \
            'puede ' \
            'dar entre dos hermanos de embarazos distintos. Representa entre el 65% y el 75% de los casos de ' \
            'embarazos ' \
            'gemelares. Son más frecuentes este tipo de gemelos dado que, por un lado, responden a un gen ' \
            'hereditario ' \
            'y, ' \
            'por otro, pueden estar influidos por otros factores como los tratamientos de reproducción asistida, ' \
            'la avanzada ' \
            'edad de la madre o el uso prolongado de pastillas anticonceptivas, entre otros.' \
            'Gemelos monocigóticos Por una razón cuyo origen médico no ha sido aún identificado, en algunos casos, ' \
            'tras la ' \
            'fecundación del óvulo (durante los siguientes 14 días), este sufre una división, dando lugar a dos ' \
            'huevos '

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_2])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}', ' esperada:Bebe')

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
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}', ' esperada:Deporte')

noticia_4 = 'Ingredientes: 75 minutos 5 unidades 1 kg Harina 0000 ' \
            '50 g Levadura Fresca o 13g de Levadura Seca (2cdas. Al ras)' \
            '50 cc. De aceite (8 cucharadas)' \
            '600 cc aprox. Agua tibia' \
            '2 cdas. De Sal (al ras)' \
            '1 cdita. Azúcar' \
            'c/n Salsa o puré de tomates' \
            'Paso 1: En un recipiente colocar la levadura fresca y desmenuzarla un poco o con las manos o ' \
            'directamente ' \
            'la levadura seca, agregarle 4 cucharadas del harina de la receta junto con la cucharadita de azúcar y ' \
            '100cc (1/2 vaso) de agua tibia y mezclar muy bien hasta unir todo (tiene que quedar una consistencia ni ' \
            'muy espesa ni muy líquida) tapar y dejar reposar por unos 10 para activar la levadura.Foto del paso 1 de ' \
            'la receta Masa de pizza fácil y casera.Paso 2:En otro recipiente amplio colocar el harina formando una ' \
            'corona y añadir alrededor la sal (esto es para que no tome contacto directo con la levadura porque la ' \
            '"mata") y en el centro colocar la levadura ya activada y el aceite.' \
            'Foto del paso 2 de la receta Masa de pizza fácil y casera.    ' \
            'Incorporar el agua tibia de a poco e ir uniendo ingredientes desde desde centro hasta lograr una ' \
            'masa chiclosa (se tiene que pegar un poco en las manos) si no te gusta esta textura para trabajarla ' \
            'agrega menos agua (con 450 a 500cc andarás bien. Todo depende como te guste el resultado final de una ' \
            'masa, más compacta o más aireada) Amasar con ganas por unos 20 aprox. Recordá que mientras más amases ' \
            'mejor miga desarrollarás para tu pizza Foto del paso 3 de la receta Masa de pizza fácil y casera Paso 4 ' \
            'Una vez finalizado el amasado formar un bollo y untarlo con un poco de aceite tapar y dejar reposar por ' \
            '40 a 50 minutos. Hasta que triplique su volumen. Foto del paso 4 de la receta Masa de pizza fácil y casera' \
            'Paso 5 Pasado el tiempo de leudado desgasificar la masa (aplastarla con las manos y sacar el gas que ' \
            'produce la levadura) y dividir en 4 bollos (si elegiste hacer la masa más humeda te recomiendo este paso ' \
            'hacerlo untando las manos en aceite para evitar que se te pegotee) Para la cocción: aceitar una pizzera y ' \
            'estirar el bollo de masa desde el centro hacia los bordes y pincelar con salsa o puré de tomates. Llevar ' \
            'a horno fuerte (200 a 250°) por 10. Foto del paso 5 de la receta Masa de pizza fácil y casera Paso 6' \
            'Y listo! Pre-pizzas listas para armar como más te gusten!'

noticia_vectorized = svm_classifier.vectorizer.transform([noticia_4])
prediction = svm_classifier.model.predict(noticia_vectorized)
predicted_category = svm_classifier.label_encoder.inverse_transform(prediction)
print(f'La noticia se clasifica en la categoría: {predicted_category[0]}', ' esperada:Recetas')
generar_nube_palabras()
title_compare('Seguridad Informatica')
