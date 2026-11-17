# Dicas de obra - publicação no Instagram (@4nderson.eng)

Publica no Instagram, pelo GitHub Actions e a API oficial do Instagram, o **feed**, o **Reel** e o **Story** de um dia.

- `publicar/AAAA-MM-DD/`: arquivos do dia (`post.jpg`, `reel.mp4`, `story.jpg`, `legenda.txt`). O Instagram baixa as imagens daqui, por isso o repositório é público.
- `scripts/publicar.py`: publica os alvos pedidos e grava `data/posted.json` (trava para nunca publicar o mesmo alvo duas vezes no mesmo dia).
- Workflow **Publicar no Instagram** (Actions > Run workflow): informe a data e marque feed, reel e/ou story.

Segredos do repositório: `IG_ACCESS_TOKEN` (token de Página, não expira). `IG_USER_ID` é opcional.
