import os
import sys

# Configurable watermark string, or pass via env var or command line
WATERMARK = os.getenv("WATERMARK_STRING", "WATERMARK-REPO-DEFAULT")

EXTENSIONS = {
    '.py': '#',
    '.js': '//',
    '.ts': '//',
    '.java': '//',
    '.lua': '--',
    '.hcl': '#',
    '.tf': '#',
    '.html': '<!--',
}

# Dockerfile detection function
def is_dockerfile(fname):
    return fname == 'Dockerfile' or fname.endswith('.Dockerfile')

def insert_watermark(file_path, watermark):
    _, ext = os.path.splitext(file_path)  # Fixed: removed *, added _
    base = os.path.basename(file_path)    # Fixed: removed * from file*path
    
    # Determine comment syntax
    if is_dockerfile(base):
        cmt = '#'
        wm_line = f"{cmt} {watermark}\n"
    elif ext in EXTENSIONS:
        cmt = EXTENSIONS[ext]
        if ext == '.html':
            wm_line = f"<!-- {watermark} -->\n"
        else:
            wm_line = f"{cmt} {watermark}\n"
    else:
        return
    
    # Read file and check for existing watermark
    try:
        with open(file_path, "r", encoding="utf8") as f:
            lines = f.readlines()
        
        if any(watermark in line for line in lines[:5]):
            return
        
        # Insert at top
        new_lines = [wm_line] + lines
        with open(file_path, "w", encoding="utf8") as f:
            f.writelines(new_lines)
        print(f"Watermarked: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def scan_and_watermark(root, watermark):
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            _, ext = os.path.splitext(fname)
            if ext in EXTENSIONS or is_dockerfile(fname):
                insert_watermark(os.path.join(dirpath, fname), watermark)

if __name__ == "__main__":  # Fixed: removed ** formatting
    # Allow override of watermark string from command line
    watermark = sys.argv[1] if len(sys.argv) > 1 else WATERMARK
    # Allow override of directory to scan (defaults to current dir)
    scan_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    scan_and_watermark(scan_dir, watermark)
