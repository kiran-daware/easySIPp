# easySIPp - SIP Testing, Simplified.

**easySIPp** streamlines SIP/VoIP testing by providing a comprehensive web platform for SIPp. Designed for telecom professionals and QA teams, it enables you to visually create XML scenarios, preview call flows, execute tests with one click, and monitor running tests in real-time — eliminating command-line complexity while maintaining full SIPp capabilities.

[![Docker Pulls](https://img.shields.io/docker/pulls/krndwr/easysipp)](https://hub.docker.com/r/krndwr/easysipp)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/kiran-daware/easySIPp/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/kiran-daware/easySIPp)](https://github.com/kiran-daware/easySIPp/stargazers)

> **🚨 Project Renamed:** This project was formerly known as `kSipP`. It is now called **easySIPp** to better reflect its mission. All functionality remains the same.

---

## 🚀 What is easySIPp?

[SIPp](https://github.com/SIPp/sipp) is a powerful CLI-based tool for VoIP/SIP testing, widely used in the telecom industry. However, its command-line interface can be challenging for many users.

**easySIPp** provides a modern web platform for SIPp, making professional VoIP testing accessible to everyone — from beginners to experienced engineers. But easySIPp is not just a GUI for SIPp; it offers much more. Beyond the web interface, it includes powerful features like click-to-create SIPp XML scenarios, call flow visualization, real-time monitoring and control of running SIPp instances, and comprehensive configuration management for complete SIP/VoIP testing workflows.

---

## ✨ Features

- **Effortless Scenario Creation** - Build and edit complex **SIPp XML scenarios** directly in the browser — no need to write raw XML, just a few clicks and your xml scenarion will be ready.  
  👉 Try the [Online SIPp XML Generator](https://kiran-daware.github.io/sipp-xml/)

- **Call Flow Visualization** - Preview and understand SIP call flows before execution with interactive diagrams.

- **Configuration Management** - Save and switch between multiple UAC (User Agent Client) and UAS (User Agent Server) configurations.

- **Intuitive Test Configuration** - Configure call flows, caller/callee numbers, rates, number of calls, and more through a simple Web GUI.

- **One-Click Execution** - Run SIPp scenarios instantly — no scripts or terminal needed.

- **Live Output Streaming** - Watch SIPp results and logs in real time, just like you would in the terminal.

- **Seamless SIPp Integration** - Under the hood, it’s still the real SIPp — just with a modern frontend.

---

## 🎯 Who Should Use This?

✅ **VoIP Testers & QA Engineers** - Streamline testing workflows with an intuitive UI  
✅ **Telecom Engineers** - Focus on test scenarios, not command-line syntax  
✅ **Network Operators** - Quickly validate SIP infrastructure and call flows  
✅ **Anyone New to SIPp** - Learn SIP testing without the steep learning curve  

---

## 🐳 How to Use (with Docker)

Get up and running in seconds using Docker:

[![](https://img.shields.io/docker/pulls/krndwr/easysipp)](https://hub.docker.com/r/krndwr/easysipp)

```bash
docker run -dt --network host --name easysipp krndwr/easysipp
```
Once your container is up and running, open your browser and go to http://localhost:8080/ (or <your_linux/docker_IP>:8080)

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

### Realtime status check control of running SIPp calls
![easySIPp - SIPp control and real-time status](/screenshots/easysipp_control_screen.png)

### Predefined SIPp XML scnarios
![easySIPp - Predefined SIPp XML scenarios](/screenshots/easysipp_xml_list.png)

### SIPp XML Scenario Generator
![easySIPp - XML Scenario generator](/screenshots/easysipp_xml_builder.png)
