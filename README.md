<div align="center">
<img width="60px" src="https://pts-project.org/android-chrome-512x512.png">
<h1>Playwright REST API</h1>
<p>
Playwright REST API Docker service for URL screenshot and traffic capture.
</p>
<p>
License: GPLv3
</p>
<p>
<a href="https://pts-project.org">Website</a> | 
<a href="https://pts-project.org/docs/colander/overview/">Documentation</a> | 
<a href="https://discord.gg/qGX73GYNdp">Support</a>
</p>
</div>

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