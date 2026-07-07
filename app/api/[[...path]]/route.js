import { NextResponse } from 'next/server'
import { MongoClient } from 'mongodb'
import { v4 as uuidv4 } from 'uuid'
import { verifyIdTokenFromRequest } from '@/lib/auth-server'

const MONGO_URL = process.env.MONGO_URL
const DB_NAME = process.env.DB_NAME || 'tani_journal'

let cachedClient = null
async function getDb() {
  if (cachedClient) return cachedClient.db(DB_NAME)
  const client = new MongoClient(MONGO_URL)
  await client.connect()
  cachedClient = client
  return client.db(DB_NAME)
}

const json = (data, status = 200) => NextResponse.json(data, { status })

function clean(doc) {
  if (!doc) return null
  const { _id, ...rest } = doc
  return rest
}

async function readBody(req) {
  try { return await req.json() } catch { return {} }
}

// Ensure user profile exists / return it. Called on any authed request.
async function ensureProfile(db, authUser) {
  const profiles = db.collection('profiles')
  const existing = await profiles.findOne({ uid: authUser.uid })
  if (existing) return existing
  const now = new Date().toISOString()
  const doc = {
    uid: authUser.uid,
    email: authUser.email,
    displayName: authUser.name || (authUser.email ? authUser.email.split('@')[0] : 'Anonymous'),
    photoURL: authUser.picture || null,
    bio: '',
    createdAt: now,
    updatedAt: now,
  }
  await profiles.insertOne(doc)
  return doc
}

function normalizeImages(imgs) {
  if (!Array.isArray(imgs)) return []
  return imgs.slice(0, 6).map(im => ({
    url: (im.url || '').toString(),
    aspectRatio: im.aspectRatio === '3:4' ? '3:4' : '16:9',
  }))
}

