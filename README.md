# AWS Solutions Architect Quiz App

An interactive web-based quiz application for studying and preparing for the AWS Certified Solutions Architect - Associate exam. This project contains practice questions organized by AWS domains and services.

## 📋 Project Overview

This is a simple HTML-based quiz application that helps you practice AWS certification questions. The app loads questions from JSON files and provides an interactive interface for testing your knowledge.

## 📁 Project Structure

```
AWS/
├── aws_saa_quiz_app.html          # Main quiz application
├── questions/                     # Practice questions by category
│   ├── domain1-secure-architectures.json
│   ├── domain2-resilient-architectures.json
│   ├── domain3-high-performing-architectures.json
│   ├── domain4-cost-optimized-architectures.json
│   ├── ec2.json
│   ├── s3.json
│   ├── rds.json
│   ├── lambda.json
│   ├── vpc.json
│   └── ... (other service-specific questions)
├── backup/                        # Backup copies of questions
├── start_quiz.py                  # Python script to run the quiz
└── tools/lint_decks.py           # Utility script for question validation
```

## 🚀 How to Use

### Web Quiz App
1. Open `aws_saa_quiz_app.html` in your web browser
2. Select a question category from the dropdown
3. Answer questions and get immediate feedback
4. Track your score and progress

### Python Quiz Runner
```bash
# Run the quiz with Python
python start_quiz.py
```

## 📚 Question Categories

### AWS Exam Domains
- **Domain 1**: Secure Architectures
- **Domain 2**: Resilient Architectures  
- **Domain 3**: High-Performing Architectures
- **Domain 4**: Cost-Optimized Architectures

### Service-Specific Questions
- EC2 (Elastic Compute Cloud)
- S3 (Simple Storage Service)
- RDS (Relational Database Service)
- Lambda (Serverless Computing)
- VPC (Virtual Private Cloud)
- And more...

## 🛠️ Technical Details

- **Frontend**: Pure HTML, CSS, and JavaScript
- **Data Format**: JSON files for questions
- **No Dependencies**: Runs entirely in the browser
- **Portable**: Can be used offline

## 📊 Features

- Interactive quiz interface
- Multiple question categories
- Immediate feedback on answers
- Score tracking
- Explanations for correct answers
- Responsive design

## 🔧 Question Format

Each question in the JSON files follows this structure:
```json
{
  "question": "Question text here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 0,
  "explanation": "Explanation for why this answer is correct"
}
```

## � Adding New Questions

1. Edit the appropriate JSON file in the `questions/` directory
2. Follow the question format shown above
3. Use the `lint_decks.py` script to validate the format

## 🤝 Contributing

Feel to contribute by:
- Adding new practice questions
- Improving explanations
- Fixing any bugs in the quiz app
- Enhancing the user interface

## 📄 License

This project is for educational purposes to help with AWS certification preparation.

---

**Happy Studying! 🚀**
