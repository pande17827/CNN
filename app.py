import streamlit as st
import os
import numpy as np
from PIL import Image
from imgaug import augmenters as iaa

# Streamlit App
st.title("Image Augmentation Tool")

# Step 1: Upload an Image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Step 2: Select Folder to Save Augmented Images
save_folder = st.text_input("Enter the folder path to save augmented images:")
if save_folder and not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Step 3: Set Augmentation Parameters
st.sidebar.header("Augmentation Parameters")
rotate = st.sidebar.slider("Rotate (degrees)", -180, 180, 0)
flip_horizontal = st.sidebar.checkbox("Flip Horizontally")
flip_vertical = st.sidebar.checkbox("Flip Vertically")
brightness = st.sidebar.slider("Adjust Brightness (0.5 = darker, 1 = original, 1.5 = brighter)", 0.5, 1.5, 1.0)
scale = st.sidebar.slider("Zoom (Scale Factor)", 0.5, 2.0, 1.0)
num_augmentations = st.sidebar.number_input("Number of Augmented Images to Generate", min_value=1, max_value=100, value=5)

# Step 4: Apply Augmentations
if uploaded_image and save_folder:
    image = Image.open(uploaded_image)
    image_array = np.array(image)

    # Define Augmentation Pipeline
    aug_pipeline = iaa.Sequential([
        iaa.Affine(rotate=rotate, scale=scale),
        iaa.Fliplr(1.0 if flip_horizontal else 0.0),
        iaa.Flipud(1.0 if flip_vertical else 0.0),
        iaa.Multiply(brightness)
    ])

    # Generate Augmented Images
    st.write("### Augmented Images")
    for i in range(num_augmentations):
        augmented_image = aug_pipeline(image=image_array)
        augmented_image_pil = Image.fromarray(augmented_image)

        # Save Augmented Image
        save_path = os.path.join(save_folder, f"augmented_{i + 1}.png")
        augmented_image_pil.save(save_path)

        # Display Augmented Image
        st.image(augmented_image_pil, caption=f"Augmented Image {i + 1}")

    st.success(f"{num_augmentations} augmented images saved to {save_folder}")
else:
    st.warning("Please upload an image and specify a folder to save augmented images.")
