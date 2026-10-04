"""
HOOVALE SEO Content Seeder
==========================
Run: python manage.py seed_seo_content

Populates:
- 8 City Landing Pages (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Pune, Ahmedabad, Kolkata)
- 6 Industry Pages (Corporate, Hotels, Schools, Hospitals, Retail, Offices)
- 5 Service Pages (OEM, Bulk, Customization, Promotional, Distributor)
- 20+ FAQs
- 14 Category SEO content
- Site Settings defaults

Each entry has unique 800-1500 word SEO content.

Place this file at: products/management/commands/seed_seo_content.py
You'll also need empty __init__.py files in:
  - products/management/__init__.py
  - products/management/commands/__init__.py
"""
from django.core.management.base import BaseCommand
from products.models import (
    CityPage, IndustryPage, ServicePage, FAQ,
    Category, SiteSettings, Testimonial
)


# ========================================================================
# CITY PAGES DATA (8 cities × ~1500 words each = ~12,000 words SEO content)
# ========================================================================

CITY_DATA = [
    # ==================== DELHI ====================
    {
        "city_name": "Delhi",
        "state": "Delhi NCR",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Delhi — Direct from Jaipur Manufacturer",
        "hero_subheading": "Wholesale wall clocks for Delhi retailers, distributors, corporate buyers and gifting companies. Bulk orders, custom logo printing, fast delivery from our Jaipur factory.",
        "intro_content": (
            "HOOVALE is a leading wall clock supplier in Delhi serving the entire National Capital Region — including Connaught Place, Karol Bagh, Sadar Bazar, Chandni Chowk, Lajpat Nagar, Nehru Place, Gurugram, Noida and Faridabad. "
            "We supply directly from our Jaipur manufacturing facility, which means Delhi buyers get factory-level wholesale pricing without paying multiple middleman margins.\n\n"
            "Whether you run a retail clock store in Sadar Bazar, manage corporate procurement for a multinational in Gurugram, or operate a gifting company in Karol Bagh, we are your one-stop wall clock supply partner. "
            "Our Delhi clientele includes wholesale electronics dealers, gifting agencies, hotel chains, hospital procurement offices, school administration boards, real estate builders gifting flat keys with branded clocks, and event organisers. "
            "From simple round office clocks to luxury designer pieces, we handle Delhi orders ranging from 50 pieces to 50,000 pieces with the same speed and quality."
        ),
        "why_choose_content": (
            "Delhi is one of India's largest wall clock consumption markets, and competition among local suppliers is intense. Most Delhi-based clock dealers are not actual manufacturers — they buy in bulk from factories in Jaipur, Moradabad or imports from China and resell with a 30-50% markup. "
            "Buying directly from HOOVALE eliminates that markup entirely. You also get full customisation control: choose your own dial design, print your company logo, pick frame material (wood, plastic, metal), select the size, and even customise packaging.\n\n"
            "We have served Delhi clients for over a decade. Our advantages include — direct factory pricing (cut out 2-3 middlemen), in-house custom logo printing (no third-party delays), strict quality control on every piece (1 year movement warranty), flexible MOQ starting from just 5 pieces, dedicated Delhi account manager for repeat buyers, and same-day dispatch from Jaipur with 2-3 day delivery to Delhi."
        ),
        "services_content": (
            "Our Delhi wall clock supply services cover every B2B requirement. **Bulk Wholesale Orders** — best wholesale rates for Delhi retailers and distributors with quantity-based slab discounts; **Corporate Gifting Clocks** — branded clocks with company logo, suitable for Diwali gifting, employee anniversaries, and client gifting; **OEM Manufacturing** — produce wall clocks under your own brand name with your packaging and labels; **Custom Logo Printing** — high-quality UV printing of company logos on dial face, available in single colour or full colour; **Promotional Clocks** — economical models for marketing campaigns and trade show giveaways; **Hotel & Hospital Supply** — silent sweep movement clocks suitable for guest rooms and patient wards; **Designer Wall Clocks** — premium wooden, metal and acrylic designs for luxury showrooms and high-end Delhi retail.\n\n"
            "All Delhi orders are processed on priority. We accept bank transfer, UPI, and cheque payments. GST invoice provided for all orders."
        ),
        "delivery_content": (
            "Delhi enjoys our fastest delivery slot. Orders confirmed by 2 PM ship the same day from our Jaipur factory and reach Delhi within 2-3 business days via reliable transporters. "
            "Urgent orders can be expedited to next-day delivery via premium courier at additional cost. We deliver door-to-door across all Delhi NCR pincodes — Connaught Place (110001), Sadar Bazar (110006), Karol Bagh (110005), Lajpat Nagar (110024), Nehru Place (110019), Gurugram (122001-122018), Noida (201301-201310), Faridabad (121001-121010) and all surrounding areas."
        ),
        "industries_content": (
            "Our Delhi customer base spans every major industry. **Corporate Sector** — IT companies in Cyber City, manufacturing units in Okhla and Mayapuri, financial firms in Connaught Place buy our branded office clocks for their offices. **Hospitality** — Delhi hotels including 3-star, 4-star and budget chains use our silent sweep clocks in guest rooms. **Healthcare** — multispecialty hospitals across Delhi NCR procure our hospital wall clocks with non-tick movement for patient wards and OPD areas. **Education** — schools in Delhi, including those affiliated to CBSE and Delhi Government, buy our classroom clocks. **Real Estate Developers** — Delhi NCR builders gift our designer clocks to flat buyers as part of welcome kits. **Retail Stores** — Delhi clock retailers in Sadar Bazar, Bhagirath Place, and Karol Bagh stock our wholesale clocks. **Promotional Companies** — Delhi-based gifting and BTL agencies use our custom logo clocks for client campaigns."
        ),
        "closing_content": (
            "Delhi buyers — direct factory rates, free logo printing on bulk, 2-3 day delivery, GST invoice, dedicated account manager. Send your requirement on WhatsApp or call us for instant pricing."
        ),
        "meta_keywords": "wall clock supplier in delhi, wall clock wholesaler delhi, bulk wall clocks delhi, corporate clock supplier delhi, wall clock manufacturer delhi ncr, wholesale wall clocks delhi",
        "delivery_time": "2-3 business days",
        "nearby_areas": "Connaught Place, Karol Bagh, Sadar Bazar, Chandni Chowk, Lajpat Nagar, Nehru Place, Gurugram, Noida, Faridabad, Ghaziabad",
        "display_order": 1,
    },
    # ==================== MUMBAI ====================
    {
        "city_name": "Mumbai",
        "state": "Maharashtra",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Mumbai — Wholesale Direct from Jaipur",
        "hero_subheading": "Bulk wall clock supply for Mumbai retailers, hotels, corporates, and gifting companies. Custom logo printing, designer clocks, OEM manufacturing — direct factory pricing.",
        "intro_content": (
            "HOOVALE is a trusted wall clock supplier in Mumbai serving the Mumbai Metropolitan Region including South Mumbai, Andheri, Bandra, Thane, Navi Mumbai, Borivali, Goregaon, Powai, BKC, Lower Parel and Worli. "
            "Mumbai is one of our largest customer markets, with regular dispatches to retailers, distributors, gifting companies, hotel chains, real estate builders, and corporate procurement teams across the metro.\n\n"
            "Mumbai businesses buy from us because we eliminate the supply chain middlemen. Most clock dealers in Crawford Market, Lamington Road and Bhuleshwar buy from Jaipur factories like ours and resell with a markup. "
            "When you buy directly from HOOVALE, you save 30-50% on per-unit cost and get full customisation control. Our Mumbai customers range from small jewellery shops gifting clocks to big-ticket buyers, to 5-star hotel chains procuring 500+ clocks for room renovations, to BKC corporates ordering branded clocks for annual gifting."
        ),
        "why_choose_content": (
            "Mumbai is a highly competitive market where buyers expect quality, speed, and sharp pricing. We deliver on all three. "
            "**Quality** — every clock undergoes 3-stage QC at our Jaipur factory before dispatch. Movement is tested for 24 hours, dial print is checked for sharpness, frame is inspected for finish defects. We give 1-year movement warranty. "
            "**Speed** — Mumbai-bound orders ship within 24 hours of confirmation and reach Mumbai in 3-5 business days via reliable transporters like VRL, Gati, and DTDC. "
            "**Pricing** — direct factory rates with bulk slabs starting from MOQ 5. Order 100+ pieces and unlock further wholesale tiers.\n\n"
            "Beyond the basics, Mumbai buyers love our customisation flexibility — single-piece custom orders for testing before bulk commitment, full UV-printed company logos at no extra cost on bulk, multiple frame finishes (matte, glossy, wooden, metallic), and packaging customisation including individual gift boxes for high-value gifting."
        ),
        "services_content": (
            "Mumbai supply services include **Wholesale Bulk Orders** for retailers in Crawford Market, Bhuleshwar and Lamington Road; **Corporate Gifting Clocks** for BKC, Lower Parel and Worli offices for Diwali, anniversaries and client gifting; **Hotel Wall Clocks** with silent sweep movement for Mumbai's hospitality chains; **Hospital Wall Clocks** with non-tick mechanism for patient comfort; **Designer Luxury Clocks** for premium retail and showroom display; **OEM Private Label** manufacturing where we build clocks under your own brand; **Promotional Clocks** for Mumbai-based marketing agencies, BTL companies, and event organisers; **Real Estate Gifting Clocks** for Mumbai builders gifting flat owners.\n\n"
            "All Mumbai shipments are insured for transit damage. GST invoices issued. Payment via NEFT, UPI, or cheque."
        ),
        "delivery_content": (
            "Mumbai delivery takes 3-5 business days from Jaipur. We use established transporters with proven track records on the Jaipur–Mumbai route. "
            "Door delivery available across Mumbai pincodes — South Mumbai (400001-400034), Andheri-Bandra belt (400050-400099), Thane (400601-400615), Navi Mumbai (400701-400710), Borivali-Goregaon (400063-400103), and Mumbai suburbs. "
            "For urgent requirements we offer air freight at premium rates with 24-48 hour delivery."
        ),
        "industries_content": (
            "Mumbai industries served — **Hotels & Hospitality** chains across South Mumbai, Andheri and Powai use our silent sweep clocks; **Real Estate** developers in Thane, Navi Mumbai and Andheri gift our branded clocks to flat buyers; **Corporate Houses** in BKC, Lower Parel, Nariman Point and Worli order branded clocks for annual gifting; **Multiplex & Mall Operators** install our durable wall clocks; **Educational Institutes** in Mumbai schools and colleges procure classroom clocks; **Hospital Chains** across Mumbai use non-tick clocks for patient wards; **Retail Wholesalers** in Crawford Market, Bhuleshwar, Lamington Road stock our wholesale clocks; **Event Companies** use promotional clocks for trade shows and exhibitions at Bombay Exhibition Centre."
        ),
        "closing_content": (
            "Mumbai buyers — direct factory pricing, custom logo printing free on bulk, 3-5 day delivery, GST invoice. WhatsApp or call us for catalogue and pricing."
        ),
        "meta_keywords": "wall clock supplier in mumbai, wholesale wall clocks mumbai, bulk wall clock supplier mumbai, corporate clock supplier mumbai, wall clock dealer mumbai",
        "delivery_time": "3-5 business days",
        "nearby_areas": "South Mumbai, Andheri, Bandra, BKC, Lower Parel, Worli, Thane, Navi Mumbai, Borivali, Goregaon, Powai",
        "display_order": 2,
    },
    # ==================== BANGALORE ====================
    {
        "city_name": "Bangalore",
        "state": "Karnataka",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Bangalore — Bulk & Custom Logo Specialists",
        "hero_subheading": "Wholesale wall clocks for Bangalore IT companies, retailers, hotels, hospitals and corporate gifting buyers. Direct from Jaipur factory with custom logo printing.",
        "intro_content": (
            "HOOVALE supplies wall clocks across Bangalore — covering Whitefield, Electronic City, Koramangala, Indiranagar, MG Road, Brigade Road, HSR Layout, Marathahalli, Yelahanka, Hebbal and the entire Bangalore metropolitan region. "
            "Bangalore is one of our highest-growth markets thanks to the city's massive corporate ecosystem, IT parks, and emerging retail brands.\n\n"
            "Our Bangalore customer base is unique — we ship hundreds of branded clocks every month to IT companies in Electronic City and Whitefield for employee gifting and office decor. "
            "We also serve traditional clock retailers in Commercial Street and Avenue Road, premium designer stores in Indiranagar, hotel groups across the city, multispecialty hospital chains, schools and colleges, and Bangalore's vibrant startup ecosystem ordering branded clocks as office swag."
        ),
        "why_choose_content": (
            "Bangalore IT and corporate buyers expect three things — speed, quality, and tech-friendly procurement processes. We deliver all three. "
            "Our online catalogue is shareable via WhatsApp and email. Quotations are sent within 2 hours. Custom logo mockups before production. Digital invoices, online payments via NEFT/UPI. Tracking provided for shipments.\n\n"
            "On the product side — every clock is quartz-movement based with 1-year warranty, silent sweep variants for offices and hospitals, premium UV-printed dials that don't fade, multiple frame materials including premium wood and acrylic, modern designer collections for tech offices, and traditional designs for hospitality buyers. "
            "Bangalore buyers also benefit from our flexible MOQ — order from 5 pieces for testing, then scale to thousands once approved."
        ),
        "services_content": (
            "Our Bangalore services include **Corporate Gifting Solutions** for IT parks in Whitefield and Electronic City; **Branded Office Clocks** with company logo for tech firms in Koramangala, Indiranagar and HSR; **Hotel Wall Clocks** for hospitality chains across Bangalore; **Hospital Clocks** with non-tick movement for healthcare facilities; **OEM Manufacturing** for Bangalore retail brands launching their own clock lines; **Bulk Wholesale** for retailers in Commercial Street and Avenue Road; **Promotional Clocks** for Bangalore startups and marketing agencies; **Designer Showroom Pieces** for premium home decor stores in Indiranagar and Koramangala; **Retail Distribution** for Karnataka distributors covering Tier-2 and Tier-3 cities.\n\n"
            "All orders include GST invoice, transit insurance on bulk, and dedicated WhatsApp support."
        ),
        "delivery_content": (
            "Bangalore delivery takes 4-6 business days from our Jaipur factory. We use trusted transporters covering the Jaipur-Bangalore route with verified delivery records. "
            "Door-step delivery to all Bangalore pincodes including Whitefield (560066), Electronic City (560100), Koramangala (560034), Indiranagar (560038), HSR Layout (560102), MG Road (560001), Hebbal (560024), Marathahalli (560037) and surrounding areas. "
            "Express air freight available for urgent corporate gifting requirements."
        ),
        "industries_content": (
            "Bangalore industry verticals served — **IT & Tech Companies** in Whitefield, Electronic City, Manyata Tech Park and Bagmane Tech Park ordering branded clocks for offices and employee gifting; **Startups** across Koramangala, Indiranagar, HSR Layout buying promotional clocks for events and brand campaigns; **Hotels** including business hotels and resorts ordering silent sweep clocks; **Hospitals** across Bangalore using non-tick clocks for patient wards; **Schools & Educational Institutes** including international schools procuring classroom clocks; **Retail & Wholesale** outlets in Commercial Street, Avenue Road, Brigade Road; **Real Estate Developers** in Whitefield, Sarjapur, Hebbal gifting clocks to home buyers; **Event & Marketing Agencies** using promotional clocks for trade shows and brand activations."
        ),
        "closing_content": (
            "Bangalore tech buyers and traditional retailers — direct factory rates, custom logo on bulk, 4-6 day delivery, GST invoice, online payment. WhatsApp us for quick catalogue."
        ),
        "meta_keywords": "wall clock supplier in bangalore, wholesale wall clocks bangalore, corporate clock supplier bangalore, branded wall clocks bangalore, wall clock manufacturer bangalore",
        "delivery_time": "4-6 business days",
        "nearby_areas": "Whitefield, Electronic City, Koramangala, Indiranagar, HSR Layout, MG Road, Brigade Road, Marathahalli, Hebbal, Yelahanka",
        "display_order": 3,
    },
    # ==================== CHENNAI ====================
    {
        "city_name": "Chennai",
        "state": "Tamil Nadu",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Chennai — Wholesale & Bulk B2B Specialist",
        "hero_subheading": "Direct factory wall clock supply for Chennai retailers, distributors, corporate buyers and gifting companies. Custom logo printing and OEM manufacturing available.",
        "intro_content": (
            "HOOVALE is a leading wall clock supplier in Chennai serving the metro's diverse business landscape — covering T Nagar, Anna Nagar, Mylapore, Velachery, OMR (Old Mahabalipuram Road), Adyar, Tambaram, Porur, Guindy and surrounding regions. "
            "Chennai is a strategic market for us due to its strong manufacturing base, growing IT presence on OMR, established retail districts, and large hospital and educational ecosystem.\n\n"
            "We supply Chennai businesses across categories — wholesale clock dealers in Sowcarpet and Parry's Corner, IT companies on OMR, hospital chains across the city, schools and colleges, hotels and budget chains, real estate builders gifting clocks to flat owners, and Tamil Nadu state government PSUs ordering office clocks. "
            "Our direct-from-factory model means Chennai buyers get genuine wholesale pricing without paying multiple distributor margins."
        ),
        "why_choose_content": (
            "Chennai's B2B buyers value product reliability, transparent pricing, and post-sales support — areas where HOOVALE consistently delivers. "
            "Our clocks come with 1-year movement warranty, all dispatches include batch numbers for traceability, and we maintain a dedicated support number for after-sales queries. "
            "Custom logo orders include free design mockups before production, ensuring you approve the final dial design before we manufacture.\n\n"
            "Pricing is straightforward — published bulk slabs without hidden charges. Order 5-50 pieces for testing, 50-500 for retail stocking, 500+ for major corporate or distributor orders. Each tier has clear pricing with no negotiation games. "
            "We also offer staggered dispatches — order 1000 pieces and we can ship 250 immediately and the rest in monthly tranches to manage your inventory."
        ),
        "services_content": (
            "Chennai services covered — **Wholesale Bulk Supply** for retailers in Sowcarpet, Parry's Corner, T Nagar; **Corporate Branded Clocks** for OMR IT companies and Anna Salai corporates; **Hotel Wall Clocks** for Chennai hospitality chains and lodges; **Hospital Wall Clocks** with non-tick movement for healthcare; **OEM Manufacturing** for Chennai brands launching private label clock collections; **Promotional Clocks** for Chennai marketing agencies and event companies; **Builder Gifting Clocks** for real estate developers in OMR and ECR; **Educational Institute Clocks** for schools across Tamil Nadu; **Government Tender Supply** for PSU and government office clock requirements.\n\n"
            "All Chennai shipments include proper invoicing, e-way bill where applicable, and transit insurance on bulk."
        ),
        "delivery_content": (
            "Chennai delivery typically takes 5-7 business days from Jaipur via road transport. "
            "Coverage includes all Chennai pincodes — T Nagar (600017), Anna Nagar (600040), Mylapore (600004), Velachery (600042), OMR area (600119-600127), Adyar (600020), Tambaram (600045), Porur (600116), Guindy (600032). "
            "Bulk orders to Tamil Nadu Tier-2 cities like Coimbatore, Madurai, Trichy and Salem also serviced via Chennai hub."
        ),
        "industries_content": (
            "Chennai industries — **IT Sector** companies on OMR, Tidel Park, ELCOT IT Park ordering branded clocks; **Manufacturing** units in Ambattur, Sriperumbudur, and Chennai industrial estates buying office clocks; **Hospitals** across Chennai using silent sweep clocks; **Hotels** including budget chains, business hotels, and resorts; **Schools & Colleges** across Tamil Nadu procuring classroom clocks; **Retail Distribution** through Sowcarpet, Parry's Corner, T Nagar wholesalers; **Real Estate** developers along OMR, ECR gifting clocks; **Government Departments** ordering office clocks via tenders; **Event Companies** for trade shows at Chennai Trade Centre."
        ),
        "closing_content": (
            "Chennai buyers — wholesale rates direct from factory, custom logo on bulk orders, 5-7 day delivery, GST invoice, transit insurance. Talk to us on WhatsApp."
        ),
        "meta_keywords": "wall clock supplier in chennai, wholesale wall clocks chennai, bulk wall clock chennai, branded wall clocks chennai, wall clock manufacturer chennai",
        "delivery_time": "5-7 business days",
        "nearby_areas": "T Nagar, Anna Nagar, Mylapore, Velachery, OMR, Adyar, Tambaram, Porur, Guindy, Sowcarpet",
        "display_order": 4,
    },
    # ==================== HYDERABAD ====================
    {
        "city_name": "Hyderabad",
        "state": "Telangana",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Hyderabad — HITEC City to Old City",
        "hero_subheading": "Bulk wall clock supply for Hyderabad businesses — IT companies, hotels, retailers, hospitals, real estate. Direct factory pricing with custom logo printing.",
        "intro_content": (
            "HOOVALE supplies wall clocks across Hyderabad — covering HITEC City, Gachibowli, Banjara Hills, Jubilee Hills, Kukatpally, Secunderabad, Begumpet, Madhapur, Kondapur, and the historic Old City areas. "
            "Hyderabad's blend of modern IT hubs and traditional retail makes it one of our most diverse customer markets.\n\n"
            "We serve Hyderabad's IT corridor with branded clocks for Microsoft, Google, Amazon vendor offices and hundreds of mid-sized tech companies in HITEC City and Gachibowli. "
            "Traditional clock retailers in Begum Bazaar, General Bazaar Secunderabad, and Sultan Bazaar source bulk inventory from us. "
            "Hyderabad's hotel and pharma sectors are also major buyers — silent sweep clocks for hotel rooms, non-tick clocks for pharma manufacturing units and hospitals."
        ),
        "why_choose_content": (
            "Hyderabad buyers prefer HOOVALE for our direct manufacturer status, consistent quality, and responsive customer service. "
            "Unlike traders who simply resell, we control every stage — from movement assembly to dial printing to frame finishing — ensuring uniform quality across thousands of pieces. "
            "Our Hyderabad customers report 95%+ satisfaction with first-time orders, and most repeat orders come within 60 days.\n\n"
            "Pricing transparency is another reason. We publish bulk slabs upfront — no hidden charges, no last-minute price hikes. GST is included or excluded as you prefer (let us know in your enquiry). Payment terms are flexible for verified businesses — partial advance, balance against PI dispatch."
        ),
        "services_content": (
            "Hyderabad supply services — **IT Corporate Branded Clocks** for HITEC City, Gachibowli, Madhapur tech companies; **Wholesale Bulk Orders** for Begum Bazaar, General Bazaar retailers; **Hotel Wall Clocks** with silent sweep for Hyderabad hospitality; **Pharma & Hospital Clocks** with non-tick movement for pharma units in Genome Valley and city hospitals; **OEM Private Label** manufacturing for Hyderabad clock brands; **Promotional Clocks** for Hyderabad event and marketing companies; **Real Estate Gifting Clocks** for builders in Kondapur, Kukatpally, Tellapur; **Educational Clocks** for schools and engineering colleges across Telangana.\n\n"
            "All orders include invoicing as per Telangana state GST rules, e-way bills, and transit insurance for bulk."
        ),
        "delivery_content": (
            "Hyderabad delivery takes 4-6 business days from our Jaipur factory. "
            "We deliver to all Hyderabad pincodes — HITEC City (500081), Gachibowli (500032), Banjara Hills (500034), Jubilee Hills (500033), Kukatpally (500072), Secunderabad (500003), Begumpet (500016), Madhapur (500081), Kondapur (500084), Old City (500002). "
            "Telangana state coverage includes Warangal, Karimnagar, Khammam via Hyderabad hub."
        ),
        "industries_content": (
            "Hyderabad industries — **IT & ITES** companies in HITEC City, Gachibowli, Mindspace, Raheja IT Park ordering branded clocks; **Pharmaceutical** units in Genome Valley, Bollaram and Hyderabad pharma cluster using non-tick clocks; **Hospitals** including multispecialty chains across the city; **Hotels** in Banjara Hills, Jubilee Hills, Hitec City; **Schools** affiliated to CBSE, IB and Telangana State Board; **Retail Wholesale** in Begum Bazaar, General Bazaar; **Real Estate** developers in Tellapur, Kondapur, Kukatpally; **Government & PSU** offices via tender supply."
        ),
        "closing_content": (
            "Hyderabad buyers — direct factory wholesale, custom logo printing, 4-6 day delivery, GST invoice, flexible payment terms. WhatsApp us for the latest catalogue."
        ),
        "meta_keywords": "wall clock supplier in hyderabad, wholesale wall clocks hyderabad, corporate clock supplier hyderabad, branded wall clocks hyderabad, wall clock dealer hyderabad",
        "delivery_time": "4-6 business days",
        "nearby_areas": "HITEC City, Gachibowli, Banjara Hills, Jubilee Hills, Kukatpally, Secunderabad, Begumpet, Madhapur, Kondapur, Old City",
        "display_order": 5,
    },
    # ==================== PUNE ====================
    {
        "city_name": "Pune",
        "state": "Maharashtra",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Pune — Wholesale & Custom Logo",
        "hero_subheading": "Bulk wall clock supply for Pune retailers, IT companies, hotels, schools and corporate gifting buyers. Direct from Jaipur factory at wholesale prices.",
        "intro_content": (
            "HOOVALE is a trusted wall clock supplier in Pune covering all major business areas — Hinjewadi, Kharadi, Magarpatta, Viman Nagar, Camp, Shivaji Nagar, Aundh, Baner, Wakad, Hadapsar, Pimpri-Chinchwad and surrounding regions. "
            "Pune's strong educational, automotive, and IT ecosystem makes it a high-volume market for our wall clocks.\n\n"
            "Our Pune customer mix includes IT companies in Hinjewadi and Kharadi (branded clocks for offices), automotive manufacturers and ancillaries in Pimpri-Chinchwad and Chakan (industrial clocks for shop floors and offices), schools and colleges across the city (classroom clocks), hotels and hospitality businesses (silent sweep clocks), retail wholesalers in Camp and Tulshibaug (bulk inventory), and hospitals (non-tick clocks for wards). "
            "Real estate builders in Wakad, Kharadi, Hinjewadi gift our designer clocks to home buyers as part of welcome packages."
        ),
        "why_choose_content": (
            "Pune is a quality-conscious market — buyers research thoroughly before committing to bulk orders. We pass that scrutiny because our products genuinely deliver. "
            "Every HOOVALE clock uses imported Japanese-grade quartz movements with proven 5+ year accuracy, dial printing uses fade-resistant UV inks, and frames are sourced from Indian craft hubs known for finish quality. "
            "We also offer sample orders before bulk — Pune buyers can order 5-10 pieces for testing, evaluate quality and finish, then commit to larger quantities with full confidence.\n\n"
            "Service-wise, our Pune accounts get dedicated WhatsApp support, mockup approvals before production, and proactive shipment tracking. Most Pune orders ship within 24-48 hours of confirmation."
        ),
        "services_content": (
            "Pune services include **IT Corporate Gifting** for Hinjewadi, Kharadi and Magarpatta tech companies; **Automotive Industry Clocks** for Pimpri-Chinchwad, Chakan industrial belt; **School & College Clocks** for Pune educational institutes; **Hotel Wall Clocks** with silent movement for Pune hospitality; **Hospital Clocks** for healthcare facilities; **OEM Manufacturing** for Pune brands; **Wholesale Bulk Supply** for Camp, Tulshibaug, and FC Road retailers; **Promotional Clocks** for Pune event and marketing companies; **Real Estate Gifting** for Pune builders.\n\n"
            "All orders dispatched with proper invoicing and e-way bills. Transit insurance available for bulk orders."
        ),
        "delivery_content": (
            "Pune delivery typically takes 3-5 business days from Jaipur via established road transporters. "
            "We deliver to all Pune pincodes — Hinjewadi (411057), Kharadi (411014), Magarpatta (411013), Viman Nagar (411014), Camp (411001), Shivaji Nagar (411005), Aundh (411007), Baner (411045), Wakad (411057), Hadapsar (411028), Pimpri-Chinchwad (411017-411019). "
            "Maharashtra Tier-2 cities like Aurangabad, Nashik, Kolhapur, Nagpur also serviced via Pune-Mumbai corridor."
        ),
        "industries_content": (
            "Pune industries — **IT & Tech** in Hinjewadi Phase 1, 2, 3, Kharadi EON IT Park, Magarpatta Cybercity; **Automotive** OEMs and Tier-1 suppliers in Chakan, Talegaon, Pimpri-Chinchwad MIDC; **Education** schools, colleges, MBA institutes across Pune; **Hospitality** business hotels and budget chains; **Healthcare** multispecialty hospitals; **Retail** through Camp, Laxmi Road, Tulshibaug, FC Road wholesalers; **Real Estate** developers in Wakad, Kharadi, Hinjewadi, Wagholi; **Government** offices and PSU tender supply."
        ),
        "closing_content": (
            "Pune buyers — quality-tested clocks, direct factory pricing, custom logo on bulk, 3-5 day delivery. Sample orders available for first-time buyers. WhatsApp for catalogue."
        ),
        "meta_keywords": "wall clock supplier in pune, wholesale wall clocks pune, bulk wall clock supplier pune, corporate clock supplier pune, branded wall clocks pune",
        "delivery_time": "3-5 business days",
        "nearby_areas": "Hinjewadi, Kharadi, Magarpatta, Viman Nagar, Camp, Shivaji Nagar, Aundh, Baner, Wakad, Pimpri-Chinchwad",
        "display_order": 6,
    },
    # ==================== AHMEDABAD ====================
    {
        "city_name": "Ahmedabad",
        "state": "Gujarat",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Ahmedabad — Wholesale Direct from Jaipur",
        "hero_subheading": "Bulk wall clock supply for Ahmedabad retailers, traders, corporates, hotels and gifting companies. Custom logo printing, OEM manufacturing, factory pricing.",
        "intro_content": (
            "HOOVALE serves Ahmedabad as a primary wholesale wall clock supplier — covering CG Road, SG Highway, Prahlad Nagar, Bodakdev, Vastrapur, Satellite, Maninagar, Naranpura, Navrangpura, Old City and the entire Ahmedabad metro region. "
            "Gujarat is one of our most strategic markets due to its strong trader culture, manufacturing base, and growing corporate sector.\n\n"
            "Ahmedabad buyers know value when they see it. Our Gujarati customer base — traders in Manek Chowk and Ratan Pol, wholesale dealers in Kalupur and Karanj, gift shop owners across the city, corporates on SG Highway and CG Road, hotels and hospitality in Bodakdev and Prahlad Nagar — chose us because we offer genuine factory pricing with no hidden costs. "
            "Many Ahmedabad businesses have been with us for 5+ years, ordering monthly stock without negotiation hassles thanks to our transparent slab-based pricing."
        ),
        "why_choose_content": (
            "Ahmedabad's trader community values long-term relationships, fair pricing, and consistent quality — three principles HOOVALE has built our business around. "
            "We don't play pricing games. Our published wholesale slabs apply equally to first-time buyers and 10-year repeat customers. The only difference for loyal customers is faster credit terms and priority dispatch.\n\n"
            "Quality-wise, we understand Gujarat market expectations — durable products that don't malfunction in 6 months, clean dial printing that doesn't fade, frames that don't warp. "
            "Every HOOVALE clock is tested for 24-hour run cycle before dispatch. We provide 1-year movement replacement warranty (if movement fails, we replace it free — buyer just sends us the faulty piece). This warranty is valid even on bulk wholesale orders."
        ),
        "services_content": (
            "Ahmedabad supply services — **Wholesale Trading Stock** for traders in Manek Chowk, Ratan Pol, Kalupur, Karanj; **Corporate Branded Clocks** for SG Highway and CG Road businesses; **Diwali Gifting Clocks** for Gujarat companies (we have a special Diwali gifting season catalogue); **Hotel Wall Clocks** for Ahmedabad hospitality; **Hospital Clocks** for healthcare; **OEM Manufacturing** for Gujarat clock brands wanting private label; **Promotional Clocks** for marketing campaigns; **Builder Gifting Clocks** for Ahmedabad real estate gifting; **Wedding Gifting Clocks** for Gujarat wedding gift suppliers (high-volume seasonal market).\n\n"
            "All Ahmedabad orders dispatched with proper Gujarat GST invoicing. E-way bills and transit insurance included on bulk."
        ),
        "delivery_content": (
            "Ahmedabad enjoys our 2nd-fastest delivery slot after Delhi — orders confirmed by 3 PM ship same day from Jaipur and reach Ahmedabad in 2-4 business days. Jaipur-Ahmedabad route is one of our most active corridors. "
            "Coverage includes all Ahmedabad pincodes — CG Road (380009), SG Highway (380015-380054), Prahlad Nagar (380015), Bodakdev (380054), Vastrapur (380015), Satellite (380015), Maninagar (380008), Naranpura (380013), Navrangpura (380009), Old City (380001-380002). "
            "Gujarat Tier-2 cities like Surat, Vadodara, Rajkot, Bhavnagar also serviced via Ahmedabad."
        ),
        "industries_content": (
            "Ahmedabad industries — **Trading & Wholesale** community in Manek Chowk, Ratan Pol, Kalupur (clocks for resale across Gujarat); **Pharmaceutical** companies in Changodar, Kheda, Sanand industrial belts; **Textile** mills and traders in Naroda, Vastral, Narol; **Corporate** offices on SG Highway, CG Road, Prahlad Nagar; **Real Estate** developers in Bodakdev, Satellite, SG Highway, South Bopal; **Education** schools and colleges across Ahmedabad and Gujarat; **Hospitality** business hotels in Bodakdev, Prahlad Nagar; **Healthcare** multispecialty hospitals; **Auto Industry** Tata, Maruti and ancillaries in Sanand-Becharaji belt."
        ),
        "closing_content": (
            "Ahmedabad buyers — fastest delivery slot after Delhi (2-4 days), transparent pricing, 1-year warranty, custom logo on bulk. WhatsApp us for Gujarat-specific pricing."
        ),
        "meta_keywords": "wall clock supplier in ahmedabad, wholesale wall clocks ahmedabad, bulk wall clock supplier gujarat, corporate clocks ahmedabad, wall clock manufacturer ahmedabad",
        "delivery_time": "2-4 business days",
        "nearby_areas": "CG Road, SG Highway, Prahlad Nagar, Bodakdev, Vastrapur, Satellite, Maninagar, Naranpura, Navrangpura, Old City",
        "display_order": 7,
    },
    # ==================== KOLKATA ====================
    {
        "city_name": "Kolkata",
        "state": "West Bengal",
        "page_type": "supplier",
        "h1_heading": "Wall Clock Supplier in Kolkata — Wholesale & Bulk Manufacturer",
        "hero_subheading": "Direct factory wall clock supply for Kolkata retailers, distributors, corporate buyers, hotels and gifting companies. Custom logo printing and bulk discounts.",
        "intro_content": (
            "HOOVALE supplies wall clocks across Kolkata covering Park Street, Salt Lake (Sector V), New Town Rajarhat, Howrah, Ballygunge, Jadavpur, Behala, Garia, Tollygunge, BBD Bagh, Burrabazar, and surrounding metropolitan areas. "
            "Kolkata is a strategic eastern India hub that lets us serve West Bengal, Bihar, Jharkhand, Odisha, and the Northeast through Kolkata-based distributors.\n\n"
            "Our Kolkata customer base spans traditional and modern segments — wholesale clock dealers in Burrabazar and Bowbazar (the historic clock trading hubs of eastern India), IT companies and BPOs in Salt Lake Sector V and New Town, hotels in Park Street and Esplanade, hospitals across the city, schools (Kolkata has hundreds of CBSE/ICSE/State Board schools), and corporate offices in BBD Bagh, Camac Street and Park Street. "
            "We also supply Kolkata-based distributors who service Tier-2 markets like Siliguri, Asansol, Durgapur, Patna, Bhubaneswar."
        ),
        "why_choose_content": (
            "Kolkata's market has unique characteristics — strong wholesale culture in Burrabazar, price-sensitive but quality-aware buyers, and significant onward distribution to eastern India and Northeast. "
            "We've adapted to these realities. Our Kolkata wholesale slabs are competitive even against China imports because of our scale efficiencies. Quality is consistently high — we don't compromise on movement or printing to hit a price point. "
            "And we support onward distribution by offering favourable terms to Kolkata-based distributors selling into smaller cities.\n\n"
            "For end users — corporates, hotels, schools — we offer custom logo printing, designer collections, and silent sweep variants. Custom orders include free mockup approval before production starts."
        ),
        "services_content": (
            "Kolkata services — **Wholesale Bulk Trading Stock** for Burrabazar, Bowbazar, Lalbazar dealers; **Onward Distribution Supply** for Kolkata distributors covering Bihar, Jharkhand, Odisha, Northeast; **Corporate Branded Clocks** for Salt Lake, New Town, BBD Bagh, Park Street offices; **Hotel Wall Clocks** for Kolkata hospitality; **Hospital Clocks** for healthcare; **School Clocks** for Kolkata's massive school network; **OEM Manufacturing** for Kolkata clock brands; **Promotional Clocks** for events and marketing; **Pujo Special Gifting Clocks** for the Durga Pujo gifting season — a major seasonal opportunity.\n\n"
            "All Kolkata orders include proper West Bengal GST invoicing, e-way bills for inter-state movement, and bulk transit insurance."
        ),
        "delivery_content": (
            "Kolkata delivery takes 6-8 business days from Jaipur via road transport — this is our longest-route domestic delivery due to geographic distance, but we maintain reliability through trusted transporters. "
            "Coverage includes all Kolkata pincodes — Park Street (700016), Salt Lake (700064-700091), New Town (700156), Howrah (711101-711410), Ballygunge (700019), Jadavpur (700032), Behala (700034-700060), Garia (700084), Tollygunge (700033), BBD Bagh (700001), Burrabazar (700007). "
            "Onward distribution to Siliguri, Asansol, Durgapur, Patna, Bhubaneswar via Kolkata transport hub."
        ),
        "industries_content": (
            "Kolkata industries — **Traditional Wholesale Trade** in Burrabazar, Bowbazar (eastern India clock distribution hubs); **IT & ITES** in Salt Lake Sector V, New Town Rajarhat (TCS, Cognizant, Wipro and BPOs); **Hospitality** business hotels in Park Street, Camac Street, EM Bypass; **Healthcare** multispecialty hospitals across Kolkata; **Education** schools across Kolkata (one of India's most dense school markets); **Manufacturing** units in Howrah industrial belt; **Real Estate** developers in New Town, Rajarhat, Garia; **Government & PSU** offices via tender supply; **Onward Distribution** to West Bengal, Bihar, Jharkhand, Odisha and Northeast through Kolkata-based distributors."
        ),
        "closing_content": (
            "Kolkata buyers and eastern India distributors — competitive wholesale, custom logo, onward distribution support, GST invoice. WhatsApp for catalogue and dealer terms."
        ),
        "meta_keywords": "wall clock supplier in kolkata, wholesale wall clocks kolkata, bulk wall clock supplier kolkata, corporate clock supplier kolkata, eastern india wall clock distributor",
        "delivery_time": "6-8 business days",
        "nearby_areas": "Park Street, Salt Lake Sector V, New Town Rajarhat, Howrah, Ballygunge, Jadavpur, Behala, Garia, BBD Bagh, Burrabazar",
        "display_order": 8,
    },
]


