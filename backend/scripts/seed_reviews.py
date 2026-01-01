"""
Review seeding script
Populates database with realistic tenant reviews for Lagos properties
"""
import sys
from pathlib import Path
import random
from decimal import Decimal

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Property, Review

# Area-specific review templates (based on real Lagos characteristics)
AREA_SPECIFIC_REVIEWS = {
    "Lekki": {
        "power": {
            "positive": ["Estate has 24/7 power with backup generator. No power issues at all.",
                        "Very stable electricity supply in this gated estate. Rarely have outages."],
            "negative": ["Power can be unstable outside the estates. Generator is necessary.",
                        "NEPA supply is inconsistent, but estate generator covers the gap."],
        },
        "water": {
            "positive": ["Borehole water is constant. No water scarcity issues.",
                        "Estate has good water management. Supply is very reliable."],
            "negative": ["Water pressure can be low sometimes. Need to store water.",
                        "Borehole maintenance is expensive, adds to service charge."],
        },
        "unique": {
            "positive": ["Peaceful environment, great for families. Close to beach and recreational spots.",
                        "Good security with gated estates and CCTV everywhere.",
                        "Love the serene atmosphere and proximity to nice restaurants and malls."],
            "negative": ["Flooding during heavy rain, especially on Orchid Road and low-lying areas.",
                        "Traffic on Lekki-Epe expressway is terrible during rush hour. Can take 2 hours to get to VI.",
                        "Very expensive rent and service charges. You pay premium for everything.",
                        "Too far from mainland. If you work on the island, commute is stressful."],
        },
    },

    "Ajah": {
        "power": {
            "positive": ["Power supply is improving. We get about 12-15 hours daily now."],
            "negative": ["Inconsistent power supply. Generator is a must-have here.",
                        "NEPA light is poor. Only get 6-8 hours on good days."],
        },
        "unique": {
            "positive": ["More affordable than Lekki while still on the peninsula.",
                        "Area is developing fast with new facilities coming up.",
                        "Good road network improving accessibility."],
            "negative": ["SEVERE flooding during rainy season! Abraham Adesanya area gets waterlogged.",
                        "Flooding is a nightmare here. Roads become rivers when it rains heavily.",
                        "Very far from the island. Commute can take 2-3 hours in traffic.",
                        "Limited public transport. You really need a car here.",
                        "Still developing, so some areas lack basic infrastructure."],
        },
    },

    "Victoria Island": {
        "power": {
            "positive": ["Excellent power supply in most estates. 20+ hours daily with generator backup.",
                        "Power is very reliable here. One of the best in Lagos."],
            "negative": ["Despite good infrastructure, some parts still experience outages."],
        },
        "unique": {
            "positive": ["Premium infrastructure and facilities. Everything works well.",
                        "Excellent security. Very safe neighborhood.",
                        "Cosmopolitan area with international schools and businesses.",
                        "Close to business districts. Short commute if you work on the island."],
            "negative": ["Traffic is TERRIBLE! Bar Beach and Ozumba Mbadiwe are always jammed.",
                        "Extremely expensive. Rent is astronomical compared to mainland.",
                        "Parking is a major problem. Very limited space.",
                        "Flooding in some low-lying areas during heavy rain.",
                        "Too expensive for what you get. Service charges are outrageous."],
        },
    },

    "Ikeja": {
        "power": {
            "positive": ["Reliable power supply. We get 18-20 hours daily.",
                        "Power is very stable in Ikeja GRA. Good infrastructure."],
            "negative": ["Power can be unstable in older parts of Ikeja.",
                        "Outside GRA, power supply is less reliable."],
        },
        "unique": {
            "positive": ["Excellent transport links. Easy to get anywhere in Lagos.",
                        "Central location with good road network and accessibility.",
                        "Moderate rent compared to island areas. Good value.",
                        "Plenty of commercial activities and facilities nearby."],
            "negative": ["Traffic congestion everywhere, especially Allen Avenue and Obafemi Awolowo.",
                        "Airport noise if you live in GRA or nearby. Can be disturbing.",
                        "Very busy and commercial. Not peaceful if you want quiet.",
                        "Air pollution from heavy traffic and commercial activities."],
        },
    },

    "Yaba": {
        "power": {
            "positive": ["Power supply is decent. We get about 16-18 hours daily.",
                        "Electricity is fairly stable in most parts of Yaba."],
            "negative": ["Power can be erratic in some streets. Generator backup needed."],
        },
        "unique": {
            "positive": ["Very affordable rent. Budget-friendly for young professionals and students.",
                        "Great transport links. Easy access to mainland and island.",
                        "Central location. Everything is accessible.",
                        "Vibrant nightlife and entertainment. Lots of spots to hang out.",
                        "Tech hub with co-working spaces. Good for tech people."],
            "negative": ["Very noisy area! Parties, events, and street noise daily.",
                        "Loud music and generator noise, especially on weekends.",
                        "Traffic can be heavy, especially on Herbert Macaulay and Jibowu.",
                        "Densely populated. Can feel crowded and chaotic.",
                        "Some parts can be rough. Security varies by street."],
        },
    },

    "Surulere": {
        "power": {
            "positive": ["Power supply is okay. Around 14-16 hours daily.",
                        "Electricity fairly stable in established areas."],
            "negative": ["Power can be inconsistent. Old infrastructure affects supply.",
                        "NEPA supply varies. Some days good, some days terrible."],
        },
        "unique": {
            "positive": ["Affordable rent for an established area.",
                        "Excellent public transport. Buses and taxis everywhere.",
                        "Central location with good accessibility to both mainland and island.",
                        "Established neighborhood with all necessary facilities."],
            "negative": ["Older infrastructure. Buildings and roads need maintenance.",
                        "Traffic on Bode Thomas, Adeniran Ogunsanya is heavy during rush hour.",
                        "Flooding in low-lying areas like Iponri during heavy rain.",
                        "Can be noisy in commercial areas near Stadium.",
                        "Mixed neighborhood. Some streets are better than others."],
        },
    },

    "Ikoyi": {
        "power": {
            "positive": ["24/7 power supply with excellent backup systems. No issues at all.",
                        "Best power infrastructure in Lagos. Never had an outage."],
            "negative": [],  # Premium area, very few complaints
        },
        "unique": {
            "positive": ["Ultra-premium area with top-notch infrastructure.",
                        "Extremely secure and safe. Best security in Lagos.",
                        "Very quiet and peaceful. Green spaces and parks.",
                        "Diplomatic zone with embassies. Well-maintained roads.",
                        "Excellent schools and facilities for families."],
            "negative": ["Rent is ASTRONOMICALLY expensive. Most expensive in Lagos.",
                        "Limited public transport. Very exclusive area.",
                        "Too quiet if you like vibrant nightlife.",
                        "Service charges are extremely high.",
                        "Not accessible for middle-class. Reserved for the very wealthy."],
        },
    },

    "Gbagada": {
        "power": {
            "positive": ["Power supply is fairly good. About 15-17 hours daily.",
                        "Electricity stable in most estates."],
            "negative": ["Power can be unstable in older parts.",
                        "Some areas have poor power infrastructure."],
        },
        "unique": {
            "positive": ["Moderate rent. Not as expensive as island areas.",
                        "Strategic location between mainland and island.",
                        "Decent neighborhood with good mix of residential and commercial.",
                        "Accessible to both Third Mainland Bridge and mainland."],
            "negative": ["Traffic on Third Mainland Bridge approach is terrible during rush hour.",
                        "Flooding in low-lying areas during heavy rain, especially around Gbagada-Oworonshoki.",
                        "Mixed infrastructure. Some areas well-developed, others not.",
                        "Can be noisy near major roads like Gbagada Expressway."],
        },
    },

    "Maryland": {
        "power": {
            "positive": ["Power supply is decent. Around 15-17 hours daily.",
                        "Electricity fairly stable in residential areas."],
            "negative": ["Power less reliable in commercial areas.",
                        "Older infrastructure affects power stability."],
        },
        "unique": {
            "positive": ["Major transport hub. Easy to get anywhere.",
                        "Good commercial facilities and shopping.",
                        "Moderate rent. More affordable than island.",
                        "Accessible location with good road network."],
            "negative": ["Heavy traffic congestion at Maryland bus stop and Ikorodu Road junction.",
                        "Very busy and commercial. Can be chaotic and noisy.",
                        "Commercial area pollution and noise from buses.",
                        "Limited parking space in commercial areas."],
        },
    },

    "Festac": {
        "power": {
            "positive": ["Power supply is okay in well-managed estates. About 14-16 hours.",
                        "Some estates have good backup generators."],
            "negative": ["Inconsistent power supply. NEPA is unreliable here.",
                        "Old infrastructure affects electricity stability.",
                        "Generator use is common. Adds to living costs."],
        },
        "water": {
            "positive": ["Borehole water available in most estates.",
                        "Water supply is manageable if estate has good infrastructure."],
            "negative": ["Water scarcity in some areas. Runs only 2-3 times weekly.",
                        "Old pipes mean water quality can be poor."],
        },
        "unique": {
            "positive": ["Affordable rent for an estate area.",
                        "Good layout and planning. Well-organized streets.",
                        "Decent security in gated estates.",
                        "Established area with schools and facilities."],
            "negative": ["Old infrastructure from 1977. Buildings and roads need renovation.",
                        "Traffic on Festac Link Bridge during rush hour is terrible.",
                        "Very far from the island. Commute can take 2+ hours.",
                        "Limited modern facilities. Area feels dated.",
                        "Transport can be challenging. Not many buses go deep into Festac."],
        },
    },
}

