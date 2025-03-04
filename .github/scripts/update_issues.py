import os
import re
from github import Github

# 获取 GitHub Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')  # 获取仓库名称

# 初始化 GitHub API
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 定义 Markdown 文件所在的目录
DOCS_DIR = 'backup'

def get_issue_by_title(title):
    """根据标题查找对应的 Issue"""
    issues = repo.get_issues(state='open')
    for issue in issues:
        if issue.title == title:
            return issue
    return None

def create_issue(title, content):
    """创建新的 Issue"""
    repo.create_issue(title=title, body=content, labels=['documentation'])

def update_issue(issue, content):
    """更新已有的 Issue"""
    issue.edit(body=content)

def process_md_file(file_path):
    """处理 Markdown 文件"""
    with open(file_path, 'r') as file:
        content = file.read()

    # 获取文件名（不包含后缀）
    file_name = os.path.basename(file_path).replace('.md', '')

    # 查找对应的 Issue
    issue = get_issue_by_title(file_name)

    if issue:
        # 如果 Issue 存在，则更新内容
        update_issue(issue, content)
        print(f"Updated issue: {file_name}")
    else:
        # 如果 Issue 不存在，则创建新的 Issue
        create_issue(file_name, content)
        print(f"Created new issue: {file_name}")

def main():
    # 遍历 docs 目录下的所有 .md 文件
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_md_file(file_path)

if __name__ == "__main__":
    main()
