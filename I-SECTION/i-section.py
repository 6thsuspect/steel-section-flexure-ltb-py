import math

def classify_section_irc24(bf_top, tf_top, bf_bot, tf_bot, d_web, tw, fy,
                           section_type="welded"):
    """
    Classify steel section as per IRC 24-2010 / IS 800:2007.
    Only the compression flange (top) and web are checked.
    Bottom tension flange is omitted from classification.
    """
    epsilon = math.sqrt(250 / fy)

    # Top flange outstand ratio (compression element)
    if section_type == "welded":
        b_tf_top = (bf_top - tw) / 2 / tf_top
    else:
        b_tf_top = bf_top / 2 / tf_top

    # Web slenderness (internal element in bending)
    d_tw = d_web / tw

    # Limits for outstand compression flange
    if section_type == "welded":
        plastic_limit_flange = 8.4 * epsilon
        compact_limit_flange = 9.4 * epsilon
        semi_compact_limit_flange = 13.6 * epsilon
    else:
        plastic_limit_flange = 9.4 * epsilon
        compact_limit_flange = 10.5 * epsilon
        semi_compact_limit_flange = 15.7 * epsilon

    # Limits for web (bending)
    plastic_limit_web = 84 * epsilon
    compact_limit_web = 105 * epsilon
    semi_compact_limit_web = 126 * epsilon

    # Classify top flange
    if b_tf_top <= plastic_limit_flange:
        top_flange_class = "Plastic"
    elif b_tf_top <= compact_limit_flange:
        top_flange_class = "Compact"
    elif b_tf_top <= semi_compact_limit_flange:
        top_flange_class = "Semi-compact"
    else:
        top_flange_class = "Slender"

    # Classify web
    if d_tw <= plastic_limit_web:
        web_class = "Plastic"
    elif d_tw <= compact_limit_web:
        web_class = "Compact"
    elif d_tw <= semi_compact_limit_web:
        web_class = "Semi-compact"
    else:
        web_class = "Slender"

    # Overall section classification = more critical of top flange and web
    class_rank = {"Plastic": 1, "Compact": 2, "Semi-compact": 3, "Slender": 4}
    overall_class = max(
        [top_flange_class, web_class],
        key=lambda x: class_rank[x]
    )

    # Bottom flange b/t ratio for information only
    if section_type == "welded":
        b_tf_bot = (bf_bot - tw) / 2 / tf_bot
    else:
        b_tf_bot = bf_bot / 2 / tf_bot

    details = {
        "epsilon": epsilon,
        "top_flange_b_tf": b_tf_top,
        "top_flange_class": top_flange_class,
        "top_flange_plastic_limit": plastic_limit_flange,
        "top_flange_compact_limit": compact_limit_flange,
        "top_flange_semi_compact_limit": semi_compact_limit_flange,
        "bottom_flange_b_tf": b_tf_bot,
        "bottom_flange_class": "Not checked (tension)",
        "web_d_tw": d_tw,
        "web_class": web_class,
        "web_plastic_limit": plastic_limit_web,
        "web_compact_limit": compact_limit_web,
        "web_semi_compact_limit": semi_compact_limit_web,
        "top_flange_slender": top_flange_class == "Slender",
        "web_slender": web_class == "Slender",
    }

    return overall_class, details


def effective_width_outstand(b, t, fy, stress_ratio=1.0):
    """
    Calculate effective width of an outstand compression element
    per Eurocode 3 Part 1-5 / IS 800.
    """
    epsilon = math.sqrt(235 / fy)
    lambda_p = (b / t) / (28.4 * epsilon * math.sqrt(stress_ratio))
    if lambda_p <= 0.748:
        rho = 1.0
    else:
        rho = (lambda_p - 0.188) / lambda_p**2
        rho = min(rho, 1.0)
    return rho * b