# Generic templates (fallback for areas not in AREA_SPECIFIC_REVIEWS)
REVIEW_TEMPLATES = {
    "power": {
        "positive": [
            "Power supply is quite stable in this area. We get light at least 18-20 hours daily.",
            "Estate has 24/7 power supply with backup generator. No NEPA wahala at all.",
            "Very reliable electricity in this location. Rarely experience outages.",
        ],
        "negative": [
            "Power supply is terrible. Sometimes we only get 4-5 hours of light per day.",
            "Constant power outage is a major issue here. You'll spend a lot on fuel for generator.",
            "NEPA light is very poor. Be prepared to use generator almost daily.",
        ],
    },
    "water": {
        "positive": [
            "Water supply is consistent. Borehole water runs regularly.",
            "No water problem at all. Estate provides constant water supply.",
            "Good water supply from both borehole and water company.",
        ],
        "negative": [
            "Water scarcity is a problem. We buy water regularly from vendors.",
            "No constant water supply. You'll need to store water or buy from water tankers.",
            "Water only runs twice a week. Very frustrating experience.",
        ],
    },
    "security": {
        "positive": [
            "The area is very secure with active estate security. I feel safe here.",
            "Security is tight. Gates are manned 24/7 and visitors are properly screened.",
            "Good security measures in place. The neighborhood is peaceful and safe.",
        ],
        "negative": [
            "Security could be better. We've had cases of break-ins in the area.",
            "Not very secure. Ensure you have good burglary proof and locks.",
            "Security is a concern. The area needs more security presence.",
        ],
    },
    "noise": {
        "positive": [
            "Very quiet and serene environment. Perfect for families.",
            "Peaceful area with minimal noise. Good for rest after work.",
            "The neighborhood is calm and quiet. No noise pollution.",
        ],
        "negative": [
            "Too much noise from generators and nearby bars. Can be disturbing.",
            "The area is noisy, especially on weekends. Lots of parties and events.",
            "Noise from the main road can be disturbing, especially at night.",
        ],
    },
    "transport": {
        "positive": [
            "Easy access to public transport. Buses and Keke are readily available.",
            "Great location with good road network. Easy to commute to work.",
            "Transportation is not a problem. The area is well connected.",
        ],
        "negative": [
            "Transportation can be difficult during rush hours. Long wait for buses.",
            "Access road is poor, especially during rainy season. Gets waterlogged.",
            "Far from major roads. You'll need a personal car for convenience.",
        ],
    },
    "landlord": {
        "positive": [
            "Landlord is very responsive and handles repairs promptly.",
            "No issues with the landlord. Very understanding and reasonable.",
            "Good landlord who respects tenants' privacy and maintains the property.",
        ],
        "negative": [
            "Landlord is difficult to deal with. Always looking for reasons to increase rent.",
            "Landlord doesn't respond to maintenance issues. Very frustrating.",
            "Agent and landlord are not cooperative. Too many unnecessary charges.",
        ],
    },
    "value": {
        "positive": [
            "The rent is reasonable for what you get. Good value for money.",
            "Fair price considering the location and facilities available.",
            "Worth every kobo. The property is well-maintained and located in a good area.",
        ],
        "negative": [
            "Rent is too high for the quality of the property and area.",
            "Overpriced in my opinion. You can get better value in other areas.",
            "Too expensive with all the additional charges and poor amenities.",
        ],
    },
}

