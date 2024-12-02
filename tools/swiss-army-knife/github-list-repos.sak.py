import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('--username', help='GitHub username to list repositories for')
    args = parser.parse_args()

    if args.info:
        print("""
Tool Name: GitHub Repository Lister
Description: Lists public repositories for a given GitHub username
Usage: swiss-army-knife github-list-repos --username <github_username>
Arguments:
  --username: GitHub username to list repositories for
Example:
  swiss-army-knife github-list-repos --username octocat
        """)
        return

    # Implementation here
    pass

if __name__ == '__main__':
    main()