---
name: FoodShare Network
colors:
  surface: '#f7f9ff'
  surface-dim: '#d1dbe8'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#edf4ff'
  surface-container: '#e4effd'
  surface-container-high: '#dfe9f7'
  surface-container-highest: '#d9e3f1'
  on-surface: '#121d26'
  on-surface-variant: '#3f4941'
  inverse-surface: '#27313c'
  inverse-on-surface: '#e8f2ff'
  outline: '#707a70'
  outline-variant: '#bfc9be'
  surface-tint: '#1b6c40'
  primary: '#00562e'
  on-primary: '#ffffff'
  primary-container: '#1f6f43'
  on-primary-container: '#a0efb8'
  inverse-primary: '#89d7a2'
  secondary: '#835400'
  on-secondary: '#ffffff'
  secondary-container: '#feb64e'
  on-secondary-container: '#714800'
  tertiary: '#0040ae'
  on-tertiary: '#ffffff'
  tertiary-container: '#0956df'
  on-tertiary-container: '#d4dcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#a5f4bc'
  primary-fixed-dim: '#89d7a2'
  on-primary-fixed: '#00210f'
  on-primary-fixed-variant: '#00522c'
  secondary-fixed: '#ffddb5'
  secondary-fixed-dim: '#ffb956'
  on-secondary-fixed: '#2a1800'
  on-secondary-fixed-variant: '#643f00'
  tertiary-fixed: '#dbe1ff'
  tertiary-fixed-dim: '#b4c5ff'
  on-tertiary-fixed: '#00174b'
  on-tertiary-fixed-variant: '#003ea8'
  background: '#f7f9ff'
  on-background: '#121d26'
  surface-variant: '#d9e3f1'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 3.5rem
    fontWeight: '700'
    lineHeight: 4.25rem
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Inter
    fontSize: 2.25rem
    fontWeight: '700'
    lineHeight: 2.75rem
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: '600'
    lineHeight: 2.5rem
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 1.625rem
    fontWeight: '600'
    lineHeight: 2.125rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
  headline-sm:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
  title-md:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.5rem
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-lg:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.025em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system powers an enterprise-grade administrative portal dedicated to food resource redistribution, aligned directly with UN Sustainable Development Goals (SDG 2: Zero Hunger and SDG 12.3: Halving Global Food Waste). 

### Personality & Core Attributes
- **Institutional Trust & Rigor:** The system conveys operational reliability, traceability, and accountability. It avoids whimsical or gamified tropes in favor of crisp administrative clarity.
- **Empathetic Efficiency:** Designed for high-stress operational logistics—kitchen managers donating surplus food during closing hours, logistics dispatchers routing refrigerated transports, and food bank coordinators verifying safety seals.
- **Ecological Stewardship:** Grounded in organic forest tones and warm agrarian accents that communicate vitality, shelf-life freshness, and social purpose without compromising high-density data readability.

### Design Movement & Aesthetic Approach
The design language is **Modern Institutional Material** with warm humanistic sensibilities:
- Generous structural whitespace framing data-dense tables, metric cards, and validation workflows.
- Purpose-driven contrast meeting strict WCAG 2.1 AA/AAA compliance across inventory tables, form fields, and batch dispatch logs.
- Tactile affordances derived from soft tonal layering, crisp micro-borders, and minimal optical depth.

## Colors

The color palette centers on agricultural regeneration (deep forest green), logistics urgency and safety warnings (warm amber), operational lifecycle tracking (vibrant blue), and high-legibility slate neutrals.

### Palette Hierarchy & Intent
- **Primary (`#1F6F43` - Forest Green):** Anchors institutional authority, primary call-to-actions (e.g., "Registrar Donación", "Confirmar Despacho"), active global navigation, and brand signatures. Supported by `#2A8F57` for hover/focus states and `#E9F5EE` for primary container surfaces.
- **Secondary / Accent (`#E8A33D` - Warm Amber):** Denotes temporal urgency, impending batch expirations (*próximo a vencer*), and items awaiting validation. Supported by `#FDF4E7` for alert containers and pending status tags.
- **Tertiary (`#2563EB` - Vibrant Blue):** Dedicated exclusively to operational reservation states (*Reservada*), logistics route handoffs, and external carrier tracking.
- **Neutral Core (`#1F2933` - Dark Slate Grey):** Primary typography and structural framing, delivering superior legibility over soft cream canvases compared to pure black.
- **Neutral Muted (`#52606D` - Muted Slate):** Secondary labels, metadata timestamps, table headers, and inactive icon states.
- **Surfaces & Canvases:** Base app canvas uses an organic Off-white/Soft Cream (`#F7F8F5`) to reduce glare during prolonged operational use. Data surfaces, modal dialogs, and cards utilize Pure White (`#FFFFFF`). Structural division is enforced through Subtle Grey (`#E4E7EB`).

