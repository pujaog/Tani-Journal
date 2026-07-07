#!/usr/bin/env python3
"""
Backend API Tests for The Tani Journal - Phase 2 (Firebase Auth)
Tests both public and protected endpoints with and without authentication.
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

def test_public_health_endpoints():
    """Test 1-2: Public health endpoints"""
    log("=" * 60)
    log("TEST 1-2: Public Health Endpoints")
    log("=" * 60)
    
    results = []
    
    # Test 1: GET /api/health
    try:
        log("Testing GET /api/health...")
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'ok' and data.get('service') == 'tani-journal' and 'time' in data:
                log("✅ GET /api/health - PASSED", "SUCCESS")
                results.append(("GET /api/health", True, "Returns correct health status"))
            else:
                log("❌ GET /api/health - FAILED: Invalid response structure", "ERROR")
                results.append(("GET /api/health", False, f"Invalid structure: {data}"))
        else:
            log(f"❌ GET /api/health - FAILED: Status {resp.status_code}", "ERROR")
            results.append(("GET /api/health", False, f"Status {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/health - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/health", False, str(e)))
    
    # Test 2: GET /api (root)
    try:
        log("\nTesting GET /api (root)...")
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'ok' and data.get('service') == 'tani-journal' and 'time' in data:
                log("✅ GET /api (root) - PASSED", "SUCCESS")
                results.append(("GET /api (root)", True, "Returns correct health status"))
            else:
                log("❌ GET /api (root) - FAILED: Invalid response structure", "ERROR")
                results.append(("GET /api (root)", False, f"Invalid structure: {data}"))
        else:
            log(f"❌ GET /api (root) - FAILED: Status {resp.status_code}", "ERROR")
            results.append(("GET /api (root)", False, f"Status {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api (root) - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api (root)", False, str(e)))
    
    return results

def test_upload_endpoint():
    """Test 3: Upload endpoint (public)"""
    log("\n" + "=" * 60)
    log("TEST 3: Upload Endpoint (Public)")
    log("=" * 60)
    
    results = []
    
    # Test with valid dataUrl
    try:
        log("Testing POST /api/upload with valid dataUrl...")
        payload = {"dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="}
        resp = requests.post(f"{BASE_URL}/upload", json=payload, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('url') == payload['dataUrl']:
                log("✅ POST /api/upload (valid) - PASSED", "SUCCESS")
                results.append(("POST /api/upload (valid)", True, "Echoes dataUrl correctly"))
            else:
                log("❌ POST /api/upload (valid) - FAILED: URL mismatch", "ERROR")
                results.append(("POST /api/upload (valid)", False, f"URL mismatch: {data}"))
        else:
            log(f"❌ POST /api/upload (valid) - FAILED: Status {resp.status_code}", "ERROR")
            results.append(("POST /api/upload (valid)", False, f"Status {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/upload (valid) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/upload (valid)", False, str(e)))
    
    # Test without dataUrl (should return 400)
    try:
        log("\nTesting POST /api/upload without dataUrl...")
        resp = requests.post(f"{BASE_URL}/upload", json={}, timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 400:
            log("✅ POST /api/upload (missing dataUrl) - PASSED", "SUCCESS")
            results.append(("POST /api/upload (missing dataUrl)", True, "Returns 400 as expected"))
        else:
            log(f"❌ POST /api/upload (missing dataUrl) - FAILED: Expected 400, got {resp.status_code}", "ERROR")
            results.append(("POST /api/upload (missing dataUrl)", False, f"Expected 400, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ POST /api/upload (missing dataUrl) - EXCEPTION: {e}", "ERROR")
        results.append(("POST /api/upload (missing dataUrl)", False, str(e)))
    
    return results

def test_public_posts_endpoint():
    """Test 4: GET /api/posts?scope=community (public, no auth)"""
    log("\n" + "=" * 60)
    log("TEST 4: GET /api/posts?scope=community (Public)")
    log("=" * 60)
    
    results = []
    
    try:
        log("Testing GET /api/posts?scope=community without auth...")
        resp = requests.get(f"{BASE_URL}/posts?scope=community", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:500]}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'posts' in data and isinstance(data['posts'], list):
                log(f"✅ GET /api/posts?scope=community - PASSED (returned {len(data['posts'])} posts)", "SUCCESS")
                
                # Verify no _id fields leak
                has_id_leak = any('_id' in post for post in data['posts'])
                if has_id_leak:
                    log("⚠️  WARNING: Found _id field in response (should be cleaned)", "WARN")
                    results.append(("GET /api/posts?scope=community", True, f"Works but has _id leak"))
                else:
                    results.append(("GET /api/posts?scope=community", True, f"Returns {len(data['posts'])} public posts"))
            else:
                log("❌ GET /api/posts?scope=community - FAILED: Invalid response structure", "ERROR")
                results.append(("GET /api/posts?scope=community", False, f"Invalid structure: {data}"))
        elif resp.status_code == 401:
            log("❌ GET /api/posts?scope=community - FAILED: Should NOT require auth (got 401)", "ERROR")
            results.append(("GET /api/posts?scope=community", False, "Incorrectly requires auth"))
        else:
            log(f"❌ GET /api/posts?scope=community - FAILED: Status {resp.status_code}", "ERROR")
            results.append(("GET /api/posts?scope=community", False, f"Status {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/posts?scope=community - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/posts?scope=community", False, str(e)))
    
    return results

def test_public_profile_endpoint():
    """Test 5: GET /api/profiles/:uid (public but uid doesn't exist)"""
    log("\n" + "=" * 60)
    log("TEST 5: GET /api/profiles/:uid (Public)")
    log("=" * 60)
    
    results = []
    
    try:
        log("Testing GET /api/profiles/some-fake-uid...")
        resp = requests.get(f"{BASE_URL}/profiles/some-fake-uid", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 404:
            data = resp.json()
            if 'error' in data:
                log("✅ GET /api/profiles/fake-uid - PASSED (404 as expected)", "SUCCESS")
                results.append(("GET /api/profiles/fake-uid", True, "Returns 404 for non-existent uid"))
            else:
                log("❌ GET /api/profiles/fake-uid - FAILED: 404 but no error field", "ERROR")
                results.append(("GET /api/profiles/fake-uid", False, "404 but no error field"))
        else:
            log(f"❌ GET /api/profiles/fake-uid - FAILED: Expected 404, got {resp.status_code}", "ERROR")
            results.append(("GET /api/profiles/fake-uid", False, f"Expected 404, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/profiles/fake-uid - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/profiles/fake-uid", False, str(e)))
    
    return results

def test_protected_endpoints_no_auth():
    """Test 6-11: Protected endpoints without auth (should return 401)"""
    log("\n" + "=" * 60)
    log("TEST 6-11: Protected Endpoints Without Auth")
    log("=" * 60)
    
    results = []
    
    protected_tests = [
        ("GET", "/me", "GET /api/me"),
        ("PATCH", "/me", "PATCH /api/me", {"displayName": "Test"}),
        ("GET", "/posts?scope=mine", "GET /api/posts?scope=mine"),
        ("POST", "/posts", "POST /api/posts", {"title": "Test", "content": "Test"}),
        ("PUT", "/posts/test-id", "PUT /api/posts/test-id", {"title": "Updated"}),
        ("DELETE", "/posts/test-id", "DELETE /api/posts/test-id"),
    ]
    
    for test in protected_tests:
        method = test[0]
        endpoint = test[1]
        name = test[2]
        payload = test[3] if len(test) > 3 else None
        
        try:
            log(f"\nTesting {name} without auth...")
            url = f"{BASE_URL}{endpoint}"
            
            if method == "GET":
                resp = requests.get(url, timeout=5)
            elif method == "POST":
                resp = requests.post(url, json=payload, timeout=5)
            elif method == "PUT":
                resp = requests.put(url, json=payload, timeout=5)
            elif method == "PATCH":
                resp = requests.patch(url, json=payload, timeout=5)
            elif method == "DELETE":
                resp = requests.delete(url, timeout=5)
            
            log(f"Status: {resp.status_code}")
            log(f"Response: {resp.text[:200]}")
            
            if resp.status_code == 401:
                data = resp.json()
                if 'error' in data:
                    log(f"✅ {name} - PASSED (401 as expected)", "SUCCESS")
                    results.append((name, True, "Returns 401 without auth"))
                else:
                    log(f"❌ {name} - FAILED: 401 but no error field", "ERROR")
                    results.append((name, False, "401 but no error field"))
            else:
                log(f"❌ {name} - FAILED: Expected 401, got {resp.status_code}", "ERROR")
                results.append((name, False, f"Expected 401, got {resp.status_code}"))
        except Exception as e:
            log(f"❌ {name} - EXCEPTION: {e}", "ERROR")
            results.append((name, False, str(e)))
    
    return results

def test_invalid_token():
    """Test 12: Protected endpoints with invalid token"""
    log("\n" + "=" * 60)
    log("TEST 12: Protected Endpoints With Invalid Token")
    log("=" * 60)
    
    results = []
    
    headers = {"Authorization": "Bearer notarealtoken.xxx.yyy"}
    
    protected_tests = [
        ("GET", "/me", "GET /api/me with invalid token"),
        ("GET", "/posts?scope=mine", "GET /api/posts?scope=mine with invalid token"),
    ]
    
    for method, endpoint, name in protected_tests:
        try:
            log(f"\nTesting {name}...")
            url = f"{BASE_URL}{endpoint}"
            
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=5)
            
            log(f"Status: {resp.status_code}")
            log(f"Response: {resp.text[:200]}")
            
            if resp.status_code == 401:
                log(f"✅ {name} - PASSED (401 as expected)", "SUCCESS")
                results.append((name, True, "Returns 401 with invalid token"))
            else:
                log(f"❌ {name} - FAILED: Expected 401, got {resp.status_code}", "ERROR")
                results.append((name, False, f"Expected 401, got {resp.status_code}"))
        except Exception as e:
            log(f"❌ {name} - EXCEPTION: {e}", "ERROR")
            results.append((name, False, str(e)))
    
    return results

def test_nonexistent_post():
    """Test 13: GET /api/posts/:id for non-existent post (no auth)"""
    log("\n" + "=" * 60)
    log("TEST 13: GET /api/posts/:id (Non-existent)")
    log("=" * 60)
    
    results = []
    
    try:
        log("Testing GET /api/posts/nonexistent-id without auth...")
        resp = requests.get(f"{BASE_URL}/posts/nonexistent-id-12345", timeout=5)
        log(f"Status: {resp.status_code}")
        log(f"Response: {resp.text[:200]}")
        
        if resp.status_code == 404:
            data = resp.json()
            if 'error' in data:
                log("✅ GET /api/posts/nonexistent-id - PASSED (404 as expected)", "SUCCESS")
                results.append(("GET /api/posts/nonexistent-id", True, "Returns 404 for non-existent post"))
            else:
                log("❌ GET /api/posts/nonexistent-id - FAILED: 404 but no error field", "ERROR")
                results.append(("GET /api/posts/nonexistent-id", False, "404 but no error field"))
        elif resp.status_code == 401:
            log("❌ GET /api/posts/nonexistent-id - FAILED: Should NOT require auth (got 401)", "ERROR")
            results.append(("GET /api/posts/nonexistent-id", False, "Incorrectly requires auth"))
        else:
            log(f"❌ GET /api/posts/nonexistent-id - FAILED: Expected 404, got {resp.status_code}", "ERROR")
            results.append(("GET /api/posts/nonexistent-id", False, f"Expected 404, got {resp.status_code}"))
    except Exception as e:
        log(f"❌ GET /api/posts/nonexistent-id - EXCEPTION: {e}", "ERROR")
        results.append(("GET /api/posts/nonexistent-id", False, str(e)))
    
    return results

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
    log("TANI JOURNAL - PHASE 2 BACKEND TESTS")
    log("=" * 60)
    log(f"Base URL: {BASE_URL}")
    log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_public_health_endpoints())
    all_results.extend(test_upload_endpoint())
    all_results.extend(test_public_posts_endpoint())
    all_results.extend(test_public_profile_endpoint())
    all_results.extend(test_protected_endpoints_no_auth())
    all_results.extend(test_invalid_token())
    all_results.extend(test_nonexistent_post())
    
    # Print summary
    success = print_summary(all_results)
    
    log("\n" + "=" * 60)
    log(f"Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
