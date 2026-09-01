<div align="center">
  
# 🏗️ Lateral Torsional Buckling Design of Welded I-Section

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![IRC 24](https://img.shields.io/badge/Design%20Code-IRC%2024%3A2010-orange)](#design-codes)
[![IS 800](https://img.shields.io/badge/Design%20Code-IS%20800%3A2007-orange)](#design-codes)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python IDE](https://img.shields.io/badge/IDE-Python%20IDE-3776AB?logo=python&logoColor=white)](https://www.onlineide.pro/playground/python?utm_source=online-python&utm_medium=navbar&utm_campaign=onlineidepro)

</div>

<div align="center">

### 🐍 Try It Online — No Installation Required!

**Copy • Run • Test • Python directly in your browser**

<a href="https://www.onlineide.pro/playground/python?utm_source=online-python&utm_medium=navbar&utm_campaign=onlineidepro">
  <img src="https://img.shields.io/badge/🚀%20Launch%20Python%20IDE-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Launch Python IDE">
</a>

</div>

> **A Python-based calculation tool for evaluating the flexural capacity of welded steel I-sections considering Lateral Torsional Buckling (LTB), section classification, slender-element effects, and effective section properties.**

**Design Basis:** `IRC:24-2010` / `IS 800:2007`
**Language:** Python 🐍
**Application:** Steel Bridge & Structural Design

---

## 📌 Overview

This tool performs a **step-by-step Lateral Torsional Buckling analysis** of welded I-sections subjected to flexure.

The program calculates:

* 🔹 Section classification
* 🔹 Gross section properties
* 🔹 Elastic and plastic section modulus
* 🔹 Minor-axis radius of gyration
* 🔹 Elastic critical LTB moment `Mcr`
* 🔹 Non-dimensional LTB slenderness `λLT`
* 🔹 LTB reduction factor `χLT`
* 🔹 Design bending stress `fbd`
* 🔹 Design flexural capacity considering LTB
* 🔹 Flexural capacity ignoring LTB
* 🔹 Effective section properties for slender sections
* 🔹 Detailed step-by-step calculation output

The tool is particularly useful for **welded plate girders, bridge girders, crane girders, and other fabricated steel I-sections**.

---

## ✨ Key Features

| Feature                       | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| 🏗️ **Welded I-Section**      | Designed specifically for fabricated/welded I-sections |
| 📐 **Section Classification** | Plastic, Compact, Semi-compact or Slender              |
| 🔄 **LTB Analysis**           | Calculates elastic critical buckling moment            |
| 📊 **Buckling Curves**        | Supports Curve `c` and Curve `d`                       |
| 🧮 **Effective Properties**   | Calculates effective properties for slender sections   |
| 📈 **Section Properties**     | Area, centroid, `Iz`, `Iy`, `ry`, `Ze`, `Zp`           |
| ⚙️ **User Inputs**            | Section dimensions, steel grade, unbraced length, etc. |
| 📝 **Detailed Output**        | Displays intermediate calculations and formulas        |
| 🎯 **Design Comparison**      | Compares capacity with and without LTB                 |
| 🇮🇳 **Indian Standards**     | Intended for IRC / IS-based steel design workflows     |

---

# 📚 Design Standards

The calculation framework is based on the following standards:

### 🇮🇳 IRC:24-2010

**Standard Specification and Code of Practice for the Design of Steel Road Bridges**

Used primarily for:

* Section classification
* Compression flange classification
* Web classification
* Steel bridge design considerations

### 🇮🇳 IS 800:2007

**General Construction in Steel — Code of Practice**

Used for:

* Flexural design
* Lateral torsional buckling
* Buckling reduction factors
* Effective section properties
* Design bending stress

> ⚠️ **Important:** The implementation should be independently checked against the applicable editions, clauses, tables and project-specific design requirements before use for a final design submission.

---

# 🔄 Calculation Workflow

```text
             ┌────────────────────────┐
             │   SECTION INPUTS       │
             │ bf, tf, d, tw, fy      │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ SECTION CLASSIFICATION │
             │ Plastic / Compact /    │
             │ Semi-compact / Slender │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ GROSS SECTION          │
             │ PROPERTIES             │
             │ A, Iz, Iy, ry, Ze, Zp  │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ EFFECTIVE PROPERTIES   │
             │ For Slender Sections   │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ ELASTIC CRITICAL       │
             │ MOMENT Mcr             │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ LTB SLENDERNESS        │
             │ λLT                    │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ REDUCTION FACTOR       │
             │ χLT                    │
             └────────────┬───────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ DESIGN MOMENT CAPACITY │
             │ Md                     │
             └────────────────────────┘
```

---

# 📐 Section Input

The program considers a welded asymmetric I-section:

```text
                 TOP FLANGE
        ┌─────────────────────────┐
        │                         │
        └──────────┬──────────────┘
                   │
                   │
                   │
                   │  WEB
                   │
                   │
        ┌──────────┴──────────────┐
        │                         │
        └─────────────────────────┘
              BOTTOM FLANGE
```

### Required Inputs

| Parameter       | Description             | Unit  |
| --------------- | ----------------------- | ----- |
| `bf_top`        | Top flange width        | mm    |
| `tf_top`        | Top flange thickness    | mm    |
| `bf_bot`        | Bottom flange width     | mm    |
| `tf_bot`        | Bottom flange thickness | mm    |
| `d_web`         | Web depth               | mm    |
| `tw`            | Web thickness           | mm    |
| `L_lt`          | LTB unbraced length     | m     |
| `fy`            | Yield strength          | MPa   |
| `section_class` | Section classification  | —     |
| `curve`         | LTB buckling curve      | c / d |
| `γm0`           | Partial safety factor   | —     |

---

# 🧮 Section Classification

The program automatically determines the section class based on the **compression flange** and **web**.

The possible classifications are:

```text
Plastic
   ↓
Compact
   ↓
Semi-compact
   ↓
Slender
```

The more critical classification between the compression flange and web is adopted as the overall section classification.

### Compression Flange

For welded sections:

```text
b/t = [(bf - tw) / 2] / tf
```

The program evaluates this ratio against the applicable limits.

### Web

The web slenderness is evaluated as:

```text
d/tw
```

The program then identifies:

```text
Plastic
Compact
Semi-compact
Slender
```

---

# 📊 Gross Section Properties

The program calculates:

### Area

```text
A = A_top + A_web + A_bottom
```

### Centroid

The centroid is obtained using:

```text
ȳ = Σ(Aᵢ yᵢ) / ΣAᵢ
```

### Major-Axis Moment of Inertia

The individual flange and web contributions are combined using the parallel-axis theorem.

```text
Iz = Σ(Iᵢ + Aᵢdᵢ²)
```

### Minor-Axis Moment of Inertia

```text
Iy =
(tf_top × bf_top³ / 12)
+
(tf_bot × bf_bot³ / 12)
+
(d_web × tw³ / 12)
```

### Radius of Gyration

```text
ry = √(Iy / A)
```

### Elastic Section Modulus

```text
Ze = Iz / yextreme
```

### Plastic Section Modulus

The program determines the plastic neutral axis and calculates:

```text
Zp
```

for the asymmetric I-section.

---

# 🧱 Slender Section Treatment

When the section is classified as **Slender**, the program reduces the effective compression elements.

### Effective Flange Width

The effective width is determined using the calculated plate slenderness parameter:

```text
λp = (b/t) / [28.4 ε √ψ]
```

and the effective width factor:

```text
ρ = (λp - 0.188) / λp²
```

The effective width is then:

```text
beff = ρ × b
```

---

## Effective Web Depth

For a slender web, the program determines the effective compressed web depth.

The resulting effective section is then used to calculate:

* Effective area
* Effective centroid
* Effective `Iz`
* Effective elastic section modulus

```text
Ze,eff = Iz,eff / yextreme
```

---

# 🔄 Lateral Torsional Buckling

The core calculation is the elastic critical moment:

```text
Mcr
```

The program uses:

```text
Mcr =
(π² E Iy hf / 2L²)
×
√[1 + (1/20)((L/ry)/(hf/tf))²]
```

where:

| Parameter | Meaning                          |
| --------- | -------------------------------- |
| `E`       | Young's modulus                  |
| `Iy`      | Minor-axis moment of inertia     |
| `hf`      | Flange centre-to-centre distance |
| `Llt`     | Unbraced length                  |
| `ry`      | Minor-axis radius of gyration    |
| `tf`      | Compression flange thickness     |

---

# 📈 LTB Slenderness

The non-dimensional LTB slenderness is calculated as:

```text
λLT = √(Meff / Mcr)
```

where:

```text
Meff = effective reference moment capacity
```

The program then determines whether LTB governs.

### If:

```text
λLT ≤ 0.4
```

the program considers:

```text
χLT = 1.0
```

and LTB does not govern.

### Otherwise

The appropriate reduction factor is calculated using the selected buckling curve.

---

# 📉 LTB Reduction Factor

For the selected buckling curve:

### Curve c

```text
αLT = 0.49
```

### Curve d

```text
αLT = 0.76
```

The program calculates:

```text
φLT =
0.5 [1 + αLT(λLT - 0.2) + λLT²]
```

and:

```text
χLT =
1 / [φLT + √(φLT² - λLT²)]
```

The reduction factor is limited to:

```text
χLT ≤ 1.0
```

---

# 💪 Design Bending Stress

The design bending compressive stress is:

```text
fbd = χLT × fy / γm0
```

This value is subsequently used to determine the design flexural resistance.

---

# 🏆 Design Flexural Capacity

For non-slender sections:

```text
Md = βb × Zp × fbd
```

For slender sections:

```text
Md = Ze,eff × fbd
```

The final result is reported as:

```text
Md = kN·m
```

---

# 🔍 LTB vs. No-LTB Capacity

One useful feature of the program is that it reports both:

### With LTB

```text
Md (LTB)
```

### Without LTB

```text
Md_no_ltb
```

This makes it easy to understand the reduction in bending capacity caused by lateral torsional buckling.

```text
              Flexural Capacity
                     │
        ┌────────────┴────────────┐
        │                         │
   No LTB Capacity           LTB Capacity
        │                         │
        │                    χLT reduction
        │                         │
        └────────────┬────────────┘
                     ▼
              Design Capacity
```

---

# 🖥️ Program Usage

Run the Python script:

```bash
python ltb_design.py
```

The program will interactively request the section dimensions and design parameters.

Example:

```text
Top flange width      = 700 mm
Top flange thickness  = 32 mm

Bottom flange width   = 1000 mm
Bottom flange thickness = 45 mm

Web depth             = 1523 mm
Web thickness         = 20 mm

Unbraced length       = 8.925 m

Yield stress fy       = 390 MPa

Section classification = Auto
LTB curve             = d
γm0                   = 1.10
```

---

# 📋 Example Output

The program generates a detailed calculation report containing:

```text
SECTION CLASSIFICATION
────────────────────────────────────

Top Flange
b/t = ...
Plastic limit = ...
Compact limit = ...
Semi-compact limit = ...
Classification = ...

Web
d/t = ...
Plastic limit = ...
Compact limit = ...
Semi-compact limit = ...
Classification = ...
```

Followed by:

```text
SECTION PROPERTIES
────────────────────────────────────

Gross Area
Centroid
Iz
Iy
ry
Ze
Zp
βb
```

and:

```text
LATERAL TORSIONAL BUCKLING
────────────────────────────────────

Mcr
λLT
φLT
χLT
fbd
Md
Md_no_ltb
```

---

# ⚙️ User Controls

The program supports:

### Section Classification

```text
1. Auto-classify
2. Plastic
3. Compact
4. Semi-compact
5. Slender
```

### LTB Buckling Curve

```text
c → αLT = 0.49

d → αLT = 0.76
```

### Partial Safety Factor

Default:

```text
γm0 = 1.10
```

---

# 📁 Suggested Repository Structure

```text
ltb-design-welded-i-section/
│
├── 📄 ltb_design.py
├── 📄 README.md
├── 📄 LICENSE
├── 📄 requirements.txt
│
├── 📁 examples/
│   └── example_calculation.txt
│
└── 📁 docs/
    └── calculation-methodology.md
```

The current script uses Python's built-in `math` module, so **no external Python packages are required**.

---

# 🚀 Future Development

Possible future enhancements include:

* [ ] Graphical user interface
* [ ] Interactive I-section geometry
* [ ] Section property visualization
* [ ] LTB moment vs. unbraced-length graph
* [ ] `λLT` vs. `χLT` interaction graph
* [ ] Automatic buckling curve selection
* [ ] Multiple steel grades
* [ ] Rolled I-section support
* [ ] Tapered girder support
* [ ] Doubly symmetric and asymmetric sections
* [ ] Shear capacity check
* [ ] Web buckling check
* [ ] Web crippling check
* [ ] Combined shear and bending
* [ ] PDF calculation report
* [ ] Excel calculation sheet
* [ ] Unit conversion
* [ ] Design summary dashboard

---

# ⚠️ Engineering Disclaimer

This software is intended as a **calculation and engineering-assistance tool**.

The output should be independently verified by a qualified structural engineer before being used for construction, tender, statutory approval, or final design documentation.

The user is responsible for confirming:

* Applicable code edition
* Clause and table requirements
* Section classification limits
* Boundary conditions
* Loading assumptions
* Lateral restraint conditions
* Buckling curve selection
* Material properties
* Partial safety factors
* Effective width assumptions
* Design applicability to the specific structural system

> **This tool does not replace engineering judgement or independent design verification.**

---

# 🛠️ Technology

```text
Python 3.x
│
├── math
│   ├── sqrt()
│   └── pi
│
└── Custom engineering functions
    ├── Section Classification
    ├── Effective Width
    ├── Effective Web Depth
    ├── Section Properties
    ├── LTB Capacity
    └── Detailed Reporting
```

---

# 👨‍💻 Author

**Arvind Singh Rawat**
Bridge Design Engineer | Structural Engineer

📧 `arvindrawat400@gmail.com`

🔗 [LinkedIn Profile](https://www.linkedin.com/in/arvindrawat400/?utm_source=chatgpt.com)

---

# ⭐ Support the Project

If you find this tool useful for steel and bridge design:

⭐ **Star the repository**
🐛 **Report issues**
💡 **Suggest improvements**
🔧 **Contribute to the project**

---

## 📜 License

This project can be distributed under the **MIT License**.

If using the MIT License, add a `LICENSE` file to the root of the repository and include the full license text.

---

<div align="center">

### 🏗️ Built for Structural Engineers

**IRC:24-2010 • IS 800:2007 • Steel Design • LTB**

⭐ Star the repository if you find it useful!

</div>
