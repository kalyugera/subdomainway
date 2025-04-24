# 🌐 Wayback Subdomain Finder

A Python script to discover and validate historical subdomains for a given domain using the [Wayback Machine](https://web.archive.org/). This tool fetches past URLs from the Wayback Machine, extracts potential subdomains, and checks their live status concurrently, saving the results to a file.

---

## 🚀 Features

- **Wayback Machine Integration**: Retrieves archived URLs for any domain.
- **Subdomain Extraction**: Extracts unique subdomains from historical data.
- **Concurrency**: Uses multithreading for fast, parallel checking of subdomain status.
- **Status Highlighting**: Color-coded output for HTTP status codes.
- **Result Export**: Saves discovered, active subdomains to `discovered_subdomains.txt`.

---

## 🛠️ How it Works

1. **User Input**: Asks for a domain name from the user.
2. **Wayback Query**: Retrieves a list of URLs from the Wayback Machine related to the domain.
3. **Extraction**: Uses regex to extract unique subdomains.
4. **Queue & Concurrency**: Subdomains are queued and checked in parallel threads.
5. **Live Check**: For each subdomain, sends a HTTP GET request to check if it’s alive.
6. **Result Display & Save**: Outputs colored HTTP status to the console and writes discovered (live) subdomains to a file.

---

## 📦 Usage

### 1. **Install Dependencies**

```
pip install requests colorama
```

### 2. **Run the Script**

``` 
python wayback_subdomain_finder.py
```

### 3. **Follow the Prompt**
Enter your target domain when prompted (e.g., `example.com`).

### 4. **Results**
- Live progress is shown in the console with colored status codes:
  - 🟩 **200** (Green): Subdomain is live!
  - 🟨 **3xx** (Yellow): Subdomain redirected.
  - 🟥 **Others** (Red): Not found or error.
  - 🟪 **X** (Magenta): Connection error.
- All discovered live subdomains are saved in `discovered_subdomains.txt`.

---

## 💡 Example Output

``` 
Enter Your Domain Here: mydomain.com
[*] Fetching URLs from Wayback Machine for mydomain.com ...
[+] Wayback Machine found 15 unique subdomains.
[i] Total unique subdomains to check: 15 http://foo.mydomain.com
[X] Connection error: http://mail.mydomain.com http://blog.mydomain.com
...
Scan complete. Results saved to discovered_subdomains.txt
Total discovered subdomains: 4
Exiting...
```


---

## ⚙️ Script Details

- **wayback_subdomains(domain)**: Fetches all historical URLs from the Wayback Machine for the root domain, then extracts unique subdomains via regex.
- **Threading & Queue**: Ten worker threads check subdomains in parallel, removing dead/unresponsive results quickly.
- **Color Output**: Uses `colorama` for readable output (Windows-compatible).
- **Error Handling**: Graceful handling of network errors, timeouts, and user input errors.

---

## ✨ Why use this tool?

- Quickly uncover forgotten or legacy subdomains which may still be live, posing security risks 🚨.
- Leverage historical data, not just current DNS entries.
- Improve your reconnaissance and bug bounty workflow 💰.

---

## 📝 License

Free to use for educational and research purposes. Please use responsibly.

---

## 🤝 Contributing

Suggestions and pull requests welcome!

---
