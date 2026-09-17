import sys
import os
import time
from playwright.sync_api import sync_playwright, expect

TARGET_URL = "http://localhost:8000"
ARTIFACTS_DIR = "/Users/manandewan/Desktop/Oxane/test-results"

def run_tests():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    console_errors = []
    console_warnings = []

    print("=" * 70)
    print("🚀 STARTING E2E AUTOMATED TESTS FOR OXANE CREDIT MASTERY APP (12 LEVELS)")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # Capture console errors and warnings
        def handle_console(msg):
            if msg.type == "error":
                # Filter out offline network fetch failures for external CDNs
                if "net::ERR_" not in msg.text:
                    console_errors.append(msg.text)
            elif msg.type == "warning":
                console_warnings.append(msg.text)

        page.on("console", handle_console)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        # -------------------------------------------------------------
        # 1. INITIAL LOAD & ROADMAP RENDERING (12 LEVELS)
        # -------------------------------------------------------------
        print("\n[TEST 1] Testing Initial Load and Level Cards Rendering...")
        page.goto(TARGET_URL)
        page.wait_for_load_state("networkidle")

        title = page.title()
        print(f"  ✓ Page Title: '{title}'")
        assert "Oxane Credit Mastery" in title, f"Unexpected page title: {title}"

        home_view = page.locator("#homeView")
        expect(home_view).to_be_visible()

        level_cards = page.locator("#levelsContainer > div")
        cards_count = level_cards.count()
        print(f"  ✓ Rendered Level Cards: {cards_count} (Expected: 12)")
        assert cards_count == 12, f"Expected 12 level cards, found {cards_count}"

        progress_text = page.locator("#overallProgressText").inner_text().strip()
        stat_completed = page.locator("#statCompleted").inner_text().strip()
        total_xp = page.locator("#totalXp").inner_text().strip()
        print(f"  ✓ Initial Progress: '{progress_text}'")
        print(f"  ✓ Initial Completed Stats: '{stat_completed}'")
        print(f"  ✓ Initial XP: '{total_xp}'")

        assert "0% Completed (0/12 Levels)" in progress_text, f"Unexpected progress: {progress_text}"
        assert stat_completed == "0 / 12", f"Unexpected completed: {stat_completed}"
        assert total_xp == "0", f"Unexpected total XP: {total_xp}"

        screenshot_1 = os.path.join(ARTIFACTS_DIR, "01_initial_roadmap_12levels.png")
        page.screenshot(path=screenshot_1)
        print(f"  📷 Captured: {screenshot_1}")

        # -------------------------------------------------------------
        # 2. HERO "CONTINUE TO NEXT LESSON" BUTTON
        # -------------------------------------------------------------
        print("\n[TEST 2] Testing Hero 'Continue to Next Lesson' Navigation...")
        continue_btn = page.locator("#heroContinueBtn, button:has-text('CONTINUE TO NEXT LESSON')")
        expect(continue_btn).to_be_visible()
        continue_btn.click()
        page.wait_for_timeout(300)

        lesson_view = page.locator("#lessonView")
        expect(lesson_view).to_be_visible()
        expect(home_view).to_be_hidden()

        lesson_level_badge = page.locator("#lessonLevelBadge").inner_text().strip()
        lesson_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Navigated to Lesson: '{lesson_level_badge}' - '{lesson_title}'")
        assert "LEVEL 1 OF 12" in lesson_level_badge.upper(), f"Unexpected lesson badge: {lesson_level_badge}"
        assert "Decoding Oxane Partners" in lesson_title, f"Unexpected title: {lesson_title}"

        # -------------------------------------------------------------
        # 3. CHECKPOINT QUIZ INTERACTION & FEEDBACK (LEVEL 1)
        # -------------------------------------------------------------
        print("\n[TEST 3] Testing Checkpoint Quiz Interactions (Level 1)...")
        quiz_options = page.locator("#quizOptions button")
        assert quiz_options.count() == 4

        # Option 0 is WRONG
        quiz_options.nth(0).click()
        page.wait_for_timeout(200)

        feedback_el = page.locator("#quizFeedback")
        expect(feedback_el).to_be_visible()
        feedback_text = feedback_el.inner_text().strip()
        assert "Not Quite" in feedback_text

        # Option 1 is CORRECT
        quiz_options.nth(1).click()
        page.wait_for_timeout(400)

        expect(feedback_el).to_be_visible()
        assert "Correct!" in feedback_el.inner_text().strip()
        assert quiz_options.nth(0).get_attribute("disabled") is not None

        modal = page.locator("#celebrationModal")
        expect(modal).to_be_visible()
        modal_title = page.locator("#celebrationHeader").inner_text().strip()
        assert "LEVEL MASTERED" in modal_title.upper()

        # -------------------------------------------------------------
        # 4. MODAL DISMISSAL & ROADMAP UPDATE
        # -------------------------------------------------------------
        print("\n[TEST 4] Testing Modal Dismissal & Roadmap Progress...")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        expect(modal).to_be_hidden()

        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(300)
        expect(home_view).to_be_visible()

        card_1_badge = page.locator("#levelsContainer > div").nth(0).locator(".rounded-full").inner_text().strip()
        card_2_badge = page.locator("#levelsContainer > div").nth(1).locator(".rounded-full").inner_text().strip()
        assert "MASTERED" in card_1_badge.upper()
        assert "CURRENT" in card_2_badge.upper()

        new_xp = page.locator("#totalXp").inner_text().strip()
        new_completed = page.locator("#statCompleted").inner_text().strip()
        assert new_xp == "50"
        assert new_completed == "1 / 12"
        print(f"  ✓ Level 1 Mastered! XP = {new_xp}, Completed = {new_completed}")

        # -------------------------------------------------------------
        # 5. LOCALSTORAGE PERSISTENCE
        # -------------------------------------------------------------
        print("\n[TEST 5] Testing LocalStorage Persistence Across Reload...")
        page.reload(wait_until="networkidle")
        reloaded_xp = page.locator("#totalXp").inner_text().strip()
        reloaded_completed = page.locator("#statCompleted").inner_text().strip()
        assert reloaded_xp == "50"
        assert reloaded_completed == "1 / 12"
        print("  ✓ State successfully persisted across reload!")

        # -------------------------------------------------------------
        # 6. MODULE FILTER TABS (MODULES 1-5)
        # -------------------------------------------------------------
        print("\n[TEST 6] Testing Module Filter Tabs Across All 5 Modules...")
        filter_tabs = [
            ("tab-1", "Module 1", 2),
            ("tab-2", "Module 2", 3),  # Levels 3, 4, 5 (Fresher Fixed Income)
            ("tab-3", "Module 3", 2),  # Levels 6, 7 (Corporate Finance & Accounting)
            ("tab-4", "Module 4", 2),  # Levels 8, 9 (Loan Underwriting)
            ("tab-5", "Module 5", 3),  # Levels 10, 11, 12 (Applied AI & Tech)
            ("tab-ALL", "All 12 Levels", 12)
        ]

        for tab_id, tab_name, expected_count in filter_tabs:
            tab_btn = page.locator(f"#{tab_id}")
            expect(tab_btn).to_be_visible()
            tab_btn.click()
            page.wait_for_timeout(200)

            visible_count = page.locator("#levelsContainer > div").count()
            print(f"  ✓ [{tab_name}] Visible cards: {visible_count} (Expected: {expected_count})")
            assert visible_count == expected_count, f"Filter {tab_id} failed: expected {expected_count}, got {visible_count}"

        # Switch back to tab-ALL
        page.locator("#tab-ALL").click()
        assert page.locator("#levelsContainer > div").count() == 12

        # -------------------------------------------------------------
        # 7. MODULE 2 FRESHER REDESIGN: LEVEL 3 (BOND FUNDAMENTALS, YTM & IRR)
        # -------------------------------------------------------------
        print("\n[TEST 7] Testing Level 3 (Bond Fundamentals, Pricing Dynamics & YTM/IRR)...")
        level_3_card = page.locator("#levelsContainer > div").nth(2)
        expect(level_3_card).to_contain_text("LEVEL 3")
        expect(level_3_card).to_contain_text("Bond Fundamentals")
        level_3_card.click()
        page.wait_for_timeout(400)

        expect(lesson_view).to_be_visible()
        l3_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Level 3 Title: '{l3_title}'")
        assert "Bond Fundamentals" in l3_title

        # Verify key user mandate requirements in DOM
        expect(page.locator("text=What happens to bond price").first).to_be_visible()
        expect(page.locator("text=IRR and How Does It Work in Bond Valuation").first).to_be_visible()
        expect(page.locator("text=Clean Price vs. Dirty Price").first).to_be_visible()
        expect(page.locator("text=Pull-to-Par").first).to_be_visible()
        print("  ✓ Level 3 Core Fixed Income Concepts verified in DOM")

        # Test Level 3 Checkpoint Quiz: Option 1 is correct (Market price increases because fixed coupons are more attractive)
        l3_quiz_options = page.locator("#quizOptions button")
        assert l3_quiz_options.count() == 4
        print("  → Clicking correct option for Level 3 (index 1 - Bond price rises as market rates fall)...")
        l3_quiz_options.nth(1).click()
        page.wait_for_timeout(300)

        expect(feedback_el).to_be_visible()
        l3_feedback = feedback_el.inner_text().strip()
        assert "Correct!" in l3_feedback
        print(f"  ✓ Level 3 Quiz Passed: '{l3_feedback[:40]}...'")

        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 8. MODULE 2 FRESHER REDESIGN: LEVEL 4 (DURATION, CONVEXITY & RATINGS)
        # -------------------------------------------------------------
        print("\n[TEST 8] Testing Level 4 (Duration, Convexity & Corporate Credit Ratings)...")
        level_4_card = page.locator("#levelsContainer > div").nth(3)
        expect(level_4_card).to_contain_text("LEVEL 4")
        expect(level_4_card).to_contain_text("Duration, Convexity")
        level_4_card.click()
        page.wait_for_timeout(400)

        expect(lesson_view).to_be_visible()
        l4_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Level 4 Title: '{l4_title}'")
        assert "Duration, Convexity" in l4_title

        # Verify key user mandate requirements in DOM
        expect(page.locator("text=Macaulay Duration vs. Modified Duration").first).to_be_visible()
        expect(page.locator("text=The Utility of Convexity in Bonds").first).to_be_visible()
        expect(page.locator("text=Assessing Corporate Credit Ratings").first).to_be_visible()
        print("  ✓ Level 4 Duration, Convexity & Ratings verified in DOM")

        # Test Level 4 Checkpoint Quiz: Option 1 is correct (Macaulay in years vs Modified in price %)
        l4_quiz_options = page.locator("#quizOptions button")
        assert l4_quiz_options.count() == 4
        print("  → Clicking correct option for Level 4 (index 1 - Macaulay balance point vs Modified price sensitivity)...")
        l4_quiz_options.nth(1).click()
        page.wait_for_timeout(300)

        expect(feedback_el).to_be_visible()
        l4_feedback = feedback_el.inner_text().strip()
        assert "Correct!" in l4_feedback
        print(f"  ✓ Level 4 Quiz Passed: '{l4_feedback[:40]}...'")

        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 9. MODULE 2 FRESHER REDESIGN: LEVEL 5 (SECURITIZATION, BANK LIQUIDITY & ASSETS)
        # -------------------------------------------------------------
        print("\n[TEST 9] Testing Level 5 (Securitization, Bank Liquidity Risk & Oxane Core Asset Classes)...")
        level_5_card = page.locator("#levelsContainer > div").nth(4)
        expect(level_5_card).to_contain_text("LEVEL 5")
        expect(level_5_card).to_contain_text("Securitization, Bank Liquidity")
        level_5_card.click()
        page.wait_for_timeout(400)

        expect(lesson_view).to_be_visible()
        l5_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Level 5 Title: '{l5_title}'")
        assert "Securitization, Bank Liquidity" in l5_title

        # Verify key user mandate requirements in DOM
        expect(page.locator("text=Why Do Banks Securitize?").first).to_be_visible()
        expect(page.locator("text=Asset-Liability Mismatch").first).to_be_visible()
        expect(page.locator("text=Which Asset Classes Does Oxane").first).to_be_visible()
        expect(page.locator("text=Significant Risk Transfer").first).to_be_visible()
        print("  ✓ Level 5 Securitization, Bank ALM & Oxane Assets verified in DOM")

        # Test Level 5 Checkpoint Quiz: Option 1 is correct (RWA relief + ALM mismatch)
        l5_quiz_options = page.locator("#quizOptions button")
        assert l5_quiz_options.count() == 4
        print("  → Clicking correct option for Level 5 (index 1 - RWA relief & ALM mismatch)...")
        l5_quiz_options.nth(1).click()
        page.wait_for_timeout(300)

        expect(feedback_el).to_be_visible()
        l5_feedback = feedback_el.inner_text().strip()
        assert "Correct!" in l5_feedback
        print(f"  ✓ Level 5 Quiz Passed: '{l5_feedback[:40]}...'")

        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 10. DIRECT NAVIGATION TO LEVEL 6 (3-STATEMENT & DEBT-TO-EQUITY)
        # -------------------------------------------------------------
        print("\n[TEST 10] Direct Navigation to Level 6 (3-Statement Financial Engine & Debt-to-Equity)...")
        level_6_card = page.locator("#levelsContainer > div").nth(5)
        expect(level_6_card).to_contain_text("LEVEL 6")
        expect(level_6_card).to_contain_text("3-Statement Financial Engine")
        level_6_card.click()
        page.wait_for_timeout(400)

        expect(lesson_view).to_be_visible()
        l6_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Level 6 Title: '{l6_title}'")
        assert "3-Statement Financial Engine" in l6_title

        # Verify Debt-to-Equity DOM blocks
        expect(page.locator("text=Debt-to-Equity (D/E) Ratio:").first).to_be_visible()
        expect(page.locator("text=Debt-to-Capital & Negative Equity:").first).to_be_visible()
        print("  ✓ Level 6 Debt-to-Equity & Ratios verified in DOM")

        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 11. DIRECT NAVIGATION TO LEVEL 12 (THE CREDIT BUILDER'S TOOLKIT)
        # -------------------------------------------------------------
        print("\n[TEST 11] Direct Navigation to Level 12 (The Credit Builder's Toolkit: SQL, Python & Excel)...")
        level_12_card = page.locator("#levelsContainer > div").nth(11)
        expect(level_12_card).to_contain_text("LEVEL 12")
        expect(level_12_card).to_contain_text("The Credit Builder's Toolkit")
        level_12_card.click()
        page.wait_for_timeout(400)

        expect(lesson_view).to_be_visible()
        l12_title = page.locator("#lessonTitle").inner_text().strip()
        print(f"  ✓ Level 12 Title: '{l12_title}'")
        assert "The Credit Builder's Toolkit" in l12_title

        # Verify Level 12 DOM content blocks
        expect(page.locator("text=The Credit Builder's Financial Trinity")).to_be_visible()
        expect(page.locator("text=1. Python-as-Excel Equivalents")).to_be_visible()
        expect(page.locator("text=List ([]) vs. Dictionary ({})")).to_be_visible()
        expect(page.locator("text=Loan Amortization Schedule Mechanics")).to_be_visible()
        expect(page.locator("text=3. Relational Data & SQL (Thinking in Tables)")).to_be_visible()
        print("  ✓ Level 12 Content verified in DOM (Builder's Trinity, Python-as-Excel, Excel Durability, Relational SQL)")

        page.locator("button:has-text('Back to Roadmap')").click()
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 12. DEMO TOGGLE (ALL 12 LEVELS MASTERED - 600 XP)
        # -------------------------------------------------------------
        print("\n[TEST 12] Demo State Toggle (All 12 Levels Mastered)...")
        demo_btn = page.locator("#demoBtn, button:has-text('Demo')")
        demo_btn.click()
        page.wait_for_timeout(300)

        progress_after_demo = page.locator("#overallProgressText").inner_text().strip()
        completed_after_demo = page.locator("#statCompleted").inner_text().strip()
        xp_after_demo = page.locator("#totalXp").inner_text().strip()

        print(f"  ✓ Progress after Demo: '{progress_after_demo}'")
        print(f"  ✓ Completed after Demo: '{completed_after_demo}'")
        print(f"  ✓ XP after Demo: '{xp_after_demo}'")

        assert "100% Completed (12/12 Levels)" in progress_after_demo
        assert completed_after_demo == "12 / 12"
        assert xp_after_demo == "600"

        # Verify reload persistence
        page.reload(wait_until="networkidle")
        reloaded_demo_progress = page.locator("#overallProgressText").inner_text().strip()
        assert "100% Completed (12/12 Levels)" in reloaded_demo_progress
        print("  ✓ 100% Mastered state (12/12) persists across page reload!")

        # -------------------------------------------------------------
        # 13. RESET BUTTON (0% RESET) & CONSOLE AUDIT
        # -------------------------------------------------------------
        print("\n[TEST 13] Reset Button & Console Audit...")
        page.once("dialog", lambda dialog: dialog.accept())
        reset_btn = page.locator("#resetBtn, button:has-text('Reset')")
        reset_btn.click()
        page.wait_for_timeout(300)

        reset_progress = page.locator("#overallProgressText").inner_text().strip()
        reset_completed = page.locator("#statCompleted").inner_text().strip()
        reset_xp = page.locator("#totalXp").inner_text().strip()

        assert "0% Completed (0/12 Levels)" in reset_progress
        assert reset_completed == "0 / 12"
        assert reset_xp == "0"
        print("  ✓ 0% reset state successfully verified!")

        print(f"  Total console errors caught:   {len(console_errors)}")
        print(f"  Total console warnings caught: {len(console_warnings)}")
        assert len(console_errors) == 0, f"Uncaught console errors: {console_errors}"
        print("  ✓ ZERO console errors across entire 12-level test suite!")

        screenshot_final = os.path.join(ARTIFACTS_DIR, "02_final_12levels_mastery.png")
        page.screenshot(path=screenshot_final)
        print(f"  📷 Captured: {screenshot_final}")

        browser.close()

    print("\n" + "=" * 70)
    print("🎉 ALL TEST SUITES PASSED FOR 12-LEVEL CURRICULUM WITH ZERO ERRORS!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"\n❌ TEST RUN ABORTED WITH FAILURE: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