def effective_depth_web_comp(d_comp, tw, fy, stress_ratio=1.0):
    """
    Calculate effective depth of web in compression for a slender web.
    """
    epsilon = math.sqrt(235 / fy)
    lambda_p = (d_comp / tw) / (28.4 * epsilon * math.sqrt(stress_ratio))
    if lambda_p <= 0.673:
        rho = 1.0
    else:
        rho = (lambda_p - 0.055 * (3 + stress_ratio)) / lambda_p**2
        rho = min(rho, 1.0)
    return rho * d_comp


def calculate_effective_section_properties(
    bf_top, tf_top, bf_bot, tf_bot, d_web, tw, fy, class_details
):
    """
    Calculate effective section properties for slender sections.
    Returns Z_e_eff (effective elastic section modulus at top).
    """
    b_eff_top = bf_top
    b_eff_bot = bf_bot
    d_web_eff = d_web

    # Reduce top flange if slender
    if class_details["top_flange_slender"]:
        outstand = (bf_top - tw) / 2
        eff_outstand = effective_width_outstand(outstand, tf_top, fy)
        b_eff_top = 2 * eff_outstand + tw

    # Determine neutral axis based on gross (or partially effective) section
    A_top = b_eff_top * tf_top
    A_bot = b_eff_bot * tf_bot
    A_web = d_web * tw
    A_total = A_top + A_bot + A_web

    y_bot_flange_centroid = tf_bot / 2
    y_web_centroid = tf_bot + d_web / 2
    y_top_flange_centroid = tf_bot + d_web + tf_top / 2

    y_bar = (
        A_bot * y_bot_flange_centroid +
        A_web * y_web_centroid +
        A_top * y_top_flange_centroid
    ) / A_total

    overall_depth = tf_bot + d_web + tf_top
    d_comp = overall_depth - y_bar - tf_top

    # Reduce web if slender
    if class_details["web_slender"]:
        d_comp_eff = effective_depth_web_comp(d_comp, tw, fy)
        d_tension = d_web - d_comp
        d_web_eff = d_comp_eff + d_tension
    else:
        d_web_eff = d_web

    # Recompute properties with effective dimensions
    A_top = b_eff_top * tf_top
    A_bot = b_eff_bot * tf_bot
    A_web = d_web_eff * tw
    A_total = A_top + A_bot + A_web

    y_bot_flange_centroid = tf_bot / 2
    y_web_centroid = tf_bot + d_web_eff / 2
    y_top_flange_centroid = tf_bot + d_web_eff + tf_top / 2

    y_bar_eff = (
        A_bot * y_bot_flange_centroid +
        A_web * y_web_centroid +
        A_top * y_top_flange_centroid
    ) / A_total

    overall_depth_eff = tf_bot + d_web_eff + tf_top
    y_top_extreme = overall_depth_eff - y_bar_eff

    I_bot = (b_eff_bot * tf_bot**3 / 12) + A_bot * (
        y_bar_eff - y_bot_flange_centroid
    )**2
    I_web = (tw * d_web_eff**3 / 12) + A_web * (
        y_bar_eff - y_web_centroid
    )**2
    I_top = (b_eff_top * tf_top**3 / 12) + A_top * (
        y_bar_eff - y_top_flange_centroid
    )**2
    I_z_eff = I_bot + I_web + I_top

    Z_e_eff = I_z_eff / y_top_extreme

    return Z_e_eff, {
        "b_eff_top": b_eff_top,
        "b_eff_bot": b_eff_bot,
        "d_web_eff": d_web_eff,
        "I_z_eff": I_z_eff,
        "y_bar_eff": y_bar_eff,
        "A_eff": A_total,
    }


