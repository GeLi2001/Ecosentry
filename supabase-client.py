import os

from supabase import create_client


def upload_image(image_path: str) -> str:
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY"),
    )
    # Use the filename as the object key in the bucket
    object_key = os.path.basename(image_path)
    # Read the file as bytes
    with open(image_path, "rb") as f:
        file_data = f.read()
    # Upload the file to the 'images' bucket
    supabase.storage.from_("imagedb").upload(object_key, file_data)

    # Get the public URL for the uploaded file
    public_url = supabase.storage.from_("images").get_public_url(object_key)
    return public_url

upload_image("/Users/lige/Desktop/avatar.jpeg")