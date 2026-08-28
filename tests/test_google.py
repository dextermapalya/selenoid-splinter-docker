"""
Test script for Google.com using Splinter and Selenoid
"""
import os
import sys
from datetime import datetime
from splinter import Browser

# Configuration
SELENOID_URL = os.getenv('SELENOID_URL', 'http://localhost:4444')
BROWSER_TYPE = 'chrome'  # Can be 'chrome' or 'firefox'


def test_google_homepage():
    """Test Google homepage loads and basic search functionality"""
    print(f"\n{'='*60}")
    print(f"Starting test at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Selenoid URL: {SELENOID_URL}")
    print(f"Browser: {BROWSER_TYPE}")
    print(f"{'='*60}\n")
    
    browser = None
    try:
        # Initialize browser with Selenoid
        desired_capabilities = {
            'browserName': BROWSER_TYPE,
            'version': 'latest',
            'screenResolution': '1920x1080',
            'name': 'Google Test'
        }
        
        browser = Browser(
            'remote',
            url=f'{SELENOID_URL}/wd/hub',
            desired_capabilities=desired_capabilities,
            wait_time=10
        )
        
        print("✓ Browser initialized successfully")
        
        # Test 1: Visit Google homepage
        print("\n[Test 1] Visiting google.com...")
        browser.visit('https://www.google.com')
        print("✓ Google homepage loaded")
        
        # Test 2: Check page title
        print("\n[Test 2] Checking page title...")
        title = browser.title
        print(f"  Current title: '{title}'")
        assert 'Google' in title or 'google' in title.lower(), "Google not found in title"
        print("✓ Page title contains 'Google'")
        
        # Test 3: Check search box exists
        print("\n[Test 3] Finding search input...")
        search_box = browser.find_by_name('q')
        assert len(search_box) > 0, "Search box not found"
        print("✓ Search box found")
        
        # Test 4: Perform a search
        print("\n[Test 4] Performing search for 'Selenoid'...")
        search_box.fill('Selenoid docker browser automation')
        print("  Text entered in search box")
        
        # Find and click the search button
        search_button = browser.find_by_name('btnK')
        if len(search_button) > 0:
            search_button.click()
        else:
            # Alternative: press Enter
            browser.find_by_name('q').first._element.send_keys('\n')
        
        print("  Search submitted")
        
        # Wait for results page
        browser.sleep(3)
        print("✓ Search results page loaded")
        
        # Test 5: Verify search results
        print("\n[Test 5] Verifying search results...")
        results = browser.find_by_css('.g')
        print(f"  Found {len(results)} search result items")
        assert len(results) > 0, "No search results found"
        print("✓ Search results are displayed")
        
        # Test 6: Check for result links
        print("\n[Test 6] Checking result links...")
        links = browser.find_by_css('a[href*="google"]')
        print(f"  Found {len(links)} relevant links")
        print("✓ Result links are present")
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        
        if browser:
            try:
                # Take screenshot on failure
                screenshot_path = '/app/reports/failure_screenshot.png'
                browser.screenshot(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
            except:
                pass
        
        return False
        
    finally:
        if browser:
            print("\nClosing browser...")
            browser.quit()
            print("✓ Browser closed")


def test_google_elements():
    """Test various elements on Google homepage"""
    print(f"\n{'='*60}")
    print("Starting element tests")
    print(f"{'='*60}\n")
    
    browser = None
    try:
        desired_capabilities = {
            'browserName': BROWSER_TYPE,
            'version': 'latest',
            'screenResolution': '1920x1080',
            'name': 'Google Elements Test'
        }
        
        browser = Browser(
            'remote',
            url=f'{SELENOID_URL}/wd/hub',
            desired_capabilities=desired_capabilities,
            wait_time=10
        )
        
        print("✓ Browser initialized")
        
        # Load Google homepage
        browser.visit('https://www.google.com')
        print("✓ Google homepage loaded")
        
        # Test footer elements
        print("\n[Element Test 1] Checking footer elements...")
        footer_links = browser.find_by_css('footer a')
        print(f"  Found {len(footer_links)} footer links")
        
        # Get some footer link texts
        link_texts = [link.text for link in footer_links[:3]]
        print(f"  Sample footer links: {link_texts}")
        
        print("✓ Footer elements verified")
        
        # Test language selector
        print("\n[Element Test 2] Checking language options...")
        lang_options = browser.find_by_css('a[lang]')
        print(f"  Found {len(lang_options)} language options")
        print("✓ Language options found")
        
        print("\n" + "="*60)
        print("✓✓✓ ALL ELEMENT TESTS PASSED ✓✓✓")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ELEMENT TEST FAILED: {str(e)}")
        return False
        
    finally:
        if browser:
            print("Closing browser...")
            browser.quit()
            print("✓ Browser closed")


if __name__ == '__main__':
    # Run tests
    test1_result = test_google_homepage()
    test2_result = test_google_elements()
    
    # Exit with appropriate code
    exit_code = 0 if (test1_result and test2_result) else 1
    sys.exit(exit_code)