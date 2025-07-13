import sys
import time
import base64
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSessionIdException

# ------------------------ Utility Functions ------------------------

def capture_debug_screenshot(driver, name="debug.png"):
    driver.save_screenshot(name)
    print(f"[📸] Screenshot saved: {name}")

def wait_for_dom_ready(driver, timeout=20):
    print("[⏳] Waiting for DOM to fully load...")
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    print("[✅] DOM is fully loaded.")

def wait_for_element(driver, by, identifier, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, identifier))
    )

def wait_and_click(driver, by, identifier, timeout=20):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, identifier))
    )
    element.click()
    print(f"[🖱️] Clicked element: {identifier}")
    return element

def smart_sleep(seconds, label="Waiting"):
    print(f"[⏱️] {label} for {seconds} second(s): ", end="", flush=True)
    for i in range(seconds):
        print(".", end="", flush=True)
        time.sleep(1)
    print(" done.")

# ------------------------ Configuration ------------------------

# Accept profile ID from CLI or default
profile_id = sys.argv[1] if len(sys.argv) > 1 else "default"

# User-defined search values
LOCATION = "USA"
CHECKIN_DATE = "08/01/2025"
CHECKOUT_DATE = "08/10/2025"
NUM_ADULTS = "2"
NUM_CHILDREN = "0"
NUM_FREE="0"
EQUIPMENT = "V"
LENGTH = "10"

# ------------------------ Browser Setup ------------------------

print(f"[🌐] Starting browser with profile: {profile_id}")
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, user_data_dir=f"selenium_session_{profile_id}")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    """
})

print("[🌐] Navigating to KOA Search Page...")
driver.get("https://koa.com/search/")
# capture_debug_screenshot(driver, "after_open.png")

smart_sleep(5, "Initial load buffer")

wait_for_dom_ready(driver)

# ------------------------ Fill Form ------------------------

print("[🧾] Filling search form...")

# Location
location_input = wait_for_element(driver, By.ID, "txtLocation")
location_input.clear()
location_input.send_keys(LOCATION)
print(f"[📍] Entered location: {LOCATION}")
smart_sleep(3, "Waiting for suggestions")
smart_sleep(1, "Waiting")
# Dates
checkin_input = wait_for_element(driver, By.ID, "checkInDate")
checkout_input = wait_for_element(driver, By.ID, "checkOutDate")

checkin_input.clear()
checkin_input.send_keys(CHECKIN_DATE)
print(f"[📅] Check-in date: {CHECKIN_DATE}")

checkout_input.clear()
checkout_input.send_keys(CHECKOUT_DATE)
print(f"[📅] Check-out date: {CHECKOUT_DATE}")
smart_sleep(2)

# Submit search to show filters
wait_and_click(driver, By.ID, "btnApplyFilter")
smart_sleep(5, "Waiting for filters to render")

# ------------------------ Fill Filters ------------------------

print("[🎚️] Applying guest filters...")
campgrounds = driver.find_elements(By.CLASS_NAME, "campground-listing")

# Adults
adults_dropdown = wait_for_element(driver, By.ID, "Adults")
Select(adults_dropdown).select_by_value(NUM_ADULTS)
print(f"[👤] Selected adults: {NUM_ADULTS}")

# Children
children_dropdown = wait_for_element(driver, By.ID, "Children")
Select(children_dropdown).select_by_value(NUM_CHILDREN)
print(f"[🧒] Selected children: {NUM_CHILDREN}")

smart_sleep(1, "Waiting")

# Equipment

equipment_dropdown = wait_for_element(driver, By.ID, "EquipmentType")
Select(equipment_dropdown).select_by_value(EQUIPMENT)
print(f"[🧒] Selected Equipment: {EQUIPMENT}")

smart_sleep(1, "Waiting")
 
#length
length_input = wait_for_element(driver, By.ID, "EquipmentLength")
length_input.clear()
length_input.send_keys(LENGTH)
print(f"[📍] Entered Length: {LENGTH}")

smart_sleep(1, "Waiting")


# Slideouts: Select "No"
slideout_radio = driver.find_element(By.XPATH, '//input[@name="SlideOuts" and @value="No"]')
driver.execute_script("arguments[0].click();", slideout_radio)
print("[🚐] Selected: No Slideouts")

# Pets: Select "No"
pets_radio = driver.find_element(By.XPATH, '//input[@name="Pets" and @value="No"]')
driver.execute_script("arguments[0].click();", pets_radio)
print("[🐶] Selected: No Pets")

smart_sleep(1, "Waiting")


# Final apply
wait_and_click(driver, By.ID, "btnApplyFilter")
print("[🔍] Final search applied.")

smart_sleep(20, "Waiting for results")

print("[🔍] Scraping campground results...\n")

# Wait for all campground listings to load

# ------------------ Navigate to First Campground ------------------

    # Step 2: Fill second reservation form

    # --- Set guest counts ---
# Wait for all campground listings to load
campgrounds = driver.find_elements(By.CLASS_NAME, "campground-listing")
print(f"[📋] Found {len(campgrounds)} campgrounds.")

# ------------------ Navigate to First Campground ------------------

try:
    # Step 1: Click "RESERVE NOW"
    print("inside the try block")
    reserve_now_span = wait_for_element(driver, By.XPATH, "//span[text()='RESERVE NOW']")
    reserve_now_button = reserve_now_span.find_element(By.XPATH, "./ancestor::a")
    driver.execute_script("arguments[0].click();", reserve_now_button)
    print("[🖱️] Clicked RESERVE NOW button")

    smart_sleep(3)

    # Step 2: Fill second reservation form

    # --- Set guest counts ---
    def set_input_with_events(driver, field_id, value):
        driver.execute_script("""
            const input = document.getElementById(arguments[0]);
            input.value = arguments[1];
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, field_id, value)
        print(f"[✅] Set {field_id} to {value} (with JS events)")




    set_input_with_events(driver, "Reservation_Adults", "2")
    set_input_with_events(driver, "Reservation_Kids", "0")
    set_input_with_events(driver, "Reservation_Free", "0")


    # --- Equipment Type ---
    try:
        equipment_dropdown = wait_for_element(driver, By.ID, "Reservation_EquipmentType")
        Select(equipment_dropdown).select_by_visible_text("Van")
        print("[🚐] Equipment Type: Van")
    except:
        print("[⚠️] Could not set Equipment Type to 'Van'")

