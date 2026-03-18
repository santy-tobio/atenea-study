#!/usr/bin/env python3
"""
DESAFÍO ATENEA - Sistema de Estudio para Torneo de Trivia Universitario.

CLI quiz app que trabaja con preguntas en CSV.
Modos: quiz, stats, agregar, debil, anki, resumen.
"""

import argparse
import csv
import os
import random
import sys
from datetime import date

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "preguntas.csv")
ANKI_PATH = os.path.join(BASE_DIR, "anki_export.txt")

# ── CSV schema ───────────────────────────────────────────────────────────────
FIELDNAMES = [
    "id", "pregunta", "respuesta", "categoria", "dificultad",
    "asignado_a", "estado", "notas", "fecha_revision", "fuente",
]

ESTADOS_VALIDOS = {"nueva", "vista", "sabia", "no_sabia", "revisar"}
DIFICULTADES = ["facil", "media", "dificil"]
PERSONAS = ["santiago", "marcos", "tiziano"]

# ── Categorías conocidas (para menú interactivo) ────────────────────────────
CATEGORIAS = [
    "geografia", "historia_argentina", "historia_mundial", "ciencia",
    "deporte", "arte", "musica", "cine_tv", "literatura", "politica",
    "economia", "tecnologia", "naturaleza", "gastronomia", "otro",
]

# ── Reglas de asignación por categoría ───────────────────────────────────────
ASIGNACION_CATEGORIA = {
    "geografia": "santiago",
    "historia_argentina": "marcos",
    "historia_mundial": "marcos",
    "ciencia": "tiziano",
    "deporte": "santiago",
    "arte": "tiziano",
    "musica": "tiziano",
    "cine_tv": "santiago",
    "literatura": "marcos",
    "politica": "marcos",
    "economia": "santiago",
    "tecnologia": "tiziano",
    "naturaleza": "tiziano",
    "gastronomia": "santiago",
    "otro": "todos",
}

# ── ANSI colors ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BG_RED  = "\033[41m"
    BG_GREEN = "\033[42m"


def colored(text, *codes):
    return "".join(codes) + str(text) + C.RESET


# ── CSV helpers ──────────────────────────────────────────────────────────────

def load_csv():
    """Carga preguntas del CSV. Devuelve lista de dicts."""
    if not os.path.exists(CSV_PATH):
        return []
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                # Normalizar keys por si hay espacios
                cleaned = {k.strip(): v.strip() if v else "" for k, v in row.items() if k}
                rows.append(cleaned)
            return rows
    except Exception as e:
        print(colored(f"Error leyendo CSV: {e}", C.RED))
        return []


def save_csv(rows):
    """Guarda lista de dicts al CSV."""
    try:
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        print(colored(f"Error guardando CSV: {e}", C.RED))


def next_id(rows):
    """Devuelve el próximo ID numérico disponible."""
    max_id = 0
    for r in rows:
        try:
            max_id = max(max_id, int(r.get("id", 0)))
        except (ValueError, TypeError):
            pass
    return max_id + 1


# ── Filtros ──────────────────────────────────────────────────────────────────

def filtrar(rows, persona=None, categoria=None, dificultad=None, estado=None):
    """Aplica filtros a la lista de preguntas."""
    resultado = rows
    if persona and persona != "todos":
        resultado = [r for r in resultado if r.get("asignado_a", "").lower() == persona.lower()]
    if categoria:
        resultado = [r for r in resultado if r.get("categoria", "").lower() == categoria.lower()]
    if dificultad:
        resultado = [r for r in resultado if r.get("dificultad", "").lower() == dificultad.lower()]
    if estado:
        resultado = [r for r in resultado if r.get("estado", "").lower() == estado.lower()]
    return resultado


# ── Banner ───────────────────────────────────────────────────────────────────

