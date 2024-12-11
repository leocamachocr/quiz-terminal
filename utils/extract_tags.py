import json
import os

# Directorio de preguntas
questions_dir = '../resources/questions'

# Inicializar un conjunto para consolidar los tags
tags_set = set()

# Recorrer todos los archivos en el directorio de preguntas
for filename in os.listdir(questions_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(questions_dir, filename)
        # Cargar el archivo JSON
        with open(filepath, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        # Extraer y consolidar los tags
        for question in questions:
            tags_set.update(question.get('tags', []))

# Convertir el set a una lista
tags_list = list(tags_set)

# Guardar la lista de tags en un nuevo archivo JSON
with open('../resources/tags/CCDAK-ayust-tags.json', 'w', encoding='utf-8') as file:
    json.dump(tags_list, file, indent=2, ensure_ascii=False)