# Unprivileged nginx: runs as UID 101 and listens on 8080, never as root.
FROM nginxinc/nginx-unprivileged:stable-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY site/ /usr/share/nginx/html/

ARG COMMIT_SHA=local
ARG BUILT_AT=unknown
USER root
RUN printf '{"commit":"%s","built_at":"%s"}\n' "$COMMIT_SHA" "$BUILT_AT" > /usr/share/nginx/html/version.json \
    && chmod -R a+rX,go-w /usr/share/nginx/html
USER 101

LABEL org.opencontainers.image.source="https://github.com/DylanJHrusko/trifffling-site" \
      org.opencontainers.image.revision="$COMMIT_SHA"
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1
