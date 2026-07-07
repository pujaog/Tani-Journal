'use client'

import { initializeApp, getApps, getApp } from 'firebase/app'
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
  signOut as fbSignOut,
  onAuthStateChanged,
} from 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
}

const app = getApps().length ? getApp() : initializeApp(firebaseConfig)
export const auth = getAuth(app)

const googleProvider = new GoogleAuthProvider()
googleProvider.setCustomParameters({ prompt: 'select_account' })

export async function signInWithGoogle() {
  return signInWithPopup(auth, googleProvider)
}

export async function signInEmail(email, password) {
  return signInWithEmailAndPassword(auth, email, password)
}

export async function signUpEmail(email, password, displayName) {
  const cred = await createUserWithEmailAndPassword(auth, email, password)
  if (displayName) {
    await updateProfile(cred.user, { displayName })
  }
  return cred
}

export async function signOut() {
  return fbSignOut(auth)
}

export { onAuthStateChanged }

export async function authedFetch(url, options = {}) {
  const user = auth.currentUser
  const headers = { ...(options.headers || {}) }
  if (user) {
    const token = await user.getIdToken()
    headers['Authorization'] = `Bearer ${token}`
  }
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  return fetch(url, { ...options, headers })
}
