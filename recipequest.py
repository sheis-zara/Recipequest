import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json
import hashlib
import os
import requests
from streamlit_lottie import st_lottie  # Added this import for animations

def load_css():
    st.markdown("""
    <style>
    /* Enhanced Chic & Mature Theme */
    :root {
        --primary: #2C3E50;
        --secondary: #34495E;
        --accent: #E67E22;
        --light: #ECF0F1;
        --dark: #2C3E50;
        --text: #2C3E50;
        --text-light: #7F8C8D;
        --success: #27AE60;
        --warning: #F39C12;
        --error: #E74C3C;
        --card-bg: #F8F9FA;
        --shadow: rgba(44, 62, 80, 0.15);
        --sidebar-bg: #FFFFFF;  /* Changed to white */
        --sidebar-text: #E67E22;  /* Changed to orange for text */
        --sidebar-hover: #FDE3CE;  /* Light orange for hover */
    }
    
    /* Sidebar styling - fixed to white background with orange text */
    .css-1d391kg, 
    .css-1v0mbdj, 
    .st-emotion-cache-1cypcdb {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(230, 126, 34, 0.2) !important;
    }
    
    .css-1d391kg p,
    .css-1v0mbdj p,
    .st-emotion-cache-1cypcdb p,
    .css-1d391kg h1,
    .css-1v0mbdj h1,
    .st-emotion-cache-1cypcdb h1,
    .css-1d391kg h2,
    .css-1v0mbdj h2,
    .st-emotion-cache-1cypcdb h2,
    .css-1d391kg h3,
    .css-1v0mbdj h3,
    .st-emotion-cache-1cypcdb h3,
    .css-1d391kg label,
    .css-1v0mbdj label,
    .st-emotion-cache-1cypcdb label,
    .css-1d391kg div,
    .css-1v0mbdj div,
    .st-emotion-cache-1cypcdb div {
        color: var(--sidebar-text) !important;
    }
    
    .stRadio > div {
        color: var(--sidebar-text) !important;
    }
    
    .stRadio > label {
        color: var(--sidebar-text) !important;
        font-weight: 500;
    }
    
    /* Sidebar radio buttons */
    .stRadio [data-baseweb="radio"] {
        margin-bottom: 0.5rem;
    }
    
    .stRadio [data-baseweb="radio"] div {
        color: var(--sidebar-text) !important;
    }
    
    .stRadio [data-baseweb="radio"]:hover {
        background-color: var(--sidebar-hover) !important;
        border-radius: 6px;
    }
    
    /* Metric cards in sidebar */
    .css-1d391kg .stMetric,
    .css-1v0mbdj .stMetric,
    .st-emotion-cache-1cypcdb .stMetric {
        background-color: rgba(230, 126, 34, 0.1) !important;
        border: 1px solid rgba(230, 126, 34, 0.2) !important;
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
    }
    
    .css-1d391kg .stMetric label,
    .css-1v0mbdj .stMetric label,
    .st-emotion-cache-1cypcdb .stMetric label,
    .css-1d391kg .stMetric div,
    .css-1v0mbdj .stMetric div,
    .st-emotion-cache-1cypcdb .stMetric div {
        color: var(--sidebar-text) !important;
    }
    
    /* Rest of your CSS remains the same */
    """, unsafe_allow_html=True)
# Password hashing for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User data management
def load_users():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Load Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize session state
def init_session_state():
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'users' not in st.session_state:
        st.session_state.users = load_users()
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'notes' not in st.session_state:
        st.session_state.notes = []
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = {}
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    if 'daily_calories' not in st.session_state:
        st.session_state.daily_calories = 0
    if 'daily_goal' not in st.session_state:
        st.session_state.daily_goal = 2000
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'chef_mood' not in st.session_state:
        st.session_state.chef_mood = "neutral"
    if 'game_ingredients' not in st.session_state:
        st.session_state.game_ingredients = []

