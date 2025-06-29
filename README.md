
# 🛍️ Digital Product Store

A full-stack e-commerce platform for digital products built with **Django**, featuring **seller onboarding**, **real-time order approval**, and **automated email delivery** for downloadable content.

---

## 🚀 Features

- 🔐 **User Authentication**
  - Login / Registration for customers and sellers.
  - Seller onboarding panel with shop profile.

- 🛒 **Shopping Cart**
  - Add/remove products.
  - Update quantity.
  - Auto-create cart for logged-in users.

- 💳 **Order System**
  - Customers confirm orders → status changes to `ORDER_CONFIRMED`.
  - Sellers approve or reject orders from dashboard.
  - Order email sent using **SendGrid** with download link.

- 📁 **Product Management**
  - Sellers can add, update, and soft-delete digital products.
  - Product details include title, price, category, image, and URL (digital download).

- 📧 **SendGrid Email Integration**
  - Beautiful HTML emails with product details and download button.
  - Notification for rejected/cancelled orders.

- 📦 **Order Status Flow**
  - `Cart Stage → Confirmed → Processed → Delivered / Rejected`

- 📊 **Admin & Seller Dashboards**
  - View all orders by status.
  - Customize shop settings (name, address).

---

## 🖼️ Sample Dummy Digital Products

You can showcase the store using free digital files like:
- eBooks (PDFs hosted on GitHub or Google Drive)
- Wallpapers (via direct image URL)
- Open-source templates
- Free icon packs
- Cheat sheets (coding/DSA)
- Fonts (.ttf / .zip)
- Portfolio templates

Example:
```txt
https://drive.google.com/file/d/123abc/view
https://github.com/yourname/sample-ebook.pdf
