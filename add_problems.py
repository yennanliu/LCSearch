#!/usr/bin/env python3
"""
Script to add LC problems from doc/*.txt files to lc_search_ui/public/data/problems.json
Only adds problems that don't already exist.
"""
import json
import re
from datetime import datetime
from pathlib import Path


def parse_problem_line(line):
    """Parse a problem line from the txt files."""
    # Example line format:
    # 026 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)|  [Python]...

    line = line.strip()
    if not line or line.startswith('#') or line.startswith('||'):
        return None

    # Extract problem number (first 3-4 digits)
    match = re.match(r'(\d+)\s*\|', line)
    if not match:
        return None

    problem_id = int(match.group(1))

    # Extract title and URL from markdown link
    title_match = re.search(r'\[([^\]]+)\]\((https://leetcode\.com/problems/[^\)]+/)\)', line)
    if not title_match:
        return None

    title = title_match.group(1)
    url = title_match.group(2)

    # Extract difficulty
    difficulty = 'Medium'  # Default
    if 'Easy' in line:
        difficulty = 'Easy'
    elif 'Hard' in line:
        difficulty = 'Hard'
    elif 'Medium' in line:
        difficulty = 'Medium'

    # Extract tags/patterns
    tags = []
    patterns = []
    companies = []

    # Look for common tags
    if 'Array' in line or 'array' in line:
        tags.append('Array')
    if 'String' in line or 'string' in line:
        tags.append('String')
    if 'Hash' in line or 'hash' in line:
        tags.append('Hash Table')
    if 'Tree' in line or 'tree' in line:
        tags.append('Tree')
    if 'Graph' in line or 'graph' in line:
        tags.append('Graph')
    if 'Stack' in line or 'stack' in line:
        tags.append('Stack')
    if 'Queue' in line or 'queue' in line:
        tags.append('Queue')
    if 'Heap' in line or 'heap' in line:
        tags.append('Heap')
    if 'DP' in line or 'Dynamic Programming' in line:
        tags.append('Dynamic Programming')
    if 'Backtrack' in line or 'backtrack' in line:
        tags.append('Backtracking')
    if 'Binary Search' in line or 'binary search' in line:
        tags.append('Binary Search')
    if 'Two Pointer' in line or 'two pointer' in line:
        patterns.append('Two Pointers')
    if 'Sliding Window' in line or 'sliding window' in line:
        patterns.append('Sliding Window')
    if 'DFS' in line or 'dfs' in line:
        patterns.append('DFS')
    if 'BFS' in line or 'bfs' in line:
        patterns.append('BFS')
    if 'Union Find' in line or 'union find' in line:
        patterns.append('Union Find')
    if 'Trie' in line or 'trie' in line:
        tags.append('Trie')

    # Extract companies
    company_patterns = [
        (r'`google`', 'Google'),
        (r'`amazon`', 'Amazon'),
        (r'`fb`', 'Facebook'),
        (r'`apple`', 'Apple'),
        (r'`microsoft`', 'Microsoft'),
        (r'`M\$`', 'Microsoft'),
        (r'`uber`', 'Uber'),
        (r'`linkedin`', 'LinkedIn'),
        (r'`bloomberg`', 'Bloomberg'),
    ]

    for pattern, company in company_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            companies.append(company)

    # Remove duplicates
    tags = list(set(tags)) if tags else ['Array']  # Default to Array if no tags found
    patterns = list(set(patterns)) if patterns else ['General']
    companies = list(set(companies)) if companies else []

    return {
        'id': problem_id,
        'title': title,
        'difficulty': difficulty,
        'url': url,
        'tags': tags,
        'patterns': patterns,
        'companies': companies,
        'dateAdded': datetime.now().strftime('%Y-%m-%d'),
        'description': f'{title} - {difficulty} level problem.'
    }


def load_existing_problems(json_path):
    """Load existing problems from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    # Create a dict of existing problem IDs
    existing_ids = {p['id'] for p in problems}
    return problems, existing_ids


def parse_txt_file(txt_path):
    """Parse problems from a txt file."""
    problems = []

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            problem = parse_problem_line(line)
            if problem:
                problems.append(problem)

    return problems


def main():
    # Paths
    project_root = Path(__file__).parent
    json_path = project_root / 'lc_search_ui/public/data/problems.json'
    must_txt = project_root / 'doc/must_problems.txt'
    again_txt = project_root / 'doc/again_problems.txt'

    # Load existing problems
    print(f"Loading existing problems from {json_path}...")
    existing_problems, existing_ids = load_existing_problems(json_path)
    print(f"Found {len(existing_problems)} existing problems")

    # Parse new problems from txt files
    new_problems = []

    print(f"\nParsing {must_txt}...")
    must_problems = parse_txt_file(must_txt)
    print(f"Found {len(must_problems)} problems in must_problems.txt")

    print(f"\nParsing {again_txt}...")
    again_problems = parse_txt_file(again_txt)
    print(f"Found {len(again_problems)} problems in again_problems.txt")

    # Combine and deduplicate
    all_new = must_problems + again_problems

    # Filter out existing problems
    for problem in all_new:
        if problem['id'] not in existing_ids:
            new_problems.append(problem)
            existing_ids.add(problem['id'])

    print(f"\nFound {len(new_problems)} new problems to add")

    if new_problems:
        # Add new problems to existing
        combined = existing_problems + new_problems

        # Sort by ID
        combined.sort(key=lambda x: x['id'])

        # Save back to JSON
        print(f"\nSaving {len(combined)} total problems to {json_path}...")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)

        print(f"\nSuccess! Added {len(new_problems)} new problems.")
        print(f"Total problems in database: {len(combined)}")

        # Show sample of added problems
        print("\nSample of added problems:")
        for p in new_problems[:5]:
            print(f"  - {p['id']:04d}: {p['title']} ({p['difficulty']})")
        if len(new_problems) > 5:
            print(f"  ... and {len(new_problems) - 5} more")
    else:
        print("\nNo new problems to add. All problems already exist in problems.json.")


if __name__ == '__main__':
    main()
