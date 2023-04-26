# Playwright REST API
Playwright REST API Docker service for URL screenshot and traffic capture.

## Example of request
```
curl -X POST --location "http://localhost:8989/capture" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://esther.codes\"}" --output out.zip
```