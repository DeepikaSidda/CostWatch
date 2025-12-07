# 💎 AWS Cost Widget

> **"I hate checking the bill manager on console, so I built this."**

A premium, always-on-top desktop widget that displays your AWS spending in real-time. No more logging into the AWS Console just to check your costs!

![Python](https://img.shields.io/badge/Python-3.8+-purple?style=for-the-badge&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cost_Explorer-orange?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<p align="center">
  <img src="docs/widget-preview.png" alt="AWS Cost Widget Preview" width="350"/>
</p>

## ✨ Features

- 🟣 **Premium Purple Theme** - AWS Cloud Clubs inspired design
- 💰 **Real-time Cost Tracking** - Month-to-date AWS spending at a glance
- 📊 **Visual Budget Progress** - Color-coded progress bar (green/yellow/red)
- 🔥 **Top Services Breakdown** - See which services cost the most
- 🖱️ **Draggable Widget** - Position anywhere on your screen
- 🔄 **Auto-refresh** - Configurable update interval (10-300 seconds)
- 🌐 **Cross-platform** - Works on Windows, macOS, and Linux
- 🎨 **Glassmorphism Design** - Modern, elegant UI that stands out

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- AWS credentials configured

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aws-cost-widget.git
cd aws-cost-widget

# Install dependencies
pip install -r requirements.txt

# Run the widget
python src/main.py
```

### AWS Credentials Setup

The widget reads AWS credentials from standard locations:

**Option 1: AWS CLI (Recommended)**

```bash
aws configure
```

**Option 2: Environment Variables**

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option 3: Credentials File**
Create `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```

> ⚠️ Your IAM user needs `ce:GetCostAndUsage` permission.

## ⚙️ Configuration

Edit `config.json` to customize the widget:

```json
{
  "budget": 100.0,
  "refresh_interval": 30,
  "use_simulated_data": false
}
```

| Option               | Description                      | Default |
| -------------------- | -------------------------------- | ------- |
| `budget`             | Monthly budget in USD            | 100.0   |
| `refresh_interval`   | Seconds between updates (10-300) | 30      |
| `use_simulated_data` | Use mock data for testing        | false   |

## 🎨 Screenshots

### Premium Purple Theme

The widget features an AWS Cloud Clubs inspired purple theme with:

- Glassmorphism effects
- Gradient borders
- Color-coded budget status
- Ranked service breakdown

## 🏗️ Architecture

```
aws-cost-widget/
├── src/
│   ├── main.py          # Application entry point
│   ├── widget.py        # UI components (tkinter)
│   ├── cost_fetcher.py  # AWS Cost Explorer integration
│   ├── config.py        # Configuration management
│   └── scheduler.py     # Auto-refresh scheduler
├── tests/               # Property-based & unit tests
├── config.json          # User configuration
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

The project uses property-based testing with Hypothesis:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Kiro](https://kiro.dev) - AI-powered IDE
- Inspired by AWS Cloud Clubs community
- Purple theme represents the AWS Cloud Clubs brand

---

<p align="center">
  Made with 💜 by developers who hate checking the AWS Console
</p>