# Recipe Database
RECIPES = {
    # Nigerian Dishes
    "Jollof Rice": {
        "ingredients": [
            "3 cups long grain rice (preferably basmati or jasmine)",
            "4-5 large fresh tomatoes (or 1 can tomato puree)",
            "2 large red bell peppers",
            "1 large onion, diced",
            "3-4 scotch bonnet peppers (adjust to taste)",
            "4-5 cups chicken or beef stock (rich and flavorful)",
            "3 seasoning cubes (Maggi or Knorr)",
            "2 bay leaves",
            "1/4 cup vegetable oil or palm oil",
            "2 tablespoons tomato paste",
            "1 teaspoon curry powder",
            "1 teaspoon thyme (dried or fresh)",
            "Salt and black pepper to taste",
            "1 teaspoon garlic powder",
            "1 teaspoon ginger powder",
            "Optional: 2 cups mixed vegetables (carrots, green beans, peas)"
        ],
        "steps": [
            "Prepare tomato base: Blend tomatoes, red bell peppers, onions, and scotch bonnet peppers until smooth. This creates the foundation of flavor for your jollof rice.",
            "Parboil the rice: Rinse rice in cold water until water runs clear. Boil rice in salted water for 8-10 minutes until 70% cooked. Drain immediately and rinse with cold water to stop cooking process.",
            "Create the sauce: Heat oil in a heavy-bottomed pot over medium heat. Add diced onions and sauté until translucent (3-4 minutes). Add tomato paste and fry for 2 minutes until darkened.",
            "Add blended mixture: Pour in the blended tomato mixture and cook for 15-20 minutes, stirring occasionally, until the mixture reduces and loses its raw taste. The color should deepen to a rich red.",
            "Season the sauce: Add curry powder, thyme, seasoning cubes, salt, pepper, garlic powder, and ginger powder. Stir well and cook for 2-3 minutes to bloom the spices.",
            "Add liquid and rice: Pour in the stock gradually, add bay leaves, then add the parboiled rice. The liquid should be about 1 inch above the rice level.",
            "Cook and steam: Bring to a boil, then reduce heat to low, cover tightly with foil then the pot lid. Cook for 20-25 minutes without lifting the lid.",
            "Add vegetables (optional): If using mixed vegetables, add them in the last 10 minutes of cooking.",
            "Rest and serve: Let the rice rest for 5 minutes after cooking. Remove bay leaves, gently mix, and serve hot with fried plantains, coleslaw, or grilled chicken."
        ],
        "time": "60 mins",
        "servings": 6,
        "category": "Lunch",
        "calories": 380,
        "difficulty": "Medium",
        "prep_time": "20 mins",
        "cook_time": "40 mins",
        "tips": [
            "Use long-grain rice for the best texture and to prevent mushiness",
            "Don't skip the parboiling step - it prevents the rice from becoming soggy",
            "Let the tomato base cook properly to remove the raw taste",
            "Use a heavy-bottomed pot to prevent burning",
            "The key to perfect jollof is the right liquid-to-rice ratio"
        ],
        "nutritional_info": {
            "protein": "8g",
            "carbs": "65g",
            "fat": "12g",
            "fiber": "3g"
        }
    },
    "Egusi Soup": {
        "ingredients": [
            "2 cups ground melon seeds (egusi)",
            "2 cups fresh spinach (ugu) or any preferred leafy vegetables, chopped",
            "1/2 cup red palm oil",
            "1 lb assorted meat (beef, goat meat, cow skin - kpomo)",
            "1/2 lb dried fish (cleaned and deboned)",
            "1/4 lb fresh fish (cut into steaks)",
            "2 large onions, diced",
            "3-4 scotch bonnet peppers (or to taste)",
            "2 tablespoons ground crayfish",
            "3 seasoning cubes",
            "2 tablespoons locust beans (iru/ogiri) - optional but authentic",
            "1 teaspoon ground ginger",
            "Salt to taste",
            "4-5 cups meat stock (from cooking the meat)",
            "1 tablespoon ground pepper (ata gungun)",
            "1 cup periwinkles (optional, for authentic taste)"
        ],
        "steps": [
            "Prepare proteins: Season and cook assorted meat with onions, salt, and seasoning cubes until tender (45-60 minutes). Reserve the stock. Clean and season fish separately.",
            "Prepare egusi paste: Mix ground melon seeds with 1/2 cup of warm stock or water to form a thick, smooth paste. This prevents lumping during cooking.",
            "Heat palm oil: In a large pot, heat palm oil on medium heat. Don't let it smoke - this creates the right base for the soup.",
            "Fry egusi paste: Add the egusi paste to the hot oil and fry for 8-10 minutes, stirring constantly to prevent burning. The paste should turn golden and aromatic.",
            "Add aromatics: Add chopped onions, ground crayfish, locust beans (if using), ground pepper, and scotch bonnet peppers. Fry for 3-4 minutes.",
            "Add proteins and stock: Add the cooked meat and fish to the pot. Gradually add the meat stock until you achieve your desired consistency (usually thick but not paste-like).",
            "Season and simmer: Add seasoning cubes, salt, and ginger. Let it simmer for 15-20 minutes, stirring occasionally. Taste and adjust seasoning.",
            "Add vegetables: Add the chopped spinach or ugu leaves in the last 5-7 minutes of cooking. Don't overcook the vegetables to maintain their color and nutrition.",
            "Final touches: Add periwinkles if using, stir gently, and cook for 2-3 more minutes. Serve hot with pounded yam, fufu, eba, or rice."
        ],
        "time": "90 mins",
        "servings": 8,
        "category": "Lunch",
        "calories": 450,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "60 mins",
        "tips": [
            "Always fry the egusi paste properly to avoid a raw taste",
            "Don't add too much liquid at once - build the consistency gradually",
            "Use fresh vegetables and add them last to maintain color and nutrients",
            "The soup tastes better the next day as flavors meld together",
            "You can blend some of the egusi with peppers for a different texture"
        ],
        "nutritional_info": {
            "protein": "35g",
            "carbs": "12g",
            "fat": "28g",
            "fiber": "6g"
        }
    },
    "Suya": {
        "ingredients": [
            "2 lbs beef sirloin or tenderloin, cut into thin strips",
            "1/4 cup yaji (suya spice blend) - see recipe below",
            "2 tablespoons groundnut oil",
            "1 large onion, sliced into rings",
            "2 large tomatoes, sliced",
            "1 large cucumber, sliced",
            "1 cabbage head, shredded",
            "For Yaji (Suya Spice):",
            "1/2 cup roasted peanuts, ground",
            "1 tablespoon ground ginger",
            "1 tablespoon garlic powder",
            "1 teaspoon ground cloves",
            "1 teaspoon ground nutmeg",
            "2 tablespoons cayenne pepper (adjust to taste)",
            "2 seasoning cubes, crushed",
            "1 teaspoon salt"
        ],
        "steps": [
            "Prepare yaji spice: Roast peanuts in a dry pan until golden. Cool completely and grind to a fine powder. Mix with all other spice ingredients. Store in an airtight container.",
            "Prepare meat: Cut beef into thin strips (about 1/4 inch thick). This ensures even cooking and better spice absorption.",
            "Marinate: Rub meat strips with groundnut oil and half of the yaji spice. Let marinate for at least 30 minutes (longer for better flavor).",
            "Prepare skewers: Thread marinated meat onto metal skewers or soaked wooden skewers, leaving small spaces between pieces for even cooking.",
            "Prepare grill: If using charcoal, let coals burn until they're glowing red with no flames. For gas grill, preheat to medium-high heat.",
            "Grill suya: Cook skewers for 10-15 minutes, turning every 3-4 minutes. Brush with oil and sprinkle more yaji during cooking.",
            "Check doneness: Meat should be slightly charred outside but tender inside. Don't overcook as it will become tough.",
            "Prepare accompaniments: Arrange sliced onions, tomatoes, cucumber, and cabbage on a platter.",
            "Serve: Remove meat from skewers, sprinkle with remaining yaji, and serve immediately with fresh vegetables and cold drinks."
        ],
        "time": "45 mins",
        "servings": 4,
        "category": "Snack",
        "calories": 320,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "15 mins",
        "tips": [
            "Use tender cuts of meat for the best results",
            "Don't skip the marination time - it makes all the difference",
            "Keep the grill at medium heat to avoid burning the spices",
            "Make extra yaji spice - it keeps well and can be used on other grilled foods",
            "Serve immediately while hot for the best experience"
        ],
        "nutritional_info": {
            "protein": "42g",
            "carbs": "8g",
            "fat": "15g",
            "fiber": "3g"
        }
    },
     "Pounded Yam": {
        "ingredients": [
            "4-5 medium tubers of white yam (about 3 lbs)",
            "Water for boiling",
            "1 teaspoon salt",
            "Ice cubes (for the perfect texture)"
        ],
        "steps": [
            "Select and prepare yam: Choose white yam tubers that are firm and free from spots. Peel with a sharp knife, removing all the brown skin and any discolored parts.",
            "Cut and wash: Cut yam into medium-sized chunks (about 3-4 inches). Wash thoroughly in cold water to remove any dirt or residue.",
            "Boil yam: Place yam pieces in a large pot with enough water to cover by 2 inches. Add salt and bring to a rapid boil.",
            "Cook until tender: Cook for 20-25 minutes until yam is very soft and easily pierced with a fork. The yam should almost fall apart when lifted.",
            "Drain carefully: Drain the yam immediately and let it cool slightly. Remove any remaining water to prevent a watery texture.",
            "Pound traditionally: Using a mortar and pestle, pound the yam while still warm. Add ice cubes gradually to achieve the smooth, elastic texture.",
            "Alternative method: If using a food processor, pulse carefully and add ice cubes to get the right consistency. Don't over-process.",
            "Check consistency: Properly pounded yam should be smooth, elastic, and stretchy without any lumps.",
            "Serve immediately: Shape into individual portions and serve hot with your favorite soup (egusi, okra, vegetable soup)."
        ],
        "time": "50 mins",
        "servings": 6,
        "category": "Lunch",
        "calories": 340,
        "difficulty": "Medium",
        "prep_time": "15 mins",
        "cook_time": "35 mins",
        "tips": [
            "Use white yam for the best texture and taste",
            "Don't overcook the yam or it will become watery",
            "Ice cubes are the secret to achieving the perfect stretchy texture",
            "Serve immediately as it hardens when cool",
            "Work quickly while the yam is still warm for easier pounding"
        ],
        "nutritional_info": {
            "protein": "4g",
            "carbs": "78g",
            "fat": "0.5g",
            "fiber": "7g"
        }
    },
     "Pepper Soup": {
        "ingredients": [
            "1 lb of protein (e.g., fresh catfish, goat meat, or assorted cow parts)",
            "2 tbsp pre-mixed pepper soup spice",
            "2-3 scotch bonnet peppers (atarodo), chopped or blended",
            "1 large onion, chopped",
            "A handful of fresh scent leaves (efirin)",
            "2 bouillon cubes",
            "Salt to taste",
            "1 small handful of uziza seeds (ground, optional)"
        ],
        "steps": [
            "Wash protein thoroughly. For goat meat or assorted cow parts, parboil with onions and a pinch of salt until slightly tender.",
            "Add enough water to the pot to cover the protein and bring to a boil.",
            "Stir in pepper soup spice, chopped peppers, and seasoning cubes. Simmer for 10-15 minutes.",
            "If using fish, gently add it to the simmering broth. Cook until tender, being careful not to stir vigorously.",
            "Taste and adjust salt/pepper. Just before serving, stir in the scent leaves to wilt.",
            "Serve hot on its own or with boiled yam, plantain, or rice."
        ],
        "time": "45 mins",
        "servings": 3,
        "category": "Dinner/Appetizer",
        "calories": 250,
        "difficulty": "Easy",
        "prep_time": "10 mins",
        "cook_time": "35 mins",
        "tips": [
            "Use a pre-made spice mix for authentic flavor and ease of preparation.",
            "Handle scotch bonnet peppers with care or use gloves.",
            "Parboiling tough meats like goat or cow parts first ensures they are tender."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "5g",
            "fat": "10g",
            "fiber": "1g"
        }
    },
    "Fried Rice": {
        "ingredients": [
            "3 cups long-grain rice (preferably basmati)",
            "1/2 cup mixed vegetables (carrots, green peas, sweet corn, diced green bell pepper)",
            "1 cup cooked chicken or beef, diced",
            "1/4 cup cooked shrimp (optional)",
            "2 eggs, beaten",
            "1 large onion, diced",
            "2 spring onions, chopped",
            "3 cloves garlic, minced",
            "1 teaspoon ginger, grated",
            "2 tablespoons vegetable oil",
            "2 tablespoons soy sauce",
            "1 teaspoon curry powder",
            "1/2 teaspoon thyme",
            "2 seasoning cubes",
            "Salt and pepper to taste",
            "2 cups chicken stock",
            "1 tablespoon butter"
        ],
        "steps": [
            "Prepare rice: Wash rice until water runs clear. Parboil in salted water until 70% cooked (about 8 minutes). Drain and set aside.",
            "Prepare vegetables: Dice all vegetables uniformly for even cooking. Keep them separate as they have different cooking times.",
            "Scramble eggs: Heat 1 tablespoon oil in a large wok or pan. Scramble beaten eggs and set aside.",
            "Cook aromatics: In the same pan, add remaining oil, sauté onions until translucent, add garlic and ginger.",
            "Add proteins: Add diced meat and shrimp, stir-fry for 2-3 minutes until heated through.",
            "Cook vegetables: Add harder vegetables first (carrots), then softer ones (bell peppers, peas, corn). Stir-fry for 3-4 minutes.",
            "Season: Add curry powder, thyme, seasoning cubes, soy sauce, salt, and pepper. Mix well.",
            "Add rice: Add the parboiled rice and mix gently. Add stock gradually until rice is tender but not mushy.",
            "Finish: Add scrambled eggs, spring onions, and butter. Toss gently and serve hot."
        ],
        "time": "45 mins",
        "servings": 6,
        "category": "Lunch",
        "calories": 420,
        "difficulty": "Medium",
        "prep_time": "20 mins",
        "cook_time": "25 mins",
        "tips": [
            "Don't fully cook the rice initially - it will finish cooking with the vegetables",
            "Use day-old rice for better texture if possible",
            "Keep vegetables crisp for better texture and nutrition",
            "Soy sauce adds umami but use sparingly",
            "A large wok or pan ensures even cooking"
        ],
        "nutritional_info": {
            "protein": "22g",
            "carbs": "58g",
            "fat": "12g",
            "fiber": "3g"
        }
    },
    "Moi Moi": {
        "ingredients": [
            "3 cups black-eyed beans (peeled)",
            "2 large red bell peppers",
            "2 medium onions",
            "2-3 scotch bonnet peppers",
            "1/2 cup palm oil",
            "3 hard-boiled eggs, sliced",
            "1/2 cup flaked fish or corned beef",
            "3 seasoning cubes",
            "1 teaspoon salt",
            "1-2 cups warm water/stock",
            "Moi moi leaves or foil for wrapping"
        ],
        "steps": [
            "Soak beans in water 10 minutes, rub to remove skins completely. Rinse until clean.",
            "Blend beans with peppers, onions, and little water until very smooth paste.",
            "Add palm oil, seasoning cubes, salt to bean paste. Mix thoroughly.",
            "Gradually add warm water/stock until mixture has thick, pourable consistency.",
            "Fold in eggs and fish/meat pieces gently.",
            "Scoop mixture into moi moi leaves, foil cups, or containers.",
            "Steam in large pot with boiling water for 45-60 minutes until firm.",
            "Test doneness with knife - should come out clean.",
            "Cool slightly before serving hot or warm."
        ],
        "time": "75 mins",
        "servings": 6,
        "category": "Breakfast",
        "calories": 200,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "45 mins",
        "tips": [
            "Remove bean skins completely for smooth texture",
            "Blend to very smooth consistency",
            "Steam steadily for even cooking",
            "Don't overfill containers"
        ],
        "nutritional_info": {
            "protein": "12g",
            "carbs": "18g",
            "fat": "8g",
            "fiber": "4g"
        }
    },
    "Akara": {
        "ingredients": [
            "2 cups black-eyed beans (soaked overnight)",
            "1 medium onion, roughly chopped",
            "2-3 scotch bonnet peppers (adjust to taste)",
            "1 teaspoon salt",
            "1/2 teaspoon ground ginger (optional)",
            "Vegetable oil for deep frying (about 3 cups)"
        ],
        "steps": [
            "Drain soaked beans and rub between palms to remove skins. Rinse until clean.",
            "Blend beans with onions, peppers, and minimal water until smooth, fluffy paste.",
            "Add salt and ginger, mix well. Batter should be thick but pipeable.",
            "Heat oil in deep pot to 350°F (test with small batter drop - should sizzle immediately).",
            "Using spoon, drop batter into hot oil, fry until golden brown (3-4 minutes).",
            "Remove with slotted spoon, drain on paper towels.",
            "Serve immediately while hot and crispy."
        ],
        "time": "25 mins",
        "servings": 4,
        "category": "Breakfast",
        "calories": 150,
        "difficulty": "Medium",
        "prep_time": "15 mins",
        "cook_time": "10 mins"
    },

    "Banga Soup": {
        "ingredients": [
            "1 lb fresh fish or beef",
            "2 cups banga paste (palm fruit concentrate)",
            "1/2 cup blended fresh pepper (scotch bonnet or rodo)",
            "1/2 cup fresh or dried prawns",
            "1/4 cup periwinkles (optional)",
            "A handful of banga spice leaves (optional)",
            "1 medium-sized onion, chopped",
            "2 bouillon cubes",
            "Salt to taste"
        ],
        "steps": [
            "If using fresh palm fruit, boil and pound to extract the thick concentrate. If using paste, dilute with water.",
            "Pour the concentrate into a large pot and bring to a boil. It will form a thick, oily soup.",
            "Add the chopped onion, fresh pepper, and seasoning cubes. Let it simmer for 15-20 minutes.",
            "Add the fish or meat, cooked prawns, and periwinkles. Cook until the fish is tender and the soup has thickened.",
            "Stir in the banga spice leaves for flavor (if using).",
            "Serve hot with starch, garri (eba), or fufu."
        ],
        "time": "50 mins",
        "servings": 4,
        "category": "Dinner",
        "calories": 450,
        "difficulty": "Medium",
        "prep_time": "15 mins",
        "cook_time": "35 mins",
        "tips": [
            "The key is to use a good quality banga paste or extract your own concentrate for best flavor.",
            "Do not overcook the soup after adding the fresh fish to prevent it from breaking apart.",
            "The soup should be a little thick, but you can add a little water if it becomes too thick."
        ],
        "nutritional_info": {
            "protein": "18g",
            "carbs": "30g",
            "fat": "30g",
            "fiber": "5g"
        }
    },
    "Ofada Rice": {
        "ingredients": [
            "3 cups ofada rice (brown short-grain rice)",
            "1/2 cup palm oil",
            "2-3 scotch bonnet peppers, blended",
            "1 cup red bell peppers (tatashe), blended",
            "1 large onion, chopped",
            "1/2 cup cooked cowhide (pomo), diced",
            "1/2 cup assorted meat (shaki, beef), cooked and diced",
            "1/4 cup cooked shrimp or prawns (optional)",
            "2 bouillon cubes",
            "Salt to taste",
            "A handful of iru (fermented locust beans)"
        ],
        "steps": [
            "Cook the ofada rice according to package directions, typically by boiling until soft. Set aside.",
            "Heat palm oil in a pot until it is hot but not smoking (the oil should be clear).",
            "Add the chopped onion and iru. Sauté until the onion is translucent.",
            "Add the blended peppers and stir-fry for 10 minutes until the oil floats to the top.",
            "Add the cooked meats (pomo, shaki, beef), seasoning cubes, and salt. Stir well.",
            "Add the cooked ofada rice to the sauce. Mix thoroughly until the rice is evenly coated.",
            "Serve hot, traditionally wrapped in 'ewe eran' leaves and with plantain or other sides."
        ],
        "time": "1 hr 15 mins",
        "servings": 5,
        "category": "Lunch/Dinner",
        "calories": 480,
        "difficulty": "Hard",
        "prep_time": "30 mins",
        "cook_time": "45 mins",
        "tips": [
            "Ofada rice has a unique earthy flavor that pairs well with the spicy, fermented sauce.",
            "Frying the sauce until the oil floats on top is a key step to develop the flavor.",
            "Fermented locust beans (`iru`) are essential for the traditional flavor of the sauce."
        ],
        "nutritional_info": {
            "protein": "15g",
            "carbs": "65g",
            "fat": "20g",
            "fiber": "4g"
        }
    },
    "Plantain Porridge": {
        "ingredients": [
            "4-5 unripe plantains, peeled and chopped",
            "1/2 cup palm oil",
            "1 large onion, chopped",
            "1/2 cup crayfish (ground)",
            "1/2 cup smoked fish, deboned",
            "1/2 cup pumpkin leaves (ugu), shredded (optional)",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "2 cups water or stock"
        ],
        "steps": [
            "Place the chopped plantains in a pot. Add enough water or stock to cover them.",
            "Add the chopped onion, crayfish, smoked fish, and seasoning cubes. Bring to a boil.",
            "Once boiling, reduce the heat to a simmer and cook until the plantains are soft and the liquid has thickened.",
            "Add the palm oil and stir to combine. Cook for another 5 minutes.",
            "Add the shredded pumpkin leaves (if using) and stir to wilt.",
            "Taste and adjust seasoning with salt and pepper as needed.",
            "Serve hot and enjoy!"
        ],
        "time": "40 mins",
        "servings": 4,
        "category": "Lunch/Dinner",
        "calories": 350,
        "difficulty": "Easy",
        "prep_time": "15 mins",
        "cook_time": "25 mins",
        "tips": [
            "Ensure the plantains are not too ripe, as they will turn mushy when cooked.",
            "Crayfish and smoked fish are essential for the smoky, savory flavor.",
            "Stir gently as the plantains cook to prevent them from breaking down completely."
        ],
        "nutritional_info": {
            "protein": "10g",
            "carbs": "50g",
            "fat": "15g",
            "fiber": "7g"
        }
    },
    "Bitter Leaf Soup": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe)",
            "2 cups washed and squeezed bitter leaf",
            "1/2 cup cocoyam, blended into a paste for thickening",
            "1/2 cup crayfish (ground)",
            "1/2 cup smoked fish, deboned",
            "1/2 cup palm oil",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1 large onion, chopped"
        ],
        "steps": [
            "Boil the assorted meat with chopped onions, salt, and seasoning cubes until tender.",
            "Add the palm oil to the boiling meat stock. Stir and bring to a simmer.",
            "Add the blended cocoyam paste in small lumps. Stir until it dissolves and the soup begins to thicken.",
            "Add the washed bitter leaf and smoked fish. Stir well and allow to simmer for 5 minutes.",
            "Stir in the ground crayfish and adjust seasoning with salt and pepper as needed.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "1 hr 30 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 480,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "1 hr",
        "tips": [
            "Washing the bitter leaf properly is crucial to reduce its bitterness.",
            "The cocoyam is the traditional thickener, but you can also use achi or ofor.",
            "Cooking the meat until it is very tender is key for a delicious soup."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "45g",
            "fat": "25g",
            "fiber": "10g"
        }
    },
    "Yam Porridge": {
        "ingredients": ["Yam", "Palm oil", "Onions", "Fish", "Spinach", "Pepper"],
        "steps": ["Cut yam into chunks", "Cook with seasonings", "Add vegetables", "Simmer"],
        "time": "35 mins",
        "servings": 4,
        "category": "Dinner",
        "calories": 320
    },
    "Nkwobi": {
        "ingredients": [
            "2 lbs cow foot (cut into small pieces)",
            "1/2 cup palm oil",
            "1 tbsp edible potash (akanwu), dissolved in water",
            "1 tbsp ground ehuru (calabash nutmeg)",
            "1 tbsp ground uziza seeds",
            "1/2 cup blended scotch bonnet peppers",
            "1 large onion, sliced into rings",
            "2 bouillon cubes",
            "Salt to taste"
        ],
        "steps": [
            "Boil the cow foot with chopped onion, salt, and seasoning cubes until it is very soft and tender.",
            "In a separate bowl, mix the palm oil with the potash solution until it turns into a thick yellow paste.",
            "Add the ground ehuru, uziza seeds, and blended peppers to the palm oil mixture. Stir well.",
            "Add the cooked cow foot to the mixture and stir to coat all the pieces evenly.",
            "Transfer to a bowl and garnish with the sliced onion rings.",
            "Serve warm as a side dish or appetizer."
        ],
        "time": "2 hrs",
        "servings": 4,
        "category": "Appetizer",
        "calories": 600,
        "difficulty": "Medium",
        "prep_time": "15 mins",
        "cook_time": "1 hr 45 mins",
        "tips": [
            "Make sure the cow foot is very soft before mixing with the sauce.",
            "The potash solution is what gives the Nkwobi its characteristic thick texture.",
            "Garnishing with onion rings adds a fresh, crunchy element."
        ],
        "nutritional_info": {
            "protein": "30g",
            "carbs": "10g",
            "fat": "40g",
            "fiber": "2g"
        }
    },
    "Chin-Chin": {
        "ingredients": [
            "4 cups all-purpose flour",
            "1 cup granulated sugar",
            "1/2 cup margarine or butter, softened",
            "1 tsp baking powder",
            "1/2 tsp salt",
            "1 egg",
            "1/2 cup evaporated milk",
            "1 tsp vanilla extract",
            "Oil for deep frying"
        ],
        "steps": [
            "In a large bowl, sift the flour, baking powder, and salt together.",
            "In a separate bowl, cream the sugar and softened margarine together until light and fluffy.",
            "Beat in the egg and vanilla extract. Gradually add the milk and mix well.",
            "Slowly add the flour mixture to the wet ingredients and mix until a firm dough is formed.",
            "Turn the dough out onto a floured surface and knead for about 5 minutes until smooth.",
            "Roll the dough out to about 1/4 inch thick and cut into desired shapes (squares or strips).",
            "Heat oil in a deep fryer or pot to 350°F (175°C).",
            "Fry the chin-chin in batches until golden brown and crispy. Drain on a paper towel.",
            "Allow to cool completely before storing in an airtight container."
        ],
        "time": "1 hr",
        "servings": 8,
        "category": "Snack",
        "calories": 200,
        "difficulty": "Easy",
        "prep_time": "30 mins",
        "cook_time": "30 mins",
        "tips": [
            "The dough should not be too soft or too hard. Adjust with flour or milk if needed.",
            "Use a pasta cutter or a sharp knife to cut uniform shapes for even frying.",
            "Fry in small batches to avoid overcrowding the pot, which can lower the oil temperature."
        ],
        "nutritional_info": {
            "protein": "4g",
            "carbs": "25g",
            "fat": "10g",
            "fiber": "1g"
        }
    },
    
    # More Nigerian dishes...
    "Okra Soup": {
        "ingredients": [
            "1 lb fresh okra, chopped",
            "1 lb assorted meat (beef, shaki, cow tripe), cooked",
            "1/2 cup palm oil",
            "1 large onion, chopped",
            "1/2 cup crayfish (ground)",
            "1/2 cup smoked fish, deboned",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1 cup water or stock"
        ],
        "steps": [
            "In a pot, heat palm oil and sauté the chopped onion until translucent.",
            "Add the cooked assorted meat, smoked fish, and crayfish. Stir-fry for 2-3 minutes.",
            "Add water or stock and bring to a boil. Add the seasoning cubes, salt, and pepper.",
            "Add the chopped okra and stir gently. Cook for 5-7 minutes until the okra is soft but still has a slight crunch.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "45 mins",
        "servings": 5,
        "category": "Dinner",
        "calories": 380,
        "difficulty": "Easy",
        "prep_time": "15 mins",
        "cook_time": "30 mins",
        "tips": [
            "Do not overcook the okra, as it will lose its texture and color.",
            "For a thicker consistency, you can use a hand blender to puree some of the okra.",
            "This soup is very versatile and you can use any protein you prefer."
        ],
        "nutritional_info": {
            "protein": "20g",
            "carbs": "15g",
            "fat": "25g",
            "fiber": "5g"
        }
    },   
    "Fisherman Soup": {
        "ingredients": [
            "1 lb mixed seafood (shrimp, fish, crabs, periwinkles)",
            "1/2 cup palm oil",
            "1 large onion, chopped",
            "1/2 cup blended scotch bonnet peppers",
            "1/2 cup ground crayfish",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "A handful of ugu or scent leaves, shredded"
        ],
        "steps": [
            "Wash and prepare the seafood. Set aside.",
            "In a pot, heat palm oil and sauté the onion and blended peppers.",
            "Add the smoked fish (if using) and stir-fry for 2-3 minutes.",
            "Add enough water to make the soup base and bring to a boil. Add seasoning cubes, salt, and pepper.",
            "Add the mixed seafood and crayfish. Cook until the seafood is just tender (do not overcook).",
            "Stir in the shredded leaves and cook for 2 minutes. Taste and adjust seasoning.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "40 mins",
        "servings": 4,
        "category": "Dinner",
        "calories": 420,
        "difficulty": "Medium",
        "prep_time": "15 mins",
        "cook_time": "25 mins",
        "tips": [
            "Use fresh, high-quality seafood for the best flavor.",
            "Do not overcook the seafood, as it can become tough and rubbery.",
            "The soup is naturally spicy, so adjust the amount of peppers to your liking."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "10g",
            "fat": "20g",
            "fiber": "2g"
        }
    },
    "Oha Soup": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe), cooked",
            "1 cup sliced oha leaves",
            "1/2 cup cocoyam, blended into a paste for thickening",
            "1/2 cup ground crayfish",
            "1/2 cup smoked fish, deboned",
            "1/2 cup palm oil",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1/4 cup oziza leaves (thinly sliced, optional)"
        ],
        "steps": [
            "Boil the assorted meat with chopped onions, salt, and seasoning cubes until tender.",
            "Add the palm oil to the boiling meat stock. Stir and bring to a simmer.",
            "Add the blended cocoyam paste in small lumps. Stir until it dissolves and the soup thickens.",
            "Add the ground crayfish, smoked fish, and oziza leaves (if using). Simmer for 5 minutes.",
            "Add the oha leaves last. Do not stir too much to avoid breaking the leaves. Cook for 2-3 minutes.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "1 hr 30 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 450,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "1 hr",
        "tips": [
            "Use fresh oha leaves, which have a distinctive flavor.",
            "Add the oha leaves at the very end to prevent them from becoming mushy.",
            "The oziza leaves add a slightly peppery taste to the soup."
        ],
        "nutritional_info": {
            "protein": "20g",
            "carbs": "40g",
            "fat": "25g",
            "fiber": "8g"
        }
    },
    "Afang Soup": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe), cooked",
            "2 cups afang leaves, pounded or blended",
            "1 cup water leaf, sliced",
            "1/2 cup ground crayfish",
            "1/2 cup smoked fish, deboned",
            "1/2 cup palm oil",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1 large onion, chopped"
        ],
        "steps": [
            "Boil the assorted meat with chopped onion, salt, and seasoning cubes until tender.",
            "Add the smoked fish and crayfish to the pot. Stir and cook for 5 minutes.",
            "Add the palm oil and sliced water leaf. Cook until the water leaf is soft.",
            "Add the pounded afang leaves and stir well. Cook for 5 minutes (do not cover the pot).",
            "Taste and adjust seasoning with salt and pepper as needed.",
            "Serve hot with fufu or pounded yam."
        ],
        "time": "1 hr 30 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 480,
        "difficulty": "Hard",
        "prep_time": "45 mins",
        "cook_time": "45 mins",
        "tips": [
            "Afang leaves are traditionally pounded, but blending them with a little water can work too.",
            "The water leaf adds a natural thickening to the soup.",
            "It is important to cook the afang soup without a lid to preserve the vibrant green color."
        ],
        "nutritional_info": {
            "protein": "22g",
            "carbs": "30g",
            "fat": "30g",
            "fiber": "12g"
        }
    },
     "Edikaikong": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe)",
            "1 cup waterleaf, sliced",
            "2 cups Ugwu (pumpkin) leaves, shredded",
            "1/2 cup palm oil",
            "1/2 cup ground crayfish",
            "1/2 cup smoked fish, deboned",
            "1/4 cup periwinkles (optional)",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1 medium-sized onion, chopped"
        ],
        "steps": [
            "Boil the assorted meat with chopped onion, salt, and seasoning cubes until tender.",
            "Add the palm oil to the pot with the meat and stock. Stir and bring to a simmer.",
            "Add the smoked fish, crayfish, and periwinkles (if using). Cook for 5 minutes.",
            "Add the waterleaf and stir. Cook for 3-5 minutes until it wilts and releases its own water.",
            "Add the Ugwu leaves and stir quickly. Reduce heat and simmer for another 2-3 minutes. Do not overcook.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "1 hr 15 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 450,
        "difficulty": "Medium",
        "prep_time": "20 mins",
        "cook_time": "55 mins",
        "tips": [
            "Ugwu and waterleaf are the key ingredients. Use a generous amount of both.",
            "Do not add water after the waterleaf, as it releases its own liquid.",
            "The soup should have a slightly crunchy texture from the vegetables. Avoid overcooking."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "20g",
            "fat": "25g",
            "fiber": "15g"
        }
    },
    "Ukwa (African Breadfruit)": {
        "ingredients": [
            "2 cups dried ukwa (African breadfruit)",
            "1/4 cup edible potash (akanwu), dissolved in water",
            "1/4 cup palm oil",
            "1 cup sweet corn",
            "1/2 cup smoked fish, deboned",
            "1/2 cup dried prawns",
            "2 bouillon cubes",
            "Salt and pepper to taste"
        ],
        "steps": [
            "Soak the dried ukwa overnight or for several hours to soften.",
            "Boil the ukwa with a small amount of potash solution until it is very tender and the seeds have opened up.",
            "Drain the excess water, but leave a little in the pot to form a sauce.",
            "Add the palm oil and stir. The potash will make the oil turn a light yellow color.",
            "Add the sweet corn, smoked fish, and dried prawns. Stir and simmer for 5 minutes.",
            "Add the seasoning cubes, salt, and pepper to taste.",
            "Serve hot as a one-pot meal."
        ],
        "time": "2 hrs",
        "servings": 4,
        "category": "Lunch/Dinner",
        "calories": 550,
        "difficulty": "Medium",
        "prep_time": "8 hrs (soaking) + 10 mins",
            "cook_time": "1 hr 50 mins",
        "tips": [
            "Soaking the ukwa is essential for proper cooking.",
            "The potash is necessary to soften the ukwa and give the soup its unique color and texture.",
            "Ukwa is often prepared as a porridge, but it can also be roasted."
        ],
        "nutritional_info": {
            "protein": "15g",
            "carbs": "70g",
            "fat": "25g",
            "fiber": "10g"
        }
    },
    "Abacha (African Salad)": {
        "ingredients": [
            "2 cups dried shredded cassava (abacha)",
            "1/2 cup palm oil",
            "1 tbsp edible potash (akanwu), dissolved in water",
            "1/2 cup ground crayfish",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1 small onion, sliced",
            "1/2 cup utazi leaves, sliced",
            "Garden eggs, sliced (for garnish)"
        ],
        "steps": [
            "Place the dried abacha in a bowl and pour hot water over it. Soak for 5-10 minutes until soft.",
            "Drain the water completely and set the abacha aside.",
            "In a separate bowl, mix the palm oil with the potash solution until it turns into a thick, yellowish paste.",
            "Add the ground crayfish, seasoning cubes, salt, and pepper to the palm oil mixture. Stir well.",
            "Add the rehydrated abacha to the sauce and mix thoroughly.",
            "Add the sliced onions and utazi leaves. Mix gently.",
            "Serve the abacha garnished with sliced garden eggs, fried fish, or ponmo."
        ],
        "time": "30 mins",
        "servings": 4,
        "category": "Salad/Appetizer",
        "calories": 350,
        "difficulty": "Easy",
        "prep_time": "20 mins",
        "cook_time": "10 mins",
        "tips": [
            "Make sure the abacha is fully drained to prevent a watery salad.",
            "Utazi leaves are a key part of the flavor, so don't skip them.",
            "Abacha can be served warm or at room temperature."
        ],
        "nutritional_info": {
            "protein": "8g",
            "carbs": "45g",
            "fat": "15g",
            "fiber": "5g"
        }
    },
    "Ogbono Soup": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe)",
            "1/2 cup ground ogbono seeds",
            "1/2 cup palm oil",
            "1/2 cup ground crayfish",
            "1/2 cup smoked fish, deboned",
            "1 large onion, chopped",
            "2 bouillon cubes",
            "Salt and pepper to taste",
            "1/2 cup fluted pumpkin leaves (ugwu) or bitter leaf, shredded (optional)"
        ],
        "steps": [
            "Boil the assorted meat with chopped onion, salt, and seasoning cubes until tender. Set aside the meat stock.",
            "In a separate pot, heat the palm oil. Add the ground ogbono and stir until it dissolves into a lump-free paste.",
            "Gradually add the hot meat stock to the ogbono paste, stirring constantly to prevent lumps and to get the desired 'draw' (viscous) consistency.",
            "Add the cooked meat, smoked fish, and crayfish to the pot. Simmer for 10-15 minutes, stirring occasionally.",
            "Taste and adjust seasoning with salt and pepper as needed.",
            "Add the shredded leaves (if using) and stir gently. Cook for 2-3 minutes.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "1 hr 15 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 480,
        "difficulty": "Medium",
        "prep_time": "20 mins",
        "cook_time": "55 mins",
        "tips": [
            "Stir the ogbono constantly when adding the stock to prevent lumps.",
            "Do not cover the pot while the ogbono is cooking to maintain its drawing ability.",
            "You can use various leaves in ogbono soup, but ugwu is a popular choice."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "40g",
            "fat": "25g",
            "fiber": "10g"
        }
    },
    "Bitter Leaf Soup": {
        "ingredients": [
            "1 lb assorted meat (beef, shaki, cow tripe)",
            "2 cups bitter leaf, well-washed",
            "1/2 cup cocoyam, blended into a paste",
            "1/2 cup ground crayfish",
            "1/2 cup smoked fish, deboned",
            "1/2 cup palm oil",
            "1 large onion, chopped",
            "2 bouillon cubes",
            "Salt and pepper to taste"
        ],
        "steps": [
            "Boil the assorted meat with chopped onions, salt, and seasoning cubes until very tender. Set aside.",
            "Add the palm oil to the boiling meat stock. Stir and bring to a simmer.",
            "Add the blended cocoyam paste in small lumps. Stir until it dissolves and the soup begins to thicken.",
            "Add the ground crayfish and smoked fish. Stir well and allow to simmer for 5 minutes.",
            "Add the well-washed bitter leaf. Stir well and allow to simmer for another 5-10 minutes.",
            "Taste and adjust seasoning with salt and pepper as needed.",
            "Serve hot with fufu, garri, or pounded yam."
        ],
        "time": "1 hr 30 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 480,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "1 hr",
        "tips": [
            "The key to a good bitter leaf soup is to wash the bitter leaf thoroughly until there is no bitterness left.",
            "The cocoyam paste is the traditional thickener, but a thickener like achi or ofor can also be used.",
            "The soup is ready when it is thick and has a rich, earthy flavor."
        ],
        "nutritional_info": {
            "protein": "25g",
            "carbs": "45g",
            "fat": "25g",
            "fiber": "10g"
        }
    },
    
    # More Nigerian dishes to reach 50...
    "Miyan Kuka": {
    "ingredients": [
        "1/2 cup kuka powder (baobab leaf powder)",
        "500 g beef (cut into chunks)",
        "1 cup dried fish (washed and deboned)",
        "1/2 cup ground crayfish",
        "2 tbsp ground pepper",
        "1 large onion (chopped)",
        "2 tbsp ground locust beans (dawadawa)",
        "3 seasoning cubes",
        "Salt to taste",
        "3 tbsp palm oil",
        "5 cups water"
    ],
    "steps": [
        "Wash beef and season with salt, pepper, and one seasoning cube.",
        "Boil meat with chopped onion until tender, adding more water as needed.",
        "Add palm oil, ground pepper, crayfish, dawadawa, and dried fish to the pot.",
        "Stir and allow to cook for 10 minutes.",
        "Gradually sprinkle kuka powder into the soup while stirring to prevent lumps.",
        "Simmer on low heat for 5–10 minutes until thick and smooth.",
        "Serve hot with Tuwo Shinkafa or any preferred swallow."
    ],
    "time": "45 mins",
    "servings": 4,
    "category": "Lunch",
    "calories": 320,
    "difficulty": "Medium"
},

