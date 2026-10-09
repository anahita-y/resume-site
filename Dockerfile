FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# لاتک برای ساخت PDF فارسی (xelatex + xepersian)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      texlive-xetex \
      texlive-lang-other \
      texlive-latex-recommended \
      fontconfig \
 && rm -rf /var/lib/apt/lists/*

# اگه هر کدوم از بسته‌های قالب نصب نشده باشه، همین‌جا بیلد شکست می‌خوره
RUN for f in xepersian.sty bidi.sty fontspec.sty xcolor.sty geometry.sty graphicx.sty; do \
      kpsewhich "$f" || exit 1; \
    done

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN python manage.py collectstatic --noinput

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers 1 --threads 2 --timeout 120"]