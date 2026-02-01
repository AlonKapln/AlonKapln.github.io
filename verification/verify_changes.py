from playwright.sync_api import sync_playwright
import os

def run():
    print("Starting verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Open index.html
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # 1. Verify LinkedIn Text
        # The link is inside #contact section.
        # But there are multiple linkedin links (one in hero, one in contact).
        # The hero one has an image inside. The contact one has text inside (previously email).

        # Specific locator for the one in contact section
        contact_linkedin = page.locator("#contact .contact-info-container a[href*='linkedin.com']")
        if contact_linkedin.count() > 0:
            text = contact_linkedin.inner_text()
            print(f"LinkedIn Text in Contact Section: '{text}'")
            if "LinkedIn Profile" in text:
                print("PASSED: LinkedIn text updated successfully.")
            else:
                print(f"FAILED: LinkedIn text expected 'LinkedIn Profile', got '{text}'")
        else:
            print("FAILED: Could not find LinkedIn link in contact section.")

        # 2. Verify Meta Tags
        desc = page.locator('meta[name="description"]')
        keywords = page.locator('meta[name="keywords"]')

        if desc.count() > 0:
            print(f"Meta Description: {desc.get_attribute('content')}")
            print("PASSED: Meta Description tag exists.")
        else:
            print("FAILED: Meta Description tag missing.")

        if keywords.count() > 0:
            print(f"Meta Keywords: {keywords.get_attribute('content')}")
            print("PASSED: Meta Keywords tag exists.")
        else:
            print("FAILED: Meta Keywords tag missing.")

        # 3. Verify Experience Section UI (Screenshots)
        # Scroll to experience section
        experience_section = page.locator("#experience")
        experience_section.scroll_into_view_if_needed()
        # Wait a bit for animations if any
        page.wait_for_timeout(1000)

        # Take Light Mode Screenshot
        page.screenshot(path="verification/experience_light.png")
        print("Captured verification/experience_light.png")

        # Toggle Dark Mode
        # Check if desktop button is visible
        theme_btn = page.locator("#theme-btn-desktop")
        if not theme_btn.is_visible():
             # maybe mobile view?
             theme_btn = page.locator("#theme-btn-mobile")

        if theme_btn.is_visible():
            theme_btn.click()
            page.wait_for_timeout(1000) # Wait for transition

            # Ensure we are scrolled to experience section
            experience_section.scroll_into_view_if_needed()
            page.wait_for_timeout(500)

            # Take Dark Mode Screenshot
            page.screenshot(path="verification/experience_dark.png")
            print("Captured verification/experience_dark.png")
        else:
            print("WARNING: Theme button not visible, skipping Dark Mode screenshot.")

        browser.close()
    print("Verification complete.")

if __name__ == "__main__":
    run()
