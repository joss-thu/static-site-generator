import os, sys
from src.site_operations import (
    create_dest_folder, copy_contents, generate_page,
    generate_pages_recursive
)


if __name__ == "__main__":
    # ------------------------------------------------------------------------
    # Copy static assets into the public folder
    # ------------------------------------------------------------------------
    # Resolve filapaths irrespective of where the script is run from
    # ----------------
    print('''
-------------------------------------------
Copying static files..
___________________________________________        
''')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_path = os.path.join(script_dir, '../public')
    dest_path = os.path.abspath(dest_path)

    src_path = os.path.join(script_dir, './static')
    src_path = os.path.abspath(src_path)
    
    create_dest_folder(dest_path)
    copy_contents(src_path, dest_path)
    # -----------------------------------
    # or use,
    # shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    # ------------------------------------------------------------------------
    # Generate the Html docuemnt from the markdown file recursively
    # ------------------------------------------------------------------------
    print('''
-------------------------------------------
Generating html..
___________________________________________        
''')
    curr_dir = os.path.dirname(__file__)

    dir_path_content = os.path.join(curr_dir, '../content/')
    dir_path_content = os.path.abspath(dir_path_content)

    template_path = os.path.join(curr_dir, '../template.html')
    template_path = os.path.abspath(template_path)

    dest_dir_path = os.path.join(curr_dir, '../public/')
    dest_dir_path = os.path.abspath(dest_dir_path)

    base_path = '/'
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    
    print(f'Base url changed to: {base_path}')

    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path)
    
