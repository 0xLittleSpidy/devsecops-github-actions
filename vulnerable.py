"""
VULNERABLE APP - FOR SECURITY TESTING ONLY
This code contains intentional security flaws for educational purposes
"""

import os
import pickle
import subprocess
import sqlite3
from flask import Flask, request, render_template_string

# ============================================
# VULNERABILITY 1: Hard-coded Secrets
# ============================================
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "admin123"
API_KEY = "sk_live_51H9xMEKkPaDeUfMC8zqMN9vY7R"
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890ABCDEFGHIJKLMNOP
-----END RSA PRIVATE KEY-----"""

# ============================================
# VULNERABILITY 2: SQL Injection
# ============================================
def get_user_by_id(user_id):
    """Vulnerable to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # BAD: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    return cursor.fetchone()

def login(username, password):
    """Another SQL injection vulnerability"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # BAD: User input directly in query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    return cursor.fetchone()

# ============================================
# VULNERABILITY 3: Command Injection
# ============================================
def ping_server(host):
    """Vulnerable to command injection"""
    # BAD: User input in shell command
    command = f"ping -c 4 {host}"
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout

def process_file(filename):
    """Another command injection"""
    # BAD: Using os.system with user input
    os.system(f"cat {filename}")

# ============================================
# VULNERABILITY 4: Path Traversal
# ============================================
def read_file(filename):
    """Vulnerable to path traversal"""
    # BAD: No validation of filename
    with open(f"/var/www/uploads/{filename}", 'r') as f:
        return f.read()

# ============================================
# VULNERABILITY 5: Insecure Deserialization
# ============================================
def load_user_data(data):
    """Vulnerable to pickle deserialization attacks"""
    # BAD: Never unpickle untrusted data
    user_obj = pickle.loads(data)
    return user_obj

# ============================================
# VULNERABILITY 6: XSS (Cross-Site Scripting)
# ============================================
app = Flask(__name__)

@app.route('/search')
def search():
    """Vulnerable to XSS"""
    query = request.args.get('q', '')
    
    # BAD: Rendering user input without escaping
    template = f"""
    <html>
        <body>
            <h1>Search Results for: {query}</h1>
        </body>
    </html>
    """
    return render_template_string(template)

# ============================================
# VULNERABILITY 7: Weak Cryptography
# ============================================
import hashlib

def hash_password(password):
    """Using weak/broken hash algorithm"""
    # BAD: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data(data):
    """Insecure encryption"""
    # BAD: Simple XOR "encryption"
    key = 42
    return ''.join(chr(ord(c) ^ key) for c in data)

# ============================================
# VULNERABILITY 8: Insecure Random
# ============================================
import random

def generate_session_token():
    """Using insecure random for security tokens"""
    # BAD: random module is not cryptographically secure
    return ''.join(random.choices('0123456789abcdef', k=32))

def generate_password_reset_token():
    """Predictable token generation"""
    # BAD: Time-based "random" token
    import time
    return str(int(time.time()))

# ============================================
# VULNERABILITY 9: Information Disclosure
# ============================================
def get_user_profile(user_id):
    """Exposing sensitive information"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
        return user
    except Exception as e:
        # BAD: Exposing full stack traces to users
        return f"Error: {str(e)}\n{traceback.format_exc()}"

# ============================================
# VULNERABILITY 10: Unsafe YAML Loading
# ============================================
import yaml

def load_config(config_string):
    """Vulnerable to YAML deserialization"""
    # BAD: yaml.load() without safe_load
    config = yaml.load(config_string)
    return config

# ============================================
# VULNERABILITY 11: SSRF (Server-Side Request Forgery)
# ============================================
import requests

def fetch_url(url):
    """Vulnerable to SSRF"""
    # BAD: Fetching arbitrary URLs without validation
    response = requests.get(url)
    return response.text

# ============================================
# VULNERABILITY 12: Insecure File Upload
# ============================================
@app.route('/upload', methods=['POST'])
def upload_file():
    """Vulnerable file upload"""
    file = request.files['file']
    
    # BAD: No validation of file type or content
    filename = file.filename
    file.save(f"/var/www/uploads/{filename}")
    
    return "File uploaded successfully"

# ============================================
# VULNERABILITY 13: Debug Mode in Production
# ============================================
if __name__ == '__main__':
    # BAD: Running Flask in debug mode
    app.run(debug=True, host='0.0.0.0')

# ============================================
# VULNERABILITY 14: Hardcoded Credentials in Connection Strings
# ============================================
DATABASE_URL = "postgresql://admin:password123@prod-db.example.com:5432/maindb"
REDIS_URL = "redis://:supersecret@redis.example.com:6379/0"
MONGO_CONNECTION = "mongodb://dbuser:dbpass123@mongodb.example.com:27017/production"

# ============================================
# VULNERABILITY 15: Exposed API Keys
# ============================================
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuv"
STRIPE_SECRET_KEY = "sk_live_51H9xMEKkPaDeUfMC8zqMN9vY7R"
SENDGRID_API_KEY = "SG.1234567890abcdefghijklmnop.qrstuvwxyz1234567890ABCDEFGHIJKLMNOP"
