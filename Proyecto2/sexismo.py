import numpy as np
import pandas as pd

sexismo_phrases = [

]

# Crear un DataFrame con las frases simuladas y sus etiquetas
df_sexismo = pd.DataFrame({
    'text': np.random.choice(sexismo_phrases, 1000),
    'label': 'sexismo'
})

# Guardar el DataFrame en un archivo CSV
df_sexismo.to_csv('sexismo_data.csv', index=False)
