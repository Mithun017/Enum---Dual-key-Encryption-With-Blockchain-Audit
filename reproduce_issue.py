import httpx
import asyncio

async def test_login(username, password, role, expected_status):
    url = "http://127.0.0.1:8000/auth/login"
    payload = {
        "user": {
            "username": username,
            "role": role
        },
        "password": password
    }
    
    print(f"Testing login for {username} ({role})...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            print(f"Payload: {payload}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == expected_status:
                print("[PASS] Test Passed")
            else:
                print(f"[FAIL] Test Failed (Expected {expected_status})")
    except Exception as e:
        print(f"[ERROR] Connection Error: {e}")
    print("-" * 30)

async def main():
    # 1. Test Correct Admin Login
    await test_login("admin", "password", "ADMIN", 200)

    # 2. Test Correct Mithun Login (Exact Case)
    await test_login("Mithun", "password", "ADMIN", 200)

    # 3. Test Mithun Login (Lowercase - check case sensitivity)
    await test_login("mithun", "password", "ADMIN", 200) # Expect PASS now

    # 4. Test Wrong Password
    await test_login("admin", "wrongpass", "ADMIN", 401)

    # 5. Test Wrong Role
    await test_login("admin", "password", "SERVICE", 403)

if __name__ == "__main__":
    asyncio.run(main())
