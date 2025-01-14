from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path, uid, db):
    try:
        # Open image
        img = Image.open(image_path).convert('RGB')
        # Process image and generate caption
        inputs = processor(images=img, return_tensors="pt")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        db[uid] = caption
    except Exception as e:
        return f"Error: {e}"
