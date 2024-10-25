from roboflow import Roboflow
import json

# Initialize Roboflow with your API key
rf = Roboflow(api_key="NgUTB1xy6mHUeMCJo33c")
project = rf.workspace("ewaste-ik8z8").project("e-waste-ojvb8")
model = project.version(3).model

# Path to input image
image_path = "Servidor_Roboflow/imagen_prueba.jpg"  # Adjust path as needed

# Run inference and get JSON output
result = model.predict(image_path, confidence=40, overlap=30).json()

# Save JSON result to a file
with open("Servidor_Roboflow/results.json", "w") as json_file:
    json.dump(result, json_file, indent=4)
print("JSON results saved to results.json")

# Save processed image with bounding boxes and labels
output_image_path = "Servidor_Roboflow/prediction_image.jpg"  # Temporary file
model.predict(image_path, confidence=40, overlap=30).save(output_image_path)
print(f"Image with predictions saved to {output_image_path}")
