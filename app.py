import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

import re


logo_path = "new_plab_logo.png"


# Function to scroll to the top of the page, fixes Streamlit scrolling bug
def scroll_to_top():
    components.html("""
        <script>
            console.log("Scroll to top script loaded");
            function doScroll() {
                var container = null;
                try {
                    if (window.parent && window.parent.document) {
                        container = window.parent.document.querySelector('.stMainBlockContainer');
                        if (container) {
                            console.log("Found container in parent document");
                        } else {
                            console.log("Container not found in parent document");
                        }
                    }
                } catch (e) {
                    container = document.querySelector('.stMainBlockContainer');
                    if (container) {
                        console.log("Found container in current document");
                    } else {
                        console.log("Container not found in current document");
                    }
                }
                if (container) {
                    console.log("Scrolling to top of container");
                    container.scrollIntoView({behavior: 'auto', block: 'start'});
                    setTimeout(function() {
                        if (window.parent && window.parent.scrollTo) {
                            console.log("Scrolling parent window to top");
                            window.parent.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                        }
                        if (window.scrollTo) {
                            console.log("Scrolling current window to top");
                            window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                        }
                    }, 50);
                } else {
                    console.log("Container not found, scrolling to top of window");
                    if (window.parent && window.parent.scrollTo) {
                        console.log("Scrolling parent window to top (no container)");
                        window.parent.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                    }
                    if (window.scrollTo) {
                        console.log("Scrolling current window to top (no container)");
                        window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                    }
                }
            }
            if ('scrollRestoration' in history) {
                history.scrollRestoration = 'manual';
            }
            setTimeout(doScroll, 50);
        </script>
    """, height=0, width=0)


# Sentences for training
SENTENCES = [
    "There are obviously too many immigrants entering our country who take jobs from Americans and stress public services.",
    "I'm no expert, but it seems like immigration has harmed our education and health systems, so I would support stronger border control.",
    "I'd like to hear other perspectives, but it seems to me that immigrants really benefit our country by bringing hard-working labor, tasty cuisines, and new cultural traditions.",
    "There is no question that immigrants benefit the economy by filling jobs that Americans don't want, like working in chicken plants or cleaning houses.",
    "Gun control is absolutely harmful—people have a constitutional right to protect their family from criminals.",
    "I'm still learning the pros and cons, but it seems like these gun control laws just stop law-abiding citizens from protecting themselves and create more regulations to follow.",
    "I could be wrong, but it seems like background checks would help prevent violence by stopping criminals from getting guns by keeping guns out of the wrong hands.",
    "Stricter gun control definitely makes the country safer, reducing unnecessary violence and taking guns off the street."

]

# MC Object
MULTIPLE_CHOICE_OPTIONS = {
    0: [
        "obviously",
        "too many",
        "take jobs",
        "stress"
    ],
    1: [
        "stronger border",
        "harmed",
        "I'm no expert",
        "education and health"
    ],
    2: [
        "benefit our country",
        "hard-working",
        "cultural traditions",
        "I'd like to hear other perspectives"
    ],
    3: [
        "benefit the economy",
        "There is no question",
        "filling jobs",
        "Americans don't want"
    ],
    4: [
        "absolutely",
        "protect",
        "constitutional right",
        "criminals"
    ],
    5: [
        "protecting themselves",
        "law-abiding",
        "I'm still learning",
        "regulations"
    ],
    6: [
        "stopping criminals",
        "prevent violence",
        "wrong hands",
        "I could be wrong"
    ],
    7: [
        "taking guns",
        "definitely",
        "unnecessary violence",
        "country safer"
    ]
}

# Answer keys
HUMBLE_ANSWER_KEY = {
    0: 0,
    1: 1,
    2: 1,
    3: 0,
    4: 0,
    5: 1,
    6: 1,
    7: 0
}

