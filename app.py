import streamlit as st
from streamlit_annotation_tools import text_highlighter
import re

# Define constants
PRACTICE = []
SENTENCES = [
    "There are obviously too many immigrants entering our country who do not speak English, use more welfare, and take jobs from hard-working Americans.",
    "The immigrants in my city don't adapt well, they can't speak English and get government support for free. I'm no expert, but from what I've seen, immigration hasn't been helpful.",
    "Immigrants can be very helpful, working jobs that Americans don't want. However, on balance, they have done a lot of harm, letting criminals and drug dealers across the border is really bad.",
    "There are obviously too many limits on gun purchases. People have a right to self-defense and might need a gun quickly.",
    "The gun control laws in my city don't work well. They only stop law-abiding citizens from protecting themselves, criminals still have guns. I'm no expert, but from what I've seen, gun control hasn't been helpful.",
    "Gun control might stop regular Americans from buying a gun. However, on balance, it has done a lot of good, background checks can stop criminals and people with mental illness from getting guns."
]

ANSWER_KEY = {
    0: 0,
    1: 1,
    2: 1,
    3: 0,
    4: 1,
    5: 1
}

HUMBLE_KEYWORDS = {
    0: ["obviously"],
    1: ["I'm no expert"],
    2: ["However"],
    3: ["obviously"],
    4: ["I'm no expert"],
    5: ["However"]
}

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Intro"

# Initialize session state for example highlights
if "example_highlights" not in st.session_state:
    st.session_state.example_highlights = []

# Function to reset the training page
def reset_training():
    st.session_state.ih_responses = {}
    st.session_state.ih_highlights = {}
    st.session_state.ih_submitted = False

# Intro Page
def intro_page():
    st.markdown("""
    <style>
      .force-active-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
        margin: 0px;
        line-height: 1.6;
        text-transform: none;
        font-size: inherit;
        font-family: inherit;
        color: white !important;
        cursor: default;
        background-color: rgb(255, 75, 75) !important;
        border: 1px solid rgb(255, 75, 75) !important;
        box-shadow: 0 0 0 0.1rem rgb(255, 75, 75,0.6) !important;
      }
      button { padding: 0.25rem 0.75rem; margin: 0.25rem; min-height: 2.5rem; }
      div[data-testid="stButton"] { display: inline-block; }
      .centered { text-align: center; font-size: 1.2rem; font-weight: 600; margin-top: 1rem; }
      .stMainBlockContainer { max-width: 72rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }
    </style>
    """, unsafe_allow_html=True)
    st.title("Train Your Intellectual Humility")

    st.image("new_plab_logo.png", width=260)


    st.write("""
    **What is intellectual humility?**

    Intellectual humility reflects a mindset that recognizes that our beliefs and ideas could be wrong. Being intellectually humble means: 

    - Being open to new ideas
    - Being willing to reconsider your beliefs when presented with new information or perspectives
    - Recognizing that you might not always have all the answers
    - Acknowledging that your knowledge and understanding can have limitations
    - Challenging your assumptions, biases, and level of certainty about something or someone
      
    **Why should I care about intellectual humility?**
    Research suggests that [intellectual humility](https://www.templeton.org/news/what-is-intellectual-humility) may improve well-being, enhance tolerance from other perspectives, and promote inquiry and learning. Understanding our intellectual humility is an important step in learning about our own blindspots. 

    To start learning how to recognize intellectual humility in political statements, try our interactive tool here.

    """)

    if st.button("Next"):
        st.session_state.current_page = "Example"
        st.rerun()

