import sys
import argparse
import requests

def get_trending_repos(language=""):
    url = "https://api.github.com/search/repositories"
    query = "stars:>100 sort:stars-desc"
    if language:
        query += f" language:{language}"
    
    params = {"q": query, "per_page": 10}
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Error fetching data: Status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Network error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch trending GitHub repositories via CLI.")
    parser.add_argument("-l", "--language", type=str, default="", help="Filter by programming language (e.g., python, javascript, java)")
    args = parser.parse_args()

    print(f"\n🔍 Fetching top trending GitHub repositories" + (f" for [{args.language}]" if args.language else "") + "...\n")
    
    repos = get_trending_repos(args.language)
    
    if not repos:
        print("No repositories found.")
        return

    for idx, repo in enumerate(repos, 1):
        name = repo.get("full_name")
        description = repo.get("description") or "No description provided."
        stars = repo.get("stargazers_count")
        lang = repo.get("language") or "N/A"
        url = repo.get("html_url")

        print(f"{idx}. 🌟 {name} ({lang}) - {stars} stars")
        print(f"   📖 {description}")
        print(f"   🔗 {url}\n")

if __name__ == "__main__":
    main()
