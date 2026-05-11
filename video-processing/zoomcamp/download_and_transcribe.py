import os
import subprocess
import glob
import re

videos = {
    "01-docker-terraform": [
        "18jIzE41fJ4", "lP8xXebHmuE", "QEcps_iskgg", "s2bOYDCKl_M", "Y2ux7gq3Z0o", "PBi0hHjLftk"
    ],
    "02-workflow-orchestration": [
        "-JLnp-iLins", "wgPxC4UjoLM", "-KmwrCqRhic", "MNOKVx8780E", "VAHm0R_XjqI", "Z9ZmmwtXDcU",
        "1pu_C_oOAMA", "E04yurp1tSU", "TLGFAOHpOYM", "52u9X_bfTAo", "b-6KhfWfk2M", "GHPtRDAv044",
        "LmnfjGKwnVU", "3IbjHfC8bMg", "XuPDQ1UcNyI"
    ],
    "03-data-warehouse": [
        "jrHljAoD6nM", "-CqXf7vhhDs", "k81mLJVX08w", "eduHi1inM4s", "B-WtpB0PuG4", "BjARzEWaznU"
    ],
    "04-analytics-engineering": [
        "uF76d5EmdtU", "gsKuETFJr54", "J0XCDyKiU64", "1HmL63e-vRs", "ueVy2N54lyc", "2dNJXHFCHaY", 
        "V2m5C0n8Gro", "Cs9Od1pcrzM", "39nLTs74A3E", "BnLkrA7a6gM", "Mork172sK_c"
    ],
    "05-data-platforms": [
        "f6vg7lGqZx0", "JJwHKSidX_c", "q0k_iz9kWsI", "224xH7h8OaQ", "uBqjLEwF8rc", 
        "YWDjnSxbBtY", "uzp_DiR4Sok", "ZElY5SoqrwI", "XCx0nDmhhxA", "3nykPEs_V7E"
    ],
    "06-batch": [
        "dcHe5Fl3MF8", "FhaqbEOuQ8U", "hqUbB9c8sKg", "r_Sf6fCB40c", "ti3aC1m3rE8", 
        "CI3P4tAtru4", "uAlp2VuZZPY", "68CipcZt7ZA", "9qrDsY_2COo", "lu7TrqAWuH4", 
        "Bdu-xIrF3OM", "k3uB2K99roI", "Yyz293hBVcQ", "HXBwSlXo5IA", "osAiAYahvh8", "HIm2BOj8C0Q"
    ],
    "07-streaming": [
        "YDUgFeHQzJU", "BgAlVknDFlQ", "VIVr7KwRQmE"
    ],
    "projects": []
}

base_dir = "data-engineering-zoomcamp"

def clean_vtt(vtt_text):
    lines = vtt_text.split('\n')
    cleaned_lines = []
    seen_text = set()
    for line in lines:
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        if '-->' in line:
            continue
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line and clean_line not in seen_text:
            cleaned_lines.append(clean_line)
            seen_text.add(clean_line)
    return ' '.join(cleaned_lines)

# Move previously downloaded stuff and setup dirs
for mod, ids in videos.items():
    mod_path = os.path.join(base_dir, mod)
    raw_dir = os.path.join(mod_path, "transcripts", "raw")
    clean_dir = os.path.join(mod_path, "transcripts", "clean")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(os.path.join(mod_path, "videos"), exist_ok=True)
    os.makedirs(os.path.join(mod_path, "notes"), exist_ok=True)
    
    print(f"Downloading transcripts for {mod}...")
    for vid in ids:
        # Check if already exists in raw_dir by looking for any vtt containing the ID
        existing = glob.glob(os.path.join(raw_dir, f"*{vid}*")) + glob.glob(os.path.join(raw_dir, "*.vtt"))
        
        # Actually yt-dlp doesn't include the ID in the title by default unless specified, 
        # so let's just run it; yt-dlp skips if it exists.
        cmd = [
            "yt-dlp", "--write-auto-subs", "--sub-langs", "en.*", "--skip-download", 
            "--output", f"{raw_dir}/%(title)s.%(ext)s", f"https://www.youtube.com/watch?v={vid}"
        ]
        # We redirect stdout/stderr to avoid massive logs
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Clean them
    for vtt_file in glob.glob(os.path.join(raw_dir, "*.vtt")):
        txt_file = os.path.join(clean_dir, os.path.basename(vtt_file).replace(".vtt", ".txt"))
        if not os.path.exists(txt_file):
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = clean_vtt(f.read())
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(content)

print("Done downloading and cleaning!")
