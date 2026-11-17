"""Publica no Instagram (@4nderson.eng) o post de um dia: feed, reel e/ou story.

Uso: python scripts/publicar.py AAAA-MM-DD feed,reel,story
Le publicar/AAAA-MM-DD/{post.jpg, reel.mp4, story.jpg, legenda.txt} e grava data/posted.json (trava contra duplicar).
Requer IG_ACCESS_TOKEN (token de Pagina) e GITHUB_REPOSITORY. IG_USER_ID e opcional.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
POSTED = ROOT / "data" / "posted.json"
ARQ = {"feed": "post.jpg", "reel": "reel.mp4", "story": "story.jpg"}


def main(date, targets):
    posted = json.loads(POSTED.read_text(encoding="utf-8")) if POSTED.exists() else {}
    day = posted.setdefault(date, {})
    folder = ROOT / "publicar" / date
    if not folder.exists():
        sys.exit(f"Nao ha arquivos em {folder}")
    caption = (folder / "legenda.txt").read_text(encoding="utf-8")
    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    base = f"https://raw.githubusercontent.com/{repo}/{branch}/publicar/{date}"

    user_id = ig.clean_secret(os.environ.get("IG_USER_ID", ""))
    token = ig.clean_secret(os.environ["IG_ACCESS_TOKEN"])
    user_id, token = ig.resolve_ig(user_id, token)

    falhas = []
    for t in targets:
        if t in day:
            print(f"[{t}] {date} ja foi publicado ({day[t]['media_id']}); pulando.")
            continue
        if not (folder / ARQ[t]).exists():
            falhas.append(f"{t}: arquivo {ARQ[t]} nao existe")
            continue
        url = f"{base}/{ARQ[t]}"
        try:
            if t == "feed":
                mid = ig.publish_image(user_id, token, url, caption)
            elif t == "reel":
                mid = ig.publish_reel(user_id, token, url, caption)
            else:
                mid = ig.publish_story(user_id, token, url)
        except Exception as e:  # noqa: BLE001
            falhas.append(f"{t}: {e}")
            print(f"[{t}] FALHOU: {e}", file=sys.stderr)
            continue
        day[t] = {"media_id": mid, "at": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds")}
        POSTED.write_text(json.dumps(posted, indent=2, ensure_ascii=False), encoding="utf-8")  # grava ja, um por um
        print(f"[{t}] publicado: media_id={mid}")
    if falhas:
        sys.exit("Falhas: " + " | ".join(falhas))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit("Uso: python scripts/publicar.py AAAA-MM-DD feed,reel,story")
    alvos = [x for x in sys.argv[2].split(",") if x in ARQ]
    if not alvos:
        sys.exit("Alvos validos: feed, reel, story")
    main(sys.argv[1], alvos)