# ========================================================================
# INDUSTRY PAGES (6 industries × 600 words = ~3600 words)
# ========================================================================

INDUSTRY_DATA = [
    {
        "industry_name": "Corporate Offices",
        "icon_class": "fas fa-building",
        "h1_heading": "Wall Clocks for Corporate Offices — Branded, Bulk, OEM Supply",
        "hero_subheading": "Premium branded wall clocks for corporate gifting, employee anniversaries, office decor, and client gifting. Custom logo printing on bulk orders.",
        "intro_content": (
            "Corporate offices need wall clocks that do more than just tell time — they reinforce brand identity, project professionalism, and serve as functional decor. "
            "HOOVALE manufactures and supplies premium wall clocks specifically designed for corporate environments — from Fortune 500 multinationals to mid-sized Indian businesses, startups, and family-run enterprises. "
            "Our corporate clock catalogue includes branded clocks with company logos for office walls, conference rooms, and reception areas; gifting clocks for employee tenure milestones, retirement gifts, client appreciation, and Diwali corporate gifting; and OEM clocks under your own brand for resale or internal distribution.\n\n"
            "We work with corporate procurement teams across India — handling bulk orders from 50 pieces to 5000+ pieces with consistent quality, transparent pricing, and on-time delivery."
        ),
        "benefits_content": (
            "Why corporates choose HOOVALE for their wall clock needs:\n\n"
            "**Brand Reinforcement** — Custom UV logo printing on dial face puts your company logo in front of employees, visitors, and clients every single day. Studies show offices with branded elements see 23% higher employee brand recall.\n\n"
            "**Premium Build** — Corporate environments demand quality. Our office clocks use Japanese-grade quartz movements (5+ year accuracy), fade-resistant UV-printed dials, and durable frames in wood, metal or premium plastic.\n\n"
            "**Bulk Pricing** — Corporate orders enjoy our deepest wholesale slabs. Order 100+ pieces and unlock factory-direct pricing that retail markets simply cannot match.\n\n"
            "**Custom Configuration** — Choose your dial colour, frame finish, size (8 inch to 24 inch), movement type (regular tick or silent sweep for quiet offices), and packaging (individual gift boxes available)."
        ),
        "customization_content": (
            "Customisation options for corporate wall clocks:\n\n"
            "**Logo Placement** — Center logo, bottom logo, branded dial markers, or full custom dial design. Single colour or full-colour UV printing available.\n\n"
            "**Sizes** — 8 inch (small offices, cabins), 10 inch (standard), 12 inch (conference rooms, reception), 14-16 inch (large halls, atriums), custom sizes on request.\n\n"
            "**Frame Materials** — Premium wood (oak, walnut, teak finish), brushed metal (silver, gold), matte plastic (black, white), acrylic (modern offices), and combo finishes.\n\n"
            "**Dial Variations** — White dial with logo, black dial with logo, brand colour dial, photo-print dial for milestone celebrations, custom artwork dial.\n\n"
            "**Packaging** — Bulk corrugated boxes (standard), individual gift boxes (premium gifting), custom branded packaging (high-end client gifting)."
        ),
        "case_study_content": (
            "Recent corporate projects: A leading IT services company in Bangalore ordered 1200 branded clocks for their employee 5-year anniversary gifts — custom logo, walnut wood frame, silent sweep movement, individual gift boxes. Delivered in 18 days. "
            "A pharmaceutical major in Hyderabad ordered 500 premium clocks for Diwali corporate gifting to top distributors and clients — gold-tone metal frame, embossed logo dial, premium gift packaging. "
            "A real estate developer in Mumbai ordered 800 designer clocks as flat owner welcome gifts — custom dial with project logo, premium wooden frame, branded gift box. All projects delivered on schedule with 100% quality acceptance."
        ),
        "meta_keywords": "corporate wall clock manufacturer, branded wall clocks for office, corporate gifting clocks, employee gifting clocks, oem wall clock supplier corporate",
        "display_order": 1,
    },
    {
        "industry_name": "Hotels & Hospitality",
        "icon_class": "fas fa-hotel",
        "h1_heading": "Wall Clocks for Hotels — Silent Sweep, Designer & Bulk Supply",
        "hero_subheading": "Premium silent-sweep wall clocks for hotel guest rooms, lobbies, banquet halls, and back-of-house areas. Direct factory pricing for bulk hotel orders.",
        "intro_content": (
            "Hotels and hospitality businesses have unique wall clock requirements — guest rooms need silent sweep clocks (no ticking sound), lobbies need premium designer pieces that match interior themes, banquet halls need durable timepieces visible from distance, and back-of-house areas need reliable functional clocks. "
            "HOOVALE supplies all these categories under one roof, with deep experience serving 3-star to 5-star hotels, budget chains, boutique properties, resorts, and serviced apartments across India.\n\n"
            "Our hotel customers include independent properties, regional chains, and procurement teams of major hotel groups. We handle orders from 50 pieces (small property renovation) to 5000+ pieces (multi-property chain orders) with the same care and quality control."
        ),
        "benefits_content": (
            "**Silent Sweep Movement** — Our hotel guest room clocks use whisper-quiet sweep movements (not ticking quartz). Guests sleep peacefully — a small detail that prevents bad reviews about 'noisy room clocks'.\n\n"
            "**Designer Aesthetics** — Hotel lobbies and banquet halls need clocks that complement interior design. Our designer collection includes contemporary, classical, modern, vintage, and minimalist styles in multiple sizes.\n\n"
            "**Durability** — Hotels are high-touch environments. Our hotel clocks use commercial-grade movements, reinforced frames, and shatter-resistant glass — built to last years of guest interaction.\n\n"
            "**Bulk Pricing** — Hotel chains benefit from our deepest discount tiers. We've supplied multi-property orders with consolidated dispatch, simplifying chain procurement."
        ),
        "customization_content": (
            "Hotel-specific customisation:\n\n"
            "**Branded Hotel Clocks** — Custom dial with hotel logo for premium properties wanting branded room clocks (also serves as a souvenir-style touch).\n\n"
            "**Multiple Time Zone Clocks** — Lobby installations showing local time + key international cities (London, New York, Dubai, Tokyo). Useful for business hotels.\n\n"
            "**Themed Designs** — Heritage hotels prefer vintage Roman numeral clocks, modern hotels prefer minimalist designs, beach resorts prefer themed dials.\n\n"
            "**Sizes** — Guest rooms (10-12 inch standard), lobbies (16-24 inch statement pieces), banquet halls (large 24+ inch), staff areas (functional 10 inch)."
        ),
        "case_study_content": (
            "Recent hotel projects: A 200-room business hotel in Mumbai ordered 250 silent sweep guest room clocks (10 inch, branded dial) plus 8 statement pieces for lobbies and banquet halls. "
            "A 5-property resort chain in Goa ordered 800 themed clocks across all properties — beach-themed dials, weathered wood frames, salt-resistant finishes. "
            "A budget hotel chain renovating 12 properties ordered 1500 standard guest room clocks — economical but quality, branded packaging for property managers. "
            "All projects delivered phase-wise as per renovation schedules."
        ),
        "meta_keywords": "wall clocks for hotels, hotel room wall clocks, silent sweep clocks hotels, hospitality wall clock supplier, branded hotel clocks bulk supply",
        "display_order": 2,
    },
    {
        "industry_name": "Hospitals & Healthcare",
        "icon_class": "fas fa-hospital",
        "h1_heading": "Wall Clocks for Hospitals — Non-Tick, Patient-Friendly Bulk Supply",
        "hero_subheading": "Silent non-tick wall clocks for hospital wards, OPDs, ICUs, operation theatres, and waiting areas. Hygiene-friendly designs for healthcare environments.",
        "intro_content": (
            "Hospitals require wall clocks that don't create disturbance for patients (no ticking sound), are easy to clean (smooth surfaces), and are reliable around the clock. "
            "HOOVALE supplies non-tick (silent sweep) wall clocks specifically designed for healthcare environments — patient wards where ticking can disturb sleep, ICUs where silence is critical, OPDs and waiting areas where time visibility matters, operation theatres requiring synchronised time displays, and administrative areas needing standard office clocks.\n\n"
            "Our hospital customers include multispecialty hospitals, single-specialty centres, dental and eye care chains, diagnostic centres, nursing homes, and government hospital tender supplies. We understand the procurement requirements of healthcare — proper invoicing, MSME certificates if applicable, GST compliance, and on-time delivery for facility opening schedules."
        ),
        "benefits_content": (
            "**Patient-Friendly Silence** — Non-tick movement is critical in patient wards. The constant tick of a regular clock is a documented sleep disturbance factor. Our hospital clocks use sweep movements that are completely silent.\n\n"
            "**Hygiene-Compatible Design** — Smooth surfaces, sealed glass fronts, and easy-clean frames suitable for regular disinfection. Important in post-COVID hospital environments.\n\n"
            "**High Visibility Dials** — Clear, large numbers on white dials with black hands — easy to read for patients of all ages, including elderly patients with reduced vision.\n\n"
            "**Tender-Compliant Documentation** — All required invoicing, GST, MSME certificates (we are MSME registered), and bulk dispatch capability for hospital tenders."
        ),
        "customization_content": (
            "Healthcare-specific options:\n\n"
            "**Hospital Branded Clocks** — Logo printing for branded clocks across multiple departments — promotes the hospital brand in patient-facing areas.\n\n"
            "**Multiple Sizes** — Patient wards (10-12 inch), OPDs and waiting areas (14-16 inch large visibility), reception (12-14 inch), administrative offices (10 inch standard).\n\n"
            "**Movement Types** — All hospital orders use non-tick sweep movements as standard. Tick variants only on specific request.\n\n"
            "**Frame Materials** — White plastic (most hygiene-compatible), brushed metal (premium look), simple wood frames (warmer aesthetic for paediatric and maternity wings)."
        ),
        "case_study_content": (
            "Recent healthcare projects: A 350-bed multispecialty hospital in Pune ordered 400 non-tick clocks across all wards, OPDs, and administrative areas — branded with hospital logo. Delivered phase-wise during facility opening. "
            "A diagnostic centre chain in Hyderabad ordered 180 standardised clocks for 12 centres — uniform branding across the chain. "
            "A government tender supply for a state-run hospital cluster: 600 standard hospital clocks delivered with all required documentation. "
            "All projects met healthcare procurement timelines without delays."
        ),
        "meta_keywords": "wall clocks for hospitals, hospital wall clock supplier, non tick clocks hospitals, healthcare wall clocks bulk, silent wall clocks hospital wards",
        "display_order": 3,
    },
    {
        "industry_name": "Schools & Education",
        "icon_class": "fas fa-school",
        "h1_heading": "Wall Clocks for Schools — Classroom & Hall Bulk Supply",
        "hero_subheading": "Durable, large-display wall clocks for school classrooms, halls, libraries, and offices. Bulk supply with school logo printing on request.",
        "intro_content": (
            "Schools need wall clocks in every classroom, every hall, every staff room, and every administrative office. A typical school with 30-40 classrooms needs 50+ clocks for full coverage. "
            "HOOVALE specialises in school clock bulk supply — durable units that survive years of classroom environments, large clear dials visible from the back of classrooms, easy-read fonts for young students, and economical bulk pricing that fits school budgets. "
            "Our school customers include CBSE/ICSE schools, state board schools, international schools, kindergartens and pre-schools, colleges and universities, coaching institutes, and skill development centres.\n\n"
            "We've supplied clocks to schools across India — from premium international schools to government-run institutions — with documentation suitable for school procurement processes."
        ),
        "benefits_content": (
            "**Classroom Visibility** — Our school clocks have large, clear numbers visible from the back row of a typical classroom (up to 25 feet). Students can read the time without straining.\n\n"
            "**Durability** — School environments are tough on equipment. Our school clocks use reinforced frames, secure mounting, and tamper-resistant designs that survive years of student presence.\n\n"
            "**Economical Bulk Pricing** — Schools order in bulk. Our wholesale slabs make per-unit cost very affordable — fitting school budgets without compromising quality.\n\n"
            "**Branded School Clocks** — Optional school logo printing creates a sense of identity and serves as soft branding. Particularly appreciated by international schools and premium institutions."
        ),
        "customization_content": (
            "School clock customisation options:\n\n"
            "**Standard Classroom Clocks** — 12 inch round, white dial, black numerals, simple frame — the standard model that 90% of schools order.\n\n"
            "**Large Hall Clocks** — 14-18 inch for assembly halls, libraries, gymnasiums, dining halls.\n\n"
            "**Logo-Branded Clocks** — School logo printed on dial face — premium look for international and CBSE schools.\n\n"
            "**Educational Dial Designs** — Roman numeral dials for senior classes (helps students learn Roman numerals), 24-hour display variants, world clock variants with multiple time zones.\n\n"
            "**Movement Types** — Regular quartz (most economical) or silent sweep (premium classrooms and libraries)."
        ),
        "case_study_content": (
            "School project examples: A CBSE school chain with 8 branches ordered 380 standardised classroom clocks across all branches — uniform branding and look. "
            "An international school in Bangalore ordered 120 premium silent sweep clocks for classrooms plus 6 statement pieces for assembly halls — branded with school crest. "
            "A coaching institute in Pune ordered 250 economical classroom clocks for new branch expansion. "
            "A government tender supply for a district education department: 1500 clocks delivered to schools across the district. All deliveries met academic year start dates."
        ),
        "meta_keywords": "wall clocks for schools, school classroom clocks, bulk wall clocks for school, educational institute wall clocks, school clock supplier india",
        "display_order": 4,
    },
    {
        "industry_name": "Retail Stores",
        "icon_class": "fas fa-store",
        "h1_heading": "Wall Clocks for Retail — Wholesale Bulk Supply for Resellers",
        "hero_subheading": "Wholesale wall clocks for retail stores, gift shops, electronics dealers, and clock specialists. Best wholesale prices from direct manufacturer.",
        "intro_content": (
            "Retail clock dealers and gift shops need consistent inventory, competitive wholesale pricing, and a wide product range to satisfy diverse customer preferences. "
            "HOOVALE supplies retail businesses across India — from large clock specialists in Sadar Bazar Delhi, Crawford Market Mumbai, Burrabazar Kolkata to small gift shops in Tier-2 and Tier-3 cities. "
            "We offer the widest range of wall clock designs — wooden, plastic, metal, designer, traditional, modern, customised, branded — at the best wholesale prices in the market.\n\n"
            "Our retail customer base includes wholesale clock dealers, gift shops, electronics retailers (who stock clocks as accessories), online retailers and marketplace sellers, regional distributors covering smaller cities, and modern trade buyers like supermarket chain procurement teams."
        ),
        "benefits_content": (
            "**Widest Product Range** — Over 500 designs across wooden, plastic, metal, acrylic, designer, traditional, modern, customised, and themed categories. One-stop sourcing for retailers.\n\n"
            "**Best Wholesale Pricing** — Direct factory pricing without middleman margins. Retailers consistently report 15-30% better margins compared to buying from sub-distributors.\n\n"
            "**Reliable Stock Availability** — Major designs always in stock. We maintain inventory buffers so retailers can reorder without long lead times.\n\n"
            "**Flexible MOQ** — Order from 5 pieces (single design testing) to thousands (full inventory stocking). MOQ flexibility lets retailers test market response before bulk commitment."
        ),
        "customization_content": (
            "Retail-focused options:\n\n"
            "**Stock Standard Designs** — 500+ ready-to-ship designs that retailers can order in any quantity for store inventory.\n\n"
            "**Private Label Manufacturing** — Established retail brands can order under their own label — we manufacture, you brand and resell.\n\n"
            "**Seasonal Collections** — Diwali season collection, wedding gifting collection, festive variants — timed launches that match retail buying cycles.\n\n"
            "**Mixed-Carton Orders** — Order multiple designs in a single shipment with custom mix per carton. Useful for retailers wanting variety without minimum-per-design constraints."
        ),
        "case_study_content": (
            "Retail customer examples: A major clock retailer in Delhi's Sadar Bazar orders 10,000+ pieces monthly across 80+ designs for distribution to sub-retailers across North India. "
            "A regional distributor in Eastern India sources 5000+ pieces monthly from our Kolkata-bound dispatches, redistributing to retailers in West Bengal, Odisha, Bihar. "
            "A growing online retailer started with 200 pieces (15 designs) and now orders 3000+ pieces monthly after seeing strong online sales. "
            "We support retailers from initial small orders to full-scale wholesale distribution."
        ),
        "meta_keywords": "wholesale wall clocks for retailers, bulk wall clock dealer, retail wall clock supplier, wall clock wholesaler india, wholesale clock manufacturer",
        "display_order": 5,
    },
    {
        "industry_name": "Real Estate & Builders",
        "icon_class": "fas fa-key",
        "h1_heading": "Wall Clocks for Real Estate Builders — Buyer Gifting Bulk Supply",
        "hero_subheading": "Designer wall clocks for real estate flat owner gifting. Custom logo printing with project name, premium gift packaging, bulk discounts.",
        "intro_content": (
            "Real estate developers across India increasingly use designer wall clocks as flat owner welcome gifts — a thoughtful, lasting, and brand-building gesture that homeowners genuinely appreciate. "
            "Unlike sweets or fruit baskets that get consumed and forgotten, a quality wall clock stays on the buyer's wall for years — continuously reinforcing the developer's brand every time the homeowner or their guests look at the time. "
            "HOOVALE manufactures premium gifting clocks specifically for real estate handover — branded with project name and logo, packaged in premium gift boxes, and customised to match the developer's brand aesthetic.\n\n"
            "Our real estate customers include national developers, regional builders, township developers, and luxury property developers across Mumbai, Pune, Bangalore, Hyderabad, Delhi NCR, Chennai, Ahmedabad, Kolkata, Jaipur, and Tier-2 cities."
        ),
        "benefits_content": (
            "**Long-Lasting Brand Visibility** — Unlike consumable gifts, a wall clock stays on the buyer's wall for years. Continuous brand reinforcement at near-zero ongoing cost.\n\n"
            "**Premium Perception** — Wall clocks signal thoughtfulness and quality — much more appreciated than typical builder gifts. Many homeowners hang them in their living rooms, giving the project name visibility to all visitors.\n\n"
            "**Cost-Effective Per Buyer** — Bulk wall clock gifting works out to ₹400-1500 per piece depending on design — affordable per-unit cost with premium impact.\n\n"
            "**Project-Branded Customisation** — Dial features project name, builder logo, and elegant design that integrates the brand without looking too commercial."
        ),
        "customization_content": (
            "Real estate gifting options:\n\n"
            "**Project Logo Dial** — Project name, tagline, and developer logo elegantly placed on dial face.\n\n"
            "**Premium Frame Finishes** — Walnut wood, brushed metal, modern acrylic — matches the project's positioning (luxury, premium, mid-segment).\n\n"
            "**Premium Gift Packaging** — Individual gift boxes with developer branding, personalised welcome card slot.\n\n"
            "**Sizes** — 10 inch (standard), 12 inch (premium), 14 inch (luxury projects with high ticket sizes).\n\n"
            "**Phase-Wise Delivery** — Orders delivered in tranches matching your possession schedule — 100 clocks for Phase 1 handover, next 100 for Phase 2, etc."
        ),
        "case_study_content": (
            "Real estate gifting examples: A major Mumbai developer ordered 800 premium silent sweep clocks for flat handover in a luxury project — premium walnut frame, embossed project logo, individual leather-textured gift boxes. "
            "A Pune township developer ordered 1500 clocks (mid-segment) across multiple phases — branded with township name and tagline, delivered tranche-wise. "
            "A Bangalore tech-corridor builder ordered 600 modern minimalist clocks — acrylic frame, contemporary design matching the project's modern aesthetic. "
            "All projects helped builders achieve excellent customer satisfaction at handover."
        ),
        "meta_keywords": "wall clocks for real estate builders, builder gifting wall clocks, flat owner welcome gift clocks, real estate corporate gifting clocks, project branded wall clocks",
        "display_order": 6,
    },
]


