# Implementation Plan: Public Landing/HomeScreens (Web & Mobile)

Introduce a premium, beautiful unauthenticated welcome experience (HomeScreen) for both the **Komunity Web Application** and the **Komunity Mobile App**.

Currently, if a user is not logged in:
- The Web app automatically redirects `/` to the credentials login page because of a `@login_required` decorator on the home view.
- The Mobile app directly mounts `LoginScreen` or `SignUpScreen`.

We will implement a premium landing experience on both channels that explains the platform, shows its features (democratic group wallets, bereavement campaigns, biometrics), and lets users sign in or sign up.

---

## Proposed Changes

### Web Application (`komunityWeb`)

#### [MODIFY] [views.py](file:///c:/Users/tjman/Desktop/komunityWeb/chema/views.py)
- Remove the `@login_required` decorator from the `home` view.
- Add an authentication check:
  - If `request.user.is_authenticated` is `False`, render a new template `chema/landing.html`.
  - If `request.user.is_authenticated` is `True`, execute the existing group dashboard logic.

#### [NEW] [landing.html](file:///c:/Users/tjman/Desktop/komunityWeb/templates/chema/landing.html)
- Create a highly aesthetic, responsive public landing page using the custom Tailwind CSS installation.
- Design elements:
  - **Hero Section**: Sleek dark mode / high-contrast premium gradient, bold modern typography, high-impact headline ("Digitizing Trust, Automating Social Safety Nets").
  - **Feature Showcase**: Interactive grid highlighting:
    - *Democratic Group Wallets*: Multi-member audits and transparent controls.
    - *Automated Bereavement*: Instant contribution campaigns.
    - *Biometric Security*: Fingerprint/FaceID locked payouts to prevent fraud.
    - *Multi-Channel Payments*: Mobile money, card, and bank support.
  - **Social Impact Stokvel/Chama Metrics**: Sleek data cards showing transaction volumes and payout speeds.
  - **Call to Action (CTA)**: High-visibility buttons to "Sign In" or "Join Komunity".

#### [MODIFY] [nav2.html](file:///c:/Users/tjman/Desktop/komunityWeb/templates/partials/nav2.html)
- Update the main navbar so it works elegantly for both authenticated and unauthenticated visitors:
  - Wrap internal dashboard navigation links (Home, My Groups, Contributions, Join Group, Create Group) inside `{% if user.is_authenticated %}`.
  - Hide the wallet balance snippet and the user profile dropdown if `user.is_authenticated` is false.
  - Add polished "Sign In" and "Create Account" buttons in the right section for unauthenticated visitors.

---

### Mobile Application (`KomunityMobile`)

#### [NEW] [WelcomeScreen.tsx](file:///c:/Users/tjman/Desktop/KomunityMobile/src/screens/WelcomeScreen.tsx)
- Create a premium onboarding screen that acts as the unauthenticated home.
- UI Highlights:
  - Gradient background, vibrant custom brand colors, sleek modern font scaling.
  - Dynamic micro-animations or modern cards describing Stokvel mutual aid, instant payouts, and high-trust biometrics.
  - Custom buttons: "Sign In" (sleek secondary/outlined style) and "Get Started / Sign Up" (vibrant filled primary button) with native haptic feedback (`expo-haptics`).

#### [MODIFY] [App.tsx](file:///c:/Users/tjman/Desktop/KomunityMobile/App.tsx)
- Add state to track whether the user is viewing the Welcome screen (`showWelcome`, default `true`).
- When `!isLoggedIn`:
  - If `showWelcome` is `true`, render the new `<WelcomeScreen>` component.
  - On `WelcomeScreen`, clicking "Sign In" sets `showWelcome(false)` and `isSigningUp(false)`.
  - Clicking "Sign Up" / "Get Started" sets `showWelcome(false)` and `isSigningUp(true)`.
  - Update `LoginScreen` and `SignUpScreen` so their "Back" actions can return to the `WelcomeScreen`.

---

## Verification Plan

### Manual Verification
1. **Web App**:
   - Access `http://127.0.0.1:8000/` as an unauthenticated guest. Verify that the new beautiful landing page is shown, scrolling is responsive, and layout rules are satisfied.
   - Click "Sign In" / "Sign Up" to confirm routing to Allauth templates.
   - Log in and verify that the page seamlessly displays the active group feed dashboard.
2. **Mobile App**:
   - Launch the mobile app and verify the new welcome/landing home screen is loaded by default.
   - Test interaction buttons (Sign In, Get Started) to ensure they transition smoothly to the credential inputs.
   - Verify that clicking back returns the user to the landing screen.
