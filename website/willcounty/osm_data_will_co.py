#!/usr/bin/env python3
"""
OpenStreetMap Data Extraction
This script extracts grocery stores, pharmacies, schools, transit stops, parks, and health centers
"""

import time

import pandas as pd
import requests


class OSMDataExtractor:
    def __init__(self, overpass_url: str = "http://overpass-api.de/api/interpreter"):
        self.overpass_url = overpass_url
        self.session = requests.Session()

    def build_overpass_query(
        self, bbox: tuple[float, float, float, float], amenity_types: list[str], timeout: int = 25
    ) -> str:
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"

        amenity_filters = ""
        for amenity in amenity_types:
            amenity_filters += f'  node["amenity"="{amenity}"]({bbox_str});\n'
            amenity_filters += f'  way["amenity"="{amenity}"]({bbox_str});\n'
            amenity_filters += f'  relation["amenity"="{amenity}"]({bbox_str});\n'

        query = f"""
        [out:json][timeout:{timeout}];
        (
        {amenity_filters}
        );
        out center;
        """
        return query

    def build_transit_query(
        self, bbox: tuple[float, float, float, float], timeout: int = 25
    ) -> str:
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"

        query = f"""
        [out:json][timeout:{timeout}];
        (
          node["highway"="bus_stop"]({bbox_str});
          node["public_transport"="stop_position"]({bbox_str});
          node["public_transport"="platform"]({bbox_str});
          node["railway"="tram_stop"]({bbox_str});
          node["railway"="station"]({bbox_str});
          node["railway"="subway_entrance"]({bbox_str});
          way["highway"="bus_stop"]({bbox_str});
          way["public_transport"="stop_position"]({bbox_str});
          way["public_transport"="platform"]({bbox_str});
          way["railway"="tram_stop"]({bbox_str});
          way["railway"="station"]({bbox_str});
        );
        out center;
        """
        return query

    def build_parks_query(self, bbox: tuple[float, float, float, float], timeout: int = 25) -> str:
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"

        query = f"""
        [out:json][timeout:{timeout}];
        (
          node["leisure"="park"]({bbox_str});
          node["leisure"="garden"]({bbox_str});
          node["leisure"="playground"]({bbox_str});
          node["leisure"="nature_reserve"]({bbox_str});
          way["leisure"="park"]({bbox_str});
          way["leisure"="garden"]({bbox_str});
          way["leisure"="playground"]({bbox_str});
          way["leisure"="nature_reserve"]({bbox_str});
          relation["leisure"="park"]({bbox_str});
          relation["leisure"="garden"]({bbox_str});
          relation["leisure"="nature_reserve"]({bbox_str});
        );
        out center;
        """
        return query

    def execute_query(self, query: str, max_retries: int = 3, delay: float = 1.0) -> dict | None:
        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    self.overpass_url,
                    data=query,
                    timeout=30,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2**attempt))
                else:
                    print(f"Failed to execute query after {max_retries} attempts")
                    return None

    def parse_osm_data(self, data: dict, category: str) -> list[dict]:
        features = []

        for element in data.get("elements", []):
            feature = {
                "id": element.get("id"),
                "type": element.get("type"),
                "category": category,
                "name": element.get("tags", {}).get("name", ""),
                "amenity": element.get("tags", {}).get("amenity", ""),
                "shop": element.get("tags", {}).get("shop", ""),
                "leisure": element.get("tags", {}).get("leisure", ""),
                "highway": element.get("tags", {}).get("highway", ""),
                "railway": element.get("tags", {}).get("railway", ""),
                "public_transport": element.get("tags", {}).get("public_transport", ""),
                "addr_street": element.get("tags", {}).get("addr:street", ""),
                "addr_housenumber": element.get("tags", {}).get("addr:housenumber", ""),
                "addr_city": element.get("tags", {}).get("addr:city", ""),
                "phone": element.get("tags", {}).get("phone", ""),
                "website": element.get("tags", {}).get("website", ""),
                "opening_hours": element.get("tags", {}).get("opening_hours", ""),
            }

            # Handle coordinates
            if element["type"] == "node":
                feature["lat"] = element.get("lat")
                feature["lon"] = element.get("lon")
            elif "center" in element:
                feature["lat"] = element["center"].get("lat")
                feature["lon"] = element["center"].get("lon")
            else:
                feature["lat"] = None
                feature["lon"] = None

            features.append(feature)

        return features

    def get_amenities_data(self, bbox: tuple[float, float, float, float]) -> pd.DataFrame:
        """Get comprehensive amenities data including shops and amenities"""
        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"

        # Comprehensive query that includes both shop and amenity tags
        query = f"""
        [out:json][timeout:25];
        (
          // Grocery stores and supermarkets (shop tags)
          node["shop"="supermarket"]({bbox_str});
          way["shop"="supermarket"]({bbox_str});
          relation["shop"="supermarket"]({bbox_str});
          node["shop"="grocery"]({bbox_str});
          way["shop"="grocery"]({bbox_str});
          relation["shop"="grocery"]({bbox_str});
          node["shop"="convenience"]({bbox_str});
          way["shop"="convenience"]({bbox_str});
          relation["shop"="convenience"]({bbox_str});
          node["shop"="greengrocer"]({bbox_str});
          way["shop"="greengrocer"]({bbox_str});
          node["shop"="deli"]({bbox_str});
          way["shop"="deli"]({bbox_str});
          node["shop"="butcher"]({bbox_str});
          way["shop"="butcher"]({bbox_str});
          node["shop"="bakery"]({bbox_str});
          way["shop"="bakery"]({bbox_str});
          
          // Pharmacies (both shop and amenity tags)
          node["amenity"="pharmacy"]({bbox_str});
          way["amenity"="pharmacy"]({bbox_str});
          relation["amenity"="pharmacy"]({bbox_str});
          node["shop"="pharmacy"]({bbox_str});
          way["shop"="pharmacy"]({bbox_str});
          
          // Schools (amenity tags)
          node["amenity"="school"]({bbox_str});
          way["amenity"="school"]({bbox_str});
          relation["amenity"="school"]({bbox_str});
          node["amenity"="university"]({bbox_str});
          way["amenity"="university"]({bbox_str});
          relation["amenity"="university"]({bbox_str});
          node["amenity"="college"]({bbox_str});
          way["amenity"="college"]({bbox_str});
          relation["amenity"="college"]({bbox_str});
          node["amenity"="kindergarten"]({bbox_str});
          way["amenity"="kindergarten"]({bbox_str});
          
          // Health centers (amenity tags)
          node["amenity"="hospital"]({bbox_str});
          way["amenity"="hospital"]({bbox_str});
          relation["amenity"="hospital"]({bbox_str});
          node["amenity"="clinic"]({bbox_str});
          way["amenity"="clinic"]({bbox_str});
          relation["amenity"="clinic"]({bbox_str});
          node["amenity"="doctors"]({bbox_str});
          way["amenity"="doctors"]({bbox_str});
          node["amenity"="dentist"]({bbox_str});
          way["amenity"="dentist"]({bbox_str});
          node["amenity"="veterinary"]({bbox_str});
          way["amenity"="veterinary"]({bbox_str});
        );
        out center;
        """

        print("Fetching amenities data (including shops)...")

        data = self.execute_query(query)
        if not data:
            return pd.DataFrame()

        features = self.parse_osm_data(data, "amenities")
        return pd.DataFrame(features)

    def get_transit_data(self, bbox: tuple[float, float, float, float]) -> pd.DataFrame:
        query = self.build_transit_query(bbox)
        print("Fetching transit data...")

        data = self.execute_query(query)
        if not data:
            return pd.DataFrame()

        features = self.parse_osm_data(data, "transit")
        return pd.DataFrame(features)

    def get_parks_data(self, bbox: tuple[float, float, float, float]) -> pd.DataFrame:
        query = self.build_parks_query(bbox)
        print("Fetching parks data...")

        data = self.execute_query(query)
        if not data:
            return pd.DataFrame()

        features = self.parse_osm_data(data, "parks")
        return pd.DataFrame(features)

    def get_all_data(self, bbox: tuple[float, float, float, float]) -> dict[str, pd.DataFrame]:
        results = {}

        results["amenities"] = self.get_amenities_data(bbox)
        time.sleep(1)

        results["transit"] = self.get_transit_data(bbox)
        time.sleep(1)

        results["parks"] = self.get_parks_data(bbox)

        return results

    def save_data(self, data: dict[str, pd.DataFrame], output_dir: str = "."):
        import os

        os.makedirs(output_dir, exist_ok=True)

        for category, df in data.items():
            if not df.empty:
                filename = os.path.join(output_dir, f"will_county_{category}.csv") # change here
                df.to_csv(filename, index=False)
                print(f"✅ Saved {len(df)} {category} records to {filename}")
            else:
                print(f"⚠️  No data found for {category}")