"Tuwo Shinkafa": {
    "ingredients": [
        "3 cups short-grain rice",
        "4–5 cups water",
        "Pinch of salt"
    ],
    "steps": [
        "Wash rice thoroughly and pour into a pot with water.",
        "Cook on medium heat until soft and mushy, stirring occasionally.",
        "Mash the cooked rice with a wooden spoon until smooth.",
        "Sprinkle a little water if needed and mold into smooth balls.",
        "Serve hot with Miyan Kuka, Miyan Taushe, or any Northern soup."
    ],
    "time": "40 mins",
    "servings": 4,
    "category": "Lunch",
    "calories": 250,
    "difficulty": "Easy"
},
"Dan Wake": {
    "ingredients": [
        "2 cups bean flour",
        "2 tbsp cassava flour",
        "1 tsp potash (dissolved in water)",
        "Pinch of salt",
        "Warm water (as needed)",
        "1 tbsp ground pepper",
        "Spring onions and boiled eggs for garnish"
    ],
    "steps": [
        "In a bowl, mix bean flour, cassava flour, salt, and ground pepper.",
        "Add dissolved potash solution and mix with warm water to form a thick dough.",
        "Pinch small portions of the dough and roll into oval dumplings.",
        "Drop dumplings into boiling water and cook until they float (about 10 minutes).",
        "Remove and drain excess water.",
        "Serve with ground pepper sauce, fried oil, boiled eggs, and spring onions."
    ],
    "time": "30 mins",
    "servings": 3,
    "category": "Snack",
    "calories": 180,
    "difficulty": "Medium"
},
"Masa": {
    "ingredients": [
        "3 cups rice (2 cups soaked overnight, 1 cup cooked)",
        "1 tsp yeast",
        "2 tbsp sugar",
        "Pinch of salt",
        "Warm water (as needed)",
        "Vegetable oil (for greasing pan)"
    ],
    "steps": [
        "Soak 2 cups of rice overnight, then rinse and blend with 1 cup of cooked rice into a smooth paste.",
        "Dissolve yeast and sugar in warm water and add to the rice paste.",
        "Mix well, cover, and allow to ferment for 6–8 hours or overnight.",
        "Heat a masa pan or small frying pan and lightly grease with oil.",
        "Pour batter into the molds and cook on low heat until the bottom sets.",
        "Flip and cook the other side briefly until golden.",
        "Serve hot with miyan taushe, honey, or suya."
    ],
    "time": "8 hours (including fermentation)",
    "servings": 6,
    "category": "Breakfast",
    "calories": 160,
    "difficulty": "Hard"
},
    "Kilishi": {
    "ingredients": [
        "1 kg beef (lean, thinly sliced)",
        "1/2 cup groundnut powder",
        "2 tbsp ground pepper (cayenne or chili)",
        "1 tbsp ground ginger",
        "1 tbsp ground cloves",
        "2 tbsp suya spice mix",
        "2 seasoning cubes",
        "Salt to taste"
    ],
    "steps": [
        "Slice beef into thin, flat pieces.",
        "Season slices with salt and suya spices, then leave to marinate for 1 hour.",
        "Dry the meat under the sun or in a low oven (50–60°C) until firm but not brittle.",
        "Mix groundnut powder with spices and a little water to form a paste.",
        "Coat the dried meat with the spiced groundnut paste.",
        "Return meat to the sun or oven to dry completely until crisp.",
        "Store in an airtight container and enjoy as a snack."
    ],
    "time": "6-8 hours (including drying time)",
    "servings": 4,
    "category": "Snack",
    "calories": 400,
    "difficulty": "Hard"
},
"Gurasa": {
    "ingredients": [
        "4 cups wheat flour",
        "2 tsp yeast",
        "1 tsp sugar",
        "1 tsp salt",
        "1 tbsp oil",
        "Warm water (as needed)"
    ],
    "steps": [
        "Mix yeast, sugar, and warm water; let it activate for 10 minutes.",
        "Add flour, salt, and oil; mix into a soft dough.",
        "Knead well for 10 minutes and cover to rise for 1 hour.",
        "Divide dough into small balls and flatten slightly.",
        "Heat a non-stick pan or clay griddle on low heat.",
        "Cook each Gurasa on both sides until golden brown and soft.",
        "Serve warm with Miyan Kuka or any preferred soup."
    ],
    "time": "90 mins",
    "servings": 4,
    "category": "Breakfast",
    "calories": 220,
    "difficulty": "Medium"
},
"Kosai": {
    "ingredients": [
        "2 cups black-eyed beans",
        "1 medium onion (chopped)",
        "2 fresh peppers (scotch bonnet)",
        "Salt to taste",
        "Vegetable oil (for frying)"
    ],
    "steps": [
        "Soak beans in water for 30 minutes and peel off the skins.",
        "Blend peeled beans with onions and peppers to a smooth paste.",
        "Add salt and mix until fluffy.",
        "Heat oil in a deep pan over medium heat.",
        "Scoop spoonfuls of the batter into hot oil.",
        "Fry until golden brown on both sides.",
        "Drain on paper towels and serve hot."
    ],
    "time": "45 mins",
    "servings": 4,
    "category": "Breakfast",
    "calories": 170,
    "difficulty": "Easy"
},
"Fura": {
    "ingredients": [
        "2 cups millet flour",
        "1 tsp ground ginger",
        "1/2 tsp ground cloves",
        "Pinch of salt",
        "Water as needed"
    ],
    "steps": [
        "Mix millet flour, ginger, cloves, and salt in a bowl.",
        "Add hot water gradually and mix into a firm dough.",
        "Form small balls from the dough.",
        "Steam the balls in a pot for 30 minutes until cooked.",
        "Serve with nono (fermented milk) or any preferred drink."
    ],
    "time": "40 mins",
    "servings": 3,
    "category": "Snack",
    "calories": 200,
    "difficulty": "Medium"
},
"Dambu": {
    "ingredients": [
        "2 cups rice",
        "500 g beef or chicken",
        "2 tbsp ground pepper",
        "1 tbsp suya spice",
        "Salt to taste",
        "1 onion (chopped)",
        "Vegetables (optional)"
    ],
    "steps": [
        "Cook rice until soft, then drain excess water.",
        "Boil meat with seasoning, then shred into small pieces.",
        "Mix shredded meat with rice and suya spice.",
        "Add pepper, chopped onion, and vegetables if desired.",
        "Fry mixture in a dry pan for 5 minutes to remove moisture.",
        "Serve warm with sauce or alone."
    ],
    "time": "50 mins",
    "servings": 4,
    "category": "Lunch",
    "calories": 350,
    "difficulty": "Medium"
},
"Kuli Kuli": {
    "ingredients": [
        "2 cups groundnuts (roasted and peeled)",
        "1 tsp ground pepper",
        "Salt to taste",
        "Vegetable oil for frying"
    ],
    "steps": [
        "Grind roasted groundnuts into a fine paste.",
        "Add pepper and salt to taste.",
        "Squeeze out excess oil from the paste (using a cloth or press).",
        "Shape the paste into sticks, rings, or balls.",
        "Deep fry the shapes in hot oil until golden brown.",
        "Drain on paper towels and allow to cool.",
        "Store in an airtight container."
    ],
    "time": "60 mins",
    "servings": 6,
    "category": "Snack",
    "calories": 280,
    "difficulty": "Medium"
},
  "Zobo": {
    "ingredients": [
        "2 cups dried hibiscus petals (zobo leaves)",
        "1 medium fresh ginger (peeled and sliced)",
        "2 cloves garlic (optional)",
        "4 cups water",
        "1 cucumber (thinly sliced)",
        "1 cup watermelon (diced)",
        "1 cup pineapple (diced)",
        "2 oranges (juiced)",
        "1 lemon (juiced)",
        "Fresh mint leaves (a few sprigs)",
        "Honey or sugar (to taste)"
    ],
    "steps": [
        "Wash zobo leaves thoroughly under cold water to remove dust and dirt.",
        "In a large pot, bring 4 cups of water to a boil.",
        "Add ginger slices and garlic (if using) to the boiling water and let it boil for 5 minutes.",
        "Add the zobo leaves and simmer for 10–15 minutes until the water turns a deep red color and flavors are infused.",
        "Turn off the heat and let the mixture cool slightly.",
        "Strain the liquid into a clean container and discard the used leaves and spices.",
        "Once cooled, add orange juice, lemon juice, and sweeten with honey or sugar to taste.",
        "Add sliced cucumber, watermelon, pineapple chunks, and fresh mint leaves for added flavor.",
        "Chill in the refrigerator for at least 2 hours before serving.",
        "Serve cold over ice with fruit pieces for garnish."
    ],
    "time": "30 mins + 2 hrs chilling",
    "servings": 4,
    "category": "Drink",
    "calories": 50,
    "difficulty": "Easy"
},
"Kunu": {
    "ingredients": [
        "2 cups tiger nuts (soaked overnight)",
        "10 fresh dates (pitted)",
        "1-inch piece fresh ginger",
        "1 liter cold water",
        "Pinch of cloves (optional)"
    ],
    "steps": [
        "Soak tiger nuts in clean water overnight or for at least 8–12 hours to soften them.",
        "Remove seeds from the dates and rinse thoroughly.",
        "Peel and slice the ginger.",
        "In a blender, add soaked tiger nuts, dates, ginger, and optional cloves with some cold water.",
        "Blend until very smooth.",
        "Pour the mixture through a fine sieve or cheesecloth into a clean bowl to extract the milk.",
        "Repeat the blending process with the remaining chaff and water to get more extract.",
        "Sweeten with additional dates or honey if desired.",
        "Chill in the refrigerator before serving.",
        "Serve cold as a refreshing and nutritious drink."
    ],
    "time": "20 mins (plus soaking time)",
    "servings": 3,
    "category": "Drink",
    "calories": 120,
    "difficulty": "Easy"
},

    # Intercontinental Dishes
    "Spaghetti Carbonara": {
        "ingredients": [
            "1 lb spaghetti pasta",
            "6 large egg yolks",
            "1 whole egg",
            "1 cup freshly grated Parmigiano-Reggiano cheese, plus more for serving",
            "8 oz guanciale or pancetta, diced into 1/4-inch pieces",
            "1/2 cup dry white wine (optional)",
            "Freshly cracked black pepper (lots of it!)",
            "Sea salt for pasta water",
            "2 tablespoons extra virgin olive oil",
            "2 cloves garlic, lightly crushed (optional, not traditional)"
        ],
        "steps": [
            "Prepare mise en place: Bring a large pot of salted water to boil. In a large bowl, whisk together egg yolks, whole egg, and grated cheese. Season generously with black pepper.",
            "Cook pasta: Add spaghetti to boiling water and cook according to package directions until al dente. Reserve 2 cups of pasta cooking water before draining.",
            "Render guanciale: While pasta cooks, heat olive oil in a large skillet over medium heat. Add guanciale and cook until golden and crispy, about 5-7 minutes.",
            "Deglaze (optional): Add white wine to the pan with guanciale and let it reduce by half, scraping up any browned bits.",
            "Temper eggs: Slowly add 1/2 cup of hot pasta water to the egg mixture, whisking constantly to prevent scrambling.",
            "Combine pasta and guanciale: Add drained hot pasta to the skillet with guanciale. Toss to coat with the rendered fat.",
            "Create the sauce: Remove pan from heat. Quickly pour the egg mixture over the pasta, tossing vigorously with tongs for 2-3 minutes.",
            "Adjust consistency: Add more pasta water gradually until you achieve a silky, creamy sauce that coats each strand.",
            "Final seasoning: Taste and adjust with more cheese, pepper, or salt as needed. Serve immediately in warm bowls."
        ],
        "time": "30 mins",
        "servings": 4,
        "category": "Dinner",
        "calories": 620,
        "difficulty": "Medium",
        "prep_time": "10 mins",
        "cook_time": "20 mins",
        "tips": [
            "The key is to work quickly and keep the pasta hot when adding eggs",
            "Never add cream - authentic carbonara uses only eggs and cheese",
            "Use the starchy pasta water to create the silky sauce",
            "Guanciale is traditional, but pancetta or good bacon works too",
            "Serve immediately in warmed bowls for the best experience"
        ],
        "nutritional_info": {
            "protein": "28g",
            "carbs": "68g",
            "fat": "24g",
            "fiber": "3g"
        }
    },
    "Chicken Tikka Masala": {
        "ingredients": [
            "For the chicken:",
            "2 lbs boneless chicken thighs or breasts, cut into chunks",
            "1 cup plain Greek yogurt",
            "2 tablespoons lemon juice",
            "2 teaspoons garam masala",
            "1 teaspoon ground cumin",
            "1 teaspoon paprika",
            "1/2 teaspoon turmeric",
            "4 garlic cloves, minced",
            "1-inch piece ginger, grated",
            "1 teaspoon salt",
            "For the masala sauce:",
            "2 tablespoons ghee or vegetable oil",
            "1 large onion, finely chopped",
            "4 garlic cloves, minced",
            "1-inch piece ginger, grated",
            "1 teaspoon ground cumin",
            "1 teaspoon ground coriander",
            "1 teaspoon paprika",
            "1/2 teaspoon turmeric",
            "1/4 teaspoon cayenne pepper",
            "1 can (28 oz) crushed tomatoes",
            "1 cup heavy cream",
            "1 teaspoon salt",
            "1 tablespoon tomato paste",
            "Fresh cilantro for garnish",
            "Basmati rice for serving"
        ],
        "steps": [
            "Marinate chicken: Combine yogurt, lemon juice, garam masala, cumin, paprika, turmeric, garlic, ginger, and salt. Add chicken and marinate for at least 1 hour (preferably 4-8 hours).",
            "Cook chicken: Heat oil in a large skillet over medium-high heat. Remove chicken from marinade and cook until browned and cooked through, about 6-8 minutes. Set aside.",
            "Start sauce: In the same pan, add ghee and sauté onions until softened and lightly golden, about 5-7 minutes.",
            "Add aromatics: Add garlic and ginger, cook for 1 minute until fragrant.",
            "Toast spices: Add cumin, coriander, paprika, turmeric, and cayenne. Cook for 30 seconds until fragrant.",
            "Build sauce base: Stir in tomato paste and cook for 1 minute. Add crushed tomatoes and simmer for 10-15 minutes until thickened.",
            "Finish sauce: Stir in heavy cream and return chicken to the pan. Simmer for 5 minutes to heat through and meld flavors.",
            "Season and serve: Adjust salt and spices to taste. Garnish with fresh cilantro and serve over basmati rice with naan bread."
        ],
        "time": "75 mins (plus marination)",
        "servings": 6,
        "category": "Dinner",
        "calories": 485,
        "difficulty": "Medium",
        "prep_time": "20 mins",
        "cook_time": "55 mins",
        "tips": [
            "Marinate chicken longer for deeper flavor - overnight is ideal",
            "Use chicken thighs for juicier, more flavorful results",
            "Don't skip browning the chicken - it adds crucial flavor",
            "Simmer the tomato base long enough to remove acidity",
            "Adjust cream and spices to your preferred richness and heat level"
        ],
        "nutritional_info": {
            "protein": "38g",
            "carbs": "18g",
            "fat": "26g",
            "fiber": "4g"
        }
    },
