import requests
from ddgs import DDGS


# ==========================================
# CONFIGURATION
# ==========================================

WIKIPEDIA_API = (
    "https://en.wikipedia.org/w/rest.php/v1"
)

USER_AGENT = (
    "Peppo-AI/1.0 "
    "(personal assistant project)"
)


# ==========================================
# DUCKDUCKGO SEARCH
# ==========================================

def search_web(query, max_results=5):

    try:

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                results.append({
                    "title": result.get(
                        "title",
                        ""
                    ),

                    "description": result.get(
                        "body",
                        ""
                    ),

                    "url": result.get(
                        "href",
                        ""
                    )
                })

        return results


    except Exception as error:

        print(
            "\nWeb search error:",
            error
        )

        return []


# ==========================================
# WIKIPEDIA SEARCH
# ==========================================

def search_wikipedia(query, limit=3):

    try:

        url = (
            f"{WIKIPEDIA_API}/search/page"
        )

        params = {
            "q": query,
            "limit": limit
        }

        headers = {
            "User-Agent": USER_AGENT
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for page in data.get(
            "pages",
            []
        ):

            results.append({
                "title": page.get(
                    "title",
                    ""
                ),

                "description": page.get(
                    "description",
                    ""
                ),

                "key": page.get(
                    "key",
                    ""
                )
            })

        return results


    except Exception as error:

        print(
            "\nWikipedia search error:",
            error
        )

        return []


# ==========================================
# WIKIPEDIA PAGE SUMMARY
# ==========================================

def get_wikipedia_summary(title):

    try:

        url = (
            f"https://en.wikipedia.org"
            f"/api/rest_v1/page/summary/"
            f"{title.replace(' ', '_')}"
        )

        headers = {
            "User-Agent": USER_AGENT
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:

            return None

        data = response.json()

        return {
            "title": data.get(
                "title",
                ""
            ),

            "description": data.get(
                "description",
                ""
            ),

            "summary": data.get(
                "extract",
                ""
            ),

            "url": data.get(
                "content_urls",
                {})
                .get(
                    "desktop",
                    {})
                .get(
                    "page",
                    ""
                ),

            "thumbnail": data.get(
                "thumbnail",
                {})
                .get(
                    "source",
                    ""
                )
        }


    except Exception as error:

        print(
            "\nWikipedia summary error:",
            error
        )

        return None


# ==========================================
# COMBINED WEB SEARCH
# ==========================================

def web_search(query):

    print(
        f"\nSearching web for: {query}"
    )

    results = search_web(
        query,
        max_results=5
    )

    return {
        "query": query,
        "source": "DuckDuckGo",
        "results": results
    }


# ==========================================
# COMBINED WIKIPEDIA SEARCH
# ==========================================

def wikipedia_search(query):

    print(
        f"\nSearching Wikipedia for: {query}"
    )

    pages = search_wikipedia(
        query,
        limit=3
    )

    results = []

    for page in pages:

        summary = get_wikipedia_summary(
            page["key"]
        )

        if summary:

            results.append(
                summary
            )

    return {
        "query": query,
        "source": "Wikipedia",
        "results": results
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "================================"
    )

    print(
        "Peppo Web Manager Test"
    )

    print(
        "================================"
    )


    # --------------------------------------
    # DUCKDUCKGO TEST
    # --------------------------------------

    query = "Python programming language"

    web_results = web_search(
        query
    )

    print(
        "\n\nDUCKDUCKGO RESULTS"
    )

    print(
        "=================="
    )

    for result in web_results["results"]:

        print(
            "\nTitle:",
            result["title"]
        )

        print(
            "Description:",
            result["description"]
        )

        print(
            "URL:",
            result["url"]
        )


    # --------------------------------------
    # WIKIPEDIA TEST
    # --------------------------------------

    wiki_results = wikipedia_search(
        "Python programming language"
    )

    print(
        "\n\nWIKIPEDIA RESULTS"
    )

    print(
        "================="
    )

    for result in wiki_results["results"]:

        print(
            "\nTitle:",
            result["title"]
        )

        print(
            "Description:",
            result["description"]
        )

        print(
            "Summary:",
            result["summary"]
        )

        print(
            "URL:",
            result["url"]
        )