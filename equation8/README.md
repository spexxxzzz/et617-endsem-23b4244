# Equation8

A calm, adaptive Class 8 tutor for linear equations in one variable. ET617 card **P4–T3–L5–C4**, roll **23b4244**.

Eight tasks span numerical responses, multiple choice, error correction and explanation. Hyde GLM assesses explanations, offers reviewed hints and generates arithmetic-checked stretch questions. The three adaptive branches are prerequisite instruction, alternative explanation and harder practice.

## Run locally

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.lock.txt
npm ci
# Configure the server-only HYDE_API_KEY in .env.
npm run dev:all
```

Open http://127.0.0.1:5173. Run `.venv/bin/python -m unittest discover -s tests -v` and `npm run build` to verify.

## Vercel

Select this folder as the Root Directory. The checked-in `vercel.json` builds Vite static assets and the minimal Python API. See [deployment configuration](docs/VERCEL.md). No deployment is started automatically.

Design: [DESIGN.md](DESIGN.md). Submission: [checklist](docs/SUBMISSION_CHECKLIST.md). Required third-party copyright notices are retained in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and distributed with the built site.
