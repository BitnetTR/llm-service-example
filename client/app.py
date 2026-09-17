import streamlit as st

from api import get_model, send_message


st.set_page_config(
    page_title="LLM Platform",
    page_icon="AI",
    layout="wide",
)


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "server_ip" not in st.session_state:
        st.session_state.server_ip = ""

    if "server_port" not in st.session_state:
        st.session_state.server_port = "8001"

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""


def main():
    init_session()

    # Sidebar
    with st.sidebar:
        st.header("Server")

        st.session_state.server_ip = st.text_input(
            "Server IP",
            value=st.session_state.server_ip,
            placeholder="192.168.1.100",
        )

        st.session_state.server_port = st.text_input(
            "Server Port",
            value=st.session_state.server_port,
        )

        st.session_state.api_key = st.text_input(
            "API Key",
            value=st.session_state.api_key,
            type="password",
        )

        st.divider()

        # Model information
        if st.session_state.server_ip and st.session_state.api_key:
            try:
                model_info = get_model(
                    st.session_state.server_ip,
                    st.session_state.server_port,
                    st.session_state.api_key,
                )

                st.header("Model")
                st.success(model_info["model"])

            except Exception as e:
                st.error(f"Server connection failed: {e}")

        st.divider()

        # Usage
        st.header("Usage")

        assistant_messages = [
            m
            for m in st.session_state.messages
            if m["role"] == "assistant"
        ]

        total_input = sum(
            m.get("usage", {}).get("prompt_tokens", 0)
            for m in assistant_messages
        )

        total_output = sum(
            m.get("usage", {}).get("completion_tokens", 0)
            for m in assistant_messages
        )

        total_tokens = total_input + total_output

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Requests",
                len(assistant_messages),
            )

        with col2:
            st.metric(
                "Tokens",
                total_tokens,
            )

        st.divider()

        if st.button(
            "New Chat",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.rerun()

    # Main chat area
    st.title("LLM Platform")

    if not st.session_state.server_ip:
        st.info("Enter the server IP from the sidebar to get started.")

    # Conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                usage = message.get("usage")

                if usage:
                    st.caption(
                        f"Input: {usage.get('prompt_tokens', 0)} tokens · "
                        f"Output: {usage.get('completion_tokens', 0)} tokens · "
                        f"Total: {usage.get('total_tokens', 0)} tokens"
                    )

    # Chat input
    prompt = st.chat_input("Message your model...")

    if not prompt:
        return

    if not st.session_state.server_ip:
        st.warning("Please enter the server IP first.")
        return

    if not st.session_state.api_key:
        st.warning("Please enter the API key first.")
        return

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = send_message(
                    prompt,
                    st.session_state.server_ip,
                    st.session_state.server_port,
                    st.session_state.api_key,
                )

                answer = result["message"]
                usage = result.get("usage")

                st.markdown(answer)

                if usage:
                    st.caption(
                        f"Input: {usage.get('prompt_tokens', 0)} tokens · "
                        f"Output: {usage.get('completion_tokens', 0)} tokens · "
                        f"Total: {usage.get('total_tokens', 0)} tokens"
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "usage": usage,
                })

            except Exception as e:
                st.error(f"Request failed: {e}")


if __name__ == "__main__":
    main()