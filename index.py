import streamlit as st

# Function to create draggable animal block using HTML and JavaScript
def draggable_animal(name, color):
    return f"""
        <div id="{name.lower()}-block" draggable="true" ondragstart="drag(event)" style="width: 80px; height: 80px; background-color: {color}; color: white; text-align: center; padding: 10px; cursor: move;">
            {name}
        </div>
    """

# Streamlit app
def main():
    st.title("Drag Animals to the Farm")

    # Display draggable animal blocks
    st.markdown(draggable_animal("Dog", "brown"), unsafe_allow_html=True)
    st.markdown(draggable_animal("Cat", "gray"), unsafe_allow_html=True)
    st.markdown(draggable_animal("Cow", "black"), unsafe_allow_html=True)
    st.markdown(draggable_animal("Chicken", "orange"), unsafe_allow_html=True)

    # Display farm area
    farm_area = st.markdown("<div id='farm-area' ondrop='drop(event)' ondragover='allowDrop(event)' style='width: 400px; height: 300px; border: 1px solid #ccc; margin: 20px; padding: 10px; position: relative;'></div>", unsafe_allow_html=True)

    # Display output area
    output_area = st.empty()

    # JavaScript code for drop and allowDrop functions
    js_code = """
        <script>
            function allowDrop(event) {
                event.preventDefault();
            }

            function drag(event) {
                event.dataTransfer.setData("text", event.target.id);
            }

            function drop(event) {
                event.preventDefault();
                var data = event.dataTransfer.getData("text");

                // Display the animal dropped into the farm
                var outputContent = document.getElementById("output-content");
                var animalName = data.split("-")[0];
                outputContent.innerHTML = "Dropped a " + animalName + " into the farm!";

                // Remove the draggable animal block from the farm area
                var draggableAnimal = document.getElementById(data);
                draggableAnimal.remove();
            }
        </script>
    """
    
    # Add JavaScript code to the output area
    output_area.markdown(js_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
