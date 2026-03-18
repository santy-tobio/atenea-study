# Desafio Atenea - Sistema de Estudio

Sistema de estudio con 669 preguntas de cultura general para preparar el torneo universitario Desafio Atenea.

## Equipo

| Persona | Categorias asignadas |
|---------|---------------------|
| **Santiago** | ciencia, logica, terminologia |
| **Marcos** | historia universal, filosofia, arte, mitologia, literatura |
| **Tiziano** | geografia, deportes, actualidad, musica |
| **Todos** | historia argentina + todas las preguntas faciles |

## Instalacion

Solo necesitas **Python 3** (sin dependencias externas).

```bash
git clone https://github.com/santy-tobio/atenea-study.git
cd atenea-study
```

## Como se usa

### Quiz interactivo (modo principal)

```bash
python3 quiz.py
```

Te muestra una pregunta, apretas **Enter** para ver la respuesta, y contestas:
- `s` — la sabia
- `n` — no la sabia
- `r` — marcar para revisar despues
- `q` — salir

Tu progreso queda guardado automaticamente en `preguntas.csv`.

### Filtros

Podes combinar cualquiera de estos filtros:

```bash
# Filtrar por persona
python3 quiz.py --persona tiziano
python3 quiz.py --persona marcos
python3 quiz.py --persona santiago

# Filtrar por categoria
python3 quiz.py --categoria mitologia
python3 quiz.py --categoria historia_argentina

# Filtrar por dificultad
python3 quiz.py --dificultad dificil

# Filtrar por estado (solo las que no sabias, o las nuevas, etc.)
python3 quiz.py --estado nueva
python3 quiz.py --estado no_sabia

# Orden aleatorio
python3 quiz.py --aleatorio

# Limitar cantidad de preguntas
python3 quiz.py --n 20

# Combinar todo
python3 quiz.py --persona marcos --categoria filosofia --aleatorio --n 10
```

### Modos

El sistema tiene 6 modos:

#### `quiz` (default) — Estudiar con preguntas

```bash
python3 quiz.py
python3 quiz.py --persona santiago --aleatorio --n 20
```

#### `debil` — Repasar puntos debiles

Muestra solo las preguntas que marcaste como "no sabia" o "revisar". Viene en orden aleatorio por default.

```bash
python3 quiz.py --modo debil
python3 quiz.py --modo debil --persona tiziano
```

#### `stats` — Estadisticas detalladas

Muestra porcentaje de aciertos por persona, por categoria, y resalta las areas debiles.

```bash
python3 quiz.py --modo stats
```

#### `resumen` — Tabla rapida por categoria

Una tabla con total/sabia/no_sabia/revisar/nueva y % de dominio por categoria.

```bash
python3 quiz.py --modo resumen
```

#### `agregar` — Agregar preguntas nuevas

Para meter preguntas que aparecen en la vida diaria o que se nos ocurren.

```bash
python3 quiz.py --modo agregar
```

Te pide pregunta, respuesta, categoria y dificultad. Se asigna automaticamente segun la categoria.

#### `anki` — Exportar a Anki

Genera `anki_export.txt` para importar como flashcards en Anki (celular/desktop).

```bash
python3 quiz.py --modo anki
python3 quiz.py --modo anki --persona marcos
```

Para importar en Anki: **File > Import** > seleccionar `anki_export.txt` > separador: **Tab**. Los tags se aplican con jerarquia `atenea::categoria::dificultad`.

## Rutina de estudio sugerida

```bash
# Sesion diaria: 20 preguntas nuevas aleatorias de tu area
python3 quiz.py --persona santiago --estado nueva --aleatorio --n 20

# Antes de dormir: repasar lo que no sabias
python3 quiz.py --modo debil --persona santiago

# Fin de semana: sesion grupal con todas las categorias
python3 quiz.py --aleatorio --n 50

# Cada tanto: ver como vamos
python3 quiz.py --modo resumen
```

## Sincronizar progreso

Cada uno tiene su progreso local en `preguntas.csv`. Para compartir preguntas nuevas que agreguen:

```bash
git add preguntas.csv
git commit -m "Agrego preguntas nuevas"
git push
```

Los demas hacen `git pull` para recibir las nuevas preguntas.

> **Nota:** si dos personas editan el CSV al mismo tiempo va a haber conflictos de merge. Lo mas simple es que cada uno agregue preguntas en su branch y despues mergeen, o que se turnen para pushear.

## Base de datos

669 preguntas distribuidas en 12 categorias:

| Categoria | Cantidad |
|-----------|----------|
| geografia | 157 |
| ciencia | 134 |
| historia_universal | 93 |
| otro | 60 |
| deportes | 43 |
| historia_argentina | 41 |
| musica | 31 |
| terminologia | 30 |
| filosofia | 25 |
| mitologia | 25 |
| literatura | 20 |
| arte | 10 |

Fuentes: OpenTriviaQA (traducidas), Trivial2b, preguntas generadas, Preguntados UTN.

## Opciones del CLI

```
--modo, -m      quiz | stats | agregar | debil | anki | resumen
--persona, -p   santiago | marcos | tiziano | todos
--categoria, -c geografia | historia_argentina | historia_universal | ciencia |
                filosofia | arte | mitologia | literatura | deportes | musica |
                terminologia | logica | actualidad | otro
--dificultad, -d facil | media | dificil
--estado, -e    nueva | vista | sabia | no_sabia | revisar
--aleatorio, -a Orden aleatorio
--n N           Limitar a N preguntas
--agregar       Atajo para --modo agregar
```
