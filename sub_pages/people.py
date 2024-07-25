import streamlit as st


st.header("People")


# Step 1: Create an empty container
containers = [st.empty() for i in range(3)]

# Step 2: Add elements to the container
for index, container in enumerate(containers):
    with container:
        with st.expander("test"):
            st.write(index)
            if st.button("Click to remove", key=index):
                container.empty()

# Step 3: Clear the container when the button is clicked
