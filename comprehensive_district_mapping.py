#!/usr/bin/env python3
"""
Comprehensive district to state mapping for all Indian states.
This includes districts, tehsils, and major cities.
"""

# Comprehensive mapping of Indian districts/places to states
COMPREHENSIVE_MAPPING = {
    # Andhra Pradesh
    'abdullapurmet': 'Andhra Pradesh', 'achampet': 'Andhra Pradesh', 'achampeta': 'Andhra Pradesh',
    'achanta': 'Andhra Pradesh', 'addagudur': 'Andhra Pradesh', 'addakal': 'Andhra Pradesh',
    'addanki': 'Andhra Pradesh', 'addateegala': 'Andhra Pradesh', 'adavi devula palli': 'Andhra Pradesh',
    'agiripalle': 'Andhra Pradesh', 'ainavilli': 'Andhra Pradesh', 'akiveedu': 'Andhra Pradesh',
    'akkannapeta': 'Andhra Pradesh', 'alair': 'Andhra Pradesh', 'alamuru': 'Andhra Pradesh',
    'anantapur': 'Andhra Pradesh', 'chittoor': 'Andhra Pradesh', 'east godavari': 'Andhra Pradesh',
    'guntur': 'Andhra Pradesh', 'krishna': 'Andhra Pradesh', 'kurnool': 'Andhra Pradesh',
    'nellore': 'Andhra Pradesh', 'prakasam': 'Andhra Pradesh', 'srikakulam': 'Andhra Pradesh',
    'visakhapatnam': 'Andhra Pradesh', 'vizianagaram': 'Andhra Pradesh', 'west godavari': 'Andhra Pradesh',
    'kadapa': 'Andhra Pradesh', 'adoni': 'Andhra Pradesh', 'gudur': 'Andhra Pradesh',
    'nandigama': 'Andhra Pradesh', 'munipalli': 'Andhra Pradesh',
    
    # Arunachal Pradesh
    'aalo east': 'Arunachal Pradesh', 'aalo west': 'Arunachal Pradesh',
    
    # Assam
    'bihpuria': 'Assam', 'golaghat south': 'Assam', 'ghilamara': 'Assam',
    'kamrup': 'Assam', 'nagaon': 'Assam', 'sonitpur': 'Assam', 'dibrugarh': 'Assam',
    'tinsukia': 'Assam', 'cachar': 'Assam', 'barpeta': 'Assam', 'dhubri': 'Assam',
    
    # Bihar
    'banmankhi': 'Bihar', 'majhiaon': 'Bihar', 'narhat': 'Bihar', 'mehdawal': 'Bihar',
    'khizrabad': 'Bihar', 'barachatty': 'Bihar', 'abhauli': 'Bihar', 'adhaura': 'Bihar',
    'agauta': 'Bihar', 'agiaon': 'Bihar', 'ahiraula': 'Bihar', 'ahirori': 'Bihar',
    'ailia': 'Bihar', 'ajitmal': 'Bihar', 'akbarpur': 'Bihar', 'akorhigola': 'Bihar',
    'alampur jafarabad': 'Bihar', 'alauli': 'Bihar', 'aliganj': 'Bihar',
    'patna': 'Bihar', 'gaya': 'Bihar', 'bhagalpur': 'Bihar', 'muzaffarpur': 'Bihar',
    'darbhanga': 'Bihar', 'purnia': 'Bihar', 'araria': 'Bihar', 'kishanganj': 'Bihar',
    
    # Chhattisgarh
    'abhanpur': 'Chhattisgarh', 'akaltara': 'Chhattisgarh',
    'bhopalpattnam': 'Chhattisgarh', 'bijapur': 'Chhattisgarh', 'dantewada': 'Chhattisgarh',
    'raipur': 'Chhattisgarh', 'bilaspur': 'Chhattisgarh', 'durg': 'Chhattisgarh',
    'korba': 'Chhattisgarh', 'rajnandgaon': 'Chhattisgarh', 'raigarh': 'Chhattisgarh',
    
    # Gujarat
    'abdasa': 'Gujarat', 'ahmedabad city & das': 'Gujarat', 'ahmedabad urban': 'Gujarat',
    'ahwa': 'Gujarat', 'ajara': 'Gujarat', 'akkalkuva': 'Gujarat', 'amod': 'Gujarat',
    'porbandar': 'Gujarat', 'surat': 'Gujarat', 'vadodara': 'Gujarat', 'rajkot': 'Gujarat',
    'bhavnagar': 'Gujarat', 'jamnagar': 'Gujarat', 'junagadh': 'Gujarat', 'gandhinagar': 'Gujarat',
    'kakwan': 'Gujarat', 'harij': 'Gujarat',
    
    # Haryana
    'bawani khera': 'Haryana', 'uchana': 'Haryana', 'abohar': 'Haryana',
    'adampur': 'Haryana', 'agroha': 'Haryana', 'akhand nagar': 'Haryana',
    'faridabad': 'Haryana', 'gurgaon': 'Haryana', 'rohtak': 'Haryana', 'hisar': 'Haryana',
    'panipat': 'Haryana', 'karnal': 'Haryana', 'sonipat': 'Haryana', 'yamunanagar': 'Haryana',
    
    # Jharkhand
    'adityapur (gamharia)': 'Jharkhand', 'albert ekka': 'Jharkhand',
    'ranchi': 'Jharkhand', 'jamshedpur': 'Jharkhand', 'dhanbad': 'Jharkhand', 'bokaro': 'Jharkhand',
    'deoghar': 'Jharkhand', 'hazaribagh': 'Jharkhand', 'giridih': 'Jharkhand',
    
    # Karnataka
    'abdasa': 'Karnataka', 'achhalda': 'Karnataka', 'afzalpur': 'Karnataka',
    'agali': 'Karnataka', 'ajjampura': 'Karnataka', 'akkalkot': 'Karnataka',
    'aland': 'Karnataka', 'alur': 'Karnataka', 'anekal': 'Karnataka',
    'bangalore': 'Karnataka', 'mysore': 'Karnataka', 'hubli': 'Karnataka', 'mangalore': 'Karnataka',
    'belgaum': 'Karnataka', 'gulbarga': 'Karnataka', 'davanagere': 'Karnataka',
    
    # Kerala
    'adimali': 'Kerala', 'agasthamuni': 'Kerala', 'alangad': 'Kerala',
    'thiruvananthapuram': 'Kerala', 'kochi': 'Kerala', 'kozhikode': 'Kerala', 'thrissur': 'Kerala',
    'kollam': 'Kerala', 'palakkad': 'Kerala', 'alappuzha': 'Kerala', 'kannur': 'Kerala',
    
    # Madhya Pradesh (expanded)
    'waraseoni': 'Madhya Pradesh', 'balaghat': 'Madhya Pradesh', 'seoni': 'Madhya Pradesh',
    'nalchha': 'Madhya Pradesh', 'kolaras': 'Madhya Pradesh', 'raghogarh': 'Madhya Pradesh',
    'pansemal': 'Madhya Pradesh', 'tonkkhurd': 'Madhya Pradesh', 'gohad': 'Madhya Pradesh',
    'aron': 'Madhya Pradesh', 'jirapur': 'Madhya Pradesh', 'parasia': 'Madhya Pradesh',
    'dhanora': 'Madhya Pradesh', 'amla': 'Madhya Pradesh', 'betul': 'Madhya Pradesh',
    'ratlam': 'Madhya Pradesh', 'bichhiya': 'Madhya Pradesh', 'maheshwar': 'Madhya Pradesh',
    'narayanganj': 'Madhya Pradesh', 'alirajpur': 'Madhya Pradesh', 'dhimar kheda': 'Madhya Pradesh',
    'udaigarh': 'Madhya Pradesh', 'ujjain': 'Madhya Pradesh', 'sheopur': 'Madhya Pradesh',
    'bhopal urban': 'Madhya Pradesh', 'bhopal': 'Madhya Pradesh', 'pawai': 'Madhya Pradesh',
    'tamia': 'Madhya Pradesh', 'jawa': 'Madhya Pradesh', 'hatta': 'Madhya Pradesh',
    'bamori': 'Madhya Pradesh', 'khargone': 'Madhya Pradesh', 'kurwai': 'Madhya Pradesh',
    'sondwa': 'Madhya Pradesh', 'bhabra': 'Madhya Pradesh', 'narwar': 'Madhya Pradesh',
    'jaora': 'Madhya Pradesh', 'dabra': 'Madhya Pradesh', 'umarvan': 'Madhya Pradesh',
    'hanumana': 'Madhya Pradesh', 'patharia': 'Madhya Pradesh', 'majholi': 'Madhya Pradesh',
    'indore urban': 'Madhya Pradesh', 'indore': 'Madhya Pradesh', 'keolari': 'Madhya Pradesh',
    'pahadgarh': 'Madhya Pradesh', 'gandhwani': 'Madhya Pradesh', 'shujalpur': 'Madhya Pradesh',
    'bhimpur': 'Madhya Pradesh', 'ichhawar': 'Madhya Pradesh', 'karanjiya': 'Madhya Pradesh',
    'bahoriband': 'Madhya Pradesh', 'datia': 'Madhya Pradesh', 'amarpur': 'Madhya Pradesh',
    'gwalior': 'Madhya Pradesh', 'gwalior urban': 'Madhya Pradesh', 'jabalpur': 'Madhya Pradesh',
    'sagar': 'Madhya Pradesh', 'dewas': 'Madhya Pradesh', 'satna': 'Madhya Pradesh',
    'rewa': 'Madhya Pradesh', 'katni': 'Madhya Pradesh', 'burhanpur': 'Madhya Pradesh',
    'chhindwara': 'Madhya Pradesh', 'damoh': 'Madhya Pradesh', 'dhar': 'Madhya Pradesh',
    'guna': 'Madhya Pradesh', 'harda': 'Madhya Pradesh', 'hoshangabad': 'Madhya Pradesh',
    'khandwa': 'Madhya Pradesh', 'mandsaur': 'Madhya Pradesh', 'morena': 'Madhya Pradesh',
    'neemuch': 'Madhya Pradesh', 'panna': 'Madhya Pradesh', 'raisen': 'Madhya Pradesh',
    'rajgarh': 'Madhya Pradesh', 'shahdol': 'Madhya Pradesh', 'shajapur': 'Madhya Pradesh',
    'shivpuri': 'Madhya Pradesh', 'sidhi': 'Madhya Pradesh', 'singrauli': 'Madhya Pradesh',
    'tikamgarh': 'Madhya Pradesh', 'umaria': 'Madhya Pradesh', 'vidisha': 'Madhya Pradesh',
    'ghatigaon': 'Madhya Pradesh', 'mahagaon': 'Madhya Pradesh', 'ajaigarh': 'Madhya Pradesh',
    'aklera': 'Madhya Pradesh', 'akrabad': 'Madhya Pradesh', 'alampur': 'Madhya Pradesh',
    'alewa': 'Madhya Pradesh', 'algapur': 'Madhya Pradesh',
    
    # Maharashtra
    'achlapur': 'Maharashtra', 'aheri': 'Maharashtra', 'akola': 'Maharashtra',
    'akot': 'Maharashtra', 'alibag': 'Maharashtra', 'amalner': 'Maharashtra',
    'mumbai': 'Maharashtra', 'pune': 'Maharashtra', 'nagpur': 'Maharashtra', 'thane': 'Maharashtra',
    'nashik': 'Maharashtra', 'aurangabad': 'Maharashtra', 'solapur': 'Maharashtra',
    'model town': 'Maharashtra',
    
    # Mizoram
    'aibawk': 'Mizoram', 'aizawl': 'Mizoram',
    
    # Nagaland (expanded)
    'akuluto': 'Nagaland', 'pungro': 'Nagaland', 'kubulong': 'Nagaland',
    'longkhim': 'Nagaland', 'tening': 'Nagaland', 'noklak': 'Nagaland',
    'wozhuru ralan': 'Nagaland', 'tizit': 'Nagaland', 'peren': 'Nagaland',
    'longleng': 'Nagaland', 'zunheboto': 'Nagaland', 'tokiye': 'Nagaland',
    'simiti': 'Nagaland', 'chukitong': 'Nagaland', 'phek': 'Nagaland',
    'mon': 'Nagaland', 'ongpangkong south': 'Nagaland', 'meluri': 'Nagaland',
    'sangsangnyu': 'Nagaland', 'sekruzu': 'Nagaland', 'kohima': 'Nagaland',
    'tobu': 'Nagaland', 'satakha': 'Nagaland', 'changtongya': 'Nagaland',
    'chessore': 'Nagaland', 'wokha': 'Nagaland', 'noksen': 'Nagaland',
    'tamlu': 'Nagaland', 'medziphema': 'Nagaland', 'dimapur': 'Nagaland',
    'kiphire': 'Nagaland', 'mokokchung': 'Nagaland', 'tuensang': 'Nagaland',

    # Rajasthan (expanded)
    'bhopalgarh': 'Rajasthan', 'bhopalsagar': 'Rajasthan', 'jodhpur': 'Rajasthan',
    'jaipur': 'Rajasthan', 'udaipur': 'Rajasthan', 'kota': 'Rajasthan',
    'ajmer': 'Rajasthan', 'bikaner': 'Rajasthan', 'alwar': 'Rajasthan',
    'abu road': 'Rajasthan', 'afzalgarh': 'Rajasthan', 'ahore': 'Rajasthan',
    'akrani': 'Rajasthan', 'bharatpur': 'Rajasthan', 'bhilwara': 'Rajasthan',
    'churu': 'Rajasthan', 'ganganagar': 'Rajasthan', 'hanumangarh': 'Rajasthan',
    'jaisalmer': 'Rajasthan', 'jhalawar': 'Rajasthan', 'jhunjhunu': 'Rajasthan',
    'nagaur': 'Rajasthan', 'pali': 'Rajasthan', 'sikar': 'Rajasthan', 'tonk': 'Rajasthan',

    # Tamil Nadu
    'aanandhur': 'Tamil Nadu', 'agarapettai': 'Tamil Nadu', 'agrapalayam': 'Tamil Nadu',
    'agastheeswaram': 'Tamil Nadu', 'airaya': 'Tamil Nadu', 'alandur': 'Tamil Nadu',
    'alanganallur': 'Tamil Nadu', 'alangiyam': 'Tamil Nadu', 'alangudi(p)': 'Tamil Nadu',
    'alangudy': 'Tamil Nadu', 'alangulam': 'Tamil Nadu', 'alanthur': 'Tamil Nadu',
    'alathur': 'Tamil Nadu', 'karimangalam': 'Tamil Nadu',
    'chennai': 'Tamil Nadu', 'coimbatore': 'Tamil Nadu', 'madurai': 'Tamil Nadu',
    'tiruchirappalli': 'Tamil Nadu', 'salem': 'Tamil Nadu', 'tirunelveli': 'Tamil Nadu',
    'tiruppur': 'Tamil Nadu', 'vellore': 'Tamil Nadu', 'erode': 'Tamil Nadu',

    # Telangana
    'damaragidda': 'Telangana', 'kammarpalle': 'Telangana', 'tadvai': 'Telangana',
    'adilabad rural': 'Telangana', 'adilabad urban': 'Telangana', 'agalpur': 'Telangana',
    'akbarpet-bhoompally': 'Telangana', 'alamela': 'Telangana', 'alamnagar': 'Telangana',
    'hyderabad': 'Telangana', 'warangal': 'Telangana', 'nizamabad': 'Telangana',
    'khammam': 'Telangana', 'karimnagar': 'Telangana', 'ramagundam': 'Telangana',
    'mahbubnagar': 'Telangana', 'nalgonda': 'Telangana', 'medak': 'Telangana',

    # Uttar Pradesh
    'achhnera': 'Uttar Pradesh', 'adapur': 'Uttar Pradesh', 'afzalgarh': 'Uttar Pradesh',
    'agra city': 'Uttar Pradesh', 'ahmedpur': 'Uttar Pradesh', 'ajnala': 'Uttar Pradesh',
    'aligarh city': 'Uttar Pradesh', 'lucknow': 'Uttar Pradesh', 'kanpur': 'Uttar Pradesh',
    'ghaziabad': 'Uttar Pradesh', 'agra': 'Uttar Pradesh', 'meerut': 'Uttar Pradesh',
    'varanasi': 'Uttar Pradesh', 'allahabad': 'Uttar Pradesh', 'bareilly': 'Uttar Pradesh',
    'aligarh': 'Uttar Pradesh', 'moradabad': 'Uttar Pradesh', 'saharanpur': 'Uttar Pradesh',
    'gorakhpur': 'Uttar Pradesh', 'noida': 'Uttar Pradesh', 'firozabad': 'Uttar Pradesh',

    # West Bengal
    'purbasthali-ii': 'West Bengal', 'guruhar sahai': 'West Bengal',
    'kolkata': 'West Bengal', 'howrah': 'West Bengal', 'durgapur': 'West Bengal',
    'asansol': 'West Bengal', 'siliguri': 'West Bengal', 'bardhaman': 'West Bengal',
    'malda': 'West Bengal', 'baharampur': 'West Bengal', 'habra': 'West Bengal',

    # Jammu & Kashmir
    'achabal': 'Jammu and Kashmir', 'akhnoor': 'Jammu and Kashmir',
    'srinagar': 'Jammu and Kashmir', 'jammu': 'Jammu and Kashmir', 'anantnag': 'Jammu and Kashmir',
    'baramulla': 'Jammu and Kashmir', 'kupwara': 'Jammu and Kashmir', 'pulwama': 'Jammu and Kashmir',

    # Punjab
    'abohar': 'Punjab', 'adampur': 'Punjab', 'ajnala': 'Punjab',
    'ludhiana': 'Punjab', 'amritsar': 'Punjab', 'jalandhar': 'Punjab', 'patiala': 'Punjab',
    'bathinda': 'Punjab', 'mohali': 'Punjab', 'firozpur': 'Punjab', 'hoshiarpur': 'Punjab',

    # Odisha
    'dumburnagar': 'Odisha', 'baririjo': 'Odisha',
    'bhubaneswar': 'Odisha', 'cuttack': 'Odisha', 'rourkela': 'Odisha', 'brahmapur': 'Odisha',
    'sambalpur': 'Odisha', 'puri': 'Odisha', 'balasore': 'Odisha', 'bhadrak': 'Odisha',
}

# Export for use in other scripts
if __name__ == "__main__":
    print(f"Total mappings: {len(COMPREHENSIVE_MAPPING)}")
    print(f"States covered: {len(set(COMPREHENSIVE_MAPPING.values()))}")

