import requests
from bs4 import BeautifulSoup
import json

headers = {
    "accept-language": "en-GB,en;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}


def get_html(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    return soup

def extract_information(soup):
    print(soup.html)

    review_elements = soup.select("div.review")

    reviews = []

    for review in review_elements:
        author_element = review.select_one("span.a-profile-name")
        author = author_element.text if author_element else None

        rating_element = review.select_one("i.review-rating")
        rating = rating_element.text.replace(" out of 5 stars", "") if rating_element else None

        title_element = review.select_one("a.review-title")
        title_span_element = title_element.select_one("span:not([class])") if title_element else None
        title = title_span_element.text if title_span_element else None

        content_element = review.select_one("span.review-text")
        content = content_element.text if content_element else None

        date_element = review.select_one("span.review-date")
        date = date_element.text.split("on ")[1] if date_element else None

        verified_element = review.select_one("span.a-size-mini")
        verified = True if verified_element and verified_element.text == "Verified Purchase" else False

        helpful_element = review.select_one("span.cr-vote-text")
        helpful_count = helpful_element.text.replace(" people found this helpful", "") if helpful_element else None

        image_element = review.select("img.review-image-tile")
        image_list = []

        for image in image_element:
            image_list.append(image.attrs["src"])

        r = {
            "author": author,
            "rating": rating,
            "title": title,
            "content": content,
            "date": date,
            "verified": verified,
            "helpful": helpful_count,
            "image_urls": image_list,
        }

        reviews.append(r)

    return reviews

def main():
    search_url = "https://www.amazon.com/Aeron-Executive-Chair-Size-Adjustable-Arms-lumbar/product-reviews/B00TXS2FR6/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    soup = get_html(search_url)
    data = extract_information(soup)

    with open("reviews.json", "w") as file:
        file.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    main()
