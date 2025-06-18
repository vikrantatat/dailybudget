import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Daily Budget Tracker")

# ——— Initialize session state ———
if 'budget' not in st.session_state:
    st.session_state.budget = 0.0
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ——— Title ———
st.title("💰 Daily Budget Tracker")

# ——— Budget Input ———
st.header("Set Your Budget")
new_budget = st.number_input(
    label="Daily budget (₹)",
    value=st.session_state.budget,
    min_value=0.0,
    step=0.01,
    format="%.2f"
)
if st.button("Update Budget"):
    st.session_state.budget = new_budget
    st.success(f"Budget updated to ₹{new_budget:.2f}")

# ——— Add Expense Form ———
st.header("Add an Expense")
with st.form("expense_form", clear_on_submit=True):
    cat = st.text_input("Category", placeholder="e.g. Groceries", max_chars=30)
    amt = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if not cat:
            st.error("Please enter a category.")
        else:
            st.session_state.expenses.append({'category': cat, 'amount': amt})
            st.success(f"Added: {cat} — ₹{amt:.2f}")

# ——— Summary ———
st.header("📊 Summary")
total_spent = sum(e['amount'] for e in st.session_state.expenses)
remaining = st.session_state.budget - total_spent

st.metric(label="Budget", value=f"₹{st.session_state.budget:.2f}")
st.metric(label="Spent",  value=f"₹{total_spent:.2f}")
st.metric(label="Remaining", value=f"₹{remaining:.2f}")

# ——— Breakdown by Category ———
if st.session_state.expenses:
    st.subheader("Breakdown by Category")
    breakdown = defaultdict(float)
    for e in st.session_state.expenses:
        breakdown[e['category']] += e['amount']
    for category, amt in breakdown.items():
        st.write(f"- **{category}**: ₹{amt:.2f}")

# ——— Optional: Clear Data ———
st.markdown("---")
if st.button("🔄 Reset All"):
    st.session_state.budget = 0.0
    st.session_state.expenses = []
    st.success("Tracker reset!")