async function handle(request, ctx) {
  const params = await ctx.params
  const segs = params?.path || []
  const path = '/' + segs.join('/')
  const method = request.method

  try {
    const db = await getDb()
    const posts = db.collection('posts')
    const profiles = db.collection('profiles')

    // Public health
    if (path === '/' || path === '/health') {
      return json({ status: 'ok', service: 'tani-journal', time: new Date().toISOString() })
    }

    // Auth for the following endpoints
    const authUser = await verifyIdTokenFromRequest(request)

    // ---- Profile endpoints ----
    // GET /me  - my profile (creates on first call)
    if (path === '/me' && method === 'GET') {
      if (!authUser) return json({ error: 'Unauthorized' }, 401)
      const prof = await ensureProfile(db, authUser)
      return json({ profile: clean(prof) })
    }
    // PATCH /me - edit my profile { displayName, photoURL, bio }
    if (path === '/me' && (method === 'PATCH' || method === 'PUT')) {
      if (!authUser) return json({ error: 'Unauthorized' }, 401)
      await ensureProfile(db, authUser)
      const body = await readBody(request)
      const update = { updatedAt: new Date().toISOString() }
      if (body.displayName !== undefined) update.displayName = String(body.displayName).slice(0, 60)
      if (body.photoURL !== undefined) update.photoURL = body.photoURL ? String(body.photoURL) : null
      if (body.bio !== undefined) update.bio = String(body.bio).slice(0, 280)
      const res = await profiles.findOneAndUpdate(
        { uid: authUser.uid },
        { $set: update },
        { returnDocument: 'after' }
      )
      const doc = res?.value || res
      return json({ profile: clean(doc) })
    }

    // GET /profiles/:uid - fetch a public profile
    if (segs[0] === 'profiles' && segs[1] && method === 'GET') {
      const prof = await profiles.findOne({ uid: segs[1] })
      if (!prof) return json({ error: 'Not found' }, 404)
      return json({ profile: clean(prof) })
    }

    // ---- Posts ----
    // GET /posts?scope=mine|community
    if (path === '/posts' && method === 'GET') {
      const url = new URL(request.url)
      const scope = url.searchParams.get('scope') || 'community'
      let filter = {}
      if (scope === 'mine') {
        if (!authUser) return json({ error: 'Unauthorized' }, 401)
        filter = { authorUid: authUser.uid }
      } else {
        filter = { visibility: 'public' }
      }
      const list = await posts.find(filter).sort({ createdAt: -1 }).limit(200).toArray()
      // Attach author info
      const uids = [...new Set(list.map(p => p.authorUid).filter(Boolean))]
      const profDocs = uids.length ? await profiles.find({ uid: { $in: uids } }).toArray() : []
      const profMap = Object.fromEntries(profDocs.map(p => [p.uid, {
        uid: p.uid, displayName: p.displayName, photoURL: p.photoURL,
      }]))
      return json({
        posts: list.map(p => ({ ...clean(p), author: profMap[p.authorUid] || null })),
      })
    }

    // POST /posts
    if (path === '/posts' && method === 'POST') {
      if (!authUser) return json({ error: 'Unauthorized' }, 401)
      await ensureProfile(db, authUser)
      const body = await readBody(request)
      const now = new Date().toISOString()
      const doc = {
        id: uuidv4(),
        authorUid: authUser.uid,
        title: (body.title || '').toString().slice(0, 200),
        content: (body.content || '').toString(),
        mood: (body.mood || '').toString().slice(0, 40),
        images: normalizeImages(body.images),
        visibility: body.visibility === 'public' ? 'public' : 'private',
        createdAt: now,
        updatedAt: now,
      }
      await posts.insertOne(doc)
      const author = await profiles.findOne({ uid: authUser.uid })
      return json({
        post: {
          ...clean(doc),
          author: author ? { uid: author.uid, displayName: author.displayName, photoURL: author.photoURL } : null,
        },
      }, 201)
    }

    // /posts/:id
    if (segs[0] === 'posts' && segs[1]) {
      const id = segs[1]
      if (method === 'GET') {
        const doc = await posts.findOne({ id })
        if (!doc) return json({ error: 'Not found' }, 404)
        // Private posts only viewable by owner
        if (doc.visibility !== 'public' && (!authUser || authUser.uid !== doc.authorUid)) {
          return json({ error: 'Forbidden' }, 403)
        }
        const author = await profiles.findOne({ uid: doc.authorUid })
        return json({
          post: {
            ...clean(doc),
            author: author ? { uid: author.uid, displayName: author.displayName, photoURL: author.photoURL } : null,
          },
        })
      }
      if (method === 'PUT' || method === 'PATCH') {
        if (!authUser) return json({ error: 'Unauthorized' }, 401)
        const existing = await posts.findOne({ id })
        if (!existing) return json({ error: 'Not found' }, 404)
        if (existing.authorUid !== authUser.uid) return json({ error: 'Forbidden' }, 403)
        const body = await readBody(request)
        const update = { updatedAt: new Date().toISOString() }
        if (body.title !== undefined) update.title = String(body.title).slice(0, 200)
        if (body.content !== undefined) update.content = String(body.content)
        if (body.mood !== undefined) update.mood = String(body.mood).slice(0, 40)
        if (Array.isArray(body.images)) update.images = normalizeImages(body.images)
        if (body.visibility !== undefined) update.visibility = body.visibility === 'public' ? 'public' : 'private'
        const res = await posts.findOneAndUpdate({ id }, { $set: update }, { returnDocument: 'after' })
        const doc = res?.value || res
        return json({ post: clean(doc) })
      }
      if (method === 'DELETE') {
        if (!authUser) return json({ error: 'Unauthorized' }, 401)
        const existing = await posts.findOne({ id })
        if (!existing) return json({ error: 'Not found' }, 404)
        if (existing.authorUid !== authUser.uid) return json({ error: 'Forbidden' }, 403)
        await posts.deleteOne({ id })
        return json({ ok: true })
      }
    }

    // Upload echo
    if (path === '/upload' && method === 'POST') {
      const body = await readBody(request)
      if (!body.dataUrl) return json({ error: 'dataUrl required' }, 400)
      return json({ url: body.dataUrl })
    }

    return json({ error: 'Not found', path, method }, 404)
  } catch (err) {
    console.error('API error:', err)
    return json({ error: 'Server error', detail: String(err?.message || err) }, 500)
  }
}

export const GET = handle
export const POST = handle
export const PUT = handle
export const PATCH = handle
export const DELETE = handle
