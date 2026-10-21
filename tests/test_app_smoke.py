"""Run both Streamlit apps headlessly and check they render without errors."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.slow
def test_phase1_dashboard_renders():
    pytest.importorskip("Distill", reason="needs spaCy en_core_web_sm and NLTK stopwords")
    app = AppTest.from_file(str(ROOT / "phase-1-conference-version" / "app" / "app.py"), default_timeout=300)
    app.run()
    assert not app.exception, app.exception
    assert app.title[0].value == "Resume Screening"


def test_phase2_signup_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("USER_DB_PATH", str(tmp_path / "users.json"))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app = AppTest.from_file(str(ROOT / "phase-2-extended-ai-version" / "app" / "app.py"), default_timeout=60)
    app.run()
    assert not app.exception, app.exception

    app.radio(key="login_signup").set_value("Signup").run()
    app.text_input[0].input("Asha")
    app.text_input[1].input("asha@example.com")
    app.text_input[2].input("pw-123")
    app.text_input[3].input("pw-123")
    app.button[0].click().run()
    assert not app.exception, app.exception
    assert app.session_state["logged_in"] is True
    assert "pw-123" not in (tmp_path / "users.json").read_text()
