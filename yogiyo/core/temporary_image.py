class TempraryImageMixin:

    @staticmethod
    def temporary_image():
        """
        임시 이미지 파일
        """
        import tempfile
        from PIL import Image

        image = Image.new('RGB', (1, 1))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        return tmp_file