#!/usr/bin/env python3
"""
Script to add state column to groundwater CSV files.
Maps district/place names to their respective Indian states.
"""

import csv
import os
from pathlib import Path
from comprehensive_district_mapping import COMPREHENSIVE_MAPPING

# Use the comprehensive mapping
DISTRICT_STATE_MAPPING = COMPREHENSIVE_MAPPING


def get_state_for_place(place_name):
    """
    Get the state for a given place name.
    Returns the state name or 'Unknown' if not found.
    """
    place_lower = place_name.lower().strip()
    
    # Direct lookup
    if place_lower in DISTRICT_STATE_MAPPING:
        return DISTRICT_STATE_MAPPING[place_lower]
    
    # Partial match (for places with suffixes like "urban", "rural", etc.)
    for district, state in DISTRICT_STATE_MAPPING.items():
        if district in place_lower or place_lower in district:
            return state
    
    return 'Unknown'


def add_state_column_to_csv(input_file, output_file):
    """
    Read CSV, add state column, and write to output file.
    """
    print(f"\n📄 Processing: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['state']
        
        rows = []
        unknown_places = set()
        state_counts = {}
        
        for row in reader:
            place = row['place']
            state = get_state_for_place(place)
            row['state'] = state
            rows.append(row)
            
            if state == 'Unknown':
                unknown_places.add(place)
            
            state_counts[state] = state_counts.get(state, 0) + 1
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Written to: {output_file}")
    print(f"   Total rows: {len(rows)}")
    print(f"   States found: {len([s for s in state_counts if s != 'Unknown'])}")
    print(f"   Unknown places: {len(unknown_places)}")
    
    if unknown_places:
        print(f"\n⚠️  Unknown places (first 10): {list(unknown_places)[:10]}")
    
    print(f"\n📊 State distribution:")
    for state, count in sorted(state_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {state}: {count}")
    
    return unknown_places


def main():
    """Main function to process all CSV files."""
    print("=" * 80)
    print("ADDING STATE COLUMN TO GROUNDWATER CSV FILES")
    print("=" * 80)
    
    data_dir = Path("data/ingres")
    csv_files = list(data_dir.glob("groundwater_*.csv"))
    
    if not csv_files:
        print("❌ No CSV files found in data/ingres/")
        return
    
    all_unknown = set()
    
    for csv_file in sorted(csv_files):
        output_file = csv_file.parent / f"{csv_file.stem}_with_state.csv"
        unknown = add_state_column_to_csv(csv_file, output_file)
        all_unknown.update(unknown)
    
    if all_unknown:
        print("\n" + "=" * 80)
        print(f"⚠️  TOTAL UNKNOWN PLACES: {len(all_unknown)}")
        print("=" * 80)
        print("These places need manual mapping. First 20:")
        for i, place in enumerate(list(all_unknown)[:20], 1):
            print(f"  {i}. {place}")
    
    print("\n" + "=" * 80)
    print("✅ DONE! New files created with '_with_state' suffix")
    print("=" * 80)


if __name__ == "__main__":
    main()