"Beef Tacos": {
    "ingredients": [
        "500g ground beef",
        "8 small taco shells",
        "1 cup shredded lettuce",
        "1 cup diced tomatoes",
        "1 cup shredded cheddar cheese",
        "1/2 cup sour cream",
        "1 tbsp olive oil",
        "1 tsp chili powder",
        "1 tsp paprika",
        "1 tsp cumin",
        "Salt and pepper to taste"
    ],
    "steps": [
        "Heat olive oil in a skillet over medium heat.",
        "Add ground beef and cook until browned, breaking it apart with a spoon (about 6–8 minutes).",
        "Season beef with chili powder, paprika, cumin, salt, and pepper. Stir well and cook for 2 more minutes.",
        "Warm taco shells in a dry pan or oven for 1–2 minutes.",
        "Prepare toppings: shred lettuce, dice tomatoes, and grate cheese.",
        "Assemble tacos by adding seasoned beef into shells, then top with lettuce, tomatoes, cheese, and sour cream.",
        "Serve immediately with lime wedges and salsa if desired."
    ],
    "time": "20 mins",
    "servings": 3,
    "category": "Lunch",
    "calories": 380,
    "difficulty": "Easy"
},
"Caesar Salad": {
    "ingredients": [
        "1 head Romaine lettuce",
        "1 cup croutons",
        "1/4 cup grated Parmesan cheese",
        "1/4 cup Caesar dressing",
        "2 anchovy fillets (optional)",
        "1 tsp lemon juice",
        "Freshly ground black pepper"
    ],
    "steps": [
        "Wash and chop Romaine lettuce into bite-sized pieces.",
        "Prepare Caesar dressing (or use store-bought): mix anchovies, lemon juice, and Caesar dressing if needed.",
        "Toss lettuce with dressing in a large bowl until evenly coated.",
        "Add croutons and sprinkle with Parmesan cheese.",
        "Finish with freshly ground black pepper and serve immediately."
    ],
    "time": "15 mins",
    "servings": 2,
    "category": "Lunch",
    "calories": 220,
    "difficulty": "Easy"
},
"Pad Thai": {
    "ingredients": [
        "200g rice noodles",
        "200g shrimp (peeled and deveined)",
        "2 eggs",
        "1 cup bean sprouts",
        "3 tbsp tamarind paste",
        "2 tbsp fish sauce",
        "1 tbsp soy sauce",
        "1 tbsp sugar",
        "2 cloves garlic (minced)",
        "1/4 cup crushed peanuts",
        "1 lime (cut into wedges)",
        "2 tbsp vegetable oil",
        "Chopped cilantro for garnish"
    ],
    "steps": [
        "Soak rice noodles in warm water for 20–30 minutes until softened, then drain.",
        "In a small bowl, mix tamarind paste, fish sauce, soy sauce, and sugar to make the sauce.",
        "Heat oil in a wok over medium-high heat. Add garlic and stir-fry until fragrant (30 seconds).",
        "Add shrimp and cook until pink (about 2 minutes). Push to the side.",
        "Crack eggs into the wok, scramble until just set, then mix with shrimp.",
        "Add noodles and pour sauce over them. Toss everything together for 3–4 minutes.",
        "Add bean sprouts and half of the peanuts. Stir for 1 more minute.",
        "Serve hot, topped with remaining peanuts, cilantro, and lime wedges."
    ],
    "time": "30 mins",
    "servings": 2,
    "category": "Dinner",
    "calories": 400,
    "difficulty": "Medium"
},
"Greek Moussaka": {
    "ingredients": [
        "2 large eggplants (sliced)",
        "500g ground lamb or beef",
        "1 onion (diced)",
        "2 cloves garlic (minced)",
        "2 cupscrushed tomatoes",
        "1 tsp cinnamon",
        "1 tsp oregano",
        "Salt and pepper to taste",
        "2 cups bechamel sauce",
        "1/2 cup grated Parmesan cheese",
        "Olive oil for frying"
    ],
    "steps": [
        "Preheat oven to 375°F (190°C).",
        "Slice eggplants and sprinkle with salt to remove bitterness. Let sit for 20 minutes, then pat dry.",
        "Heat olive oil in a skillet and fry eggplant slices until golden. Set aside.",
        "In the same skillet, sauté onion and garlic until soft. Add ground meat and cook until browned.",
        "Add crushed tomatoes, cinnamon, oregano, salt, and pepper. Simmer for 15 minutes.",
        "Prepare bechamel sauce if not pre-made.",
        "In a baking dish, layer eggplant slices, then meat sauce, and repeat until all are used.",
        "Pour bechamel sauce on top and sprinkle with Parmesan cheese.",
        "Bake for 45 minutes until golden and bubbling. Let rest before serving."
    ],
    "time": "90 mins",
    "servings": 6,
    "category": "Dinner",
    "calories": 520,
    "difficulty": "Hard"
},
"Sushi Rolls": {
    "ingredients": [
        "2 cups sushi rice",
        "3 sheets nori (seaweed)",
        "200g fresh sushi-grade fish (salmon or tuna)",
        "1/2 avocado (sliced)",
        "1/2 cucumber (julienned)",
        "2 tbsp rice vinegar",
        "1 tbsp sugar",
        "Soy sauce (for dipping)",
        "Pickled ginger and wasabi (for serving)"
    ],
    "steps": [
        "Cook sushi rice according to package instructions, then mix with rice vinegar and sugar. Let cool.",
        "Place a sheet of nori on a bamboo sushi mat, shiny side down.",
        "Spread an even layer of rice on the nori, leaving 1 inch at the top edge uncovered.",
        "Arrange fish, avocado, and cucumber in a line across the middle of the rice.",
        "Roll tightly using the mat, then seal the edge with a little water.",
        "Slice the roll into 6–8 pieces using a sharp knife.",
        "Serve with soy sauce, pickled ginger, and wasabi."
    ],
    "time": "40 mins",
    "servings": 3,
    "category": "Lunch",
    "calories": 300,
    "difficulty": "Medium"
},
"French Onion Soup": {
    "ingredients": [
        "4 large onions (thinly sliced)",
        "6 cups beef broth",
        "1/2 cup dry white wine",
        "2 tbsp butter",
        "1 tbsp olive oil",
        "1 tsp sugar",
        "Salt and pepper to taste",
        "6 slices French bread",
        "1 cup grated Gruyere cheese"
    ],
    "steps": [
        "Heat butter and olive oil in a pot over medium heat.",
        "Add sliced onions and cook slowly, stirring often, until caramelized (about 30 minutes).",
        "Add sugar and cook for another 2 minutes.",
        "Pour in white wine and cook until mostly evaporated.",
        "Add beef broth, season with salt and pepper, and simmer for 20 minutes.",
        "Toast bread slices and top with Gruyere cheese.",
        "Ladle soup into oven-safe bowls, top with cheesy bread, and broil until golden.",
        "Serve hot."
    ],
    "time": "60 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 280,
    "difficulty": "Medium"
},
"Paella": {
    "ingredients": [
        "2 cups short-grain rice",
        "1/4 tsp saffron threads",
        "500g mixed seafood (shrimp, mussels, squid)",
        "300g chicken (cut into pieces)",
        "1 onion (diced)",
        "1 bell pepper (sliced)",
        "2 tomatoes (chopped)",
        "4 cups chicken broth",
        "2 tbsp olive oil",
        "1 tsp paprika",
        "Salt to taste"
    ],
    "steps": [
        "Heat olive oil in a large paella pan over medium heat.",
        "Add chicken pieces and cook until browned. Remove and set aside.",
        "In the same pan, sauté onion and bell pepper until soft, then add chopped tomatoes and paprika.",
        "Add rice and stir for 2 minutes to coat with oil.",
        "Pour in broth and saffron, bring to a simmer.",
        "Add chicken back in and cook uncovered for 15 minutes.",
        "Arrange seafood on top and cook for another 10 minutes until rice absorbs the liquid.",
        "Let rest for 5 minutes before serving."
    ],
    "time": "45 mins",
    "servings": 6,
    "category": "Dinner",
    "calories": 420,
    "difficulty": "Medium"
},
"Fish and Chips": {
    "ingredients": [
        "400g white fish fillets (cod or haddock)",
        "4 large potatoes",
        "1 cup all-purpose flour",
        "1 cup cold beer or sparkling water",
        "1 tsp baking powder",
        "Salt and pepper",
        "Oil for deep frying"
    ],
    "steps": [
        "Peel and cut potatoes into thick chips. Soak in cold water for 30 minutes, then pat dry.",
        "Heat oil in a deep fryer or large pot to 350°F (175°C).",
        "Par-fry chips for 5 minutes until soft but not golden. Remove and set aside.",
        "Mix flour, baking powder, salt, and beer to make a smooth batter.",
        "Season fish fillets with salt and pepper, then dip in batter.",
        "Fry fish in hot oil for 6–8 minutes until golden and crispy. Remove and drain on paper towels.",
        "Return chips to oil and fry until golden and crispy.",
        "Serve immediately with tartar sauce and lemon wedges."
    ],
    "time": "40 mins",
    "servings": 2,
    "category": "Lunch",
    "calories": 680,
    "difficulty": "Medium"
},
    
    # More Intercontinental dishes...
  "Beef Stroganoff": {
    "ingredients": [
      "500g beef sirloin (sliced thin)",
      "200g mushrooms (sliced)",
      "1 onion (chopped)",
      "2 cloves garlic (minced)",
      "200ml sour cream",
      "1 tbsp Dijon mustard",
      "250ml beef stock",
      "2 tbsp butter",
      "Salt and black pepper",
      "Fresh parsley (for garnish)",
      "300g egg noodles or pasta"
    ],
    "steps": [
      "Season beef slices with salt and pepper.",
      "Heat butter in a skillet, sear beef in batches, then remove.",
      "In the same skillet, sauté onions and garlic until soft.",
      "Add mushrooms and cook until browned.",
      "Pour in beef stock and mustard, then simmer for 5 minutes.",
      "Stir in sour cream and return beef to the pan.",
      "Simmer gently for 3–4 minutes without boiling.",
      "Serve hot over cooked pasta, garnish with parsley."
    ],
    "time": "35 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 520
  },
  "Chicken Parmesan": {
    "ingredients": [
      "3 chicken breasts (pounded flat)",
      "1 cup breadcrumbs",
      "1/2 cup grated Parmesan",
      "1 cup mozzarella cheese (shredded)",
      "1 cup tomato sauce",
      "2 eggs (beaten)",
      "1/2 cup all-purpose flour",
      "Salt and pepper",
      "2 tbsp olive oil",
      "Fresh basil (for garnish)"
    ],
    "steps": [
      "Preheat oven to 200°C (400°F).",
      "Season chicken with salt and pepper.",
      "Dredge chicken in flour, dip in egg, then coat with breadcrumbs and Parmesan mixture.",
      "Heat olive oil in a skillet and fry chicken until golden on both sides.",
      "Transfer to a baking dish, top each with tomato sauce and mozzarella.",
      "Bake for 15–20 minutes until cheese melts and chicken is fully cooked.",
      "Garnish with fresh basil.",
      "Serve with pasta or salad."
    ],
    "time": "40 mins",
    "servings": 3,
    "category": "Dinner",
    "calories": 480
  },
  "Ratatouille": {
    "ingredients": [
      "1 eggplant (diced)",
      "2 zucchinis (sliced)",
      "2 bell peppers (sliced)",
      "4 tomatoes (diced)",
      "1 onion (chopped)",
      "3 cloves garlic (minced)",
      "3 tbsp olive oil",
      "1 tsp dried thyme",
      "Salt and pepper",
      "Fresh basil (for garnish)"
    ],
    "steps": [
      "Preheat oven to 180°C (350°F).",
      "Heat olive oil in a pan and sauté onion and garlic until soft.",
      "Add diced tomatoes and cook for 5 minutes.",
      "In a baking dish, layer eggplant, zucchini, and bell peppers.",
      "Pour tomato mixture over layered vegetables.",
      "Season with thyme, salt, and pepper.",
      "Cover with foil and bake for 45 minutes, then uncover and bake for 15 more minutes.",
      "Serve warm, garnished with fresh basil."
    ],
    "time": "70 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 180
  },
  "Coq au Vin": {
    "ingredients": [
      "1 whole chicken (cut into pieces)",
      "250ml red wine",
      "100g bacon (diced)",
      "200g mushrooms (sliced)",
      "1 onion (chopped)",
      "2 carrots (sliced)",
      "2 cloves garlic",
      "2 tbsp tomato paste",
      "500ml chicken stock",
      "Salt, pepper, and thyme"
    ],
    "steps": [
      "Marinate chicken in wine for at least 1 hour.",
      "Fry bacon in a large pot, then remove and set aside.",
      "Brown chicken pieces in the bacon fat and remove.",
      "Sauté onion, garlic, and carrots in the pot.",
      "Stir in tomato paste, then return chicken and bacon to the pot.",
      "Add mushrooms, thyme, and chicken stock.",
      "Simmer gently for 60–75 minutes until chicken is tender.",
      "Serve hot with mashed potatoes or bread."
    ],
    "time": "90 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 450
  },
  "Beef Bourguignon": {
    "ingredients": [
      "1kg beef chuck (cubed)",
      "750ml red wine",
      "2 carrots (sliced)",
      "2 onions (chopped)",
      "2 cloves garlic",
      "2 tbsp tomato paste",
      "500ml beef stock",
      "200g mushrooms",
      "100g bacon",
      "Salt, pepper, and thyme"
    ],
    "steps": [
      "Marinate beef in wine for 2 hours or overnight.",
      "Fry bacon in a large Dutch oven, remove and set aside.",
      "Brown beef cubes in batches and remove.",
      "Sauté onion, garlic, and carrots.",
      "Stir in tomato paste, then add beef and bacon back.",
      "Pour in wine marinade and beef stock.",
      "Add mushrooms and thyme, then cover and simmer for 2.5–3 hours.",
      "Serve with mashed potatoes or crusty bread."
    ],
    "time": "180 mins",
    "servings": 6,
    "category": "Dinner",
    "calories": 520
  },
  "Lasagna": {
        "ingredients": [
            "12 lasagna noodles",
            "500 g ground beef",
            "2 cups ricotta cheese",
            "2 cups mozzarella cheese, shredded",
            "1/2 cup Parmesan cheese, grated",
            "1 jar (680 g) marinara sauce",
            "1 onion, chopped",
            "2 cloves garlic, minced",
            "2 tbsp olive oil",
            "1 egg",
            "1 tsp dried basil",
            "1 tsp dried oregano",
            "Salt and pepper to taste"
        ],
        "steps": [
            "Cook lasagna noodles according to package instructions. Drain and set aside.",
            "In a large skillet, heat olive oil over medium heat. Add onion and garlic; sauté until fragrant.",
            "Add ground beef, cook until browned. Drain excess fat.",
            "Stir in marinara sauce, basil, oregano, salt, and pepper. Simmer for 10 minutes.",
            "In a bowl, mix ricotta cheese, egg, and 1/4 cup Parmesan cheese.",
            "Preheat oven to 180°C (350°F).",
            "Spread a thin layer of meat sauce on the bottom of a baking dish.",
            "Layer noodles, ricotta mixture, meat sauce, and mozzarella cheese. Repeat layers, ending with sauce and mozzarella on top.",
            "Sprinkle remaining Parmesan cheese on top.",
            "Cover with foil and bake for 25 minutes. Remove foil and bake for another 15 minutes until cheese is golden and bubbly.",
            "Let it rest for 10 minutes before slicing and serving."
        ],
        "time": "60 mins",
        "servings": 6,
        "category": "Dinner",
        "calories": 600
},

    "Thai Green Curry": {"ingredients": ["Chicken", "Green curry paste", "Coconut milk", "Thai basil", "Vegetables"], "steps": ["Cook curry paste", "Add coconut milk", "Add chicken", "Simmer"], "time": "30 mins", "servings": 3, "category": "Dinner", "calories": 380},
   "Moroccan Tagine": {
    "ingredients": [
        "1 kg lamb or chicken pieces",
        "2 onions, finely chopped",
        "3 tbsp olive oil",
        "2 tsp ground cumin",
        "2 tsp ground cinnamon",
        "1 tsp ground ginger",
        "1 tsp turmeric",
        "150 g dried apricots",
        "50 g raisins",
        "50 g almonds, toasted",
        "500 ml chicken stock",
        "Salt to taste",
        "Fresh coriander for garnish"
    ],
    "steps": [
        "Heat olive oil in a heavy-bottomed pot or tagine.",
        "Add chopped onions and sauté until golden brown.",
        "Add lamb pieces and brown on all sides.",
        "Stir in cumin, cinnamon, ginger, and turmeric. Cook for 1 minute to release aromas.",
        "Add chicken stock and bring to a simmer.",
        "Cover and cook on low heat for 1.5–2 hours until meat is tender.",
        "Add dried apricots and raisins. Cook for an additional 15 minutes.",
        "Sprinkle toasted almonds on top before serving.",
        "Garnish with fresh coriander and serve with couscous or bread."
    ],
    "time": "120 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 480
},

