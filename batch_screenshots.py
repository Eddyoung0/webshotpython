#!/usr/bin/env python3
"""
Batch Website Screenshot Tool
Process multiple URLs and create PDFs from all of them
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from webpage_to_pdf import screenshot_webpage


def load_urls_from_file(filename):
    """Load URLs from a text file (one URL per line)"""
    urls = []
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []


def batch_process(urls, output_dir=None, wait_time=3):
    """
    Process multiple URLs and create screenshots
    
    Args:
        urls (list): List of URLs to process
        output_dir (str): Directory to save files
        wait_time (int): Wait time for each page to load
    
    Returns:
        dict: Results summary
    """
    if not urls:
        print("No URLs provided")
        return {'success': 0, 'failed': 0, 'files': []}
    
    # Create output directory if specified
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    else:
        output_dir = '.'
    
    results = {
        'success': 0,
        'failed': 0,
        'files': [],
        'errors': [],
        'start_time': datetime.now().isoformat(),
    }
    
    print(f"\n🔄 Processing {len(urls)} URL(s)")
    print("=" * 60)
    
    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] Processing: {url}")
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.split('://')[1].split('/')[0].replace('.', '_').replace(':', '_')
        pdf_filename = f"{domain}_{timestamp}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        success, message, files = screenshot_webpage(
            url,
            output_pdf=pdf_path,
            wait_time=wait_time
        )
        
        if success:
            results['success'] += 1
            results['files'].append({
                'url': url,
                'pdf': pdf_path,
                'size_mb': os.path.getsize(pdf_path) / (1024 * 1024)
            })
            print(f"   ✅ Success: {pdf_filename}")
        else:
            results['failed'] += 1
            results['errors'].append({'url': url, 'error': message})
            print(f"   ❌ Failed: {message}")
    
    results['end_time'] = datetime.now().isoformat()
    
    return results


def print_summary(results):
    """Print a summary of the batch processing results"""
    print("\n" + "=" * 60)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {results['success']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"📁 Total files created: {len(results['files'])}")
    
    if results['files']:
        total_size = sum(f['size_mb'] for f in results['files'])
        print(f"📦 Total size: {total_size:.2f} MB")
        
        print("\n📋 Files created:")
        for i, file_info in enumerate(results['files'], 1):
            print(f"   {i}. {file_info['url']}")
            print(f"      → {file_info['pdf']} ({file_info['size_mb']:.2f} MB)")
    
    if results['errors']:
        print("\n⚠️  Failed URLs:")
        for error in results['errors']:
            print(f"   - {error['url']}: {error['error']}")
    
    print("=" * 60 + "\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Batch convert multiple webpages to PDF',
        epilog="""
Examples:
  # Process URLs from a file
  python batch_screenshots.py urls.txt
  
  # Process URLs from a file to a specific directory
  python batch_screenshots.py urls.txt -o output_pdfs/
  
  # Process with longer wait time
  python batch_screenshots.py urls.txt -w 5
  
  # Direct URL list (comma-separated)
  python batch_screenshots.py "https://example.com,https://google.com" -o ./pdfs/
        """
    )
    
    parser.add_argument('input', help='URLs file (one per line) or comma-separated URLs')
    parser.add_argument('-o', '--output-dir', help='Output directory for PDF files')
    parser.add_argument('-w', '--wait', type=int, default=3,
                       help='Wait time for each page in seconds (default: 3)')
    
    args = parser.parse_args()
    
    # Determine if input is a file or direct URLs
    if os.path.isfile(args.input):
        urls = load_urls_from_file(args.input)
    else:
        # Treat as comma-separated URLs
        urls = [u.strip() for u in args.input.split(',')]
    
    if not urls:
        print("Error: No valid URLs found")
        sys.exit(1)
    
    print("🚀 Batch Website Screenshot to PDF Converter")
    print(f"📝 Found {len(urls)} URL(s) to process")
    
    results = batch_process(urls, output_dir=args.output_dir, wait_time=args.wait)
    print_summary(results)
    
    # Save results to JSON
    if args.output_dir:
        results_file = os.path.join(args.output_dir, 'batch_results.json')
    else:
        results_file = 'batch_results.json'
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📊 Results saved to: {results_file}")


if __name__ == '__main__':
    main()
