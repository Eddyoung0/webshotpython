#!/usr/bin/env python3
"""
Webpage Screenshot to PDF Converter
Takes a URL and converts the full webpage to a PDF file
"""

import os
import sys
import argparse
from datetime import datetime


def ensure_playwright_browser_installed():
    """Install Chromium browser binaries for Playwright using the active Python."""
    import subprocess
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def install_dependencies():
    """Install required packages if not already installed"""
    import subprocess
    
    packages = ['playwright', 'Pillow']
    for package in packages:
        try:
            __import__(package.lower() if package != 'Pillow' else 'PIL')
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Always ensure Playwright browser binaries exist for this interpreter.
    print("Installing Playwright browser binaries (Chromium)...")
    ensure_playwright_browser_installed()


def capture_full_length_image(page, max_scroll_steps=500):
    """Capture full content as an image.

    Tries full_page first; if that is still viewport-limited, falls back to
    scroll-and-stitch capture to support internal scrollable viewers.
    
    Args:
        page: Playwright page object
        max_scroll_steps (int): Maximum number of scrolls to attempt (default: 500)
    """
    from PIL import Image
    import io
    import hashlib

    viewport = page.viewport_size or {'width': 1920, 'height': 1080}
    full_page_bytes = page.screenshot(full_page=True)
    full_page_image = Image.open(io.BytesIO(full_page_bytes)).convert('RGB')

    # If image height is close to viewport height, full_page likely failed.
    if full_page_image.height > int(viewport['height'] * 1.2):
        return full_page_image

    print("Full-page capture is viewport-limited. Using scroll-and-stitch fallback...")
    page.mouse.move(viewport['width'] // 2, viewport['height'] // 2)

    frames = []
    seen_hashes = set()
    repeated_frames = 0

    for step in range(max_scroll_steps):
        frame_bytes = page.screenshot(full_page=False)
        frame_hash = hashlib.sha1(frame_bytes).hexdigest()

        if frame_hash in seen_hashes:
            repeated_frames += 1
            if repeated_frames >= 5:  # Increased threshold for consistency
                print(f"✓ Reached end of content after {step} scrolls ({len(frames)} frames captured)")
                break
        else:
            repeated_frames = 0
            seen_hashes.add(frame_hash)
            frames.append(Image.open(io.BytesIO(frame_bytes)).convert('RGB'))

        page.mouse.wheel(0, int(viewport['height'] * 0.85))
        page.wait_for_timeout(450)

    if not frames:
        return full_page_image

    stitched_width = max(frame.width for frame in frames)
    stitched_height = sum(frame.height for frame in frames)
    stitched = Image.new('RGB', (stitched_width, stitched_height), 'white')

    current_y = 0
    for frame in frames:
        stitched.paste(frame, (0, current_y))
        current_y += frame.height

    return stitched


def save_full_length_pdf_from_image(image, output_pdf):
    """Save a long image as a multi-page PDF.

    Many websites render poorly with page.pdf() and may only include the first
    screen in print mode. This keeps screen rendering and slices the long image
    into page-sized chunks.
    """
    # Create page slices using an A4-like portrait ratio based on image width.
    page_height = max(1, int(image.width * 1.4142))
    pages = []

    for top in range(0, image.height, page_height):
        bottom = min(top + page_height, image.height)
        pages.append(image.crop((0, top, image.width, bottom)))

    if not pages:
        raise RuntimeError("Failed to create PDF pages from screenshot")

    first_page, remaining_pages = pages[0], pages[1:]
    first_page.save(
        output_pdf,
        "PDF",
        save_all=True,
        append_images=remaining_pages,
        resolution=100.0
    )


def screenshot_webpage(url, output_pdf=None, output_image=None, wait_time=3, max_scroll_steps=500):
    """
    Take a screenshot of a webpage and optionally convert to PDF
    
    Args:
        url (str): The URL of the webpage to screenshot
        output_pdf (str): Output path for PDF file (optional)
        output_image (str): Output path for image file (optional)
        wait_time (int): Time to wait for page to load (in seconds)
        max_scroll_steps (int): Maximum number of scroll attempts for full-page capture (default: 500)
    
    Returns:
        tuple: (success: bool, message: str, files_created: list)
    """
    from playwright.sync_api import sync_playwright
    
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"📱 Accessing webpage: {url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})
            
            # Navigate to URL
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for dynamic content
            page.wait_for_timeout(wait_time * 1000)
            
            files_created = []
            
            # Generate output filenames if not provided
            if not output_pdf and not output_image:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = url.split('://')[1].split('/')[0].replace('.', '_')
                output_pdf = f"screenshot_{domain}_{timestamp}.pdf"
            
            # Capture a true full-length image first.
            full_length_image = capture_full_length_image(page, max_scroll_steps=max_scroll_steps)

            # Save as PDF (default behavior)
            if not output_pdf:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = url.split('://')[1].split('/')[0].replace('.', '_')
                output_pdf = f"screenshot_{domain}_{timestamp}.pdf"

            save_full_length_pdf_from_image(full_length_image, output_pdf)
            files_created.append(output_pdf)
            print(f"✅ Full-length PDF saved: {output_pdf}")

            # Save screenshot image if requested.
            if output_image:
                full_length_image.save(output_image, format='PNG')
                files_created.append(output_image)
                print(f"✅ Screenshot saved: {output_image}")
            
            browser.close()
            
            return True, f"Successfully created {len(files_created)} file(s)", files_created
    
    except Exception as e:
        # Auto-heal the common first-run issue where browser binaries are missing.
        err = str(e)
        if "Executable doesn't exist" in err or "playwright install" in err:
            try:
                print("Playwright browser not found. Installing Chromium...")
                ensure_playwright_browser_installed()
                return screenshot_webpage(url, output_pdf, output_image, wait_time, max_scroll_steps)
            except Exception as install_error:
                return False, f"Error installing Playwright browser: {install_error}", []

        return False, f"Error: {err}", []


def main():
    parser = argparse.ArgumentParser(
        description='Convert a webpage to a PDF screenshot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python webpage_to_pdf.py https://www.example.com
  python webpage_to_pdf.py https://www.example.com -o mypage.pdf
  python webpage_to_pdf.py example.com -o output.pdf -i screenshot.png
  python webpage_to_pdf.py https://www.example.com --wait 5
  python webpage_to_pdf.py https://www.verylongpage.com --max-scroll 1000
        """
    )
    
    parser.add_argument('url', help='URL of the webpage to screenshot')
    parser.add_argument('-o', '--output-pdf', 
                       help='Output PDF filename (default: auto-generated)')
    parser.add_argument('-i', '--output-image', 
                       help='Also save as PNG image')
    parser.add_argument('-w', '--wait', type=int, default=3,
                       help='Wait time for page to load in seconds (default: 3)')
    parser.add_argument('--max-scroll', type=int, default=500,
                       help='Maximum scroll attempts for capturing full-page content (default: 500)')
    
    args = parser.parse_args()
    
    # Ensure dependencies and browser binaries are available.
    try:
        import playwright
        ensure_playwright_browser_installed()
    except ImportError:
        print("Installing required dependencies...")
        install_dependencies()
    
    print("🚀 Webpage Screenshot to PDF Converter")
    print("=" * 50)
    
    success, message, files = screenshot_webpage(
        args.url,
        output_pdf=args.output_pdf,
        output_image=args.output_image,
        wait_time=args.wait,
        max_scroll_steps=args.max_scroll
    )
    
    print("=" * 50)
    print(message)
    
    if not success:
        sys.exit(1)
    
    print(f"\n📁 Output files:")
    for file in files:
        file_size = os.path.getsize(file) / (1024 * 1024)  # Convert to MB
        print(f"   - {file} ({file_size:.2f} MB)")


if __name__ == '__main__':
    main()
