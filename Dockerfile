# Sivas Belediyesi Akıllı Şehir Web Portalı
# Django Application Dockerfile
# Python 3.11 Alpine tabanlı, production-ready container

# Build stage
FROM python:3.13-alpine as builder

# Metadata
LABEL maintainer="Sivas Belediyesi Akıllı Şehir Müdürlüğü <akillisehir@sivas.bel.tr>"
LABEL description="Sivas Belediyesi Akıllı Şehir Web Portalı - Django Application"
LABEL version="1.0.0"

# Python optimizasyonları
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Sistem bağımlılıklarını yükle
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt

# Production stage
FROM python:3.13-alpine

# Metadata
LABEL maintainer="Sivas Belediyesi Akıllı Şehir Müdürlüğü <akillisehir@sivas.bel.tr>"
LABEL description="Sivas Belediyesi Akıllı Şehir Web Portalı - Django Application"

# Python optimizasyonları
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/django/.local/bin:$PATH"

# Runtime bağımlılıkları
RUN apk add --no-cache \
    postgresql-client \
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    tk \
    tcl \
    harfbuzz \
    fribidi \
    cairo \
    pango \
    gdk-pixbuf \
    netcat-openbsd \
    su-exec

# Django kullanıcısı oluştur (güvenlik için)
RUN addgroup -g 1000 django && \
    adduser -D -u 1000 -G django django

# Python paketlerini builder'dan kopyala
COPY --from=builder /root/.local /home/django/.local

# Çalışma dizini oluştur
WORKDIR /app

# Uygulama dosyalarını kopyala
COPY --chown=django:django . .

# Static dosyalar için dizin oluştur
RUN mkdir -p /app/staticfiles && \
    chown -R django:django /app/staticfiles

# Media dosyalar için dizin oluştur (MinIO kullanılsa da local backup için)
RUN mkdir -p /app/media && \
    chown -R django:django /app/media

# Log dizini oluştur
RUN mkdir -p /app/logs && \
    chown -R django:django /app/logs

# Entrypoint script'i kopyala
COPY --chown=django:django entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Port açık
EXPOSE 8000

# Kullanıcıyı değiştir
USER django

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD nc -z localhost 8000 || exit 1

# Varsayılan komut
ENTRYPOINT ["/app/entrypoint.sh"]