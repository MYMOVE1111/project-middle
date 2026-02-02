#!/usr/bin/env python
"""Quick API Test Script"""
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    """Test API endpoints"""
    print("\n" + "="*60)
    print("TESTING RECIPE SHARING API")
    print("="*60 + "\n")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test 1: GET Recipes
    print("\n✓ TEST 1: GET /api/recipes/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        print(f"  ✓ Total recipes: {data.get('count', 0)}")
        if data.get('results'):
            print(f"  ✓ First recipe: {data['results'][0]['title']}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 2: GET Categories
    print("\n✓ TEST 2: GET /api/categories/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/categories/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        if isinstance(data, list):
            print(f"  ✓ Total categories: {len(data)}")
            if data:
                print(f"  ✓ First category: {data[0]['name']}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 3: GET Single Recipe
    print("\n✓ TEST 3: GET /api/recipes/1/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/1/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        print(f"  ✓ Recipe: {data['title']}")
        print(f"  ✓ Author: {data['author_username']}")
        print(f"  ✓ Average Rating: {data['average_rating']}")
        print(f"  ✓ Comments: {data['comments_count']}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 4: GET Recipe Comments
    print("\n✓ TEST 4: GET /api/recipes/1/comments/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/1/comments/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        if isinstance(data, list):
            print(f"  ✓ Total comments: {len(data)}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 5: GET Recipe Ratings
    print("\n✓ TEST 5: GET /api/recipes/1/ratings/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/1/ratings/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        if isinstance(data, list):
            print(f"  ✓ Total ratings: {len(data)}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 6: GET Recipe Average Rating
    print("\n✓ TEST 6: GET /api/recipes/1/average_rating/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/1/average_rating/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        print(f"  ✓ Average Rating: {data['average_rating']} stars ({data['total_ratings']} ratings)")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 7: GET Comments List
    print("\n✓ TEST 7: GET /api/comments/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/comments/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        if 'results' in data:
            print(f"  ✓ Total comments: {data.get('count', 0)}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 8: GET Ratings List
    print("\n✓ TEST 8: GET /api/ratings/")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/ratings/")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        if 'results' in data:
            print(f"  ✓ Total ratings: {data.get('count', 0)}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 9: Search Recipes
    print("\n✓ TEST 9: GET /api/recipes/?search=pasta")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/?search=pasta")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        print(f"  ✓ Results found: {len(data.get('results', []))}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    # Test 10: Filter by Difficulty
    print("\n✓ TEST 10: GET /api/recipes/?difficulty=easy")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/api/recipes/?difficulty=easy")
        data = json.loads(response.read().decode())
        print(f"  ✓ Status: {response.status}")
        print(f"  ✓ Easy recipes: {len(data.get('results', []))}")
    except urllib.error.URLError as e:
        print(f"  ✗ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ API TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_api()
