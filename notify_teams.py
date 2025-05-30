#!/usr/bin/env python3

import os
import sys
import requests


def get_author_avatar(author: str) -> str:
    """Get the avatar URL for a GitHub user."""
    response = requests.get(f"https://api.github.com/users/{author}")
    response.raise_for_status()
    return response.json()["avatar_url"]


def create_teams_message(review_data):
    """Create a Teams message card with PR review information."""
    # Determine badge text and style based on review state
    review_state = os.getenv("REVIEW_STATE", "")
    badge_text = review_state.replace("_", " ").title()
    
    # Map review states to badge styles
    badge_styles = {
        "APPROVED": "Good",
        "CHANGES_REQUESTED": "Attention",
        "COMMENTED": "Default"
    }
    badge_style = badge_styles.get(review_state, "Default")
    
    # Get reviewer's avatar URL
    reviewer = os.getenv("REVIEWER", "")
    try:
        reviewer_avatar_url = get_author_avatar(reviewer)
    except requests.exceptions.RequestException:
        # Fallback to GitHub's default avatar if the request fails
        reviewer_avatar_url = f"https://github.com/identicons/{reviewer}.png"
    
    # Create the message card
    message = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "speak": "Pull request reviewed",
                    "type": "AdaptiveCard",
                    "version": "1.5",
                    "body": [
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Image",
                                            "size": "Medium",
                                            "style": "RoundedCorners",
                                            "url": os.getenv("BOT_IMAGE_URL")
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**Pull Request Notifier**",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**{os.getenv('REPO')}**",
                                            "wrap": True,
                                            "color": "Good"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Badge",
                                            "text": badge_text,
                                            "size": "Large",
                                            "style": badge_style,
                                            "shape": "Rounded",
                                            "appearance": "Tint"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "TextBlock",
                            "text": f"#{os.getenv('PR_NUMBER')} - {os.getenv('PR_TITLE')}",
                            "wrap": True,
                            "size": "ExtraLarge",
                            "weight": "Bolder",
                            "color": "Accent"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "Image",
                                            "size": "Small",
                                            "style": "Person",
                                            "url": reviewer_avatar_url
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": f"**{reviewer}** {os.getenv('EVENT')} the pull request review.",
                                            "size": "Large",
                                            "wrap": True,
                                            "spacing": "Small"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Global comment:** {os.getenv('GLOBAL_COMMENT')}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Number of comments:** {os.getenv('COMMENTS_COUNT')}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Head:** {os.getenv('HEAD_REF')}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"**Base:** {os.getenv('BASE_REF')}",
                                            "wrap": True,
                                            "spacing": "Small"
                                        }
                                    ],
                                    "verticalContentAlignment": "Center"
                                }
                            ]
                        }
                    ],
                    "msteams": {
                        "width": "full"
                    },
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "View pull request",
                            "url": os.getenv("PR_URL")
                        }
                    ],
                    "msTeams": {
                        "width": "full"
                    }
                }
            }
        ]
    }
    
    return message


def send_teams_notification(webhook_url):
    """Send notification to Microsoft Teams."""
    message = create_teams_message({})
    
    try:
        response = requests.post(
            webhook_url,
            json=message,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print("Successfully sent notification to Teams")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification to Teams: {str(e)}")
        return False


def main():
    # Get webhook URL from environment variable
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("Error: TEAMS_WEBHOOK_URL environment variable is not set")
        sys.exit(1)

    # Send notification
    success = send_teams_notification(webhook_url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
