import os
import subprocess
import tempfile
import shutil
from .file_utils import is_binary_file, format_file_size
from .url_handler import normalize_github_url

class RepositoryProcessor:
    def __init__(self, repo_url):
        self.repo_url = normalize_github_url(repo_url)
        self.temp_dir = None

    def clone_repository(self):
        """Clone the repository to a temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        print(f"Downloading repository...")
        git_cmd = ['git', 'clone', '--depth', '1', self.repo_url, self.temp_dir]
        subprocess.run(git_cmd, check=True, capture_output=True)

    def process_files(self, output_file):
        """Process repository files and write to output file."""
        print("Processing files...")
        with open(output_file, 'w', encoding='utf-8') as out:
            for root, _, files in os.walk(self.temp_dir):
                # Skip .git directory
                if '.git' in root:
                    continue

                for file in files:
                    self._process_single_file(root, file, out)

        print(f"Repository contents saved to: {output_file}")

    def _process_single_file(self, root, file, out):
        """Process a single file from the repository."""
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, self.temp_dir)
        
        # Skip binary files
        if is_binary_file(file_path):
            return

        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Write file header
        out.write('=' * 80 + '\n')
        out.write(f"File: {rel_path}\n")
        out.write(f"Size: {format_file_size(file_size)}\n")
        out.write('=' * 80 + '\n\n')

        # Write file contents
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                out.write(f.read())
            out.write('\n\n')
        except UnicodeDecodeError:
            pass

    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir:
            print("Cleaning up temporary files...")
            shutil.rmtree(self.temp_dir, ignore_errors=True)