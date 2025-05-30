# Notify PR Reviews to Microsoft Teams

![License](https://img.shields.io/badge/license-Apache%202.0-blue)

This GitHub Action sends pull request review notifications to a Microsoft Teams channel. It provides detailed information about PR reviews, including reviewer details, review state, comments, and branch information.

## 🚀 Features

- Sends a Microsoft Teams Adaptive Card with PR review information
- Displays PR details (number, title, branches)
- Shows reviewer information with their GitHub avatar
- Includes review state (APPROVED, CHANGES_REQUESTED, COMMENTED)
- Shows number of comments and global review comment
- Provides link to view the pull request
- Easily reusable across repositories

## 📦 Usage

### Step 1: Add to Your Workflow

```yaml
name: PR Review Notification

on:
  pull_request_review:
    types: [submitted, edited, dismissed]

jobs:
  notify-teams:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Microsoft Teams
        uses: your-org/notify-pr-reviews-teams-action@v1
        with:
          webhook_url: ${{ secrets.TEAMS_WEBHOOK_URL }}
          bot_image_url: https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png
          repo: ${{ github.repository }}
          pr_number: ${{ github.event.pull_request.number }}
          pr_title: ${{ github.event.pull_request.title }}
          reviewer: ${{ github.event.review.user.login }}
          review_state: ${{ github.event.review.state }}
          global_comment: ${{ github.event.review.body || 'No comment provided' }}
          comments_count: ${{ github.event.review.comments || 0 }}
          head_ref: ${{ github.event.pull_request.head.ref }}
          base_ref: ${{ github.event.pull_request.base.ref }}
          event: ${{ github.event.action }}
          pr_url: ${{ github.event.pull_request.html_url }}
```