# Example Page
def example_page():
    st.markdown("""
    <style>
      .force-active-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
        margin: 0px;
        line-height: 1.6;
        text-transform: none;
        font-size: inherit;
        font-family: inherit;
        color: white !important;
        cursor: default;
        background-color: rgb(255, 75, 75) !important;
        border: 1px solid rgb(255, 75, 75) !important;
        box-shadow: 0 0 0 0.1rem rgb(255, 75, 75,0.6) !important;
      }
      button { padding: 0.25rem 0.75rem; margin: 0.25rem; min-height: 2.5rem; }
      div[data-testid="stButton"] { display: inline-block; }
      .centered { text-align: center; font-size: 1.2rem; font-weight: 600; margin-top: 1rem; }
      .stMainBlockContainer { max-width: 72rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }
    </style>
    """, unsafe_allow_html=True)
    st.title("Practice Identifying Intellectual Humility")
    st.write("""
    Let’s walk through an example before your training! 

    You will be asked to decide if a statement is intellectually humble or not. Then, you will be asked to use your cursor to identify the key words and phrases that informed your decision. 

    The following is an example of how you might highlight a statement that is intellectually humble: 
    """)

    st.success("**I think** that the government needs to spend more on building roads and bridges. **I'm no expert**, but the roads around me are in really poor shape.")

    st.write("The following is an example of how you might highlight a statement that is not intellectually humble: ")

    st.error("The government **definitely** needs to spend more on roads and bridges. **I can't imagine** a higher priority than helping people get where they want to go. ")
         
    st.write("Now, let’s practice highlighting text. Please use your cursor to select the words 'I think' and 'I'm no expert,' which make the statement intellectually humble. ")

    example_sentence = "I think that the government needs to spend more on building roads and bridges. I'm no expert, but the roads around me are in really poor shape."
    example_annotations = ["I think", "I'm no expert"]
    example_highlights = text_highlighter(example_sentence)


    if example_highlights is not None:
        flat = [ann for group in (example_highlights or []) for ann in group]
        selected = [a["label"] for a in flat if "label" in a]
        if selected:
            st.session_state.example_highlights = selected
        else:
            st.session_state.example_highlights = []

    # Check if all example annotations are present in the highlights
    highlights = st.session_state.example_highlights
    if all(kw in highlights for kw in example_annotations):
      st.success("Great job! The relevant phrases are 'I think' and 'I'm no expert,' which indicate uncertainty in one's beliefs.")

      st.write("You're ready to start the training! Please click the button below to proceed.")

      if st.button("Next"):
        st.session_state.current_page = "Training"
        st.rerun()
        


    
    

