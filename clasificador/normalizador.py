from gensim.models import KeyedVectors
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from unidecode import unidecode
from sentence_transformers import SentenceTransformer, util
from prettytable import PrettyTable
from transformers import BertTokenizer, BertModel
import torch



def resumen_categoria(categoria):
    data = pd.read_csv('data/dataset.csv', delimiter='|')
    data_filtrado = data[data['category'] == categoria]
    columna_texto = data_filtrado['text']
    resumen = ' '.join(columna_texto.astype(str))
    return resumen


def title_category(category):
    data = pd.read_csv('data/dataset.csv', delimiter='|')
    data_filter = data[data['category'] == category]
    titles = []
    for text in data_filter['title']:
        titles.append(text)
    return titles
"""
def title_compare(category):
    model = KeyedVectors.load_word2vec_format('SBW-vectors-300-min5.bin.gz', binary=True)
    titles = title_category(category)
    num_titles = len(titles)
    for i in range(num_titles):
        for j in range(i + 1, num_titles):
            title1 = titles[i]
            title2 = titles[j]
            title1_tokens = title1.split()
            title2_tokens = title2.split()
            title1_tokens = [token for token in title1_tokens if token in model]
            title2_tokens = [token for token in title2_tokens if token in model]
            if not title1_tokens or not title2_tokens:
                continue
            similarity = model.n_similarity(title1_tokens, title2_tokens)
            print(f"Similitud entre '{title1}' y '{title2}': {similarity:.4f}")
"""
def title_compare(category):
    # Cargar modelos
    w2v_model = KeyedVectors.load_word2vec_format('SBW-vectors-300-min5.bin.gz', binary=True)
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Obtener títulos
    titles = title_category(category)
    num_titles = len(titles)

    for i in range(num_titles):
        for j in range(i + 1, num_titles):
            title1 = titles[i]
            title2 = titles[j]

            # Word2Vec
            title1_tokens_w2v = [token for token in title1.split() if token in w2v_model]
            title2_tokens_w2v = [token for token in title2.split() if token in w2v_model]
            if title1_tokens_w2v and title2_tokens_w2v:
                similarity_w2v = w2v_model.n_similarity(title1_tokens_w2v, title2_tokens_w2v)
                print(f"Similitud (Word2Vec) entre '{title1}' y '{title2}': {similarity_w2v:.4f}")

            # BERT
            combined_titles = title1 + " [SEP] " + title2
            tokens_tensor = bert_tokenizer(combined_titles, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                output = bert_model(**tokens_tensor)
            embeddings_bert = output.last_hidden_state.mean(dim=1)
            similarity_bert = torch.nn.functional.cosine_similarity(embeddings_bert[0], embeddings_bert[0], dim=0).item()
            print(f"Similitud (BERT) entre '{title1}' y '{title2}': {similarity_bert:.4f}")


            # SBERT
            embeddings_sbert = sbert_model.encode([title1, title2])
            embeddings_sbert_tensor = torch.tensor(embeddings_sbert)  # Convierte a tensor de PyTorch
            similarity_sbert = torch.nn.functional.cosine_similarity(embeddings_sbert_tensor[0], embeddings_sbert_tensor[1], dim=0).item()
            print(f"Similitud (SBERT) entre '{title1}' y '{title2}': {similarity_sbert:.4f}")





def procesar_texto(categoria):
    texto = resumen_categoria(categoria)
    texto = texto.lower()
    texto = unidecode(texto)
    palabras = word_tokenize(texto)
    stop_words = set(stopwords.words('spanish'))
    palabras_vacias_espanol = ["estan", "aun", "tambien", "vez", "todos", "todas", "asi", "uno", "dos", "gran", "aqui",
                               "min", "mas", "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por",
                               "un", "para",
                               "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o",
                               "fue", "este", "ha", "sí", "porque", "esta", "son", "entre", "está", "cuando", "muy",
                               "sin", "sobre", "ser", "también", "me", "hasta", "hay", "donde", "quien", "desde",
                               "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso",
                               "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo", "otro",
                               "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos",
                               "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis",
                               "tú", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosotros", "vosotras", "os", "mío",
                               "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos",
                               "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros",
                               "vuestras", "esos", "esas", "estoy", "estás", "está", "estamos", "estáis", "están",
                               "esté", "estés", "estemos", "estéis", "estén", "estaré", "estarás", "estará",
                               "estaremos", "estaréis", "estarán", "estaría", "estarías", "estaríamos", "estaríais",
                               "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban", "estuve",
                               "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera",
                               "estuvieras", "estuviéramos", "estuvierais", "estuvieran", "estuviese", "estuvieses",
                               "estuviésemos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados",
                               "estadas", "estad", "he", "has", "ha", "hemos", "habéis", "han", "haya", "hayas",
                               "hayamos", "hayáis", "hayan", "habré", "habrás", "habrá", "habremos", "habréis",
                               "habrán", "habría", "habrías", "habríamos", "habríais", "habrían", "había", "habías",
                               "habíamos", "habíais", "habían", "hube", "hubiste", "hubo", "hubimos", "hubisteis",
                               "hubieron", "hubiera", "hubieras", "hubiéramos", "hubierais", "hubieran", "hubiese",
                               "hubieses", "hubiésemos", "hubieseis", "hubiesen", "habiendo", "habido", "habida",
                               "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas",
                               "seamos", "seáis", "sean", "seré", "serás", "será", "seremos", "seréis", "serán",
                               "sería", "serías", "seríamos", "seríais", "serían", "era", "eras", "éramos", "erais",
                               "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras",
                               "fuéramos", "fuerais", "fueran", "fuese", "fueses", "fuésemos", "fueseis", "fuesen",
                               "tenía", "tenías", "teníamos", "teníais", "tenían", "tuve", "tuviste", "tuvo", "tuvimos",
                               "tuvisteis", "tuvieron", "tuviera", "tuvieras", "tuviéramos", "tuvierais", "tuvieran",
                               "tuviese", "tuvieses", "tuviésemos", "tuvieseis", "tuviesen", "teniendo", "tenido",
                               "tenida", "tenidos", "tenidas", "tened", "me", "te", "se", "nos", "os", "le", "les",
                               "te", "lo", "la", "los", "las", "mi", "tu", "su", "nuestro", "vuestro", "mejor", "peor",
                               "menor", "mayor", "bueno", "malo", "alto", "bajo", "nuevo", "viejo", "primero", "último",
                               "propio", "ajeno", "mismo", "distinto", "cerca", "lejos", "dentro", "fuera", "encima",
                               "debajo", "delante", "detrás", "antes", "después", "ayer", "hoy", "mañana", "siempre",
                               "nunca", "quizás", "acaso", "tal", "cual", "ambos", "cada", "cualquier", "alguno",
                               "ninguno", "otro", "demás", "muchos", "pocos", "varios", "tantos", "más", "menos", "tan",
                               "mucho", "poco", "bastante", "demasiado", "todo", "nada", "algo", "nada", "uno", "otro",
                               "otra", "otros", "otras", "ya", "todavía", "hasta", "incluso", "casi", "como", "pero",
                               "aunque", "porque", "pues", "para", "si", "no", "ni", "o", "y", "aún", "mientras",
                               "cuando", "desde", "donde", "adónde", "cómo", "cuánto", "cual", "cuales", "cuán", "qué",
                               "quien", "quienes", "uno", "una", "unas", "unos", "sí", "no", "nunca", "siempre",
                               "quizás", "tal vez", "a lo mejor", "así", "bien", "mal", "muy", "poco", "más", "menos",
                               "bastante", "demasiado", "también", "sólo", "solo", "incluso", "hasta", "aún", "todavía",
                               "casi", "apenas", "quizás", "acaso", "tan", "así que", "por lo tanto", "en cambio",
                               "sin embargo", "porque", "aunque", "como", "si", "para", "de", "a", "en", "con", "por",
                               "sobre", "durante", "hasta", "antes", "después", "cuando", "mientras", "porque", "si",
                               "pero", "aunque", "sin embargo", "y", "o", "ya", "es", "está", "son", "están", "ser",
                               "estar", "fue", "ha", "había", "hecho", "hizo", "tener", "tener", "tiene", "tuvieron",
                               "hacer", "hace", "hizo", "hicieron", "decir", "dice", "dijo", "dicen", "ir", "fue",
                               "voy", "vamos", "van", "vaya", "vas", "iba", "fuiste", "fueron", "poder", "puede",
                               "pueden", "podemos", "querer", "quiere", "quieres", "quieren", "saber", "sabe", "sabes",
                               "saben", "creer", "cree", "crees", "creen", "parecer", "parece", "pareces", "parecen",
                               "parecía", "parecías", "parecíamos", "parecíais", "parecían", "dar", "doy", "das", "da",
                               "damos", "dais", "dan", "daba", "diste", "dieron", "decir", "digo", "dices", "dice",
                               "decimos", "decís", "dicen", "dije", "dijiste", "dijimos", "dijisteis", "dijeron",
                               "pensar", "pienso", "piensas", "piensa", "pensamos", "pensáis", "piensan", "pensaba",
                               "pensabas", "pensábamos", "pensabais", "pensaban", "encontrar", "encuentro",
                               "encuentras", "encuentra", "encontramos", "encontráis", "encuentran", "encontraba",
                               "encontrabas", "encontrábamos", "encontrabais", "encontraban", "tener", "tengo",
                               "tienes", "tiene", "tenemos", "tenéis", "tienen", "tenía", "tenías", "teníamos",
                               "teníais", "tenían", "haber", "he", "has", "ha", "hemos", "habéis", "han", "había",
                               "habías", "habíamos", "habíais", "habían", "haya", "hayas", "hayamos", "hayáis", "hayan",
                               "habré", "habrás", "habrá", "habremos", "habréis", "habrán", "habría", "habrías",
                               "habríamos", "habríais", "habrían", "había", "habías", "habíamos", "habíais", "habían",
                               "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras",
                               "hubiéramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubiésemos", "hubieseis",
                               "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es",
                               "somos", "sois", "son", "sea", "seas", "seamos", "seáis", "sean", "seré", "serás",
                               "será", "seremos", "seréis", "serán", "sería", "serías", "seríamos", "seríais", "serían",
                               "era", "eras", "éramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis",
                               "fueron", "fuera", "fueras", "fuéramos", "fuerais", "fueran", "fuese", "fueses",
                               "fuésemos", "fueseis", "fuesen", "tenía", "tenías", "teníamos", "teníais", "tenían",
                               "tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron", "tuviera", "tuvieras",
                               "tuviéramos", "tuvierais", "tuvieran", "tuviese", "tuvieses", "tuviésemos", "tuvieseis",
                               "tuviesen", "teniendo", "tenido", "tenida", "tenidos", "tenidas", "tened","ano"]
    stop_words.update(palabras_vacias_espanol)
    palabras = [palabra for palabra in palabras if len(palabra) >= 3 and palabra not in stop_words]
    return palabras, categoria