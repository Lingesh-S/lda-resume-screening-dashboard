"""Build the processed CSVs (`Resume_Data.csv`, `Job_Data.csv`) the dashboard reads.

Two input modes:

    # A folder of .pdf / .docx / .txt files (your own resumes or job descriptions)
    python core/fileReader.py folder --input path/to/resumes --output data/Resume_Data.csv

    # The public Kaggle resume dataset (Category, Resume columns), anonymised
    python core/fileReader.py kaggle --input data/resume_dataset.csv \
        --output data/Resume_Data.csv --per-category 2

Run from the `phase-1-conference-version` folder.
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import Cleaner  # noqa: E402
import tf_idf  # noqa: E402

COLUMNS = ["Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"]
SUPPORTED = {".pdf", ".docx", ".txt"}

logger = logging.getLogger("fileReader")


def read_file(path: Path) -> str:
    """Return the plain text of a .pdf, .docx or .txt file."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if suffix == ".docx":
        import docx

        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {path.name}")


def process_document(name: str, text: str) -> list:
    """Clean one document into the six columns the dashboard expects."""
    # Cleaner returns [lemmatised words, de-duplicated words, noun-only words]
    cleaned, deduped, nouns = Cleaner.Cleaner(text)
    tf_based = tf_idf.do_tfidf(deduped)
    return [name, text, " ".join(cleaned), " ".join(deduped), " ".join(nouns), tf_based]


def from_folder(folder: Path) -> pd.DataFrame:
    files = sorted(p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED)
    if not files:
        raise FileNotFoundError(f"No {', '.join(sorted(SUPPORTED))} files in {folder}")
    rows = []
    for path in files:
        try:
            rows.append(process_document(path.name, read_file(path)))
        except Exception as exc:  # keep going if one file is unreadable
            logger.warning("Skipping %s: %s", path.name, exc)
    return pd.DataFrame(rows, columns=COLUMNS)


def from_kaggle(csv_path: Path, per_category: int, seed: int = 42) -> pd.DataFrame:
    """Sample anonymised resumes from the Kaggle dataset, named by category only."""
    data = pd.read_csv(csv_path)
    shuffled = data.sample(frac=1, random_state=seed)
    sample = shuffled.groupby("Category").head(per_category).sort_values("Category").reset_index(drop=True)
    rows = []
    counters: dict = {}
    for category, text in zip(sample["Category"], sample["Resume"], strict=True):
        counters[category] = counters.get(category, 0) + 1
        rows.append(process_document(f"{category} #{counters[category]}", text))
    return pd.DataFrame(rows, columns=COLUMNS)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)
    folder = sub.add_parser("folder", help="Process a folder of documents")
    folder.add_argument("--input", type=Path, required=True)
    folder.add_argument("--output", type=Path, required=True)
    kaggle = sub.add_parser("kaggle", help="Process the Kaggle resume CSV")
    kaggle.add_argument("--input", type=Path, required=True)
    kaggle.add_argument("--output", type=Path, required=True)
    kaggle.add_argument("--per-category", type=int, default=2)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.mode == "folder":
        frame = from_folder(args.input)
    else:
        frame = from_kaggle(args.input, args.per_category)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)
    logger.info("Wrote %d rows to %s", len(frame), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
