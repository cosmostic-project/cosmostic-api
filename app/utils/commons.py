from flask import jsonify, make_response
from io import BytesIO
from PIL import Image


def create_cape_preview(cape_texture):
    """
    Creates a preview of a cape texture.

    Args:
        cape_texture: The cape texture file.

    Returns:
        BytesIO: A BytesIO object containing the preview image.
    """
    # open image
    img = Image.open(cape_texture)

    cropped = img.crop((1, 1, 11, 16))   # crop

    # save image
    output = BytesIO()
    cropped.save(output, format=img.format)

    return output

def create_response(code:int, message:str=None, data=None):
    """
    Creates a response object with the given code and optional message and data.

    Parameters:
        code (int): The status code of the response.
        message (str, optional): The message to include in the response. Defaults to None.
        data (Any, optional): The data to include in the response. Defaults to None.

    Returns:
        Response: The response object with the specified code, message, and data.
    """
    if data is not None:
        return make_response(jsonify(data), code)
    else:
        return make_response(jsonify({'code': code, 'message': message if message else ''}), code)