#!/bin/bash
# setup_github.sh – Chạy 1 lần để khởi tạo Git repo
# Usage: bash setup_github.sh <github-username> <repo-name>
#
# Ví dụ: bash setup_github.sh B22DCAT249 quiz-trivia-tooltest

USERNAME=${1:-"your-github-username"}
REPO=${2:-"quiz-trivia-tooltest"}

echo "=== Khởi tạo Git repo: $USERNAME/$REPO ==="

git init
git add .
git commit -m "feat: initial tool test structure

- data/: 7 Excel files (TC_Login, TC_QuizCoreFlow, TC_QuizManagement,
         TC_AIFeatures, TC_Postman, TC_JMeter, TC_Master_Index)
- selenium/scripts/conftest.py: fixtures + Firebase helper + ExcelResultWriter
- .github/workflows/selenium_ci.yml: CI pipeline
- README.md: setup & run instructions"

echo ""
echo "=== Tạo remote và push ==="
echo "Chạy các lệnh sau (thay YOUR_TOKEN bằng GitHub Personal Access Token):"
echo ""
echo "  git remote add origin https://github.com/$USERNAME/$REPO.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "Hoặc dùng GitHub CLI:"
echo "  gh repo create $REPO --public --source=. --push"
