# 📡 Pi-hole Security Gateway (Raspberry Pi 3)

A network-wide DNS filtering, monitoring, and security analytics system built on a Raspberry Pi 3 using **Pi-hole**, **Unbound**, and custom Python tooling.

This project transforms a Raspberry Pi into a **DNS security gateway** that provides ad/tracker blocking, local recursive DNS resolution, traffic analytics, and IDS-style visibility into DNS behavior.

---

## 🔧 System Architecture

Client Devices
↓ (DHCP + DNS)
Raspberry Pi 3
├── Pi-hole (DNS filtering + logging)
├── Unbound (local recursive DNS resolver)
├── FTL / Gravity Databases
└── Python Telemetry Exporter
↓
JSON / CSV Metrics


All DNS queries on the network are routed through the Pi, where they are filtered, logged, and analyzed.

---

## ✨ Features

### 🛑 Network-Wide Ad & Tracker Blocking
- Blocks ~80k+ known malicious and advertising domains
- Enforced at the DNS layer (works for all devices)

### 🔐 Local Recursive DNS (Unbound)
- Eliminates reliance on third-party resolvers (Google, Cloudflare)
- Improves privacy and DNS security
- DNSSEC-aware

### 📊 DNS Telemetry & Analytics
- Extracts live DNS statistics directly from Pi-hole’s **FTL SQLite databases**
- Tracks:
  - Total DNS queries per day
  - Blocked queries
  - Unique domains
  - Unique clients
  - Blocklist size (gravity.db)

### 🧠 IDS-Style Detection Logic
- Identifies blocked DNS activity using Pi-hole status codes
- Designed to be extended for:
  - Suspicious TLDs
  - DGA-style domains
  - Anomalous client behavior

### 🐍 Custom Python Exporter
- No external exporters required
- Reads directly from:
  - `/etc/pihole/pihole-FTL.db`
  - `/etc/pihole/gravity.db`
- Outputs:
  - `dns_stats.json` (snapshot)
  - `dns_stats.csv` (time-series)

---

## 📁 Repository Structure



pihole-security-gateway/
├── export_dns_stats.py # Python telemetry exporter
├── dns_stats.json # Latest DNS snapshot
├── dns_stats.csv # Historical DNS metrics
├── README.md
