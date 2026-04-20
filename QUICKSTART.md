# 🚀 Quick Start Guide - Webpage Screenshot to PDF

## What You Get
Your Python app includes 4 files:
- `webpage_to_pdf.py` - Main app (take screenshots of single URLs)
- `batch_screenshots.py` - Batch processor (process multiple URLs at once)
- `README.md` - Full documentation
- `urls_example.txt` - Example URL list for batch processing

## Installation (First Time Only)

### Windows
```bash
python webpage_to_pdf.py https://www.example.com
```
The app will automatically install needed dependencies!

### Mac/Linux
```bash
python3 webpage_to_pdf.py https://www.example.com
```

That's it! It will install everything automatically.

---

## Basic Usage

### ✨ Screenshot a Single Website
```bash
python webpage_to_pdf.py https://www.example.com
```

Output: `screenshot_example_com_20240115_143022.pdf`

### 📝 Save with Custom Filename
```bash
python webpage_to_pdf.py https://www.example.com -o mypage.pdf
```

### 🖼️ Save Both PDF and PNG
```bash
python webpage_to_pdf.py https://www.example.com -o page.pdf -i page.png
```

### ⏱️ Wait Longer for Complex Sites
```bash
python webpage_to_pdf.py https://www.example.com --wait 5
```

---

## Batch Processing (Multiple URLs)

### Create a File with URLs
Create `my_urls.txt`:
```
https://www.google.com
https://www.wikipedia.org
https://www.github.com
```

### Run Batch Processing
```bash
python batch_screenshots.py my_urls.txt
```

### Save to Specific Folder
```bash
python batch_screenshots.py my_urls.txt -o ./output_pdfs/
```

### Batch with Custom Wait Time
```bash
python batch_screenshots.py my_urls.txt -w 5 -o ./pdfs/
```

---

## Real-World Examples

### Capture a GitHub Profile
```bash
python webpage_to_pdf.py github.com/torvalds -o linus_torvalds_profile.pdf
```

### Save a Medium Article
```bash
python webpage_to_pdf.py https://medium.com/@username/article-title -o article.pdf
```

### Screenshot Wikipedia Page
```bash
python webpage_to_pdf.py en.wikipedia.org/wiki/Artificial_intelligence -o ai_wiki.pdf
```

### Batch Process Multiple Articles
```bash
# Create articles.txt with URLs
python batch_screenshots.py articles.txt -o articles/ -w 4
```

---

## Tips & Tricks

✅ **Works Best For:**
- Web articles and blogs
- Documentation pages
- Screenshots of websites
- Archiving web content
- Portfolio websites

⚠️ **Known Limitations:**
- Very heavy JavaScript sites might need `--wait 5` or more
- Some sites block automated access
- Protected/login pages won't work
- Very long pages create large PDFs

📊 **File Sizes:**
- Simple pages: 1-3 MB
- Medium pages: 3-8 MB
- Complex pages: 8-20 MB

⚡ **Speed Tips:**
- Use `--wait 1` for fast sites (saves time)
- Use `--wait 3-5` for JavaScript heavy sites
- Batch processing is usually slower due to disk I/O

---

## Common Commands Cheat Sheet

```bash
# Single screenshot with default naming
python webpage_to_pdf.py https://example.com

# Screenshot with custom filename
python webpage_to_pdf.py https://example.com -o output.pdf

# Include PNG image too
python webpage_to_pdf.py https://example.com -o page.pdf -i page.png

# Longer wait for slow sites
python webpage_to_pdf.py https://example.com -w 5

# Batch from file
python batch_screenshots.py urls.txt -o ./pdfs/

# Quick command for testing
python webpage_to_pdf.py google.com -o test.pdf
```

---

## Troubleshooting

### ❌ "ModuleNotFoundError"
Just run the command again - it installs packages automatically on first run

### ❌ "Timed out waiting"
Increase wait time:
```bash
python webpage_to_pdf.py URL --wait 10
```

### ❌ "Access denied"
Some sites block automated access. Try a different URL.

### ❌ "File saved but looks empty"
The page might need more load time:
```bash
python webpage_to_pdf.py URL -w 8
```

---

## Next Steps

1. **Test it:** Try capturing a simple website first
2. **Explore:** Use different wait times and output options
3. **Batch:** When ready, process multiple URLs at once
4. **Customize:** Edit the Python files to add more features

---

## File Organization

Recommended folder structure:
```
my_screenshots/
├── webpage_to_pdf.py
├── batch_screenshots.py
├── urls.txt
└── output/
    ├── screenshot1.pdf
    ├── screenshot2.pdf
    └── ...
```

---

## Need Help?

Refer to `README.md` for complete documentation with:
- Full command options
- Detailed examples
- Advanced features
- Performance tips

---

**Happy Screenshotting! 📸**
