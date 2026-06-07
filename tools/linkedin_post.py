import asyncio
from playwright.async_api import async_playwright

PROFILE_DIR = "linkedin_profile"

# ✅ GLOBAL LOCK (prevents multiple Telegram triggers breaking UI)
POST_LOCK = asyncio.Lock()


async def post_to_linkedin(content: str):

    async with POST_LOCK:

        async with async_playwright() as p:

            # ---------------- PERSISTENT LOGIN ----------------
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=False,
                slow_mo=300
            )

            page = await context.new_page()

            # ---------------- OPEN LINKEDIN ----------------
            await page.goto(
                "https://www.linkedin.com/feed/",
                wait_until="domcontentloaded"
            )

            await page.wait_for_timeout(5000)

            # ---------------- LOGIN CHECK ----------------
            if "login" in page.url:
                print("❌ Logged out. Please login once manually.")
                await context.close()
                return

            print("✅ LinkedIn session active")

            # ---------------- CLICK START POST ----------------
            try:
                start_btn = page.get_by_role("button", name="Start a post")
                await start_btn.wait_for(timeout=20000)
                await start_btn.click()

            except Exception:
                try:
                    await page.locator("button[aria-label='Start a post']").click(timeout=10000)
                except Exception:
                    await page.locator("span:has-text('Start a post')").first.click()

            await page.wait_for_timeout(4000)

            # ---------------- WAIT FOR MODAL ----------------
            try:
                await page.wait_for_selector("div[role='dialog']", timeout=20000)
                print("📦 Post modal opened")
            except Exception:
                print("❌ Post modal not found")
                await context.close()
                return

            # ---------------- FIND TEXTBOX (ROBUST FIX) ----------------
            box = None

            try:
                box = page.locator("div[role='dialog'] div[role='textbox']").first
                await box.wait_for(timeout=20000)

            except Exception:
                try:
                    box = page.locator("div[role='textbox']").first
                    await box.wait_for(timeout=20000)
                except Exception:
                    print("❌ Textbox not found")
                    await context.close()
                    return

            # ---------------- TYPE CONTENT ----------------
            try:
                await box.click()
                await box.fill(content)
                print("✍️ Post added")
            except Exception as e:
                print("❌ Failed typing:", e)
                await context.close()
                return

            await page.wait_for_timeout(2000)

            # ---------------- CLICK POST ----------------
            try:
                post_btn = page.get_by_role("button", name="Post")
                await post_btn.wait_for(timeout=20000)
                await post_btn.click()

            except Exception:
                try:
                    await page.locator("button.share-actions__primary-action").click(timeout=10000)
                except Exception as e:
                    print("❌ Post button failed:", e)
                    await context.close()
                    return

            print("🚀 Posted successfully!")

            await page.wait_for_timeout(5000)

            await context.close()