def ltb_moment_capacity_welded(
    bf_top, tf_top, bf_bot, tf_bot, d_web, tw, L_lt, fy,
    section_class=None, curve="d", gamma_m0=1.10
):
    """
    Calculates design flexural moment capacity of a welded I-section
    considering Lateral Torsional Buckling as per IS 800:2007 / IRC:24.
    Handles Plastic, Compact, Semi-compact, and Slender sections.
    If λ_LT ≤ 0.4, LTB does not govern and full section capacity is used.
    Also computes the capacity ignoring LTB (laterally supported).
    """
    E = 2e5

    # ---------------- Gross section properties ----------------
    A_top = bf_top * tf_top
    A_bot = bf_bot * tf_bot
    A_web = d_web * tw
    A_total = A_top + A_bot + A_web

    y_bot_flange_centroid = tf_bot / 2
    y_web_centroid = tf_bot + d_web / 2
    y_top_flange_centroid = tf_bot + d_web + tf_top / 2

    y_bar = (
        A_bot * y_bot_flange_centroid +
        A_web * y_web_centroid +
        A_top * y_top_flange_centroid
    ) / A_total

    overall_depth = tf_bot + d_web + tf_top
    y_top_extreme = overall_depth - y_bar

    I_bot = (bf_bot * tf_bot**3 / 12) + A_bot * (
        y_bar - y_bot_flange_centroid
    )**2
    I_web = (tw * d_web**3 / 12) + A_web * (
        y_bar - y_web_centroid
    )**2
    I_top = (bf_top * tf_top**3 / 12) + A_top * (
        y_bar - y_top_flange_centroid
    )**2
    I_z_gross = I_bot + I_web + I_top

    I_y_gross = (
        (tf_top * bf_top**3 / 12) +
        (tf_bot * bf_bot**3 / 12) +
        (d_web * tw**3 / 12)
    )
    r_y = math.sqrt(I_y_gross / A_total)

    Z_e_gross = I_z_gross / y_top_extreme

    # Plastic section modulus (gross)
    half_area = A_total / 2.0
    if A_bot >= half_area:
        y_pna = half_area / bf_bot
        Z_p = 0.0
        Z_p += bf_bot * (y_pna**2) / 2.0
        Z_p += bf_bot * ((tf_bot - y_pna)**2) / 2.0
        Z_p += A_web * (tf_bot - y_pna + d_web / 2)
        Z_p += A_top * (tf_bot - y_pna + d_web + tf_top / 2)
    else:
        remaining = half_area - A_bot
        y_web_comp = remaining / tw
        y_pna = tf_bot + y_web_comp
        Z_p = 0.0
        Z_p += A_bot * (y_pna - y_bot_flange_centroid)
        Z_p += tw * (y_web_comp**2) / 2.0
        y_web_tens_centroid = (
            tf_bot + y_web_comp + (d_web - y_web_comp) / 2
        )
        Z_p += (tw * (d_web - y_web_comp)) * (
            y_web_tens_centroid - y_pna
        )
        Z_p += A_top * (y_top_flange_centroid - y_pna)

    # ---------------- Section classification ----------------
    if section_class is None:
        section_class, class_details = classify_section_irc24(
            bf_top, tf_top, bf_bot, tf_bot, d_web, tw, fy, "welded"
        )
    else:
        _, class_details = classify_section_irc24(
            bf_top, tf_top, bf_bot, tf_bot, d_web, tw, fy, "welded"
        )

    # ---------------- Effective properties for slender sections ----------------
    if section_class.lower() == "slender":
        Z_e_eff, eff_details = calculate_effective_section_properties(
            bf_top, tf_top, bf_bot, tf_bot, d_web, tw, fy, class_details
        )
        Z_used = Z_e_eff
        beta_b = 1.0
    else:
        Z_used = Z_p if section_class.lower() in ["plastic", "compact"] else Z_e_gross
        beta_b = 1.0 if section_class.lower() in ["plastic", "compact"] else Z_e_gross / Z_p
        eff_details = None

    # ---------------- Elastic critical LTB moment (M_cr) ----------------
    h_f = overall_depth - tf_top / 2 - tf_bot / 2
    t_f = tf_top
    term1 = (math.pi**2 * E * I_y_gross * h_f) / (2 * L_lt**2)
    ratio = (L_lt / r_y) / (h_f / t_f)
    factor = math.sqrt(1 + (1 / 20) * ratio**2)
    M_cr = term1 * factor   # N·mm

    # ---------------- Non-dimensional slenderness λ_LT ----------------
    if section_class.lower() == "slender":
        M_eff = Z_e_eff * fy
    else:
        M_eff = beta_b * Z_p * fy if section_class.lower() in ["plastic", "compact"] else Z_e_gross * fy
    lambda_lt = math.sqrt(M_eff / M_cr)

    # ---------------- Reduction factor χ_LT ----------------
    if lambda_lt <= 0.4:
        chi_lt = 1.0
        phi_lt = 0.0
        alpha_lt = None
    else:
        if curve == "c":
            alpha_lt = 0.49
        elif curve == "d":
            alpha_lt = 0.76
        else:
            raise ValueError("curve must be 'c' or 'd'")
        phi_lt = 0.5 * (1 + alpha_lt * (lambda_lt - 0.2) + lambda_lt**2)
        chi_lt = 1.0 / (phi_lt + math.sqrt(phi_lt**2 - lambda_lt**2))
        chi_lt = min(chi_lt, 1.0)

    # ---------------- Design bending stress and moment (LTB) ----------------
    f_bd = chi_lt * fy / gamma_m0

    if section_class.lower() == "slender":
        M_d = Z_e_eff * f_bd
    else:
        M_d = beta_b * Z_p * f_bd

    M_d_kNm = M_d / 1e6

    # ---------------- Flexure capacity ignoring LTB (laterally supported) ----------------
    if section_class.lower() == "slender":
        M_d_no_ltb = Z_e_eff * fy / gamma_m0
    else:
        M_d_no_ltb = beta_b * Z_p * fy / gamma_m0

    M_d_no_ltb_kNm = M_d_no_ltb / 1e6

    # Store all relevant intermediate values for detailed printing
    details = {
        "A_total": A_total,
        "y_bar": y_bar,
        "I_z_gross": I_z_gross,
        "I_y_gross": I_y_gross,
        "r_y": r_y,
        "Z_e_gross": Z_e_gross,
        "Z_p": Z_p,
        "beta_b": beta_b,
        "M_cr_kNm": M_cr / 1e6,
        "lambda_lt": lambda_lt,
        "phi_lt": phi_lt,
        "chi_lt": chi_lt,
        "f_bd": f_bd,
        "M_d_Nmm": M_d,
        "M_d_kNm": M_d_kNm,
        "M_d_no_ltb_kNm": M_d_no_ltb_kNm,
        "section_class": section_class,
        "class_details": class_details,
        "effective_details": eff_details,
        "Z_used": Z_used,
        "ltb_governs": lambda_lt > 0.4,
        "E": E,
        "h_f": h_f,
        "t_f": t_f,
        "L_lt": L_lt,
        "I_y_gross": I_y_gross,
        "term1": term1,
        "ratio": ratio,
        "factor": factor,
        "M_eff": M_eff,
        "fy": fy,
        "gamma_m0": gamma_m0,
        "alpha_lt": alpha_lt,
        "curve": curve,
    }
    return M_d_kNm, details


