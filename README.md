# 📧 Automated Email Management System

> An AI-powered email automation workflow built with **n8n**, **Google Gemini AI**, **Gmail**, and **Slack** to automatically classify, route, and manage incoming emails.

![Workflow](./screenshots/workflow.png)

---

## 📖 Overview

The **Automated Email Management System** is an intelligent workflow built with **n8n** that automates the processing of incoming emails. Using **Google Gemini AI**, the workflow analyzes email content, classifies it into predefined categories, and performs automated actions such as sending replies, notifying teams, creating support tickets, archiving newsletters, and deleting spam.

This project demonstrates how AI can streamline email operations, improve response times, and reduce repetitive manual work.

---

## 🚀 Features

- 📥 Real-time Gmail Trigger
- 🤖 AI Email Classification using Google Gemini
- 📨 Automated Email Replies
- 🎯 Smart Email Routing
- 🔔 Slack Notifications
- 🎫 Support Ticket Creation
- 🏷 Automatic Gmail Labels & Archiving
- 🚫 Spam Detection & Deletion
- 📊 Structured JSON Output
- ⚡ Fully Automated n8n Workflow

---

## 🏗 Workflow Architecture

```text
New Email Received
        │
        ▼
Extract Email Data
        │
        ▼
Google Gemini AI
Email Classification
        │
        ▼
 Smart Routing
        │
 ┌──────┼──────────┬─────────────┐
 ▼      ▼          ▼             ▼
High   Support  Newsletter      Spam
Priority
 │       │          │             │
 ▼       ▼          ▼             ▼
Reply   Reply     Archive      Delete
 │       │
 ▼       ▼
Slack   Store Ticket
```

---

## 🧠 AI Classification Categories

The AI classifies incoming emails into one of the following categories:

| Category | Action |
|----------|--------|
| 🔴 High Priority | Auto Reply → Slack Notification → Archive |
| 💬 Customer Support | Auto Reply → Store Support Ticket |
| 📰 Newsletter | Archive & Apply Gmail Label |
| 🚫 Spam | Delete Email |

---

## ⚙ Workflow Components

### 📥 Gmail Trigger

Monitors your Gmail inbox and starts the workflow whenever a new email is received.

---

### 📄 Extract Email Data

Extracts important information including:

- Sender
- Subject
- Email Body
- Timestamp
- Attachments (Optional)

---

### 🤖 AI Email Classification

Google Gemini analyzes the email and returns structured JSON output.

Example:

```json
{
  "category": "Customer Support",
  "confidence": 0.98,
  "reason": "Customer needs assistance with login issue."
}
```

---

### 🎯 Smart Routing

Routes the email to the correct workflow based on AI prediction.

---

### 📧 Auto Reply

Automatically sends personalized responses for:

- Customer Support
- High Priority Emails

---

### 🔔 Slack Notification

High Priority emails generate instant Slack notifications containing:

- Sender
- Subject
- Category
- AI Summary

---

### 🎫 Support Ticket

Support emails are automatically stored in a ticket database.

Example fields:

- Customer Name
- Email
- Subject
- Category
- Status
- Created Date

---

### 🏷 Gmail Archive & Labels

Automatically organizes inbox by:

- Applying Labels
- Archiving Newsletters

---

### 🚫 Spam Management

Spam emails are automatically deleted.

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|----------|
| n8n | Workflow Automation |
| Gmail API | Email Management |
| Google Gemini AI | AI Classification |
| Slack | Team Notifications |
| JSON Schema | Structured Output |
| AI Agent | Intelligent Routing |

---

# 📂 Project Structure

```text
Automated-Email-Management-System/
│
├── README.md
├── workflow.json
├── screenshots/
│   └── workflow.png
├── docs/
│   ├── setup.md
│   ├── architecture.md
│   └── prompts.md
└── assets/
```

---

# ⚡ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Automated-Email-Management-System.git
```

```bash
cd Automated-Email-Management-System
```

---

## Import Workflow

1. Open **n8n**
2. Click **Import Workflow**
3. Select `workflow.json`

---

## Configure Credentials

Add credentials for:

- Gmail OAuth2
- Google Gemini API
- Slack OAuth

---

## Activate Workflow

Click **Execute Workflow** to test.

Then activate the workflow.

---

# 📊 Example Flow

### Incoming Email

```text
Subject:
Unable to login

Body:
Hi,
I'm unable to access my account.
Please help.
```

↓

AI Output

```json
{
  "category": "Customer Support",
  "confidence": 0.97
}
```

↓

Workflow Actions

- ✅ Auto Reply Sent
- ✅ Support Ticket Created

---

# 📈 Benefits

- Save hours of manual work
- Instant customer responses
- Intelligent AI classification
- Organized inbox
- Reduced response time
- Improved customer satisfaction
- Easy to customize
- Scalable workflow

---

# 🔮 Future Improvements

- Outlook Integration
- Microsoft Teams Notifications
- CRM Integration
- Sentiment Analysis
- Priority Scoring
- AI Generated Smart Replies
- Analytics Dashboard
- Knowledge Base Integration
- Human Approval Workflow

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create your feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Nadeem Ashraf**

📧 Email: nadeem.ashraf.dev@gmail.com

💼 LinkedIn: https://linkedin.com/in/nadeemashraf

🐙 GitHub: https://github.com/nadeemashraf

---

## ⭐ If you like this project, don't forget to give it a Star!