# General review templates
GENERAL_REVIEWS = [
    {
        "text": "I've lived here for {} {} and overall it's been {}. {pros} {cons}",
        "sentiment": "mixed"
    },
    {
        "text": "This is {} place to live. {pros} However, {cons}",
        "sentiment": "mixed"
    },
    {
        "text": "{pros} I would {} recommend this area to others. {cons}",
        "sentiment": "positive"
    },
]

# Time periods
TIME_PERIODS = [
    ("6 months", 0.5),
    ("1 year", 1),
    ("2 years", 2),
    ("3 years", 3),
]

# Sentiment words
SENTIMENT_WORDS = {
    "positive": ["a great", "an excellent", "a wonderful", "a fantastic", "a lovely"],
    "negative": ["a terrible", "a poor", "a disappointing", "a frustrating", "a bad"],
    "mixed": ["an okay", "a decent", "an average", "a manageable", "a fair"],
}


def generate_review_text(rating, area=None):
    """Generate realistic review text based on rating and area"""
    pros_list = []
    cons_list = []

    # Determine sentiment based on rating
    if rating >= 4:
        sentiment = "positive"
        num_pros = random.randint(3, 5)
        num_cons = random.randint(0, 1)
    elif rating >= 3:
        sentiment = "mixed"
        num_pros = random.randint(2, 3)
        num_cons = random.randint(1, 2)
    else:
        sentiment = "negative"
        num_pros = random.randint(0, 1)
        num_cons = random.randint(3, 5)

    # Use area-specific templates if available, otherwise use generic templates
    if area and area in AREA_SPECIFIC_REVIEWS:
        area_templates = AREA_SPECIFIC_REVIEWS[area]

        # Collect available aspects for this area
        available_aspects = list(area_templates.keys())
        random.shuffle(available_aspects)

        # Add pros (prefer area-specific unique aspects)
        aspects_used = 0
        for aspect in available_aspects:
            if aspects_used >= num_pros:
                break
            if sentiment == "positive" or (sentiment == "mixed" and random.random() > 0.5):
                if "positive" in area_templates[aspect] and area_templates[aspect]["positive"]:
                    pros_list.append(random.choice(area_templates[aspect]["positive"]))
                    aspects_used += 1

        # Add cons (prefer area-specific unique issues)
        aspects_used = 0
        for aspect in available_aspects:
            if aspects_used >= num_cons:
                break
            if "negative" in area_templates[aspect] and area_templates[aspect]["negative"]:
                cons_list.append(random.choice(area_templates[aspect]["negative"]))
                aspects_used += 1

        # Fill remaining with generic if needed
        while len(pros_list) < num_pros:
            aspect = random.choice(list(REVIEW_TEMPLATES.keys()))
            pros_list.append(random.choice(REVIEW_TEMPLATES[aspect]["positive"]))

        while len(cons_list) < num_cons:
            aspect = random.choice(list(REVIEW_TEMPLATES.keys()))
            cons_list.append(random.choice(REVIEW_TEMPLATES[aspect]["negative"]))
    else:
        # Use generic templates
        aspects = list(REVIEW_TEMPLATES.keys())
        random.shuffle(aspects)

        # Add pros
        for aspect in aspects[:num_pros]:
            pros_list.append(random.choice(REVIEW_TEMPLATES[aspect]["positive"]))

        # Add cons
        for aspect in aspects[num_pros:num_pros + num_cons]:
            cons_list.append(random.choice(REVIEW_TEMPLATES[aspect]["negative"]))

    # Construct review
    pros_text = " ".join(pros_list) if pros_list else ""
    cons_text = " ".join(cons_list) if cons_list else ""

    # Full review text
    if sentiment == "positive":
        full_text = f"{pros_text} Overall, I'm very satisfied living here."
    elif sentiment == "negative":
        full_text = f"{cons_text} I wouldn't recommend this area unless you have no other option."
    else:
        full_text = f"{pros_text} On the downside, {cons_text.lower() if cons_text else 'there are minor issues.'}"

    return full_text, pros_text, cons_text


