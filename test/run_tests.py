
from migration import helpers
from main import main
from main import main
import shutil
import os


input_dir = os.path.join(os.getcwd(), "test_sources")
output_dir = os.path.join(os.getcwd(), "test_target")


def clear_test_target():
    for filename in os.listdir(output_dir):
        filepath = os.path.join(output_dir, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


def test_copy_files():
    clear_test_target()
    helpers.copy_files(input_dir, output_dir)


def test_update_file_names():
    clear_test_target()
    helpers.copy_files(input_dir, output_dir)

    for f in helpers.get_html_files(output_dir):
        helpers.update_file_name(f)


def test_get_html_files():
    clear_test_target()
    helpers.copy_files(input_dir, output_dir)
    print(helpers.get_html_files(output_dir))


def test_edit_src_and_href_paths():
    clear_test_target()
    helpers.copy_files(input_dir, output_dir)

    for f in helpers.get_html_files(output_dir):
        helpers.edit_src_and_href_paths(f)


def test_add_header_markup():
    clear_test_target()
    helpers.copy_files(input_dir, output_dir)

    for f in helpers.get_html_files(output_dir):
        helpers.add_header_markup(f)


def test_end_to_end():
    clear_test_target()
    main([input_dir, output_dir])


# Just put the test method you wnat to run here and execute the whole file in PyCharm... lol
test_end_to_end()