"Korean Bulgogi": {
    "ingredients": [
        "500 g beef sirloin, thinly sliced",
        "4 tbsp soy sauce",
        "2 tbsp sugar",
        "1 tbsp sesame oil",
        "3 cloves garlic, minced",
        "1 Asian pear, grated",
        "1 tbsp sesame seeds",
        "1 small onion, sliced",
        "2 green onions, chopped",
        "Fresh lettuce leaves (for serving)"
    ],
    "steps": [
        "In a bowl, mix soy sauce, sugar, sesame oil, garlic, grated pear, and sesame seeds.",
        "Add sliced beef and marinate for at least 30 minutes (preferably 2 hours in the fridge).",
        "Heat a grill pan or skillet over high heat.",
        "Cook the marinated beef slices for 2-3 minutes per side until cooked and caramelized.",
        "Serve hot with rice, lettuce wraps, and kimchi."
    ],
    "time": "25 mins (plus marinating)",
    "servings": 3,
    "category": "Dinner",
    "calories": 420
},

"Indian Butter Chicken": {
    "ingredients": [
        "500 g boneless chicken",
        "200 g plain yogurt",
        "2 tbsp lemon juice",
        "2 tbsp butter",
        "1 large onion, finely chopped",
        "3 tomatoes, pureed",
        "150 ml heavy cream",
        "2 tsp garam masala",
        "1 tsp turmeric",
        "1 tsp chili powder",
        "1 tsp cumin powder",
        "Salt to taste",
        "Fresh coriander for garnish"
    ],
    "steps": [
        "Marinate chicken in yogurt, lemon juice, and half the spices for at least 1 hour.",
        "Heat butter in a large pan, add onions, and cook until golden.",
        "Add pureed tomatoes and remaining spices; cook for 10 minutes until thickened.",
        "Add chicken pieces and cook for 15 minutes until tender.",
        "Stir in heavy cream and simmer for 5 more minutes.",
        "Garnish with coriander and serve with naan or rice."
    ],
    "time": "40 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 460
},

"Mexican Enchiladas": {
    "ingredients": [
        "8 corn tortillas",
        "2 cups shredded cooked chicken",
        "1 cup grated cheddar cheese",
        "2 cups enchilada sauce",
        "1 onion, finely chopped",
        "Fresh cilantro for garnish"
    ],
    "steps": [
        "Preheat oven to 180°C (350°F).",
        "Warm tortillas to make them pliable.",
        "Fill each tortilla with chicken and a little cheese; roll up and place seam-side down in a baking dish.",
        "Pour enchilada sauce over the tortillas and sprinkle remaining cheese on top.",
        "Bake for 20 minutes until bubbly and golden.",
        "Garnish with fresh cilantro and serve with sour cream."
    ],
    "time": "35 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 380
},

"Italian Risotto": {
    "ingredients": [
        "1 cup Arborio rice",
        "3 cups chicken or vegetable broth",
        "1/2 cup white wine",
        "1 small onion, finely chopped",
        "1 cup sliced mushrooms",
        "2 tbsp butter",
        "1/4 cup grated Parmesan cheese",
        "Salt and pepper to taste"
    ],
    "steps": [
        "Heat broth in a separate pot and keep warm.",
        "In a large pan, melt butter and sauté onions and mushrooms until softened.",
        "Add Arborio rice and toast for 2 minutes.",
        "Pour in white wine and cook until absorbed.",
        "Add warm broth one ladle at a time, stirring constantly until absorbed before adding more.",
        "Continue until rice is creamy and al dente (about 20 minutes).",
        "Stir in Parmesan cheese and season with salt and pepper.",
        "Serve hot with extra cheese on top."
    ],
    "time": "30 mins",
    "servings": 3,
    "category": "Dinner",
    "calories": 350
},

"Spanish Gazpacho": {
    "ingredients": [
        "6 ripe tomatoes",
        "1 cucumber, peeled",
        "1 red bell pepper",
        "1 small onion",
        "2 cloves garlic",
        "3 tbsp olive oil",
        "2 tbsp red wine vinegar",
        "Salt and pepper to taste"
    ],
    "steps": [
        "Chop tomatoes, cucumber, bell pepper, and onion.",
        "Add vegetables and garlic to a blender.",
        "Blend until smooth, then add olive oil, vinegar, salt, and pepper.",
        "Chill in the refrigerator for at least 2 hours.",
        "Serve cold, drizzled with extra olive oil."
    ],
    "time": "20 mins (plus chilling)",
    "servings": 4,
    "category": "Lunch",
    "calories": 120
},

"German Sauerbraten": {
    "ingredients": [
        "1.5 kg beef roast",
        "2 cups vinegar",
        "2 onions, sliced",
        "2 carrots, chopped",
        "2 cloves garlic",
        "10 peppercorns",
        "2 bay leaves",
        "Salt to taste",
        "2 tbsp sugar",
        "1/2 cup gingersnap cookies, crushed"
    ],
    "steps": [
        "Marinate beef in vinegar, onions, carrots, garlic, peppercorns, bay leaves, and sugar for 2-3 days in the fridge.",
        "Remove beef and pat dry. Brown on all sides in a large pot.",
        "Add marinade (strained) and simmer gently for 3 hours until tender.",
        "Add crushed gingersnaps to thicken the gravy.",
        "Slice beef and serve with gravy, red cabbage, and potatoes."
    ],
    "time": "240 mins (plus marinating)",
    "servings": 6,
    "category": "Dinner",
    "calories": 480
},
"Japanese Tempura": {
    "ingredients": [
        "200 g shrimp, peeled",
        "Assorted vegetables (carrot, zucchini, sweet potato)",
        "1 cup tempura flour",
        "1 cup ice-cold water",
        "Oil for deep frying",
        "Tempura dipping sauce"
    ],
    "steps": [
        "Prepare shrimp and vegetables by cutting them into uniform pieces.",
        "Mix tempura flour and ice-cold water to make a light batter (do not overmix).",
        "Heat oil in a deep pan to 180°C (350°F).",
        "Dip shrimp and vegetables into the batter and fry until golden and crisp (about 2 minutes).",
        "Drain on paper towels and serve immediately with dipping sauce."
    ],
    "time": "25 mins",
    "servings": 3,
    "category": "Lunch",
    "calories": 320
},
"Russian Borscht": {
    "ingredients": [
        "3 medium beets",
        "1/2 small cabbage, shredded",
        "1 carrot, grated",
        "1 onion, chopped",
        "1 potato, diced",
        "4 cups beef broth",
        "2 tbsp tomato paste",
        "1 tbsp vinegar",
        "Sour cream and fresh dill for garnish"
    ],
    "steps": [
        "Roast or boil beets until tender, then peel and grate.",
        "In a pot, sauté onions and carrots until soft.",
        "Add beef broth, diced potato, cabbage, and tomato paste.",
        "Add grated beets and vinegar, simmer for 30 minutes.",
        "Season with salt and pepper.",
        "Serve hot with a dollop of sour cream and fresh dill."
    ],
    "time": "90 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 180
},
"Brazilian Feijoada": {
    "ingredients": [
        "500 g black beans",
        "300 g pork shoulder, cut into chunks",
        "200 g smoked sausage, sliced",
        "100 g bacon, diced",
        "1 large onion, chopped",
        "3 cloves garlic, minced",
        "2 bay leaves",
        "1 tsp black pepper",
        "Salt to taste"
    ],
    "steps": [
        "Soak black beans overnight, then drain.",
        "In a large pot, cook bacon until crisp. Remove and set aside.",
        "Brown pork shoulder and sausage in the same pot.",
        "Add onions and garlic; sauté until fragrant.",
        "Add beans, bay leaves, and enough water to cover everything.",
        "Simmer for 2 hours, stirring occasionally, until beans and meat are tender.",
        "Season with salt and pepper.",
        "Serve with white rice and orange slices."
    ],
    "time": "150 mins",
    "servings": 6,
    "category": "Dinner",
    "calories": 550
},
"Lebanese Hummus": {
    "ingredients": [
        "400 g canned chickpeas",
        "3 tbsp tahini",
        "3 tbsp olive oil",
        "2 cloves garlic",
        "Juice of 1 lemon",
        "Salt to taste",
        "Paprika for garnish"
    ],
    "steps": [
        "Drain and rinse chickpeas.",
        "Blend chickpeas, tahini, olive oil, garlic, lemon juice, and salt until smooth.",
        "Add a little water if needed for a creamy texture.",
        "Transfer to a bowl and drizzle with olive oil.",
        "Sprinkle paprika on top before serving."
    ],
    "time": "15 mins",
    "servings": 4,
    "category": "Appetizer",
    "calories": 160
},

