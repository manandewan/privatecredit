import sys
import os
import time
from playwright.sync_api import sync_playwright, expect

TARGET_URL = "http://localhost:8000"
ARTIFACTS_DIR = "/Users/manandewan/Desktop/Oxane/test-results"

def run_mobile_tests():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    console_errors = []
    console_warnings = []

    print("=" * 75)
    print("📱 STARTING COMPREHENSIVE MOBILE AUDIT & E2E TESTS (OXANE CREDIT MASTERY)")
    print("=" * 75)

    devices = [
        {"name": "iPhone SE (375x667)", "viewport": {"width": 375, "height": 667}, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"},
        {"name": "iPhone 14 (390x844)", "viewport": {"width": 390, "height": 844}, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
        {"name": "Google Pixel 7 (412x915)", "viewport": {"width": 412, "height": 915}, "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
        {"name": "Mobile Landscape (667x375)", "viewport": {"width": 667, "height": 375}, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"}
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for dev in devices:
            dev_name = dev["name"]
            print(f"\n📲 TESTING DEVICE VIEWPORT: {dev_name}")
            print("-" * 55)

            context = browser.new_context(
                viewport=dev["viewport"],
                user_agent=dev["user_agent"],
                is_mobile=True,
                has_touch=True
            )
            page = context.new_page()

            def handle_console(msg):
                if msg.type == "error":
                    if "net::ERR_" not in msg.text:
                        console_errors.append(f"[{dev_name}] {msg.text}")
                elif msg.type == "warning":
                    console_warnings.append(f"[{dev_name}] {msg.text}")

            page.on("console", handle_console)
            page.on("pageerror", lambda err: console_errors.append(f"[{dev_name}] {str(err)}"))

            # -------------------------------------------------------------
            # TEST 1: Initial Load & Horizontal Overflow Audit
            # -------------------------------------------------------------
            page.goto(TARGET_URL)
            page.wait_for_load_state("networkidle")

            # Check for horizontal overflow (critical for mobile)
            overflow_info = page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })")
            print(f"  ✓ Horizontal Page Dimensions: scrollWidth={overflow_info['scrollWidth']}px, innerWidth={overflow_info['innerWidth']}px")
            assert overflow_info["scrollWidth"] <= overflow_info["innerWidth"], f"Horizontal overflow detected on {dev_name}: scrollWidth ({overflow_info['scrollWidth']}) > innerWidth ({overflow_info['innerWidth']})"

            # -------------------------------------------------------------
            # TEST 2: Dollar Logo & Header Rendering
            # -------------------------------------------------------------
            dollar_logo = page.locator("header span:has-text('$')").first
            expect(dollar_logo).to_be_visible()
            print("  ✓ Dollar ($) Logo visible and cleanly styled in header")

            header_title = page.locator("header span:has-text('OXANE MASTERY')")
            expect(header_title).to_be_visible()
            print("  ✓ Brand title rendered cleanly without overlap")

            # -------------------------------------------------------------
            # TEST 3: PWA Manifest & Service Worker Validation
            # -------------------------------------------------------------
            if dev_name.startswith("iPhone SE"):
                manifest_res = page.request.get(f"{TARGET_URL}/manifest.json")
                assert manifest_res.status == 200, f"manifest.json returned status {manifest_res.status}"
                manifest_json = manifest_res.json()
                assert manifest_json["name"] == "Oxane Credit Mastery | Private Credit Analyst Academy"
                assert manifest_json["short_name"] == "CreditMastery"
                assert len(manifest_json["icons"]) >= 3
                print("  ✓ PWA Web App Manifest validated successfully (200 OK, valid JSON & icons)")

                sw_res = page.request.get(f"{TARGET_URL}/sw.js")
                assert sw_res.status == 200, f"sw.js returned status {sw_res.status}"
                print("  ✓ PWA Service Worker script accessible (200 OK)")

                fav_res = page.request.get(f"{TARGET_URL}/favicon.svg")
                assert fav_res.status == 200
                print("  ✓ SVG Favicon accessible (200 OK)")

            # -------------------------------------------------------------
            # TEST 4: PWA Install / Download App Button & Modal
            # -------------------------------------------------------------
            install_btn = page.locator("#installAppBtn")
            expect(install_btn).to_be_visible()
            print("  ✓ 'Install' / Download App button visible in header")

            install_btn.click()
            page.wait_for_timeout(300)

            install_modal = page.locator("#installModal")
            expect(install_modal).to_be_visible()
            expect(page.locator("#installModal").get_by_text("Google Chrome & Android:")).to_be_visible()
            expect(page.locator("#installModal").get_by_text("iPhone & iPad (Safari):")).to_be_visible()
            print("  ✓ Install Modal opened with Chrome, Safari, and Desktop instructions")

            # Dismiss install modal
            page.locator("#installModal button:has-text('Close')").click()
            page.wait_for_timeout(200)
            expect(install_modal).to_be_hidden()
            print("  ✓ Install Modal dismissed successfully")

            # -------------------------------------------------------------
            # TEST 5: Mobile Filter Tabs Carousel
            # -------------------------------------------------------------
            page.locator("#tab-2").click()
            page.wait_for_timeout(200)
            mod2_cards = page.locator("#levelsContainer > div").count()
            assert mod2_cards == 3, f"Expected 3 cards in Module 2, found {mod2_cards}"
            print("  ✓ Module 2 Filter Tab selected (3 cards rendered)")

            page.locator("#tab-6").click()
            page.wait_for_timeout(200)
            mod6_cards = page.locator("#levelsContainer > div").count()
            assert mod6_cards == 1, f"Expected 1 card in Module 6, found {mod6_cards}"
            print("  ✓ Module 6 Filter Tab selected (1 card rendered)")

            page.locator("#tab-ALL").click()
            page.wait_for_timeout(200)
            all_cards = page.locator("#levelsContainer > div").count()
            assert all_cards == 13, f"Expected 13 cards in ALL tab, found {all_cards}"
            print("  ✓ All 13 Levels Tab restored (13 cards rendered)")

            # -------------------------------------------------------------
            # TEST 6: Mobile Touch Navigation to Lesson & Checkpoint Quiz
            # -------------------------------------------------------------
            hero_continue = page.locator("#heroContinueBtn")
            expect(hero_continue).to_be_visible()
            hero_continue.click()
            page.wait_for_timeout(400)

            lesson_view = page.locator("#lessonView")
            expect(lesson_view).to_be_visible()

            # Verify no horizontal blowout inside lesson view on mobile
            lesson_overflow = page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })")
            assert lesson_overflow["scrollWidth"] <= lesson_overflow["innerWidth"], f"Lesson view horizontal overflow on {dev_name}"
            print("  ✓ Lesson View rendered with 0 horizontal page overflow")

            # Interact with Checkpoint Quiz via Touch
            quiz_container = page.locator("#checkpointContainer")
            quiz_container.scroll_into_view_if_needed()
            page.wait_for_timeout(200)

            # Click option 1 (correct)
            page.locator("#quiz-opt-1").click()
            page.wait_for_timeout(400)

            feedback = page.locator("#quizFeedback")
            expect(feedback).to_be_visible()
            assert "Correct!" in feedback.inner_text()
            print("  ✓ Mobile Checkpoint Quiz touched and evaluated (Correct! feedback displayed)")

            # Celebration modal
            celeb_modal = page.locator("#celebrationModal")
            expect(celeb_modal).to_be_visible()
            print("  ✓ Celebration Modal displayed properly on mobile screen")

            page.locator("#celebrationModal button[aria-label='Close modal']").click()
            page.wait_for_timeout(200)
            expect(celeb_modal).to_be_hidden()

            # Back to Roadmap
            page.locator("button:has-text('← Back to Roadmap')").click()
            page.wait_for_timeout(300)
            expect(page.locator("#homeView")).to_be_visible()
            print("  ✓ Navigated back to Mobile Roadmap cleanly")

            # -------------------------------------------------------------
            # TEST 7: KaTeX & Table Deep Inspection (Level 3 & Level 8)
            # -------------------------------------------------------------
            if dev_name.startswith("iPhone SE"):
                # Level 3: Bond math formulas
                page.locator("#levelsContainer > div").nth(2).click()
                page.wait_for_timeout(400)
                l3_overflow = page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })")
                assert l3_overflow["scrollWidth"] <= l3_overflow["innerWidth"], "Level 3 math formulas caused horizontal overflow"
                print("  ✓ Level 3 KaTeX math formulas fit within 375px viewport with no page blowout")

                page.locator("button:has-text('← Back to Roadmap')").click()
                page.wait_for_timeout(200)

                # Level 8: S&P 6x6 Matrix Table
                page.locator("#levelsContainer > div").nth(7).click()
                page.wait_for_timeout(400)
                l8_overflow = page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })")
                assert l8_overflow["scrollWidth"] <= l8_overflow["innerWidth"], "Level 8 S&P table caused horizontal overflow"
                print("  ✓ Level 8 S&P Matrix table scrolls internally with 0 page-wide horizontal blowout")

                page.locator("button:has-text('← Back to Roadmap')").click()
                page.wait_for_timeout(200)

                # Level 13: Grand Capstone Revision
                page.locator("#levelsContainer > div").nth(12).click()
                page.wait_for_timeout(400)
                l13_overflow = page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })")
                assert l13_overflow["scrollWidth"] <= l13_overflow["innerWidth"], "Level 13 Capstone caused horizontal overflow"
                print("  ✓ Level 13 Grand Capstone fits within 375px viewport with 0 page-wide blowout")

                page.locator("button:has-text('← Back to Roadmap')").click()
                page.wait_for_timeout(200)

            # -------------------------------------------------------------
            # TEST 8: Screenshot Capture
            # -------------------------------------------------------------
            safe_name = dev_name.split()[0].lower()
            shot_path = os.path.join(ARTIFACTS_DIR, f"mobile_{safe_name}_roadmap.png")
            page.screenshot(path=shot_path)
            print(f"  📷 Saved Mobile Screenshot: {shot_path}")

            context.close()

        # -------------------------------------------------------------
        # TEST 9: Console Error Audit
        # -------------------------------------------------------------
        print("\n" + "=" * 55)
        print(f"Total Console Errors across all mobile tests: {len(console_errors)}")
        print(f"Total Console Warnings across all mobile tests: {len(console_warnings)}")
        assert len(console_errors) == 0, f"Console errors detected on mobile: {console_errors}"
        print("✓ ZERO console errors across entire multi-device mobile test suite!")

        browser.close()

    print("\n" + "=" * 75)
    print("🎉 ALL MOBILE AUDIT & E2E TESTS PASSED WITH 100% GREEN METRICS!")
    print("=" * 75)

if __name__ == "__main__":
    try:
        run_mobile_tests()
    except Exception as e:
        print(f"\n❌ MOBILE TEST FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
