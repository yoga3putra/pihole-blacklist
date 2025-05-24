import requests

def split_header_and_domains(filename):
    header_lines = []
    domain_lines = []
    domain_section_started = False
    with open(filename, "r") as f:
        for line in f:
            if not domain_section_started and line.strip().startswith("0.0.0.0") and len(line.strip().split()) == 2:
                domain_section_started = True
            if domain_section_started:
                domain_lines.append(line)
            else:
                header_lines.append(line)
    return header_lines, domain_lines


def extract_domains(lines):
    """Ambil domain dari baris yang valid"""
    domains = set()
    for line in lines:
        line = line.strip()
        if line.startswith("0.0.0.0"):
            parts = line.split()
            if len(parts) == 2:
                domains.add(parts[1].lower())
    return domains

def load_gov_domains(url):
    """Ambil daftar domain blacklist dari URL"""
    print(f"📥 Mengambil dari: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return set(
        line.strip().lower()
        for line in response.text.splitlines()
        if line.strip() and not line.startswith("#")
    )

def save_filtered_file(header_lines, domains, filename):
    """Simpan hasil domain yang telah difilter"""
    with open(filename, "w") as f:
        # Tulis ulang header asli
        f.writelines(header_lines)

        # Tulis domain hasil filter
        for domain in sorted(domains):
            f.write(f"0.0.0.0 {domain}\n")

def main():
    URL = "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_blacklist_complete.txt"
    FILENAME = "pihole_blacklist.txt"

    header_lines, domain_lines = split_header_and_domains(FILENAME)
    my_domains = extract_domains(domain_lines)
    gov_domains = load_gov_domains(URL)

    filtered_domains = my_domains - gov_domains

    save_filtered_file(header_lines, filtered_domains, FILENAME)

    print(f"✅ Selesai: {len(filtered_domains)} domain ditulis kembali ke {FILENAME}")

if __name__ == "__main__":
    main()
