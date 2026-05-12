import unittest
from crawl import *

class TestCrawl(unittest.TestCase):
    # --- Normalization ---
    def test_normalize_url_slash(self):
        self.assertEqual(normalize_url("https://boot.dev/path/"), "boot.dev/path")

    def test_normalize_url_http(self):
        self.assertEqual(normalize_url("http://boot.dev/path"), "boot.dev/path")

    def test_normalize_url_no_slash(self):
        self.assertEqual(normalize_url("https://boot.dev/path"), "boot.dev/path")

    # --- Headings ---
    def test_get_heading_h1_exists(self):
        self.assertEqual(get_heading_from_html("<h1>Big</h1>"), "Big")
    
    def test_get_heading_h2_fallback(self):
        self.assertEqual(get_heading_from_html("<h2>Small</h2>"), "Small")

    def test_get_heading_not_found(self):
        self.assertEqual(get_heading_from_html("<div>Empty</div>"), "")

    # --- Paragraphs ---
    def test_get_para_in_main(self):
        html = "<p>Ignore</p><main><p>Keep</p></main>"
        self.assertEqual(get_first_paragraph_from_html(html), "Keep")

    def test_get_para_fallback_no_main(self):
        self.assertEqual(get_first_paragraph_from_html("<p>Hello</p>"), "Hello")

    def test_get_para_not_found(self):
        self.assertEqual(get_first_paragraph_from_html("<div>None</div>"), "")

    # --- URLs ---
    def test_get_urls_relative_to_abs(self):
        self.assertEqual(get_urls_from_html('<a href="/hi"></a>', "https://b.dev"), ["https://b.dev/hi"])

    def test_get_urls_absolute_stays_abs(self):
        self.assertEqual(get_urls_from_html('<a href="https://g.com"></a>', "https://b.dev"), ["https://g.com"])

    def test_get_urls_no_links(self):
        self.assertEqual(get_urls_from_html('<div>None</div>', "https://b.dev"), [])

    # --- Images ---
    def test_get_images_relative_to_abs(self):
        self.assertEqual(get_images_from_html('<img src="/i.png">', "https://b.dev"), ["https://b.dev/i.png"])

    def test_get_images_no_src(self):
        self.assertEqual(get_images_from_html('<img>', "https://b.dev"), [])

    # --- Extract Page Data (Dict structure) ---
    def test_extract_data_has_url(self):
        res = extract_page_data("<html></html>", "https://site.com")
        self.assertEqual(res["url"], "https://site.com")

    def test_extract_data_has_heading(self):
        res = extract_page_data("<h1>Hello</h1>", "https://site.com")
        self.assertEqual(res["heading"], "Hello")

    def test_extract_data_has_paragraph(self):
        res = extract_page_data("<p>Content</p>", "https://site.com")
        self.assertEqual(res["first_paragraph"], "Content")

    def test_extract_data_has_links(self):
        res = extract_page_data('<a href="/1"></a>', "https://site.com")
        self.assertEqual(res["outgoing_links"], ["https://site.com/1"])

    def test_extract_data_has_images(self):
        res = extract_page_data('<img src="/2.png">', "https://site.com")
        self.assertEqual(res["image_urls"], ["https://site.com/2.png"])

    def test_extract_data_complex_integration(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><h1>Title</h1><p>Text</p><a href="/l"></a><img src="/i.jpg"></body></html>'
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["heading"], "Title")
        self.assertEqual(len(actual["outgoing_links"]), 1)

if __name__ == "__main__":
    unittest.main()
