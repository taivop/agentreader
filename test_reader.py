from reader import ReaderTool, page_result


def test_page_result():
    s = "Hello world"
    assert page_result(s, 0, 5) == "Hello"
    assert page_result(s, 4, 1) == "o"
    assert page_result(s, 10, 5) == "d"


def test_reader_blog_article():
    tool = ReaderTool()
    url = "https://www.taivo.ai/startup-stock-options/"

    result = tool.run({"url": url})

    expected_start = "TITLE: Startup stock options: a beginner's guide"

    assert result.strip().startswith(expected_start)
    assert (
        "TOP_IMAGE_URL: https://www.taivo.ai/content/images/2022/01/stonks.jpg"
        in result
    )
    assert "assume the option package is worth nothing" in result


def test_cursor():
    tool = ReaderTool()
    url = "https://www.taivo.ai/startup-stock-options/"

    result = tool.run({"url": url, "cursor": 10000})

    assert "you buy stock in a publicly-traded company" not in result


def test_reader_blog_article_no_body():
    tool = ReaderTool()
    url = "https://www.taivo.ai/startup-stock-options/"

    result = tool.run({"url": url, "include_body": False})

    expected_start = "TITLE: Startup stock options: a beginner's guide"

    assert result.strip().startswith(expected_start)
    assert "assume the option package is worth nothing" not in result


def test_google_com():
    tool = ReaderTool()
    url = "https://www.google.com"

    result = tool.run({"url": url, "include_body": False})

    assert "TITLE: Google" in result
