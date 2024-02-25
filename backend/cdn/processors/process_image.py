from pathlib import Path
from typing import Optional, Tuple, Union
from PIL import Image


def process_image(stream, file_path: Path, max_dimention: Optional[Union[int, Tuple[int, int]]] = None):
    image = Image.open(stream)
    if image.format not in ["PNG", "JPG", "JPEG"]:
        raise ValueError('Incorrect format!')
    elif image.format == "PNG":
        image = image.convert('RGB')
    
    if isinstance(max_dimention, int):
        (width, height) = image.size
        
        if (width > height):
            max_dimention = (max_dimention, int((height / width) * max_dimention))
        elif (width < height):
            max_dimention = (int((width / height) * max_dimention), max_dimention)
        else:
            max_dimention = (max_dimention, max_dimention)
        
    if isinstance(max_dimention, tuple):
        image = image.resize(max_dimention)
        
    image.save(file_path, format="JPEG", quality = 80)