def banner():
    print()
    print(colored("═" * 55, C.CYAN, C.BOLD))
    print(colored("  \U0001f3db\ufe0f  DESAFÍO ATENEA - Sistema de Estudio", C.CYAN, C.BOLD))
    print(colored("═" * 55, C.CYAN, C.BOLD))
    print()


# ── Mode: QUIZ ───────────────────────────────────────────────────────────────

def modo_quiz(args):
    rows = load_csv()
    if not rows:
        print(colored("No hay preguntas cargadas. Usá --modo agregar para sumar.", C.YELLOW))
        return

    preguntas = filtrar(rows, args.persona, args.categoria, args.dificultad, args.estado)
    if not preguntas:
        print(colored("No se encontraron preguntas con esos filtros.", C.YELLOW))
        return

    if args.aleatorio:
        random.shuffle(preguntas)

    if args.n and args.n > 0:
        preguntas = preguntas[:args.n]

    total = len(preguntas)
    print(colored(f"\U0001f4da {total} preguntas encontradas", C.BLUE, C.BOLD))
    print()

    correctas = 0
    incorrectas = 0
    revisar = 0
    respondidas = 0

    for i, pregunta in enumerate(preguntas):
        cat = pregunta.get("categoria", "?")
        dif = pregunta.get("dificultad", "?")
        texto = pregunta.get("pregunta", "")
        respuesta = pregunta.get("respuesta", "")

        dif_color = {"facil": C.GREEN, "media": C.YELLOW, "dificil": C.RED}.get(dif, C.WHITE)

        print(colored("─" * 55, C.DIM))
        print(f"  {colored(f'[{i+1}/{total}]', C.BOLD)}  {colored(cat, C.CYAN)}  {colored(dif, dif_color)}")
        print()
        print(f"  {colored(texto, C.WHITE, C.BOLD)}")
        print()

        try:
            input(colored("  Presioná Enter para ver la respuesta...", C.DIM))
        except (EOFError, KeyboardInterrupt):
            print()
            break

        print(f"  \u2705 {colored('Respuesta:', C.GREEN, C.BOLD)} {respuesta}")
        if pregunta.get("notas"):
            print(f"  {colored('Nota:', C.DIM)} {pregunta['notas']}")
        if pregunta.get("fuente"):
            print(f"  {colored('Fuente:', C.DIM)} {pregunta['fuente']}")
        print()

        while True:
            try:
                resp = input(colored("  ¿La sabías? (s)í / (n)o / (r)evisar / (q)uit: ", C.MAGENTA)).strip().lower()
            except (EOFError, KeyboardInterrupt):
                resp = "q"
            if resp in ("s", "si", "sí", "y"):
                pregunta["estado"] = "sabia"
                correctas += 1
                respondidas += 1
                break
            elif resp in ("n", "no"):
                pregunta["estado"] = "no_sabia"
                incorrectas += 1
                respondidas += 1
                break
            elif resp in ("r", "revisar"):
                pregunta["estado"] = "revisar"
                revisar += 1
                respondidas += 1
                break
            elif resp in ("q", "quit", "salir"):
                save_csv(rows)
                print()
                _resumen_sesion(respondidas, correctas, incorrectas, revisar)
                return
            else:
                print(colored("  Opción no válida. Usá s/n/r/q.", C.RED))

        pregunta["fecha_revision"] = date.today().isoformat()
        save_csv(rows)
        print()

    print(colored("─" * 55, C.DIM))
    _resumen_sesion(respondidas, correctas, incorrectas, revisar)


def _resumen_sesion(total, correctas, incorrectas, revisar):
    print(colored("\U0001f4ca Resumen de sesión:", C.BOLD))
    print(f"  Total respondidas: {colored(total, C.BOLD)}")
    if total > 0:
        pct = correctas / total * 100
        print(f"  Sabía:    {colored(correctas, C.GREEN, C.BOLD)} ({pct:.0f}%)")
        print(f"  No sabía: {colored(incorrectas, C.RED, C.BOLD)}")
        print(f"  Revisar:  {colored(revisar, C.YELLOW, C.BOLD)}")
    print()


