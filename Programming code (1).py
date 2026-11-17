# Fordham Vehicle Hire - Quote Calculator
# Date: 13/02/2026
# Created by: Juan Diego Perez Munoz 19260388

# Constants
DAILY_RATES = {
    "S": 22.50,
    "HP": 28.00,
    "V": 35.00,
}

VEHICLE_NAMES = {
    "S": "Saloon",
    "HP": "High Performance",
    "V": "Van",
}

INSURANCE_PREMIUM = 15.50
DEPOSIT = 50.00
LONG_HIRE_DISCOUNT_RATE = 0.10  # 10%
GOLD_HP_PROMO_DISCOUNT = 18.00


# Inputs
def get_vehicle_type():
    while True:
        vehicle_type = input("Enter vehicle type (S = Saloon, HP = High Performance, V = Van): ").strip().upper()     # Repeats until the user enters a valid code found in DAILY_RATES.
        if vehicle_type in DAILY_RATES:                                                                               # strip() removed extra spaces, upper() allows input like "hp" or "Hp".
            return vehicle_type
        print("Invalid vehicle type. Please enter S, HP, or V.")


def get_days_hired(max_days=10):
    while True:
        raw = input(f"Enter number of days hire required (1 to {max_days}): ").strip()            # Converts the user's input to an integer; ValueError catches non-numeric input.
        try:                                                                                      # Range check enforces the assigment rule: 1 to max_days inclusive.
            days = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number (e.g., 3).")                        
            continue

        if 1 <= days <= max_days:
            return days
        print(f"Number of days must be between 1 and {max_days}.")


def get_yes_no(prompt):
    while True:
        answer = input(f"{prompt} (Yes/No): ").strip().lower()                                     # Accept yes.y or no/n in any case; returns a Boolean (True for yes, False for no).
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Invalid response. Please enter Yes or No.")


def get_customer_type():
    while True:
        answer = input("Is the quote for a New or Existing customer?: ").strip().lower()           # Normalises input to lowercase so "New", "NEW", "new" all match.
        if answer in ("new", "existing"):
            return answer
        print("Invalid response. Please enter New or Existing.")


def get_loyalty_type():
    while True:
        loyalty = input("Enter loyalty card type (Bronze/Silver/Gold): ").strip().lower()          # Customer type determines whether we ask for loyalty card details.
        if loyalty in ("bronze", "silver", "gold"):
            return loyalty
        print("Invalid loyalty type. Please enter Bronze, Silver, or Gold.")


# Calculation
def calculate_quote(vehicle_type, days_hired, insurance_required, customer_type, loyalty_type):
    daily_rate = DAILY_RATES[vehicle_type]
    vehicle_name = VEHICLE_NAMES[vehicle_type]

    hire_subtotal = daily_rate * days_hired                                                        # hire_subtotal is the base hire cost before extras/discounts: daily_rate * days_hired.

    # Discounts
    long_hire_discount = 0.0
    if days_hired > 7:                                                                             # Long hire dicsount applies only when days_hired >7 and is a percentage of hire_subtotal.
        long_hire_discount = hire_subtotal * LONG_HIRE_DISCOUNT_RATE

    promo_discount = 0.0
    if loyalty_type == "gold" and vehicle_type == "HP":                                            # Promo discount is a fixed £ amount and pplies only for Gold + HP.
        promo_discount = GOLD_HP_PROMO_DISCOUNT

    # Extras
    insurance_cost = INSURANCE_PREMIUM if insurance_required else 0.0                              # Insurance is a fixed add-on fee if selected.

    # Total
    total_cost = hire_subtotal - long_hire_discount - promo_discount + insurance_cost + DEPOSIT

    return {
        "vehicle_type": vehicle_type,
        "vehicle_name": vehicle_name,
        "days_hired": days_hired,
        "daily_rate": daily_rate,
        "customer_type": customer_type,
        "loyalty_type": loyalty_type,
        "insurance_required": insurance_required,                                                   # Returning a breakdown dictionary makes it easy to display teh summary later.
        "hire_subtotal": hire_subtotal,
        "long_hire_discount": long_hire_discount,
        "promo_discount": promo_discount,
        "insurance_cost": insurance_cost,
        "deposit": DEPOSIT,
        "total_cost": total_cost,
    }


def display_summary(breakdown):
    vehicle_name = str(breakdown["vehicle_name"])
    vehicle_type = str(breakdown["vehicle_type"])
    days_hired = int(breakdown["days_hired"])
    customer_type = str(breakdown["customer_type"])
    loyalty_type = breakdown["loyalty_type"]
    insurance_required = bool(breakdown["insurance_required"])                                       # (str/int/float/bool) ensures correct formatting even if types change.
    daily_rate = float(breakdown["daily_rate"])
    hire_subtotal = float(breakdown["hire_subtotal"])
    long_hire_discount = float(breakdown["long_hire_discount"])
    promo_discount = float(breakdown["promo_discount"])
    insurance_cost = float(breakdown["insurance_cost"])
    deposit = float(breakdown["deposit"])
    total_cost = float(breakdown["total_cost"])

    print("\n" + "=" * 30)
    print("      HIRE QUOTE SUMMARY")
    print("=" * 30)
    print(f"Vehicle Type: {vehicle_name} ({vehicle_type})")
    print(f"Days Hired: {days_hired}")
    print(f"Customer Type: {customer_type.title()}")

    if customer_type == "existing":
        if isinstance(loyalty_type, str) and loyalty_type != "none":                                  # Loyalty card is only relevant for existing customers; new customers show "None".
            print(f"Loyalty Card: {loyalty_type.title()}")
        else:
            print("Loyalty Card: None")

    print(f"Insurance Included: {'Yes' if insurance_required else 'No'}")
    print("-" * 30)
    print(f"Daily Rate: £{daily_rate:.2f}")
    print(f"Subtotal (rate x days): £{hire_subtotal:.2f}")

    # Show discounts applied
    if long_hire_discount > 0:
        print(f"Long Hire Discount (10%): -£{long_hire_discount:.2f}")
    if promo_discount > 0:
        print(f"Gold + HP Promo Discount: -£{promo_discount:.2f}")                                    # Discounts/estras are printed only if they apply, to keep the summary clean.
    if long_hire_discount == 0 and promo_discount == 0:
        print("Discounts Applied: None")

    # Show extras
    if insurance_cost > 0:
        print(f"Insurance Premium: +£{insurance_cost:.2f}")
    print(f"Returnable Deposit: +£{deposit:.2f}")

    print("-" * 30)
    print(f"TOTAL HIRE COST: £{total_cost:.2f}")
    print("=" * 30 + "\n")


def main():  # 
    print("Fordham Vehicle Hire - Quote Calculator\n")

    vehicle_type = get_vehicle_type()
    days_hired = get_days_hired(max_days=10)
    insurance_required = get_yes_no("Is insurance cover required?")                                   # Collects valid user inputs.

    customer_type = get_customer_type()
    loyalty_type = None
    if customer_type == "existing":
        loyalty_type = get_loyalty_type()
    else:
        loyalty_type = "none"

    breakdown = calculate_quote(
        vehicle_type=vehicle_type,
        days_hired=days_hired,
        insurance_required=insurance_required,                                                        # Display itemised summary to the user.
        customer_type=customer_type,
        loyalty_type=loyalty_type,
    )

    display_summary(breakdown)


if __name__ == "__main__":                                                                            # This ensures main() only runs when the file is executed directly
    main()
