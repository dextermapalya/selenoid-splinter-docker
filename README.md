# Selenoid + Splinter + Docker Test Environment

A complete Docker-based automation testing environment combining **Selenoid** (containerized browser hub), **Splinter** (Python test framework), and **Docker Compose** for automated web testing.

## Features

✅ **Selenoid** - Lightweight Selenium Grid alternative running browsers in Docker containers  
✅ **Splinter** - Python testing framework with simple, readable API  
✅ **Docker Compose** - Orchestrated multi-container setup  
✅ **Selenoid UI** - Web interface to monitor test runs (http://localhost:8080)  
✅ **Chrome & Firefox** - Multi-browser support  
✅ **Test Reports** - Pytest HTML reports  
✅ **Sample Tests** - Google.com test cases included  

## Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose (v1.29+)
- 2+ GB free disk space for browser images

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/dextermapalya/selenoid-splinter-docker.git
cd selenoid-splinter-docker
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will:
- Start Selenoid (browser hub) on port 4444
- Start Selenoid UI on port 8080
- Build and start the test runner container

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f selenoid
docker-compose logs -f test-runner
```

### 4. Monitor Tests

Open your browser and navigate to:
- **Selenoid UI**: http://localhost:8080
- **Tests Output**: Watch the logs in your terminal

### 5. Stop Services

```bash
docker-compose down
```

## Running Tests

### Run Default Tests (Google.com)

```bash
docker-compose up test-runner
```

### Run Tests Locally (Without Docker)

First install dependencies:

```bash
pip install -r requirements.txt
```

Then ensure Selenoid is running and execute:

```bash
python tests/test_google.py
```

### Run Tests with Custom Browser

```bash
# Using Firefox instead of Chrome
BROWSER_TYPE=firefox python tests/test_google.py
```

### Run with Pytest

```bash
# Run all tests with pytest
docker-compose exec test-runner pytest tests/ -v

# Generate HTML report
docker-compose exec test-runner pytest tests/ -v --html=reports/report.html
```

## Project Structure

```
selenoid-splinter-docker/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Test runner image
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── selenoid/
│   └── config/
│       └── browsers.json       # Selenoid browser capabilities
├── tests/
│   └── test_google.py          # Sample Google.com tests
└── reports/                    # Test reports (generated)
```

## Test Script Details

### test_google.py

The sample test script (`tests/test_google.py`) contains:

1. **test_google_homepage()** - Tests basic Google homepage functionality:
   - Loads google.com
   - Verifies page title
   - Finds search box
   - Performs a search
   - Validates search results

2. **test_google_elements()** - Tests page elements:
   - Verifies footer links
   - Checks language options

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SELENOID_URL` | `http://selenoid:4444` | Selenoid hub URL |
| `BROWSER_TYPE` | `chrome` | Browser to use (chrome/firefox) |
| `PYTHONUNBUFFERED` | `1` | Enable real-time logging |

### Browser Capabilities

Edit `selenoid/config/browsers.json` to:
- Add more browser versions
- Change default browser
- Configure screen resolution
- Set browser timeouts

Example:

```json
{
  "chrome": {
    "default": "latest",
    "versions": {
      "latest": {
        "image": "selenoid/chrome:latest",
        "port": "4444",
        "path": "/"
      },
      "116.0": {
        "image": "selenoid/chrome:116.0",
        "port": "4444",
        "path": "/"
      }
    }
  }
}
```

## Splinter API Quick Reference

```python
from splinter import Browser

# Initialize browser
browser = Browser('remote', url='http://selenoid:4444/wd/hub')

# Navigate
browser.visit('https://www.google.com')

# Find elements
browser.find_by_name('q')           # By name attribute
browser.find_by_css('.element')     # By CSS selector
browser.find_by_xpath('//a')        # By XPath
browser.find_by_text('Click me')    # By visible text

# Interact
browser.fill('search_term', 'query')
browser.click_link_by_text('Next')
browser.check('checkbox_id')
browser.select('option', 'value')

# Assertions
assert browser.title == 'Title'
assert browser.is_element_present_by_css('.element')
assert browser.is_element_not_present_by_id('missing')

# Wait & Sleep
browser.sleep(2)
browser.wait_time = 10  # Global wait time

# Get info
text = browser.find_by_css('p').text
url = browser.url
```

## Troubleshooting

### Selenoid Won't Start

```bash
# Check Docker daemon
docker info

# Verify volume mounts
docker-compose ps

# Check Selenoid logs
docker logs selenoid
```

### Browser Connection Timeout

```bash
# Increase wait time in test
browser.wait_time = 20

# Or set in capabilities
desired_capabilities = {
    'browserName': 'chrome',
    'timeZone': 'UTC',
    'screenResolution': '1920x1080'
}
```

### No Search Results Found

- Google may have changed the DOM structure
- Update CSS selectors in `test_google.py`
- Inspect page with Selenoid UI to see actual elements

### Port Already in Use

```bash
# Find process using port
lsof -i :4444
lsof -i :8080

# Or use different ports in docker-compose.yml
```

## Advanced Usage

### Add New Tests

Create `tests/test_example.py`:

```python
from splinter import Browser
import os

SELENOID_URL = os.getenv('SELENOID_URL', 'http://localhost:4444')

def test_example():
    browser = Browser(
        'remote',
        url=f'{SELENOID_URL}/wd/hub',
        desired_capabilities={'browserName': 'chrome'}
    )
    
    try:
        browser.visit('https://example.com')
        assert 'Example' in browser.title
        print("✓ Test passed!")
    finally:
        browser.quit()
```

Run with:

```bash
docker-compose exec test-runner pytest tests/test_example.py -v
```

### Screenshot on Failure

```python
try:
    browser.visit('https://example.com')
    assert some_condition
except AssertionError:
    browser.screenshot('reports/failure.png')
    raise
```

### Video Recording

Selenoid automatically records videos. Access them via:

```bash
# From Selenoid UI or
docker exec selenoid ls /opt/selenoid/logs/
```

### Running Tests in Parallel

```bash
docker-compose exec test-runner pytest tests/ -v -n auto
```

(Requires `pytest-xdist` in requirements.txt)

## Performance Tips

- Use `headless` mode for faster execution
- Run multiple test-runner containers for parallel testing
- Disable browser cache between tests if needed
- Use smaller screen resolutions (1280x720) to reduce resource usage

## Resources

- [Splinter Documentation](https://splinter.readthedocs.io/)
- [Selenoid GitHub](https://github.com/aerokube/selenoid)
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium WebDriver](https://www.selenium.dev/)

## License

MIT License - Feel free to use this template for your testing projects!

## Contributing

Found a bug or have suggestions? Open an issue or submit a PR!

---

**Happy Testing! 🎉**