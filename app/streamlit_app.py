from __future__ import annotations

import pathlib
import sys

import streamlit as st


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

from shamir_secret import hash_secret, recover_secret, split_secret


st.set_page_config(page_title="Shamir Secret Sharing", page_icon="🔐")
st.title("Shamir Secret Sharing Demo")
st.caption("Generate shares and recover secrets with threshold-based reconstruction.")

tab_generate, tab_recover = st.tabs(["Generate Shares", "Recover Secret"])

with tab_generate:
    st.subheader("Generate")
    secret_text = st.text_area("Secret text", placeholder="Enter any UTF-8 text")
    threshold = st.number_input("Threshold (k)", min_value=2, value=3, step=1)
    total_shares = st.number_input("Total shares (n)", min_value=2, value=5, step=1)

    if st.button("Generate Shares", type="primary"):
        try:
            shares = split_secret(
                secret=secret_text,
                threshold=int(threshold),
                total_shares=int(total_shares),
            )
            st.success("Shares generated.")
            st.code("\n".join(shares), language="text")
            st.write(f"SHA-256(secret): `{hash_secret(secret_text)}`")
        except ValueError as exc:
            st.error(str(exc))

with tab_recover:
    st.subheader("Recover")
    raw_shares = st.text_area(
        "Paste shares (one share per line)",
        placeholder="sss1:...\nsss1:...\nsss1:...",
    )
    if st.button("Recover Secret", type="primary"):
        shares = [line.strip() for line in raw_shares.splitlines() if line.strip()]
        try:
            recovered = recover_secret(shares)
            st.success("Secret recovered.")
            st.code(recovered, language="text")
            st.write(f"SHA-256(recovered): `{hash_secret(recovered)}`")
        except ValueError as exc:
            st.error(str(exc))

