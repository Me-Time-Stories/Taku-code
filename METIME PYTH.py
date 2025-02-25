import streamlit as st
import logging
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(page_title="Me Time Stories", page_icon="📖", layout="wide")

# Update the CSS section with enhanced styling
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f8fafc;
    }

    /* Navigation Bar */
    .top-nav {
        background: linear-gradient(135deg, #2A4365 0%, #1a365d 100%);
        padding: 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .nav-item {
        color: white;
        padding: 0.75rem 1.5rem;
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .nav-item:hover {
        background-color: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }

    /* Logo and Branding */
    .logo-text {
        font-family: 'Playfair Display', serif;
        color: #2A4365;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .tagline {
        color: #2A4365;
        font-style: italic;
        font-size: 1.3em;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
    }

    /* Dashboard Cards */
    .dashboard-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        border: 1px solid #e2e8f0;
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #2A4365 0%, #1a365d 100%);
        color: white;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 1rem;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Metrics and Stats */
    .metrics-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Story Cards */
    .story-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .story-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }

    /* Progress Bars */
    .stProgress > div > div {
        background-color: #2A4365;
        height: 10px;
        border-radius: 5px;
    }

    /* Select Boxes */
    .stSelectbox {
        border-radius: 10px;
    }

    /* Text Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }

    /* Charts and Graphs */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'story_choice' not in st.session_state:
    st.session_state.story_choice = None
if 'page' not in st.session_state:
    st.session_state.page = "landing"
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'teacher_dashboard' not in st.session_state:
    st.session_state.teacher_dashboard = {
        "students": [
            {"name": "Alice", "reading_time": 120, "stories_completed": 5},
            {"name": "Bob", "reading_time": 90, "stories_completed": 3},
            {"name": "Charlie", "reading_time": 150, "stories_completed": 7}
        ],
        "class_stats": {
            "total_reading_time": 360,
            "total_stories_completed": 15,
            "average_reading_time": 120
        },
        "recommendations": {
            "Alice": ["Time-Travelling Tractor", "Romeo & Juliet"],
            "Bob": ["Moses & Pharaoh", "Diary of a Wimpy Kid"],
            "Charlie": ["The Treasure in the Treehouse", "Time-Travelling Tractor"]
        }
    }
if 'child_dashboard' not in st.session_state:
    st.session_state.child_dashboard = {
        "achievements": [
            {"title": "First Story", "description": "Completed your first story", "earned": False},
            {"title": "Bookworm", "description": "Read for 30 minutes", "earned": False},
            {"title": "Story Explorer", "description": "Try all story types", "earned": False}
        ],
        "favorite_stories": [],
        "reading_stats": {
            "weekly_minutes": [0] * 7,  # Last 7 days
            "stories_by_type": {
                "Adventure": 0,
                "Fantasy": 0,
                "Historical": 0,
                "Comedy": 0,
                "Drama": 0
            }
        },
        "current_streak": 0,
        "last_read": None
    }
if 'parent_dashboard' not in st.session_state:
    st.session_state.parent_dashboard = {
        "child_name": "Default",
        "reading_time": 0,
        "completed_stories": [],
        "preferences": {"educational": True, "bedtime_mode": False, "sound_effects": True, "read_aloud": False},
        "last_read": datetime.now()
    }
if 'subscription_plans' not in st.session_state:
    st.session_state.subscription_plans = {
        "basic": {
            "name": "Basic",
            "price": "£9.99/month",
            "books": 3,
            "tokens": 50,
            "features": [
                "3 printed books/month",
                "50 customization tokens",
                "Basic story templates",
                "Digital reading unlimited"
            ]
        },
        "premium": {
            "name": "Premium",
            "price": "£14.99/month",
            "books": 6,
            "tokens": 100,
            "features": [
                "6 printed books/month",
                "100 customization tokens",
                "Advanced story templates",
                "Priority support",
                "Digital reading unlimited"
            ]
        },
        "unlimited": {
            "name": "Unlimited",
            "price": "£19.99/month",
            "books": -1,  # Unlimited
            "tokens": 200,
            "features": [
                "Unlimited printed books",
                "200 customization tokens",
                "All story templates",
                "Priority support",
                "Digital reading unlimited",
                "Exclusive content"
            ]
        }
    }


# Define gamified question flow
gamified_questions = [
    ("user_name", "Hi! What's your name? 😊"),
    ("mother_name", "Nice to meet you, {user_name}! What's your mom's name?"),
    ("father_name", "And your dad's name?"),
    ("has_sibling", "Do you have any siblings? (Yes/No)"),
    ("older_sibling", "What's your older sibling's name?", "has_sibling", "Yes"),
    ("younger_sibling", "What's your younger sibling's name?", "has_sibling", "Yes"),
    ("uncle_name", "What about an uncle? Who's your favorite?"),
    ("grandparent_name", "And a grandparent you love?"),
    ("friend_home", "Who's your best friend?"),
    ("villain_name", "If you were in an adventure story, who would be your arch-nemesis?"),
]

def parent_dashboard():
    st.title("👨‍👩‍👧‍👦 Parent Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Reading Time", f"{st.session_state.parent_dashboard['reading_time']} mins")
    with col2:
        st.metric("Stories Completed", len(st.session_state.parent_dashboard['completed_stories']))

    st.subheader("Reading Preferences")
    educational = st.checkbox("Educational Content",
                            value=st.session_state.parent_dashboard['preferences']['educational'])
    bedtime = st.checkbox("Bedtime Mode",
                         value=st.session_state.parent_dashboard['preferences']['bedtime_mode'])

    if st.button("Save Preferences"):
        st.session_state.parent_dashboard['preferences']['educational'] = educational
        st.session_state.parent_dashboard['preferences']['bedtime_mode'] = bedtime
        st.success("Preferences saved!")

def collect_user_data():
    st.title("📖 MeTime: Personalized Story Generator")

    current_step = st.session_state.step - 1

    if current_step < len(gamified_questions):
        key, question, *condition = gamified_questions[current_step]

        if condition:
            condition_key, expected_value = condition
            if st.session_state.user_data.get(condition_key) != expected_value:
                st.session_state.step += 1
                st.rerun()
                return

        response = st.text_input(
            question.format(**st.session_state.user_data) if '{' in question else question
        )

        if st.button("Next"):
            if response:
                st.session_state.user_data[key] = response
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("Please enter something to continue.")
    else:
        st.session_state.page = "select_story"
        st.rerun()

def generate_moses_story():
    data = st.session_state.get('user_data', {})
    return f"""
    # {data.get('user_name', 'Moses')} & The Tyranny of Pharaoh {data.get('villain_name', 'Pharaoh')}

    In the scorching heat of ancient Egypt, where the mighty Nile flowed like a ribbon of life through the desert, 
    lived a young person named {data.get('user_name')}. The Israelites had been enslaved for generations under the cruel rule 
    of Pharaoh {data.get('villain_name')}.

    One day, while tending to the sheep with {data.get('friend_home')}, {data.get('user_name')} witnessed something extraordinary
    - a bush that burned but was not consumed. God spoke through the burning bush, saying:

    "I have indeed seen the misery of my people in Egypt. I am sending you to Pharaoh to bring my people out of Egypt."

    {data.get('user_name')} was hesitant at first, saying, "Who am I to go to Pharaoh?"

    But with the support of {data.get('older_sibling', 'Aaron')} as a spokesperson, {data.get('user_name')} gained courage
    and confronted Pharaoh {data.get('villain_name')}.

    "Let my people go!" {data.get('user_name')} demanded, standing tall before the throne.

    Pharaoh {data.get('villain_name')} laughed mockingly. "Who is this God that I should obey him?"

    Thus began the great contest between God's power and Pharaoh's stubbornness. One by one, ten terrible plagues struck Egypt:

    1. The water turned to blood
    2. Frogs covered the land
    3. Gnats swarmed everywhere
    4. Flies filled the air
    5. Disease struck the livestock
    6. Painful boils afflicted the people
    7. Devastating hail fell from the sky
    8. Locusts devoured the crops
    9. Darkness covered the land for three days
    10. The final, most terrible plague - the death of the firstborn

    After each plague, {data.get('user_name')} would return to Pharaoh:
    "Thus says the Lord: 'Let my people go, that they may serve me.'"

    Finally, after the last plague, Pharaoh relented. The Israelites rushed to leave, led by {data.get('user_name')}.
    But Pharaoh changed his mind! He sent his army in pursuit.

    The Israelites reached the Red Sea, trapped between the water and the approaching army. {data.get('friend_home')} cried out,
    "What will we do now?"

    {data.get('user_name')} raised the staff as God had commanded. The waters parted, creating walls of water on either side.
    The people crossed on dry ground!

    When Pharaoh's army tried to follow, the waters crashed back together, and the Egyptian army was no more.
    {data.get('mother_name')} led the women in songs of victory, while {data.get('father_name')} and the men celebrated their freedom.

    That night, as the stars shone over the desert, {data.get('grandparent_name')} gathered the children to recount the miracle
    they had witnessed. "Remember this day," they said, "for generations to come will tell of how {data.get('user_name')} led
    our people to freedom."

    And so began the journey to the Promised Land, with {data.get('user_name')} leading the way, guided by God's presence in
    a pillar of cloud by day and fire by night.

    The End
    """

def generate_wimpy_kid_story():
    data = st.session_state.get('user_data', {})
    return f"""
    # Diary of {data.get('user_name', 'Greg')}

    Dear Diary,

    You won't BELIEVE the week I've had. Mom ({data.get('mother_name')}) says I should write down my feelings or whatever,
    so here goes nothing.

    Monday:
    It all started when my best friend {data.get('friend_home')} came up with this "brilliant" idea to run for class president.
    The thing is, I was planning to do absolutely nothing this year - which, by the way, is a legitimate life strategy.

    {data.get('friend_home')}: "Come on, you'd make a great campaign manager!"
    Me: "I'd rather eat my gym socks."
    {data.get('friend_home')}: "I'll split my lunch with you for a month."
    Me: "... I'm listening."

    Tuesday:
    Dad ({data.get('father_name')}) found out about the campaign thing and got WAY too excited. He started telling me about
    his "glory days" in student government, which was about as fun as watching paint dry.

    The worst part? My arch-nemesis {data.get('villain_name')} decided to run too. Because OF COURSE they did.

    Wednesday:
    Things got really weird when {data.get('older_sibling')} offered to help. And by "help," I mean completely take over
    and turn everything into some kind of professional operation. They even made SPREADSHEETS. Who does that?

    {data.get('older_sibling')}: "We need to analyze the demographic voting patterns of fourth graders."
    Me: "They vote based on who has the coolest shoes."
    {data.get('older_sibling')}: "Exactly! That's data!"

    Thursday:
    Disaster struck during the campaign speech. {data.get('friend_home')} was doing great until {data.get('younger_sibling')}
    ran onto the stage with my embarrassing baby photos. Apparently, {data.get('villain_name')} had convinced them it would
    be "hilarious."

    The audience:
    "Awww, is that {data.get('user_name')} in a duck costume?"
    "Look at those chubby cheeks!"
    Me: *dying inside*

    Friday:
    Uncle {data.get('uncle_name')} showed up at school with a campaign truck and started handing out free ice cream.
    Which would have been awesome if it wasn't AGAINST THE RULES. Principal Johnson was not amused.

    Principal Johnson: "This is a school election, not a state senate race!"
    Uncle {data.get('uncle_name')}: "The people deserve ice cream!"
    Me: *pretending to be invisible*

    Saturday:
    Grandparent {data.get('grandparent_name')} came over to "comfort" me about the whole election disaster, but ended up
    telling stories about their own school days that made my week look totally normal.

    {data.get('grandparent_name')}: "Did I ever tell you about the time I ran for class treasurer and accidentally set
    the gym on fire?"
    Me: "No, and please don't."

    Sunday:
    Plot twist! {data.get('friend_home')} won the election! Turns out the baby photos actually helped - people thought
    they were "adorable" or whatever. 

    The victory party at my house was actually pretty cool until {data.get('younger_sibling')} started a food fight
    and Mom ({data.get('mother_name')}) made everyone help clean up.

    So yeah, that's been my week. {data.get('villain_name')} is still giving me the evil eye, but whatever. At least
    I'm getting free lunch for a month.

    Note to self: Next time someone asks for help with anything, run in the opposite direction.

    - {data.get('user_name')}

    P.S. If anyone's reading this (looking at you, {data.get('younger_sibling')}), I will deny everything.
    """

def generate_tractor_story():
    data = st.session_state.get('user_data', {})
    return f"""
    # {data.get('user_name')} & The Time-Travelling Tractor

    It was just another ordinary Saturday morning when {data.get('user_name')} visited their Uncle {data.get('uncle_name')}'s farm.
    The sun was barely peeking over the horizon, and the morning dew sparkled on the grass like tiny diamonds.

    "Now remember," Uncle {data.get('uncle_name')} said sternly, "don't touch the old red tractor in the back barn.
    There's something peculiar about it."

    Of course, telling {data.get('user_name')} not to do something was practically an invitation to do exactly that.
    Especially when {data.get('friend_home')} was visiting too.

    "Come on," whispered {data.get('friend_home')}, "let's check it out!"

    The old red tractor sat in the shadows of the barn, covered in a thin layer of dust. It looked ordinary enough,
    except for the strange golden dial on the dashboard marked with different years.

    {data.get('user_name')}: "I wonder what this does..."
    {data.get('friend_home')}: "Maybe we should listen to your uncle..."
    {data.get('user_name')}: "Just one tiny turn..."

    *FLASH* *BOOM* *WHIRRRRR*

    Suddenly, the barn disappeared! The tractor was now sitting in the middle of a lush jungle, and the air was thick
    and humid. A massive shadow passed overhead.

    {data.get('friend_home')}: "Is that... a PTERODACTYL?!"
    {data.get('user_name')}: "We're in the age of dinosaurs!"

    They weren't alone for long. A curious young Triceratops wandered over to investigate the strange machine.
    {data.get('user_name')} decided to name it {data.get('younger_sibling')}, because it reminded them of their
    younger sibling - especially when it started headbutting the tractor playfully.

    But their adventure was about to get more exciting - and dangerous. A terrifying roar echoed through the trees.

    "That sounds like {data.get('villain_name')}!" {data.get('friend_home')} exclaimed, referring to their school bully.
    But this was much worse - it was a Tyrannosaurus Rex!

    The massive predator burst through the trees, its teeth gleaming in the prehistoric sun. {data.get('user_name')}
    jumped into the driver's seat and turned the key. The tractor sputtered to life!

    "Hold on!" {data.get('user_name')} shouted as they spun the year dial randomly.

    *FLASH* *BOOM* *WHIRRRRR*

    Now they were in medieval times! Knights in shining armor stared in amazement at the mysterious red machine.
    One knight, who looked surprisingly like {data.get('older_sibling')}, raised his visor in shock.

    "What sorcery is this?" the knight demanded.

    Before they could answer, {data.get('user_name')} noticed the dial was spinning on its own!

    *FLASH* *BOOM* *WHIRRRRR*

    They landed in Ancient Egypt, right in the middle of building the pyramids! The workers scattered as the tractor
    appeared out of nowhere. A wise-looking overseer who reminded them of {data.get('grandparent_name')} approached
    cautiously.

    But the dial kept spinning!

    They visited:
    - The Wild West, where they accidentally joined a cattle drive
    - Ancient Rome, where they crashed a chariot race
    - The first Moon landing, where they had to hide the tractor behind a crater
    - The age of pirates, where they nearly became part of a crew

    Finally, with one last *FLASH* *BOOM* *WHIRRRRR*, they found themselves back in Uncle {data.get('uncle_name')}'s barn.
    Only seconds had passed.

    "Did... did that really happen?" {data.get('friend_home')} asked, still shaking.

    {data.get('user_name')} was about to answer when they noticed something in their pocket - a small dinosaur tooth,
    a piece of pyramid stone, and a pirate's gold coin.

    Just then, Uncle {data.get('uncle_name')} walked in. "I see you found my special tractor," he said with a knowing smile.
    "Your mom {data.get('mother_name')} and dad {data.get('father_name')} had quite an adventure with it when they
    were your age too."

    {data.get('user_name')} and {data.get('friend_home')} looked at each other in amazement. This was definitely
    going to be a secret worth keeping!

    The End

    (But maybe not really the end... that golden dial is still turning...)
    """

def generate_romeo_juliet_story():
    data = st.session_state.get('user_data', {})
    return f"""
    # The Tale of {data.get('user_name')} & {data.get('friend_home')}

    In the beautiful city of Verona, where our story takes place, two families had been feuding for so long that
    no one could remember why it started. The {data.get('mother_name')} family and the {data.get('father_name')} family
    were both respected, both wealthy, and both equally stubborn.

    Young {data.get('user_name')}, of the {data.get('mother_name')} family, had never given much thought to the feud
    until the night of the grand masquerade ball. That's where they first saw {data.get('friend_home')}, who belonged
    to the rival {data.get('father_name')} family.

    The great hall was filled with music and laughter, the crystal chandeliers casting magical shadows on the walls.
    {data.get('user_name')} wore a mask of silver stars, while {data.get('friend_home')} chose one decorated with
    golden leaves.

    Their eyes met across the crowded room:

    {data.get('user_name')}: *thinking* "Who is that beautiful stranger?"
    {data.get('friend_home')}: *thinking* "I've never seen anyone so enchanting..."

    They danced together, lost in their own world, until {data.get('older_sibling')} recognized {data.get('friend_home')}
    and whispered the terrible truth to {data.get('user_name')}.

    Later that night, unable to stay away, {data.get('user_name')} snuck into the {data.get('father_name')} family's
    garden. {data.get('friend_home')} stood on the famous balcony, talking to the stars:

    {data.get('friend_home')}: "Oh, {data.get('user_name')}, why must you be a {data.get('mother_name')}? What's in
    a name? That which we call a rose by any other name would smell as sweet..."

    {data.get('user_name')} stepped out from behind the rose bushes:
    "My feelings for you are worth all the stars in the sky!"

    But their secret meetings were discovered by {data.get('villain_name')}, who had always despised both families.
    They threatened to reveal everything unless {data.get('friend_home')} agreed to marry them instead.

    {data.get('villain_name')}: "Choose wisely, or both families will suffer!"

    But true love found unexpected allies. {data.get('uncle_name')}, who had always thought the feud was foolish,
    offered to help. And wise {data.get('grandparent_name')} knew of an ancient law that could end the feud once
    and for all.

    The young lovers made a bold plan. During the next full moon, they would meet at the old church where
    {data.get('grandparent_name')} had arranged for a secret ceremony. But {data.get('villain_name')} discovered
    their plan.

    The night of the wedding, as {data.get('user_name')} waited anxiously at the church, {data.get('villain_name')}
    arrived with both families in tow, expecting to cause chaos.

    But something unexpected happened. When the families saw the pure love between {data.get('user_name')} and
    {data.get('friend_home')}, and heard {data.get('grandparent_name')}'s words about the foolishness of their
    ancient quarrel, hearts began to soften.

    {data.get('mother_name')}: "Perhaps it's time to end this feud..."
    {data.get('father_name')}: "Our children's happiness is worth more than our pride..."

    Even {data.get('villain_name')} was moved by the power of their love, though they tried to hide it behind
    their usual scowl.

    The wedding proceeded, more beautiful than anyone could have imagined. {data.get('younger_sibling')} scattered
    rose petals, while {data.get('older_sibling')} played the violin. The two families sat together, sharing tears
    of joy instead of anger.

    And so, the ancient feud ended not with violence, but with love. {data.get('user_name')} and {data.get('friend_home')}
    proved that the power of love could bridge any divide, heal any wound, and bring peace to even the most bitter
    of enemies.

    They lived happily ever after, and their story was told for generations as proof that love truly conquers all.

    The End
    """

def generate_treehouse_story():
    data = st.session_state.get('user_data', {})
    return f"""
    # The Treasure in the Treehouse

    {data.get('user_name')} had always known their treehouse was special. Built by their grandfather {data.get('grandparent_name')}
    years ago, it stood majestically in the ancient oak tree at the bottom of their garden. But they never expected
    to find actual treasure there!

    It all started on a rainy Saturday morning when Mom ({data.get('mother_name')}) was cleaning the attic.
    She found an old map with mysterious markings.

    "Look what I found in your grandfather's things," she said, handing {data.get('user_name')} a weathered envelope.

    Inside was a letter:

    "Dear {data.get('user_name')},
    If you're reading this, you're old enough for an adventure. The treehouse holds more secrets than you know.
    Follow the clues, but beware - you're not the only one looking for treasure!
    Love, Grandparent {data.get('grandparent_name')}"

    {data.get('user_name')} immediately called their best friend {data.get('friend_home')} over.

    {data.get('friend_home')}: "This is just like those adventure movies we watch!"
    {data.get('user_name')}: "But this is real! Look at these weird symbols..."

    The first clue led them to a loose board in the treehouse floor, where they found an old compass
    and another note. But they weren't alone - {data.get('villain_name')}, the neighborhood troublemaker,
    had been spying on them!

    {data.get('villain_name')}: "Whatever you found up there, it's mine now!"
    {data.get('user_name')}: "No way! This is my grandfather's treasure!"

    A chase ensued around the garden, with {data.get('older_sibling')} and {data.get('younger_sibling')}
    joining in to help their sibling. Uncle {data.get('uncle_name')}, who was visiting, watched the chaos
    with amusement.

    The hunt led them all over:
    - Behind the old shed (where they found a mysterious key)
    - Under Dad ({data.get('father_name')})'s workbench (discovering a cryptic riddle)
    - Through Mom's flower garden (sorry, Mom!)
    - Up to the attic again (following a trail of clues)

    Each clue was cleverer than the last, and {data.get('user_name')} realized their grandfather had planned
    this elaborate treasure hunt years ago!

    The final clue read:
    "Where leaves dance in summer's breeze,
    Where childhood dreams swing in the trees,
    Look not down but up above,
    To find the treasure filled with love."

    {data.get('user_name')} and {data.get('friend_home')} climbed to the very top of the treehouse.
    Even {data.get('villain_name')} stopped trying to steal the clues and watched in amazement.

    There, hidden in a secret compartment in the roof, they found a small chest. Inside was:
    - A collection of family photographs
    - Handwritten stories about {data.get('grandparent_name')}'s adventures
    - A special note for each grandchild
    - And a real gold coin from a Spanish galleon!

    But the real treasure was the letter explaining how the treehouse itself was built with love,
    designed to bring family and friends together for generations of adventures.

    {data.get('villain_name')}, touched by the story, admitted, "That's better than any treasure I
    could have stolen."

    They all ended up sitting in the treehouse together, sharing stories and snacks that Mom brought up.
    Even Uncle {data.get('uncle_name')} climbed up to join them!

    That evening, as the sun set, {data.get('user_name')} added their own note to the treasure chest,
    starting a new tradition for future generations to discover.

    The treehouse had always been special, but now it was magical - a place where adventures began,
    friendships were strengthened, and family memories would live forever.

    The End
    """

def generate_story():
    st.title("📜 Your Personalized Story")

    story_choice = st.session_state.get('story_choice')

    # Track reading timestart_time = datetime.now()

    if story_choice == "Moses & Pharaoh":story = generate_moses_story()
    elif story_choice == "Diary of a Wimpy Kid":
        story = generate_wimpy_kid_story()
    elif story_choice == "Time-Travelling Tractor":
        story = generate_tractor_story()
    elif story_choice == "Romeo& Juliet":
        story = generate_romeo_juliet_story()
    else:  # "The Treasure in the Treehouse"
        story = generate_treehouse_story()

    st.markdown(story)

    if st.button("Finish Reading"):
        end_time = datetime.now()
        reading_duration = (end_time - start_time).seconds // 60
        st.session_state.parent_dashboard['reading_time'] += reading_duration
        if story_choice not in st.session_state.parent_dashboard['completed_stories']:
            st.session_state.parent_dashboard['completed_stories'].append(story_choice)
        st.session_state.page = "select_story"
        st.rerun()

def select_story():
    st.title("📚 Choose Your Story")

    story_choice = st.radio(
        "Select a story:",
        ["Moses & Pharaoh", "Diary of a Wimpy Kid", "Time-Travelling Tractor",
         "Romeo & Juliet", "The Treasure in the Treehouse"]
    )

    if st.button("Generate Story ✨"):
        st.session_state.story_choice = story_choice
        st.session_state.page = "generate_story"
        st.rerun()

def show_login():
    # Add logo and branding
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 class="logo-text">Me Time Stories</h1>
            <p class="tagline">Where You are the center of every Story</p>
        </div>
    """, unsafe_allow_html=True)

    # Add dashboard options with enhanced styling
    st.markdown('<div style="max-width: 1200px; margin: 0 auto;">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3>👨‍🏫 Teacher Dashboard</h3>
            <p style="color: #4a5568; margin: 1rem 0;">Create engaging lessons and track student progress with our comprehensive teaching tools.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Login as Teacher", key="teacher_btn"):
            st.session_state.user_type = "teacher"
            st.session_state.page = "teacher_dashboard"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3>👶 Student Dashboard</h3>
            <p style="color: #4a5568; margin: 1rem 0;">Embark on your personalized reading adventure with interactive stories and fun challenges.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Student", key="student_btn"):
            st.session_state.user_type = "student"
            st.session_state.page = "collect_data"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <h3>👨‍👩‍👧‍👦 Parent Dashboard</h3>
            <p style="color: #4a5568; margin: 1rem 0;">Track your child's reading journey and customize their learning experience.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Parent Access", key="parent_btn"):
            st.session_state.page = "parent_dashboard"
            st.rerun()

    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <h3>✍️ Author Portal</h3>
            <p style="color: #4a5568; margin: 1rem 0;">Create and publish engaging educational content for our growing community.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Author Login", key="author_btn"):
            st.session_state.user_type = "author"
            st.session_state.page = "author_portal"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def student_progress_tracking():
    """Live Student Progress Monitoring"""
    st.title("📊 Student Performance Tracker")

    # Simulated Real-Time Progress Data
    student_data = [
        {"name": "Alice", "completion": 90, "accuracy": 85, "current_task": "Comprehension Practice"},
        {"name": "Bob", "completion": 65, "accuracy": 70, "current_task": "Word Problems"},
        {"name": "Charlie", "completion": 40, "accuracy": 50, "current_task": "Basic Addition"},
    ]

    for student in student_data:
        with st.expander(f"🎓 {student['name']} - {student['current_task']}"):
            st.progress(student["completion"])
            st.write(f"✅ **Accuracy:** {student['accuracy']}%")

            # Live AI Recommendations
            if student["accuracy"] < 60:
                st.warning("⚠️ AI Suggests: Reduce difficulty, add extra practice.")
            elif 60 <= student["accuracy"] < 80:
                st.info("🔹 AI Suggests: Assign more mixed exercises.")
            else:
                st.success("✅ AI Suggests: Move to more challenging tasks.")

def teacher_dashboard():
    st.title("👩‍🏫 Teacher Dashboard")

    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", [
            "Lesson Planning",
            "Student Progress",
            "Class Management",
            "Resources Library"
        ])

    if page == "Lesson Planning":
        show_lesson_planner()
    elif page == "Student Progress":
        student_progress_tracking()
    elif page == "Class Management":
        manage_classes()
    else:
        show_resources_library()

def show_lesson_planner():
    st.header("📚 Lesson Planning")

    # Subject Selection
    subject = st.selectbox("Select Subject", 
        ["English", "Mathematics", "Science", "Biology"]
    )

    # Key Stage Selection
    key_stage = st.selectbox("Select Key Stage", 
        ["KS1", "KS2", "KS3", "KS4"]
    )

    # Class Selection
    selected_class = st.selectbox("Select Class", 
        ["Class 7A", "Class 8B", "Class 9C"]
    )

    # Common Controls
    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.slider("Difficulty Level", 1, 5, 3)
        comprehension_level = st.slider("Comprehension Level", 1, 5, 3)
    with col2:
        duration = st.number_input("Lesson Duration (minutes)", min_value=30, max_value=120, value=60)
        interactive_elements = st.slider("Interactive Elements", 1, 5, 3)

    # Subject Specific Controls
    if subject == "English":
        show_english_controls()
    elif subject == "Mathematics":
        show_math_controls()
    elif subject == "Science":
        show_science_controls()
    elif subject == "Biology":
        show_biology_controls()

def show_english_controls():
    st.subheader("📖 English Lesson Configuration")

    # Text Analysis Tools
    st.markdown("### Text Analysis Tools")
    text_type = st.selectbox("Select Text Type", 
        ["Story", "Poetry", "Non-Fiction", "Drama"]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Grammar Analysis")
        st.checkbox("Vocabulary Builder")
        st.checkbox("Creative Writing Prompts")
    with col2:
        st.checkbox("Reading Comprehension")
        st.checkbox("Literary Devices")
        st.checkbox("Character Analysis")

    # Task Configuration
    st.markdown("### Task Settings")
    num_questions = st.slider("Number of Questions", 5, 30, 15)
    writing_length = st.select_slider("Writing Task Length", 
        options=["Short", "Medium", "Long", "Extended"]
    )

    # Preview Area
    st.markdown("### Lesson Preview")
    st.info("📝 Interactive text analysis tools will highlight grammar, vocabulary, and literary devices in real-time")

    if st.button("Generate Lesson Plan"):
        st.success("Lesson plan generated! Check the Resources tab to view and modify.")

def show_math_controls():
    st.subheader("🔢 Mathematics Lesson Configuration")

    # Topic Selection
    topic = st.selectbox("Select Topic", 
        ["Algebra", "Geometry", "Statistics", "Calculus"]
    )

    # Visual Tools
    st.markdown("### Visual Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Interactive Graphs")
        st.checkbox("Step-by-Step Solutions")
        st.checkbox("3D Shapes Visualization")
    with col2:
        st.checkbox("Real-world Examples")
        st.checkbox("Formula Breakdown")
        st.checkbox("Practice Problems")

    # Equation Complexity
    st.markdown("### Equation Settings")
    eq_complexity = st.select_slider("Equation Complexity", 
        options=["Basic", "Intermediate", "Advanced", "Challenge"]
    )

    # Preview Area
    st.markdown("### Interactive Preview")
    st.info("📊 Equations will be visualized with step-by-step breakdowns and real-world applications")

    if st.button("Generate Math Lesson"):
        st.success("Math lesson materials generated! View in Resources tab.")

def show_science_controls():
    st.subheader("🧪 Science Lesson Configuration")

    # Topic Selection
    topic = st.selectbox("Select Topic", 
        ["States of Matter", "Chemical Reactions", "Forces", "Energy"]
    )

    # Visualization Tools
    st.markdown("### Visualization Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Molecular Structure Viewer")
        st.checkbox("Chemical Reaction Simulator")
        st.checkbox("Interactive Experiments")
    with col2:
        st.checkbox("Real-time Data Graphs")
        st.checkbox("3D Models")
        st.checkbox("Virtual Lab Setup")

    # Example: H2O Visualization
    st.markdown("### Interactive Models")
    st.info("💧 Water (H2O) Molecular Structure will be shown with interactive 3D model")

    if st.button("Generate Science Lesson"):
        st.success("Science lesson with interactive visualizations generated!")

def show_biology_controls():
    st.subheader("🧬 Biology Lesson Configuration")

    # System Selection
    system = st.selectbox("Select Body System", 
        ["Respiratory", "Circulatory", "Digestive", "Nervous"]
    )

    # Visualization Tools
    st.markdown("### Visualization Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("3D Anatomy Models")
        st.checkbox("System Animations")
        st.checkbox("Cell Structure Viewer")
    with col2:
        st.checkbox("Process Simulations")
        st.checkbox("Interactive Diagrams")
        st.checkbox("Virtual Dissection")

    # Animation Settings
    st.markdown("### Animation Controls")
    animation_speed = st.slider("Animation Speed", 1, 5, 3)
    detail_level = st.select_slider("Detail Level", 
        options=["Basic", "Intermediate", "Advanced", "Medical"]
    )

    # Preview Area
    st.markdown("### System Preview")
    st.info("🫁 Interactive anatomy models will show detailed animations of selected body systems")

    if st.button("Generate Biology Lesson"):
        st.success("Biology lesson with interactive models generated!")

def manage_classes():
    st.subheader("👥 Class Management")

    # Class Overview
    classes = {
        "Class 7A": {"students": 25, "average_level": "Intermediate"},
        "Class 8B": {"students": 28, "average_level": "Advanced"},
        "Class 9C": {"students": 22, "average_level": "Basic"}
    }

    for class_name, details in classes.items():
        with st.expander(f"{class_name} - {details['students']} students"):
            st.write(f"Average Level: {details['average_level']}")
            st.button(f"View Individual Progress ({class_name})")
            st.button(f"Adjust Class Settings ({class_name})")

def show_resources_library():
    st.subheader("📚 Resources Library")

    # Resource Categories
    categories = ["Lesson Plans", "Interactive Materials", "Assessments", "Visual Aids"]

    for category in categories:
        with st.expander(category):
            st.write("Recent Resources:")
            st.write("• Interactive Algebra Solver")
            st.write("• Virtual Science Lab")
            st.write("• 3D Biology Models")
            st.button(f"Upload New {category}")

def show_author_portal():
    st.title("✍️ Author Portal")

    # Author Dashboard Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reads", "12.5K")
    with col2:
        st.metric("Active Licenses", "45")
    with col3:
        st.metric("Revenue this Month", "£2,450")

    # Story Management
    st.subheader("📚 My Stories")

    with st.expander("Create New Story"):
        st.text_input("Story Title")
        genre = st.selectbox("Genre", ["Adventure", "Educational", "Fantasy", "Historical"])
        age_range = st.select_slider("Target Age Range", options=["4-6", "7-9", "10-12", "13+"])
        customization = st.multiselect(
            "Customizable Elements",
            ["Character Names", "Locations", "Plot Elements", "Visual Themes"]
        )

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("AI Writing Assistant")
            st.checkbox("Interactive Elements")
        with col2:
            st.checkbox("Educational Content")
            st.checkbox("Multi-language Support")

        if st.button("Start Writing"):
            st.success("Story template created! Opening editor...")

    # Story Analytics
    st.subheader("📊 Story Performance")
    stories = {
        "The Magic Garden": {"reads": 5200, "rating": 4.8, "revenue": "£850"},
        "Space Adventures": {"reads": 3800, "rating": 4.6, "revenue": "£620"},
        "Math with Dragons": {"reads": 3500, "rating": 4.7, "revenue": "£580"}
    }

    for title, stats in stories.items():
        with st.expander(f"{title} Statistics"):
            st.write(f"Total Reads: {stats['reads']}")
            st.write(f"Average Rating: ⭐ {stats['rating']}/5.0")
            st.write(f"Revenue Generated: {stats['revenue']}")
            st.progress(int(stats['rating'] / 5.0 * 100))

            col1, col2 = st.columns(2)
            with col1:
                st.button(f"Edit {title}")
            with col2:
                st.button(f"View Analytics for {title}")

    # Licensing Management
    st.subheader("💰 Licensing & Revenue")
    with st.expander("License Management"):
        st.write("Current License Terms:")
        st.write("• School License: 60% revenue share")
        st.write("• Individual License: 70% revenue share")
        st.write("• Bulk Purchase: 65% revenue share")

        if st.button("Modify License Terms"):
            st.info("Contact support to modify your license terms")

    # Revenue Analytics
    st.subheader("📈 Revenue Analytics")
    chart_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Revenue': [1200, 1500, 1800, 2200, 2450]
    })

    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x='Month',
        y='Revenue',
        tooltip=['Month', 'Revenue']
    ).properties(title='Monthly Revenue')

    st.altair_chart(chart, use_container_width=True)

def enhanced_parent_dashboard():
    st.title("👨‍👩‍👧‍👦 Parent Dashboard")

    # Child Selection (if multiple children)
    child_name = st.selectbox("Select Child", 
        [st.session_state.parent_dashboard["child_name"], "Add New Child +"]
    )

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Reading Time", f"{st.session_state.parent_dashboard['reading_time']} mins")
    with col2:
        st.metric("Stories Completed", len(st.session_state.parent_dashboard['completed_stories']))
    with col3:
        st.metric("Current Streak", "5 days")
    with col4:
        st.metric("Reading Level", "Advanced")

    # Reading Progress
    st.subheader("📚 Reading Journey")

    # Weekly Progress Chart
    progress_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Minutes': [30, 45, 20, 60, 30, 45, 15]
    })

    chart = alt.Chart(progress_data).mark_bar().encode(
        x='Day',
        y='Minutes',
        color=alt.value('#2A4365')
    ).properties(title='Weekly Reading Activity')

    st.altair_chart(chart, use_container_width=True)

    # Learning Preferences
    st.subheader("🎯 Learning Settings")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Reading Preferences")
        reading_level = st.select_slider(
            "Reading Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        st.checkbox("Educational Focus", value=st.session_state.parent_dashboard['preferences']['educational'])
        st.checkbox("Bedtime Mode", value=st.session_state.parent_dashboard['preferences']['bedtime_mode'])

    with col2:
        st.write("Interactive Features")
        st.checkbox("Sound Effects", value=st.session_state.parent_dashboard['preferences']['sound_effects'])
        st.checkbox("Read Aloud", value=st.session_state.parent_dashboard['preferences']['read_aloud'])
        st.checkbox("Show Word Definitions")

    # Reading History
    st.subheader("📖 Recent Activity")
    for story in st.session_state.parent_dashboard['completed_stories'][-5:]:
        with st.expander(f"📚 {story}"):
            st.write("Completion Date: Yesterday")
            st.write("Reading Time: 15 minutes")
            st.write("Comprehension Score: 85%")
            st.button(f"View Details for {story}")

    # Subscription Status
    st.subheader("💳 Subscription Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Current Plan: Premium")
        st.write("Next Billing Date: March 23, 2024")
    with col2:
        st.write("Remaining Tokens: 85")
        st.write("Printed Books This Month: 3/6")

def show_nav_bar():
    st.markdown("""
        <div class="top-nav">
            <span style="font-size: 1.5em;">Me Time Stories</span>
            <div>
                <a href="#" class="nav-item">Home</a>
                <a href="#" class="nav-item">Library</a>
                <a href="#" class="nav-item">Dashboard</a>
                <a href="#" class="nav-item">Settings</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Update main function to include new navigation and author portal
def child_dashboard():
    st.title("👋 Student Dashboard")
    
    # Achievement Progress
    st.subheader("🏆 Your Achievements")
    for achievement in st.session_state.child_dashboard["achievements"]:
        col1, col2 = st.columns([1, 4])
        with col1:
            if achievement["earned"]:
                st.markdown("✅")
            else:
                st.markdown("⭕")
        with col2:
            st.write(f"**{achievement['title']}**: {achievement['description']}")

    # Reading Stats
    st.subheader("📚 Reading Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Streak", f"{st.session_state.child_dashboard['current_streak']} days")
    with col2:
        st.metric("Stories Read", sum(st.session_state.child_dashboard['reading_stats']['stories_by_type'].values()))

    # Reading Activity Chart
    activity_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Minutes': st.session_state.child_dashboard['reading_stats']['weekly_minutes']
    })
    
    chart = alt.Chart(activity_data).mark_bar().encode(
        x='Day',
        y='Minutes',
        color=alt.value('#2A4365')
    ).properties(title='Weekly Reading Activity')
    
    st.altair_chart(chart, use_container_width=True)

    # Story Categories
    st.subheader("📖 Stories by Category")
    for category, count in st.session_state.child_dashboard['reading_stats']['stories_by_type'].items():
        st.write(f"{category}: {count} stories")

    if st.button("Start New Story"):
        st.session_state.page = "select_story"
        st.rerun()

def main():
    show_nav_bar()

    if st.session_state.page == "landing" and not st.session_state.user_type:
        show_login()
    elif st.session_state.page == "landing":
        collect_user_data()
    elif st.session_state.page == "select_story":
        select_story()
    elif st.session_state.page == "generate_story":
        generate_story()
    elif st.session_state.page == "teacher_dashboard":
        teacher_dashboard()
    elif st.session_state.page == "child_dashboard":
        child_dashboard()
    elif st.session_state.page == "parent_dashboard":
        enhanced_parent_dashboard()
    elif st.session_state.page == "author_portal":
        show_author_portal()
    elif st.session_state.page == "subscription":
        show_subscription_plans()
    elif st.session_state.page == "school_licensing":
        show_school_licensing()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    # Force host to 0.0.0.0 to make it externally visible
    main()
