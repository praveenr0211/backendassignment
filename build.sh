#!/bin/bash
set -e

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build completed successfully!"
