import random

class AIShoppingAssistant:
    def __init__(self):
        self.sources = ["Amazon", "eBay", "Walmart", "Independent Retailers"]
        self.filters = {}
        self.purchase_history = {}
        self.preferences = {}
        self.excluded_brands = {}

    def search_products(self, query, user_id):
        results = self.fetch_from_sources(query)
        results = self.remove_sponsored(results)  # Exclude sponsored results
        randomized_results = self.randomize_results(results)
        return self.apply_filters(randomized_results, user_id)

    def fetch_from_sources(self, query):
        # Simulating product retrieval from multiple sources
        products = [
            {"name": "Product A", "price": 20, "quality": "High", "convenience": "Fast Shipping", "source": "Amazon", "brand": "BrandX", "sponsored": True},
            {"name": "Product B", "price": 18, "quality": "Medium", "convenience": "Local Pickup", "source": "eBay", "brand": "BrandY", "sponsored": False},
            {"name": "Product C", "price": 22, "quality": "High", "convenience": "Standard Shipping", "source": "Walmart", "brand": "BrandZ", "sponsored": False},
            {"name": "Product D", "price": 19, "quality": "Low", "convenience": "Independent Seller", "source": "Independent", "brand": "BrandA", "sponsored": True},
        ]
        return [p for p in products if query.lower() in p["name"].lower()]

    def remove_sponsored(self, results):
        return [p for p in results if not p.get("sponsored", False)]  # Exclude sponsored products

    def randomize_results(self, results):
        random.shuffle(results)
        return results

    def set_filter(self, user_id, key, value):
        if user_id not in self.preferences:
            self.preferences[user_id] = {}
        self.preferences[user_id][key] = value

    def exclude_brand_or_retailer(self, user_id, exclusion):
        if user_id not in self.excluded_brands:
            self.excluded_brands[user_id] = []
        self.excluded_brands[user_id].append(exclusion)

    def apply_filters(self, results, user_id):
        if user_id in self.preferences:
            for key, value in self.preferences[user_id].items():
                results = [p for p in results if p.get(key) == value]
        if user_id in self.excluded_brands:
            results = [p for p in results if p["brand"] not in self.excluded_brands[user_id] and p["source"] not in self.excluded_brands[user_id]]
        return results

    def record_purchase(self, user_id, product):
        if user_id not in self.purchase_history:
            self.purchase_history[user_id] = []
        self.purchase_history[user_id].append(product)
        print(f"Recorded purchase: {product['name']} for user {user_id}")

    def chatbot_interface(self):
        print("Welcome to the AI Shopping Assistant! (Text-based only)")
        user_id = input("Enter your user ID: ")
        print("What do you prioritize when shopping?")
        preference = input("Choose: price, quality, or convenience: ").lower()
        if preference in ["price", "quality", "convenience"]:
            self.set_filter(user_id, preference, "High" if preference == "quality" else "Fast Shipping" if preference == "convenience" else None)

        exclude_choice = input("Would you like to exclude any brands or retailers? (yes/no): ").lower()
        if exclude_choice == "yes":
            exclusion = input("Enter the brand or retailer name to exclude: ")
            self.exclude_brand_or_retailer(user_id, exclusion)

        while True:
            user_input = input("What product are you looking for? (Type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            results = self.search_products(user_input, user_id)
            if results:
                print("Here are some product options based on your preference:")
                for idx, product in enumerate(results, start=1):
                    print(f"{idx}. {product['name']} from {product['source']} for ${product['price']} - Quality: {product['quality']}, Convenience: {product['convenience']}, Brand: {product['brand']}")
                purchase_choice = input("Enter the number of the product you purchased, or 'n' to skip: ")
                if purchase_choice.isdigit():
                    purchase_choice = int(purchase_choice) - 1
                    if 0 <= purchase_choice < len(results):
                        self.record_purchase(user_id, results[purchase_choice])
            else:
                print("No matching products found.")

assistant = AIShoppingAssistant()
assistant.chatbot_interface() 