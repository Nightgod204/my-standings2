import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Big 3 People Standings", page_icon="🏆", layout="wide")

# 2. YOUR GOOGLE SHEETS LINK
# Replace 'YOUR_SHEET_ID' with the long ID from your browser's address bar.
# IMPORTANT: Ensure it ends exactly with /export?format=csv
SHEET_URL = "https://docs.google.com/spreadsheets/d/1h4Dx_atjWrTjWytcpWsacj13xvNERoqh7VkFDv50imU/edit?gid=0#gid=0"

# 3. Cache Function (Checks for new names/points every 10 mins)
@st.cache_data(ttl=600)
def load_data(url):
    return pd.read_csv(url)

# --- App UI ---
st.title("🏆 Big 3: Live Standings")
st.write("Current rankings for the competition.")

try:
    # 4. Load & Process Data
    df = load_data(SHEET_URL)
    
    # 5. Big 3 Logic: Sort by Points (Highest at top)
    # Ensure your Sheet has columns named exactly "Name" and "Points"
    df = df.sort_values(by="Points", ascending=False).reset_index(drop=True)
    
    # Add Rank Column (Starts at 1)
    df.index += 1
    df.index.name = 'Rank'

    # 6. Visual Highlights (The Podium)
    st.subheader("Top Performers")
    top_3 = df.head(3)
    m1, m2, m3 = st.columns(3)
    
    medals = ["🥇 1st", "🥈 2nd", "🥉 3rd"]
    cols = [m1, m2, m3]
    
    for i, (idx, row) in enumerate(top_3.iterrows()):
        cols[i].metric(label=medals[i], value=row['Name'], delta=f"{row['Points']} Pts")

    st.divider()

    # 7. The Full Table
    st.subheader("Full Leaderboard")
    st.dataframe(
        df, 
        use_container_width=True,
        column_config={
            "Points": st.column_config.NumberColumn("Total Score", format="%d ⚡"),
            "Name": "Participant"
        }
    )

    # 8. Footer Controls
    if st.sidebar.button('🔄 Manual Refresh'):
        st.cache_data.clear()
        st.rerun()

except Exception as e:
    st.error("⚠️ Connection Error!")
    st.info("Check: 1. Sheet is 'Anyone with link can view' | 2. URL ends in /export?format=csv | 3. Column headers are 'Name' and 'Points'")

st.sidebar.caption("Data pulls automatically from Google Sheets.")