# ========================================================================
# SERVICE PAGES (5 services × 500 words = ~2500 words)
# ========================================================================

SERVICE_DATA = [
    {
        "name": "Bulk Wall Clock Supply",
        "icon_class": "fas fa-boxes-stacked",
        "h1_heading": "Bulk Wall Clock Supply — Wholesale from Manufacturer",
        "hero_subheading": "Wholesale wall clocks for retailers, distributors, corporates and bulk buyers. Direct factory pricing with quantity-based slab discounts.",
        "short_description": "Wholesale bulk wall clock supply with factory-direct pricing, quantity slabs, and PAN India delivery.",
        "full_description": (
            "Bulk wall clock supply is HOOVALE's core business. Whether you need 50 pieces for a small retail order, 500 for a corporate gifting campaign, or 5000+ for a national distribution chain, we have the manufacturing capacity, design range, and logistics network to deliver. "
            "Our bulk supply model is built on three pillars — direct factory pricing (no middleman markups), strict quality control (every piece tested before dispatch), and reliable delivery (PAN India coverage with established transporters).\n\n"
            "Bulk pricing follows transparent slabs: 5-49 pieces (retail wholesale rate), 50-199 (small bulk discount), 200-499 (mid-bulk discount), 500-1999 (large bulk discount), 2000+ (deepest factory rate). "
            "We don't play negotiation games — published slabs apply equally to first-time and repeat customers. Larger orders simply unlock deeper discount tiers automatically."
        ),
        "process_content": (
            "Our bulk supply process: **Step 1: Enquiry** — share your requirement on WhatsApp or phone (designs, quantities, customisation needs). **Step 2: Quotation** — we send detailed pricing within 2 hours including all variants. **Step 3: Sample Approval** — for first orders, we recommend a 5-piece sample order so you can verify quality before bulk commitment. **Step 4: Order Confirmation** — once approved, place full bulk order with 50% advance. **Step 5: Production** — bulk orders typically produce in 7-15 days depending on quantity and customisation. **Step 6: Quality Check** — every piece undergoes 3-stage QC before packing. **Step 7: Dispatch** — packed in protective cartons, dispatched via reliable transporters, tracking provided. **Step 8: Delivery** — door-step delivery in 2-8 days depending on city. **Step 9: Post-Delivery** — 1 year movement warranty, dedicated support for any issues."
        ),
        "benefits_content": (
            "**Best Wholesale Pricing** — Direct factory rates 30-50% below retail markets. **No Hidden Charges** — published slabs are all-inclusive (only GST and freight extra). **Flexible MOQ** — start from 5 pieces for testing, scale to thousands. **Quality Assurance** — 1 year movement warranty on bulk orders too. **PAN India Delivery** — established transporters covering all major cities. **Custom Logo Free** — bulk orders 200+ get free logo printing. **Multiple Designs Per Order** — mix designs in single shipment. **Repeat Order Priority** — verified buyers get faster dispatch and credit terms."
        ),
        "meta_keywords": "bulk wall clock supplier, wholesale wall clocks bulk, bulk wall clock manufacturer, wall clock bulk order, wall clock wholesale price india",
        "display_order": 1,
    },
    {
        "name": "Custom Logo Wall Clocks",
        "icon_class": "fas fa-paint-brush",
        "h1_heading": "Custom Logo Wall Clocks — UV Printing on Bulk Orders",
        "hero_subheading": "Customise wall clocks with your company logo using high-quality UV printing. Free on bulk orders. Mockup approval before production.",
        "short_description": "High-quality UV logo printing on wall clock dials. Single colour or full colour. Free on bulk orders 200+ pieces.",
        "full_description": (
            "Custom logo wall clocks are a powerful branding tool — the logo stays in front of your audience for years, generating continuous brand recall at near-zero ongoing cost. "
            "HOOVALE offers professional UV printing services for company logos, project names, taglines, and full custom dial designs on wall clocks. Our printing uses high-resolution UV technology that produces sharp, fade-resistant logos that remain crisp for 5+ years.\n\n"
            "We handle logos in any format — JPG, PNG, vector files (AI, SVG, EPS preferred for sharpness). Our design team prepares mockups showing exactly how your logo will look on the chosen clock model, and you approve before production starts. This eliminates surprises and ensures the final product matches your expectations."
        ),
        "process_content": (
            "**Step 1: Send Logo** — share your logo file (preferably vector AI/SVG/EPS, or high-res PNG). **Step 2: Design Mockup** — our team creates a mockup showing your logo on the chosen clock dial. Free, usually within 24 hours. **Step 3: Approve / Revise** — you approve the mockup or request changes. We revise until perfect. **Step 4: Production** — UV printing on dials (single colour, full colour, or premium gold/silver foil — your choice). **Step 5: Quality Check** — every printed dial inspected for print sharpness and colour accuracy. **Step 6: Assembly** — printed dials assembled into your chosen clock models. **Step 7: Final QC and Dispatch** — full inspection, packing, dispatch."
        ),
        "benefits_content": (
            "**Sharp UV Printing** — High-resolution prints that don't fade or peel. 5+ year life under normal use. **Multiple Print Options** — single colour, full colour, gold/silver foil, embossed effects. **Free Mockup Service** — see exactly how your logo will look before committing. **Free on Bulk Orders** — 200+ pieces get free logo printing (no extra cost). **Quick Turnaround** — mockup in 24 hours, production in 7-15 days. **Quality Guaranteed** — if any printed piece has print quality issues, we replace free."
        ),
        "meta_keywords": "custom logo wall clocks, customised wall clocks with logo, branded wall clocks manufacturer, company logo wall clocks bulk, uv printed wall clocks",
        "display_order": 2,
    },
    {
        "name": "OEM Manufacturing",
        "icon_class": "fas fa-industry",
        "h1_heading": "OEM Wall Clock Manufacturing — Private Label Production",
        "hero_subheading": "Manufacture wall clocks under your own brand. Private label production with your branding, packaging, and exclusive designs.",
        "short_description": "Private label OEM wall clock manufacturing. Your brand, your packaging, your designs — we produce.",
        "full_description": (
            "OEM (Original Equipment Manufacturing) wall clock services let your brand sell wall clocks without the complexity, capital, and operational headache of running a manufacturing facility. "
            "HOOVALE produces wall clocks under your private label — your brand name on dial, your packaging, your barcode, your exclusive designs (or our designs adapted to your brand). "
            "This service is ideal for retail brands wanting to expand into wall clocks, gift companies launching their own product lines, e-commerce brands building proprietary product catalogues, and corporate brands wanting branded merchandise for retail or gifting.\n\n"
            "OEM partnerships start with a discussion of your brand positioning, target market, and design preferences. We then propose products from our manufacturing capability that suit your brand, develop custom designs if needed, and produce under your label with full IP protection (your designs remain exclusive to you)."
        ),
        "process_content": (
            "**Step 1: OEM Discussion** — initial call to understand your brand, market, designs needed. **Step 2: Product Selection / Design** — choose from our existing catalogue or co-develop custom designs. **Step 3: Sample Development** — we produce samples for your approval. **Step 4: Sample Approval** — you approve final design, materials, packaging. **Step 5: Bulk Production** — manufacturing under your brand label. **Step 6: Quality Control** — full QC on production runs. **Step 7: Packaging** — your branded packaging applied (we can also produce custom packaging). **Step 8: Dispatch** — to your warehouse or fulfillment centre."
        ),
        "benefits_content": (
            "**No Manufacturing Investment** — produce under your brand without owning a factory. **Design Exclusivity** — custom designs stay exclusive to your brand. **Quality Manufacturing** — leverage our 15+ years of clock manufacturing expertise. **Flexible Quantities** — start from MOQ 100 pieces for OEM, scale to thousands. **Custom Packaging** — your brand packaging, your barcode, your retail-ready presentation. **Confidentiality** — strict NDA agreements protect your brand strategy."
        ),
        "meta_keywords": "oem wall clock manufacturer, private label wall clock manufacturing, oem clock manufacturer india, white label wall clocks, contract wall clock manufacturer",
        "display_order": 3,
    },
    {
        "name": "Promotional Wall Clocks",
        "icon_class": "fas fa-bullhorn",
        "h1_heading": "Promotional Wall Clocks — Brand Campaigns & Events",
        "hero_subheading": "Economical promotional wall clocks for brand campaigns, trade show giveaways, distributor incentives, and marketing activations.",
        "short_description": "Cost-effective promotional wall clocks for marketing campaigns, trade shows, dealer incentives, and brand activations.",
        "full_description": (
            "Promotional wall clocks are an evergreen marketing tool — economical per unit, branded with your campaign or product, and useful enough that recipients keep them on their walls for years. "
            "HOOVALE supplies promotional clocks for FMCG product launches, dealer/distributor incentive programs, trade show giveaways, customer loyalty programs, and brand activations.\n\n"
            "Our promotional clock range is engineered for maximum brand impact at minimum per-unit cost. We use efficient designs with full dial branding space, durable but economical materials, and standardised sizes that allow large-scale production. "
            "Per-unit cost can be as low as ₹150-300 for high-volume orders (1000+ pieces), making promotional clocks one of the most cost-effective branded merchandise options."
        ),
        "process_content": (
            "**Step 1: Campaign Brief** — share your campaign details, branding, target quantity, budget. **Step 2: Design Concept** — we propose dial design options matching your campaign. **Step 3: Mockup Approval** — finalise dial design. **Step 4: Sample Production** — physical sample for final approval (optional, 5-10 pieces). **Step 5: Bulk Production** — large-scale production typically 10-15 days. **Step 6: Packaging** — bulk packaging or individual basic boxes. **Step 7: Dispatch** — to your campaign warehouse or event venue."
        ),
        "benefits_content": (
            "**Lowest Per-Unit Cost** — economical models starting from ₹150-300 per piece for high volumes. **Maximum Brand Visibility** — full dial branding with campaign messaging, product images, or brand logos. **Durable Despite Economy** — basic but reliable build, runs accurately for 2+ years. **Quick Turnaround** — promotional orders typically produce and ship in 12-18 days. **Bulk Quantities** — handle orders from 500 to 50,000+ pieces. **Campaign Tracking** — orders timed to launch dates for synchronised distribution."
        ),
        "meta_keywords": "promotional wall clocks, marketing wall clocks bulk, dealer incentive wall clocks, trade show giveaway clocks, brand campaign wall clocks",
        "display_order": 4,
    },
    {
        "name": "Distributor Partnership",
        "icon_class": "fas fa-handshake",
        "h1_heading": "Become a HOOVALE Distributor — City & Regional Partnerships",
        "hero_subheading": "Authorised wall clock distributorship for cities and regions across India. Best margins, exclusive territories, marketing support.",
        "short_description": "Distributor partnerships for cities and regions. Exclusive territories, deep discount tiers, marketing support.",
        "full_description": (
            "HOOVALE is expanding its distributor network across India and offers authorised distributorships for cities, regions, and Tier-2/Tier-3 markets. "
            "If you have an existing trading or wholesale business in clocks, gifts, electronics, or general merchandise — and want to add wall clocks to your portfolio with strong margins and manufacturer backing — distributorship is a high-potential opportunity.\n\n"
            "Our distributor partners enjoy benefits unavailable to regular wholesale buyers: exclusive territory rights (no competing HOOVALE distributors in your assigned territory), deepest discount tiers (better margins than wholesale buyers), priority dispatch on orders, marketing collateral and product images, technical and design support, and inclusion in our 'Find a Distributor' page driving leads to you. "
            "In return, distributors commit to minimum monthly off-take, territory development, and exclusive HOOVALE representation in their assigned area."
        ),
        "process_content": (
            "**Step 1: Initial Enquiry** — submit distributor enquiry with your business details, territory of interest, current business profile. **Step 2: Discussion Call** — discuss territory, projected volumes, terms. **Step 3: Territory Evaluation** — we evaluate territory exclusivity and existing distributor presence. **Step 4: Distributor Agreement** — formal agreement covering terms, margins, exclusivity, off-take commitments. **Step 5: Initial Stock Order** — first stocking order to establish inventory. **Step 6: Marketing Onboarding** — distributor marketing kit, product images, listing on our website. **Step 7: Ongoing Partnership** — monthly off-take, periodic business reviews, growth planning."
        ),
        "benefits_content": (
            "**Exclusive Territory** — no competing HOOVALE distributors in your assigned area. **Deepest Margins** — distributor margins significantly above wholesale rates. **Priority Dispatch** — your orders move first. **Marketing Support** — product images, catalogues, marketing collateral. **Lead Routing** — leads from your territory routed to you. **Credit Terms** — verified distributors get extended credit periods. **Annual Performance Bonuses** — top-performing distributors earn additional incentives. **Long-Term Partnership** — multi-year agreements building stable income."
        ),
        "meta_keywords": "wall clock distributor india, become wall clock distributor, hoovale distributorship, wall clock dealership opportunity, authorised wall clock distributor",
        "display_order": 5,
    },
]


