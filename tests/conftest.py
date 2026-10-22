import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASE1 = ROOT / "phase-1-conference-version"
PHASE2 = ROOT / "phase-2-extended-ai-version"

sys.path.insert(0, str(PHASE1 / "core"))
sys.path.insert(0, str(PHASE2 / "app"))
