# Playwright REST API
Playwright REST API Docker service for URL screenshot and traffic capture.

## Example of usage
First, start the Playwright container:
```
docker run --rm --name playwright -p 8989:80 ghcr.io/piroguetoolsuite/playwright-rest-api:main
```

Then, capture the given URL, here `https://pts-project.org`:
```
curl -X POST --location "http://localhost:8989/capture" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://pts-project.org\"}" --output out.zip
```

The returned ZIP archive contains:
* `screenshot.png`
* `capture.har`