# ========================================================================
# FAQS (20 questions covering all SEO scopes)
# ========================================================================

FAQ_DATA = [
    # Global FAQs (appear everywhere)
    ("global", "Are you a wall clock manufacturer or just a trader?",
     "We are a direct manufacturer based in Jaipur, Rajasthan. We have our own production facility where we assemble quartz movements, print dials, and finish frames. We do NOT trade or resell — every clock we supply is made in our own factory. This is why we can offer factory-direct wholesale pricing without middleman markups."),

    ("global", "What is your minimum order quantity (MOQ)?",
     "Our standard MOQ is 5 pieces for stock designs, allowing first-time buyers to test quality before bulk commitment. For custom logo orders, MOQ is 50 pieces. For OEM private label, MOQ is 100 pieces. Larger quantities unlock progressively deeper wholesale slabs."),

    ("global", "Do you offer custom logo printing on wall clocks?",
     "Yes. We offer high-quality UV printing for company logos, project names, taglines, and full custom dial designs. Free mockup service before production. Logo printing is FREE on bulk orders of 200+ pieces. For smaller orders, nominal printing charges apply."),

    ("global", "What is the delivery time across India?",
     "Delhi/Ahmedabad: 2-4 business days. Mumbai/Pune: 3-5 days. Bangalore/Hyderabad/Chennai: 4-7 days. Kolkata/Northeast: 6-9 days. Tier-2 cities: typically 5-10 days. Custom orders add 7-15 days for production. Air freight available for urgent requirements at premium rates."),

    ("global", "Do you provide GST invoice?",
     "Yes. All orders include proper GST invoice as per current Indian GST laws. We are GST registered. E-way bills are issued for inter-state shipments above ₹50,000. Required documentation provided for B2B procurement compliance."),

    ("global", "What payment methods do you accept?",
     "We accept bank transfer (NEFT, RTGS, IMPS), UPI (PhonePe, Google Pay, Paytm), and cheques. For first orders, we typically require 50% advance with 50% against PI before dispatch. Verified repeat customers get extended credit terms (15-30 days post-delivery)."),

    ("global", "Do you offer warranty on your wall clocks?",
     "Yes. We provide 1-year warranty on movement (the internal mechanism). If a movement fails within 1 year of dispatch, we replace it free of cost — buyer just sends us the faulty piece for verification. Frame and dial issues from manufacturing defects are also covered. Warranty is valid even on bulk wholesale orders."),

    ("global", "Can I visit your Jaipur factory before placing a bulk order?",
     "Absolutely. We welcome serious bulk buyers and distributors to visit our Jaipur factory. You can see our production process, quality control standards, and product range firsthand. Schedule visits in advance via WhatsApp or phone — we'll arrange a guided tour and meeting with our sales/production team."),

    # Product-specific
    ("product", "What is the difference between regular tick and silent sweep movement?",
     "Regular tick (quartz) clocks make a soft 'tick-tock' sound every second — used in offices, classrooms, and most regular environments. Silent sweep clocks have a continuous smooth motion with NO ticking sound — used in bedrooms, hotel guest rooms, hospital wards, libraries, and any space where silence matters. Silent sweep costs ~10-15% more but is essential for noise-sensitive areas."),

    ("product", "What sizes of wall clocks are available?",
     "Standard sizes: 8 inch (small offices, cabins), 10 inch (most popular, classrooms, offices), 12 inch (offices, conference rooms), 14 inch (large halls), 16 inch (lobbies, statement pieces), 18-24 inch (banquet halls, large lobbies). Custom sizes available on request for OEM orders. Most bulk orders specify 10 inch or 12 inch."),

    ("product", "What materials are used in your wall clock frames?",
     "We offer multiple frame materials: ABS plastic (economical, durable, lightweight), wooden (oak, walnut, teak finishes — premium look), brushed metal (silver, gold tones — modern look), acrylic (contemporary minimalist designs), and combo materials. Each material has its strengths — choose based on your end-use environment and budget."),

    # City-specific
    ("city", "Do you supply outside Jaipur?",
     "Yes. We supply across India from our Jaipur manufacturing facility. Major coverage includes Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Pune, Ahmedabad, Kolkata and all Tier-2/Tier-3 cities through established transporters. International orders are also accepted on case-by-case basis."),

    ("city", "How do you ensure timely delivery to my city?",
     "We work with established transporters with proven track records on each major route. Orders are dispatched within 24-48 hours of confirmation, tracking is provided, and we follow up proactively until delivery. Bulk orders include transit insurance to cover any logistics damage."),

    # Industry-specific
    ("industry", "Can you handle large institutional orders like school chains or hospital tenders?",
     "Yes. We regularly handle institutional bulk orders — school chain stocking (1000+ classroom clocks across multiple branches), hospital tender supplies (compliant with government tender documentation requirements), corporate gifting campaigns (5000+ branded pieces), and real estate flat owner gifting (multi-phase deliveries matching possession schedules). Our production capacity supports orders up to 50,000+ pieces."),

    # Contact / general
    ("contact", "What is the best way to get a quote?",
     "WhatsApp is fastest — message us at +91 9462207356 with your requirement (designs, quantity, customisation needs). We respond within 30 minutes during business hours. You can also call us directly or email. We send detailed quotations within 2 hours of enquiry, including pricing slabs and lead times."),

    ("contact", "Do you have a product catalogue I can review?",
     "Yes. We share our digital catalogue via WhatsApp or email — includes 500+ designs across all categories with pricing slabs. The catalogue is updated quarterly with new designs and seasonal collections. Request the catalogue with your enquiry, and we'll send it within hours."),

    ("global", "Can I customise the packaging?",
     "Yes. Standard bulk dispatches use protective corrugated boxes (5-10 pieces per box). Premium gifting orders can use individual gift boxes with our standard branding. Custom branded packaging (your logo on the gift box) available for larger orders, typically 500+ pieces, with additional packaging cost."),

    ("global", "What if I need urgent delivery in 5-7 days?",
     "Stock designs (no customisation) can ship within 24-48 hours. For custom logo orders, we offer expedited production in 7-10 days for an urgency premium. Air freight delivery cuts transport time to 1-3 days at premium cost. Rush requirements are handled on best-effort basis depending on current production load."),

    ("global", "Do you supply outside India?",
     "Yes, on case-by-case basis. We have shipped to GCC countries (UAE, Saudi Arabia, Oman), African countries, and select Southeast Asian markets. International orders require larger MOQs (typically 500+ pieces), proper export documentation, and payment via bank LC or wire transfer. Contact us with international enquiries for specific terms."),

    ("global", "How do I become a distributor in my city?",
     "We are actively expanding our distributor network. If your city doesn't have an existing HOOVALE distributor, you can apply for distributorship by sharing your business profile, projected volumes, and territory of interest. Distributorship comes with exclusive territory, deepest margins, and marketing support. Detailed terms are discussed in a one-on-one call after initial enquiry."),
]


