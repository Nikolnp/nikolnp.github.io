import streamlit as st

# Function to create draggable block using HTML and JavaScript
def draggable_block():
    return f"""
        <div id="draggable-block" draggable="true" ondragstart="drag(event)" style="width: 80px; height: 80px; background-color: #4CAF50; color: white; text-align: center; padding: 10px; cursor: move;">
            Block
        </div>
        <script>
            function drag(event) {{
                event.dataTransfer.setData("text", event.target.id);
            }}
        </script>
    """

# Streamlit app
def main():
    st.title("Drag and Drop Programming for Kids")

    # Display the draggable block
    st.markdown(draggable_block(), unsafe_allow_html=True)

    # Display drop area
    drop_area = st.markdown("<div id='code-area' ondrop='drop(event)' ondragover='allowDrop(event)' style='width: 400px; height: 300px; border: 1px solid #ccc; margin: 20px; padding: 10px; position: relative;'></div>", unsafe_allow_html=True)

    # Display output area
    output_area = st.empty()

    # JavaScript code for drop and allowDrop functions
    js_code = """
        <script>
            function allowDrop(event) {
                event.preventDefault();
            }

            function drop(event) {
                event.preventDefault();
                var data = event.dataTransfer.getData("text");

                // Display the block position in the output
                var outputContent = document.getElementById("output-content");
                var x = event.clientX - outputContent.getBoundingClientRect().left;
                var y = event.clientY - outputContent.getBoundingClientRect().top;
                outputContent.innerHTML = "Block dropped at X: " + x + ", Y: " + y;

                // Remove the draggable block from the code area
                var draggableBlock = document.getElementById("draggable-block");
                draggableBlock.remove();
            }
        </script>
    """
    
    # Add JavaScript code to the output area
    output_area.markdown(js_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
