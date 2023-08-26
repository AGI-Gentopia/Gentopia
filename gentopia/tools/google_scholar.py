from typing import AnyStr, List
from scholarly import scholarly, ProxyGenerator
from gentopia.tools.basetool import *
from scholarly import ProxyGenerator
from itertools import islice


class SearchAuthorByNameArgs(BaseModel):
    author: str = Field(..., description="author name with the institute name (optional), e.g., Tan Lee")
    top_k: int = Field(..., description="number of results to display. 5 is prefered")


class SearchAuthorByName(BaseTool):
    name = "search_author_by_name"
    description = ("search an author with google scholar."
                   "input a name, return a list of authors with info (including uid)."
                   "you can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = SearchAuthorByNameArgs
    author: str = ""
    results: List = []

    def _run(self, author: AnyStr, top_k: int = 5) -> str:
        if author != self.author:
            self.results = scholarly.search_author(author)
        self.author = author
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'name': it["name"],
                'uid': it["scholar_id"],
                'affiliation': it["affiliation"],
                'interests': it['interests'],
                'citation': it['citedby'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchAuthorByInterestsArgs(BaseModel):
    interests: str = Field(..., description="research interests separated by comma, e.g., 'crowdsourcing,privacy'")
    top_k: int = Field(..., description="number of results to display. 5 is prefered.")


class SearchAuthorByInterests(BaseTool):
    name = "search_author_by_interests"
    description = ("search authors given keywords of research interests"
                   "input interests, return a list of authors."
                   "you can repeat calling the function to get next results."
                  )
    args_schema: Optional[Type[BaseModel]] = SearchAuthorByInterestsArgs
    interests: str = ""
    results: List = []

    def _run(self, interests: AnyStr, top_k: int = 5) -> str:
        if interests != self.interests:
            self.results = scholarly.search_keywords(interests.split(','))
        self.interests = interests
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'name': it["name"],
                'uid': it['scholar_id'],
                'affiliation': it['affiliation'],
                'interests': it['interests'],
                'citation': it['citedby'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class AuthorUID2PaperArgs(BaseModel):
    uid: str = Field(..., description="a unique identifier assigned to author in Google scholar")
    sort_by: str = Field(..., description="either 'citedby' or 'year'.")
    top_k: int = Field(..., description="number of results to display. 5 is prefered")


class AuthorUID2Paper(BaseTool):
    name = "author_uid2paper"
    description = ("search the papers given the UID of an author."
                   "you can use search_author first to get UID."
                   "you can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = AuthorUID2PaperArgs
    uid: str = ""
    sort_by: str = ""
    results: List = []

    def _run(self, uid: AnyStr, sort_by: AnyStr, top_k: int = 5) -> str:
        if uid != self.uid or sort_by != self.sort_by:
            author = scholarly.search_author_id(uid)
            author = scholarly.fill(author, sortby=sort_by)
            self.results = iter(author['publications'])
        self.uid = uid
        self.sort_by = sort_by
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['citation'],
                # "abstract": it['bib']['abstract'],
                # 'url': it['pub_url'],
                'citation': it['num_citations'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchPaperArgs(BaseModel):
    title: str = Field(..., description="title name")
    sort_by: str = Field(..., description="either 'relevance' or 'date'.")
    top_k: int = Field(..., description="number of results to display. 5 is prefered. set to 1 if given the complete title")


class SearchPaper(BaseTool):
    name = "search_paper"
    description = ("search a paper with the title relevant to the input text."
                   "input text query, return a list of papers."
                   "you can repeat calling the function to get next results."
                  )
    args_schema: Optional[Type[BaseModel]] = SearchPaperArgs
    title: str = ""
    sort_by: str = ""
    results: List = []

    def _run(self, title: AnyStr, sort_by: AnyStr, top_k: int = 5) -> str:
        if title != self.title or sort_by != self.sort_by:
            self.results = scholarly.search_pubs(title, sort_by=sort_by)
        self.title = title
        self.sort_by = sort_by
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchRelatedPaperArgs(BaseModel):
    title: str = Field(..., description="title name")
    top_k: int = Field(..., description="number of results to display. 5 is prefered.")


class SearchRelatedPaper(BaseTool):
    name = "search_related_paper"
    description = ("search the papers related to the target one."
                   "input the complete paper title, return a list of relevant papers."
                   "you can repeat calling the function to get next results."
                  )
    args_schema: Optional[Type[BaseModel]] = SearchRelatedPaperArgs
    title: str = ""
    results: List = []

    def _run(self, title: AnyStr, top_k: int = 5) -> str:
        if title != self.title:
            # please make sure the title is complete
            paper = scholarly.search_single_pub(title)
            self.results = scholarly.get_related_articles(paper)
        self.title = title
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchCitePaperArgs(BaseModel):
    title: str = Field(..., description="title name")
    top_k: int = Field(..., description="number of results to display. 5 is prefered.")


class SearchCitePaper(BaseTool):
    name = "search_cite_paper"
    description = ("search the papers citing to the target one."
                   "input the complete paper title, return a list of papers citing the one."
                   "you can repeat calling the function to get next results."
                  )
    args_schema: Optional[Type[BaseModel]] = SearchCitePaperArgs
    title: str = ""
    results: List = []

    def _run(self, title: AnyStr, top_k: int = 5) -> str:
        if title != self.title:
            # please make sure the title is complete
            paper = scholarly.search_single_pub(title)
            self.results = scholarly.citedby(paper)
        self.title = title
        assert self.results is not None
        ans = []
        for it in islice(self.results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    # import pdb
    # searcher1 = SearchAuthorByName()
    # ans1 = searcher1._run("Tan Lee")
    # ans2 = searcher1._run("Tan Lee")
    searcher3 = AuthorUID2Paper()
    searcher3._run("5VTS11IAAAAJ", sort_by='year')
    # searcher4 = SearchPaper()
    # ans4 = searcher4._run("Attention is all you need")
    # searcher5 = SearchAuthorByInterests()
    # searcher5._run("privacy,robustness")
    # print(ans4)
    # pdb.set_trace()
    # search6 = SearchRelatedPaper()
    # ans = search6._run("Attention is all you need")
    # search7 = SearchCitePaper()
    # ans = search7._run("Attention is all you need")
    # print(ans)
