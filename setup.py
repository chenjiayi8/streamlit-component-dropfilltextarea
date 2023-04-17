from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-component-dropfilltextarea",
    version="0.1.0",
    author="Jiayi Chen",
    author_email="chenjiayi_344@hotmail.com",
    description="Streamlit Component DropFillTextarea allows you to drag and drop files onto a text area, making it easy to fill in large amounts of text quickly. With dropfill_textarea, users can quickly populate text areas with pre-existing text files, reducing manual input and increasing efficiency. The component also offers flexible layout options, allowing users to customize the label and text area's size, position, and other properties. Whether you're a developer or a user, dropfill_textarea is the perfect solution for simplifying your workflow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "jinja2"],
)
