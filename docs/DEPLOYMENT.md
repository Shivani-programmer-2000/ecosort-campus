# Deployment guide

Two things can go live, and you can do them in any order:

| What | Where | Cost | Needs keys? |
|---|---|---|---|
| **Website** (`docs/index.html`, offline mode) | GitHub Pages | Free | No |
| **Granite-powered app** (`app.py`) | Streamlit Community Cloud | Free | Only for Granite (falls back to offline without keys) |

Prices and limits below were checked in September 2026. Vendors change them, so confirm on the linked pages.

---

## 0. Do I need credits?

| Piece | Needed to run or deploy the app? | Cost |
|---|---|---|
| **IBM Bob** | **No.** Bob is a build-time tool. The app and website never call it. It is an internship requirement, so use it while ideating, building or reviewing and keep screenshots as evidence. | 30-day free trial with a small Bobcoin allowance (IBM's trial page says 40, its download page says 50). After the trial, paid plans start around $20 per user per month. A community post reports trial users running out of Bobcoins after a few days of heavy use, so plan focused sessions. Check <https://bob.ibm.com/trial>. Ask your internship coordinator whether the programme provides Bob access. |
| **IBM Granite** (in the app) | **No.** Without keys the app runs in offline mode and still works. Add Granite when you want model-written answers. | Free options below. |
| **watsonx.ai free plan** | Only if you want hosted Granite on Streamlit Cloud | IBM lists a free plan with up to 300,000 foundation-model tokens per month. Beyond that, pay-as-you-go, for example granite-4-h-small at USD 0.06 per million input tokens and USD 0.25 per million output tokens. <https://www.ibm.com/watsonx/pricing> |
| **Granite locally** (Ollama or Hugging Face) | Only for running on your own computer | Free, but needs a reasonably powerful laptop. **Cannot run on Streamlit Community Cloud.** |
| **GitHub** and **Streamlit Community Cloud** | Yes, accounts | Free |

**How far do 300,000 tokens go?** Each Granite call in this app sends roughly 400 to 500 tokens (my estimate, not a measured figure), so the free allowance is on the order of 600 answers a month. The app protects it in three ways: repeated items are cached, `LLM_DAILY_CAP` (default 25) limits model calls per day, and when the cap or a model error is hit the app answers from the knowledge base instead of failing.

**Recommended path for the internship:** deploy the website (free, no keys) and the Streamlit app in offline mode first. Add Granite once your watsonx.ai project is ready.

---

## 1. Upload the project to GitHub

1. Create a new **public** repository named `ecosort-campus` on GitHub (no README, no licence, so it starts empty).
2. Unzip `ecosort-campus.zip`, open a terminal in the folder, and run:

```bash
git init
git add .
git commit -m "EcoSort Campus: AI for Sustainability project"
git branch -M main
git remote add origin https://github.com/<your-username>/ecosort-campus.git
git push -u origin main
```

3. Check that `.env` and `.streamlit/secrets.toml` are **not** in the repo (they are git-ignored). Never commit keys.

---

## 2. Publish the website (GitHub Pages)

1. Repo **Settings → Pages**.
2. **Build and deployment → Deploy from a branch**, branch `main`, folder **`/docs`**, then **Save**.
3. Wait about a minute. Your site is at `https://<your-username>.github.io/ecosort-campus/`.

---

## 3. Get IBM Granite credentials (optional)

Skip this section to deploy in offline mode.

1. Sign up for **IBM Cloud** and open **watsonx.ai** on the free plan (<https://www.ibm.com/watsonx/pricing>). Note the region (for example Dallas or Frankfurt).
2. Create a **project** in watsonx.ai. Open its **Manage** tab and copy the **Project ID**.
3. In the project, associate a **watsonx.ai Runtime** service instance (Manage → Services and integrations), or inference calls will be rejected.
4. In IBM Cloud, go to **Manage → Access (IAM) → API keys**, create a key and copy it once. It is shown only at creation.
5. Pick a Granite model available in your region (open **Prompt Lab** and look at the model list). The default in this repo is `ibm/granite-4-h-small`. Use the exact model ID shown to you.
6. Match the URL to your region:
   * Dallas: `https://us-south.ml.cloud.ibm.com`
   * Frankfurt: `https://eu-de.ml.cloud.ibm.com`

Menu names can differ slightly as IBM updates its console.

**Test locally before deploying:**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then edit with your values
streamlit run app.py
```

The sidebar should say **Mode: IBM Granite via watsonx:...**. If it says offline with a warning, the connection failed. Read the note under the answer for the reason.

---

## 4. Deploy the app on Streamlit Community Cloud

1. Go to <https://share.streamlit.io> and sign in with GitHub. Allow it to access your repository.
2. Click **Create app** (or **New app**) and choose **Deploy a public app from GitHub**.
3. Select repository `<your-username>/ecosort-campus`, branch `main`, and main file path **`app.py`**.
4. Click **Advanced settings**:
   * **Python version**: 3.12 (the default) works.
   * **Secrets**: paste the contents of your `secrets.toml` (from step 3). For offline mode, leave it empty or paste only `LLM_PROVIDER = "offline"`.
5. Click **Deploy**. The first build takes a few minutes.
6. Your app gets a URL like `https://<subdomain>.streamlit.app`. You can change the subdomain in the app's **Settings**.
7. To change secrets later: **Settings → Secrets**, edit and save.

Notes:
* Streamlit Community Cloud apps go to sleep after inactivity and wake on the next visit.
* The app's disk is temporary. The three anonymous feedback counters reset when the app restarts.
* Ollama and other local model servers do not work there. Use watsonx.ai or offline mode.

---

## 5. Link the website to the app

1. Put your Streamlit URL in `site/config.json`:

```json
{ "app_url": "https://<subdomain>.streamlit.app" }
```

2. Rebuild, then commit and push:

```bash
python scripts/build_site.py
git add . && git commit -m "Link website to live app" && git push
```

GitHub Pages updates in about a minute.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Sidebar says offline and shows a warning | Keys or model ID are wrong, the model is not available in your region, or the Runtime service is not associated with the project. The note under the answer shows the error type. |
| "Daily model quota reached" | You hit `LLM_DAILY_CAP`. Raise it in secrets or wait a day. Answers continue from the knowledge base. |
| Streamlit build fails on dependencies | Open the build logs (Manage app). Confirm `requirements.txt` is at the repo root. |
| Website does not update | Confirm Pages is set to `main` and `/docs`, and that `docs/index.html` was pushed. |
| CI says the website is out of date | Run `python scripts/build_site.py` and commit `docs/index.html`. |
