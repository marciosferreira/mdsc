"""Testa perguntas reais contra o agente rodando em localhost e salva as respostas."""
import json
import sys
import time

import requests

BASE = "http://127.0.0.1:8125"

QUESTIONS = [
    ("Q1", "Quanto foi alocado pra CLARO_BR neste quarter?"),
    ("Q2", "Quais Key Accounts estão com WOI crítico (abaixo de 10)?"),
    ("Q3", "Qual a alocação de hoje?"),
    ("Q4", "Quais deals foram completados integralmente?"),
    ("Q5", "Compara a alocação de FQ1 com FQ2"),
]


def ask(qid: str, message: str) -> None:
    print(f"\n{'=' * 70}\n{qid}: {message}\n{'=' * 70}", flush=True)
    t0 = time.time()
    try:
        r = requests.post(
            f"{BASE}/chat",
            json={"message": message, "session_id": f"test-claude-{qid}-{int(time.time())}"},
            timeout=300,
        )
        elapsed = time.time() - t0
        print(f"[status={r.status_code} | {elapsed:.0f}s]", flush=True)
        body = r.json()
        reply = body.get("reply", body)
        print(reply, flush=True)
    except Exception as e:
        print(f"[ERRO após {time.time() - t0:.0f}s] {type(e).__name__}: {e}", flush=True)


if __name__ == "__main__":
    only = sys.argv[1:] or None
    for qid, msg in QUESTIONS:
        if only and qid not in only:
            continue
        ask(qid, msg)
