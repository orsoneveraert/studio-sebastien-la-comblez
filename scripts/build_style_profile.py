#!/usr/bin/env python3
"""Build a lexical style profile from the L'art même PDF corpus."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


WORD_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿŒœÆæÇç]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿŒœÆæÇç]+)*"
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+")
EMAIL_RE = re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")

STOPWORDS = {
    "a",
    "afin",
    "ah",
    "ai",
    "aie",
    "aient",
    "aies",
    "ait",
    "alors",
    "au",
    "aucun",
    "aucune",
    "aura",
    "aurait",
    "auras",
    "aurez",
    "auriez",
    "aurions",
    "aurons",
    "auront",
    "aussi",
    "autre",
    "autres",
    "aux",
    "avait",
    "avec",
    "avez",
    "aviez",
    "avions",
    "avoir",
    "avons",
    "ayant",
    "ayez",
    "ayons",
    "bien",
    "bon",
    "car",
    "ce",
    "ceci",
    "cela",
    "celle",
    "celles",
    "celui",
    "cependant",
    "certain",
    "certaine",
    "certains",
    "ces",
    "cet",
    "cette",
    "ceux",
    "chaque",
    "ci",
    "comme",
    "comment",
    "contre",
    "d",
    "da",
    "dans",
    "de",
    "debout",
    "dedans",
    "dehors",
    "delà",
    "depuis",
    "derrière",
    "des",
    "dès",
    "dessous",
    "dessus",
    "deux",
    "devant",
    "doit",
    "donc",
    "dos",
    "droite",
    "du",
    "durant",
    "e",
    "elle",
    "elles",
    "en",
    "encore",
    "entre",
    "envers",
    "es",
    "est",
    "et",
    "etaient",
    "étaient",
    "était",
    "etant",
    "étant",
    "etc",
    "été",
    "etre",
    "être",
    "eu",
    "eux",
    "fait",
    "faites",
    "fois",
    "font",
    "hors",
    "ici",
    "il",
    "ils",
    "j",
    "jamais",
    "je",
    "jusqu",
    "jusque",
    "l",
    "la",
    "le",
    "les",
    "leur",
    "leurs",
    "lors",
    "lui",
    "m",
    "ma",
    "mais",
    "me",
    "même",
    "mes",
    "moi",
    "moins",
    "mon",
    "ne",
    "ni",
    "non",
    "nos",
    "notre",
    "nous",
    "nouvelles",
    "nul",
    "on",
    "ont",
    "ou",
    "où",
    "par",
    "parce",
    "pas",
    "pendant",
    "peu",
    "peut",
    "peuvent",
    "plus",
    "pour",
    "pourquoi",
    "qu",
    "quand",
    "que",
    "quel",
    "quelle",
    "quelles",
    "quels",
    "qui",
    "quoi",
    "sa",
    "sans",
    "se",
    "sera",
    "serai",
    "seraient",
    "serais",
    "serait",
    "seras",
    "serez",
    "seriez",
    "serions",
    "serons",
    "seront",
    "ses",
    "seulement",
    "si",
    "sien",
    "son",
    "sont",
    "sous",
    "soyez",
    "suis",
    "sur",
    "ta",
    "tandis",
    "te",
    "tel",
    "telle",
    "telles",
    "tels",
    "tes",
    "toi",
    "ton",
    "tous",
    "tout",
    "toute",
    "toutes",
    "tu",
    "un",
    "une",
    "vos",
    "votre",
    "vous",
    "y",
    "dont",
    "ainsi",
    "très",
    "the",
    "of",
    "in",
    "and",
}

CONNECTEURS = [
    "ainsi",
    "cependant",
    "en effet",
    "en revanche",
    "par ailleurs",
    "dès lors",
    "notamment",
    "voire",
    "or",
    "néanmoins",
    "de fait",
    "autrement dit",
    "en somme",
    "au contraire",
]

NOISE_SUBSTRINGS = [
    "rédactrice en chef",
    "suivi de production",
    "éditeur responsable",
    "éditrice responsable",
    "secrétaire de rédaction",
    "conseil de rédaction",
    "ont collaboré",
    "pour nous informer",
    "toute reproduction des textes",
    "la production et la diffusion de cette revue",
    "la revue l’art même est produite",
    "la revue l'art même est produite",
    "direction générale de la culture",
    "responsable des manuscrits",
    "documents non sollicités",
    "photo ©",
    "courtesy",
]

APOSTROPHE_PREFIXES = ("d'", "l'", "c'", "j'", "n'", "s'", "t'", "m'", "qu'")
NOISE_TOKENS = {
    "www",
    "http",
    "https",
    "be",
    "org",
    "com",
    "net",
    "pdf",
    "cm",
    "mm",
    "isbn",
    "issn",
    "op",
    "cit",
}
LEXICON_EXCLUDE = {
    "faire",
    "voir",
    "tant",
    "autant",
    "toujours",
    "aujourd'hui",
    "avant",
    "ans",
    "soit",
    "là",
    "jusqu'au",
    "question",
    "manière",
    "temps",
    "part",
    "place",
    "point",
    "vue",
    "titre",
    "prix",
    "édition",
    "trois",
    "première",
    "premier",
    "également",
    "bruxelles",
    "paris",
    "new",
    "york",
    "vit",
    "travaille",
}
NGRAM_EXCLUDE = LEXICON_EXCLUDE | {
    "communauté",
    "française",
    "fédération",
    "wallonie-bruxelles",
    "boulevard",
    "léopold",
    "université",
    "libre",
}


@dataclass
class DocStats:
    issue: str
    pdf: str
    txt: str
    words: int
    content_words: int
    sentences: int
    avg_sentence_len: float
    chars: int


def issue_sort_key(pdf_path: Path) -> tuple[int, str]:
    match = re.search(r"ART-MEME-(.+)$", pdf_path.stem, flags=re.IGNORECASE)
    if not match:
        return (9999, pdf_path.stem)
    suffix = match.group(1)
    if suffix == "1_":
        return (1, suffix)
    number_match = re.match(r"(\d+)", suffix)
    if number_match:
        return (int(number_match.group(1)), suffix)
    return (9999, suffix)


def run_extract(pdf_path: Path, txt_path: Path) -> None:
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    pdftotext_cmd = [
        "pdftotext",
        "-enc",
        "UTF-8",
        "-nopgbrk",
        str(pdf_path),
        str(txt_path),
    ]
    first = subprocess.run(pdftotext_cmd, capture_output=True, text=True)
    if first.returncode == 0 and txt_path.exists() and txt_path.stat().st_size > 0:
        return

    mutool_cmd = [
        "mutool",
        "draw",
        "-F",
        "txt",
        "-o",
        str(txt_path),
        str(pdf_path),
    ]
    second = subprocess.run(mutool_cmd, capture_output=True, text=True)
    if second.returncode != 0 or not txt_path.exists() or txt_path.stat().st_size == 0:
        raise RuntimeError(
            f"Extraction failed for {pdf_path.name}: "
            f"pdftotext={first.returncode}, mutool={second.returncode}"
        )


def is_noise_line(line: str) -> bool:
    low = line.lower()

    if not line.strip():
        return True
    if "\x0c" in line:
        return True
    if "www." in low or "http://" in low or "https://" in low:
        return True
    if "©" in line:
        return True
    if "@" in line or EMAIL_RE.search(low):
        return True
    if any(fragment in low for fragment in NOISE_SUBSTRINGS):
        return True
    if re.fullmatch(r"[-–—]?\s*\d{1,4}\s*[-–—]?", line):
        return True
    if re.fullmatch(r"[mM]?\s*\d+\s*/\s*\d+", line):
        return True
    if re.fullmatch(r"[\d\s./-]{1,20}", line):
        return True

    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿŒœÆæÇç]+", line)
    if words:
        uppercase_words = sum(1 for word in words if word.isupper())
        if len(words) <= 8 and uppercase_words / len(words) >= 0.8:
            return True
    return False


def clean_text(raw: str) -> str:
    text = raw.replace("\r", "\n").replace("\u00ad", "")
    text = text.replace("\x0c", "\n")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)

    kept_lines: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if is_noise_line(line):
            continue
        low = line.lower()
        if re.fullmatch(r"l[’']art\s+même", low):
            continue
        kept_lines.append(line)

    flat = " ".join(kept_lines)
    flat = re.sub(r"\s+", " ", flat)
    return flat.strip()


def tokenize(text: str) -> list[str]:
    tokens = []
    for token in WORD_RE.findall(text.lower()):
        token = token.replace("’", "'").strip("'-")
        for prefix in APOSTROPHE_PREFIXES:
            if token.startswith(prefix) and len(token) > len(prefix) + 1:
                token = token[len(prefix) :]
                break
        token = token.strip("'-")
        if len(token) < 2:
            continue
        if re.search(r"\d", token):
            continue
        if token in NOISE_TOKENS:
            continue
        tokens.append(token)
    return tokens


def count_connecteurs(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    lowered = text.lower()
    for phrase in CONNECTEURS:
        pattern = r"\b" + re.escape(phrase).replace(r"\ ", r"\s+") + r"\b"
        counts[phrase] = len(re.findall(pattern, lowered))
    return counts


def sentence_lengths(text: str) -> list[int]:
    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    lengths: list[int] = []
    for sentence in sentences:
        token_count = len(tokenize(sentence))
        if token_count:
            lengths.append(token_count)
    return lengths


def percentile(values: list[int], p: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = (len(sorted_vals) - 1) * p
    lower = int(idx)
    upper = min(lower + 1, len(sorted_vals) - 1)
    if lower == upper:
        return float(sorted_vals[lower])
    weight = idx - lower
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight


def top_counter(counter: Counter, n: int) -> list[dict[str, int]]:
    return [{"token": k, "count": v} for k, v in counter.most_common(n)]


def build_style_guide(profile: dict) -> str:
    top_content_words = ", ".join(
        item["token"] for item in profile["top_content_words"][:25]
    )
    top_bigrams = ", ".join(
        " ".join(item["ngram"]) for item in profile["top_content_bigrams"][:20]
    )
    connecteurs = ", ".join(
        f"{item['phrase']} ({item['count']})"
        for item in profile["top_connecteurs"]
        if item["count"] > 0
    )

    sentence = profile["sentence_length"]
    punct = profile["punctuation_per_1000_words"]

    lines = [
        "# Profil lexical - L'art même",
        "",
        "## Ce qui caractérise le lexique",
        f"- Vocabulaire dominant (hors mots-outils): {top_content_words}",
        f"- Collocations fortes (bigrams): {top_bigrams}",
        f"- Connecteurs argumentatifs récurrents: {connecteurs or 'faible présence structurée'}",
        "",
        "## Rythme syntaxique observé",
        f"- Longueur moyenne de phrase: {sentence['mean']} mots",
        f"- Médiane: {sentence['median']} mots",
        f"- Zone centrale (P25-P75): {sentence['p25']} à {sentence['p75']} mots",
        f"- Phrase courte typique: <= {sentence['p10']} mots",
        f"- Phrase longue typique: >= {sentence['p90']} mots",
        "",
        "## Ponctuation (pour 1000 mots)",
        f"- Virgule: {punct.get(',', 0)}",
        f"- Point: {punct.get('.', 0)}",
        f"- Point-virgule: {punct.get(';', 0)}",
        f"- Deux-points: {punct.get(':', 0)}",
        f"- Point d'interrogation: {punct.get('?', 0)}",
        f"- Point d'exclamation: {punct.get('!', 0)}",
        "",
        "## Règles d'adaptation à appliquer",
        "- Employer un registre critique-descriptif: analyser l'oeuvre avant de juger.",
        "- Favoriser les noms abstraits et les verbes d'observation (inscrire, déplacer, interroger, articuler, révéler).",
        "- Construire des phrases denses mais lisibles: alterner phrases moyennes et phrases longues.",
        "- Utiliser des connecteurs logiques pour relier perception, contexte, enjeu.",
        "- Garder un ton analytique sobre, éviter le marketing et les tournures promotionnelles.",
        "- Conserver une densité lexicale élevée: peu de répétitions exactes, privilégier variantes proches.",
        "",
        "## Mode opératoire quand tu me donnes un texte",
        "1. Je détecte le niveau de langue et le sujet d'origine.",
        "2. Je remplace progressivement le vocabulaire par le lexique dominant du corpus.",
        "3. Je réécris la syntaxe pour se rapprocher du rythme de phrase observé.",
        "4. Je vérifie la proximité lexicale (mots-clés + collocations) tout en gardant ton sens initial.",
    ]
    return "\n".join(lines) + "\n"


def build_prompt_template(profile: dict) -> str:
    lexeme_bank = ", ".join(item["token"] for item in profile["top_content_words"][:80])
    connector_bank = ", ".join(item["phrase"] for item in profile["top_connecteurs"][:12])
    return (
        "# Template de réécriture vers le style L'art même\n\n"
        "## Consigne\n"
        "Réécris le texte fourni en conservant le fond, mais en maximisant la proximité "
        "lexicale avec le corpus de L'art même.\n\n"
        "## Contraintes\n"
        "- Registre: critique artistique analytique.\n"
        "- Ne pas inventer de faits absents du texte source.\n"
        "- Conserver la structure argumentative globale.\n"
        "- Employer préférentiellement les lexèmes de la banque ci-dessous.\n"
        "- Intégrer des connecteurs logiques du corpus.\n\n"
        "## Banque lexicale prioritaire\n"
        f"{lexeme_bank}\n\n"
        "## Connecteurs recommandés\n"
        f"{connector_bank}\n\n"
        "## Format de sortie attendu\n"
        "1. Version réécrite\n"
        "2. Mini-audit de proximité lexicale (10 mots-clés alignés)\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root",
    )
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Force re-extraction even when .txt files already exist",
    )
    parser.add_argument(
        "--min-words-per-doc",
        type=int,
        default=500,
        help="Ignore documents with fewer cleaned words than this threshold",
    )
    args = parser.parse_args()

    root = args.root
    pdf_dir = root / "data" / "art-meme-pdfs"
    txt_dir = root / "analysis" / "texts"
    results_dir = root / "analysis" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    txt_dir.mkdir(parents=True, exist_ok=True)

    pdf_paths = sorted(pdf_dir.glob("*.pdf"), key=issue_sort_key)
    if not pdf_paths:
        raise SystemExit(f"No PDFs found in {pdf_dir}")

    doc_stats: list[DocStats] = []
    all_tokens: list[str] = []
    all_content_tokens: list[str] = []
    corpus_chunks: list[str] = []
    all_sentence_lengths: list[int] = []
    punctuation_counter: Counter[str] = Counter()
    connecteur_counter: Counter[str] = Counter()
    content_bigrams: Counter[tuple[str, str]] = Counter()
    content_trigrams: Counter[tuple[str, str, str]] = Counter()
    excluded_docs: list[dict[str, str | int]] = []

    for pdf_path in pdf_paths:
        txt_path = txt_dir / f"{pdf_path.stem}.txt"
        if args.force_extract or not txt_path.exists() or txt_path.stat().st_size == 0:
            run_extract(pdf_path, txt_path)

        raw_text = txt_path.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_text(raw_text)
        corpus_chunks.append(cleaned)

        tokens = tokenize(cleaned)
        content_tokens = [t for t in tokens if t not in STOPWORDS]
        sent_lengths = sentence_lengths(cleaned)

        if len(tokens) < args.min_words_per_doc:
            excluded_docs.append(
                {
                    "issue": pdf_path.stem.replace("ART-MEME-", ""),
                    "pdf": str(pdf_path),
                    "words": len(tokens),
                }
            )
            continue

        all_tokens.extend(tokens)
        all_content_tokens.extend(content_tokens)
        all_sentence_lengths.extend(sent_lengths)
        connecteur_counter.update(count_connecteurs(cleaned))

        punctuation_counter.update(ch for ch in cleaned if ch in ",.;:!?")

        for i in range(len(content_tokens) - 1):
            content_bigrams[(content_tokens[i], content_tokens[i + 1])] += 1
        for i in range(len(content_tokens) - 2):
            content_trigrams[
                (content_tokens[i], content_tokens[i + 1], content_tokens[i + 2])
            ] += 1

        mean_len = round(sum(sent_lengths) / len(sent_lengths), 2) if sent_lengths else 0.0
        doc_stats.append(
            DocStats(
                issue=pdf_path.stem.replace("ART-MEME-", ""),
                pdf=str(pdf_path),
                txt=str(txt_path),
                words=len(tokens),
                content_words=len(content_tokens),
                sentences=len(sent_lengths),
                avg_sentence_len=mean_len,
                chars=len(cleaned),
            )
        )

    content_counter = Counter(all_content_tokens)
    filtered_content_counter = Counter(
        {
            token: count
            for token, count in content_counter.items()
            if token not in LEXICON_EXCLUDE and len(token) >= 3
        }
    )
    raw_counter = Counter(all_tokens)
    total_words = len(all_tokens)
    unique_words = len(set(all_tokens))
    hapax = sum(1 for _, c in raw_counter.items() if c == 1)

    p25 = round(percentile(all_sentence_lengths, 0.25), 2)
    p75 = round(percentile(all_sentence_lengths, 0.75), 2)
    p10 = round(percentile(all_sentence_lengths, 0.10), 2)
    p90 = round(percentile(all_sentence_lengths, 0.90), 2)
    mean_sentence = (
        round(sum(all_sentence_lengths) / len(all_sentence_lengths), 2)
        if all_sentence_lengths
        else 0.0
    )
    median_sentence = round(statistics.median(all_sentence_lengths), 2) if all_sentence_lengths else 0.0

    punctuation_per_1000 = {
        char: round((count / total_words) * 1000, 2)
        for char, count in punctuation_counter.items()
    }

    top_bigrams = [
        {"ngram": [a, b], "count": count}
        for (a, b), count in content_bigrams.most_common(800)
        if count >= 8 and a not in NGRAM_EXCLUDE and b not in NGRAM_EXCLUDE
    ][:80]
    top_trigrams = [
        {"ngram": [a, b, c], "count": count}
        for (a, b, c), count in content_trigrams.most_common(1000)
        if count >= 5 and a not in NGRAM_EXCLUDE and b not in NGRAM_EXCLUDE and c not in NGRAM_EXCLUDE
    ][:80]

    style_profile = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "corpus": {
            "pdf_count": len(pdf_paths),
            "document_count_used": len(doc_stats),
            "document_count_excluded": len(excluded_docs),
            "total_words": total_words,
            "unique_words": unique_words,
            "lexical_richness_ttr": round(unique_words / total_words, 4) if total_words else 0.0,
            "hapax_count": hapax,
            "hapax_ratio": round(hapax / unique_words, 4) if unique_words else 0.0,
        },
        "sentence_length": {
            "mean": mean_sentence,
            "median": median_sentence,
            "p10": p10,
            "p25": p25,
            "p75": p75,
            "p90": p90,
        },
        "punctuation_per_1000_words": punctuation_per_1000,
        "top_content_words": top_counter(filtered_content_counter, 300),
        "top_words_including_stopwords": top_counter(raw_counter, 120),
        "top_content_bigrams": top_bigrams,
        "top_content_trigrams": top_trigrams,
        "top_connecteurs": [
            {"phrase": k, "count": v} for k, v in connecteur_counter.most_common()
        ],
        "documents": [doc.__dict__ for doc in doc_stats],
        "excluded_documents": excluded_docs,
    }

    corpus_text = "\n".join(corpus_chunks)
    (results_dir / "corpus_clean.txt").write_text(corpus_text, encoding="utf-8")
    (results_dir / "style_profile.json").write_text(
        json.dumps(style_profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lexicon_lines = ["token\tcount\tper_million"]
    for token, count in filtered_content_counter.most_common(800):
        per_million = round((count / total_words) * 1_000_000, 2) if total_words else 0.0
        lexicon_lines.append(f"{token}\t{count}\t{per_million}")
    (results_dir / "lexicon_top_800.tsv").write_text(
        "\n".join(lexicon_lines) + "\n",
        encoding="utf-8",
    )

    style_guide = build_style_guide(style_profile)
    (results_dir / "style_guide.md").write_text(style_guide, encoding="utf-8")

    prompt_template = build_prompt_template(style_profile)
    (results_dir / "rewrite_template.md").write_text(
        prompt_template, encoding="utf-8"
    )

    summary = {
        "pdf_count": len(pdf_paths),
        "docs_used": len(doc_stats),
        "docs_excluded": len(excluded_docs),
        "total_words": total_words,
        "unique_words": unique_words,
        "avg_sentence_len": mean_sentence,
        "top_10_content_words": [w["token"] for w in style_profile["top_content_words"][:10]],
        "outputs": {
            "style_profile_json": str(results_dir / "style_profile.json"),
            "style_guide_md": str(results_dir / "style_guide.md"),
            "rewrite_template_md": str(results_dir / "rewrite_template.md"),
            "lexicon_tsv": str(results_dir / "lexicon_top_800.tsv"),
            "corpus_clean_txt": str(results_dir / "corpus_clean.txt"),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
