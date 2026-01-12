# CommunityScale Public Data

This folder contains public data files that can be accessed directly via raw GitHub URLs.

## Using Raw GitHub Content

To reference these data files in web applications, use the raw GitHub URL format:

```
https://raw.githubusercontent.com/CommunityScale/public/refs/heads/main/data/{path-to-file}
```

### Available Data Files

| File | Description | Raw URL |
|------|-------------|---------|
| `US/USA_CTs_251222.json` | US Census Tract data | `https://raw.githubusercontent.com/CommunityScale/public/refs/heads/main/data/US/USA_CTs_251222.json` |
| `US/USA_zips_251222.json` | US ZIP code data | `https://raw.githubusercontent.com/CommunityScale/public/refs/heads/main/data/US/USA_zips_251222.json` |

### Example Usage

**JavaScript fetch:**
```javascript
const DATA_URL = 'https://raw.githubusercontent.com/CommunityScale/public/refs/heads/main/data/US/USA_CTs_251222.json';

fetch(DATA_URL)
    .then(response => response.json())
    .then(data => {
        console.log('Loaded', data.length, 'records');
    });
```

### Why Use Raw GitHub URLs?

- **No CORS issues**: Raw GitHub content is served with appropriate headers for cross-origin requests
- **CDN-backed**: GitHub's raw content is served via a CDN for fast global access
- **Version control**: Reference specific branches or commits for stability

### URL Formats

| Format | Example |
|--------|---------|
| Main branch | `https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/main/{path}` |
| Specific branch | `https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{path}` |
| Specific commit | `https://raw.githubusercontent.com/{owner}/{repo}/{commit-sha}/{path}` |

### Rate Limits

GitHub raw content has rate limits. For high-traffic applications, consider:
- Caching responses in your application
- Using a CDN like jsDelivr: `https://cdn.jsdelivr.net/gh/CommunityScale/public@main/data/US/USA_CTs_251222.json`
