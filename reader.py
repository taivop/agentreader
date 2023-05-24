from typing import Type

import trafilatura
from langchain.tools.base import BaseTool
from newspaper import Article
from pydantic import BaseModel, Field

FULL_TEMPLATE = """
TITLE: {title}
AUTHORS: {authors}
PUBLISH DATE: {publish_date}
TOP_IMAGE_URL: {top_image}
TEXT:

{text}
"""

ONLY_METADATA_TEMPLATE = """
TITLE: {title}
AUTHORS: {authors}
PUBLISH DATE: {publish_date}
TOP_IMAGE_URL: {top_image}
"""

MAX_RESULT_LENGTH_CHAR = 2000 * 4  # characters


def page_result(text: str, cursor: int, max_length: int) -> str:
    return text[cursor : cursor + max_length]


class ReaderToolInput(BaseModel):
    url: str = Field(..., description="URL of the website to read")
    include_body: bool = Field(
        default=True,
        description="If false, only the title, authors,"
        "publish date and top image will be returned."
        "If true, response will also contain full body"
        "of the article.",
    )
    cursor: int = Field(
        default=0,
        description="Start reading from this character."
        "Use when the first response was truncated"
        "and you want to continue reading the page.",
    )


class ReaderTool(BaseTool):
    """Reader tool for getting website title and contents."""

    name: str = "read_page"
    args_schema: Type[BaseModel] = ReaderToolInput
    description: str = "use this to read a website"

    def _run(self, url: str, include_body: bool = True, cursor: int = 0) -> str:
        a = Article(url)
        a.download()
        a.parse()

        if not include_body:
            return ONLY_METADATA_TEMPLATE.format(
                title=a.title,
                authors=a.authors,
                publish_date=a.publish_date,
                top_image=a.top_image,
            )

        # If no content, try to get it with Trafilatura
        if not a.text:
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                raise ValueError("Could not download article.")
            result = trafilatura.extract(downloaded)
            res = FULL_TEMPLATE.format(
                title=a.title,
                authors=a.authors,
                publish_date=a.publish_date,
                top_image=a.top_image,
                text=result,
            )
        else:
            res = FULL_TEMPLATE.format(
                title=a.title,
                authors=a.authors,
                publish_date=a.publish_date,
                top_image=a.top_image,
                text=a.text,
            )

        if len(res) > MAX_RESULT_LENGTH_CHAR:
            res = page_result(res, cursor, MAX_RESULT_LENGTH_CHAR)
            res += f"\nRESULT TOO LONG, TRUNCATED. USE CURSOR={cursor+len(res)} TO CONTINUE."
        return res

    async def _arun(self, url: str) -> str:
        raise NotImplementedError