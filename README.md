# Desafio Atenea - Sistema de Estudio

Sistema de estudio para torneo universitario de cultura general.

## Equipo
- **Santiago** — ciencia, logica, terminologia
- **Marcos** — historia universal, filosofia, arte, mitologia, literatura
- **Tiziano** — geografia, deportes, actualidad, musica
- **Todos** — historia argentina + preguntas faciles

## Setup

Solo necesitas Python 3 (sin dependencias externas).

```bash
git clone git@github.com:santy-tobio/atenea-study.git
cd atenea-study
```

## Uso

```bash
# Quiz interactivo (20 preguntas aleatorias para tu persona)
python3 quiz.py --persona tiziano --aleatorio --n 20
python3 quiz.py --persona marcos --aleatorio --n 20
python3 quiz.py --persona santiago --aleatorio --n 20

# Quiz por categoria
python3 quiz.py --categoria mitologia --aleatorio

# Repasar lo que no sabias
python3 quiz.py --modo debil --persona marcos

# Ver estadisticas
python3 quiz.py --modo stats

# Resumen rapido
python3 quiz.py --modo resumen

# Agregar preguntas nuevas
python3 quiz.py --modo agregar

# Exportar a Anki
python3 quiz.py --modo anki --persona tiziano
```

## Base de datos

669 preguntas en `preguntas.csv` con categorias: geografia, ciencia, historia universal, historia argentina, deportes, musica, terminologia, filosofia, mitologia, literatura, arte, logica, actualidad.

Fuentes: OpenTriviaQA (traducidas), Trivial2b, preguntas generadas, Preguntados UTN.

## Anki

Importar `anki_export.txt` en Anki: File > Import > separador Tab. Tags con jerarquia `atenea::categoria::dificultad`.
