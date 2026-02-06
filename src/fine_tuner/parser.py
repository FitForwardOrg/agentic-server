import logging

logger = logging.getLogger(__name__)


def mk_doc_converter(source: str) -> str:
    """Convert document of supported formats to Markdown.
    It returns an empty string if the conversion fails.
    """
    # model loading takes ~3sec on a dev laptop, so we do lazy loading
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    try:
        result = converter.convert(source)
        return result.document.export_to_markdown()
    except Exception as e:
        logger.error("Error converting document:", exc_info=e)
        return ""