"Turkish Kebab": {
    "ingredients": [
        "500 g lamb mince",
        "1 onion, grated",
        "2 cloves garlic, minced",
        "1 tsp cumin",
        "1 tsp paprika",
        "1 tsp salt",
        "Fresh parsley, chopped"
    ],
    "steps": [
        "Mix lamb mince with onion, garlic, spices, and parsley.",
        "Shape into long kebabs around skewers.",
        "Grill over medium heat for 10–12 minutes, turning occasionally.",
        "Serve with flatbread, salad, and yogurt sauce."
    ],
    "time": "25 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 420
},
"Chinese Kung Pao Chicken": {
    "ingredients": [
        "500 g boneless chicken breast, diced",
        "3 tbsp soy sauce",
        "1 tbsp rice vinegar",
        "1 tbsp hoisin sauce",
        "1 tsp chili paste",
        "1 bell pepper, chopped",
        "1/2 cup roasted peanuts",
        "3 cloves garlic, minced",
        "2 tbsp oil"
    ],
    "steps": [
        "Marinate chicken in 2 tbsp soy sauce for 10 minutes.",
        "Heat oil in a wok and stir-fry chicken until cooked.",
        "Add garlic, bell pepper, and chili paste; stir-fry for 2 minutes.",
        "Add remaining soy sauce, vinegar, and hoisin sauce; mix well.",
        "Stir in peanuts and cook for 1 minute.",
        "Serve hot with steamed rice."
    ],
    "time": "20 mins",
    "servings": 3,
    "category": "Dinner",
    "calories": 380
},
"Argentine Empanadas": {
    "ingredients": [
        "500 g ground beef",
        "1 onion, chopped",
        "1 hard-boiled egg, chopped",
        "1/4 cup green olives, chopped",
        "1 tsp paprika",
        "1 tsp cumin",
        "Empanada dough (12 discs)",
        "1 egg yolk (for brushing)"
    ],
    "steps": [
        "Cook ground beef with onions until browned.",
        "Add paprika, cumin, olives, and chopped boiled egg; mix well.",
        "Cool the filling before assembling.",
        "Place filling in the center of each dough disc, fold, and seal edges.",
        "Brush with egg yolk and bake at 180°C (350°F) for 20–25 minutes until golden.",
        "Serve warm."
    ],
    "time": "40 mins",
    "servings": "12 pieces",
    "category": "Snack",
    "calories": 210
},
"Ethiopian Doro Wat": {
    "ingredients": [
        "1 kg chicken pieces",
        "3 onions, finely chopped",
        "3 tbsp berbere spice mix",
        "3 tbsp clarified butter (niter kibbeh)",
        "2 cloves garlic, minced",
        "1 tbsp ginger, minced",
        "2 hard-boiled eggs",
        "1 cup chicken broth",
        "Salt to taste"
    ],
    "steps": [
        "Dry-cook onions in a pot until they soften and caramelize.",
        "Add clarified butter, garlic, and ginger; cook for 2 minutes.",
        "Stir in berbere spice and cook for 1 minute.",
        "Add chicken pieces and coat them with spices.",
        "Pour in chicken broth and simmer for 40 minutes.",
        "Add boiled eggs and cook for another 10 minutes.",
        "Serve hot with injera bread."
    ],
    "time": "60 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 500
},
"Peruvian Ceviche": {
    "ingredients": [
        "500 g fresh white fish (sea bass), diced",
        "1 cup lime juice",
        "1 red onion, thinly sliced",
        "1 chili pepper, chopped",
        "Fresh coriander",
        "Salt to taste"
    ],
    "steps": [
        "Place diced fish in a bowl and cover with lime juice.",
        "Add sliced onions, chili, and salt.",
        "Let it marinate in the fridge for 15–20 minutes until fish turns opaque.",
        "Garnish with coriander and serve immediately with sweet potato and corn."
    ],
    "time": "25 mins",
    "servings": 3,
    "category": "Appetizer",
    "calories": 180
},
"Vietnamese Pho": {
    "ingredients": [
        "500 g beef bones",
        "300 g beef slices",
        "200 g rice noodles",
        "1 onion, charred",
        "1 piece ginger, charred",
        "2 star anise",
        "1 cinnamon stick",
        "2 cloves",
        "Fish sauce",
        "Fresh herbs (basil, cilantro)"
    ],
    "steps": [
        "Simmer beef bones with onion, ginger, and spices for 4 hours to make broth.",
        "Soak rice noodles in hot water until soft.",
        "Slice beef thinly.",
        "Strain broth and season with fish sauce.",
        "Place noodles in bowls, add beef slices, and pour hot broth on top.",
        "Garnish with fresh herbs and lime wedges."
    ],
    "time": "4 hrs 30 mins",
    "servings": 4,
    "category": "Dinner",
    "calories": 450
},
"Hungarian Goulash": {
    "ingredients": [
        "1 kg beef chuck, diced",
        "2 onions, chopped",
        "2 tbsp paprika",
        "1 bell pepper, chopped",
        "2 tomatoes, chopped",
        "4 cups beef broth",
        "2 potatoes, diced",
        "Salt and pepper to taste"
    ],
    "steps": [
        "Brown beef in a large pot and set aside.",
        "Sauté onions until golden, then stir in paprika.",
        "Add tomatoes and bell pepper; cook for 5 minutes.",
        "Return beef to pot, pour in broth, and simmer for 1.5–2 hours.",
        "Add potatoes and cook until tender.",
        "Serve hot with bread or dumplings."
    ],
    "time": "150 mins",
    "servings": 6,
    "category": "Dinner",
    "calories": 500
},

    # Cake Varieties
   "Chocolate Cake": {
        "ingredients": [
            "For the cake:",
            "2 cups all-purpose flour",
            "3/4 cup unsweetened cocoa powder (Dutch-processed preferred)",
            "2 cups granulated sugar",
            "2 teaspoons baking soda",
            "1 teaspoon baking powder",
            "1 teaspoon salt",
            "2 large eggs, room temperature",
            "1 cup buttermilk, room temperature",
            "1 cup strong black coffee, hot",
            "1/2 cup vegetable oil",
            "2 teaspoons vanilla extract",
            "For chocolate buttercream:",
            "1 cup unsalted butter, softened",
            "3-4 cups powdered sugar",
            "1/2 cup cocoa powder",
            "1/4 cup heavy cream",
            "2 teaspoons vanilla extract",
            "Pinch of salt"
        ],
        "steps": [
            "Prepare pans and oven: Preheat oven to 350°F (175°C). Grease two 9-inch round cake pans, line with parchment paper, and dust with cocoa powder.",
            "Mix dry ingredients: In a large bowl, whisk together flour, cocoa powder, sugar, baking soda, baking powder, and salt until well combined.",
            "Combine wet ingredients: In another bowl, whisk together eggs, buttermilk, oil, and vanilla until smooth.",
            "Make batter: Add wet ingredients to dry ingredients, mixing until just combined. Gradually stir in hot coffee - batter will be thin.",
            "Bake cakes: Divide batter evenly between prepared pans. Bake for 28-32 minutes or until a toothpick inserted in center comes out clean.",
            "Cool completely: Cool in pans for 10 minutes, then turn out onto wire racks to cool completely before frosting.",
            "Make buttercream: Beat butter until light and fluffy (3-4 minutes). Gradually add powdered sugar and cocoa powder, alternating with cream. Beat until smooth.",
            "Assemble cake: Place one layer on serving plate, spread frosting on top, add second layer, and frost entire cake.",
            "Serve: Let cake set for 30 minutes before slicing. Store covered at room temperature for up to 3 days."
        ],
        "time": "90 mins",
        "servings": 12,
        "category": "Dessert",
        "calories": 520,
        "difficulty": "Medium",
        "prep_time": "30 mins",
        "cook_time": "60 mins",
        "tips": [
            "Room temperature ingredients mix better and create a smoother batter",
            "Don't overmix the batter - this can make the cake tough",
            "Hot coffee enhances the chocolate flavor without making it taste like coffee",
            "Cool completely before frosting to prevent melting",
            "Use parchment paper for easy cake removal"
        ],
        "nutritional_info": {
            "protein": "6g",
            "carbs": "78g",
            "fat": "18g",
            "fiber": "4g"
        }
    },

    "Vanilla Sponge Cake": {
        "ingredients": [
            "2 cups all-purpose flour",
            "1 ½ cups granulated sugar",
            "4 large eggs",
            "1 cup unsalted butter (softened)",
            "2 teaspoons vanilla extract",
            "2 teaspoons baking powder",
            "½ teaspoon salt",
            "½ cup whole milk"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease two 8-inch round cake pans.",
            "In a mixing bowl, cream butter and sugar together until light and fluffy.",
            "Add eggs one at a time, beating well after each addition.",
            "Stir in vanilla extract.",
            "In a separate bowl, whisk together flour, baking powder, and salt.",
            "Gradually add dry ingredients to the wet mixture, alternating with milk. Mix until smooth.",
            "Divide batter evenly into prepared pans and smooth the tops.",
            "Bake for 30-35 minutes or until a toothpick comes out clean.",
            "Cool in pans for 10 minutes, then transfer to a wire rack to cool completely."
        ],
        "time": "45 mins",
        "servings": 6,
        "category": "Dessert",
        "calories": 320,
        "difficulty": "Easy",
        "prep_time": "15 mins",
        "cook_time": "30 mins",
        "tips": [
            "Ensure butter is at room temperature for proper creaming.",
            "Do not overmix after adding flour to keep the cake light.",
            "Check doneness with a toothpick in the center."
        ],
        "nutritional_info": {
            "protein": "6g",
            "carbs": "50g",
            "fat": "12g",
            "fiber": "1g"
        }
    },

    "Red Velvet Cake": {
        "ingredients": [
            "2 ½ cups all-purpose flour",
            "2 tablespoons cocoa powder",
            "1 teaspoon baking soda",
            "½ teaspoon salt",
            "1 ½ cups granulated sugar",
            "1 cup vegetable oil",
            "2 large eggs",
            "1 cup buttermilk",
            "2 tablespoons red food coloring",
            "1 teaspoon vanilla extract",
            "1 teaspoon white vinegar",
            "Cream cheese frosting (for filling and decoration)"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease two 9-inch round cake pans.",
            "In a bowl, whisk together flour, cocoa powder, baking soda, and salt.",
            "In a large bowl, beat sugar and oil until combined. Add eggs one at a time.",
            "Mix in buttermilk, vanilla, and food coloring.",
            "Add dry ingredients to wet mixture in 2 additions, mixing gently.",
            "Stir in vinegar at the end.",
            "Divide batter into pans and bake for 25-30 minutes or until a toothpick comes out clean.",
            "Cool completely before frosting with cream cheese frosting."
        ],
        "time": "90 mins",
        "servings": 10,
        "category": "Dessert",
        "calories": 480,
        "difficulty": "Intermediate",
        "prep_time": "30 mins",
        "cook_time": "30 mins",
        "tips": [
            "Use gel food coloring for vibrant color.",
            "Do not overmix the batter after adding flour.",
            "Cool cakes completely before frosting."
        ],
        "nutritional_info": {
            "protein": "6g",
            "carbs": "65g",
            "fat": "20g",
            "fiber": "2g"
        }
    },

    "Carrot Cake": {
        "ingredients": [
            "2 cups all-purpose flour",
            "2 cups grated carrots",
            "1 cup granulated sugar",
            "1 cup brown sugar",
            "1 cup vegetable oil",
            "4 large eggs",
            "2 teaspoons baking powder",
            "1 teaspoon baking soda",
            "1 teaspoon ground cinnamon",
            "½ teaspoon nutmeg",
            "½ teaspoon salt",
            "1 cup crushed pineapple (drained)",
            "½ cup chopped walnuts (optional)",
            "Cream cheese frosting (for filling and topping)"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease two 9-inch cake pans.",
            "In a large bowl, whisk eggs and sugars until smooth.",
            "Add oil and mix well.",
            "Stir in grated carrots and pineapple.",
            "In a separate bowl, whisk flour, baking powder, baking soda, salt, cinnamon, and nutmeg.",
            "Gradually mix dry ingredients into wet mixture.",
            "Fold in walnuts if using.",
            "Pour batter evenly into pans and bake for 35-40 minutes.",
            "Cool completely before frosting."
        ],
        "time": "75 mins",
        "servings": 8,
        "category": "Dessert",
        "calories": 420,
        "difficulty": "Intermediate",
        "prep_time": "25 mins",
        "cook_time": "40 mins",
        "tips": [
            "Grate carrots finely for a smoother texture.",
            "Add pineapple for extra moisture.",
            "Toast walnuts for a richer flavor."
        ],
        "nutritional_info": {
            "protein": "5g",
            "carbs": "55g",
            "fat": "18g",
            "fiber": "3g"
        }
    },

    "Lemon Drizzle Cake": {
        "ingredients": [
            "1 ½ cups all-purpose flour",
            "1 teaspoon baking powder",
            "½ teaspoon salt",
            "1 cup granulated sugar",
            "½ cup unsalted butter (softened)",
            "2 large eggs",
            "2 lemons (zest and juice)",
            "½ cup milk",
            "½ cup powdered sugar (for glaze)"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease a loaf pan.",
            "Cream butter and sugar until light and fluffy.",
            "Add eggs one at a time, then mix in lemon zest.",
            "In another bowl, whisk flour, baking powder, and salt.",
            "Alternate adding dry ingredients and milk to the batter.",
            "Pour batter into pan and bake for 40-45 minutes.",
            "Mix lemon juice and powdered sugar for drizzle.",
            "While cake is warm, poke holes and pour drizzle over.",
            "Cool completely before slicing."
        ],
        "time": "50 mins",
        "servings": 6,
        "category": "Dessert",
        "calories": 380,
        "difficulty": "Easy",
        "prep_time": "10 mins",
        "cook_time": "40 mins",
        "tips": [
            "Use fresh lemons for best flavor.",
            "Pour drizzle while cake is still warm for better absorption.",
            "Store in airtight container to keep moist."
        ],
        "nutritional_info": {
            "protein": "4g",
            "carbs": "58g",
            "fat": "12g",
            "fiber": "1g"
        }
    },

    "Black Forest Cake": {
        "ingredients": [
            "2 layers chocolate sponge cake",
            "2 cups whipped cream",
            "1 ½ cups pitted cherries (fresh or canned)",
            "½ cup cherry syrup or Kirsch (cherry brandy)",
            "½ cup chocolate shavings"
        ],
        "steps": [
            "Bake chocolate sponge and let it cool completely.",
            "Slice each sponge layer horizontally to make 4 layers.",
            "Brush each layer with cherry syrup or Kirsch.",
            "Spread whipped cream and cherries between layers.",
            "Frost the outside with whipped cream and top with chocolate shavings and cherries."
        ],
        "time": "120 mins",
        "servings": 10,
        "category": "Dessert",
        "calories": 520,
        "difficulty": "Advanced",
        "prep_time": "60 mins",
        "cook_time": "40 mins",
        "tips": [
            "Chill whipped cream before frosting.",
            "Soak cherries in syrup for extra flavor.",
            "Decorate with fresh cherries for a classic look."
        ],
        "nutritional_info": {
            "protein": "7g",
            "carbs": "68g",
            "fat": "24g",
            "fiber": "3g"
        }
    },

    "Cheesecake": {
        "ingredients": [
            "2 cups graham cracker crumbs",
            "½ cup melted butter",
            "3 (8 oz) packages cream cheese (softened)",
            "1 cup sugar",
            "3 large eggs",
            "1 teaspoon vanilla extract",
            "1 cup sour cream"
        ],
        "steps": [
            "Preheat oven to 325°F (163°C).",
            "Combine graham cracker crumbs with melted butter and press into a springform pan.",
            "Beat cream cheese and sugar until smooth.",
            "Add eggs one at a time, then vanilla.",
            "Pour filling over crust and bake for 55-60 minutes.",
            "Cool completely, then chill for at least 4 hours before serving."
        ],
        "time": "180 mins",
        "servings": 8,
        "category": "Dessert",
        "calories": 580,
        "difficulty": "Intermediate",
        "prep_time": "20 mins",
        "cook_time": "60 mins",
        "tips": [
            "Do not overmix to avoid cracks.",
            "Bake in a water bath for a smoother texture.",
            "Chill overnight for best results."
        ],
        "nutritional_info": {
            "protein": "9g",
            "carbs": "45g",
            "fat": "38g",
            "fiber": "0g"
        }
    },
    "Angel Food Cake": {
        "ingredients": [
            "1 cup cake flour",
            "1 ½ cups granulated sugar",
            "12 large egg whites (room temperature)",
            "1 ½ teaspoons cream of tartar",
            "1 teaspoon vanilla extract",
            "¼ teaspoon almond extract",
            "½ teaspoon salt"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C).",
            "Sift flour and ½ cup of sugar together and set aside.",
            "In a large bowl, beat egg whites until foamy.",
            "Add cream of tartar and salt, continue beating until soft peaks form.",
            "Gradually add remaining sugar and beat until stiff peaks form.",
            "Gently fold in flour mixture, vanilla, and almond extract.",
            "Pour batter into an ungreased tube pan.",
            "Bake for 35-40 minutes until golden and springs back when touched.",
            "Invert pan to cool completely before removing."
        ],
        "time": "60 mins",
        "servings": 12,
        "category": "Dessert",
        "calories": 150,
        "difficulty": "Intermediate",
        "prep_time": "20 mins",
        "cook_time": "40 mins",
        "tips": [
            "Do not grease the pan; this helps the cake rise properly.",
            "Use room-temperature egg whites for maximum volume.",
            "Cool upside down to prevent collapsing."
        ],
        "nutritional_info": {
            "protein": "4g",
            "carbs": "34g",
            "fat": "0g",
            "fiber": "0g"
        }
    },

    "Fruit Cake": {
        "ingredients": [
            "2 cups all-purpose flour",
            "1 ½ cups mixed dried fruits",
            "1 cup brown sugar",
            "1 cup unsigned butter (softened)",
            "4 large eggs",
            "1 teaspoon baking powder",
            "½ teaspoon ground cinnamon",
            "½ teaspoon ground nutmeg",
            "½ cup orange juice",
            "¼ cup brandy (optional)"
        ],
        "steps": [
            "Preheat oven to 325°F (163°C) and grease a loaf or round pan.",
            "Soak dried fruits in orange juice (and brandy if using) for at least 1 hour.",
            "Cream butter and sugar together until light and fluffy.",
            "Add eggs one at a time, mixing well.",
            "In a separate bowl, whisk flour, baking powder, and spices.",
            "Combine dry ingredients with creamed mixture.",
            "Fold in soaked fruits and any remaining liquid.",
            "Pour into pan and bake for 60-75 minutes until a toothpick comes out clean.",
            "Cool completely before slicing."
        ],
        "time": "2 hrs",
        "servings": 8,
        "category": "Dessert",
        "calories": 420,
        "difficulty": "Intermediate",
        "prep_time": "30 mins",
        "cook_time": "75 mins",
        "tips": [
            "For a richer flavor, soak fruits overnight.",
            "Wrap cooled cake in foil and let it rest for a day before serving.",
            "Brush with extra brandy for a moist texture."
        ],
        "nutritional_info": {
            "protein": "5g",
            "carbs": "65g",
            "fat": "15g",
            "fiber": "3g"
        }
    },

    "Pound Cake": {
        "ingredients": [
            "1 cup unsigned butter (softened)",
            "1 cup granulated sugar",
            "4 large eggs",
            "2 cups all-purpose flour",
            "1 teaspoon vanilla extract",
            "½ teaspoon baking powder",
            "¼ teaspoon salt"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease a loaf pan.",
            "Cream butter and sugar until pale and fluffy.",
            "Add eggs one at a time, mixing well after each addition.",
            "Mix in vanilla extract.",
            "Combine flour, baking powder, and salt, then add to the batter gradually.",
            "Pour into the prepared pan and smooth the top.",
            "Bake for 55-65 minutes until a toothpick comes out clean.",
            "Cool in the pan for 10 minutes, then transfer to a wire rack."
        ],
        "time": "80 mins",
        "servings": 8,
        "category": "Dessert",
        "calories": 410,
        "difficulty": "Easy",
        "prep_time": "15 mins",
        "cook_time": "60 mins",
        "tips": [
            "Do not overmix the batter after adding flour.",
            "Use room-temperature butter and eggs for the best texture.",
            "Serve with whipped cream or fresh berries for extra flavor."
        ],
        "nutritional_info": {
            "protein": "6g",
            "carbs": "48g",
            "fat": "20g",
            "fiber": "1g"
        }
    },

    "Banana Bread": {
        "ingredients": [
            "2 cups all-purpose flour",
            "1 teaspoon baking soda",
            "½ teaspoon salt",
            "½ cup unsigned butter (softened)",
            "¾ cup granulated sugar",
            "2 large eggs",
            "3 ripe bananas (mashed)",
            "1 teaspoon vanilla extract",
            "½ cup chopped walnuts (optional)"
        ],
        "steps": [
            "Preheat oven to 350°F (175°C) and grease a loaf pan.",
            "In a small bowl, whisk flour, baking soda, and salt.",
            "In a large bowl, cream butter and sugar together.",
            "Add eggs, mashed bananas, and vanilla extract.",
            "Stir in dry ingredients just until combined.",
            "Fold in walnuts if using.",
            "Pour into the loaf pan and bake for 60-70 minutes.",
            "Cool before slicing."
        ],
        "time": "75 mins",
        "servings": 8,
        "category": "Dessert",
        "calories": 330,
        "difficulty": "Easy",
        "prep_time": "15 mins",
        "cook_time": "60 mins",
        "tips": [
            "Use very ripe bananas for the sweetest flavor.",
            "Do not overmix after adding flour to keep bread moist.",
            "Add chocolate chips for a fun twist."
        ],
        "nutritional_info": {
            "protein": "4g",
            "carbs": "54g",
            "fat": "12g",
            "fiber": "2g"
        }
    },

    "Chocolate Lava Cake": {
        "ingredients": [
            "½ cup unsigned butter",
            "6 oz bittersweet chocolate (chopped)",
            "1 cup powdered sugar",
            "2 large eggs",
            "2 large egg yolks",
            "1 teaspoon vanilla extract",
            "½ cup all-purpose flour"
        ],
        "steps": [
            "Preheat oven to 425°F (218°C) and grease ramekins.",
            "Melt butter and chocolate together over a double boiler or in the microwave.",
            "Stir in powdered sugar until smooth.",
            "Whisk in eggs, egg yolks, and vanilla.",
            "Fold in flour just until combined.",
            "Divide batter into ramekins and bake for 12-14 minutes until edges are firm but center is soft.",
            "Cool for 1 minute, then invert onto plates and serve immediately."
        ],
        "time": "25 mins",
        "servings": 4,
        "category": "Dessert",
        "calories": 400,
        "difficulty": "Intermediate",
        "prep_time": "10 mins",
        "cook_time": "12 mins",
        "tips": [
            "Do not overbake; the center should be gooey.",
            "Serve with vanilla ice cream for the best experience.",
            "Grease ramekins well to prevent sticking."
        ],
        "nutritional_info": {
            "protein": "6g",
            "carbs": "45g",
            "fat": "22g",
            "fiber": "3g"
        }
    },
    
    # Drinks
    "Mango Smoothie": {
    "ingredients": [
        "2 large ripe mangoes, peeled and cubed (or 2 cups frozen mango chunks)",
        "1 cup plain Greek yogurt",
        "1/2 cup coconut milk (or regular milk)",
        "2 tablespoons honey (adjust to taste)",
        "1 tablespoon lime juice",
        "1/2 teaspoon vanilla extract",
        "1/4 teaspoon ground cardamom (optional)",
        "1 cup ice cubes",
        "Fresh mint leaves for garnish",
        "Toasted coconut flakes for garnish"
    ],
    "steps": [
        "Prepare ingredients: If using fresh mangoes, peel and cube them. Chill all ingredients beforehand for best texture.",
        "Blend base: Add mango chunks, yogurt, and coconut milk to a high-speed blender.",
        "Add flavors: Add honey, lime juice, vanilla extract, and cardamom if using.",
        "Blend smooth: Blend on high speed for 60-90 seconds until completely smooth and creamy.",
        "Adjust consistency: Add ice cubes and blend again until desired consistency is reached. Add more liquid if too thick.",
        "Taste and adjust: Sample and adjust sweetness with more honey or tartness with lime juice as needed.",
        "Serve immediately: Pour into chilled glasses and garnish with mint leaves and toasted coconut.",
        "Storage tip: Can be stored in refrigerator for up to 24 hours. Stir well before serving."
    ],
    "time": "10 mins",
    "servings": 2,
    "category": "Drink",
    "calories": 220,
    "difficulty": "Easy",
    "prep_time": "10 mins",
    "cook_time": "0 mins",
    "tips": [
        "Use ripe mangoes for natural sweetness and best flavor",
        "Frozen mango creates a thicker, colder smoothie",
        "Greek yogurt adds protein and creaminess",
        "Cardamom adds an exotic, aromatic touch",
        "Chill your glass beforehand for the ultimate experience"
    ],
    "nutritional_info": {
        "protein": "12g",
        "carbs": "42g",
        "fat": "4g",
        "fiber": "4g",
        "vitamin_c": "80% DV",
        "vitamin_a": "35% DV"
    }
},

