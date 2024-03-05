from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=opts)

amazon_email = "alexhayden141@gmail.com"
amazon_password = "haydenbaba"

def get_html(url):

    driver.get(url=url)

    try:
        email_input_field = driver.find_element(By.ID, "ap_email")
        email_input_field.send_keys(amazon_email)

        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()

        password_input_field = driver.find_element(By.ID, "ap_password")
        password_input_field.send_keys(amazon_password)

        sign_in_button = driver.find_element(By.ID, "signInSubmit")
        sign_in_button.click()

    except:
        print("Email input not found")

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

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
    page_number = 1
    reviews = []

    while True:
        search_url = "https://www.amazon.com/Aeron-Executive-Chair-Size-Adjustable-Arms-lumbar/product-reviews/B00TXS2FR6/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(page_number)
        soup = get_html(search_url)
        data = extract_information(soup)

        if (data == []):
            break

        reviews = reviews + data
        page_number = page_number + 1

    with open("reviews.json", "w") as file:
        file.write(json.dumps(reviews, indent=4))

if __name__ == '__main__':
    main()
