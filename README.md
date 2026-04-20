# Webpage Screenshot to PDF Converter

A Python application that captures full-page screenshots of websites and converts them to PDF files.

## Features

✨ **Full-page screenshots** - Captures entire webpage content (not just visible area)
📄 **PDF conversion** - Automatically saves full-length webpages as multi-page PDF
⚡ **Fast & reliable** - Uses Playwright for headless browser automation
🎨 **PNG export** - Optional PNG image export
⏱️ **Customizable wait time** - Configure page load wait duration
🔄 **Auto-dependency installation** - Installs required packages automatically

## Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

### Option 1: Quick Start (Recommended)
The app will automatically install dependencies on first run:

```bash
python webpage_to_pdf.py https://www.example.com
```

### Option 2: Manual Installation
```bash
# Install required packages
pip install playwright Pillow

# Install browser binaries (required for Playwright)
python -m playwright install chromium
```

## Usage

### Basic Usage
```bash
# Take screenshot of a website (auto-generates filename)
python webpage_to_pdf.py https://www.example.com
```

### Specify Output Filename
```bash
# Save to specific PDF file
python webpage_to_pdf.py https://www.example.com -o mypage.pdf
```

### Save Both PDF and PNG
```bash
# Create both PDF and PNG versions
python webpage_to_pdf.py https://www.example.com -o page.pdf -i page.png
```

### Custom Wait Time
```bash
# Wait 5 seconds for dynamic content to load
python webpage_to_pdf.py https://www.example.com --wait 5
```

### Without Protocol
```bash
# Works with or without https://
python webpage_to_pdf.py example.com -o output.pdf
```

## Command Line Options

```
positional arguments:
  url                   URL of the webpage to screenshot

optional arguments:
  -h, --help           Show help message
  -o, --output-pdf     Output PDF filename (default: auto-generated)
  -i, --output-image   Also save as PNG image file
  -w, --wait SECONDS   Wait time for page to load (default: 3 seconds)
```

## Examples

```bash
# Screenshot a news website
python webpage_to_pdf.py https://www.bbc.com -o bbc_homepage.pdf

# Capture GitHub profile
python webpage_to_pdf.py github.com/username -o github_profile.pdf

# Save in both formats with longer wait time
python webpage_to_pdf.py https://www.medium.com -o article.pdf -i article.png -w 5

# Screenshot a long article with custom wait
python webpage_to_pdf.py https://example.com/long-article -w 10 -o article.pdf
```

## Output Files

By default, files are saved in the current directory with auto-generated names:
- Format: `screenshot_[domain]_[timestamp].pdf`
- Example: `screenshot_example_com_20240115_143022.pdf`

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Dependencies will install automatically. If not, run:
```bash
pip install playwright Pillow
python -m playwright install chromium
```

### Issue: Timeout waiting for page to load
**Solution:** Increase wait time:
```bash
python webpage_to_pdf.py URL --wait 10
```

### Issue: JavaScript content not loading
**Solution:** The app waits for network idle, but some sites need more time:
```bash
python webpage_to_pdf.py URL --wait 8
```

### Issue: SSL certificate error
**Solution:** Try without https:
```bash
python webpage_to_pdf.py example.com
```

## How It Works

1. **Validates URL** - Ensures proper format (adds https:// if needed)
2. **Launches Browser** - Starts headless Chromium browser
3. **Loads Webpage** - Navigates to URL with network idle wait
4. **Renders Content** - Waits for dynamic content to load
5. **Captures Screenshot** - Takes full-page screenshot
6. **Converts to PDF** - Saves as high-quality PDF file
7. **Closes Browser** - Cleans up resources

## Advanced Features

### Batch Processing Script
Create a file `batch_screenshots.py`:

```python
from webpage_to_pdf import screenshot_webpage

urls = [
    'https://www.example.com',
    'https://www.google.com',
    'https://www.github.com'
]

for url in urls:
    success, msg, files = screenshot_webpage(url)
    print(f"{url}: {msg}")
```

Then run:
```bash
python batch_screenshots.py
```

## Performance Tips

- Use `--wait 2` or `--wait 1` for fast-loading sites to save time
- Use `--wait 5` or higher for JavaScript-heavy sites
- PNG files are larger; use PDF for archival
- Close other applications to speed up rendering

## File Size

- Average PDF: 2-10 MB per page
- PNG images: 3-15 MB per page
- Depends on webpage complexity and content

## Security Notes

- The app only takes screenshots; no data is sent anywhere
- Downloaded files are stored locally
- Uses headless browser for safe rendering
- No credentials or sensitive data is logged

## License

Free to use and modify

## Support

For issues or questions, check:
- Your Python version: `python --version` (should be 3.7+)
- Playwright installation: `python -m playwright install chromium`
- Internet connection and URL accessibility
