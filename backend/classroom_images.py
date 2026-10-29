"""Safe storage for normalized classroom images."""
import io
import os
import uuid

from PIL import Image, ImageOps

MAX_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 20_000_000
IMAGE_DIR = "img"


class ImageTooLarge(Exception):
    pass


class InvalidImage(Exception):
    pass


class ImageStorageError(Exception):
    pass


def normalize_and_store(data: bytes) -> str:
    """Validate and re-encode supported image bytes to a fresh JPEG ID."""
    if len(data) > MAX_BYTES:
        raise ImageTooLarge()
    try:
        with Image.open(io.BytesIO(data)) as source:
            if source.format not in ("JPEG", "PNG", "WEBP"):
                raise InvalidImage()
            if source.width <= 0 or source.height <= 0 or source.width * source.height > MAX_PIXELS:
                raise InvalidImage()
            source.load()
            oriented = ImageOps.exif_transpose(source)
            oriented.load()
            if oriented.mode in ("RGBA", "LA") or "transparency" in oriented.info:
                rgba = oriented.convert("RGBA")
                image = Image.new("RGB", rgba.size, "white")
                image.paste(rgba, mask=rgba.getchannel("A"))
            else:
                image = oriented.convert("RGB")
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=88, optimize=True)
            encoded = output.getvalue()
    except InvalidImage:
        raise
    except Exception as exc:
        raise InvalidImage() from exc

    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        # Exclusive creation prevents collisions from overwriting legacy images.
        for _ in range(5):
            ident = "classroom_" + uuid.uuid4().hex
            path = os.path.join(IMAGE_DIR, ident + ".jpg")
            try:
                with open(path, "xb") as file:
                    file.write(encoded)
                return ident
            except FileExistsError:
                continue
            except OSError:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except OSError:
                    pass
                raise
        raise OSError("could not allocate unique image name")
    except Exception as exc:
        raise ImageStorageError() from exc
