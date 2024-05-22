from uuid import UUID
from PIL import Image
from io import BytesIO
import string
import json
from jsonschema import validate, ValidationError


class InputValidator():
    def integer(self, value):
        """
        Check if input value is an integer.

        Parameters:
        - value: The value to be tested.

        Returns:
        int: The integer representation of the input value.

        Raises:
        ValueError: If the conversion to an integer fails.
        """
        try:
            value = int(value)
        except:
            raise ValueError("Parameter must be an integer (int)")
        
        return value

    def string(self, value):
        """
        Check if input value is a string within specified constraints.

        Parameters:
        - value: The string value to be validated.

        Returns:
        str: The validated string.

        Raises:
        ValueError: If the parameter is not a string, exceeds 50 characters, or is empty.
        """
        if not isinstance(value, str):
            raise ValueError("Parameter must be a string (str)")

        allowed = string.ascii_letters + string.digits + "_-"   # allowed characters
        for char in value:
            if char not in allowed:
                raise ValueError("Invalid string")

        if len(value) > 16:
            raise ValueError("Parameter must not exceed 16 characters")
        elif len(value) < 2:
            raise ValueError("Parameter must not be less than 2 characters")
        elif len(value) == 0:
            raise ValueError("Parameter cannot be empty")

        return value

    def boolean(self, value):
        """
        Check and converts a string representation of a boolean to a boolean value.

        Parameters:
        - value: The string value representing a boolean ("true" or "false").

        Returns:
        bool: The boolean representation of the input value.

        Raises:
        ValueError: If the parameter is not a valid boolean string.
        """
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise ValueError("Parameter must be a boolean (true/false)")
    
    def uuid(self, value):
        """
        Check if input value is an uuid.

        Parameters:
        - value: The string value to be validated.

        Returns:
        str: The validated uuid.

        Raises:
        ValueError: If the parameter is not an uuid.
        """
        try:
            uuid = UUID(value)
        except ValueError:
            raise ValueError("Parameter must be an uuid")
        return uuid

    def cape_texture(self, image):
        """
        Validate the cape texture image.

        Args:
            image (FileStorage): The image file to be validated.

        Raises:
            ValueError: If the image is not a PNG file or if its dimensions are not 46x22 pixels.

        Returns:
            FileStorage: The validated image file.
        """
        # check image type
        if not image.content_type or not image.content_type.startswith('image/png'):
            raise ValueError("File must be an image (png)")

        # check image dimensions
        image_data = BytesIO(image.read())
        img = Image.open(image_data)
        width, height = img.size

        if width != 46 or height != 22:
            raise ValueError("Dimensions must be 46x22 pixels")

        return image
    
    def accessory_texture(self, image):
        """
        Validate the accessory texture image.

        Args:
            image (FileStorage): The image file to be validated.

        Raises:
            ValueError: If the image is not a PNG file or if its dimensions are not between 16x16 and 100x100 pixels.

        Returns:
            FileStorage: The validated image file.
        """
        # check image type
        if not image.content_type or not image.content_type.startswith('image/png'):
            raise ValueError("File must be an image (png)")
        
        # check image dimensions
        image_data = BytesIO(image.read())
        img = Image.open(image_data)
        width, height = img.size

        if width < 16 or width > 100 or height < 16 or height > 100:
            raise ValueError("Dimensions must be between 16x16 and 100x100 pixels")

        return image
    
    def accessory_preview(self, image):
        """
        Validate the accessory preview image.

        Args:
            image (FileStorage): The image file to be validated.

        Raises:
            ValueError: If the image is not a PNG file or if its dimensions are not 150x150 pixels.

        Returns:
            FileStorage: The validated image file.
        """
        # check image type
        if not image.content_type or not image.content_type.startswith('image/png'):
            raise ValueError("File must be an image (png)")
        
        # check image dimensions
        image_data = BytesIO(image.read())
        img = Image.open(image_data)
        width, height = img.size

        if width != 150 or height != 150:
            raise ValueError("Dimensions must be 150x150 pixels")
        
        return image
    
    def accessory_model(self, value):
        """
        Validates the accessory model parameter.

        Parameters:
            value (str): The JSON string representing the accessory model.

        Returns:
            dict: The validated accessory model.

        Raises:
            ValueError: If the parameter is not a valid JSON or does not respect the accessory model schema.
        """
        # check if json
        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError as e:
            raise ValueError("Parameter must be a valid JSON") 

        # check if right schema
        schema = {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "textureSize": {"type": "array", "items": {"type": "integer"}},
                "models": {"type": "array"},
            },
            "required": ["type", "textureSize", "models"],
        }

        try:
            validate(instance=value, schema=schema)
        except ValidationError as e:
            raise ValueError("Parameter must respect the accessory model schema")
        
        return value


    # documentation
    integer.__schema__ = {'type': 'integer'}
    string.__schema__ = {'type': 'string'}
    boolean.__schema__ = {'type': 'boolean'}
    uuid.__schema__ = {'type': 'uuid'}
    cape_texture.__schema__ = {'type': 'capetexture'}
    accessory_texture.__schema__ = {'type': 'accessorytexture'}
    accessory_model.__schema__ = {'type': 'accessorymodel'}