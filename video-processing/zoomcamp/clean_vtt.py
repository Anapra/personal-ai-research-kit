import re
import sys

def clean_vtt(vtt_text):
    lines = vtt_text.split('\n')
    cleaned_lines = []
    seen_text = set()
    
    for line in lines:
        # Skip VTT headers and empty lines
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        # Skip timestamp lines
        if '-->' in line:
            continue
        # Remove HTML tags like <00:00:00.400><c>
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line and clean_line not in seen_text:
            cleaned_lines.append(clean_line)
            seen_text.add(clean_line)
            
    return ' '.join(cleaned_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_vtt.py <file_path>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    
    print(clean_vtt(text))
