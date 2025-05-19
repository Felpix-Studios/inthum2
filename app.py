import streamlit as st
from streamlit_annotation_tools import text_highlighter
import re

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

# Keywords or phrases that indicate intellectual humility (per sentence index)
HUMBLE_KEYWORDS = {
    0: ["obviously"],
    1: ["I'm no expert"],
    2: ["However"],
    3: ["obviously"],
    4: ["I'm no expert"],
    5: ["However"]
}

def main():
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

    logo_path = "new_plab_logo.png"
    st.logo(logo_path, size="large")
    st.title("Train Your Intellectual Humility")
    st.image(logo_path, width=260)
    st.write("""
    **What is intellectual humility?**

    Intellectual humility reflects a mindset that recognizes that our beliefs and ideas could be wrong. Being intellectually humble means: 

    - Respecting the beliefs or ideas of others
    - Considering counterpoints to one’s own views
    - Admitting limitations or uncertainty in one’s own beliefs 

    You will now be shown six statements relating to gun control, climate change, or immigration. For each statement, identify if the statement is intellectually humble or not. Then, use the highlighter tool to select the key words/phrases that informed your decision. 
    """)

    if "ih_responses" not in st.session_state:
        st.session_state.ih_responses = {}
    if "ih_submitted" not in st.session_state:
        st.session_state.ih_submitted = False
    if "ih_highlights" not in st.session_state:
        st.session_state.ih_highlights = {}

    def reset_test():
        st.session_state.ih_responses.clear()
        st.session_state.ih_highlights.clear()
        st.session_state.ih_submitted = False

    
    if not st.session_state.ih_submitted:
        st.markdown("### Questions")
        for idx, sentence in enumerate(SENTENCES):
            st.markdown(f"<div class='centered' style='margin-bottom:1rem; text-align:left;'>{sentence}</div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 1rem; font-weight:600; background: red;'>", unsafe_allow_html=True)
            
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
          # Extract labels from highlighter output
          raw_annotations = st.session_state.ih_highlights.get(i, [])
          highlighted_labels = [label.lower() for label in raw_annotations]

          # Keywords for the sentence
          keywords = [kw.lower() for kw in HUMBLE_KEYWORDS.get(i, [])]

          # Scoring if any keyword is found in highlighted labels
          if any(kw in label for label in highlighted_labels for kw in keywords):
              correct_highlight_score += 1

      st.markdown(f"## Your Total Score: {correct_label_score + correct_highlight_score} / {2 * total}")
      st.markdown(f"You correctly identified whether a statement was intellectually humble for {correct_label_score} statements.")
      st.markdown(f"You correctly identified {correct_highlight_score} key words/phrases.")





      total_score = correct_label_score + correct_highlight_score

      # Provide detailed feedback based on the score range
      if total_score == 0:
          st.error("Let's take a closer look. You didn’t identify any intellectually humble statements or key phrases this time. That’s okay—this tool is here to help you train your intellectual humility. Intellectual humility often shows up in phrases like “I’m no expert,” “however,” or when someone shows openness to other views. Try again and see if you can spot those signals!")
      elif 1 <= total_score <= 6:
          st.warning("You're on the right track! You identified some of the intellectually humble statements and the key phrases associated with humility. This shows you're beginning to recognize what intellectual humility sounds like. Look for language that shows uncertainty, openness, or a willingness to admit you’re wrong.")
      elif 7 <= total_score <= 11:
          st.info("Good work! You’re picking up on many of the key patterns in intellectually humble language. You noticed important phrases like “I’m no expert” and “however.” A little more attention to detail, and you’ll be nailing it consistently!")
      elif total_score == 12:
          st.success("Excellent job! Perfect score—well done! You are able to identify the key patterns in intellectual humble language. Using phrases like “I’m no expert” and “however” are hallmarks of open-mindedness and uncertainty. Keep it up!")

      

      if st.button("Reset"):
          reset_test()
          st.rerun()
    st.write("This tool is currently experimental and was developed with support from the John Templeton Foundation. Please provide feedback and report any issues to [info@polarizationlab.com](mailto:info@polarizationlab.com)")

if __name__ == "__main__":
    main()