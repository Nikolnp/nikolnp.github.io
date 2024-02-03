import streamlit as st

# Function to create draggable animal image using custom HTML
def draggable_animal(name, image_url):
    return f"""
        <img id="{name.lower()}-image" src="{image_url}" alt="{name}" style="width: 80px; height: 80px; cursor: move;" draggable="true"
            ondragstart="dragStart(event)">
        <script>
            function dragStart(event) {{
                event.dataTransfer.setData("text", event.target.id);
                event.target.style.opacity = '0.4';
            }}
        </script>
    """

# Streamlit app
def main():
    st.title("Drag Animals to the Farm")

    # Define animal data (name, image URL, color)
    animals = [
        {"name": "Dog", "image_url": "https://example.com/dog.png", "color": "brown"},
        {"name": "Cat", "image_url": "https://example.com/cat.png", "color": "gray"},
        {"name": "Cow", "image_url": "https://example.com/cow.png", "color": "black"},
        {"name": "Chicken", "image_url": "https://example.com/chicken.png", "color": "orange"},
    ]

    # Display draggable animal images using custom HTML
    for animal in animals:
        st.markdown(draggable_animal(animal["name"], animal["image_url"]), unsafe_allow_html=True)

    # Display farm area
    farm_area = st.empty()

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

                // Get the dragged animal's name
                var animalName = data.split("-")[0];

                // Display the animal dropped into the farm
                var outputContent = document.getElementById("output-content");
                outputContent.innerHTML = "Dropped a " + animalName + " into the farm!";

                // Move the dragged animal image into the farm area
                var droppedItem = document.getElementById(data);
                droppedItem.style.opacity = "1";  // Reset opacity
                var farmArea = document.getElementById("farm-area");
                farmArea.appendChild(droppedItem);
            }
        </script>
    """
    
    # Add JavaScript code to the output area
    output_area.markdown(js_code, unsafe_allow_html=True)

    # Add an invisible HTML element for tracking drop events
    st.markdown("<div id='farm-area' ondrop='drop(event)' ondragover='allowDrop(event)' style='width: 500px; height: 400px; border: 2px solid #4CAF50; margin: 20px; padding: 10px; position: relative;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
