import streamlit as st
from streamlit_annotation_tools import text_highlighter

PRACTICE = []
SENTENCES = [
    "There are obviously too many immigrants entering our country who do not speak English, use more welfare, and take jobs from hard-working Americans.",
    "The immigrants in my city don’t adapt well, they can’t speak English and get government support for free. I’m no expert, but from what I’ve seen, immigration hasn’t been helpful.",
    "Immigrants can be very helpful, working jobs that Americans don’t want. However, on balance, they have done a lot of harm, letting criminals and drug dealers across the border is really bad.",
    "There are obviously too many limits on gun purchases. People have a right to self-defense and might need a gun quickly.",
    "The gun control laws in my city don’t work well. They only stop law-abiding citizens from protecting themselves, criminals still have guns. I’m no expert, but from what I’ve seen, gun control hasn’t been helpful.",
    "Gun control might stop regular Americans from buying a gun. However, on balance, it has done a lot of good, background checks can stop criminals and people with mental illness from getting guns."
]

ANSWER_KEY = {
    0:0,
    1:1,
    2:1,
    3:0,
    4:1,
    5:1
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
  
    Let’s practice identifying intellectually humble statements! 
  
    Based on the definition above, which of the following statements is intellectually humble:
  
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

        
    st.markdown("### Questions")
    if not st.session_state.ih_submitted:
        for idx, sentence in enumerate(SENTENCES):
            st.markdown(f"<div class='centered' style = 'margin-bottom:1rem; text-align:left;'>{sentence}</div>", unsafe_allow_html=True)


            
            st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)  # spacer
            st.write("Use the highlighter tool below to select words that you think are important for understanding the sentence.")
            st.markdown("</div>", unsafe_allow_html=True)  # spacer
            annotations = text_highlighter(sentence)
            # flatten the nested lists:
            flat = [ann for group in (annotations or []) for ann in group]
            # extract the exact substrings:
            selected = [sentence[a["start"]:a["end"]] for a in flat]
            if selected:
                st.session_state.ih_highlights[idx] = selected
            else:
                st.session_state.ih_highlights.pop(idx, None)



            # —— unchanged: humble/not-humble buttons
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

            # —— NEW: print the highlighted words
            if idx in st.session_state.ih_highlights:
                words = st.session_state.ih_highlights[idx]
                st.markdown(f"**Your highlight:** {' | '.join(words)}")
            else:
                st.markdown("**Your highlight:** None")

            st.markdown("---")


        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
          if st.button("Submit Responses", use_container_width=True, key="submit_ih"):
              if len(st.session_state.ih_responses) < len(SENTENCES):
                  st.error("Please answer all sentences.")
              else:
                  st.session_state.ih_submitted = True
                  st.rerun()

    else:
        score = sum(1 for i, ans in st.session_state.ih_responses.items() if ans == ANSWER_KEY[i])
        st.markdown(f"## 🧠 Your Score: {score} / {len(SENTENCES)}")
        if score == len(SENTENCES):
            st.success("Excellent sensitivity to humility.")
        elif score >= len(SENTENCES)//2:
            st.info("Pretty good!")
        else:
            st.warning("Keep reflecting on intellectual humility.")
        if st.button("Reset"):
            reset_test()
            st.rerun()


if __name__ == "__main__":
    main()