# --- Length ---
    try:
        length_input = wait_for_element(driver, By.ID, "Reservation_EquipmentLength")
        length_input.clear()
        length_input.send_keys("2")
        print("[📏] Length: 2")
    except:
        print("[⚠️] Could not set Length")

    # --- Slideouts ---
    slideouts_radio = wait_for_element(driver, By.XPATH, '//input[@name="Reservation.SlideOuts" and @value="No"]')
    driver.execute_script("arguments[0].click();", slideouts_radio)
    print("[📦] No Slideouts selected")

    # --- Pets ---
    pets_radio = wait_for_element(driver, By.XPATH, '//input[@name="Reservation.Pets" and @value="No"]')
    driver.execute_script("arguments[0].click();", pets_radio)
    print("[🐾] No Pets selected")


    smart_sleep(2, "Waiting after second form fill")

    # --- Click Next ---
    next_button = wait_for_element(driver, By.ID, "nextButton")
    next_button.click()
    print("[➡️] Clicked Next button")

    smart_sleep(5, "Waiting for price page")

    # --- Scrape Price ---
    try:
        price_element = wait_for_element(driver, By.XPATH, "//span[contains(text(), '$')]", timeout=10)
        price = price_element.text.strip()
        print(f"[💲] Price: {price}")
    except:
        print("[📭] No price available. Likely no reservation slots.")


except InvalidSessionIdException:
    print("[❌] Browser session lost! Chrome crashed or closed.")
except Exception as e:
    print(f"[❌] Some other error: {e}")







#smart_sleep(20, " Data scraping complete. Note: Site is currently down, so no prices were available. Toodles - ")

# Uncomment to quit when done
# driver.quit()
