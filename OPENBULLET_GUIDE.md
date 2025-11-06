# OpenBullet 2 Config Creation Guide

## Using SUSH to Create OpenBullet 2 Configs

This guide explains how to use the captured network traffic from SUSH to create OpenBullet 2 configurations.

### What SUSH Captures

When you analyze a login page with SUSH, it captures:

1. **Request URL** - The endpoint where login data is sent
2. **Request Method** - Usually POST for login forms
3. **Request Headers** - Important headers like:
   - User-Agent
   - Content-Type
   - Referer
   - Origin
   - Cookie (session cookies, CSRF tokens)
4. **POST Data** - The format of credentials and other parameters:
   - Username/email field name
   - Password field name
   - CSRF tokens
   - Hidden form fields
   - Additional parameters
5. **Response Data** - To identify success/failure:
   - Status codes
   - Response headers (Set-Cookie, Location for redirects)
   - Response body patterns

### Steps to Create Config

#### 1. Analyze the Login Page
```bash
python sush_tool.py
```
Enter the login URL and click ANALYZE.

#### 2. Perform the Login
In the browser window that opens, perform a real login with test credentials.

#### 3. Find the Login Request
In the captured traffic, look for:
- POST request to login/signin/auth endpoint
- Check the Request Body section for the data format

Example captured POST data:
```
username=testuser&password=testpass&csrf_token=abc123&remember=1
```

#### 4. Identify Success/Failure Patterns
Look at the response to identify:
- Success: Status 200, redirect (302), specific text in response
- Failure: Status 401, error message in response

#### 5. Create OpenBullet 2 Config

Use the captured information:

**Request Block:**
- URL: From captured request URL
- Method: POST
- Headers: Copy important headers from captured data
- POST Data: Use the parameter names from captured body
  - Replace actual values with `<INPUT>` and `<PASS>` variables

**Parse Block:**
- Add conditions to check for success/failure patterns
- Look for specific text, status codes, or headers

**Example Config Structure:**
```
REQUEST POST https://example.com/api/login
  HEADER "User-Agent" "Mozilla/5.0..."
  HEADER "Content-Type" "application/x-www-form-urlencoded"
  CONTENT "username=<INPUT>&password=<PASS>&csrf_token=<CSRF>"
  
PARSE
  LR "<csrf_token>" "value=\"" "\"" -> VAR "CSRF"
  
KEYCHECK
  SUCCESS KEY "<div>Welcome"
  FAIL KEY "Invalid credentials"
```

### Common Patterns

#### Pattern 1: Simple POST with Username/Password
```
POST /login
Content-Type: application/x-www-form-urlencoded

username=<INPUT>&password=<PASS>
```

#### Pattern 2: JSON API Login
```
POST /api/auth/login
Content-Type: application/json

{"username":"<INPUT>","password":"<PASS>"}
```

#### Pattern 3: Login with CSRF Token
```
1. GET /login (capture CSRF token from page)
2. POST /login with token
   csrf_token=<CSRF>&username=<INPUT>&password=<PASS>
```

#### Pattern 4: Multi-step Login
```
1. POST /check-username (validate username exists)
2. POST /authenticate (send password)
```

### Tips

- **Always test with dummy credentials first**
- Look for hidden fields in the POST data
- Check if cookies from previous requests are needed
- Some sites require specific headers (Referer, Origin)
- Watch for rate limiting or captcha requirements
- Check if the login uses JavaScript/AJAX (Content-Type: application/json)

### Troubleshooting

**Issue**: No POST request captured
- Solution: Make sure you actually submit the login form in the browser

**Issue**: Too many requests captured
- Solution: Filter by looking for POST methods to auth/login endpoints

**Issue**: Can't find credentials in POST data
- Solution: Check if the site uses JSON format or base64 encoding

**Issue**: Success pattern unclear
- Solution: Look for redirects (302), Set-Cookie headers, or specific success messages

### Security Note

⚠️ **IMPORTANT**: This tool is for educational purposes and testing your own applications. Always:
- Get permission before testing third-party websites
- Use dummy/test credentials only
- Respect rate limits and terms of service
- Don't use for malicious purposes

### Additional Resources

- OpenBullet 2 Documentation: https://openbullet2.github.io/
- HTTP methods and headers: MDN Web Docs
- Understanding CSRF tokens and session management

---

Made with ❤️ and lots of ☕ by the SUSH team
