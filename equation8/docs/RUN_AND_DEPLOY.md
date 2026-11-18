# Run and deploy: ET617 / 23b4244

## Local

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.lock.txt
npm ci
# Put the private HYDE_API_KEY in .env, using .env.example as the template.
npm run dev:all
```

Open http://127.0.0.1:5173. The key must remain on the Python server. No VITE-prefixed secret is used. `HYDE_MODEL=hyde/glm-5.3-flash`; verification currently uses a separate call to the same model. The original Gemini media adapter is retained for the upstream workspace but is not used by this lesson.

## Verify

```sh
.venv/bin/python -m unittest discover -s tests -v
npm run build
# Explicitly uses the configured live provider and records synthetic scenario outputs:
.venv/bin/python scripts/verify-et617-live.py
# Rebuild the report after capturing screenshots:
.venv/bin/python scripts/build-et617-report.py
```

## Deployment preparation

Vercel is configured with a static Vite frontend and a minimal Python API. Follow [VERCEL.md](VERCEL.md). The serverless deployment uses encrypted device checkpoints; SQLite is only the local-development storage. No deployment has been performed.

## Current advisory

The available npm registry version of picomatch is 4.0.7, which npm audit flags for a glob-pattern ReDoS issue through Vite's development/build dependency chain (four high findings including dependent packages). No fixed 4.0.8 release was available during this work. No forced major downgrade was applied. The production browser bundle does not include the Vite development server; review the advisory and available updates before public deployment.
