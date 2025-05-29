import os, shutil, re
from src.transformation import markdown_to_html_node
from src.htmlnode import HTMLNode

def create_dest_folder(dest_path):
    # Create /public if it does not already exist
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        print(f'Destination folder created at: {dest_path}')

    # Delete folder contents
    for filename in os.listdir(dest_path):
        print(filename)
        file_path = os.path.join(dest_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def copy_contents(src_path, dest_path):
    print(f'Source path is: {src_path}')
    src_file_names = os.listdir(src_path)
    print(f'File names at source path: {src_file_names}')
    for file_name in src_file_names:
        src_file = os.path.abspath(os.path.join(src_path, file_name))
        if os.path.isdir(src_file):
            print(f'Copying directory: {src_file}')
            dest_dir = os.path.abspath(os.path.join(dest_path, file_name))
            print(f'Destination directory: {dest_dir}')
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            copy_contents(src_file, dest_dir)
        elif os.path.isfile(src_file):
            print(f'Coyping file: {src_file}')
            dest_file = os.path.abspath(os.path.join(dest_path, file_name))
            print(f'Destination path: {dest_file}')
            paste_path = shutil.copy(src_file, dest_file)
            print(f'New file at: {paste_path}')

def extract_title(markdown):
    heading = re.findall(r'^[\n]*# (.*)', markdown)
    if heading:
        [heading] = heading
        return heading
    else:
        raise ValueError("no title found")

def generate_page(from_path, template_path, dest_path,base_path = '/'):
    print(from_path)
    print(f'Generating page from {from_path} to {dest_path} using {template_path}.')
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'href="{base_path}')
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Html generated at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path = '/'):
    print(f'Source path is: {dir_path_content}')
    src_file_names = os.listdir(dir_path_content)
    print(f'File names at source path: {src_file_names}')
    for file_name in src_file_names:
        src_file = os.path.abspath(os.path.join(dir_path_content, file_name))
        if os.path.isdir(src_file):
            print(f'Copying directory: {src_file}')
            dest_dir = os.path.abspath(os.path.join(dest_dir_path, file_name))
            print(f'Destination directory: {dest_dir}')
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            generate_pages_recursive(src_file, template_path, dest_dir, base_path)
        if os.path.isfile(src_file):
            print(f'Coyping file: {src_file}')
            if file_name[-3:] == '.md':
                file_name = file_name[:-3] + '.html'
                dest_file = os.path.abspath(os.path.join(dest_dir_path, file_name))
                print(f'Destination path: {dest_file}')
                generate_page(src_file, template_path, dest_file)
            else:
                continue




    
    


