# Oxane Credit Mastery | Private Credit Analyst Academy 💵

An institutional, gamified credit risk and private debt learning academy designed for **Credit Risk Analyst & Analytics** candidates. Built with **zero blind formula memorization**, interactive checkpoint quizzes, real-time gamification (XP, rank tiers, daily streaks), and **Progressive Web App (PWA)** offline capabilities.

---

## 🚀 Live Access & Progressive Web App (PWA)

### GitHub Pages Deployment (`github.io`)
This repository is configured out of the box for **GitHub Pages**:
1. In the repository settings on GitHub, navigate to **Settings** > **Pages**.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Choose branch `main` and root folder `/ (root)`.
4. Click **Save**. The live web app will be available at:  
   **`https://manandewan.github.io/privatecredit/`**

### Download & Install App to Mobile / Desktop
Oxane Credit Mastery is a full **Progressive Web App (PWA)** that can be downloaded and installed directly from Google Chrome, Safari, Edge, and Android/iOS devices:
- **Google Chrome (Android & Desktop)**: Click the **⬇ Install** button in the top navigation bar or the install icon (⊞) in the browser address bar.
- **Apple Safari (iPhone & iPad)**: Tap the **Share** button (⎋), scroll down and tap **Add to Home Screen** (⊞).
- **Offline Access**: The application includes a Service Worker (`sw.js`) and Web App Manifest (`manifest.json`), caching core lessons and formulas for offline study without an internet connection.

---

## 🧭 The 12-Level Master Curriculum (600 XP)

```
├── Module 1: Oxane Ecosystem & Business Model
│   ├── Level 1: Decoding Oxane Partners (3 Pillars: PMRS, Valuations & CAG, Agency EMEA)
│   └── Level 2: Asset Spectrum, 5-Stage CAG Lifecycle & The Master Pitch
├── Module 2: Fixed Income & Securitization (Fresher Edition)
│   ├── Level 3: Bond Fundamentals, Pricing Dynamics & YTM / IRR
│   ├── Level 4: Duration, Convexity & Corporate Credit Ratings
│   └── Level 5: Securitization, Bank Liquidity Risk & Oxane's Core Asset Classes
├── Module 3: Corporate Finance & Accounting
│   ├── Level 6: 3-Statement Financial Engine, $10 Depreciation & Credit Ratios (inc. Debt-to-Equity)
│   └── Level 7: Enterprise Value Cushion, Debt DCF FCFF & Top 10 Campus Technicals
├── Module 4: Loan Underwriting Case Studies
│   ├── Level 8: Institutional Loan Underwriting, S&P 6x6 Matrix & Apex Credit Memo
│   └── Level 9: Advanced Underwriting Case Studies: SaaS, Industrials & CRE Debt
└── Module 5: Applied AI & The Credit Builder's Toolkit
    ├── Level 10: Applied AI in Credit: The 5 Mission-Critical Pillars & IIT Ropar Defense
    ├── Level 11: Financial Data Science, Risk Modeling & ML Evaluation (PR-AUC, Trees)
    └── Level 12: The Credit Builder's Toolkit: SQL, Python & Excel
```

---

## 🛠️ Tech Stack & Features

- **Frontend Architecture**: Zero-build single-page web app (`index.html`) using semantic modern HTML5, Tailwind CSS, and KaTeX for LaTeX mathematical formulas.
- **Progressive Web App (PWA)**:
  - `manifest.json`: Web App Manifest defining standalone display, theme color (`#070F1E`), and responsive icons.
  - `sw.js`: Service worker implementing network-first HTML caching and cache-first asset caching.
  - `icons/`: Standard 192×192, 512×512, apple-touch-icon, and maskable icons centered around the modern Dollar (`$`) emblem.
- **State Persistence**: Automatic `localStorage` saving (`completedLevels`, `totalXp`, `streakDays`, `activeViewingId`).
- **Responsive Design**: Zero horizontal overflow on screens from 320px (compact mobile) to 4K ultra-wide monitors.

---

## 🧪 Automated Testing

Comprehensive end-to-end automated testing is implemented using **Python Playwright**:

### Run Mobile E2E Test Suite
Simulates iPhone SE (375×667), iPhone 14 (390×844), Google Pixel 7 (412×915), and Mobile Landscape (667×375):
```bash
python3 test_mobile_app.py
```

### Run Desktop E2E Test Suite
Runs through all 12 levels, checkpoint quizzes, demo modes, and reset flows:
```bash
python3 test_web_app.py
```

---

## 📄 License & Attribution

Crafted for candidates targeting Credit Risk Analyst, Credit Analytics Group (CAG), and structured finance roles at Oxane Partners, Nomura, CRISIL, and global private debt institutions.
