# easySIPp - SIP Testing, Simplified.

**easySIPp** streamlines SIP/VoIP testing by providing a comprehensive web platform for SIPp. Designed for telecom professionals and QA teams, it enables you to visually create XML scenarios, preview call flows, execute tests with one click, and monitor running tests in real time — eliminating command-line complexity while maintaining full SIPp capabilities.

[![Docker Pulls](https://img.shields.io/docker/pulls/krndwr/easysipp)](https://hub.docker.com/r/krndwr/easysipp)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/kiran-daware/easySIPp/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/kiran-daware/easySIPp)](https://github.com/kiran-daware/easySIPp/stargazers)

---

## 🚀 What is easySIPp?

[SIPp](https://github.com/SIPp/sipp) is a powerful CLI-based tool for VoIP/SIP testing, widely used in the telecom industry. However, its command-line interface can be challenging for many users.

**easySIPp** provides a modern web platform for SIPp, making professional VoIP testing accessible to everyone — from beginners to experienced engineers. But it is more than a GUI: it lets you create SIPp XML scenarios with a few clicks, visualize call flows, monitor and control running SIPp instances in real time, and manage your UAC/UAS configurations in one place.

---

## ✨ Features

- **Effortless Scenario Creation** - Build and edit complex **SIPp XML scenarios** directly in the browser. No need to write raw XML — a few clicks and your scenario is ready.  
  👉 Try the [Online SIPp XML Generator](https://kiran-daware.github.io/sipp-xml/)

- **Call Flow Visualization** - Preview and understand SIP call flows before execution with interactive diagrams.

- **Configuration Management** - Save and switch between multiple UAC (User Agent Client) and UAS (User Agent Server) configurations.

- **Intuitive Test Configuration** - Configure call flows, caller/callee numbers, call rate, number of calls, and more through a simple web GUI.

- **One-Click Execution** - Run SIPp scenarios instantly — no scripts or terminal needed.

- **Live Output Streaming** - Watch SIPp results and logs in real time, just like you would in the terminal.

- **Seamless SIPp Integration** - Under the hood, it's still the real SIPp — just with a modern frontend.

---

## 🎯 Who Should Use This?

✅ **VoIP Testers & QA Engineers** - Streamline testing workflows with an intuitive UI  
✅ **Telecom Engineers** - Focus on test scenarios, not command-line syntax  
✅ **Network Operators** - Quickly validate SIP infrastructure and call flows  
✅ **Anyone New to SIPp** - Learn SIP testing without the steep learning curve  

---

## 1. 🐳 How to Use (with Docker - Recommended)

**Prerequisite:** [Docker](https://docs.docker.com/get-docker/) installed on your machine or server. The container uses host networking (`--network host`), which works best on Linux.

### Quick Start

```bash
# Pull and run (first time)
docker pull krndwr/easysipp:latest
docker run -dt --network host --name easysipp krndwr/easysipp
```

**Access at:** `http://localhost:8080` (or `http://<your-server-ip>:8080`)

### Daily Usage

```bash
# Start container (after stopping or reboot)
docker start easysipp

# Stop container
docker stop easysipp
```

### Update to Latest Version

> [!WARNING]
> Running `docker rm easysipp` will permanently delete existing data from the easysipp container, including modified or uploaded XML files. Back up any important files first.

```bash
docker stop easysipp
docker rm easysipp     # All existing data (like your modified or uploaded XML files) will be lost
docker pull krndwr/easysipp:latest
docker run -dt --network host --name easysipp krndwr/easysipp
```

### Complete Removal

```bash
docker stop easysipp
docker rm easysipp     # All existing data (like your modified or uploaded XML files) will be lost
docker rmi krndwr/easysipp
```

---

## 2. 💻 Run Without Docker (Development Environment)

If you'd rather run easySIPp directly on your machine, for example to develop or customize it, use the included `run_dev_env.sh` script.

### First-Time Setup

**Prerequisites:** `python3` (with `venv` and `pip`), `curl`, and `coreutils` (provides `sha256sum`), plus `libcap2-bin`. The script checks for these on startup. On Debian/Ubuntu, install everything with:

```bash
sudo apt-get install -y python3 python3-venv python3-pip curl coreutils libcap2-bin
```

Then clone the repository and make the script executable:
```bash
git clone https://github.com/kiran-daware/easySIPp.git
cd easySIPp
chmod +x run_dev_env.sh​
```

### Regular Usage

```bash
cd easySIPp
./run_dev_env.sh
```

**Access at:** `http://127.0.0.1:8080`

### Options

The script reads two optional environment variables:

| Variable | Default     | Description                        |
|----------|-------------|------------------------------------|
| `HOST`   | `127.0.0.1` | Address the server binds to        |
| `PORT`   | `8080`      | Port the server listens on         |

```bash
# Make it reachable from other machines on your network
HOST=0.0.0.0 ./run_dev_env.sh

# Use a custom port
PORT=9000 ./run_dev_env.sh

# Both
HOST=0.0.0.0 PORT=9000 ./run_dev_env.sh
```


---

## ❓ FAQ

<details>
<summary><strong>What is easySIPp?</strong></summary>
A comprehensive web platform for SIPp that enables visual scenario creation, call flow preview, one-click execution, and real-time monitoring — eliminating command-line complexity.
</details>

<details>
<summary><strong>Does it replace SIPp?</strong></summary>
No, it enhances SIPp. easySIPp runs the original SIPp engine under the hood, providing a modern web interface on top.
</details>

<details>
<summary><strong>Is it open source?</strong></summary>
Yes! easySIPp is open source under GPLv3. Contributions are welcome.
</details>

<details>
<summary><strong>Can I use this in production?</strong></summary>
easySIPp is actively developed and used for VoIP testing. However, as with any testing tool, validate it in your environment first.
</details>

---

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Server**: Nginx + Uvicorn (ASGI)
- **Containerization**: Docker
- **Core Engine**: SIPp

---

## 🤝 Contributing

Found a bug or have an idea? [Open an issue](https://github.com/kiran-daware/easySIPp/issues) or submit a pull request. Feedback and contributions are always welcome.

---

## 📝 License

This project is licensed under the **GNU General Public License v3.0** (GPLv3).

**Note**: easySIPp bundles the [SIPp](https://github.com/SIPp/sipp) binary, which is also licensed under GPLv3. By using this software, you agree to comply with the terms of the GPLv3 license.

---

## ⚠️ Disclaimer

This project is provided **"as is"** without warranty of any kind. Use at your own risk.

---

<div align="center">

**Made with ❤️ by [Kiran Daware](https://dkiran.net)**

⭐ Star this repo if you find it useful!

</div>

---

## 📸 Screenshots

### Main Dashboard & Test Execution
![easySIPp - Web GUI for SIPp](/screenshots/easysipp_home.png)

### Call flow preview before starting the tests
![easySIPp - Call flow preview](/screenshots/easysipp_call_flow_preview.png)

### Real-time status and control of running SIPp calls
![easySIPp - SIPp control and real-time status](/screenshots/easysipp_control_screen.png)

### Predefined SIPp XML scenarios
![easySIPp - Predefined SIPp XML scenarios](/screenshots/easysipp_xml_list.png)

### SIPp XML Scenario Generator
![easySIPp - XML Scenario generator](/screenshots/easysipp_xml_builder.png)