### Operational Status Tokens
Status indicators govern critical inventory lifecycles and require dedicated color pairings (background tint + solid stroke/text):
- **Disponible (Available):** `#1F6F43` text on `#E9F5EE` fill; `#22C55E` accent dot.
- **Pendiente / Próximo a Vencer (Pending / Nearing Expiry):** `#B45309` text on `#FDF4E7` fill; `#F59E0B` indicator.
- **Reservada (Reserved / En Tránsito):** `#1D4ED8` text on `#EFF6FF` fill; `#2563EB` indicator.
- **Entregada (Delivered / Archivo):** `#374151` text on `#F3F4F6` fill; `#6B7280` indicator.
- **Vencida / Rechazada / Error (Expired / Rejected):** `#B91C1C` text on `#FEF2F2` fill; `#DC2626` indicator.

## Typography

The type scale is powered entirely by **Inter**, selected for its optical neutrality, tall x-height, and open aperture clarity when reading complex tabular logistics data or small-scale batch numbers on mobile devices.

### Typographic Rules
- **Numerical Alignment:** All tabular metrics, weight volumes (kg, tons), batch IDs, and expiry countdowns must employ tabular lining figures (`font-variant-numeric: tabular-nums`) to ensure strict visual vertical alignment across ledger tables.
- **Hierarchy & Weight:** Semibold (`600`) is reserved for headlines, entity titles, card headers, and interactive labels. Regular (`400`) carries all descriptive narratives, data table rows, and helper copy. Bold (`700`) is constrained exclusively to top-level KPI metrics in dashboard summary rows.
- **Mobile Density:** Headline roles shift proportionally via breakpoint tokens to prevent headline clipping and preserve operational vertical screen real estate.

## Layout & Spacing

The portal adheres to a structured **fluid-responsive grid** built on an 8pt base spatial unit, scaling cleanly from dockside mobile devices to dual-monitor dispatch stations.

### Grid & Breakpoints
- **Desktop (1280px+):** 12-column layout. Margin: `2rem` (32px), Gutters: `1.5rem` (24px). Sidebar navigation remains pinned at 280px width, while main operational panels flex fluidly up to a maximum reading container of 1600px.
- **Tablet (768px – 1279px):** 8-column layout. Margin: `1.5rem` (24px), Gutters: `1rem` (16px). Navigation collapses to an icon rail (72px) or off-canvas drawer.
- **Mobile (< 768px):** 4-column layout. Margin: `1rem` (16px), Gutters: `1rem` (16px). Multi-column tables convert into stacked card interfaces with persistent sticky actions.

### Spacing Application Rules
- `space-xs` (4px): Micro gaps between status badge icons and text labels; nested form item margins.
- `space-sm` (8px): Button icon-to-label separation; spacing between compact list rows.
- `space-md` (16px): Internal padding for data cells, form field vertical margins, and compact cards.
- `space-lg` (24px): Standard structural padding within dashboard cards, modals, and container headers.
- `space-xl` (32px): Vertical separation between distinct operational modules (e.g., metric counters and recent activity feeds).

## Elevation & Depth

To preserve an orderly administrative interface and avoid visual fatigue, this design system rejects heavy, dark dropshadows. Instead, elevation is expressed through **tonal separation**, **crisp border definition**, and **diffused ambient shadows** tinted with dark slate.

### Elevation Hierarchy
- **Level 0 (Flat Canvas):** Off-white base canvas (`#F7F8F5`). Borders are omitted; separation occurs purely through spatial margins.
- **Level 1 (Card & Surface Base):** Pure white cards (`#FFFFFF`) sitting on the `#F7F8F5` background. Rendered with a subtle structural boundary of `1px solid #E4E7EB` combined with an ambient shadow: `0 1px 3px 0 rgba(31, 41, 51, 0.04), 0 1px 2px -1px rgba(31, 41, 51, 0.02)`.
- **Level 2 (Interactive / Hover):** Activated cards, hover states for donor listings, and table row emphasis: `0 4px 6px -1px rgba(31, 41, 51, 0.07), 0 2px 4px -2px rgba(31, 41, 51, 0.04)`, accompanied by border shift to `#D2D6DC`.
- **Level 3 (Overlays & Dropdowns):** Role switcher dropdowns, date pickers, filter flyouts: `0 10px 15px -3px rgba(31, 41, 51, 0.08), 0 4px 6px -4px rgba(31, 41, 51, 0.03)` with border `#E4E7EB`.
- **Level 4 (Modals & Urgent Dispatch Dialogs):** Centered modal viewports: `0 20px 25px -5px rgba(31, 41, 51, 0.10), 0 8px 10px -6px rgba(31, 41, 51, 0.05)`, placed over a tinted backdrop of `rgba(31, 41, 51, 0.45)`.