"Green Smoothie": {
    "ingredients": [
        "2 cups fresh spinach (packed)",
        "1 ripe banana",
        "1 medium apple (cored and chopped)",
        "1/2 cup Greek yogurt",
        "1 tablespoon honey (optional)",
        "1 cup cold water or almond milk",
        "1 cup ice cubes",
        "Chia seeds or flaxseeds for garnish"
    ],
    "steps": [
        "Prepare greens: Wash spinach thoroughly and pat dry.",
        "Blend base: Add spinach and water (or almond milk) to a blender and blend until smooth.",
        "Add fruits and yogurt: Add banana, apple, Greek yogurt, and honey if desired.",
        "Blend smooth: Blend for 60 seconds until creamy and no leafy chunks remain.",
        "Add ice: Add ice cubes and blend again until cold and thick.",
        "Serve immediately: Pour into glasses and sprinkle chia or flaxseeds for extra nutrition."
    ],
    "time": "7 mins",
    "servings": 2,
    "category": "Drink",
    "calories": 150,
    "difficulty": "Easy",
    "prep_time": "7 mins",
    "cook_time": "0 mins",
    "tips": [
        "Freeze banana chunks for a thicker texture",
        "Add protein powder for a post-workout smoothie",
        "Use kale instead of spinach for variation",
        "Add a squeeze of lemon juice for extra freshness"
    ],
    "nutritional_info": {
        "protein": "6g",
        "carbs": "28g",
        "fat": "2g",
        "fiber": "6g",
        "vitamin_c": "70% DV",
        "vitamin_k": "150% DV"
    }
},

"Mojito": {
    "ingredients": [
        "2 oz white rum",
        "8-10 fresh mint leaves",
        "1 oz fresh lime juice",
        "2 teaspoons sugar",
        "Club soda to top",
        "Ice cubes",
        "Lime wedges and mint sprig for garnish"
    ],
    "steps": [
        "Muddle mint: In a sturdy glass, muddle mint leaves with sugar and lime juice to release flavors.",
        "Add rum: Pour in white rum and mix well.",
        "Add ice: Fill glass with ice cubes.",
        "Top with soda: Add club soda to fill the glass and stir gently.",
        "Garnish: Add a mint sprig and lime wedge before serving."
    ],
    "time": "5 mins",
    "servings": 1,
    "category": "Drink",
    "calories": 200,
    "difficulty": "Easy",
    "prep_time": "5 mins",
    "cook_time": "0 mins",
    "tips": [
        "Use crushed ice for better chilling",
        "Do not over-muddle mint to avoid bitterness",
        "Adjust sugar to taste"
    ],
    "nutritional_info": {
        "protein": "0g",
        "carbs": "6g",
        "fat": "0g",
        "fiber": "1g"
    }
},

"Virgin Piña Colada": {
    "ingredients": [
        "1 cup pineapple juice",
        "1/2 cup coconut cream",
        "1/2 cup crushed ice",
        "Pineapple chunks for garnish",
        "Maraschino cherry for garnish"
    ],
    "steps": [
        "Blend base: Combine pineapple juice, coconut cream, and crushed ice in a blender.",
        "Blend until smooth and creamy.",
        "Serve immediately in a tall chilled glass.",
        "Garnish with pineapple chunks and a cherry."
    ],
    "time": "3 mins",
    "servings": 1,
    "category": "Drink",
    "calories": 280,
    "difficulty": "Easy",
    "prep_time": "3 mins",
    "cook_time": "0 mins",
    "tips": [
        "Use fresh pineapple juice for best taste",
        "Add more coconut cream for a creamier texture"
    ],
    "nutritional_info": {
        "protein": "1g",
        "carbs": "34g",
        "fat": "9g",
        "fiber": "2g"
    }
},

"Chocolate Milkshake": {
    "ingredients": [
        "2 scoops chocolate ice cream",
        "1 cup whole milk",
        "3 tablespoons chocolate syrup",
        "Whipped cream for topping",
        "Chocolate shavings for garnish"
    ],
    "steps": [
        "Combine ingredients: Add ice cream, milk, and chocolate syrup to a blender.",
        "Blend for 30-60 seconds until creamy and smooth.",
        "Pour into a tall glass and top with whipped cream and chocolate shavings.",
        "Serve immediately with a straw."
    ],
    "time": "3 mins",
    "servings": 1,
    "category": "Drink",
    "calories": 420,
    "difficulty": "Easy",
    "prep_time": "3 mins",
    "cook_time": "0 mins",
    "tips": [
        "Use full-fat milk for creamier texture",
        "Add a shot of espresso for a mocha milkshake"
    ],
    "nutritional_info": {
        "protein": "8g",
        "carbs": "55g",
        "fat": "18g",
        "fiber": "3g"
    }
},

"Fresh Orange Juice": {
    "ingredients": [
        "6 medium oranges",
        "Ice cubes",
        "Sugar (optional)",
        "Mint leaves for garnish"
    ],
    "steps": [
        "Juice oranges using a citrus juicer.",
        "Strain juice to remove pulp (optional).",
        "Serve over ice and garnish with mint leaves."
    ],
    "time": "5 mins",
    "servings": 2,
    "category": "Drink",
    "calories": 120,
    "difficulty": "Easy",
    "prep_time": "5 mins",
    "cook_time": "0 mins",
    "tips": [
        "Use fresh sweet oranges for the best taste",
        "Chill oranges before juicing for a colder drink"
    ],
    "nutritional_info": {
        "protein": "2g",
        "carbs": "28g",
        "fat": "0g",
        "fiber": "4g",
        "vitamin_c": "150% DV"
    }
},

"Iced Tea": {
    "ingredients": [
        "4 black tea bags",
        "4 cups boiling water",
        "1/4 cup sugar (or to taste)",
        "Ice cubes",
        "Lemon slices for garnish"
    ],
    "steps": [
        "Brew tea: Steep tea bags in boiling water for 5 minutes.",
        "Sweeten: Remove bags and stir in sugar until dissolved.",
        "Cool: Let tea come to room temperature, then refrigerate until cold.",
        "Serve: Pour over ice and garnish with lemon slices."
    ],
    "time": "15 mins",
    "servings": 4,
    "category": "Drink",
    "calories": 80,
    "difficulty": "Easy",
    "prep_time": "10 mins",
    "cook_time": "5 mins",
    "tips": [
        "For stronger tea, steep longer or use more tea bags",
        "Add fresh mint for extra flavor"
    ],
    "nutritional_info": {
        "protein": "0g",
        "carbs": "21g",
        "fat": "0g"
    }
},

"Watermelon Juice": {
    "ingredients": [
        "4 cups watermelon cubes (seedless)",
        "1 tablespoon lime juice",
        "Fresh mint leaves",
        "Ice cubes"
    ],
    "steps": [
        "Blend watermelon and lime juice in a blender until smooth.",
        "Strain juice to remove pulp if desired.",
        "Serve over ice and garnish with mint leaves."
    ],
    "time": "5 mins",
    "servings": 3,
    "category": "Drink",
    "calories": 90,
    "difficulty": "Easy",
    "prep_time": "5 mins",
    "cook_time": "0 mins",
    "tips": [
        "Chill watermelon before blending for a refreshing drink",
        "Add a pinch of salt to enhance flavor"
    ],
    "nutritional_info": {
        "protein": "1g",
        "carbs": "23g",
        "fat": "0g",
        "fiber": "1g"
    }
}
}

# Authentication functions
def show_auth_page():
    st.title("🍲 Welcome to Recipe Quest")
    
    # Switch order: Sign Up first, then Login
    tab1, tab2 = st.tabs(["Sign Up", "Login"])
    
    with tab1:
        st.subheader("Sign Up")
        new_username = st.text_input("Choose Username", key="signup_user")
        new_password = st.text_input("Choose Password", type="password", key="signup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Sign Up"):
            if new_username and new_password:
                if new_password == confirm_password:
                    if new_username not in st.session_state.users:
                        st.session_state.users[new_username] = {
                            "password": new_password,
                            "created_at": datetime.now().isoformat()
                        }
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Passwords don't match")
            else:
                st.error("Please fill all fields")
    
    with tab2:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if username in st.session_state.users:
                if st.session_state.users[username]["password"] == password:
                    st.session_state.user_authenticated = True
                    st.session_state.current_user = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid password")
            else:
                st.error("User not found")

