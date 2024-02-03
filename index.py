import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Function to download and save image
def download_image(image_url, filename):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)

# Function to create draggable animal image using HTML and JavaScript
def draggable_animal(name, local_image_path):
    return f"""
        <img id="{name.lower()}-image" draggable="true" ondragstart="drag(event)" src="data:image/png;base64, {local_image_path}" style="width: 80px; height: 80px; cursor: move;">
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

    # Download and save images locally
    for animal in animals:
        local_image_path = f"{animal['name'].lower()}_image.png"
        download_image(animal["image_url"], local_image_path)

    # Display draggable animal images
    for animal in animals:
        st.markdown(draggable_animal(animal["name"], local_image_path), unsafe_allow_html=True)

    # Display farm area
    farm_area = st.markdown("<div id='farm-area' ondrop='drop(event)' ondragover='allowDrop(event)' style='width: 500px; height: 400px; border: 2px solid #4CAF50; margin: 20px; padding: 10px; position: relative;'></div>", unsafe_allow_html=True)

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

                // Get the dragged animal's name
                var animalName = data.split("-")[0];

                // Display the animal dropped into the farm
                var outputContent = document.getElementById("output-content");
                outputContent.innerHTML = "Dropped a " + animalName + " into the farm!";

                // Move the dragged animal image into the farm area
                var draggableAnimal = document.getElementById(data);
                var farmArea = document.getElementById("farm-area");
                var x = event.clientX - farmArea.getBoundingClientRect().left - draggableAnimal.width / 2;
                var y = event.clientY - farmArea.getBoundingClientRect().top - draggableAnimal.height / 2;
                draggableAnimal.style.position = "absolute";
                draggableAnimal.style.left = x + "px";
                draggableAnimal.style.top = y + "px";
                farmArea.appendChild(draggableAnimal);
            }
        </script>
    """
    
    # Add JavaScript code to the output area
    output_area.markdown(js_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
