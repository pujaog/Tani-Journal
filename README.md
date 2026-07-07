# The Tani Journal

> Your story, beautifully kept. A media-rich journaling platform with authentication, private/public entries, engagement (likes, comments, views), Google Drive backup, presence indicators, follows, and moderation.

![Next.js](https://img.shields.io/badge/Next.js-15-black) ![Firebase](https://img.shields.io/badge/Firebase%20Auth-Google%20%2B%20Email-orange) ![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green) ![Tailwind](https://img.shields.io/badge/Tailwind-3-06B6D4)

---

## Features

- ✈️ **Rich post editor** — markdown-style body, image + video uploads (up to 20 MB), per-media aspect ratio (16:9 or 3:4), mood chips
- 📖 **Timeline feed** grouped by month, with three tabs: **My Journal**, **Following**, **Community**
- 🎨 **Style engine** — 4 background themes (Paper, Midnight, Sepia, Forest) × 4 typefaces (Fraunces, Inter, Playfair, JetBrains Mono)
- 🔐 **Firebase Auth** — Google Sign-In + Email/Password + password reset
- ☁️ **Google Drive integration** — optional; entries also saved as `.md` files in a *The Tani Journal* folder in your Drive
- ❤️ **Engagement** — likes, view counts, near-realtime comments (8s polling)
- 🔵 **Presence** — blue/dark dots showing who is online (heartbeat every 25 s)
- 👤 **Profiles + follows** — click any author for their public timeline
- 🔔 **Notifications** — likes, comments, and follows
- 🛡️ **Report & moderation** — users report inappropriate posts; admin queue to dismiss or delete

---

## Tech Stack

- **Frontend & Backend**: Next.js 15 (App Router) with API routes
- **Database**: MongoDB (Atlas for prod)
- **Auth**: Firebase Authentication (server-side ID token verification with `jose` + Firebase public JWKS — no service account needed)
- **Storage**: Optional Google Drive (`drive.file` OAuth scope) via lightweight REST client
- **Styling**: Tailwind CSS + shadcn primitives
- **Icons**: lucide-react

---

## Local Development

### 1. Clone

```bash
git clone https://github.com/pujaog/The-Tani-Journal-.git
cd The-Tani-Journal-
```

### 2. Install dependencies

```bash
yarn install
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Then fill in the values — see [Environment Variables](#environment-variables) below.

### 4. Run

```bash
yarn dev
```

Open http://localhost:3000

---

## Environment Variables

See [.env.example](./.env.example) for the full template.

| Variable | Required | Purpose |
|---|---|---|
| `MONGO_URL` | ✅ | MongoDB connection string |
| `DB_NAME` | ✅ | MongoDB database name (e.g. `tani_journal`) |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | ✅ | Firebase Web SDK config |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | ✅ | Firebase Web SDK config |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | ✅ | Firebase Web SDK config — also used server-side for token verification |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | ✅ | Firebase Web SDK config |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | ✅ | Firebase Web SDK config |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | ✅ | Firebase Web SDK config |
| `NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID` | ❌ | Optional analytics ID |
| `ADMIN_EMAILS` | ❌ | Comma-separated emails that see the moderation queue |
| `CORS_ORIGINS` | ❌ | Defaults to `*` |

---

## Deploying to Vercel + GitHub

### Step 1: Set up MongoDB Atlas (free tier)

1. Go to https://www.mongodb.com/cloud/atlas/register and sign up (free)
2. Create a new project
3. Click **Build a Database** → choose **M0 Free** → pick a cloud region close to Vercel’s (AWS `us-east-1` is a safe pick) → **Create**
4. When prompted for **Security Quickstart**:
   - Create a database user (remember username + password)
   - Under **Where would you like to connect from?** choose **My Local Environment** → click **Add My Current IP Address**, then also add `0.0.0.0/0` (Allow access from anywhere) so Vercel can reach it
5. Once cluster is ready, click **Connect** → **Drivers** → select **Node.js** → copy the connection string. It looks like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<username>` and `<password>` with the ones you created. This is your `MONGO_URL`.
7. Choose a `DB_NAME` (e.g. `tani_journal`) — MongoDB auto-creates it on first write.

### Step 2: Set up Firebase (if you haven’t already)

1. Go to https://console.firebase.google.com → **Add project** → name it, disable Analytics if you like, create
2. Add a **Web app** (`</>` icon) — copy the `firebaseConfig` object shown; those go into your env vars
3. Enable sign-in methods: **Authentication → Sign-in method** → enable **Google** and **Email/Password**
4. Add your production domain to **Authentication → Settings → Authorized domains** (e.g. `your-app.vercel.app`)

### Step 3: (Optional) Enable Google Drive integration

1. In Google Cloud Console (same project as Firebase): **APIs & Services → Library → Google Drive API → Enable**
2. **OAuth consent screen → Scopes → Add or Remove Scopes** → add `https://www.googleapis.com/auth/drive.file`
3. If in *Testing* mode, add your email as a **Test user**

### Step 4: Push to GitHub

```bash
cd The-Tani-Journal-
git init
git add .
git commit -m "Initial commit: The Tani Journal"
git branch -M main
git remote add origin https://github.com/pujaog/The-Tani-Journal-.git
git push -u origin main
```

### Step 5: Deploy on Vercel

1. Go to https://vercel.com and sign in with GitHub
2. Click **Add New → Project** → import `pujaog/The-Tani-Journal-`
3. Framework Preset: **Next.js** (auto-detected)
4. Under **Environment Variables**, add ALL variables from your `.env` file:
   - Set `MONGO_URL` to your Atlas connection string (from Step 1)
   - Set all `NEXT_PUBLIC_FIREBASE_*` values from Firebase Console (Step 2)
   - Set `DB_NAME`, `ADMIN_EMAILS`, etc.
   - Set `NEXT_PUBLIC_BASE_URL` to `https://your-app.vercel.app` (after first deploy Vercel will assign you a URL)
5. Click **Deploy**
6. After deploy, copy your Vercel URL and:
   - Add it to **Firebase Auth → Authorized domains**
   - Optionally set it as `NEXT_PUBLIC_BASE_URL` env var and redeploy

### Step 6: Post-deploy checks

- Visit `https://your-app.vercel.app/api/health` → should return `{ "status": "ok", ... }`
- Sign in with Google or Email/Password
- Write your first entry 🎉

---

## Project Structure

```
app/
  api/[[...path]]/route.js   # All backend endpoints (catch-all)
  page.js                    # Main app UI (sign-in, feed, editor, admin, etc.)
  layout.js                  # Root layout with fonts
  globals.css                # Themes + design tokens
lib/
  firebase.js                # Client-side Firebase Auth + Drive OAuth
  auth-server.js             # Server-side ID token verification (jose)
  drive.js                   # Lightweight Drive REST client (no SDK)
components/ui/               # shadcn primitives
.env.example                 # Env var template
vercel.json                  # Vercel config (API function timeout)
```

---

## Database Schema (MongoDB collections)

- **posts** `{ id, authorUid, title, content, mood, images[], visibility, likeCount, commentCount, viewCount, viewerUids[], createdAt, updatedAt }`
- **profiles** `{ uid, email, displayName, photoURL, bio, createdAt, updatedAt }`
- **likes** `{ id, postId, uid, createdAt }` (unique compound on postId+uid)
- **comments** `{ id, postId, authorUid, content, createdAt }`
- **follows** `{ id, followerUid, followingUid, createdAt }` (unique compound)
- **presence** `{ uid, lastSeen }` (unique on uid)
- **notifications** `{ id, userUid, actorUid, type, postId, commentId, meta, read, createdAt }`
- **reports** `{ id, postId, authorUid, reporterUid, reason, status, createdAt, resolvedAt?, resolvedBy?, note? }`

---

## API Endpoints

All routes are prefixed with `/api`.

### Public
- `GET /api/health` — health check
- `GET /api/posts?scope=community` — public feed
- `GET /api/posts/:id` — single post (public only unless owner)
- `POST /api/posts/:id/view` — increment view count
- `GET /api/posts/:id/comments` — list comments (if post is public)
- `GET /api/profiles/:uid` — public profile + stats
- `GET /api/profiles/:uid/posts` — that user’s public posts
- `GET /api/presence?uids=a,b,c` — presence map
- `POST /api/upload` — echoes back a data URL (for MVP media uploads)

### Authenticated (Firebase ID token in `Authorization: Bearer <token>`)
- `GET /api/me` / `PATCH /api/me` — profile
- `GET /api/posts?scope=mine` — my journal
- `GET /api/posts?scope=following` — people I follow
- `POST /api/posts` — create
- `PUT /api/posts/:id` / `DELETE /api/posts/:id` — owner only
- `POST /api/posts/:id/like` — toggle
- `POST /api/posts/:id/comments` / `DELETE /api/comments/:id`
- `POST /api/posts/:id/report`
- `POST /api/follow/:uid` — toggle, `GET /api/follows`
- `POST /api/heartbeat`
- `GET /api/notifications` / `POST /api/notifications/read`

### Drive (auth + `X-Drive-Token` header)
- `POST /api/drive/verify`
- `POST /api/drive/sync-all`
- `POST /api/drive/sync/:postId`

### Admin (auth + email in `ADMIN_EMAILS`)
- `GET /api/admin/status` (returns `{ isAdmin: bool }` for any authed user)
- `GET /api/admin/reports`
- `POST /api/admin/reports/:id/resolve`
- `DELETE /api/admin/posts/:id`

---

## Troubleshooting

**Google sign-in fails with `auth/unauthorized-domain`**
→ Add your production domain in Firebase Console → Authentication → Settings → Authorized domains.

**Drive sync fails with 401**
→ The OAuth access token expired (they last ~1h). Reconnect Drive from the user menu.

**MongoDB connection times out on Vercel**
→ Add `0.0.0.0/0` to your MongoDB Atlas Network Access list.

**Videos don’t upload**
→ Files are limited to 20 MB in the current MVP (base64 embedded). For larger media, hook up a real object store.

---

## License

MIT — do whatever you want, just be kind.
