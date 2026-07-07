import { NextResponse } from 'next/server'
import { MongoClient } from 'mongodb'
import { v4 as uuidv4 } from 'uuid'

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

function json(data, status = 200) {
  return NextResponse.json(data, { status })
}

function cleanPost(p) {
  if (!p) return null
  const { _id, ...rest } = p
  return rest
}

async function readBody(req) {
  try { return await req.json() } catch { return {} }
}

// Route handler dispatcher
async function handle(request, ctx) {
  const params = await ctx.params
  const pathSegments = (params?.path || [])
  const path = '/' + pathSegments.join('/')
  const method = request.method
  const db = await getDb()
  const posts = db.collection('posts')

  try {
    // Health
    if (path === '/' || path === '/health') {
      return json({ status: 'ok', service: 'tani-journal', time: new Date().toISOString() })
    }

    // /posts collection
    if (path === '/posts') {
      if (method === 'GET') {
        const list = await posts.find({}).sort({ createdAt: -1 }).toArray()
        return json({ posts: list.map(cleanPost) })
      }
      if (method === 'POST') {
        const body = await readBody(request)
        const now = new Date().toISOString()
        const doc = {
          id: uuidv4(),
          title: (body.title || '').toString().slice(0, 200),
          content: (body.content || '').toString(),
          mood: (body.mood || '').toString().slice(0, 40),
          images: Array.isArray(body.images) ? body.images.slice(0, 6).map(im => ({
            url: (im.url || '').toString(),
            aspectRatio: im.aspectRatio === '3:4' ? '3:4' : '16:9',
          })) : [],
          createdAt: now,
          updatedAt: now,
        }
        await posts.insertOne(doc)
        return json({ post: cleanPost(doc) }, 201)
      }
    }

    // /posts/:id
    if (pathSegments[0] === 'posts' && pathSegments[1]) {
      const id = pathSegments[1]
      if (method === 'GET') {
        const doc = await posts.findOne({ id })
        if (!doc) return json({ error: 'Not found' }, 404)
        return json({ post: cleanPost(doc) })
      }
      if (method === 'PUT' || method === 'PATCH') {
        const body = await readBody(request)
        const update = { updatedAt: new Date().toISOString() }
        if (body.title !== undefined) update.title = String(body.title).slice(0, 200)
        if (body.content !== undefined) update.content = String(body.content)
        if (body.mood !== undefined) update.mood = String(body.mood).slice(0, 40)
        if (Array.isArray(body.images)) {
          update.images = body.images.slice(0, 6).map(im => ({
            url: (im.url || '').toString(),
            aspectRatio: im.aspectRatio === '3:4' ? '3:4' : '16:9',
          }))
        }
        const res = await posts.findOneAndUpdate({ id }, { $set: update }, { returnDocument: 'after' })
        const doc = res.value || res // driver variance
        if (!doc) return json({ error: 'Not found' }, 404)
        return json({ post: cleanPost(doc) })
      }
      if (method === 'DELETE') {
        const r = await posts.deleteOne({ id })
        if (r.deletedCount === 0) return json({ error: 'Not found' }, 404)
        return json({ ok: true })
      }
    }

    // /upload - accepts base64 data URLs; simply echoes back (stored inline in posts for MVP)
    if (path === '/upload' && method === 'POST') {
      const body = await readBody(request)
      if (!body.dataUrl) return json({ error: 'dataUrl required' }, 400)
      // For MVP we just return the data URL back as "stored" - client will embed directly in post
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