def print_detailed_ltb_calculations(res):
    """Print step-by-step calculations for LTB parameters."""
    print("\n" + "=" * 70)
    print("DETAILED LTB CALCULATIONS")
    print("=" * 70)

    # 1. M_cr calculation
    print("\n1. Elastic Critical Lateral Torsional Buckling Moment (M_cr)")
    print("   Formula (IS 800 Annex E simplified):")
    print("   M_cr = (π² E I_y h_f) / (2 L_lt²) * sqrt(1 + (1/20) * ((L_lt/r_y)/(h_f/t_f))²)")
    print("   Where:")
    print(f"      E = {res['E']:.0f} N/mm²")
    print(f"      I_y (minor axis) = {res['I_y_gross']:.2e} mm⁴")
    print(f"      h_f = c/c distance between flanges = {res['h_f']:.2f} mm")
    print(f"      L_lt = {res['L_lt']:.0f} mm")
    print(f"      r_y = {res['r_y']:.2f} mm")
    print(f"      t_f (compression flange thickness) = {res['t_f']:.0f} mm")
    print(f"   Step 1: term1 = (π² * E * I_y * h_f) / (2 * L_lt²)")
    print(f"           = (π² * {res['E']:.0f} * {res['I_y_gross']:.2e} * {res['h_f']:.2f}) / (2 * {res['L_lt']}²)")
    print(f"           = {res['term1']:.2f} N·mm")
    print(f"   Step 2: ratio = (L_lt/r_y) / (h_f/t_f) = ({res['L_lt']:.0f}/{res['r_y']:.2f}) / ({res['h_f']:.2f}/{res['t_f']:.0f}) = {res['ratio']:.4f}")
    print(f"   Step 3: factor = sqrt(1 + (1/20) * ratio²) = sqrt(1 + 0.05 * {res['ratio']:.4f}²) = {res['factor']:.4f}")
    print(f"   M_cr = {res['term1']:.2f} * {res['factor']:.4f} = {res['M_cr_kNm']*1e6:.2f} N·mm = {res['M_cr_kNm']:.2f} kN·m")

    # 2. λ_LT calculation
    print("\n2. Non-dimensional Slenderness Ratio (λ_LT)")
    print("   Formula: λ_LT = sqrt(M_eff / M_cr)")
    print(f"      M_eff = Z_used * fy = {res['Z_used']:.2e} mm³ * {res['fy']:.0f} MPa = {res['M_eff']:.2f} N·mm")
    print(f"      M_cr = {res['M_cr_kNm']*1e6:.2f} N·mm")
    print(f"   λ_LT = sqrt({res['M_eff']:.2f} / {res['M_cr_kNm']*1e6:.2f}) = {res['lambda_lt']:.4f}")

    # 3. φ_LT and χ_LT
    print("\n3. Reduction Factor (χ_LT)")
    if res['lambda_lt'] <= 0.4:
        print("   Since λ_LT ≤ 0.4, LTB does not govern.")
        print("   Therefore, χ_LT = 1.0 and φ_LT is not required.")
    else:
        print(f"   Buckling curve: {res['curve']} (α_LT = {res['alpha_lt']:.2f})")
        print("   Formula: φ_LT = 0.5 * [1 + α_LT (λ_LT - 0.2) + λ_LT²]")
        print(f"           = 0.5 * [1 + {res['alpha_lt']:.2f} * ({res['lambda_lt']:.4f} - 0.2) + {res['lambda_lt']:.4f}²]")
        print(f"           = {res['phi_lt']:.4f}")
        print("   Formula: χ_LT = 1 / (φ_LT + sqrt(φ_LT² - λ_LT²))")
        print(f"           = 1 / ({res['phi_lt']:.4f} + sqrt({res['phi_lt']:.4f}² - {res['lambda_lt']:.4f}²))")
        print(f"           = {res['chi_lt']:.4f}")

    # 4. f_bd
    print("\n4. Design Bending Compressive Stress (f_bd)")
    print("   Formula: f_bd = χ_LT * fy / γ_m0")
    print(f"           = {res['chi_lt']:.4f} * {res['fy']:.0f} / {res['gamma_m0']:.2f}")
    print(f"           = {res['f_bd']:.2f} MPa")

    # 5. M_d (LTB)
    print("\n5. Design Flexural Moment Capacity with LTB (M_d)")
    if res['section_class'].lower() == "slender":
        print("   For slender section, M_d = Z_e_eff * f_bd")
        print(f"   Z_e_eff = {res['Z_used']:.2e} mm³")
    else:
        print(f"   For {res['section_class']} section, M_d = β_b * Z_p * f_bd")
        print(f"   β_b = {res['beta_b']:.4f}, Z_p = {res['Z_p']:.2e} mm³")
    print(f"   M_d = {res['M_d_Nmm']:.2f} N·mm = {res['M_d_kNm']:.2f} kN·m")

    # 6. M_d_no_ltb (flexure capacity ignoring LTB)
    print("\n6. Flexure Capacity Irrespective of LTB (M_d_no_ltb)")
    if res['section_class'].lower() == "slender":
        print("   For slender section, M_d_no_ltb = Z_e_eff * fy / γ_m0")
        print(f"   Z_e_eff = {res['Z_used']:.2e} mm³")
    else:
        print(f"   For {res['section_class']} section, M_d_no_ltb = β_b * Z_p * fy / γ_m0")
        print(f"   β_b = {res['beta_b']:.4f}, Z_p = {res['Z_p']:.2e} mm³")
    print(f"   M_d_no_ltb = {res['M_d_no_ltb_kNm']:.2f} kN·m")
    print("=" * 70)