# ── Mode: STATS ──────────────────────────────────────────────────────────────

def modo_stats(args):
    rows = load_csv()
    if not rows:
        print(colored("No hay preguntas cargadas.", C.YELLOW))
        return

    total = len(rows)
    print(colored(f"\U0001f4ca Estadísticas generales ({total} preguntas)", C.BOLD, C.CYAN))
    print(colored("─" * 55, C.DIM))

    # Por estado
    estados = {}
    for r in rows:
        e = r.get("estado", "nueva") or "nueva"
        estados[e] = estados.get(e, 0) + 1

    for e in ["nueva", "sabia", "no_sabia", "revisar", "vista"]:
        cnt = estados.get(e, 0)
        color = {"sabia": C.GREEN, "no_sabia": C.RED, "revisar": C.YELLOW, "nueva": C.BLUE, "vista": C.DIM}.get(e, C.WHITE)
        bar = colored("█" * min(cnt, 40), color)
        print(f"  {e:<12} {cnt:>4}  {bar}")
    print()

    # Por persona
    print(colored("Por persona:", C.BOLD))
    personas_data = {}
    for r in rows:
        p = r.get("asignado_a", "sin_asignar") or "sin_asignar"
        if p not in personas_data:
            personas_data[p] = {"total": 0, "sabia": 0, "no_sabia": 0, "revisar": 0}
        personas_data[p]["total"] += 1
        e = r.get("estado", "")
        if e in personas_data[p]:
            personas_data[p][e] += 1

    for p in sorted(personas_data):
        d = personas_data[p]
        pct = d["sabia"] / d["total"] * 100 if d["total"] > 0 else 0
        pct_color = C.GREEN if pct >= 60 else C.YELLOW if pct >= 30 else C.RED
        print(f"  {p:<15} total: {d['total']:>4}  sabia: {colored(d['sabia'], C.GREEN)}  "
              f"no_sabia: {colored(d['no_sabia'], C.RED)}  revisar: {colored(d['revisar'], C.YELLOW)}  "
              f"dominio: {colored(f'{pct:.0f}%', pct_color)}")
    print()

    # Por categoría
    print(colored("Por categoría:", C.BOLD))
    cat_data = {}
    for r in rows:
        c = r.get("categoria", "otro") or "otro"
        if c not in cat_data:
            cat_data[c] = {"total": 0, "sabia": 0, "no_sabia": 0, "revisar": 0, "nueva": 0}
        cat_data[c]["total"] += 1
        e = r.get("estado", "nueva") or "nueva"
        if e in cat_data[c]:
            cat_data[c][e] += 1

    for c in sorted(cat_data):
        d = cat_data[c]
        pct = d["sabia"] / d["total"] * 100 if d["total"] > 0 else 0
        pct_color = C.GREEN if pct >= 60 else C.YELLOW if pct >= 30 else C.RED
        print(f"  {c:<22} total: {d['total']:>4}  sabia: {colored(d['sabia'], C.GREEN)}  "
              f"no_sabia: {colored(d['no_sabia'], C.RED)}  dominio: {colored(f'{pct:.0f}%', pct_color)}")
    print()

    # Weak areas
    weak = []
    for c, d in cat_data.items():
        answered = d["sabia"] + d["no_sabia"]
        if answered > 0 and d["no_sabia"] / answered > 0.5:
            weak.append((c, d["no_sabia"] / answered * 100))

    if weak:
        print(colored("\u26a0\ufe0f  Áreas débiles (>50% no_sabia):", C.RED, C.BOLD))
        for c, pct in sorted(weak, key=lambda x: -x[1]):
            print(f"  {colored(c, C.RED)}  ({pct:.0f}% incorrectas)")
        print()


# ── Mode: AGREGAR ────────────────────────────────────────────────────────────

