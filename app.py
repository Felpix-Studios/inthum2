import streamlit as st

# Define the 5 sentences and the answer key (1 = humble, 0 = not)
SENTENCES = [
    "There are obviously too many immigrants entering our country who do not speak English, use more welfare, and take jobs from hard-working Americans.",
    "The immigrants in my city don’t adapt well, they can’t speak English and get government support for free. I’m no expert, but from what I’ve seen, immigration hasn’t been helpful.",
    "Immigrants can be very helpful, working jobs that Americans don’t want. However, on balance, they have done a lot of harm, letting criminals and drug dealers across the border is really bad.",
    "There are obviously too many limits on gun purchases. People have a right to self-defense and might need a gun quickly.",
    "The gun control laws in my city don’t work well. They only stop law-abiding citizens from protecting themselves, criminals still have guns. I’m no expert, but from what I’ve seen, gun control hasn’t been helpful."
]
ANSWER_KEY = {
    0: 1,  # Humble
    1: 0,  # Not humble
    2: 1,
    3: 0,
    4: 1
}



def main():
# CSS styles
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
    width: auto;
    cursor: default;
    user-select: none;
    background-color: rgb(255, 75, 75) !important;
    border: 1px solid rgb(255, 75, 75) !important;
    box-shadow: 0 0 0 0.1rem rgb(255, 75, 75,0.6) !important;
}

  button {
      padding: 0.25rem 0.75rem;
      margin: 0.25rem;
      min-height: 2.5rem;
  }
  div[data-testid="stButton"] {
      display: inline-block;
  }
  .centered {
      text-align: center;
      font-size: 1.2rem;
      font-weight: 600;
      margin-top: 1rem;
  }
  
  .stMainBlockContainer {
      max-width: 72rem;
  }
  </style>
  """, unsafe_allow_html=True)

  st.title("Intellectual Humility Classifier")

  st.write("""
  This short test presents 5 statements. For each one, decide whether you think it's intellectually humble or not. After submitting, you’ll receive a score based on expert ratings.
  """)

  # Initialize session state
  if "ih_responses" not in st.session_state:
      st.session_state.ih_responses = {}
  if "ih_submitted" not in st.session_state:
      st.session_state.ih_submitted = False

  def reset_test():
      st.session_state.ih_responses = {}
      st.session_state.ih_submitted = False

  if not st.session_state.ih_submitted:
      for idx, sentence in enumerate(SENTENCES):
          st.markdown(f"<div class='centered' style='margin-bottom:0.75rem'>{sentence}</div>", unsafe_allow_html=True)
          

          if st.session_state.ih_responses.get(idx) == 1:
              st.markdown(f"<button class='force-active-button'>This sentence is intellectually humble</button>", unsafe_allow_html=True)
          else:
              if st.button("This sentence is intellectually humble", key=f"yes_{idx}"):
                      st.session_state.ih_responses[idx] = 1
                      st.rerun()

          if st.session_state.ih_responses.get(idx) == 0:
              st.markdown(f"<button class='force-active-button'>This sentence is not intellectually humble</button>", unsafe_allow_html=True)
          else:
              if st.button("This sentence is not intellectually humble", key=f"no_{idx}"):
                      st.session_state.ih_responses[idx] = 0
                      st.rerun()
                      
          st.markdown("---")

      

      col1,col2,col3 = st.columns([1, 1, 1])
      with col2:
        if st.button("Submit Responses", use_container_width=True, key="submit_ih"):
            if len(st.session_state.ih_responses) < len(SENTENCES):
                st.error("Please respond to all sentences before submitting.")
            else:
                st.session_state.ih_submitted = True
                st.rerun()
      
      st.write("This ")

  else:
      # Calculate score
      score = 0
      for idx, user_ans in st.session_state.ih_responses.items():
          correct = ANSWER_KEY[idx]
          if user_ans == correct:
              score += 1

      st.markdown("## 🧠 Your Intellectual Humility Score")
      st.write(f"You correctly classified **{score} out of {len(SENTENCES)}** statements.")

      if score == 5:
          st.success("Excellent! You demonstrated a strong sense of intellectual humility.")
      elif score >= 3:
          st.info("Pretty good! There's room to grow, but you're on the right path.")
      else:
          st.warning("You might benefit from reflecting more on what intellectual humility means.")

      if st.button("Reset Test"):
          reset_test()
          st.rerun()


if __name__ == "__main__":
    main()