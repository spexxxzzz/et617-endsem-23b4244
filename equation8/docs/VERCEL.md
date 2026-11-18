# Vercel preparation

No deployment has been made. Deploy only when authorized.

1. Import the new repository and set Root Directory to **equation8**.
2. Keep the checked-in `vercel.json`: Vite static build plus a Python FastAPI function.
3. Add **HYDE_API_KEY** to server environment variables. Do not prefix it with VITE_.
4. Set **HYDE_MODEL=hyde/glm-5.3-flash**.
5. Set **SESSION_SECRET** to a stable random secret (32+ characters). This encrypts checkpoints. If omitted, the existing server-only Hyde key is used to derive the encryption key.
6. Vercel sets VERCEL=1. This switches sessions from local SQLite to authenticated encrypted checkpoints. No database integration is needed for this individual device-based lesson.
7. After deployment, check `/api/health`, all three adaptive branches, live grading and pause/reload before submission.

The learner's device stores an opaque encrypted checkpoint and unfinished drafts. The server verifies/decrypts the checkpoint on each request and returns an updated checkpoint. This supports function restarts without writable persistent disk. It is not a centralized teacher analytics database, and clearing device storage loses access to the local record. Rotating SESSION_SECRET invalidates older checkpoints. Exported evidence does not include the opaque token.

Local development continues to use SQLite and server checkpoints. The stateless deployment path has separate integration tests. A real Vercel build and public smoke test remain to be performed when deployment is authorized.
