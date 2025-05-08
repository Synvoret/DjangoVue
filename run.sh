#!/bin/bash
# set -e # Exit immediately if a command exits with a non-zero status
# run backend
cd back_end
# activate virtual enviroment for python
echo "🔧 Activating Python venv..."
source venv/bin/activate
echo "🧹 Formatting backend code..."
black .
isort .
echo "🔍 Linting backend code..."
flake8 .
echo "🛠 Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo "🚀 Starting Django server..."
python manage.py runserver &


# run frontend
cd ../front_end
npm run lint:py
npm run format:py
echo "🧪 Linting and formatting frontend code..."
npm run check:py
echo "🚀 Starting Vite dev server..."
npm run dev &

# wait for the finish process
wait
