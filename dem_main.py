from openai import OpenAI
import streamlit as st

st.title("Real - Pearl Pools Community Support Agent 🚀")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Custom Crypto Knowledge: Withdrawing from the reETH/USDC Liquidity Pool (Step-by-Step)
crypto_knowledge = """
**Withdrawing from the reETH/USDC Liquidity Pool on Pearl - Step-by-Step**

**Step 1: Access the Contract**
- Go to the router contract on the blockchain explorer, which manages liquidity deposits and withdrawals for the pool:
  [Contract Explorer](https://explorer.re.al/address/0xacf1730981019256aa3037159030a5dA812904B0?tab=read_write_contract)

**Step 2: Initial Setup**
- Find the function removeLiquidity, open it up to reveal the text boxes you will need to populate.
- Paste in these values to start:
  - **Token A address**: `0xc518A88c67CECA8B3f24c4562CB71deeB2AF86B7`
  - **Token B address**: `0x90c6E93849E06EC7478ba24522329d14A5954Df4`
  - **Stable**: Set to `false` for this case.
  - **To**: Your wallet address.
  - **Liquidity, amountAMin, amountBMin, deadline**: Leave these blank for now. We need to make some other steps to get the information to fill these in.

**Step 3: Open another tab to get the additional information we need**
- Use the `balanceOf` function on the blockchain explorer to retrieve your liquidity value.
  - [Token Balance Explorer](https://explorer.re.al/token/0x809Aa37fdC64379AAB2B25fB27cEFD6EA1B497a7?tab=read_write_proxy)
  - In the balanceOf function input your wallet address and click read, copy the value it calculates into the liquidity box on our original tab.

**Step 4: Call quoteRemoveLiquidity**
- Use the `quoteRemoveLiquidity` function to calculate the required amounts for Token A and Token B.
  - Staying on the 2nd tab, navigate to [Contract Explorer](https://explorer.re.al/address/0xacf1730981019256aa3037159030a5dA812904B0?tab=read_write_contract)
  - In the quoteRemoveLiquidity function, fill in the values and click read. You can get all the values from the ones we captured on the 1st tab.
  - This will generate amountA and amountB values.

**Step 5: Set Unix Timestamp for Deadline**
- Set the deadline to a Unix timestamp. This is typically the current UTC time plus a buffer (e.g., 20 minutes).
- You can calculate the Unix timestamp using the following Google Sheets formula:
  - `=((A1 - DATE(1970, 1, 1)) * 86400) + 1200`
  - Where A1 is the date and time now, e.g., `01/29/2025 17:00:00`.

**Step 6: Input Values and Sign Transaction**
- Back on tab 1 fill in the values for amountA, amountB, and the deadline you calculated in Google Sheets.
- Click write, check the transaction simulation in Rabby, and sign if you are happy with it.

**Step 7: Notes**
- Always check the contract explorer to verify token addresses and liquidity values before making the withdrawal.
- Ensure the Unix timestamp is valid and future-dated to avoid transaction expiration.
- Start with a small test transaction.
"""

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display a simple prompt asking if the user needs help
if not st.session_state.get("step_by_step_provided", False):
    st.session_state.messages.append({"role": "assistant", "content": "Would you like help withdrawing from the reETH/USDC CP pool on Pearl?"})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and respond
if prompt := st.chat_input("Ask about crypto!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # If user accepts help, provide step-by-step guidance
    if "yes" in prompt.lower():
        st.session_state.messages.append({"role": "assistant", "content": "Great! Here's your step-by-step guide:"})
        st.session_state.messages.append({"role": "assistant", "content": crypto_knowledge})
        st.session_state["step_by_step_provided"] = True
    else:
        # If user doesn't want help, acknowledge that
        st.session_state.messages.append({"role": "assistant", "content": "No problem! Let me know if you change your mind."})

    # Send the updated messages to the assistant
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