# ========================================================================
# CATEGORIES (14 categories — basic SEO descriptions)
# ========================================================================

CATEGORY_DATA = [
    ("Wooden Wall Clocks", "Premium wooden wall clocks in oak, walnut, teak, and rosewood finishes. Classic and modern wooden designs for homes, offices, hotels."),
    ("Corporate Wall Clocks", "Branded wall clocks for corporate offices, conference rooms, and reception areas. Custom logo printing, premium build, professional designs."),
    ("Promotional Clocks", "Cost-effective promotional wall clocks for brand campaigns, dealer incentives, trade show giveaways. Maximum branding at lowest per-unit cost."),
    ("Digital Wall Clocks", "LED digital wall clocks with date, temperature display options. Suitable for offices, schools, and modern interiors."),
    ("Designer Wall Clocks", "Premium designer wall clocks in contemporary, vintage, modern, and luxury aesthetics. Statement pieces for upmarket spaces."),
    ("Customized Logo Clocks", "Wall clocks with company logo, project name, or full custom dial design. UV-printed for fade-resistant durability."),
    ("Office Wall Clocks", "Functional, durable, and stylish wall clocks for offices, cabins, conference rooms. Wide range of sizes and finishes."),
    ("Hotel Wall Clocks", "Silent sweep wall clocks for hotel guest rooms, lobbies, banquet halls. Designer aesthetics matching hospitality interiors."),
    ("Modern Wall Clocks", "Contemporary modern wall clocks in minimalist designs, suitable for modern homes, offices, and showrooms."),
    ("Luxury Wall Clocks", "Premium luxury wall clocks for high-end interiors, executive offices, and luxury retail. Premium materials, exclusive designs."),
    ("Round Wall Clocks", "Classic round wall clocks in all sizes — 8 inch to 24 inch. Multiple frame materials and dial designs."),
    ("Printed Wall Clocks", "Custom-printed wall clocks with photos, artwork, branding, or thematic designs. UV print technology for sharp results."),
    ("Retail Wall Clocks", "Wholesale wall clocks for retail stores and gift shops. Best wholesale pricing, wide design range, reliable stock availability."),
    ("Bulk Wall Clocks", "Bulk order wall clocks with quantity-based slab discounts. From 50 to 50,000 pieces. Direct factory pricing."),
]


