#!/usr/bin/env python3
"""
Test script for PTT API
"""

import requests
import json

BASE_URL = "http://localhost:12000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_parse_single():
    """Test single parse endpoint"""
    print("Testing single parse endpoint...")
    title = "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole"
    response = requests.get(f"{BASE_URL}/parse", params={"title": title})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_parse_simple():
    """Test simple parse endpoint"""
    print("Testing simple parse endpoint...")
    title = "The.Walking.Dead.S06E07.SUBFRENCH.HDTV.x264-AMB3R.mkv"
    response = requests.get(f"{BASE_URL}/parse-simple", params={
        "title": title,
        "translate_languages": True
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_batch_parse():
    """Test batch parse endpoint"""
    print("Testing batch parse endpoint...")
    data = {
        "titles": [
            "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole",
            "Game.of.Thrones.S08E06.The.Iron.Throne.1080p.AMZN.WEB-DL.DDP5.1.H.264-GoT",
            "Avengers.Endgame.2019.2160p.UHD.BluRay.x265.HDR.Atmos-TERMINAL"
        ],
        "translate_languages": False
    }
    response = requests.post(f"{BASE_URL}/parse-batch", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_examples():
    """Test examples endpoint"""
    print("Testing examples endpoint...")
    response = requests.get(f"{BASE_URL}/examples")
    print(f"Status: {response.status_code}")
    print(f"Number of examples: {len(response.json()['examples'])}")
    print()

if __name__ == "__main__":
    print("PTT API Test Suite")
    print("=" * 50)
    
    try:
        test_health()
        test_parse_single()
        test_parse_simple()
        test_batch_parse()
        test_examples()
        print("All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on http://localhost:12000")
    except Exception as e:
        print(f"Error: {e}")