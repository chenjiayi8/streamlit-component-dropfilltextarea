from pathlib import Path
from typing import Optional

import os
import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = False

# Tell streamlit that there is a component called st_dropfill_textarea,
# and that the code to display that component is in the "frontend" folder

if not _RELEASE:
    _component_func = components.declare_component(
        "dropfill_textarea",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "dropfill_textarea", path=build_dir)

# Create the python function that will be called
def st_dropfill_textarea(
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        key=key,
    )

    return component_value


def main():
    st.write("## Example")
    value = st_dropfill_textarea()

    st.write(value)


if __name__ == "__main__":
    main()
