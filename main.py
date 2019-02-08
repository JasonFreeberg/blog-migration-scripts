
import sys
import os
import shutil
from migration import helpers


def main(argv):
    input_dir = argv[0]
    output_dir = argv[1]

    print("Input directory: " + input_dir)
    print("Output directory: " + output_dir)

    helpers.copy_files(input_dir, output_dir)
    print("Copied files to output directory.")

    try:
        for f in helpers.get_html_files(output_dir):
            print("Editing file: " + os.path.basename(f))
            helpers.edit_src_and_href_paths(f)
            helpers.add_header_markup(f)
            helpers.remove_title_tag(f)
            helpers.update_file_name(f) # Update the file name last
    except Exception as e:
        print(e)
        print('Batch process failed. Deleting the contents of the output directory.')
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)

    print('Done.')
    exit()


if __name__ == "__main__":
    main(sys.argv[1:])