def main():
    """Main function to extract Area of Interest data"""
    print("🎯 Starting Data Extraction")
    print("=" * 60)

    # Initialize extractor
    extractor = OSMDataExtractor()

    # Area of interest bounding box (south, west, north, east)
    aoi_bbox = (41.2, -88.27, 41.74, -87.52)

    print("📍 Area of interest: Will County") # add feature to update name
    print(f"📏 Bounding box: {aoi_bbox}")
    print("📐 Approximate area: ~226 square miles") # replace/calculate?
    print()

    try:
        # Extract all data
        print("🔄 Starting data extraction...")
        start_time = time.time()

        all_data = extractor.get_all_data(aoi_bbox)

        extraction_time = time.time() - start_time
        print(f"⏱️  Extraction completed in {extraction_time:.1f} seconds")
        print()

        # Print detailed summary
        print("📊 EXTRACTION SUMMARY")
        print("-" * 40)

        total_records = 0
        for category, df in all_data.items():
            count = len(df)
            total_records += count
            print(f"{category.capitalize():<12}: {count:>6} records")

            if not df.empty and count > 0:
                # Show breakdown by type
                if category == "amenities":
                    amenity_breakdown = df["amenity"].value_counts().head(5)
                    for amenity, count in amenity_breakdown.items():
                        print(f"  └─ {amenity:<10}: {count:>4}")

                # Show sample names
                sample_names = df["name"].dropna().head(3).tolist()
                if sample_names:
                    print(f"  └─ Examples: {', '.join(sample_names)}")

        print(f"{'Total':<12}: {total_records:>6} records")
        print()

        # Save to files
        print("💾 Saving data to CSV files...")
        extractor.save_data(all_data, "will_county_data") #change name as needed
        print()

        # Additional analysis
        if not all_data["amenities"].empty:
            amenities_df = all_data["amenities"]

            print("🏪 AMENITY BREAKDOWN")
            print("-" * 30)

            # Show both amenity and shop breakdowns
            amenity_counts = amenities_df["amenity"].value_counts()
            shop_counts = amenities_df["shop"].value_counts()

            print("By amenity tag:")
            for amenity, count in amenity_counts.items():
                if amenity:  # Only show non-empty values
                    print(f"  {amenity:<15}: {count:>3}")

            print("\nBy shop tag:")
            for shop, count in shop_counts.items():
                if shop:  # Only show non-empty values
                    print(f"  {shop:<15}: {count:>3}")

            # Show grocery-specific breakdown
            grocery_related = amenities_df[
                (
                    amenities_df["shop"].isin(
                        [
                            "supermarket",
                            "grocery",
                            "convenience",
                            "greengrocer",
                            "deli",
                            "bakery",
                            "butcher",
                        ]
                    )
                )
                | (amenities_df["amenity"].isin(["supermarket", "grocery", "convenience"]))
            ]

            if not grocery_related.empty:
                print(f"\n🛒 GROCERY STORES FOUND: {len(grocery_related)}")
                for _, store in grocery_related.head(10).iterrows():
                    store_type = store["shop"] if store["shop"] else store["amenity"]
                    name = store["name"] if store["name"] else "Unnamed"
                    print(f"  └─ {name} ({store_type})")
            print()

        print("✅ Will County data extraction completed successfully!") # change name as needed
        print("📁 Files saved in './will_county_data/' directory") # change name as needed

    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