def print_summary(res):
    """Print a concise summary of the key results."""
    print("\n" + "=" * 70)
    print("SUMMARY OF RESULTS")
    print("=" * 70)
    print(f"M_cr         = {res['M_cr_kNm']:.2f} kN·m")
    print(f"λ_LT         = {res['lambda_lt']:.4f}")
    print(f"φ_LT         = {res['phi_lt']:.4f}")
    print(f"χ_LT         = {res['chi_lt']:.4f}")
    print(f"f_bd         = {res['f_bd']:.2f} MPa")
    print(f"M_d (LTB)    = {res['M_d_kNm']:.2f} kN·m")
    print(f"M_d_no_ltb   = {res['M_d_no_ltb_kNm']:.2f} kN·m")
    print("=" * 70)


# ---------------- User Input Helpers ----------------
def get_float_input(prompt, default=None):
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if user_input == "":
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()
            return float(user_input)
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_curve_input():
    while True:
        print("\nSelect LTB buckling curve (for welded sections):")
        print("c. Curve 'c' (α_LT = 0.49) - for h/b ≤ 2")
        print("d. Curve 'd' (α_LT = 0.76) - for h/b > 2")
        choice = input("Enter choice (c/d) [d]: ").strip().lower()
        if choice == "":
            return "d"
        elif choice == "c":
            return "c"
        elif choice == "d":
            return "d"
        else:
            print("Invalid choice! Please enter 'c' or 'd'.")


