#!/usr/bin/env python3
"""
Simple Mock Counter API for Cloud Resume Challenge

This is a lightweight Flask server that provides a mock visitor counter API.
It maintains an in-memory counter that increments with each POST request.

Usage:
    python mock_counter_api.py

The API will be available at: http://localhost:5000/api/visitor-count
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# In-memory counter (resets when server restarts)
visitor_count = 0


@app.route('/api/visitor-count', methods=['POST'])
def increment_visitor_count():
    """
    Increment and return the visitor count

    Returns:
        JSON response with the current count
    """
    global visitor_count
    visitor_count += 1

    return jsonify({
        'count': visitor_count,
        'message': 'Counter incremented successfully'
    }), 200


@app.route('/api/visitor-count', methods=['GET'])
def get_visitor_count():
    """
    Get the current visitor count without incrementing

    Returns:
        JSON response with the current count
    """
    return jsonify({
        'count': visitor_count,
        'message': 'Current count retrieved'
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint

    Returns:
        JSON response indicating the API is running
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Mock Counter API is running'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint with API information
    """
    return jsonify({
        'name': 'Mock Counter API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/visitor-count': 'Increment and get visitor count',
            'GET /api/visitor-count': 'Get current visitor count',
            'GET /api/health': 'Health check'
        }
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'

    print(f"Starting Mock Counter API on port {port}")
    print(f"API endpoint: http://localhost:{port}/api/visitor-count")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
