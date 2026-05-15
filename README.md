# 📄 CV Checker

**CV Checker** is an AI-powered CV submission and analysis system. It allows candidates to submit their CVs, extracts the text from PDF files, and processes the data (via n8n and AI agents) to generate a comprehensive candidate match report. It also includes an automated HTML email system to send the results to applicants or recruiters.

![CV Checker](https://img.shields.io/badge/Status-Active-success)
![UI](https://img.shields.io/badge/UI-HTML%20%7C%20CSS%20%7C%20JS-blue)
![Backend](https://img.shields.io/badge/Backend-Python-yellow)

## ✨ Features

- **🎨 Beautiful UI**: A modern, responsive, dark-mode frontend interface for candidates to submit their CVs and view real-time analysis results.
- **📄 Robust PDF Extraction**: A Python script utilizing `pdfplumber` (with a fallback to `PyPDF2`) to accurately extract text from PDF CVs.
- **🧠 AI Analysis Parsing**: Parses structured JSON feedback from AI agents (typically connected via n8n).
- **📧 Automated Email Reports**: Automatically formats the AI results into a stunning HTML email or a terminal-friendly plain-text report and sends it via SMTP.
- **📊 Detailed Verdicts**: Scores candidates out of 100, determines a match verdict (Strong, Good, Partial, Weak), and highlights strengths, gaps, and missing keywords.

## 📂 Project Structure

- `index.html`: The frontend web interface for CV submission and displaying AI analysis results. Features smooth animations and a premium dark aesthetic.
- `extract_cv.py`: A standalone Python tool to extract text from a provided PDF file. Can output as plain text or JSON (ideal for n8n execution nodes).
- `parse_result.py`: A Python script that takes the AI's JSON output, formats it into a beautiful text or HTML report, and sends it out via email.

## 🚀 Getting Started

### 1. Frontend

Simply open `index.html` in any modern web browser to view the CV submission interface. If you are integrating this with a backend, you'll need to link the form submission to your n8n webhook or backend API.

### 2. Python Backend Tools

Ensure you have Python 3 installed. Install the required dependencies:

```bash
pip install pdfplumber PyPDF2
```

#### Extracting Text from a CV

Run the extractor script and pass the path to the PDF file:

```bash
# Get plain text output
python extract_cv.py path/to/cv.pdf

# Get JSON output (useful for n8n integrations)
python extract_cv.py path/to/cv.pdf --json
```

#### Parsing Results & Sending Emails

Before sending emails, open `parse_result.py` and configure your SMTP credentials:

```python
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password_here"
EMAIL_FROM    = "CV Checker <your_email@gmail.com>"
```

To parse an AI result and send an email:

```bash
python parse_result.py '{"match_score": 85, "verdict": "STRONG MATCH", "summary": "Great fit", "strengths": ["Python"], "gaps": [], "recommendations": "Hire", "keywords_matched": ["Python"], "keywords_missing": ["Docker"]}' --email applicant@example.com
```

## ⚙️ Integration with n8n

This repository is designed to be highly interoperable with **n8n**. 
1. Use the **Execute Command** node in n8n to call `extract_cv.py --json`.
2. Pass the extracted text to an AI node (like OpenAI) with a prompt to grade the CV against a job description.
3. Use the **Execute Command** node again to pass the AI's JSON response to `parse_result.py` to send the final email report.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