def get_section_class_input():
    while True:
        print("\nSection classification options:")
        print("1. Auto-classify (as per IRC 24-2010)")
        print("2. Plastic")
        print("3. Compact")
        print("4. Semi-compact")
        print("5. Slender (force slender)")
        choice = input("Enter choice (1/2/3/4/5) [1]: ").strip()
        if choice == "" or choice == "1":
            return None
        elif choice == "2":
            return "plastic"
        elif choice == "3":
            return "compact"
        elif choice == "4":
            return "semi-compact"
        elif choice == "5":
            return "slender"
        else:
            print("Invalid choice! Please enter 1-5.")


def print_section_classification(class_details):
    if class_details is None:
        return
    print("\n" + "-" * 70)
    print("SECTION CLASSIFICATION DETAILS (as per IRC 24-2010)")
    print("-" * 70)
    eps = class_details['epsilon']
    print(f"ε = √(250/fy) = {eps:.4f}")

    print("\n--- Top Flange (Compression) ---")
    print(f"b/t = {class_details['top_flange_b_tf']:.2f}")
    print(f"  Plastic limit: {class_details['top_flange_plastic_limit']:.2f}")
    print(f"  Compact limit: {class_details['top_flange_compact_limit']:.2f}")
    print(
        f"  Semi-compact limit: "
        f"{class_details['top_flange_semi_compact_limit']:.2f}"
    )
    print(f"  Classification: {class_details['top_flange_class']}")

    print("\n--- Web ---")
    print(f"d/t = {class_details['web_d_tw']:.2f}")
    print(f"  Plastic limit: {class_details['web_plastic_limit']:.2f}")
    print(f"  Compact limit: {class_details['web_compact_limit']:.2f}")
    print(
        f"  Semi-compact limit: "
        f"{class_details['web_semi_compact_limit']:.2f}"
    )
    print(f"  Classification: {class_details['web_class']}")

    print("\n--- Bottom Flange (Tension) ---")
    print(f"b/t = {class_details['bottom_flange_b_tf']:.2f}")
    print(f"  Classification: {class_details['bottom_flange_class']}")


