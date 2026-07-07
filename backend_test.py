#!/usr/bin/env python3
"""
Backend API Tests for The Tani Journal - Phase 3
Tests engagement, follow system, presence, and author profile endpoints.
"""

import requests
import json
import sys
from datetime import datetime

# Base URL from environment
BASE_URL = "https://journal-media-hub.preview.emergentagent.com/api"

def log(msg, level="INFO"):
    """Log test messages with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def test_engagement_endpoints():
    """Test 1-7: Engagement endpoints (likes, views, comments, reports)"""
    log("=" * 60)
    log("TEST 1-7: Engagement Endpoints")
    log("=" * 60)
    
    results = []
    fake_post_id = "fake-post-id-12345"
    fake_comment_id = "fake-comment-id-12345"
    
    # Test 1: POST /api/posts/fake-id/like (no auth) → expect 401
    try:
        log("\n1. Testing POST /api/posts/fake-id/like without auth...")
        resp = requests.post(f"{BASE_URL}/posts/{fake_post_id}/like", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/posts/fake-id/like (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/posts/fake-id/like (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/posts/fake-id/like (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts/fake-id/like (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts/fake-id/like (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts/fake-id/like (no auth)", False, str(e)))
    
    # Test 2: POST /api/posts/fake-id/like (with invalid token) → expect 401
    try:
        log("\n2. Testing POST /api/posts/fake-id/like with invalid token...")
        headers = {"Authorization": "Bearer badtoken"}
        resp = requests.post(f"{BASE_URL}/posts/{fake_post_id}/like", headers=headers, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/posts/fake-id/like (invalid token) - PASSED", "SUCCESS")
            results.append(("POST /api/posts/fake-id/like (invalid token)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/posts/fake-id/like (invalid token) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts/fake-id/like (invalid token)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts/fake-id/like (invalid token) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts/fake-id/like (invalid token)", False, str(e)))
    
    # Test 3: POST /api/posts/fake-id/view (no auth) → expect 404
    try:
        log("\n3. Testing POST /api/posts/fake-id/view without auth...")
        resp = requests.post(f"{BASE_URL}/posts/{fake_post_id}/view", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 404:
            log("✅ POST /api/posts/fake-id/view (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/posts/fake-id/view (no auth)", True, "Returns 404 as expected (post doesn't exist)"))
        elif resp.status_code == 500:
            log("❌ POST /api/posts/fake-id/view (no auth) - FAILED: Got 500 instead of 404", "ERROR")
            results.append(("POST /api/posts/fake-id/view (no auth)", False, "Returns 500 instead of 404"))
        else:
            log(f"❌ POST /api/posts/fake-id/view (no auth) - FAILED: Expected 404, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts/fake-id/view (no auth)", False, f"Expected 404, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts/fake-id/view (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts/fake-id/view (no auth)", False, str(e)))
    
    # Test 4: GET /api/posts/fake-id/comments (no auth) → 404
    try:
        log("\n4. Testing GET /api/posts/fake-id/comments without auth...")
        resp = requests.get(f"{BASE_URL}/posts/{fake_post_id}/comments", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 404:
            log("✅ GET /api/posts/fake-id/comments (no auth) - PASSED", "SUCCESS")
            results.append(("GET /api/posts/fake-id/comments (no auth)", True, "Returns 404 as expected"))
        else:
            log(f"❌ GET /api/posts/fake-id/comments (no auth) - FAILED: Expected 404, got {resp.status_code}", "ERROR")
            results.append(("GET /api/posts/fake-id/comments (no auth)", False, f"Expected 404, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/posts/fake-id/comments (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/posts/fake-id/comments (no auth)", False, str(e)))
    
    # Test 5: POST /api/posts/{fake-id}/comments (no auth) → 401
    try:
        log("\n5. Testing POST /api/posts/fake-id/comments without auth...")
        payload = {"content": "hi"}
        resp = requests.post(f"{BASE_URL}/posts/{fake_post_id}/comments", json=payload, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/posts/fake-id/comments (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/posts/fake-id/comments (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/posts/fake-id/comments (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts/fake-id/comments (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts/fake-id/comments (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts/fake-id/comments (no auth)", False, str(e)))
    
    # Test 6: DELETE /api/comments/fake-id (no auth) → 401
    try:
        log("\n6. Testing DELETE /api/comments/fake-id without auth...")
        resp = requests.delete(f"{BASE_URL}/comments/{fake_comment_id}", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ DELETE /api/comments/fake-id (no auth) - PASSED", "SUCCESS")
            results.append(("DELETE /api/comments/fake-id (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ DELETE /api/comments/fake-id (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("DELETE /api/comments/fake-id (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ DELETE /api/comments/fake-id (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("DELETE /api/comments/fake-id (no auth)", False, str(e)))
    
    # Test 7: POST /api/posts/fake-id/report (no auth) → 401
    try:
        log("\n7. Testing POST /api/posts/fake-id/report without auth...")
        payload = {"reason": "spam"}
        resp = requests.post(f"{BASE_URL}/posts/{fake_post_id}/report", json=payload, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/posts/fake-id/report (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/posts/fake-id/report (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/posts/fake-id/report (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts/fake-id/report (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts/fake-id/report (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts/fake-id/report (no auth)", False, str(e)))
    
    return results

def test_follow_system():
    """Test 8-10: Follow system endpoints"""
    log("\n" + "=" * 60)
    log("TEST 8-10: Follow System Endpoints")
    log("=" * 60)
    
    results = []
    
    # Test 8: POST /api/follow/xyz (no auth) → 401
    try:
        log("\n8. Testing POST /api/follow/xyz without auth...")
        resp = requests.post(f"{BASE_URL}/follow/xyz", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/follow/xyz (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/follow/xyz (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/follow/xyz (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/follow/xyz (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/follow/xyz (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/follow/xyz (no auth)", False, str(e)))
    
    # Test 9: GET /api/follows (no auth) → 401
    try:
        log("\n9. Testing GET /api/follows without auth...")
        resp = requests.get(f"{BASE_URL}/follows", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ GET /api/follows (no auth) - PASSED", "SUCCESS")
            results.append(("GET /api/follows (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ GET /api/follows (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("GET /api/follows (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/follows (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/follows (no auth)", False, str(e)))
    
    # Test 10: GET /api/posts?scope=following (no auth) → 401
    try:
        log("\n10. Testing GET /api/posts?scope=following without auth...")
        resp = requests.get(f"{BASE_URL}/posts?scope=following", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ GET /api/posts?scope=following (no auth) - PASSED", "SUCCESS")
            results.append(("GET /api/posts?scope=following (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ GET /api/posts?scope=following (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("GET /api/posts?scope=following (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/posts?scope=following (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/posts?scope=following (no auth)", False, str(e)))
    
    return results

def test_presence_endpoints():
    """Test 11-13: Presence endpoints"""
    log("\n" + "=" * 60)
    log("TEST 11-13: Presence Endpoints")
    log("=" * 60)
    
    results = []
    
    # Test 11: POST /api/heartbeat (no auth) → 401
    try:
        log("\n11. Testing POST /api/heartbeat without auth...")
        resp = requests.post(f"{BASE_URL}/heartbeat", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/heartbeat (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/heartbeat (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/heartbeat (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/heartbeat (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/heartbeat (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/heartbeat (no auth)", False, str(e)))
    
    # Test 12: GET /api/presence (no auth, no query) → 200 with { presence: {} }
    try:
        log("\n12. Testing GET /api/presence without auth and no query...")
        resp = requests.get(f"{BASE_URL}/presence", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'presence' in data and data['presence'] == {}:
                log("✅ GET /api/presence (no query) - PASSED", "SUCCESS")
                results.append(("GET /api/presence (no query)", True, "Returns 200 with empty presence object"))
            else:
                log(f"❌ GET /api/presence (no query) - FAILED: Expected {{presence: {{}}}}, got {data}", "ERROR")
                results.append(("GET /api/presence (no query)", False, f"Expected {{presence: {{}}}}, got {data}"))
        else:
            log(f"❌ GET /api/presence (no query) - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("GET /api/presence (no query)", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/presence (no query) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/presence (no query)", False, str(e)))
    
    # Test 13: GET /api/presence?uids=alice,bob (no auth) → 200 { presence: { alice: false, bob: false } }
    try:
        log("\n13. Testing GET /api/presence?uids=alice,bob without auth...")
        resp = requests.get(f"{BASE_URL}/presence?uids=alice,bob", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'presence' in data and data['presence'].get('alice') == False and data['presence'].get('bob') == False:
                log("✅ GET /api/presence?uids=alice,bob - PASSED", "SUCCESS")
                results.append(("GET /api/presence?uids=alice,bob", True, "Returns 200 with presence: {alice: false, bob: false}"))
            else:
                log(f"❌ GET /api/presence?uids=alice,bob - FAILED: Expected alice and bob to be false, got {data}", "ERROR")
                results.append(("GET /api/presence?uids=alice,bob", False, f"Expected alice and bob to be false, got {data}"))
        else:
            log(f"❌ GET /api/presence?uids=alice,bob - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("GET /api/presence?uids=alice,bob", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/presence?uids=alice,bob - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/presence?uids=alice,bob", False, str(e)))
    
    return results

def test_author_profile_endpoints():
    """Test 14-15: Author profile endpoints"""
    log("\n" + "=" * 60)
    log("TEST 14-15: Author Profile Endpoints")
    log("=" * 60)
    
    results = []
    
    # Test 14: GET /api/profiles/nonexistent (no auth) → 404
    try:
        log("\n14. Testing GET /api/profiles/nonexistent without auth...")
        resp = requests.get(f"{BASE_URL}/profiles/nonexistent", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 404:
            log("✅ GET /api/profiles/nonexistent - PASSED", "SUCCESS")
            results.append(("GET /api/profiles/nonexistent", True, "Returns 404 as expected"))
        else:
            log(f"❌ GET /api/profiles/nonexistent - FAILED: Expected 404, got {resp.status_code}", "ERROR")
            results.append(("GET /api/profiles/nonexistent", False, f"Expected 404, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/profiles/nonexistent - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/profiles/nonexistent", False, str(e)))
    
    # Test 15: GET /api/profiles/nonexistent/posts (no auth) → 200 { posts: [] }
    try:
        log("\n15. Testing GET /api/profiles/nonexistent/posts without auth...")
        resp = requests.get(f"{BASE_URL}/profiles/nonexistent/posts", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'posts' in data and data['posts'] == []:
                log("✅ GET /api/profiles/nonexistent/posts - PASSED", "SUCCESS")
                results.append(("GET /api/profiles/nonexistent/posts", True, "Returns 200 with empty posts array"))
            else:
                log(f"❌ GET /api/profiles/nonexistent/posts - FAILED: Expected {{posts: []}}, got {data}", "ERROR")
                results.append(("GET /api/profiles/nonexistent/posts", False, f"Expected {{posts: []}}, got {data}"))
        else:
            log(f"❌ GET /api/profiles/nonexistent/posts - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("GET /api/profiles/nonexistent/posts", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/profiles/nonexistent/posts - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/profiles/nonexistent/posts", False, str(e)))
    
    return results

def test_regression_endpoints():
    """Test 16-20: Regression tests for existing endpoints"""
    log("\n" + "=" * 60)
    log("TEST 16-20: Regression Tests")
    log("=" * 60)
    
    results = []
    
    # Test 16: GET /api/health → 200 ok
    try:
        log("\n16. Testing GET /api/health...")
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'ok':
                log("✅ GET /api/health - PASSED", "SUCCESS")
                results.append(("GET /api/health", True, "Returns 200 with status ok"))
            else:
                log(f"❌ GET /api/health - FAILED: Expected status ok, got {data}", "ERROR")
                results.append(("GET /api/health", False, f"Expected status ok, got {data}"))
        else:
            log(f"❌ GET /api/health - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("GET /api/health", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/health - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/health", False, str(e)))
    
    # Test 17: GET /api/posts?scope=community → 200 { posts: [] }
    try:
        log("\n17. Testing GET /api/posts?scope=community...")
        resp = requests.get(f"{BASE_URL}/posts?scope=community", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'posts' in data and isinstance(data['posts'], list):
                log("✅ GET /api/posts?scope=community - PASSED", "SUCCESS")
                results.append(("GET /api/posts?scope=community", True, f"Returns 200 with {len(data['posts'])} posts"))
            else:
                log(f"❌ GET /api/posts?scope=community - FAILED: Expected posts array, got {data}", "ERROR")
                results.append(("GET /api/posts?scope=community", False, f"Expected posts array, got {data}"))
        else:
            log(f"❌ GET /api/posts?scope=community - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("GET /api/posts?scope=community", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/posts?scope=community - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/posts?scope=community", False, str(e)))
    
    # Test 18: POST /api/upload {dataUrl:'data:image/png;base64,AA'} → 200 { url: '...' }
    try:
        log("\n18. Testing POST /api/upload...")
        payload = {"dataUrl": "data:image/png;base64,AA"}
        resp = requests.post(f"{BASE_URL}/upload", json=payload, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'url' in data:
                log("✅ POST /api/upload - PASSED", "SUCCESS")
                results.append(("POST /api/upload", True, "Returns 200 with url"))
            else:
                log(f"❌ POST /api/upload - FAILED: Expected url field, got {data}", "ERROR")
                results.append(("POST /api/upload", False, f"Expected url field, got {data}"))
        else:
            log(f"❌ POST /api/upload - FAILED: Expected 200, got {resp.status_code}", "ERROR")
            results.append(("POST /api/upload", False, f"Expected 200, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/upload - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/upload", False, str(e)))
    
    # Test 19: GET /api/me (no auth) → 401
    try:
        log("\n19. Testing GET /api/me without auth...")
        resp = requests.get(f"{BASE_URL}/me", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ GET /api/me (no auth) - PASSED", "SUCCESS")
            results.append(("GET /api/me (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ GET /api/me (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("GET /api/me (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/me (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/me (no auth)", False, str(e)))
    
    # Test 20: POST /api/posts (no auth) → 401
    try:
        log("\n20. Testing POST /api/posts without auth...")
        payload = {"title": "Test", "content": "Test content"}
        resp = requests.post(f"{BASE_URL}/posts", json=payload, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 401:
            log("✅ POST /api/posts (no auth) - PASSED", "SUCCESS")
            results.append(("POST /api/posts (no auth)", True, "Returns 401 as expected"))
        else:
            log(f"❌ POST /api/posts (no auth) - FAILED: Expected 401, got {resp.status_code}", "ERROR")
            results.append(("POST /api/posts (no auth)", False, f"Expected 401, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/posts (no auth) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/posts (no auth)", False, str(e)))
    
    return results

def check_no_id_leaks(all_results):
    """Check for _id field leaks in responses"""
    log("\n" + "=" * 60)
    log("CHECKING FOR _id FIELD LEAKS")
    log("=" * 60)
    
    # Test a few endpoints that return data
    endpoints_to_check = [
        f"{BASE_URL}/posts?scope=community",
        f"{BASE_URL}/presence?uids=alice,bob",
        f"{BASE_URL}/profiles/nonexistent/posts",
    ]
    
    for endpoint in endpoints_to_check:
        try:
            resp = requests.get(endpoint, timeout=5)
            if resp.status_code == 200:
                text = resp.text
                if '"_id"' in text:
                    log(f"⚠️  WARNING: Found _id field in {endpoint}", "WARN")
                else:
                    log(f"✅ No _id leak in {endpoint}", "SUCCESS")
        except Exception as e:
            log(f"Could not check {endpoint}: {e}", "WARN")

def print_summary(all_results):
    """Print test summary"""
    log("\n" + "=" * 60)
    log("TEST SUMMARY")
    log("=" * 60)
    
    total = len(all_results)
    passed = sum(1 for _, success, _ in all_results if success)
    failed = total - passed
    
    log(f"\nTotal Tests: {total}")
    log(f"Passed: {passed}")
    log(f"Failed: {failed}")
    log(f"Success Rate: {(passed/total*100):.1f}%\n")
    
    if failed > 0:
        log("FAILED TESTS:", "ERROR")
        for name, success, msg in all_results:
            if not success:
                log(f"  ❌ {name}: {msg}", "ERROR")
    
    log("\nPASSED TESTS:", "SUCCESS")
    for name, success, msg in all_results:
        if success:
            log(f"  ✅ {name}: {msg}", "SUCCESS")
    
    return passed == total

def main():
    """Run all tests"""
    log("=" * 60)
    log("TANI JOURNAL - PHASE 3 BACKEND TESTS")
    log("=" * 60)
    log(f"Base URL: {BASE_URL}")
    log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_engagement_endpoints())
    all_results.extend(test_follow_system())
    all_results.extend(test_presence_endpoints())
    all_results.extend(test_author_profile_endpoints())
    all_results.extend(test_regression_endpoints())
    
    # Check for _id leaks
    check_no_id_leaks(all_results)
    
    # Print summary
    success = print_summary(all_results)
    
    log("\n" + "=" * 60)
    log(f"Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
