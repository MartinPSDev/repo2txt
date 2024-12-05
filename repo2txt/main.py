import sys
from .repository import RepositoryProcessor
from .url_handler import get_repo_name

def main():
    """Main function to handle script execution."""
    if len(sys.argv) != 2:
        print("Usage: repo2txt <repository-url>")
        print("Example: repo2txt https://github.com/username/repository")
        print("         repo2txt username/repository")
        sys.exit(1)

    repo_url = sys.argv[1]
    processor = None

    try:
        repo_name = get_repo_name(repo_url)
        output_file = f"{repo_name}.txt"
        
        processor = RepositoryProcessor(repo_url)
        processor.clone_repository()
        processor.process_files(output_file)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if processor:
            processor.cleanup()