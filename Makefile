.PHONY: start backend frontend check-tools setup-venv kill-port

# defaults ports
DJANGO_PORT ?= 8000
VITE_PORT ?= 5173

start: check-tools backend frontend
	@wait

check-tools:
	@command -v python3 >/dev/null || (echo "❌ python3 not found." && exit 1)
	@command -v npm >/dev/null || (echo "❌ npm not found." && exit 1)

backend: setup-venv
	@echo "🔍 Checking Django port $(DJANGO_PORT)..."
	@$(MAKE) kill-port PORT=$(DJANGO_PORT)
	cd back_end && \
	echo "🧹 Formatting backend..." && \
	venv/bin/black . && \
	venv/bin/isort . && \
	echo "🔍 Linting backend..." && \
	venv/bin/flake8 . && \
	echo "🛠 Running migrations..." && \
	venv/bin/python manage.py makemigrations && \
	venv/bin/python manage.py migrate && \
	venv/bin/python manage.py shell < scripts/create_superuser.py && \
	echo "🚀 Starting Django on port $(DJANGO_PORT)..." && \
	venv/bin/python manage.py runserver 0.0.0.0:$(DJANGO_PORT) &

setup-venv:
	@if [ ! -d "back_end/venv" ]; then \
		echo "⚙️  Creating virtual environment..."; \
		python3 -m venv back_end/venv; \
		echo "📦 Installing Python dependencies..."; \
		back_end/venv/bin/pip install --upgrade pip; \
		back_end/venv/bin/pip install -r back_end/requirements.txt; \
	else \
		echo "✅ Python virtual environment already exists."; \
	fi

frontend:
	@echo "🔍 Checking Vite port $(VITE_PORT)..."
	@$(MAKE) kill-port PORT=$(VITE_PORT)
	cd front_end && \
	if [ ! -d "node_modules" ]; then \
		echo "📦 Installing Node.js dependencies..."; \
		npm install; \
	else \
		echo "✅ Node.js dependencies already installed."; \
	fi && \
	echo "🚀 Starting Vite on port $(VITE_PORT)..." && \
	npm run dev -- --port=$(VITE_PORT)

kill-port:
	@if lsof -i :$(PORT) >/dev/null; then \
		echo "⚠️  Port $(PORT) is in use. Killing process..."; \
		fuser -k $(PORT)/tcp; \
	else \
		echo "✅ Port $(PORT) is free."; \
	fi
