import sys
import argparse
from .repository import RepositoryProcessor
from .url_handler import get_repo_name
from .file_utils import split_file

def main():
    """Main function to handle script execution."""
    parser = argparse.ArgumentParser(description='Convert GitHub repository to text file')
    parser.add_argument('repo_url', help='GitHub repository URL')
    parser.add_argument('-f', '--fragment', type=float, help='Split output into files of specified size in MB')
    args = parser.parse_args()

    processor = None

    try:
        repo_name = get_repo_name(args.repo_url)
        output_file = f"{repo_name}.txt"
        
        processor = RepositoryProcessor(args.repo_url)
        processor.clone_repository()
        processor.process_files(output_file)

        if args.fragment:
            print(f"\nSplitting file into {args.fragment}MB parts...")
            num_files = split_file(output_file, args.fragment)
            print(f"\nFile split into {num_files} parts")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if processor:
            processor.cleanup()