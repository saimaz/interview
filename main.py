#!/usr/bin/env python3
import json
import sqlite3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os
import random
import time

DB_FILE = "chat_messages.db"
PORT = 8000

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_bot_response(user_message):
    responses = [
        "That's an interesting point. Tell me more about it.",
        "I understand what you're saying. How does that make you feel?",
        "Could you elaborate on that thought?",
        "That's a great observation. What led you to that conclusion?",
        "I see. Have you considered other perspectives on this?",
        "Interesting! What would be the ideal outcome for you?",
        "Thank you for sharing that. What aspects are most important to you?",
        "That makes sense. How long have you been thinking about this?",
        "I appreciate your input. What challenges do you foresee?",
        "Good question! Let me think about that for a moment.",
        "Your message has been received and processed successfully.",
        "That's worth exploring further. What specific areas interest you most?",
        "I'm processing your request. Could you provide more context?",
        "Understood. What would you like to focus on next?",
        "Thanks for that information. How can I assist you further?"
    ]

    if "hello" in user_message.lower() or "hi" in user_message.lower():
        return "Hello! How can I assist you today?"
    elif "bye" in user_message.lower() or "goodbye" in user_message.lower():
        return "Goodbye! Have a great day!"
    elif "?" in user_message:
        return random.choice([
            "That's a great question. Let me help you with that.",
            "I'll do my best to answer your question.",
            "Interesting question! Here's what I think...",
            "Let me provide some insights on that."
        ])
    else:
        return random.choice(responses)

class ChatHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/api/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')

                if not message:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': 'Message cannot be empty'}).encode())
                    return

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()

                user_timestamp = datetime.now().isoformat()
                cursor.execute(
                    'INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
                    ('User', message, user_timestamp)
                )
                user_message_id = cursor.lastrowid

                time.sleep(0.5)

                bot_response = generate_bot_response(message)
                bot_timestamp = datetime.now().isoformat()
                cursor.execute(
                    'INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
                    ('Bot', bot_response, bot_timestamp)
                )
                bot_message_id = cursor.lastrowid

                conn.commit()

                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM messages ORDER BY id DESC LIMIT 10'
                )
                rows = cursor.fetchall()
                conn.close()

                messages = []
                for row in rows:
                    messages.append({
                        'id': row['id'],
                        'username': row['username'],
                        'message': row['message'],
                        'timestamp': row['timestamp']
                    })

                messages.reverse()

                self._set_headers(201)
                self.wfile.write(json.dumps({
                    'user_message': {
                        'id': user_message_id,
                        'username': 'User',
                        'message': message,
                        'timestamp': user_timestamp
                    },
                    'bot_response': {
                        'id': bot_message_id,
                        'username': 'Bot',
                        'message': bot_response,
                        'timestamp': bot_timestamp
                    },
                    'messages': messages
                }).encode())

            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_GET(self):
        if self.path == '/api/messages' or self.path.startswith('/api/messages?'):
            try:
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                limit = int(query_params.get('limit', [50])[0])
                offset = int(query_params.get('offset', [0])[0])

                conn = sqlite3.connect(DB_FILE)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM messages ORDER BY id DESC LIMIT ? OFFSET ?',
                    (limit, offset)
                )
                rows = cursor.fetchall()
                conn.close()

                messages = []
                for row in rows:
                    messages.append({
                        'id': row['id'],
                        'username': row['username'],
                        'message': row['message'],
                        'timestamp': row['timestamp']
                    })

                messages.reverse()

                self._set_headers()
                self.wfile.write(json.dumps({'messages': messages}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def log_message(self, format, *args):
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")

def main():
    init_db()
    print(f"Initializing chat backend...")
    print(f"Database: {os.path.abspath(DB_FILE)}")

    with socketserver.TCPServer(("", PORT), ChatHandler) as httpd:
        print(f"\nServer running at http://localhost:{PORT}")
        print("\nEndpoints:")
        print(f"  POST http://localhost:{PORT}/api/message")
        print(f"       Body: {{'message': 'string'}}")
        print(f"  GET  http://localhost:{PORT}/api/messages")
        print(f"       Query params: ?limit=50&offset=0 (optional)")
        print("\nPress Ctrl+C to stop the server")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")

if __name__ == "__main__":
    main()