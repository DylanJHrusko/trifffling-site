# Dylan's Site — trifffling.com

**Production:** https://trifffling.com
**QA:** https://qa.trifffling.com

A simple containerized website deployed to my own DigitalOcean Droplet with GitHub Actions. Both environments run behind Traefik with Let's Encrypt HTTPS.

## Promotion rule

| Branch | Deploys to | Image tag |
|---|---|---|
| `qa` | QA — https://qa.trifffling.com | `dylanhrusko/trifffling-site:qa` |
| `main` | Production — https://trifffling.com | `dylanhrusko/trifffling-site:prod` |

1. Push a change to the `qa` branch. It deploys to QA only; production is unchanged.
2. After checking QA, open a pull request from `qa` into `main`. The PR runs the same checks but never publishes or deploys.
3. Merging the PR into `main` promotes the change to production.

## How CI/CD works

**Trigger:** any push to `qa` or `main` (and pull requests into `main`, which only run the checks).

**Checks:** `tests/test_site.py` validates the page (title, owner heading, no inline scripts, referenced files exist, nginx hides its version, image runs as non-root). The workflow then builds the Docker image and smoke-tests the running container with a read-only filesystem and no Linux capabilities: it must serve the page, report the exact commit in `/version.json`, hide the nginx version, and not run as root. **Any failed check stops the job before anything is pushed or deployed.**

**Build:** the [`Dockerfile`](Dockerfile) copies the site into the official unprivileged nginx image (UID 101, port 8080) and writes the commit SHA into `/version.json`.

**Delivery:** the tested image is pushed to Docker Hub as `sha-<commit>` plus `:qa` or `:prod`, using the `DOCKER_API_KEY` GitHub Actions secret. On the server, [WUD](https://getwud.app) checks Docker Hub every minute and recreates only the container whose tag changed. The workflow's last step waits until the public site reports the new commit, so a green run means the change is live. GitHub holds no credentials for the server.

## Repository layout

| Path | Purpose |
|---|---|
| `site/` | Website source (HTML, CSS, JS) |
| `nginx/default.conf` | Web server config: security headers, hidden version |
| `Dockerfile` | Image build |
| `tests/test_site.py` | Validation run before every build |
| `.github/workflows/cicd.yml` | CI/CD workflow |
| `deploy/compose.yaml` | Server deployment: QA + production containers and the WUD updater, routed by Traefik |

Image registry: https://hub.docker.com/r/dylanhrusko/trifffling-site/tags

## Test Evidence

_Filled in after the QA → production demonstration._