def modo_agregar(args):
    rows = load_csv()

    while True:
        print(colored("─" * 55, C.DIM))
        print(colored("Nueva pregunta:", C.BOLD, C.CYAN))
        print()

        try:
            pregunta = input(colored("  Pregunta: ", C.BOLD)).strip()
            if not pregunta:
                print(colored("  Pregunta vacía, cancelando.", C.YELLOW))
                break

            respuesta = input(colored("  Respuesta: ", C.BOLD)).strip()
            if not respuesta:
                print(colored("  Respuesta vacía, cancelando.", C.YELLOW))
                break

            # Categoría
            print(colored("  Categorías disponibles:", C.DIM))
            for i, cat in enumerate(CATEGORIAS):
                print(f"    {i+1:>2}. {cat}")
            cat_input = input(colored(f"  Categoría [default: otro]: ", C.BOLD)).strip().lower()
            if cat_input.isdigit() and 1 <= int(cat_input) <= len(CATEGORIAS):
                categoria = CATEGORIAS[int(cat_input) - 1]
            elif cat_input in CATEGORIAS:
                categoria = cat_input
            elif cat_input == "":
                categoria = "otro"
            else:
                categoria = cat_input  # free-form

            # Dificultad
            dif_input = input(colored("  Dificultad (facil/media/dificil) [default: media]: ", C.BOLD)).strip().lower()
            dificultad = dif_input if dif_input in DIFICULTADES else "media"

            # Asignación automática
            asignado = ASIGNACION_CATEGORIA.get(categoria, "todos")

            # Notas opcionales
            notas = input(colored("  Notas (opcional): ", C.DIM)).strip()

            new_id = next_id(rows)
            nueva = {
                "id": str(new_id),
                "pregunta": pregunta,
                "respuesta": respuesta,
                "categoria": categoria,
                "dificultad": dificultad,
                "asignado_a": asignado,
                "estado": "nueva",
                "notas": notas,
                "fecha_revision": "",
                "fuente": "manual",
            }

            rows.append(nueva)
            save_csv(rows)
            print(colored(f"  \u2705 Pregunta #{new_id} agregada (asignada a: {asignado})", C.GREEN, C.BOLD))
            print()

            otra = input(colored("  ¿Agregar otra? (s/n) [s]: ", C.MAGENTA)).strip().lower()
            if otra in ("n", "no"):
                break

        except (EOFError, KeyboardInterrupt):
            print()
            break

    print(colored(f"\n  Total preguntas en base: {len(rows)}", C.BLUE))
    print()


# ── Mode: WEAK SPOTS (debil) ────────────────────────────────────────────────

