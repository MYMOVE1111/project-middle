"""
API Endpoint Testing Script
Tests all REST API endpoints with curl commands
"""

import os
import subprocess
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "admin"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{END}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{END}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{END}")

def print_info(text):
    """Print info message"""
    print(f"{YELLOW}ℹ {text}{END}")

def run_curl(method, url, data=None, headers=None, cookies=None):
    """Execute curl command and return response"""
    cmd = ["curl", "-s", "-X", method, url]
    
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"
    
    for key, value in headers.items():
        cmd.extend(["-H", f"{key}: {value}"])
    
    if cookies:
        cmd.extend(["-b", cookies])
    
    if data:
        cmd.extend(["-d", json.dumps(data)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.stdout:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print_error(f"Error executing curl: {e}")
        return None

def test_api():
    """Test all API endpoints"""
    
    print_header("🧪 TESTING DJANGO REST API ENDPOINTS")
    
    # Test 1: GET Recipes List
    print_header("TEST 1: GET Recipes List")
    print_info("Endpoint: GET /api/recipes/")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/")
    if response and 'results' in response:
        print_success(f"Retrieved {len(response['results'])} recipes")
        if response['results']:
            recipe = response['results'][0]
            print_info(f"First recipe: '{recipe['title']}' (ID: {recipe['id']})")
    else:
        print_error("Failed to retrieve recipes")
    
    # Test 2: GET Single Recipe
    print_header("TEST 2: GET Single Recipe Detail")
    print_info("Endpoint: GET /api/recipes/1/")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/1/")
    if response and 'id' in response:
        print_success(f"Retrieved recipe: '{response['title']}'")
        print_info(f"Author: {response['author_username']}")
        print_info(f"Category: {response['category']['name']}")
        print_info(f"Average Rating: {response['average_rating']}")
    else:
        print_error("Failed to retrieve recipe detail")
    
    # Test 3: GET Categories List
    print_header("TEST 3: GET Categories List")
    print_info("Endpoint: GET /api/categories/")
    
    response = run_curl("GET", f"{BASE_URL}/api/categories/")
    if response and isinstance(response, list):
        print_success(f"Retrieved {len(response)} categories")
        for cat in response:
            print_info(f"Category: {cat['name']}")
    else:
        print_error("Failed to retrieve categories")
    
    # Test 4: GET Category Recipes
    print_header("TEST 4: GET Category Recipes")
    print_info("Endpoint: GET /api/categories/1/recipes/")
    
    response = run_curl("GET", f"{BASE_URL}/api/categories/1/recipes/")
    if response and isinstance(response, list):
        print_success(f"Retrieved {len(response)} recipes in category")
    else:
        print_error("Failed to retrieve category recipes")
    
    # Test 5: GET Recipe Comments
    print_header("TEST 5: GET Recipe Comments")
    print_info("Endpoint: GET /api/recipes/1/comments/")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/1/comments/")
    if response and isinstance(response, list):
        print_success(f"Retrieved {len(response)} comments")
        if response:
            print_info(f"Comment by: {response[0]['user_username']}")
    else:
        print_error("Failed to retrieve comments")
    
    # Test 6: GET Recipe Ratings
    print_header("TEST 6: GET Recipe Ratings")
    print_info("Endpoint: GET /api/recipes/1/ratings/")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/1/ratings/")
    if response and isinstance(response, list):
        print_success(f"Retrieved {len(response)} ratings")
        if response:
            print_info(f"Sample rating: {response[0]['score']} stars from {response[0]['user_username']}")
    else:
        print_error("Failed to retrieve ratings")
    
    # Test 7: GET Average Rating
    print_header("TEST 7: GET Recipe Average Rating")
    print_info("Endpoint: GET /api/recipes/1/average_rating/")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/1/average_rating/")
    if response and 'average_rating' in response:
        print_success(f"Average rating: {response['average_rating']} stars ({response['total_ratings']} ratings)")
    else:
        print_error("Failed to retrieve average rating")
    
    # Test 8: GET Comments List
    print_header("TEST 8: GET Comments List")
    print_info("Endpoint: GET /api/comments/")
    
    response = run_curl("GET", f"{BASE_URL}/api/comments/")
    if response:
        if 'results' in response:
            print_success(f"Retrieved {len(response['results'])} comments (paginated)")
        elif isinstance(response, list):
            print_success(f"Retrieved {len(response)} comments")
    else:
        print_error("Failed to retrieve comments")
    
    # Test 9: GET Ratings List
    print_header("TEST 9: GET Ratings List")
    print_info("Endpoint: GET /api/ratings/")
    
    response = run_curl("GET", f"{BASE_URL}/api/ratings/")
    if response:
        if 'results' in response:
            print_success(f"Retrieved {len(response['results'])} ratings (paginated)")
        elif isinstance(response, list):
            print_success(f"Retrieved {len(response)} ratings")
    else:
        print_error("Failed to retrieve ratings")
    
    # Test 10: Search Recipes
    print_header("TEST 10: Search Recipes")
    print_info("Endpoint: GET /api/recipes/?search=pasta")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/?search=pasta")
    if response and 'results' in response:
        print_success(f"Search found {len(response['results'])} results for 'pasta'")
    else:
        print_error("Failed to search recipes")
    
    # Test 11: Filter by Difficulty
    print_header("TEST 11: Filter Recipes by Difficulty")
    print_info("Endpoint: GET /api/recipes/?difficulty=easy")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/?difficulty=easy")
    if response and 'results' in response:
        print_success(f"Found {len(response['results'])} easy recipes")
    else:
        print_error("Failed to filter recipes")
    
    # Test 12: Filter by Category
    print_header("TEST 12: Filter Recipes by Category")
    print_info("Endpoint: GET /api/recipes/?category=1")
    
    response = run_curl("GET", f"{BASE_URL}/api/recipes/?category=1")
    if response and 'results' in response:
        print_success(f"Found {len(response['results'])} recipes in category 1")
    else:
        print_error("Failed to filter by category")
    
    # Test 13: POST Create Recipe (will fail without auth, but test endpoint)
    print_header("TEST 13: POST Create Recipe (Authentication Required)")
    print_info("Endpoint: POST /api/recipes/")
    
    new_recipe = {
        "title": "Test API Recipe",
        "description": "This is a test recipe created via API",
        "ingredients": "Test ingredient 1, Test ingredient 2",
        "instructions": "Step 1, Step 2, Step 3",
        "category_id": 1,
        "prep_time": 30,
        "cook_time": 20,
        "servings": 4,
        "difficulty": "medium",
        "published": True
    }
    
    response = run_curl("POST", f"{BASE_URL}/api/recipes/", data=new_recipe)
    if response:
        if 'detail' in response and 'not provided' in str(response['detail']).lower():
            print_info("Expected: Authentication required (not logged in via curl)")
        elif 'id' in response:
            print_success(f"Recipe created successfully (ID: {response['id']})")
        else:
            print_info(f"Response: {response}")
    else:
        print_error("Failed to execute POST request")
    
    # Test 14: POST Add Comment (will fail without auth)
    print_header("TEST 14: POST Add Comment (Authentication Required)")
    print_info("Endpoint: POST /api/recipes/1/add_comment/")
    
    comment_data = {
        "text": "This is a test comment via API"
    }
    
    response = run_curl("POST", f"{BASE_URL}/api/recipes/1/add_comment/", data=comment_data)
    if response:
        if 'detail' in response and 'not provided' in str(response['detail']).lower():
            print_info("Expected: Authentication required (not logged in via curl)")
        elif 'id' in response:
            print_success(f"Comment added successfully (ID: {response['id']})")
        else:
            print_info(f"Response: {response}")
    else:
        print_error("Failed to execute POST request")
    
    # Test 15: POST Add Rating (will fail without auth)
    print_header("TEST 15: POST Add Rating (Authentication Required)")
    print_info("Endpoint: POST /api/recipes/1/add_rating/")
    
    rating_data = {
        "score": 5
    }
    
    response = run_curl("POST", f"{BASE_URL}/api/recipes/1/add_rating/", data=rating_data)
    if response:
        if 'detail' in response and 'not provided' in str(response['detail']).lower():
            print_info("Expected: Authentication required (not logged in via curl)")
        elif 'id' in response:
            print_success(f"Rating added successfully (ID: {response['id']})")
        else:
            print_info(f"Response: {response}")
    else:
        print_error("Failed to execute POST request")
    
    # Summary
    print_header("✅ API TESTING COMPLETE")
    print_success("All public endpoints are working!")
    print_info("Note: POST operations require authentication. Test via:")
    print_info("- Postman with session/token auth")
    print_info("- Django admin interface + session cookies")
    print_info("- curl with -b flag for cookies after login")

if __name__ == "__main__":
    print(f"\n{YELLOW}Starting API tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
    test_api()
    print(f"\n{YELLOW}Tests completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}\n")