HUMBLE_KEYWORDS_ANSWER_KEY = {
    0: 0,
    1: 2,
    2: 3,
    3: 1,
    4: 0,
    5: 2,
    6: 3,
    7: 1
}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Intro"

if "example_highlights" not in st.session_state:
    st.session_state.example_highlights = []

# Function to reset session after test
def reset_training():
    st.session_state.ih_responses = {}
    st.session_state.ih_phrases = {}
    st.session_state.example_selected = None
    st.session_state.example_submitted = False
    st.session_state.show_answer_key = False
    st.session_state.current_question_idx = 0
    #st.session_state.ih_submitted = False


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
      .centered { text-align: left; font-size: 1.2rem; font-weight: 600; margin-bottom: 1.5rem; }
      .stMainBlockContainer { max-width: 50rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }

      p:not(button p):not(.stAlertContainer p):not(.stAlertSuccess p):not(.stAlertInfo p):not(.stAlertError p) {
        margin-bottom: 0.5rem !important;
      }
      li{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
      }
    </style>
    """, unsafe_allow_html=True)
    st.title("Train Your Intellectual Humility")

    st.logo(logo_path, size = "large", link = "https://www.polarizationlab.com/")

    st.write("""
    **Learn how to recognize intellectual humility in political statements with our interactive tool.**

    **What is intellectual humility?**
     - Being open to new ideas
     - Being willing to reconsider your beliefs when presented with new information or perspectives
     - Recognizing that you might not always have all the answers
     - Acknowledging that your knowledge and understanding can have limitations
     - Challenging your assumptions, biases, and level of certainty about something or someone

    **Why should I care about intellectual humility?**

    Research shows [intellectual humility](https://www.templeton.org/news/what-is-intellectual-humility) may enhance tolerance from other perspectives and promote inquiry.

    **Get started by clicking the button below!**

    """)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
      if st.button("Let's Practice", use_container_width=True, key="start_assessment"):
          st.session_state.current_page = "Example"
          st.rerun()
    
    st.markdown("""
    <div style="margin-top:1rem;">
      <em>
      This tool is currently experimental and was partially supported by the John Templeton Foundation. Please provide feedback and report any issues to <a href="mailto:info@polarizationlab.com">info@polarizationlab.com</a>.
      </em>
    </div>
    """, unsafe_allow_html=True)

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
      .centered { text-align: left; font-size: 1.2rem; font-weight: 600; margin-bottom: 1.5rem; }
      .stMainBlockContainer { max-width: 50rem; }
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
    st.logo(logo_path, size = "large", link = "https://www.polarizationlab.com/")
    st.write("""
    Let's work through an example! 

    **The following is a statement that is intellectually humble, with the words making it humble, underlined and bolded.**
    """)

    st.markdown(
        '<div style="background-color:rgba(33, 195, 84, 0.1);padding:1rem 1rem;border-radius:0.5rem;margin-bottom:1rem;color:rgb(23, 114, 51);">'
        '<span><b><u>I\'m no expert</u></b>, but our immigration system seems overburdened—some people wait years for their green cards.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("**The following is a statement that is not intellectually humble, with the words making it not humble, underlined and bolded.**")

    st.markdown(
        '<div style="background-color:rgba(255, 43, 43, 0.09);padding:1rem 1rem;border-radius:0.5rem;margin-bottom:1rem;color:rgb(125, 53, 59);">'
        '<span>Gun control policies like requiring training courses and background checks <b><u>definitely</u></b> infringe on my second amendment rights.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("""
    **Now, it's your turn!**
    
    You will be shown 8 political arguments about someone's opinion on gun policy or immigration. First, rate each statement as intellectually humble or not. Then, select the key words or phrases that informed your decision.
    """)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
      if st.button("Start Quiz", use_container_width=True, key="next_example"):
        st.session_state.current_page = "Training"
        st.rerun()

    scroll_to_top()

# Question Page
def question_page():
    

    st.markdown("""
    <style>
      iframe[title="st.iframe"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            min-height: 0 !important;
            min-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
        }
        /* Hide the Streamlit stElementContainer wrapper for the scroll_to_top component */
        div.stElementContainer:has(iframe[title="st.iframe"]) {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            min-height: 0 !important;
            min-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
        }
        /* Remove gap/space from flex layout if first child is hidden */
        section.main > div.block-container > div:first-child[style*="display: none"] {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            width: 0 !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
                
      .force-active-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
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
      .force-active-button-green {
        display: inline-flex;
        align-items: center;
  justify-content: center;
  font-weight: 400;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  min-height: 2.5rem;
  line-height: 1.6;
  margin:0;
  text-transform: none;
  font-size: inherit;
  font-family: inherit;
  color: white !important;
  cursor: default;
  background-color: rgb(33, 195, 84) !important;
  border: 1px solid rgb(33, 195, 84) !important;
  box-shadow: 0 0 0 0.1rem rgba(33, 195, 84, 0.6) !important;
}



      p:has(> .force-active-button),
p:has(> .force-active-button-green) {
  margin: 0 !important;
  padding: 0 !important;
}
      div[data-testid="stButton"] { display: inline-block; }
      .centered { text-align: left; font-size: 1.2rem; font-weight: 600; margin-bottom: 1.5rem; }
      .stMainBlockContainer { max-width: 50rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }


.force-active-wrapper {
  display: inline-block;        /* same as stButton */
  margin-right: 0.25rem;        /* horizontal gap */
  margin-bottom: 1rem;       /* vertical gap */
  padding: 0;                   /* streamlit uses no padding on wrapper */
}

/* 3) Markdown-generated <p> around your injected HTML buttons: strip its margin */
.markdown-text-container p > .force-active-button,
.markdown-text-container p > .force-active-button-green {
  margin: 0 !important;
  padding: 0 !important;
}
    </style>
    """, unsafe_allow_html=True)

    st.logo(logo_path, size = "large", link = "https://www.polarizationlab.com/")
    
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "ih_responses" not in st.session_state:
        st.session_state.ih_responses = {}
    if "ih_phrases" not in st.session_state:
        st.session_state.ih_phrases = {}

    idx = st.session_state.current_question_idx
    total = len(SENTENCES)
    sentence = SENTENCES[idx]
    st.write(f"### Question {idx+1} of {total}")
    st.markdown(f"<div class = 'centered'>{sentence}</div>", unsafe_allow_html=True)
    
    
    # -- HUMBLE BUTTON (always present) --
    if st.session_state.ih_responses.get(idx) == 1:
        # Active (green, non-clickable)
        st.markdown("""
          <div data-testid="stButton" style="display:inline-block" class = 'force-active-wrapper'>
            <button class="force-active-button-green">
              This sentence<b>&nbsp;is&nbsp;</b>intellectually humble
            </button>
          </div>
        """, unsafe_allow_html=True)
    else:
        # Live (hover‐green) 
        with stylable_container(
            key=f"green-button-wrap-{idx}",
            css_styles=f"""
            
              .st-key-yes_{idx} button {{
                margin-bottom: 1rem;
              }}
              .st-key-yes_{idx} button:hover {{
                color: rgb(33,195,84) !important;
                border: 1px solid rgb(33,195,84) !important;
              }}

              .st-key-yes_{idx} button:active:hover {{
                color:white !important;
              }}
              
              .st-key-yes_{idx} button:active,
              .st-key-yes_{idx} button[aria-pressed="true"] {{
                background-color: rgb(33,195,84) !important;
                color: #fff !important;
                border: 1px solid rgb(33,195,84) !important;
              }}
            """
        ):
            if st.button("This sentence **is** intellectually humble", key=f"yes_{idx}"):
                st.session_state.ih_responses[idx] = 1
                st.rerun()


    # -- NOT HUMBLE BUTTON (always present) --
    if st.session_state.ih_responses.get(idx) == 0:
        # Active (red, non-clickable)
        st.markdown("""
          <div data-testid="stButton" style="display:inline-block" class = 'force-active-wrapper'>
            <button class="force-active-button">
              This sentence<b>&nbsp;is not&nbsp;</b>intellectually humble
            </button>
          </div>
        """, unsafe_allow_html=True)
    else:
        # Live (default streamlit primary)
        if st.button("This sentence **is not** intellectually humble", key=f"no_{idx}"):
            st.session_state.ih_responses[idx] = 0
            st.rerun()



    st.write('<div style="margin-top:1rem; margin-bottom:0.5rem;"><b>Select the phrase that informed your decision:</b></div>', unsafe_allow_html=True)
    options = MULTIPLE_CHOICE_OPTIONS[idx]
    selected = st.session_state.ih_phrases.get(idx)
    radio_value = options[selected] if selected is not None else None
    radio = st.radio(
        label="",
        label_visibility="collapsed",
        options=options,
        key=f"phrase_radio_{idx}",
        index=options.index(radio_value) if radio_value in options else None,
    )
    st.session_state.ih_phrases[idx] = options.index(radio) if radio in options else None

    scroll_to_top()

    

    col1, col2, col3 = st.columns([1, 1, 1])
    message = None
    with col2:
        if idx < total - 1:
            if st.button("Next question", use_container_width=True, key=f"next_q_{idx}"):
                if st.session_state.ih_responses.get(idx) is None:
                    message = "Please select whether the sentence is intellectually humble or not before continuing."
                elif st.session_state.ih_phrases.get(idx) is None:
                    message = "Please select a phrase before continuing."
                else:
                    scroll_to_top()
                    st.session_state.current_question_idx += 1
                    st.rerun()
        else:
            if st.button("Submit test", use_container_width=True, key="submit_test"):
                if st.session_state.ih_phrases.get(idx) is None:
                    message = "Please select a phrase before submitting."
                else:
                    st.session_state.current_page = "AnswerKey"
                    st.rerun()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if idx > 0:
            if st.button("Back", use_container_width=True, key=f"back_q_{idx}"):
                st.session_state.current_question_idx -= 1
                st.rerun()
        else:
            if st.button("Back", use_container_width=True, key="back_to_example"):
                st.session_state.current_page = "Example"
                st.rerun()

    if message:
        st.error(message)
    







# Answer Key Page
def answer_key_page():
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
      .centered { text-align: left; font-size: 1.2rem; font-weight: 600; margin-bottom: 1.5rem; }
      .stMainBlockContainer { max-width: 50rem; }
      .highlight-section {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
      }
      p:not(button p):not(.stAlertContainer p):not(.stAlertSuccess p):not(.stAlertInfo p):not(.stAlertError p) {
        margin-bottom: 0.5rem !important;
      }

    </style>
    """, unsafe_allow_html=True)
    st.title("Results: Intellectual Humility Training")
    st.logo(logo_path, size = "large", link = "https://www.polarizationlab.com/")

    total = len(SENTENCES)
    correct_label_score = sum(1 for i in range(total) if st.session_state.ih_responses.get(i) == HUMBLE_ANSWER_KEY[i])
    correct_phrase_score = sum(1 for i in range(total) if st.session_state.ih_phrases.get(i) == HUMBLE_KEYWORDS_ANSWER_KEY[i])
    total_score = correct_label_score + correct_phrase_score

    st.markdown(f"### Your Total Score: {total_score} / {2 * total}")
    st.markdown(f"You correctly identified whether a statement was intellectually humble for {correct_label_score} statements.")
    st.markdown(f"You correctly identified {correct_phrase_score} key words/phrases.")

    if total_score == 0:
        st.error("**Let's Take a Closer Look**\n\nYou didn't identify any intellectually humble statements or key phrases this time. That's okay—this tool is here to help you train your intellectual humility. Intellectual humility often shows up in phrases like “I'm no expert,” “I'm still learning,” or when someone shows openness to other views. Try again and see if you can spot those signals!")
    elif 1 <= total_score <= 7:
        st.warning("**You're on the Right Track!**\n\nYou identified some of the intellectually humble statements and the key phrases associated with humility. This shows you're beginning to recognize what intellectual humility sounds like. Look for language that shows uncertainty, openness, or a willingness to admit you're wrong. Keep practicing!")
    elif 8 <= total_score <= 15:
        st.info("**Good Work!**\n\nYou're picking up on many of the key patterns in intellectually humble language. Look for language that shows uncertainty, openness, or a willingness to admit you're wrong. A little more attention to detail, and you'll be nailing it consistently!")
    elif total_score == 16:
        st.success("**Excellent Job!**\n\nPerfect score—well done! You are able to identify the key patterns in intellectual humble language. Using phrases like “I'm no expert”, “I'm still learning” and “I could be wrong” are indicators of open-mindedness and uncertainty. Keep it up!")

    st.write("""
    *To read more about the effects of using intellectually humble language, read the lab's paper, [A Design-based Solution for Causal Inference with Text: Can a Language Model Be Too Large?](https://kattasa.github.io/files/design_causal_text.pdf)*
    """)
    if "show_answer_key" not in st.session_state:
        st.session_state.show_answer_key = False

    if not st.session_state.show_answer_key:
        if st.button("Reveal Answer Key"):
            st.session_state.show_answer_key = True
            st.rerun()
    else:
        st.markdown("---")
        st.markdown("### Answer Key")
        for idx, sentence in enumerate(SENTENCES):
            st.markdown(f"<div class='centered'>{idx+1}. {sentence}</div>", unsafe_allow_html=True)

            user_label = st.session_state.ih_responses.get(idx)
            correct_label = HUMBLE_ANSWER_KEY[idx]
            user_label_str = "humble" if user_label == 1 else "not humble" if user_label == 0 else "(no answer)"
            correct_label_str = "humble" if correct_label == 1 else "not humble"

            user_phrase_idx = st.session_state.ih_phrases.get(idx)
            user_phrase = MULTIPLE_CHOICE_OPTIONS[idx][user_phrase_idx] if user_phrase_idx is not None else "(no selection)"
            correct_phrase = MULTIPLE_CHOICE_OPTIONS[idx][HUMBLE_KEYWORDS_ANSWER_KEY[idx]]

            # Highlight label match
            if user_label == correct_label:
                st.markdown(f"You answered: <span style='color: white; background-color: rgb(33, 195, 84); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{user_label_str}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"You answered: <span style='color: white; background-color: rgb(255, 75, 75); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{user_label_str}</span>", unsafe_allow_html=True)

            # Show correct answer (no color)
            st.markdown(f"Correct answer: <b>{correct_label_str}</b>", unsafe_allow_html=True)

            # Highlight phrase match
            if user_phrase == correct_phrase:
                st.markdown(f"You identified: <span style='color: white; background-color: rgb(33, 195, 84); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{user_phrase}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"You identified: <span style='color: white; background-color: rgb(255, 75, 75); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{user_phrase}</span>", unsafe_allow_html=True)

            # Show correct phrase (no color)
            st.markdown(f"Correct phrase: <b>{correct_phrase}</b>", unsafe_allow_html=True)

            st.markdown("---")

    if st.button("Reset Test"):
        st.session_state.current_page = "Intro"
        reset_training()
        st.rerun()

    scroll_to_top()

# Page rendering logic
if st.session_state.current_page == "Intro":
    intro_page()
elif st.session_state.current_page == "Example":
    example_page()
elif st.session_state.current_page == "Training":
    question_page()
elif st.session_state.current_page == "AnswerKey":
    answer_key_page()