def modo_debil(args):
    args.aleatorio = True
    # Filtrar por no_sabia y revisar
    rows = load_csv()
    if not rows:
        print(colored("No hay preguntas cargadas.", C.YELLOW))
        return

    preguntas_debiles = [
        r for r in rows
        if r.get("estado", "").lower() in ("no_sabia", "revisar")
    ]

    # Apply additional filters
    preguntas_debiles = filtrar(
        preguntas_debiles, args.persona, args.categoria, args.dificultad, estado=None
    )

    if not preguntas_debiles:
        print(colored("\U0001f389 No hay preguntas débiles. ¡Buen trabajo!", C.GREEN, C.BOLD))
        return

    # We need to run quiz on these but keep reference to original rows for saving.
    # Build a set of IDs for the weak questions
    weak_ids = {r.get("id") for r in preguntas_debiles}

    # Shuffle
    random.shuffle(preguntas_debiles)

    if args.n and args.n > 0:
        preguntas_debiles = preguntas_debiles[:args.n]

    total = len(preguntas_debiles)
    print(colored(f"\U0001f4aa Modo repaso: {total} preguntas débiles", C.RED, C.BOLD))
    print()

    correctas = 0
    incorrectas = 0
    revisar_cnt = 0
    respondidas = 0

    for i, pregunta in enumerate(preguntas_debiles):
        cat = pregunta.get("categoria", "?")
        dif = pregunta.get("dificultad", "?")
        texto = pregunta.get("pregunta", "")
        respuesta = pregunta.get("respuesta", "")
        estado_prev = pregunta.get("estado", "")

        dif_color = {"facil": C.GREEN, "media": C.YELLOW, "dificil": C.RED}.get(dif, C.WHITE)
        estado_color = {"no_sabia": C.RED, "revisar": C.YELLOW}.get(estado_prev, C.WHITE)

        print(colored("─" * 55, C.DIM))
        print(f"  {colored(f'[{i+1}/{total}]', C.BOLD)}  {colored(cat, C.CYAN)}  "
              f"{colored(dif, dif_color)}  {colored(f'({estado_prev})', estado_color)}")
        print()
        print(f"  {colored(texto, C.WHITE, C.BOLD)}")
        print()

        try:
            input(colored("  Presioná Enter para ver la respuesta...", C.DIM))
        except (EOFError, KeyboardInterrupt):
            print()
            break

        print(f"  \u2705 {colored('Respuesta:', C.GREEN, C.BOLD)} {respuesta}")
        print()

        while True:
            try:
                resp = input(colored("  ¿La sabías? (s)í / (n)o / (r)evisar / (q)uit: ", C.MAGENTA)).strip().lower()
            except (EOFError, KeyboardInterrupt):
                resp = "q"
            if resp in ("s", "si", "sí", "y"):
                pregunta["estado"] = "sabia"
                correctas += 1
                respondidas += 1
                break
            elif resp in ("n", "no"):
                pregunta["estado"] = "no_sabia"
                incorrectas += 1
                respondidas += 1
                break
            elif resp in ("r", "revisar"):
                pregunta["estado"] = "revisar"
                revisar_cnt += 1
                respondidas += 1
                break
            elif resp in ("q", "quit", "salir"):
                save_csv(rows)
                print()
                _resumen_sesion(respondidas, correctas, incorrectas, revisar_cnt)
                return
            else:
                print(colored("  Opción no válida. Usá s/n/r/q.", C.RED))

        pregunta["fecha_revision"] = date.today().isoformat()
        save_csv(rows)
        print()

    print(colored("─" * 55, C.DIM))
    _resumen_sesion(respondidas, correctas, incorrectas, revisar_cnt)


# ── Mode: ANKI EXPORT ────────────────────────────────────────────────────────

def modo_anki(args):
    rows = load_csv()
    if not rows:
        print(colored("No hay preguntas cargadas.", C.YELLOW))
        return

    preguntas = rows
    if args.persona and args.persona != "todos":
        preguntas = [r for r in preguntas if r.get("asignado_a", "").lower() == args.persona.lower()]

    if not preguntas:
        print(colored("No se encontraron preguntas con esos filtros.", C.YELLOW))
        return

    try:
        with open(ANKI_PATH, "w", encoding="utf-8") as f:
            for r in preguntas:
                pregunta = r.get("pregunta", "").replace("\t", " ").replace("\n", " ")
                respuesta = r.get("respuesta", "").replace("\t", " ").replace("\n", " ")
                cat = r.get("categoria", "otro") or "otro"
                dif = r.get("dificultad", "media") or "media"
                tags = f"atenea::{cat}::{dif}"
                f.write(f"{pregunta}\t{respuesta}\t{tags}\n")

        print(colored(f"\u2705 Exportadas {len(preguntas)} preguntas a:", C.GREEN, C.BOLD))
        print(f"  {ANKI_PATH}")
        print(colored("  Formato: pregunta<TAB>respuesta<TAB>tags", C.DIM))
        print()
    except Exception as e:
        print(colored(f"Error exportando: {e}", C.RED))


# ── Mode: RESUMEN ────────────────────────────────────────────────────────────