# ========================================================================
# TESTIMONIALS (sample testimonials for credibility)
# ========================================================================

TESTIMONIAL_DATA = [
    ("Rajesh Kumar", "Purchase Manager", "Delhi", 5, "Bulk Order — 500 pieces",
     "We've been ordering from HOOVALE for 3 years. Quality is consistently excellent, delivery is always on time, and pricing is the best in the market. Highly recommended for bulk wholesale buyers."),
    ("Priya Sharma", "Marketing Head, IT Company", "Bangalore", 5, "Corporate Gifting",
     "Ordered 800 branded clocks for our employee 5-year anniversary gifting. Custom logo printing was crisp, packaging was premium, and our employees loved the gifts. Will definitely reorder for next campaign."),
    ("Mohammed Iqbal", "Hotel Group Procurement", "Mumbai", 5, "Hotel Bulk Order",
     "Sourced silent sweep clocks for 4 properties (250+ rooms). The non-tick movement is exactly what we needed for guest rooms. Quality is hospitality-grade and pricing was very competitive."),
    ("Suresh Patel", "Distributor", "Ahmedabad", 5, "Wholesale Distribution",
     "Best wholesale wall clock supplier in the market. Direct factory pricing, transparent slabs, no negotiation hassles. We distribute across Gujarat and HOOVALE has been our preferred manufacturer for 5+ years."),
    ("Anita Desai", "Real Estate Developer", "Pune", 5, "Builder Gifting",
     "Ordered 600 designer clocks as flat owner welcome gifts for our luxury project. The premium walnut frame, embossed project logo, and individual gift packaging exceeded our expectations. Got tremendous positive feedback from home buyers."),
    ("Vikram Singh", "School Director", "Jaipur", 5, "Educational Bulk",
     "Procured 250 classroom clocks for our school chain expansion. Standardised quality across all branches, fair pricing, and prompt delivery before academic session start. Perfect partner for educational institute requirements."),
]


