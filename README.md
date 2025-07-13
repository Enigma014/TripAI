# 🏕 KOA Campground Reservation Bot

This is an automated web scraping bot built using Python and Selenium to search for and initiate campground reservations on [koa.com](https://koa.com). It simulates a user filling out the reservation form, applying filters, and proceeding to the price page.

---

## 📌 Features

- Searches for campgrounds based on location and date
- Fills guest information (adults, children, etc.)
- Applies filters: equipment type, length, pets, slideouts
- Automatically clicks "RESERVE NOW"
- Fills the second reservation form
- Extracts final pricing (if available)

---

## ⚙️ Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver
- Dependencies in `requirements.txt`:
  - `undetected-chromedriver`
  - `selenium`

---

## 🛠 Setup Instructions![Uploading Screenshot 2025-07-13 at 6.15.18 PM.png…]()


1. **Clone the repo:**
   ```bash![Uploading Screenshot 2025-07-13 at 6.14.49 PM.png…]()

   git clone https://github.com/your-username/koa-reservation-bot.git
   cd koa-reservation-bot
# Troubleshooting
You might be prompted to check the cloudfare checkbox do that manually.
