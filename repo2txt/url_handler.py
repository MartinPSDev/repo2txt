import re

def normalize_github_url(url):
    """Normalize various GitHub URL formats to a consistent format."""
    # Remove trailing slashes
    url = url.rstrip('/')
    
    # Handle git@ URLs
    if url.startswith('git@github.com:'):
        return url
    
    # Handle short format (user/repo)
    if re.match(r'^[\w-]+/[\w-]+$', url):
        return f'https://github.com/{url}'
    
    # Handle full HTTPS URLs
    if url.startswith('https://github.com/'):
        return url
    
    raise ValueError('Invalid GitHub repository URL format')

def get_repo_name(url):
    """Extract repository name from URL."""
    if url.endswith('.git'):
        url = url[:-4]
    return url.split('/')[-1]