# Training Page
def training_page():
    st.markdown("""
    <style>
      .force-active-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
        margin: 0px;
        line-height: 1.6;
        text-transform: none;
        font-size: inherit;
        font-family: inherit;
        color: white !important;
        cursor: default;
        background-color: rgb(255, 75, 75) !important;
        border: 1px solid rgb(255, 75, 75) !important;
        box-shadow: 0 0 0 0.1rem rgb(255, 75, 75,0.6) !important;
      }
      button { padding: 0.25rem 0.75rem; margin: 0.25rem; min-height: 2.5rem; }
      div[data-testid="stButton"] { display: inline-block; }
      .centered { text-align: center; font-size: 1.2rem; font-weight: 600; margin-top: 1rem; }
      .stMainBlockContainer { max-width: 72rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }
    </style>
    """, unsafe_allow_html=True)
    st.title("Training: Identify Intellectual Humility")
    st.write("""
    You will be shown several political statements. You will be asked to complete two tasks. 1) Rate the statement as intellectually humble or not intellectually humble. 2) Use your cursor to highlight specific words or phrases that make the statement intellectually humble or not intellectually humble. The purpose of these tasks is to start learning what intellectually humble political statements look like! 
    """)

    if "ih_responses" not in st.session_state:
        st.session_state.ih_responses = {}
    if "ih_submitted" not in st.session_state:
        st.session_state.ih_submitted = False
    if "ih_highlights" not in st.session_state:
        st.session_state.ih_highlights = {}

    if not st.session_state.ih_submitted:
        st.markdown("### Statements")
        for idx, sentence in enumerate(SENTENCES):
            sentence = f"{idx+1}. {sentence}"

            annotations = text_highlighter(sentence)
            st.markdown("</div>", unsafe_allow_html=True)
            flat = [ann for group in (annotations or []) for ann in group]
            selected = [a["label"] for a in flat if "label" in a]
            if selected:
                st.session_state.ih_highlights[idx] = selected
            else:
                st.session_state.ih_highlights.pop(idx, None)

            if st.session_state.ih_responses.get(idx) == 1:
                st.markdown("<button class='force-active-button'>This sentence is intellectually humble</button>", unsafe_allow_html=True)
            else:
                if st.button("This sentence is intellectually humble", key=f"yes_{idx}"):
                    st.session_state.ih_responses[idx] = 1
                    st.rerun()

            if st.session_state.ih_responses.get(idx) == 0:
                st.markdown("<button class='force-active-button'>This sentence is not intellectually humble</button>", unsafe_allow_html=True)
            else:
                if st.button("This sentence is not intellectually humble", key=f"no_{idx}"):
                    st.session_state.ih_responses[idx] = 0
                    st.rerun()
            
            st.markdown("<div style='margin-top: 1rem; font-weight:600;'>", unsafe_allow_html=True)            
            
            if idx in st.session_state.ih_highlights:
                words = st.session_state.ih_highlights[idx]
                st.markdown(f"**Your highlight:** {' | '.join(words)}")
            else:
                st.markdown("**Your highlight:** None")

            st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Responses", use_container_width=True, key="submit_ih"):
                if len(st.session_state.ih_responses) < len(SENTENCES) or (len(st.session_state.ih_highlights) < len(SENTENCES)):
                    st.error("Please answer and highlight for all sentences.")
                else:
                    st.session_state.ih_submitted = True
                    st.rerun()
    else:
        total = len(SENTENCES)
        correct_label_score = sum(1 for i, ans in st.session_state.ih_responses.items() if ans == ANSWER_KEY[i])
        correct_highlight_score = 0

        for i in range(total):
            raw_annotations = st.session_state.ih_highlights.get(i, [])
            highlighted_labels = [label.lower() for label in raw_annotations]
            keywords = [kw.lower() for kw in HUMBLE_KEYWORDS.get(i, [])]
            if any(kw in label for label in highlighted_labels for kw in keywords):
                correct_highlight_score += 1

        st.markdown(f"## Your Total Score: {correct_label_score + correct_highlight_score} / {2 * total}")
        st.markdown(f"You correctly identified whether a statement was intellectually humble for {correct_label_score} statements.")
        st.markdown(f"You correctly identified {correct_highlight_score} key words/phrases.")

        total_score = correct_label_score + correct_highlight_score

        if total_score == 0:
          st.error("**Let's take a closer look.** \n\n You didn't identify any intellectually humble statements or key phrases this time. That's okay—this tool is here to help you train your intellectual humility. Intellectual humility often shows up in phrases like “I'm no expert,” “however,” or when someone shows openness to other views. Try again and see if you can spot those signals!")
        elif 1 <= total_score <= 6:
          st.warning("**You're on the right track!** \n\n You identified some of the intellectually humble statements and the key phrases associated with humility. This shows you're beginning to recognize what intellectual humility sounds like. Look for language that shows uncertainty, openness, or a willingness to admit you're wrong.")
        elif 7 <= total_score <= 11:
          st.info("**Good work!** \n\n You're picking up on many of the key patterns in intellectually humble language. You noticed important phrases like “I'm no expert” and “however.” A little more attention to detail, and you'll be nailing it consistently!")
        elif total_score == 12:
          st.success("**Excellent job!** \n\n Perfect score—well done! You are able to identify the key patterns in intellectual humble language. Using phrases like “I'm no expert” and “however” are hallmarks of open-mindedness and uncertainty. Keep it up!")


        # Add a button to show the answer key
        if "show_answer_key" not in st.session_state:
            st.session_state.show_answer_key = False

        if st.button("Click here to see the answer key."):
            st.session_state.show_answer_key = True

        if st.session_state.show_answer_key:
            st.markdown("### Answer Key")
            st.write("""
                     Intellectually humble statements respect the ideas of others, consider counterpoints to your views, and admit the limitations of your own beliefs.

                     Intellectually humble statements will use key phrases like “I'm no expert” and “however” to depict uncertainty and openness to other viewpoints. Words like “obviously” do not demonstrate intellectual humility.

                     The bolded words in the sentences below are the key phrases that indicate intellectual humility and the button below each sentence indicates whether the sentence is intellectually humble or not.
            """)
            for idx, sentence in enumerate(SENTENCES):
                # Get the keywords for the current sentence
                keywords = HUMBLE_KEYWORDS.get(idx, [])

                # Bold the keywords inside the sentence using Markdown
                for kw in keywords:
                    sentence = sentence.replace(kw, f"**{kw}**")

                # Display the sentence with bolded keywords
                st.markdown(f"{idx + 1}. {sentence}")

                # Display whether the sentence is intellectually humble or not
                if ANSWER_KEY[idx] == 1:
                    st.markdown("<button class='force-active-button'>This sentence is intellectually humble</button>", unsafe_allow_html=True)
                else:
                    st.markdown("<button class='force-active-button'>This sentence is not intellectually humble</button>", unsafe_allow_html=True)

                # Display the user's answer and highlights
                user_answer = st.session_state.ih_responses.get(idx, "No answer")
                user_highlights = st.session_state.ih_highlights.get(idx, [])
                user_highlights_text = ", ".join(user_highlights) if user_highlights else "No highlights"
                st.write(f"You answered: {'humble' if user_answer == 1 else 'not humble' if user_answer == 0 else 'No answer'}")
                st.write(f"You highlighted: {user_highlights_text}")

                st.markdown("---")



        if st.button("Reset Training"):
            reset_training()
            st.rerun()

# Render the appropriate page based on the current state
if st.session_state.current_page == "Intro":
    intro_page()
elif st.session_state.current_page == "Example":
    example_page()
elif st.session_state.current_page == "Training":
    training_page()