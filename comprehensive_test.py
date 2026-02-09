#!/usr/bin/env python3
"""
Comprehensive test script for Aquamitra chatbot
Tests all major question categories
"""

import requests
import json
import time
from typing import Dict, List

BASE_URL = "http://localhost:8000/api/chat"

# Test categories with questions
TEST_CATEGORIES = {
    "1. Basic State & Status Filtering": [
        "Show me areas in Madhya Pradesh where groundwater is being sustainably managed",
        "How many safe areas are there?",
        "Which districts in Rajasthan have over-exploited groundwater?",
        "List all safe areas in Bihar",
    ],
    "2. Numerical Aggregations": [
        "What is the average rainfall in Madhya Pradesh?",
        "What is the total groundwater used in Bihar?",
        "How many total records are in the database?",
        "Which area has the highest rainfall?",
        "Which area has the lowest rainfall?",
    ],
    "3. Comparisons & Filtering": [
        "Which areas use more groundwater than they refill?",
        "Which areas have rainfall above 1500mm?",
        "Show me districts with groundwater usage above 5000",
    ],
    "4. Top/Bottom Queries": [
        "Show me top 5 districts with highest groundwater usage",
        "List top 10 areas with highest rainfall",
        "Show me bottom 5 districts with lowest rainfall",
    ],
    "5. Percentage & Ratio Calculations": [
        "What percentage of land is irrigated in Bihar?",
        "Show areas where usage is more than 80% of refill",
    ],
    "6. Year-Based Queries": [
        "What is the average rainfall in Madhya Pradesh in 2023?",
        "Show me all safe areas in 2024",
        "Count safe areas for each year",
    ],
    "7. Grouped Aggregations": [
        "Count how many areas are over-exploited in each state",
        "Show average rainfall for each state",
        "Count areas by groundwater status",
    ],
    "8. Complex Multi-Condition": [
        "Show safe areas in Madhya Pradesh with rainfall above 1000mm",
        "Which critical areas in Rajasthan have low rainfall?",
    ],
}

def test_query(question: str, delay: float = 2.0) -> Dict:
    """Test a single query"""
    try:
        response = requests.post(
            BASE_URL,
            json={"messages": [{"role": "user", "content": question}], "language": "en"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        time.sleep(delay)  # Rate limiting
        return {
            "success": True,
            "response": data.get("response", ""),
            "sql_query": data.get("sql_query", ""),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "response": "",
            "sql_query": "",
            "error": str(e)
        }

def main():
    print("=" * 80)
    print("COMPREHENSIVE AQUAMITRA CHATBOT TEST")
    print("=" * 80)
    
    total_tests = sum(len(questions) for questions in TEST_CATEGORIES.values())
    passed = 0
    failed = 0
    results = []
    
    for category, questions in TEST_CATEGORIES.items():
        print(f"\n{'=' * 80}")
        print(f"{category}")
        print(f"{'=' * 80}")
        
        for i, question in enumerate(questions, 1):
            print(f"\n[Test {i}/{len(questions)}] {question}")
            result = test_query(question)
            
            if result["success"]:
                passed += 1
                status = "✅ PASS"
                print(f"{status}")
                print(f"Response: {result['response'][:200]}...")
                print(f"SQL: {result['sql_query']}")
            else:
                failed += 1
                status = "❌ FAIL"
                print(f"{status}")
                print(f"Error: {result['error']}")
            
            results.append({
                "category": category,
                "question": question,
                "status": status,
                "result": result
            })
    
    # Summary
    print(f"\n{'=' * 80}")
    print("TEST SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total_tests)*100:.1f}%")
    
    # Save detailed results
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to test_results.json")

if __name__ == "__main__":
    main()

