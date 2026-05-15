
# 📄 CV Checker

**CV Checker** is an automated AI-powered CV submission and analysis system. The entire backend operations and logic are seamlessly orchestrated using **n8n** (Node-based automation), transforming a simple form submission into an intelligent candidate evaluation pipeline.

![Status](https://img.shields.io/badge/Status-Active-success)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-blue)
![Backend](https://img.shields.io/badge/Backend-n8n%20%7C%20Python-orange)

## 🌟 How It Works (The n8n Backend)

Unlike traditional backends, CV Checker relies on **n8n workflows** to handle everything from receiving the file to analyzing it and dispatching emails. 

Here is the complete workflow execution in n8n:
1. **Webhook Receiver:** The `index.html` frontend submits the user's CV via a POST request directly to an n8n Webhook node.
2. **PDF Extraction:** n8n passes the file to an **Execute Command** node that runs the `extract_cv.py` helper script to extract the plain text from the PDF.
3. **AI Analysis:** n8n takes the extracted text and sends it to an **AI Node** (e.g., OpenAI) equipped with a strict system prompt to evaluate the CV against a job description. The AI returns a highly structured JSON object (Score, Verdict, Strengths, Gaps, Keywords).
4. **Email Dispatch:** The AI's JSON output is then passed to another **Execute Command** node running `parse_result.py`, which formats the data into a stunning HTML email and sends it to the candidate.
5. **Frontend Response:** n8n responds back to the frontend with the JSON result, triggering the UI to display the final verdict and smooth animations.

## ✨ Features

- **⚙️ n8n Powered Workflow**: No traditional backend code is needed; the entire pipeline is visually built and executed in n8n.
- **🎨 Premium UI**: A modern, glassmorphism dark-mode frontend interface for candidates to submit their CVs.
- **📄 Robust PDF Extraction**: Python script utilizing `pdfplumber` to accurately extract text, executed via n8n.
- **🧠 AI Agent Integration**: Deep integration with AI models to intelligently score candidates.
- **📧 Automated Email Reports**: Sends beautifully formatted HTML emails automatically using SMTP within the n8n flow.

## 📂 Project Structure

- `index.html`: The beautiful frontend. Simply point its API endpoint to your n8n Webhook URL.
- `extract_cv.py`: Python helper script for n8n. Extracts text from PDFs and returns JSON.
- `parse_result.py`: Python helper script for n8n. Parses AI JSON feedback and sends the stylized HTML email.

## 🚀 Getting Started

### 1. Setting up the n8n Workflow

1. Install and run **n8n**.
2. Create a new Workflow with a Webhook trigger.
3. Ensure the environment running n8n has Python 3 installed along with dependencies:
   ```bash
   pip install pdfplumber PyPDF2
   ```
4. Add **Execute Command** nodes to trigger the python files whenever necessary.
   - *Example Extract Node:* `python /path/to/extract_cv.py /tmp/cv.pdf --json`
   - *Example Email Node:* `python /path/to/parse_result.py '{{$json.ai_response}}' --email candidate@email.com`

*(Note: Open `parse_result.py` and input your SMTP credentials inside the file before running).*

### 2. Setting up the Frontend

1. Open `index.html`.
2. Update the Javascript fetch URL to point to your **n8n Webhook URL**.
3. Host `index.html` on any static provider (Vercel, GitHub Pages, Netlify) or just open it locally in your browser.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
