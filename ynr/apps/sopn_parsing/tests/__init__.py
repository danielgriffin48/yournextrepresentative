def should_skip_pdf_tests():
    try:
        import camelot  # noqa

        return False
    except ImportError:
        return True


def should_skip_conversion_tests():
    try:
        import pandoc  # noqa

        return False
    except ImportError:
        return True