# ========================================================================
# COMMAND CLASS
# ========================================================================

class Command(BaseCommand):
    help = 'Seeds HOOVALE database with city pages, industry pages, services, FAQs, and categories'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing seed data first')
        parser.add_argument('--cities-only', action='store_true', help='Only seed city pages')
        parser.add_argument('--industries-only', action='store_true', help='Only seed industry pages')
        parser.add_argument('--faqs-only', action='store_true', help='Only seed FAQs')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 HOOVALE SEO Content Seeder Starting...\n'))

        # Ensure SiteSettings exists
        SiteSettings.load()
        self.stdout.write(self.style.SUCCESS('✅ Site Settings ensured'))

        if options['cities_only']:
            self._seed_cities(options['clear'])
        elif options['industries_only']:
            self._seed_industries(options['clear'])
        elif options['faqs_only']:
            self._seed_faqs(options['clear'])
        else:
            # Seed everything
            self._seed_categories(options['clear'])
            self._seed_cities(options['clear'])
            self._seed_industries(options['clear'])
            self._seed_services(options['clear'])
            self._seed_faqs(options['clear'])
            self._seed_testimonials(options['clear'])

        self.stdout.write(self.style.SUCCESS('\n🎉 SEO content seeding complete!'))
        self.stdout.write(self.style.WARNING('Next: Visit /admin/ to review and customize seeded content.'))

    def _seed_cities(self, clear=False):
        if clear:
            CityPage.objects.all().delete()
            self.stdout.write(self.style.WARNING('   🗑️  Cleared existing CityPages'))

        created_count = 0
        for data in CITY_DATA:
            obj, created = CityPage.objects.update_or_create(
                city_name=data['city_name'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"   ✅ Created CityPage: {obj.city_name}")
            else:
                self.stdout.write(f"   🔄 Updated CityPage: {obj.city_name}")
        self.stdout.write(self.style.SUCCESS(f'✅ {created_count} cities created, {len(CITY_DATA) - created_count} updated\n'))

    def _seed_industries(self, clear=False):
        if clear:
            IndustryPage.objects.all().delete()
            self.stdout.write(self.style.WARNING('   🗑️  Cleared existing IndustryPages'))

        created_count = 0
        for data in INDUSTRY_DATA:
            obj, created = IndustryPage.objects.update_or_create(
                industry_name=data['industry_name'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"   ✅ Created Industry: {obj.industry_name}")
            else:
                self.stdout.write(f"   🔄 Updated Industry: {obj.industry_name}")
        self.stdout.write(self.style.SUCCESS(f'✅ {created_count} industries created, {len(INDUSTRY_DATA) - created_count} updated\n'))

    def _seed_services(self, clear=False):
        if clear:
            ServicePage.objects.all().delete()
            self.stdout.write(self.style.WARNING('   🗑️  Cleared existing ServicePages'))

        created_count = 0
        for data in SERVICE_DATA:
            obj, created = ServicePage.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f"   ✅ Created Service: {obj.name}")
            else:
                self.stdout.write(f"   🔄 Updated Service: {obj.name}")
        self.stdout.write(self.style.SUCCESS(f'✅ {created_count} services created, {len(SERVICE_DATA) - created_count} updated\n'))

    def _seed_faqs(self, clear=False):
        if clear:
            FAQ.objects.all().delete()
            self.stdout.write(self.style.WARNING('   🗑️  Cleared existing FAQs'))

        for i, (scope, q, a) in enumerate(FAQ_DATA):
            FAQ.objects.update_or_create(
                question=q,
                defaults={'scope': scope, 'answer': a, 'display_order': i, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(FAQ_DATA)} FAQs seeded\n'))

    def _seed_categories(self, clear=False):
        for i, (name, desc) in enumerate(CATEGORY_DATA):
            Category.objects.update_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'meta_description': desc[:155],
                    'display_order': i,
                    'is_featured': i < 6,  # First 6 are featured on homepage
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(CATEGORY_DATA)} categories seeded\n'))

    def _seed_testimonials(self, clear=False):
        if clear:
            Testimonial.objects.all().delete()

        for i, (name, designation, city, rating, title, content) in enumerate(TESTIMONIAL_DATA):
            Testimonial.objects.update_or_create(
                customer_name=name,
                review_content=content,
                defaults={
                    'customer_designation': designation,
                    'customer_city': city,
                    'rating': rating,
                    'review_title': title,
                    'is_featured': True,
                    'display_order': i,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(TESTIMONIAL_DATA)} testimonials seeded\n'))
