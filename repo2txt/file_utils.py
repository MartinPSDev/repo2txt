import os

def is_binary_file(file_path):
    """Check if a file is binary."""
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read(1024)
            return False
    except UnicodeDecodeError:
        return True

def format_file_size(size):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def split_file(input_file, mb_size):
    """Split a file into multiple files of specified size in MB."""
    bytes_per_file = int(mb_size * 1024 * 1024)  # Convert MB to bytes
    base_name, extension = os.path.splitext(input_file)
    extension = extension.lstrip('.')  # Remove the dot

    # Check if file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        return 0

    # Get total file size
    total_size = os.path.getsize(input_file)
    if total_size == 0:
        print("Error: Input file is empty.")
        return 0

    print(f"Input file: {input_file} ({format_file_size(total_size)})")
    print(f"Splitting into parts of size: {mb_size} MB")

    current_part = 1
    bytes_read = 0

    with open(input_file, 'rb') as infile:
        while bytes_read < total_size:
            # Create output filename
            output_file = f"{base_name}_Part{current_part}.{extension}" if extension else f"{base_name}_Part{current_part}"
            
            with open(output_file, 'wb') as outfile:
                chunk = infile.read(bytes_per_file)
                if not chunk:  # End of file
                    break
                
                outfile.write(chunk)
                print(f"Created file: {output_file} ({format_file_size(len(chunk))})")
                
                bytes_read += len(chunk)
                current_part += 1

    print(f"Finished splitting. Total parts created: {current_part - 1}")
    return current_part - 1