def modo_resumen(args):
    rows = load_csv()
    if not rows:
        print(colored("No hay preguntas cargadas.", C.YELLOW))
        return

    cat_data = {}
    for r in rows:
        c = r.get("categoria", "otro") or "otro"
        if c not in cat_data:
            cat_data[c] = {"total": 0, "sabia": 0, "no_sabia": 0, "revisar": 0, "nueva": 0}
        cat_data[c]["total"] += 1
        e = r.get("estado", "nueva") or "nueva"
        if e in cat_data[c]:
            cat_data[c][e] += 1

    # Header
    header = f"{'Categoría':<22} {'Total':>5} {'Sabía':>6} {'NoSab':>6} {'Revis':>6} {'Nueva':>6} {'%Dom':>6}"
    print(colored(header, C.BOLD))
    print(colored("─" * len(header), C.DIM))

    total_all = {"total": 0, "sabia": 0, "no_sabia": 0, "revisar": 0, "nueva": 0}

    for c in sorted(cat_data):
        d = cat_data[c]
        pct = d["sabia"] / d["total"] * 100 if d["total"] > 0 else 0
        pct_color = C.GREEN if pct >= 60 else C.YELLOW if pct >= 30 else C.RED

        # Color the whole line based on dominio
        print(f"  {c:<20} {d['total']:>5} {colored(d['sabia'], C.GREEN):>15} "
              f"{colored(d['no_sabia'], C.RED):>15} {colored(d['revisar'], C.YELLOW):>15} "
              f"{colored(d['nueva'], C.BLUE):>15} {colored(f'{pct:.0f}%', pct_color):>15}")

        for k in total_all:
            total_all[k] += d[k]

    print(colored("─" * len(header), C.DIM))
    pct_all = total_all["sabia"] / total_all["total"] * 100 if total_all["total"] > 0 else 0
    pct_color = C.GREEN if pct_all >= 60 else C.YELLOW if pct_all >= 30 else C.RED
    print(f"  {'TOTAL':<20} {total_all['total']:>5} {colored(total_all['sabia'], C.GREEN):>15} "
          f"{colored(total_all['no_sabia'], C.RED):>15} {colored(total_all['revisar'], C.YELLOW):>15} "
          f"{colored(total_all['nueva'], C.BLUE):>15} {colored(f'{pct_all:.0f}%', pct_color):>15}")
    print()


# ── CLI argument parser ──────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="\U0001f3db\ufe0f DESAFÍO ATENEA - Sistema de Estudio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--modo", "-m",
        choices=["quiz", "stats", "agregar", "debil", "anki", "resumen"],
        default="quiz",
        help="Modo de operación (default: quiz)",
    )
    parser.add_argument(
        "--agregar", action="store_true",
        help="Atajo para --modo agregar",
    )
    parser.add_argument(
        "--persona", "-p",
        help="Filtrar por persona (santiago/marcos/tiziano/todos)",
    )
    parser.add_argument(
        "--categoria", "-c",
        help="Filtrar por categoría",
    )
    parser.add_argument(
        "--dificultad", "-d",
        choices=DIFICULTADES,
        help="Filtrar por dificultad",
    )
    parser.add_argument(
        "--estado", "-e",
        choices=list(ESTADOS_VALIDOS),
        help="Filtrar por estado",
    )
    parser.add_argument(
        "--aleatorio", "-a",
        action="store_true",
        help="Orden aleatorio (default en modo debil)",
    )
    parser.add_argument(
        "--n", type=int, default=0,
        help="Limitar a N preguntas por sesión",
    )

    return parser


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Shortcut: --agregar
    if args.agregar:
        args.modo = "agregar"

    banner()

    dispatch = {
        "quiz": modo_quiz,
        "stats": modo_stats,
        "agregar": modo_agregar,
        "debil": modo_debil,
        "anki": modo_anki,
        "resumen": modo_resumen,
    }

    handler = dispatch.get(args.modo, modo_quiz)
    try:
        handler(args)
    except KeyboardInterrupt:
        print(colored("\n\nSesión interrumpida.", C.YELLOW))
        sys.exit(0)


if __name__ == "__main__":
    main()