## Shapes

The design system implements **Level 2 (Rounded)** curvature. This standard balances soft approachability with the structural discipline required for tabular enterprise software.

### Shape Geometry Rules
- **Base Components (`rounded`, 0.5rem / 8px):** Standard input fields, button groups, list items, action chips, and nested sub-panels.
- **Containers & Surface Cards (`rounded-lg`, 0.75rem to 1rem / 12px to 16px):** Primary dashboard cards, analytical widgets, filter sidebars, and dialogue modals.
- **Pill Geometry (Full Radius / 9999px):** Status badges, role indicators, counter tags, and avatar frames. Never use pill shapes for primary form inputs or standard action buttons.

## Components

### 1. Buttons
- **Primary:** Forest green background (`#1F6F43`), white text (`#FFFFFF`), `font-weight: 600`, height: 40px (desktop) / 44px (mobile), border radius: 8px. Hover state deepens to `#2A8F57`. Focus rings must present a 2px offset ring of `#1F6F43`.
- **Secondary / Outlined:** Transparent background, 1.5px border in `#1F6F43`, text in `#1F6F43`. Hover triggers `#E9F5EE` background fill.
- **Subtle / Ghost:** Slate muted text (`#52606D`), no border. Hover triggers `#F3F4F6` background.
- **Destructive:** Crimson Red (`#DC2626`) fill or outline, reserved for cancelling delivery routes, marking food as spoiled, or purging records.

### 2. Status Chips & Role Badges
- **Status Chips:** Pill-shaped (`rounded-full`), height: 24px, padding: 2px 10px. Typography uses `label-md` (`font-weight: 600`). Accompanied by a 6px solid circular status dot preceding the text.
- **Role Switcher Badges:** Prominently featured in top navigation to delineate operating contexts:
  - *Restaurante Donante:* Amber tint base (`#FDF4E7`), text & icon `#B45309`.
  - *Fundación Receptora:* Blue tint base (`#EFF6FF`), text & icon `#1D4ED8`.
  - *Administrador de Red:* Forest Green tint base (`#E9F5EE`), text & icon `#1F6F43`.

### 3. Form Inputs & Selectors
- **Structure:** Explicit floating or top-aligned labels rendered in `label-lg` using Dark Slate Grey (`#1F2933`).
- **Fields:** Minimum height of 42px, background `#FFFFFF`, border: `1.5px solid #E4E7EB`, border-radius: 8px, padding: `0.5rem 0.875rem`.
- **States:** Hover border changes to `#52606D`. Active/Focus changes border to `#1F6F43` with a box-shadow halo of `0 0 0 3px rgba(31, 111, 67, 0.15)`. Error states invoke `#DC2626` borders and helper text.
- **Mandatory Units:** Specialized weight/quantity inputs must feature fixed suffix lockups (e.g., "kg", "raciones", "cajas térmicas") rendered in `#52606D`.

### 4. Cards
- **Base Layout:** `#FFFFFF` background, 1px border `#E4E7EB`, 12px border radius, 24px internal padding (`space-lg`).
- **Inventory Donation Cards:** Must include:
  1. Header with Food Category tag and absolute Expiration Countdown.
  2. Main body with donation title, donor establishment name, and verified weight.
  3. Footer containing logistical criteria (refrigeration required, allergen flags) and immediate action button ("Reservar", "Validar").

### 5. Selection Controls (Checkboxes & Radios)
- **Checkboxes:** 18x18px, 4px border radius. Unselected: 1.5px border `#E4E7EB`. Selected: `#1F6F43` fill with white checkmark icon.
- **Radio Buttons:** 18x18px circular. Selected state features `#1F6F43` outer border with a centered `#1F6F43` inner dot (8px).

### 6. Food Expiration Countdown Timers
Specialized visual indicator for items approaching safety expiration windows:
- **> 24 hours remaining:** Slate neutral tag (`#52606D`).
- **< 12 hours remaining:** Warning tag (`#E8A33D` background tint, `#B45309` text, pulsing amber clock icon).
- **< 3 hours remaining / Critical:** Crimson tag (`#FEF2F2` background, `#DC2626` text, urgent high-contrast countdown).