# ---------------- Main Program ----------------
if __name__ == "__main__":
    print("=" * 70)
    print("LATERAL TORSIONAL BUCKLING DESIGN OF WELDED I-SECTION")
    print("AS PER IRC:24-2010 / IS 800:2007")
    print("=" * 70)

    print("\n--- Enter Section Dimensions ---")
    print("(All dimensions in mm)")

    bf_top = get_float_input("\nTop flange width (bf_top)", default=700)
    tf_top = get_float_input("Top flange thickness (tf_top)", default=32)
    bf_bot = get_float_input("Bottom flange width (bf_bot)", default=1000)
    tf_bot = get_float_input("Bottom flange thickness (tf_bot)", default=45)
    d_web = get_float_input("Web depth (d_web)", default=1523)
    tw = get_float_input("Web thickness (tw)", default=20)

    print("\n--- Enter Loading and Material Properties ---")

    L_lt_input = input("\nUnbraced length L_lt in m [8.925]: ").strip()
    if L_lt_input == "":
        L_lt = 8925
    else:
        try:
            L_lt = float(L_lt_input) * 1000
        except ValueError:
            print("Invalid input! Using default value 8.925 m")
            L_lt = 8925

    fy = get_float_input("\nYield stress fy in MPa", default=390)

    section_class = get_section_class_input()
    curve = get_curve_input()
    gamma_m0 = get_float_input("\nPartial safety factor γ_m0", default=1.10)

    print("\n" + "=" * 70)
    print("CALCULATING...")
    print("=" * 70)

    Md, res = ltb_moment_capacity_welded(
        bf_top, tf_top,
        bf_bot, tf_bot,
        d_web, tw,
        L_lt,
        fy,
        section_class,
        curve,
        gamma_m0
    )

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\nSection: Top flange {bf_top:.0f}×{tf_top:.0f} mm")
    print(f"         Bottom flange {bf_bot:.0f}×{tf_bot:.0f} mm")
    print(f"         Web {d_web:.0f}×{tw:.0f} mm")
    print(f"L_lt = {L_lt:.0f} mm ({L_lt/1000:.3f} m)")
    print(f"fy = {fy:.0f} MPa")
    print(f"Section class = {res['section_class']}")
    print(f"LTB curve = {curve}")
    print(f"γ_m0 = {gamma_m0:.2f}")

    if res['class_details']:
        print_section_classification(res['class_details'])

    print("\n--- Section Properties ---")
    print(f"Gross area A = {res['A_total']:.0f} mm²")
    print(f"Gross centroid y_bar = {res['y_bar']:.2f} mm from bottom")
    print(f"Gross I_z = {res['I_z_gross']:.2e} mm⁴")
    print(f"Gross I_y = {res['I_y_gross']:.2e} mm⁴")
    print(f"Gross r_y = {res['r_y']:.2f} mm")
    print(f"Gross elastic modulus Z_e = {res['Z_e_gross']:.2e} mm³")
    print(f"Plastic modulus Z_p = {res['Z_p']:.2e} mm³")

    if res['section_class'].lower() == "slender" and res['effective_details']:
        eff = res['effective_details']
        print("\n--- Effective Section Properties (Slender) ---")
        print(f"Effective top flange width = {eff['b_eff_top']:.1f} mm")
        print(f"Effective bottom flange width = {eff['b_eff_bot']:.1f} mm")
        print(f"Effective web depth = {eff['d_web_eff']:.1f} mm")
        print(f"Effective area = {eff['A_eff']:.0f} mm²")
        print(f"Effective I_z = {eff['I_z_eff']:.2e} mm⁴")
        print(f"Effective centroid = {eff['y_bar_eff']:.2f} mm from bottom")
        print(f"Effective elastic modulus Z_e_eff = {res['Z_used']:.2e} mm³")

    print(f"\nβ_b = {res['beta_b']:.4f}")

    # Print detailed LTB calculations
    print_detailed_ltb_calculations(res)

    # Print summary of results
    print_summary(res)

    print("\n" + "=" * 70)

    if res['ltb_governs']:
        print("\nNOTE: λ_LT > 0.4, Lateral Torsional Buckling governs the design.")
    else:
        print("\nNOTE: λ_LT ≤ 0.4, Lateral Torsional Buckling does NOT govern.")
        print("The beam is laterally supported; full section capacity is used.")
    print("=" * 70)
