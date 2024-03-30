import cv2
from easyocr import Reader
from ocr_date_detector.date_parser import DateParser


class OcrDetector:
    """
    The main class of the OCRDateDetector.
    """

    def __init__(self, languages=["en"], month_mapping=None, use_gpu=True, ocr_optimize=True, debug=False):
        """
        Args:
            languages: A list of languages codes (ISO 639) detected during OCR analysis.
            use_gpu: A boolean indicating if the GPU acceleration should be used (greatly improves performance)
            ocr_optimize: A boolean indicating if the detection should be performed on the lower right part first
            debug: A boolean controlling additional debug logs
        """
        self.languages = languages
        self.date_parser = DateParser(month_mapping, debug)
        self.use_gpu = use_gpu
        self.optimization = ocr_optimize
        self.debug = debug

    def __get_valid_date(self, detection_results):
        for _, text, prob in detection_results:
            if self.debug:
                print("Detected: {} prob: {}".format(text, prob))
            parsed_date = self.date_parser.parse_date(text)
            if parsed_date:
                return parsed_date

    def get_date_ocr(self, img_path):
        """
        Detects the date from the input image using OCR.

        Args:
            img_path: Path to the input image

        Returns:
            - A datetime object if the date has been correctly determined
            - None if the date has not been detected.
        """
        src_image = cv2.imread(img_path)
        if src_image is None:
            return None
        reader = Reader(self.languages, gpu=self.use_gpu)
        results = None
        final_date = None
        if self.optimization:
            height, width = src_image.shape[:2]
            # Usually the date would be present in the lower right corner
            right_bottom_region = src_image[(height // 2): height, (width // 2): width]
            results = reader.readtext(right_bottom_region)
            if not results:
                final_date = self.__get_valid_date(results)

        if not results or not final_date:
            # Fallback - try to detect from full image if not present in the bottom right part
            results = reader.readtext(src_image)

        return self.__get_valid_date(results)
