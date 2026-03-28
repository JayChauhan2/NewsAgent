import sys
import os

# Add the project root to sys.path so we can import from 'backend'
# This path is relative to the Vercel execution context
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api import app

# This is the entry point for Vercel
# Vercel will look for 'app' in this module