# Main app functions
def show_home():
    st.markdown("""
    <div class="main-header">
        <h1>🍲 Recipe Quest</h1>
        <p>Your Ultimate Cooking Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="recipe-card">
            <h3>🥘 90+ Recipes</h3>
            <p>Nigerian & International dishes, cakes, and drinks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="recipe-card">
            <h3>📅 Meal Planning</h3>
            <p>Plan your weekly meals with ease</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="recipe-card">
            <h3>🎮 Cooking Game</h3>
            <p>Fun ingredient matching game</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Featured recipes
    st.subheader("🌟 Featured Recipes")
    featured = random.sample(list(RECIPES.keys()), 3)
    
    cols = st.columns(3)
    for i, recipe in enumerate(featured):
        with cols[i]:
            st.markdown(f"""
            <div class="recipe-card">
                <h4>{recipe}</h4>
                <p>⏱️ {RECIPES[recipe]['time']}</p>
                <p>🍽️ Serves {RECIPES[recipe]['servings']}</p>
                <p>🔥 {RECIPES[recipe]['calories']} cal</p>
            </div>
            """, unsafe_allow_html=True)
    
   # Daily tip
tips = [
    "🧄 Crush garlic with the flat side of a knife for easier peeling",
    "🧅 To prevent tears when cutting onions, chill them first",
    "🍅 Store tomatoes at room temperature for better flavor",
    "🥓 Cook bacon in a cold pan for even cooking",
    "🍋 Roll citrus fruits before juicing for more juice",
    "🥔 Soak cut potatoes in water to remove excess starch before frying",
    "🥩 Let meat rest after cooking for juicier results",
    "🥗 Add salt to boiling water for brighter vegetables",
    "🥖 Revive stale bread by sprinkling with water and warming in the oven",
    "🥒 Use a spoon to easily peel ginger without wasting flesh",
    "🍝 Save pasta water to thicken sauces and add flavor",
    "🧈 Soften butter quickly by grating it instead of microwaving",
    "🌽 Add a pinch of sugar when boiling corn for natural sweetness",
    "🥚 Test egg freshness by placing it in water; fresh eggs sink",
    "🍫 Add a pinch of salt to chocolate desserts to enhance flavor",
    "🫑 Cut bell peppers from the bottom to avoid seeds spilling everywhere",
    "🍄 Clean mushrooms with a damp cloth instead of rinsing to prevent sogginess",
    "🥬 Wrap herbs in a damp paper towel and refrigerate to keep them fresh",
    "🍊 Zest citrus before juicing for extra flavor in dishes",
    "🥛 Warm milk slightly before adding to yeast for better activation"
]
    
st.info(f"💡 **Cooking Tip of the Day:** {random.choice(tips)}")

def show_recipes():
    st.title("🥘 Recipe Collection")
    
    # Search functionality
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search recipes...", placeholder="Enter dish name or ingredient")
    with col2:
        category_filter = st.selectbox("Filter by category", 
                                     ["All", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Drink"])
    with col3:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
    
    # Filter recipes
    filtered_recipes = RECIPES.copy()
    
    if search_query:
        filtered_recipes = {
            name: recipe for name, recipe in RECIPES.items()
            if search_query.lower() in name.lower() or
            any(search_query.lower() in ingredient.lower() for ingredient in recipe['ingredients'])
        }
        
        if not filtered_recipes:
            suggestions = [name for name in RECIPES.keys() 
                         if any(word in name.lower() for word in search_query.lower().split())][:3]
            if suggestions:
                st.warning(f"No exact matches found. Did you mean: {', '.join(suggestions)}?")
    
    if category_filter != "All":
        filtered_recipes = {
            name: recipe for name, recipe in filtered_recipes.items()
            if recipe['category'] == category_filter
        }
    
    if difficulty_filter != "All":
        filtered_recipes = {
            name: recipe for name, recipe in filtered_recipes.items()
            if recipe.get('difficulty', 'Medium') == difficulty_filter
        }
    
    # Display recipes
    if filtered_recipes:
        st.write(f"Found {len(filtered_recipes)} recipes")
        
        for recipe_name, recipe_data in filtered_recipes.items():
            with st.expander(f"🍽️ {recipe_name}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Ingredients:**")
                    for ingredient in recipe_data['ingredients']:
                        st.write(f"• {ingredient}")
                    
                    st.write(f"**⏱️ Time:** {recipe_data['time']}")
                    st.write(f"**🍽️ Servings:** {recipe_data['servings']}")
                    st.write(f"**📂 Category:** {recipe_data['category']}")
                    st.write(f"**🔥 Calories:** {recipe_data['calories']}")
                
                with col2:
                    st.write("**Instructions:**")
                    for i, step in enumerate(recipe_data['steps'], 1):
                        st.write(f"{i}. {step}")
                    
                    # Action buttons
                    button_col1, button_col2, button_col3 = st.columns(3)
                    with button_col1:
                        if st.button(f"❤️ Favorite", key=f"fav_{recipe_name}"):
                            if recipe_name not in st.session_state.favorites:
                                st.session_state.favorites.append(recipe_name)
                                st.success("Added to favorites!")
                    
                    with button_col2:
                        if st.button(f"📝 Add Note", key=f"note_{recipe_name}"):
                            st.session_state.current_recipe_note = recipe_name
                    
                    with button_col3:
                        if 'video' in recipe_data:
                            st.markdown(f"[🎥 Watch Video]({recipe_data['video']})")
    else:
        st.warning("No recipes found matching your search criteria.")
        
        # External search option
        if search_query:
            if st.button(f"🌐 Search '{search_query}' on the web"):
                st.info("Opening external search in new tab...")

def show_meal_planner():
    st.title("📅 Meal Planner")
    
    # Weekly planner
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meals = ['Breakfast', 'Lunch', 'Dinner']
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🎲 Chef's Suggestion"):
            # Generate random meal plan
            for day in days:
                if day not in st.session_state.meal_plan:
                    st.session_state.meal_plan[day] = {}
                for meal in meals:
                    suitable_recipes = [name for name, data in RECIPES.items() 
                                      if data['category'] == meal or 
                                      (meal == 'Breakfast' and data['category'] in ['Breakfast', 'Snack']) or
                                      (meal == 'Lunch' and data['category'] in ['Lunch', 'Snack']) or
                                      (meal == 'Dinner' and data['category'] in ['Dinner', 'Lunch'])]
                    if suitable_recipes:
                        st.session_state.meal_plan[day][meal] = random.choice(suitable_recipes)
            st.success("Random meal plan generated!")
    
    with col1:
        st.subheader("Weekly Meal Plan")
    
    # Create meal plan grid
    for day in days:
        st.subheader(f"📅 {day}")
        cols = st.columns(3)
        
        if day not in st.session_state.meal_plan:
            st.session_state.meal_plan[day] = {}
        
        for i, meal in enumerate(meals):
            with cols[i]:
                st.write(f"**{meal}**")
                current_meal = st.session_state.meal_plan[day].get(meal, "")
                
                selected_recipe = st.selectbox(
                    f"Select {meal.lower()}",
                    [""] + list(RECIPES.keys()),
                    index=list([""] + list(RECIPES.keys())).index(current_meal) if current_meal in RECIPES else 0,
                    key=f"{day}_{meal}"
                )
                
                if selected_recipe:
                    st.session_state.meal_plan[day][meal] = selected_recipe
                    recipe_data = RECIPES[selected_recipe]
                    st.write(f"⏱️ {recipe_data['time']}")
                    st.write(f"🔥 {recipe_data['calories']} cal")
    
    st.markdown("---")
    
    # Download meal plan
    if st.button("📄 Download Meal Plan as PDF"):
        # Create a simple text version for download
        meal_plan_text = "WEEKLY MEAL PLAN\n" + "="*50 + "\n\n"
        total_calories = 0
        
        for day in days:
            meal_plan_text += f"{day.upper()}\n" + "-"*30 + "\n"
            day_calories = 0
            
            for meal in meals:
                recipe = st.session_state.meal_plan[day].get(meal, "Not planned")
                meal_plan_text += f"{meal}: {recipe}\n"
                
                if recipe in RECIPES:
                    calories = RECIPES[recipe]['calories']
                    day_calories += calories
                    meal_plan_text += f"  Calories: {calories}\n"
            
            meal_plan_text += f"Daily Total: {day_calories} calories\n\n"
            total_calories += day_calories
        
        meal_plan_text += f"WEEKLY TOTAL CALORIES: {total_calories}\n"
        meal_plan_text += f"AVERAGE DAILY CALORIES: {total_calories//7}\n"
        
        st.download_button(
            label="📥 Download Meal Plan",
            data=meal_plan_text,
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
        st.success("Meal plan ready for download!")

def show_cooking_timer():
    st.title("⏰ Cooking Timer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Set Timer")
        hours = st.number_input("Hours", min_value=0, max_value=23, value=0)
        minutes = st.number_input("Minutes", min_value=0, max_value=59, value=5)
        seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        if st.button("🎯 Start Timer"):
            st.session_state.timer_end = time.time() + total_seconds
            st.session_state.timer_running = True
    
    with col2:
        st.subheader("Quick Timers")
        quick_times = {
            "🥚 Soft Boiled Egg": 180,
            "🍝 Pasta": 600,
            "🍞 Toast": 120,
            "☕ Coffee Brew": 240,
            "🍖 Steak (Medium)": 300,
            "🍚 Rice": 1200
        }
        
        for timer_name, timer_seconds in quick_times.items():
            if st.button(timer_name):
                st.session_state.timer_end = time.time() + timer_seconds
                st.session_state.timer_running = True
    
    # Timer display
    if hasattr(st.session_state, 'timer_running') and st.session_state.timer_running:
        if hasattr(st.session_state, 'timer_end'):
            remaining = st.session_state.timer_end - time.time()
            
            if remaining > 0:
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                st.markdown(f"""
                <div class="timer-display">
                    {hours:02d}:{minutes:02d}:{seconds:02d}
                </div>
                """, unsafe_allow_html=True)
                
                # Auto refresh
                time.sleep(1)
                st.rerun()
            else:
                st.markdown("""
                <div class="timer-display" style="color: #ff4444;">
                    TIME'S UP! ⏰
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                st.session_state.timer_running = False

def show_cooking_game():
    st.title("🎮 Cooking Challenge Game")
    
    # Initialize ALL game state variables
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
    if 'current_dish' not in st.session_state:
        st.session_state.current_dish = ""
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = 0
    if 'selected_ingredients' not in st.session_state:
        st.session_state.selected_ingredients = []
    if 'revealed' not in st.session_state:
        st.session_state.revealed = False
    if 'hint_used' not in st.session_state:
        st.session_state.hint_used = False
    if 'game_ingredients' not in st.session_state:
        st.session_state.game_ingredients = []
    if 'chef_mood' not in st.session_state:
        st.session_state.chef_mood = "neutral"

    # ===== CHEF ANIMATION USING YOUR DOWNLOADED FILES =====
    try:
        # Use your downloaded files
        mood_file = f"chef_{st.session_state.chef_mood}.json"
        with open(mood_file, "r") as file:
            chef_data = json.load(file)
        st_lottie(chef_data, height=150, key=f"chef_{st.session_state.chef_mood}")
    except:
        # If files don't work, show emoji instead
        mood_emoji = "😊" if st.session_state.chef_mood == "happy" else "😢" if st.session_state.chef_mood == "sad" else "👨‍🍳"
        st.markdown(f"<div style='text-align: center; font-size: 100px;'>{mood_emoji}</div>", unsafe_allow_html=True)

    # Display game header
    st.markdown("""
    <div class="game-section">
        <h2>Ingredient Matching Challenge!</h2>
        <p>Select the correct ingredients for the given dish within 60 seconds!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.game_active:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start New Game"):
                # Reset and start game
                st.session_state.current_dish = random.choice(list(RECIPES.keys()))
                st.session_state.game_active = True
                st.session_state.game_start_time = time.time()
                st.session_state.selected_ingredients = []
                st.session_state.revealed = False
                st.session_state.hint_used = False
                st.session_state.chef_mood = "neutral"
                
                # Generate ingredients ONCE and store them
                correct_ingredients = RECIPES[st.session_state.current_dish]['ingredients']
                all_possible_ingredients = set()
                for recipe in RECIPES.values():
                    all_possible_ingredients.update(recipe['ingredients'])
                extra_ingredients = random.sample(
                    list(all_possible_ingredients - set(correct_ingredients)), 
                    min(8, len(all_possible_ingredients - set(correct_ingredients)))
                )
                game_ingredients = list(correct_ingredients) + extra_ingredients
                random.shuffle(game_ingredients)
                st.session_state.game_ingredients = game_ingredients
                
                st.rerun()
        
        with col2:
            st.metric("🏆 High Score", st.session_state.game_score)
    else:
        # Active game
        dish = st.session_state.current_dish
        correct_ingredients = RECIPES[dish]['ingredients']
        num_correct_needed = len(correct_ingredients)
        
        # Timer
        elapsed = time.time() - st.session_state.game_start_time
        remaining = max(0, 60 - elapsed)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"🍽️ Dish: {dish}")
            st.info(f"Select exactly {num_correct_needed} ingredients!")
        with col2:
            st.metric("⏱️ Time Left", f"{remaining:.0f}s")
            st.progress(remaining / 60)
        
        if remaining <= 0:
            st.error("⏰ Time's up!")
            st.session_state.game_active = False
            st.session_state.revealed = True
            st.session_state.chef_mood = "sad"
            st.rerun()
        
        # Use the STORED ingredients list (won't reshuffle!)
        st.subheader("Available Ingredients:")
        cols = st.columns(4)
        
        for i, ingredient in enumerate(st.session_state.game_ingredients):
            with cols[i % 4]:
                is_selected = ingredient in st.session_state.selected_ingredients
                if st.button(
                    f"{'✅ ' if is_selected else ''}{ingredient}", 
                    key=f"ingredient_{i}_{ingredient}",
                    type="primary" if is_selected else "secondary"
                ):
                    if ingredient in st.session_state.selected_ingredients:
                        st.session_state.selected_ingredients.remove(ingredient)
                    else:
                        st.session_state.selected_ingredients.append(ingredient)
                    st.rerun()
        
        # Show selected ingredients
        st.subheader("Your Selections:")
        if st.session_state.selected_ingredients:
            st.write(", ".join([f"✅ {ing}" for ing in st.session_state.selected_ingredients]))
        else:
            st.info("None selected yet.")
        
        # Game controls
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Submit Answer"):
                correct_selected = set(st.session_state.selected_ingredients) & set(correct_ingredients)
                extra_selected = set(st.session_state.selected_ingredients) - set(correct_ingredients)
                missed = set(correct_ingredients) - set(st.session_state.selected_ingredients)
                
                base_score = (len(correct_selected) / num_correct_needed) * 100
                time_bonus = (remaining / 60) * 50
                penalty = len(extra_selected) * 10 + (5 if st.session_state.hint_used else 0)
                final_score = max(0, int(base_score + time_bonus - penalty))
                
                st.session_state.game_score = max(st.session_state.game_score, final_score)
                st.session_state.game_active = False
                st.session_state.revealed = True
                
                # Set chef mood based on performance
                if len(correct_selected) == num_correct_needed and not extra_selected:
                    st.session_state.chef_mood = "happy"
                    st.success(f"🎉 Perfect! Score: {final_score}")
                elif final_score >= 70:
                    st.session_state.chef_mood = "happy"
                    st.success(f"👍 Great job! Score: {final_score}")
                else:
                    st.session_state.chef_mood = "sad"
                    st.info(f"Score: {final_score}. You got {len(correct_selected)}/{num_correct_needed} correct!")
                
                st.rerun()
        
        with col2:
            if st.button("💡 Hint (costs 5 points)"):
                if not st.session_state.hint_used and correct_ingredients:
                    hint_ing = random.choice(correct_ingredients)
                    st.info(f"Hint: '{hint_ing}' is a correct ingredient!")
                    st.session_state.hint_used = True
                    st.rerun()
        
        
        with col3:
            if st.button("❌ Quit Game"):
                st.session_state.game_active = False
                st.session_state.revealed = True
                st.session_state.chef_mood = "sad"
                st.warning("Game quit. Score: 0")
                st.rerun()
        
        # Show feedback if revealed
        if st.session_state.revealed:
            st.subheader("Game Feedback:")
            st.success(f"Correct: {', '.join(correct_ingredients)}")
            if st.session_state.selected_ingredients:
                correct_selected = set(st.session_state.selected_ingredients) & set(correct_ingredients)
                extra = set(st.session_state.selected_ingredients) - set(correct_ingredients)
                missed = set(correct_ingredients) - set(st.session_state.selected_ingredients)
                if correct_selected:
                    st.success(f"You got right: {', '.join(correct_selected)}")
                if extra:
                    st.error(f"Extra/wrong: {', '.join(extra)}")
                if missed:
                    st.warning(f"Missed: {', '.join(missed)}")
            
            # Play again button
            if st.button("🔄 Play Again"):
                st.session_state.game_active = False
                st.session_state.revealed = False
                st.session_state.chef_mood = "neutral"
                st.rerun()
        
        # Auto-refresh for timer
        if st.session_state.game_active and not st.session_state.revealed:
            time.sleep(1)
            st.rerun()
def show_drinks():
    st.title("🍹 Drinks Collection")
    
    # Filter drinks from recipes
    drinks = {name: data for name, data in RECIPES.items() if data['category'] == 'Drink'}
    
    # Additional drink categories
    categories = {
        "🥤 All Drinks": drinks,
        "🥛 Smoothies": {k: v for k, v in drinks.items() if 'smoothie' in k.lower()},
        "🍹 Cocktails": {k: v for k, v in drinks.items() if any(word in k.lower() for word in ['mojito', 'cocktail', 'rum'])},
        "🧊 Mocktails": {k: v for k, v in drinks.items() if 'virgin' in k.lower() or 'mocktail' in k.lower()},
        "🥤 Juices": {k: v for k, v in drinks.items() if 'juice' in k.lower()},
        "🥛 Milkshakes": {k: v for k, v in drinks.items() if 'milkshake' in k.lower() or 'shake' in k.lower()},
        "🌿 Nigerian Drinks": {k: v for k, v in drinks.items() if k in ['Zobo', 'Kunu']}
    }
    
    selected_category = st.selectbox("Choose category", list(categories.keys()))
    display_drinks = categories[selected_category]
    
    if display_drinks:
        cols = st.columns(2)
        for i, (drink_name, drink_data) in enumerate(display_drinks.items()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="recipe-card">
                    <h3>🍹 {drink_name}</h3>
                    <p><strong>Time:</strong> {drink_data['time']}</p>
                    <p><strong>Servings:</strong> {drink_data['servings']}</p>
                    <p><strong>Calories:</strong> {drink_data['calories']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Recipe"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Ingredients:**")
                        for ingredient in drink_data['ingredients']:
                            st.write(f"• {ingredient}")
                    
                    with col2:
                        st.write("**Instructions:**")
                        for j, step in enumerate(drink_data['steps'], 1):
                            st.write(f"{j}. {step}")
    else:
        st.info("No drinks found in this category.")

def show_notes():
    st.title("📝 Personal Notes & Favorites")
    
    tab1, tab2 = st.tabs(["💖 Favorites", "📝 Notes"])
    
    with tab1:
        st.subheader("Your Favorite Recipes")
        if st.session_state.favorites:
            for favorite in st.session_state.favorites:
                if favorite in RECIPES:
                    recipe_data = RECIPES[favorite]
                    with st.expander(f"❤️ {favorite}"):
                        st.write(f"**Time:** {recipe_data['time']} | **Servings:** {recipe_data['servings']} | **Calories:** {recipe_data['calories']}")
                        
                        if st.button(f"Remove from favorites", key=f"remove_{favorite}"):
                            st.session_state.favorites.remove(favorite)
                            st.success("Removed from favorites!")
                            st.rerun()
        else:
            st.info("No favorite recipes yet. Add some from the Recipes page!")
    
    with tab2:
        st.subheader("Your Personal Notes")
        
        # Add new note
        with st.expander("➕ Add New Note"):
            note_title = st.text_input("Note Title")
            note_content = st.text_area("Note Content", height=100)
            note_recipe = st.selectbox("Related Recipe (optional)", ["None"] + list(RECIPES.keys()))
            
            if st.button("💾 Save Note"):
                if note_title and note_content:
                    new_note = {
                        "title": note_title,
                        "content": note_content,
                        "recipe": note_recipe if note_recipe != "None" else None,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.notes.append(new_note)
                    st.success("Note saved!")
                else:
                    st.error("Please fill in title and content")
        
        # Display notes
        if st.session_state.notes:
            for i, note in enumerate(st.session_state.notes):
                with st.expander(f"📝 {note['title']} - {note['created']}"):
                    st.write(note['content'])
                    if note['recipe']:
                        st.write(f"**Related Recipe:** {note['recipe']}")
                    
                    if st.button(f"🗑️ Delete", key=f"delete_note_{i}"):
                        st.session_state.notes.pop(i)
                        st.success("Note deleted!")
                        st.rerun()
        else:
            st.info("No notes yet. Create your first note above!")

def show_settings():
    st.title("⚙️ Settings & Personalization")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Themes", "👤 Profile", "🔥 Calorie Tracker"])
    
    with tab1:
    
        st.subheader("Choose Your Theme")
        
        theme_options = {
            "Light": "Default light theme",
            "Dark": "Dark mode for night cooking",
            "Food": "Warm food-themed colors"
        }
        
        selected_theme = st.radio("Select Theme", list(theme_options.keys()), 
                                 index=list(theme_options.keys()).index(st.session_state.theme))
        
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.success(f"Theme changed to {selected_theme}!")
        
        st.write(f"**Current theme:** {theme_options[st.session_state.theme]}")
        
        # Theme preview with actual theme classes
        
        st.markdown(f"""
<div data-theme="{st.session_state.theme.lower()}" class="theme-container">
    <div class="recipe-card">
        <h4>{"🌙 Dark Theme" if st.session_state.theme == "Dark" else "🍊 Food Theme" if st.session_state.theme == "Food" else "☀️ Light Theme"} Preview</h4>
        <p>{"Perfect for late-night cooking sessions!" if st.session_state.theme == "Dark" else "Warm and appetizing colors!" if st.session_state.theme == "Food" else "Clean and bright interface!"}</p>
        <p>⏱️ 30 mins | 🍽️ Serves 4 | 🔥 350 cal</p>
    </div>
</div>
""", unsafe_allow_html=True)


    with tab2:
        st.subheader("Profile Settings")
        if st.session_state.current_user:
            st.write(f"**Username:** {st.session_state.current_user}")
            st.write(f"**Total Favorite Recipes:** {len(st.session_state.favorites)}")
            st.write(f"**Total Notes:** {len(st.session_state.notes)}")
            st.write(f"**Game High Score:** {st.session_state.game_score}")
            
            if st.button("🚪 Logout"):
                st.session_state.user_authenticated = False
                st.session_state.current_user = None
                st.success("Logged out successfully!")
                st.rerun()
        else:
            st.info("Please log in to view profile settings.")
    
    with tab3:
        st.subheader("Daily Calorie Tracker")
        
        col1, col2 = st.columns(2)
        with col1:
            daily_goal = st.number_input("Daily Calorie Goal", min_value=1000, max_value=5000, value=2000)
            st.session_state.daily_goal = daily_goal
        
        with col2:
            st.metric("Today's Calories", st.session_state.daily_calories, f"{st.session_state.daily_calories - daily_goal} vs goal")
        
        # Add calories
        st.subheader("Add Meal Calories")
        selected_recipe = st.selectbox("Select a recipe you ate", [""] + list(RECIPES.keys()))
        
        if selected_recipe and st.button("➕ Add to Daily Total"):
            calories_to_add = RECIPES[selected_recipe]['calories']
            st.session_state.daily_calories += calories_to_add
            st.success(f"Added {calories_to_add} calories from {selected_recipe}!")
        
        # Manual calorie input
        manual_calories = st.number_input("Or add calories manually", min_value=0, max_value=2000, value=0)
        if manual_calories > 0 and st.button("➕ Add Manual Calories"):
            st.session_state.daily_calories += manual_calories
            st.success(f"Added {manual_calories} calories!")
        
        # Reset daily calories
        if st.button("🔄 Reset Daily Counter"):
            st.session_state.daily_calories = 0
            st.success("Daily calories reset!")
        
        # Progress bar
        if st.session_state.daily_calories > 0:
            progress = min(st.session_state.daily_calories / daily_goal, 1.0)
            st.progress(progress)
            
            if st.session_state.daily_calories >= daily_goal:
                st.success("🎉 Daily calorie goal reached!")
            else:
                remaining = daily_goal - st.session_state.daily_calories
                st.info(f"💪 {remaining} calories remaining to reach your goal!")

def main():
    load_css()
    init_session_state()
    
    if not st.session_state.user_authenticated:
        show_auth_page()
        return
    
    # Sidebar navigation
    st.sidebar.title("🍲 Recipe Quest")
    st.sidebar.write(f"👋 Welcome, {st.session_state.current_user}!")
    
    pages = {
        "🏠 Home": show_home,
        "🥘 Recipes": show_recipes,
        "📅 Meal Planner": show_meal_planner,
        "⏰ Cooking Timer": show_cooking_timer,
        "🎮 Cooking Game": show_cooking_game,
        "🍹 Drinks": show_drinks,
        "📝 Notes": show_notes,
        "⚙️ Settings": show_settings
    }
    
    selected_page = st.sidebar.radio("Navigate", list(pages.keys()))
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.metric("🔍 Total Recipes", len(RECIPES))
    st.sidebar.metric("❤️ Favorites", len(st.session_state.favorites))
    st.sidebar.metric("🏆 Game Score", st.session_state.game_score)
    st.sidebar.metric("🔥 Today's Calories", st.session_state.daily_calories)
    
    # Theme application - Add data-theme attribute to body
    theme_js = f"""
    <script>
    document.body.setAttribute('data-theme', '{st.session_state.theme.lower()}');
    </script>
    """
    st.components.v1.html(theme_js, height=0)
    
    # Additional theme-specific adjustments
    if st.session_state.theme == "Dark":
        st.markdown("""
        <style>
        /* Additional dark theme fixes */
        .stButton>button {
            background: #444 !important;
            color: white !important;
            border: 1px solid #666 !important;
        }
        .stSelectbox>div>div {
            background-color: #3d3d3d !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif st.session_state.theme == "Food":
        st.markdown("""
        <style>
        /* Additional food theme fixes */
        .stButton>button {
            background: linear-gradient(135deg, #ff7b35 0%, #ff5a1a 100%) !important;
            color: white !important;
            border: none !important;
        }
        .main-header {
            background: linear-gradient(135deg, #ff7b35 0%, #ff5a1a 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Display selected page
    pages[selected_page]()

if __name__ == "__main__":  # No spaces before this line
    main()