def seed_reviews(db, num_reviews=250):
    """Seed reviews table with Lagos tenant experiences"""
    print(f"\n💬 Seeding {num_reviews} reviews...")

    # Get all properties
    properties = db.query(Property).all()

    if not properties:
        print("❌ No properties found. Please seed properties first!")
        return

    # Area-based rating weights (more realistic distribution)
    AREA_RATING_WEIGHTS = {
        # Premium areas (avg ~3.8-4.0)
        "Lekki": [0.02, 0.05, 0.18, 0.45, 0.30],           # Very good
        "Ikoyi": [0.01, 0.04, 0.15, 0.45, 0.35],           # Excellent
        "Victoria Island": [0.02, 0.06, 0.20, 0.45, 0.27], # Very good

        # Upper-middle areas (avg ~3.5-3.7)
        "Ikeja": [0.03, 0.08, 0.25, 0.42, 0.22],          # Good
        "Surulere": [0.04, 0.10, 0.28, 0.40, 0.18],       # Good
        "Ajah": [0.05, 0.10, 0.25, 0.40, 0.20],           # Good

        # Middle areas (avg ~3.3-3.5)
        "Yaba": [0.05, 0.12, 0.30, 0.38, 0.15],           # Decent
        "Gbagada": [0.06, 0.12, 0.30, 0.37, 0.15],        # Decent
        "Maryland": [0.05, 0.10, 0.32, 0.38, 0.15],       # Decent
        "Festac": [0.04, 0.10, 0.28, 0.40, 0.18],         # Good
    }

    # Default weights for areas not listed (avg ~3.5)
    DEFAULT_WEIGHTS = [0.05, 0.10, 0.25, 0.40, 0.20]

    reviews_created = 0

    for _ in range(num_reviews):
        # 70% of reviews linked to properties, 30% general area reviews
        if random.random() < 0.7 and properties:
            property_obj = random.choice(properties)
            property_id = property_obj.id
            area = property_obj.area
            property_type = property_obj.property_type.value
            rent_paid = property_obj.rent_price
        else:
            property_id = None
            area = random.choice(list(REVIEW_TEMPLATES.keys()))
            property_type = random.choice(["apartment", "house", "duplex", "room"])
            # Generate random rent for general reviews
            rent_paid = Decimal(random.randint(300000, 3000000))

        # Generate rating based on area (more realistic!)
        weights = AREA_RATING_WEIGHTS.get(area, DEFAULT_WEIGHTS)
        rating = random.choices([1, 2, 3, 4, 5], weights=weights)[0]

        # Generate review text with area-specific content
        review_text, pros, cons = generate_review_text(rating, area=area)

        # Create review
        review = Review(
            property_id=property_id,
            area=area,
            rent_paid=rent_paid,
            property_type=property_type,
            review_text=review_text,
            pros=pros if pros else None,
            cons=cons if cons else None,
            rating=rating,
            is_anonymous=True,
        )

        db.add(review)
        reviews_created += 1

        if reviews_created % 50 == 0:
            db.commit()  # Commit in batches
            print(f"  ✓ Created {reviews_created} reviews...")

    db.commit()
    print(f"✅ Successfully created {reviews_created} reviews!")


def main():
    """Main seeding function"""
    print("=" * 50)
    print("🌱 Starting Review Seeding...")
    print("=" * 50)

    db = SessionLocal()

    try:
        # Check if reviews already exist
        existing_count = db.query(Review).count()
        if existing_count > 0:
            response = input(f"\n⚠️  Found {existing_count} existing reviews. Continue anyway? (yes/no): ")
            if response.lower() != "yes":
                print("Seeding cancelled.")
                return

        # Seed reviews
        seed_reviews(db, num_reviews=250)

        print("\n" + "=" * 50)
        print("✅ Review seeding completed successfully!")
        print("=" * 50)

        # Print summary
        total_reviews = db.query(Review).count()
        avg_rating = db.query(Review).filter(Review.rating.isnot(None)).with_entities(Review.rating).all()

        if avg_rating:
            avg = sum(r[0] for r in avg_rating) / len(avg_rating)
            print(f"\n📊 Summary:")
            print(f"  Total Reviews: {total_reviews}")
            print(f"  Average Rating: {avg:.2f}/5.0")
        else:
            print(f"\n📊 Summary:")
            print(f"  Total Reviews: {total_reviews}")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
