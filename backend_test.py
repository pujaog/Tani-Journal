#!/usr/bin/env python3
"""
Backend API tests for The Tani Journal - Phase 1
Tests all CRUD endpoints, health checks, and upload functionality
"""
import requests
import json
import time
from datetime import datetime

# Base URL from .env NEXT_PUBLIC_BASE_URL
BASE_URL = "https://journal-media-hub.preview.emergentagent.com/api"

def log_test(test_name, passed, details=""):
    """Log test results"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {test_name}")
    if details:
        print(f"  Details: {details}")
    return passed

def test_health_endpoints():
    """Test GET /api and GET /api/health"""
    print("\n" + "="*60)
    print("Testing Health Endpoints")
    print("="*60)
    
    all_passed = True
    
    # Test GET /api
    try:
        response = requests.get(f"{BASE_URL}", timeout=10)
        data = response.json()
        
        passed = (
            response.status_code == 200 and
            data.get('status') == 'ok' and
            data.get('service') == 'tani-journal' and
            'time' in data
        )
        all_passed &= log_test(
            "GET /api returns health status",
            passed,
            f"Status: {response.status_code}, Data: {data}"
        )
    except Exception as e:
        all_passed &= log_test("GET /api returns health status", False, str(e))
    
    # Test GET /api/health
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        data = response.json()
        
        passed = (
            response.status_code == 200 and
            data.get('status') == 'ok' and
            data.get('service') == 'tani-journal' and
            'time' in data
        )
        all_passed &= log_test(
            "GET /api/health returns health status",
            passed,
            f"Status: {response.status_code}, Data: {data}"
        )
    except Exception as e:
        all_passed &= log_test("GET /api/health returns health status", False, str(e))
    
    return all_passed

def test_upload_endpoint():
    """Test POST /api/upload"""
    print("\n" + "="*60)
    print("Testing Upload Endpoint")
    print("="*60)
    
    all_passed = True
    
    # Test with valid dataUrl
    try:
        sample_data_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        response = requests.post(
            f"{BASE_URL}/upload",
            json={"dataUrl": sample_data_url},
            timeout=10
        )
        data = response.json()
        
        passed = (
            response.status_code == 200 and
            data.get('url') == sample_data_url
        )
        all_passed &= log_test(
            "POST /api/upload echoes back dataUrl",
            passed,
            f"Status: {response.status_code}, URL matches: {data.get('url') == sample_data_url}"
        )
    except Exception as e:
        all_passed &= log_test("POST /api/upload echoes back dataUrl", False, str(e))
    
    # Test without dataUrl (should return 400)
    try:
        response = requests.post(
            f"{BASE_URL}/upload",
            json={},
            timeout=10
        )
        data = response.json()
        
        passed = response.status_code == 400 and 'error' in data
        all_passed &= log_test(
            "POST /api/upload without dataUrl returns 400",
            passed,
            f"Status: {response.status_code}, Data: {data}"
        )
    except Exception as e:
        all_passed &= log_test("POST /api/upload without dataUrl returns 400", False, str(e))
    
    return all_passed

def test_posts_crud():
    """Test full CRUD operations for posts"""
    print("\n" + "="*60)
    print("Testing Posts CRUD Operations")
    print("="*60)
    
    all_passed = True
    created_post_ids = []
    
    # 1. Test GET /api/posts (initially might be empty or have existing posts)
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=10)
        data = response.json()
        
        passed = (
            response.status_code == 200 and
            'posts' in data and
            isinstance(data['posts'], list)
        )
        initial_count = len(data['posts'])
        all_passed &= log_test(
            "GET /api/posts returns posts array",
            passed,
            f"Status: {response.status_code}, Initial posts count: {initial_count}"
        )
    except Exception as e:
        all_passed &= log_test("GET /api/posts returns posts array", False, str(e))
        return all_passed
    
    # 2. Test POST /api/posts - Create post with 16:9 images
    try:
        new_post = {
            "title": "My First Day at the Beach",
            "content": "Today was absolutely magical. The waves were gentle, the sun was warm, and I felt completely at peace. I spent hours just walking along the shore, collecting shells and watching the seabirds. This is exactly what I needed.",
            "mood": "peaceful",
            "images": [
                {
                    "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k=",
                    "aspectRatio": "16:9"
                },
                {
                    "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k=",
                    "aspectRatio": "16:9"
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/posts",
            json=new_post,
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 201 and 'post' in data:
            post = data['post']
            created_post_ids.append(post.get('id'))
            
            # Verify post structure
            passed = (
                'id' in post and
                '_id' not in post and  # No Mongo _id leak
                post.get('title') == new_post['title'] and
                post.get('content') == new_post['content'] and
                post.get('mood') == new_post['mood'] and
                'createdAt' in post and
                'updatedAt' in post and
                len(post.get('images', [])) == 2 and
                all(img.get('aspectRatio') == '16:9' for img in post.get('images', []))
            )
            
            # Check if id is UUID format
            post_id = post.get('id', '')
            is_uuid = len(post_id.split('-')) == 5
            
            all_passed &= log_test(
                "POST /api/posts creates post with UUID and 16:9 images",
                passed and is_uuid,
                f"Status: {response.status_code}, ID: {post_id}, Images: {len(post.get('images', []))}"
            )
        else:
            all_passed &= log_test(
                "POST /api/posts creates post with UUID and 16:9 images",
                False,
                f"Status: {response.status_code}, Data: {data}"
            )
    except Exception as e:
        all_passed &= log_test("POST /api/posts creates post with UUID and 16:9 images", False, str(e))
    
    # 3. Test POST /api/posts - Create post with 3:4 images
    try:
        new_post_34 = {
            "title": "Morning Coffee Ritual",
            "content": "There's something deeply satisfying about the morning coffee ritual. The aroma, the warmth of the cup, the first sip. It's my daily meditation.",
            "mood": "content",
            "images": [
                {
                    "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k=",
                    "aspectRatio": "3:4"
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/posts",
            json=new_post_34,
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 201 and 'post' in data:
            post = data['post']
            created_post_ids.append(post.get('id'))
            
            passed = (
                len(post.get('images', [])) == 1 and
                post['images'][0].get('aspectRatio') == '3:4'
            )
            all_passed &= log_test(
                "POST /api/posts creates post with 3:4 aspect ratio",
                passed,
                f"Status: {response.status_code}, AspectRatio: {post['images'][0].get('aspectRatio')}"
            )
        else:
            all_passed &= log_test(
                "POST /api/posts creates post with 3:4 aspect ratio",
                False,
                f"Status: {response.status_code}"
            )
    except Exception as e:
        all_passed &= log_test("POST /api/posts creates post with 3:4 aspect ratio", False, str(e))
    
    # 4. Test POST /api/posts - Invalid aspect ratio defaults to 16:9
    try:
        new_post_invalid = {
            "title": "Testing Invalid Aspect Ratio",
            "content": "This post tests that invalid aspect ratios default to 16:9",
            "mood": "curious",
            "images": [
                {
                    "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k=",
                    "aspectRatio": "1:1"  # Invalid - should default to 16:9
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/posts",
            json=new_post_invalid,
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 201 and 'post' in data:
            post = data['post']
            created_post_ids.append(post.get('id'))
            
            passed = (
                len(post.get('images', [])) == 1 and
                post['images'][0].get('aspectRatio') == '16:9'
            )
            all_passed &= log_test(
                "POST /api/posts defaults invalid aspect ratio to 16:9",
                passed,
                f"Status: {response.status_code}, AspectRatio: {post['images'][0].get('aspectRatio')}"
            )
        else:
            all_passed &= log_test(
                "POST /api/posts defaults invalid aspect ratio to 16:9",
                False,
                f"Status: {response.status_code}"
            )
    except Exception as e:
        all_passed &= log_test("POST /api/posts defaults invalid aspect ratio to 16:9", False, str(e))
    
    # 5. Test POST /api/posts - Images capped to 6
    try:
        new_post_many_images = {
            "title": "Testing Image Limit",
            "content": "This post has more than 6 images to test the cap",
            "mood": "experimental",
            "images": [{"url": f"data:image/jpeg;base64,test{i}", "aspectRatio": "16:9"} for i in range(10)]
        }
        
        response = requests.post(
            f"{BASE_URL}/posts",
            json=new_post_many_images,
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 201 and 'post' in data:
            post = data['post']
            created_post_ids.append(post.get('id'))
            
            passed = len(post.get('images', [])) == 6
            all_passed &= log_test(
                "POST /api/posts caps images to 6",
                passed,
                f"Status: {response.status_code}, Images count: {len(post.get('images', []))}"
            )
        else:
            all_passed &= log_test(
                "POST /api/posts caps images to 6",
                False,
                f"Status: {response.status_code}"
            )
    except Exception as e:
        all_passed &= log_test("POST /api/posts caps images to 6", False, str(e))
    
    # Wait a moment to ensure different timestamps
    time.sleep(0.1)
    
    # 6. Test GET /api/posts - Verify sorting (newest first)
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=10)
        data = response.json()
        
        if response.status_code == 200 and 'posts' in data:
            posts = data['posts']
            
            # Check that we have more posts now
            passed = len(posts) >= len(created_post_ids)
            
            # Verify sorting - createdAt should be descending
            if len(posts) >= 2:
                dates_sorted = all(
                    posts[i]['createdAt'] >= posts[i+1]['createdAt']
                    for i in range(len(posts)-1)
                )
                passed = passed and dates_sorted
            
            # Verify no _id in responses
            no_mongo_id = all('_id' not in post for post in posts)
            passed = passed and no_mongo_id
            
            all_passed &= log_test(
                "GET /api/posts returns sorted posts (newest first) without _id",
                passed,
                f"Status: {response.status_code}, Posts count: {len(posts)}, Sorted: {dates_sorted if len(posts) >= 2 else 'N/A'}"
            )
        else:
            all_passed &= log_test(
                "GET /api/posts returns sorted posts (newest first) without _id",
                False,
                f"Status: {response.status_code}"
            )
    except Exception as e:
        all_passed &= log_test("GET /api/posts returns sorted posts (newest first) without _id", False, str(e))
    
    # 7. Test GET /api/posts/:id
    if created_post_ids:
        try:
            test_id = created_post_ids[0]
            response = requests.get(f"{BASE_URL}/posts/{test_id}", timeout=10)
            data = response.json()
            
            passed = (
                response.status_code == 200 and
                'post' in data and
                data['post'].get('id') == test_id and
                '_id' not in data['post']
            )
            all_passed &= log_test(
                "GET /api/posts/:id returns specific post",
                passed,
                f"Status: {response.status_code}, ID matches: {data.get('post', {}).get('id') == test_id}"
            )
        except Exception as e:
            all_passed &= log_test("GET /api/posts/:id returns specific post", False, str(e))
    
    # 8. Test GET /api/posts/:id with invalid ID (should return 404)
    try:
        response = requests.get(f"{BASE_URL}/posts/invalid-uuid-12345", timeout=10)
        data = response.json()
        
        passed = response.status_code == 404 and 'error' in data
        all_passed &= log_test(
            "GET /api/posts/:id returns 404 for unknown ID",
            passed,
            f"Status: {response.status_code}, Data: {data}"
        )
    except Exception as e:
        all_passed &= log_test("GET /api/posts/:id returns 404 for unknown ID", False, str(e))
    
    # 9. Test PUT /api/posts/:id - Partial update (only title)
    if created_post_ids:
        try:
            test_id = created_post_ids[0]
            update_data = {
                "title": "Updated: My First Day at the Beach (Evening Reflection)"
            }
            
            response = requests.put(
                f"{BASE_URL}/posts/{test_id}",
                json=update_data,
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200 and 'post' in data:
                post = data['post']
                passed = (
                    post.get('id') == test_id and
                    post.get('title') == update_data['title'] and
                    post.get('updatedAt') > post.get('createdAt') and
                    '_id' not in post
                )
                all_passed &= log_test(
                    "PUT /api/posts/:id updates title and bumps updatedAt",
                    passed,
                    f"Status: {response.status_code}, Title updated: {post.get('title') == update_data['title']}"
                )
            else:
                all_passed &= log_test(
                    "PUT /api/posts/:id updates title and bumps updatedAt",
                    False,
                    f"Status: {response.status_code}"
                )
        except Exception as e:
            all_passed &= log_test("PUT /api/posts/:id updates title and bumps updatedAt", False, str(e))
    
    # 10. Test PUT /api/posts/:id - Update images only
    if len(created_post_ids) >= 2:
        try:
            test_id = created_post_ids[1]
            update_data = {
                "images": [
                    {
                        "url": "data:image/jpeg;base64,updated_image",
                        "aspectRatio": "16:9"
                    }
                ]
            }
            
            response = requests.put(
                f"{BASE_URL}/posts/{test_id}",
                json=update_data,
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200 and 'post' in data:
                post = data['post']
                passed = (
                    len(post.get('images', [])) == 1 and
                    post['images'][0].get('url') == update_data['images'][0]['url']
                )
                all_passed &= log_test(
                    "PUT /api/posts/:id updates images only",
                    passed,
                    f"Status: {response.status_code}, Images updated: {len(post.get('images', []))}"
                )
            else:
                all_passed &= log_test(
                    "PUT /api/posts/:id updates images only",
                    False,
                    f"Status: {response.status_code}"
                )
        except Exception as e:
            all_passed &= log_test("PUT /api/posts/:id updates images only", False, str(e))
    
    # 11. Test DELETE /api/posts/:id
    if len(created_post_ids) >= 3:
        try:
            test_id = created_post_ids[2]
            response = requests.delete(f"{BASE_URL}/posts/{test_id}", timeout=10)
            data = response.json()
            
            passed = response.status_code == 200 and data.get('ok') == True
            all_passed &= log_test(
                "DELETE /api/posts/:id returns ok: true",
                passed,
                f"Status: {response.status_code}, Data: {data}"
            )
            
            # Verify post is actually deleted
            if passed:
                verify_response = requests.get(f"{BASE_URL}/posts/{test_id}", timeout=10)
                verify_passed = verify_response.status_code == 404
                all_passed &= log_test(
                    "DELETE /api/posts/:id actually deletes post (GET returns 404)",
                    verify_passed,
                    f"Verify status: {verify_response.status_code}"
                )
        except Exception as e:
            all_passed &= log_test("DELETE /api/posts/:id returns ok: true", False, str(e))
    
    # 12. Test DELETE /api/posts/:id with invalid ID (should return 404)
    try:
        response = requests.delete(f"{BASE_URL}/posts/invalid-uuid-99999", timeout=10)
        data = response.json()
        
        passed = response.status_code == 404 and 'error' in data
        all_passed &= log_test(
            "DELETE /api/posts/:id returns 404 for unknown ID",
            passed,
            f"Status: {response.status_code}, Data: {data}"
        )
    except Exception as e:
        all_passed &= log_test("DELETE /api/posts/:id returns 404 for unknown ID", False, str(e))
    
    return all_passed

def main():
    """Run all backend tests"""
    print("\n" + "="*60)
    print("THE TANI JOURNAL - PHASE 1 BACKEND API TESTS")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test started at: {datetime.now().isoformat()}")
    
    results = {
        "health": test_health_endpoints(),
        "upload": test_upload_endpoint(),
        "posts_crud": test_posts_crud()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
